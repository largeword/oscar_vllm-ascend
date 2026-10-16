# OSCAR implementation review: calibration, INT2, and attention

This is the primary review following the user's scope clarification. The original
OSCAR code is the algorithmic reference; its hosting framework is incidental.
Paths are relative to `/home/luxinliang/hw_projects/`.

**Authoritative reference:** `/home/luxinliang/hw_projects/OSCAR/` (the parent
directory's `OSCAR` checkout). Compare its OSCAR implementation directly with
`/home/luxinliang/hw_projects/gpt_new_oscar_kimi/`. The older vLLM PR is historical
context explaining choices in the port; it does not define the migration target.
The reference entry point is `OSCAR/rotation/run/qwen3.8-27b.sh`, followed through
to its rotation fitter, artifact loader, quantization kernels, and mixed-cache
attention implementation.

## Main conclusion

**The clearest implementation gap is that the automatic Ascend PT path does not
perform OSCAR's data-dependent calibration.** It generates data-free Hadamard
matrices. The next confirmed gap is disabled clipping by default. Newer original
OSCAR also supports per-head rotations and key centering, which the port's
artifact/runtime contract cannot currently express.

These are source-confirmed differences. Their individual contributions to the
reported model-quality loss have not been measured.

## 1. PT generation and consumption

### Original calibrated OSCAR

For each FULL layer and KV head, collect aligned Q/K/V at the attention input,
after QK normalization and RoPE. For the query heads associated with KV head `h`:

```text
Cq[h] = Q_group[h]^T Q_group[h] / number_of_grouped_query_rows
w[t,h] = K[t,h]^T Cq[h] K[t,h]
Cv[h] = sum_t w[t,h] V[t,h] V[t,h]^T / sum_t w[t,h]

Rk = eigenbasis(Cq) @ H @ Pbr
Rv = eigenbasis(Cv) @ H @ Pbr
```

The older shared-layer variant averages head moments before eigendecomposition.
The newer per-head variant preserves them. The centered variant also exports
`k_mean[h]`.

Evidence:

- `OSCAR/rotation/compute_kv_rotation.py:108–159,257–311`.
- `OSCAR/python/sglang/srt/mem_cache/oscar_calibration.py:417–459,646–743`.
- `OSCAR/rotation/tools/fit_oscar2_variants.py:250–344`.

The original offline fitter uses FP64 statistics/eigensolve and saves FP32
matrices. Its CLI needs explicit `--composition r_h_pbr`; its default is `plain`.
The startup fitter emits shared-layer rotations; saving moments and running the
per-head fitter is a separate step.

### Current automatic Ascend path

```text
model config → FULL layer IDs and D → Hadamard H
                                      ↓
                            every layer: Rk=H, Rv=H
                            calibrated=False
```

`gpt_new_oscar_kimi/tools/prepare_rotations.py:55–65` only supports this automatic
method. `oscar_ascend/rotations.py:181–199` constructs it. No Q/K/V observations
are used.

The sample API in `rotations.py:221–320` implements the shared-layer moment
formula, but lacks an integrated collector, TP aggregation, and a supplied
validated production eigensolver. It uses FP32 statistics and does not export
per-head means.

### Artifact migration

The old vLLM OSCAR PR loads separate per-layer K/V files. The Ascend port loads a
combined file with named layer entries containing `Rk` and `Rv`. Its validator
requires one orthogonal `[D,D]` matrix per layer (`rotations.py:129–178`).

- **Shared orthogonal pair:** can be repackaged without changing the matrices.
- **Per-head pair:** needs global-head-aware loading and rank selection.
- **Centered pair:** additionally needs mean subtraction and consistent attention
  score/LSE handling.
- **Non-orthogonal pair:** additionally needs distinct query/output dual
  transforms; not required for an initial orthogonal migration.

Do not average fitted rotation matrices or discard companion fields to satisfy
the existing schema.

For Qwen3.8's reference geometry, TP4 gives one KV head per rank. A rank-aware
loader can therefore select one per-head matrix and retain the existing 2-D
matrix operator interface. TP2 gives two KV heads per rank and needs head-aware
rotation selection in the operators.

## 2. Clipping and INT2 numerics

| Component | Original OSCAR reference | Current Ascend port |
|---|---|---|
| Default K/V clip in referenced recipe | .96/.92 | 0/0 |
| Clip rule | absolute-value order statistic | linearly interpolated quantile |
| Rotation arithmetic | normally BF16 on this reference path | FP32 |
| Quantizer metadata | FP32 scale and zero point | FP16-rounded scale and minimum |
| Reconstruction | `(code-zero_point)*scale` | `code*scale+minimum` |
| Canonical byte layout | four quarter-separated channels | four adjacent channels |

Sources:

- `OSCAR/rotation/eval_oscar_gpqa.sh:330–348`.
- `OSCAR/python/sglang/QuantKernel/oscar_rotation_clip_int2_kv.py:109–127,181–218,387–399`.
- `gpt_new_oscar_kimi/oscar_ascend/integration/cache_storage_ops.py:49–59`.
- `gpt_new_oscar_kimi/csrc/kernels/rotate_clip_store.cpp:139–204`.

**Distinguish an algorithm choice from a porting bug.** The Ascend quantizer
largely follows the pinned vLLM OSCAR PR's contract. Its FP16 metadata and linear
quantile are not independently established implementation mistakes. However,
they differ from the current original OSCAR reference and must be isolated when
claiming parity.

The affine parameterizations are equivalent in exact arithmetic; rounding makes
their implemented results differ. Packing is accuracy-neutral if writer/reader
agree. Higher-precision rotation is not intrinsically wrong, but it can change
INT2 threshold decisions.

First enable and evaluate clipping under the chosen contract. Then compare
quantizer profiles on identical captured Q/K/V. Avoid changing metadata dtype
inside the existing cache layout: D256 K+V history uses 136 bytes with FP16
metadata and 144 bytes with FP32 metadata, requiring layout/capacity updates.

## 3. OSCAR attention correctness

### Key centering with raw windows

The current port uses transformed compressed history plus raw BF16 windows and
current K/V. If centering is added only to history, its logits shift by
`-attention_scale * dot(q_raw, k_mean)`.

Before merging history with uncentered sources, correct:

```text
LSE_history += attention_scale * dot(q_raw, k_mean)
```

The normalized history output needs no correction for this constant shift.
Alternatively, center all sources consistently. This is required for a future
centered-artifact migration; the current uncentered implementation does not
already have this particular error.

### Value inverse and output gate

History output must return through `Rv.T` to original value coordinates before
the model's elementwise output gate. A general rotation does not commute with
that gate. Preserve the port's original-space partial-output/LSE merge design.

### Cache lifecycle

The OSCAR-specific invariants to retain are:

- Exact, nonoverlapping coverage of history/window/current causal positions.
- Reading the old recent window before publishing a large new chunk.
- Preserving recent-window contents through speculative rejection.
- Matching compressed writer/reader layouts, including candidate striped formats.
- Correct physical-page versus virtual-block mapping.
- Shared-prefix snapshots remaining exact and immutable while shared.
- Padding never writing live cache rows.
- Graph replay refreshing metadata without stale per-step reuse.

Evidence: `gpt_new_oscar_kimi/docs/runtime_implementation.md:26–100` and
`oscar_ascend/integration/impl.py:215–295`.

These are review/test targets, not newly demonstrated defects in the current
cache implementation.

## 4. Migration of the reference script's OSCAR workflow

The script's relevant role is to select a PT pair, quantizer settings, and
high-precision windows. Transfer that workflow into the external plugin:

1. Accept an explicit rotation artifact or explicit calibration request.
2. Validate and use an existing artifact instead of always preparing Hadamard.
3. For calibration, collect aligned post-RoPE Q/K/V once, preserving token,
   global-layer, and global-head identity; exclude dummy/padding rows.
4. Fit shared moments with correct TP aggregation, or retain per-head moments
   for per-head fitting. Validate eigensolver residuals and transform identities.
5. Export source provenance and the supported artifact schema; publish atomically.
6. Load the correct matrices per FULL layer/rank/head.
7. Set the intended clip profile, uniform INT2, group D256, and sink/recent 64/256.
8. For centered artifacts, implement mean/LSE handling before enabling them.

Current code changes belong primarily in:

- `tools/prepare_rotations.py`: supplied-artifact handling and calibrated workflow.
- `oscar_ascend/rotations.py`: richer schema/statistics/transform validation.
- `oscar_ascend/runtime.py`: rank-aware artifact selection and persistent constants.
- `integration/cache_storage_ops.py` and rotation/store operators: clipping and
  optional mean subtraction.
- Attention partial/LSE handling: centering consistency across sources.

Calibration must use representative positions and the actual attention input
frame. Treat these as calibration provenance requirements; there is no need to
turn the review into a comparison of serving frameworks.

## 5. Accuracy investigation order

Hold the surrounding model execution fixed and compare:

1. Current Hadamard/no-clip OSCAR.
2. Same implementation with clipping enabled.
3. Shared calibrated rotations under the same quantizer.
4. Per-head calibrated rotations.
5. Per-head rotations plus correctly integrated centering.
6. Original-reference versus PR-style quantizer numerics on identical inputs.

At each step distinguish:

- **Implementation error:** Ascend operator versus an independent oracle of the
  exact chosen OSCAR contract, on identical input/cache bytes.
- **Compression error:** that OSCAR contract versus uncompressed attention and
  ultimately model logits/quality under common tokens.

Use a quantization-disabled transform/merge check first. Then measure per-head
score error, LSE, attention-output error, and teacher-forced model-logit error.
Include positions that actually read INT2 history; current-only prefill can hide
compression error. Existing kernel tolerances do not substitute for model-level
quality criteria.

**Priority: integrate real calibration and clipping first; then add newer
per-head/centering semantics and measure quantizer differences.** The current
evidence does not identify a single faulty attention instruction as the cause.
