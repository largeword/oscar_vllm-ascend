# Qwen3.8-27B: OSCAR → vLLM-Ascend migration and accuracy review

Date: 2026-10-16. Paths below are relative to `/home/luxinliang/hw_projects/`.

## Executive conclusion

**Scope clarification: the primary review is now [OSCAR_IMPLEMENTATION_REVIEW.md](OSCAR_IMPLEMENTATION_REVIEW.md).** It focuses on OSCAR calibration, artifact loading, transforms, clipping/INT2 numerics, and mixed-cache attention. General model-serving, native-version, RoPE configuration, and GDN-precision observations below are retained as background from the broader initial review, not priorities for the clarified task.

**The checked-in Ascend OSCAR path differs from the original calibrated implementation.** It follows an older vLLM OSCAR PR, automatically prepares data-free Hadamard rotations, and disables clipping by default. Newer original OSCAR also supports per-head calibrated rotations and key centering that the port cannot currently represent.

The first priorities are:

1. Integrate data-dependent Q/K/V calibration into the PT-generation workflow.
2. Evaluate clipping explicitly: current defaults are **0/0**, versus **0.96/0.92** in the referenced OSCAR recipe.
3. Preserve the selected artifact's layer/head identity and transform fields.
4. Implement mean/LSE consistency before enabling centered artifacts.
5. Isolate original-reference versus pinned-PR quantizer numerics on identical inputs.
6. Distinguish operator implementation error from OSCAR compression error.

These are confirmed source/configuration differences, not measured causal attributions for the user's latest accuracy result. No Qwen3.8 weights, deployed rotation pair, or paired Qwen3.8 logits were available here.

## 0. Sources and documentation coverage

### Versions inspected

| Project | Local HEAD |
|---|---|
| `OSCAR` | `339368e8fb440c53d5e157a5974036f25f3841a0` |
| `gpt_new_oscar_kimi` | `7047ce36a19e001046a07a7d85de2a4092cd7941` |
| `vllm` | `aa0c433a3e5ee65641b7996e56c018ce91f9273d` |
| `vllm-ascend` | `1026eedfd2a13662d54f78e1c45566989a7157af` |

All four source trees had clean status at the initial inspection. This review adds files only under `oscar_vllm-ascend/`.

The port's historical reference manifest instead pins:

- vLLM: `0fc695fc6d1d82e9a5ac6835ac8e4e1c83703665`.
- vLLM-Ascend: `19e436985102f4ed3aad36c137a6481653688a6c` (v0.23.0 + PR12607).
- OSCAR vLLM PR46774: `57286d5d2cb08c3dcd8c17bb59e132d6985e6796`.
- OSCAR paper snapshot: `41ebcdba3db5f0ce1339c3727caea80df575d437`.

Evidence: `gpt_new_oscar_kimi/docs/reference_manifest.md:5–22`. Its referenced `references/` directory is absent from this checkout. I fetched the pinned PR's `rotation.py`, `config.py`, and `oscar_attn.py` from GitHub raw URLs, rather than treating the manifest as the source code. The current sibling vLLM Python tree contains no `oscar_int2`/OSCAR implementation in the search performed.

Pinned PR source base:
`https://raw.githubusercontent.com/vllm-project/vllm/57286d5d2cb08c3dcd8c17bb59e132d6985e6796/`

### Markdown coverage — explicit scope

Every Markdown file in the four project trees was read by the documentation scanner, including hidden documentation and `.MD` variants, excluding Git internals/virtual environments/node_modules/bytecode directories:

| Project | Files | Lines |
|---|---:|---:|
| OSCAR, including vendored dump tree | 378 | 63,924 |
| Ascend port | 101 | 37,998 |
| vLLM | 322 | 52,295 |
| vLLM-Ascend | 317 | 80,571 |
| **Total** | **1,118** | **234,788** |

`documentation_inventory.json` records every path, complete-file SHA256, size, headings, and topic counts. `documentation_excerpts.md` contains selected contextual matches. **This is complete automated full-text scanning, not a claim that I manually read all 234,788 lines.** Detailed reading covered the central rotation/semantics/runtime/design/acceptance documentation, current and historical launch policies, relevant archive entries, OSCAR README/porting/recipe documentation, native Qwen3.8 deployment guidance, hybrid-cache design, speculative-decoding guarantees, and accuracy-debugging guidance. The user's literal request for a line-by-line reading of every Markdown file is therefore not fully completed.

Historical documentation conflicts were resolved against current code and dated updates. Examples:

- `OSCAR/rotation/examples/README.md` still says only Qwen3-30B uses per-head rotations and omits Qwen3.8 from its group-256 list; the current README and Qwen3.8 script are newer evidence.
- `gpt_new_oscar_kimi/docs/prefix_caching_compatibility.md` describes an earlier default-APC-on policy. Current `target.json`, `target_cli.py`, and the 2026-10-15 notes set APC off and a 16,384-token budget.
- Statements that GDN is native refer to its numerical kernels; the current plugin also changes GDN metadata classification and execution routing.

## 1. What the reference script actually does

`OSCAR/rotation/run/qwen3.8-27b.sh` is a **serving/evaluation recipe, not itself a PT-generation script**:

```text
qwen3.8-27b.sh
  → source rotation/run/_common.sh
  → need_rot(ROT_DIR)
  → exec rotation/eval_oscar_gpqa.sh
  → SGLang server + OpenAI-compatible GPQA client
```

`need_rot` normally requires a rotation pair already on disk. `STARTUP_CALIBRATE=1` changes this: it selects the conventional filenames and permits the server to fit missing files. Existing files can still be reused; this flag does not guarantee a fresh calibration.

### Effective defaults

| Setting | Reference | Port's checked-in configuration |
|---|---|---|
| Model | `Qwen/Qwen3.8-27B` | `/softwarePlatform/c00879303/Qwen3.5-27B-w8a8-mtp` |
| Served name | model ID | `qwen3.5` |
| TP | 2 | 4 |
| FULL layers | 3, 7, 11, …, 63; 16 layers | discovered from local model config |
| Reference geometry | 24 Q heads, 4 KV heads, D=256 | must verify actual checkpoint |
| Quantization group | 256 | whole head vector; D=256 is one group |
| Sink/recent | 64/256 | 64/256, with additional speculative preservation |
| K/V clip | 0.96/0.92 | 0/0 because fields are absent |
| Levels | uniform INT2, Lloyd-Max disabled | uniform INT2 |
| Rotations | pair selected from `ROT_DIR` | auto-generated Hadamard, unless explicit combined artifact supplied |
| Metadata dtype | FP32 | FP16 |
| GDN recurrent-state dtype | FP32 default unless config/environment overrides it | explicitly BF16 in launcher |
| RoPE | native; script explicitly says no YaRN needed | YaRN factor 4 override |
| Prefix cache | enabled, SGLang `extra_buffer` | disabled by default |
| MTP | not requested by this recipe | `qwen3_5_mtp`, 3 speculative tokens |
| Weight quantization | no weight-quantization flag in recipe | Ascend W8A8 checkpoint/`--quantization ascend` |
| Sampling | temperature 1, top-p .95, top-k 20, presence penalty 0 | determined by caller; not fixed by `target.json` |

Sources:

- `OSCAR/rotation/run/qwen3.8-27b.sh:2–26`.
- `OSCAR/rotation/run/_common.sh:17–50`.
- `OSCAR/rotation/eval_oscar_gpqa.sh:60–64,131,330–351,446–460`.
- `gpt_new_oscar_kimi/configs/target.json`.
- `gpt_new_oscar_kimi/oscar_ascend/integration/cache_storage_ops.py:49–59`.

**The script alone does not prove that a run used per-head/centered PT files or per-head clips.** The README describes those in the current results recipe, but the wrapper discovers whichever pair is supplied and does not explicitly set `SGLANG_OSCAR_K_CLIP_PER_HEAD`. Record the actual pair and clip table. There is no local Qwen3.8 zoo pair: the checked-in zoo contains only Qwen3-8B and Qwen3-32B pairs. The remote Qwen3.8 zoo-directory lookup did not resolve in this review.

Another reproducibility detail: the driver defaults to **32,768 generated tokens**, whereas the published README GPQA table says **64K generation budget**. To reproduce that table, specify 65,536 explicitly and preserve the scoring/client settings. The README's Qwen3.8 numbers, 88.4→86.9 GPQA and KL=0.029 at 128K, are published reference results, not Ascend guarantees.

## 2. PT generation: original OSCAR, vLLM PR, and the Ascend port

### 2.1 Original offline calibrated route

The original shared-layer fitter reads **aligned post-RoPE Q/K/V** dumps, derives attention-aware second moments, eigendecomposes them, and composes the rotations.

For KV head `h` and its associated query-head group:

```text
Cq[h] = Q_group[h]^T Q_group[h] / number_of_grouped_query_rows
w[t,h] = K[t,h]^T Cq[h] K[t,h]
Cv[h] = sum_t w[t,h] V[t,h] V[t,h]^T / sum_t w[t,h]
```

For the old shared-layer variant, average `Cq[h]` and `Cv[h]` over KV heads before decomposition. The K objective is the **query second moment**, not simply `K^T K`; the V objective is an **attention-energy-weighted value second moment**, not simply `V^T V` or an explicit softmax covariance.

```text
C = E diag(lambda) E^T
Rk = Ek H Pbr(lambda_k)
Rv = Ev H Pbr(lambda_v)
```

The fitter uses FP64 moments/eigensolve and saves FP32 matrices. Evidence: `OSCAR/rotation/compute_kv_rotation.py:67–159,257–311`.

**Specify `--composition r_h_pbr`.** The Python CLI defaults to `plain` (`:389–403`), despite an internal comment calling RHP the default. The shell wrapper correctly supplies `r_h_pbr` (`rotation/qwen3-8B/compute_rotation.sh:22–26,93–100`).

### 2.2 Original startup route and newer per-head fitting

The startup collector observes Q/K/V at the attention boundary (`radix_attention.py:179–194`) after model Q/K normalization and RoPE. It collects per-head statistics, reduces shared-layer statistics across TP, decomposes on rank 0, broadcasts, and publishes a K/V pair.

Important distinction: **startup `finalize()` itself produces shared-layer format-1 rotations**. The more capable per-head/centered route is a second fitter over saved moments:

```text
startup collector → oscar_moments_rank*.pt
                 → fit_oscar2_variants.py --variants perhead,center
                 → per-head rotation pair, optional k_mean
```

Evidence: `oscar_calibration.py:417–459,493–572,646–743`; `fit_oscar2_variants.py:250–344`.

The `center` variant preserves a separate 256×256 basis and 256-element key mean for each of the 4 global KV heads in each FULL layer. Non-orthogonal variants additionally require query/output companion matrices. They are not necessary for an initial Qwen3.8 `center` migration, and the original README explicitly warns that its non-orthogonal K ablations collapse under scalar INT2 at long context.

### 2.3 The original vLLM PR

The pinned PR's `vllm/model_executor/layers/quantization/oscar/rotation.py` **loads the original exporter’s files**. The inspected runtime loader does not fit them. It accepts a per-layer dictionary or stacked layer matrices and requires a single `[D,D]` matrix for a layer.

Its attention implementation:

- reads separate K/V rotation paths;
- performs FP32 `x @ R`;
- clips via `torch.quantile(abs(x), ratio)` with linear interpolation;
- uses FP16 scale/minimum metadata and adjacent-channel packing;
- has a native-current prefill path and a full-history dequantization continuation path;
- has staging-eviction behavior and no graph/spec-as-decode support in that snapshot.

The Ascend port substantially changes the execution/cache machinery, but mostly follows **this older PR's numerical contract**, not the current SGLang one.

### 2.4 What your automatic generator does

`gpt_new_oscar_kimi/tools/prepare_rotations.py:43–68`:

1. Reads local `config.json`, derives FULL-layer names and head dimension.
2. Hashes config bytes and, if present, the safetensors **index JSON**.
3. Calls `build_hadamard_artifact` on NPU.
4. Saves `artifacts/rotations/<fingerprint>/hadamard.pt`.
5. Explicitly rejects any automatic `rotation_method` other than `hadamard`.

`oscar_ascend/rotations.py:181–199` creates:

```text
for each FULL layer:
    Rk = H
    Rv = H
objective = "hadamard"
calibrated = False
```

It never loads model weights for a forward pass, never observes Q/K/V, and never learns a spectral basis. The model fingerprint identifies the file's intended use; it does not make the matrix data-dependent. Hadamard is a valid OSCAR ablation, but **Hadamard alone is not `E @ H @ Pbr`**.

There is a real sample API (`sample_covariances`, `build_sample_artifact`, `rotations.py:221–320`), but:

- it is not connected to automatic preparation;
- it requires the caller to supply aligned samples and an eigensolver;
- it accumulates FP32, whereas the original fitter uses FP64;
- it averages across supplied heads, yielding a shared-layer matrix;
- it contains no cross-rank gather/reduction;
- it provides no per-head means or per-head clip fitting.

The sample formula is recognizably the original shared-layer qqt/sst formula. The decisive default-path difference is **not using that formula at all**. For TP4, independently fitting one local head on each rank and then saving one shared file would also be wrong: either preserve per-rank head identity or aggregate moments globally before fitting a shared basis.

### 2.5 File-schema incompatibility

| Aspect | Original calibrated pair | Current Ascend combined artifact |
|---|---|---|
| Files | separate K and V | one file |
| Layer keys | integer/global-layer ID | `model.layers.N.self_attn.attn` |
| Matrix field | `rotation` | `Rk`, `Rv` |
| Shared shape | `[256,256]` | `[256,256]` |
| Per-head shape | `[4,256,256]` supported by newer SGLang | rejected |
| Key mean | optional `k_mean` | unsupported |
| Dual transforms | optional `q_rotation`, `o_rotation` | unsupported; orthogonality required |
| Provenance | generation/model/prompt metadata varies by exporter | model/PR fingerprints and `test_only` |

`validate_artifact` requires `format_version=1`, `source_grouping="layer"`, exact layer names, and `[D,D]` FP32 orthogonal matrices (`rotations.py:129–178`). It reconstructs entries using only `layer_id`, `Rk`, and `Rv`; merely adding a `k_mean` key does not add centering support.

A converter can losslessly repackage **old shared orthogonal** files. It cannot turn per-head calibrated/centered files into an equivalent shared, uncentered artifact. Do not average matrices, select global head 0 on every TP rank, drop `k_mean`, or use `R.T` as the inverse of a non-orthogonal transform.

The runtime can select an explicit combined file via `rotation_artifact` or `OSCAR_ROTATION_ARTIFACT` (`runtime.py:740–744`). Automatic preparation does not honor that selection in the same way; it still generates/validates the default Hadamard output unless `--output` is supplied. A migrated orchestration path must validate the selected artifact and skip inappropriate regeneration.

## 3. Runtime numerical differences beyond PT generation

### Quantizer and precision contract

| Operation | Current SGLang reference path | Ascend port / pinned vLLM PR |
|---|---|---|
| Rotation runtime | normally BF16 matrix/input/output | FP32 matrices and rotated outputs |
| Clip threshold | sorted absolute row at `min(int(ratio*D),D-1)` | interpolated quantile at `ratio*(D-1)` |
| Scale | `max(max-min,1e-8)/3` | `max((max-min)/3,1e-8)`, then FP16 round |
| Stored second parameter | zero point `z=-min/scale` | minimum `m=min`, FP16 rounded |
| Encoding | `trunc(x/scale + z + .5)` | `clamp(trunc((x-m)/scale + .5),0,3)` using rounded metadata |
| Reconstruction | `(code-z)*scale` | `code*scale+m` |
| Metadata | FP32 in the reference driver | FP16 |
| Byte channel mapping, D256 | channels `j,j+64,j+128,j+192` | canonical layout: `4j,4j+1,4j+2,4j+3` |
| BF16 window frame | centered/rotated in SGLang mixed pool | raw/unrotated in the port |

Sources:

- SGLang `unified_kv_pool.py:530–630,1373–1405,1506–1543`.
- SGLang `QuantKernel/oscar_rotation_clip_int2_kv.py:109–127,181–218,387–399`.
- SGLang `srt/mem_cache/kv_quant_kernels.py:45–100`.
- Port `csrc/kernels/rotate_clip_store.cpp:139–204` and `docs/semantics.md:19–39`.
- Port candidate striped formats additionally rearrange storage; their writer/reader bundle must remain paired.

For D256 specifically, K=.96 chooses sorted element **245** in SGLang, versus interpolation at **244.8** in the port. V=.92 chooses **235**, versus **234.6**. Therefore setting the same ratios fixes the default mismatch but does not establish exact reference parity.

The two affine parameterizations are algebraically equivalent in exact arithmetic. FP16 metadata rounding, BF16 rotation rounding, epsilon placement, and different arithmetic order prevent byte/numerical equivalence in general. **Different packing is not itself an accuracy bug when the writer and reader agree.** It becomes a severe bug if bytes or metadata are consumed under the other interpretation. PT rotations are matrices, not packed cache bytes: PT reuse does not require reuse of SGLang's physical cache layout.

FP32 rotation/attention should not be described as intrinsically worse than BF16. Nevertheless, INT2 threshold decisions are discrete, so “higher precision” is not proof of reproducing a recipe calibrated and evaluated with another rounding path. Match one reference contract first, then assess precision changes separately.

### Key-centering trap when preserving raw windows

SGLang centers **all** keys—HP windows, INT2 history, and extend-time keys—consistently (`unified_kv_pool.py:1373–1382`). Thus every logit for a query shifts by the same constant.

The port's history is transformed, but its windows/current chunk remain in raw coordinates (`integration/impl.py:215–295`). If the migration centers only history:

```text
l_history_centered = attention_scale * q · (k - mu)
                   = l_history_raw - attention_scale * q · mu
```

The history's normalized output does not change from this constant shift, but its LSE does. Before merging with raw-window/current LSEs, use:

```text
LSE_history_raw = LSE_history_centered + attention_scale * dot(q_raw, mu)
```

Apply this per query, per corresponding KV head, to each history partial before the stable merge. Alternatively, center all three sources consistently. Keeping exact raw windows plus correcting history LSE is a natural fit for this port; finite-precision equivalence still requires verification.

A scalar counterexample is in `source_audit.json`: two equal original logits give history probability 0.5. Centering only history by a shift of −1 without correction gives **0.268941**, even with no quantization error. This is a **migration hazard**, not a claim that the current uncentered port already has this bug.

### Preserve output-gate order

Qwen's FULL attention is gated. The model executes attention, then an elementwise sigmoid gate, then `o_proj`:

- SGLang `models/qwen3_5.py:1523–1532`.
- Ascend `patch/worker/patch_qwen3_5.py:91–97`.

Return the attention result to the **original value coordinate system before the gate**. A general rotation does not commute with an elementwise gate. Do not move `Rv.T` through that gate or blindly absorb it into `o_proj`. The reference driver defaults V-rotation absorption off.

## 4. How to migrate `qwen3.8-27b.sh`

### 4.1 Flag mapping

| SGLang recipe item | Ascend migration |
|---|---|
| `python -m sglang.launch_server` | `vllm serve` with Ascend platform plugin and OSCAR external plugin |
| `--model-path` | positional model path; port currently needs a local directory for artifact/config reads |
| `CUDA_VISIBLE_DEVICES` | explicit `ASCEND_RT_VISIBLE_DEVICES` |
| `--tensor-parallel-size` | same concept; current port launcher enforces exactly four device IDs |
| `--kv-cache-dtype int2` | external plugin's backend/spec routing; not a native Ascend CLI dtype |
| `--kv-cache-quant-group-size 256` | whole-head D256 quantization in the current port |
| SGLang K/V rotation environment | explicit supported combined artifact, or implement a pair-aware loader |
| SGLang clip environment | port config `k_clip_ratio` / `v_clip_ratio`; separately implement reference clip mode |
| `--attention-backend triton` | OSCAR Ascend backend selected by plugin; not a mechanical flag translation |
| `--mamba-radix-cache-strategy extra_buffer` | native vLLM hybrid/Mamba cache-mode and APC protocol; no 1:1 flag |
| `--mem-fraction-static` | `--gpu-memory-utilization` as an approximate budgeting counterpart, not identical allocation semantics |
| `--max-running-requests` | `--max-num-seqs` |
| CUDA graph flags | target-supported ACL graph configuration; current port hooks runner V1 |
| GPQA client | reuse OpenAI-compatible client, matching alias/sampling/scorer/budget |

Neither `SGLANG_OSCAR_*` variables nor old-PR `VLLM_OSCAR_*` variables configure this external port. In particular, copying `--kv-cache-dtype oscar_int2` from the CUDA PR does not install the implementation into the sibling native vLLM checkout.

### 4.2 Required implementation sequence

**A. Establish a separate Qwen3.8 configuration.** Keep the previous performance configuration as a historical baseline. Set the actual Qwen3.8 model directory/name; use native RoPE; explicitly bind weight format, effective dtype, FULL geometry, and software revisions. BF16 versus W8A8 must be a deliberate comparison axis. `qwen3_5_mtp` is a valid method name for Qwen3.8—it shares the architecture—so the method spelling itself is not a bug (`vllm-ascend/docs/source/tutorials/models/Qwen3.8-27B.md:271–275`).

**B. Rebase the external integration onto one pinned native pair.** Check backend/spec allocation, runner V1, GDN metadata, MTP, and sampler signatures. Do this before assuming the locally available native checkouts are compatible; concrete failures are listed in §5.

**C. Implement calibrated artifact ingestion.** Add versioned support for global layer IDs, per-head matrices, means, and clip tables, with explicit semantics. For the orthogonal `center` recipe, Q uses `Rk` and output uses `Rv.T`. If general non-orthogonal support is added later, validate `Q_transform @ Rk.T = I` and `Rv @ O_transform.T = I` instead of demanding orthogonality.

**TP4 simplification:** with 4 global KV heads, every rank has one KV head and 6 query heads. Selecting `Rk[layer,rank]`/`Rv[layer,rank]` in a rank-aware loader allows existing 2-D matrix operators to operate on a per-head basis. This still requires loader/provenance changes, mean/LSE support, and clip selection. With TP2, each rank has two KV heads and twelve queries: operators must select the appropriate matrix by KV head, and by `q_head // 6` on the query/output side. A single 2-D matrix per layer is then insufficient.

**D. Implement or reuse a calibration collector.** Capture aligned Q/K/V once, immediately before FULL attention, after QK normalization and RoPE, before OSCAR transformation. Preserve layer ID, global head ID, TP rank, sample/token IDs, logical position, and prompt boundaries. Exclude padding, dummy graph calls, duplicate prefix-cache observations, and GDN states. Collect with the actual deployed weights and effective RoPE. If matching the old shared-layer fitter, reduce moments across TP before the eigensolve; if matching the new per-head fitter, preserve heads and gather the distinct shards.

Use the original FP64 fitter as an offline comparison reference. The port's present policy requires NPU production numerical work and rejects CPU test artifacts; importing a validated external fitted artifact would need a deliberately supported provenance path, rather than clearing `test_only` on a test artifact. If keeping the all-NPU fitting requirement, supply and validate an eigensolver against that offline reference. Returning NPU tensors alone does not prove the solver ran entirely on NPU.

**E. Calibrate on representative lengths.** Thirty thousand total short-prompt tokens do not cover 64K/128K positional behavior. Use disjoint representative calibration prompts with long-position coverage, preserve the task's text template, and evaluate on held-out inputs. Record the effective RoPE and exact weight revision in the artifact.

**F. Implement a named SGLang-compatible quantizer profile or explicitly retain a PR-compatible profile.** Match clip order statistics, metadata precision/units, and rounding when claiming parity. Keep cache-layout changes internally consistent. With FP32 metadata, D256 K+V history grows from 136 to 144 bytes per token/head; recompute pool capacity and snapshot offsets rather than replacing the dtype in place.

**G. Migrate orchestration.** Validate an explicit supplied artifact; fit only when requested; publish atomically; stop on missing FULL layers. Run native and compressed arms with the same model, tokenizer, RoPE, weight dtype, chunk budget, MTP/APC setting, and sampling. Later re-enable each production feature against its own paired control.

### 4.3 Native Qwen3.8 parity launch example

This is a **native-cache control** for the new accuracy investigation, not a replacement for the port's frozen performance launch. It deliberately begins without speculative decoding, matching the reference script's lack of an MTP request. These commands were not executed here.

```bash
export MODEL=/absolute/path/to/Qwen3.8-27B
export ASCEND_RT_VISIBLE_DEVICES=0,1,2,3
export OSCAR_ENABLED=0
export VLLM_USE_V2_MODEL_RUNNER=0

vllm serve "$MODEL" \
  --served-model-name qwen3.8 \
  --host 127.0.0.1 --port 8989 \
  --tensor-parallel-size 4 --data-parallel-size 1 \
  --dtype bfloat16 --kv-cache-dtype auto \
  --max-model-len 262144 \
  --max-num-batched-tokens 16384 --max-num-seqs 32 \
  --gpu-memory-utilization 0.85 \
  --mamba-cache-dtype bfloat16 --mamba-ssm-cache-dtype float32 \
  --no-enable-prefix-caching \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
  --trust-remote-code
```

For an actual Ascend W8A8 checkpoint, change `MODEL` and add `--quantization ascend` **to both arms**. Omit the inherited `--hf-overrides` YaRN object. This example selects FP32 SSM state to match the SGLang default; use the actual reference run's state dtype once established. A second paired BF16-SSM experiment isolates the port's historical state-precision choice. Hardware support, changed hybrid-page geometry/memory feasibility, and the chosen native-version options still need target validation.

For the compressed arm **after B–F are implemented**, use the same CLI and:

```bash
export OSCAR_ENABLED=1
export OSCAR_TARGET_CONFIG=/absolute/path/to/qwen38-accuracy.json
# The installed oscar_ascend general plugin performs backend/spec registration.
```

The plugin configuration must match the CLI's geometry/budgets and point to the calibrated artifact. Essential existing fields are:

```json
{
  "model": "/absolute/path/to/Qwen3.8-27B",
  "devices": [0, 1, 2, 3],
  "max_model_len": 262144,
  "max_num_batched_tokens": 16384,
  "max_num_seqs": 32,
  "compilation_config": {"cudagraph_mode": "FULL_DECODE_ONLY"},
  "speculative_config": {},
  "enable_prefix_caching": false,
  "sink_tokens": 64,
  "recent_tokens": 256,
  "k_clip_ratio": 0.96,
  "v_clip_ratio": 0.92,
  "rotation_artifact": "/absolute/path/to/validated-qwen38-calibrated.pt"
}
```

This illustrates the configuration handoff, **not an already-working per-head/centered migration**: the current loader cannot consume that richer artifact. An old shared orthogonal artifact can be repackaged for the existing schema, but would only test the older algorithm. Do not name a Hadamard artifact “calibrated” to make this path appear complete.

The existing `tools.target_cli.serve_argv` always emits quantization, speculative, and HF-override arguments; it needs optional-field handling for a clean BF16/no-MTP parity launch. `tools.prepare_rotations` needs an explicit supplied-artifact path and calibrated mode. `target_env` enforces four devices, so changing `TP_SIZE=2` in a copied shell wrapper is insufficient.

### 4.4 Evaluation-client migration

The existing GPQA client uses the OpenAI-compatible API and can target vLLM:

```bash
python /absolute/path/to/OSCAR/rotation/_eval_runner/run_simple_eval.py \
  --task gpqa --model qwen3.8 \
  --base-url http://127.0.0.1:8989/v1 \
  --max-tokens 65536 \
  --temperature 1.0 --top-p 0.95 --top-k 20 \
  --presence-penalty 0 --num-threads 32 \
  --n-repeats 1 --seed 0 \
  --output-dir /absolute/path/to/results/qwen38-native
```

This is a reproducibility example, not a request to repeat previously completed AISBench runs. The client requires the `simple_evals` dependency/submodule and its own Python dependencies. Preserve the same seed on both arms; a shared seed does not imply tokenwise identity across engines.

The client reads `message.content` only (`run_simple_eval.py:142–155`). Match reasoning/template handling and ensure the final answer reaches that field; do not accidentally score only a reasoning fragment. Its GPQA answer extractor is explicitly patched to accept `Answer:\nA` forms (`:226–237`), so scores from another harness are not automatically comparable.

**The long-context KL client is not API-portable as written.** It calls SGLang `/generate` and requires `SGLANG_OSCAR_LOGITS_DUMP_DIR` full-vocabulary dumps (`kl_longctx.py:72–101`). A vLLM version needs its own teacher-forced/logit collection path with aligned positions and token IDs. Top-k logprobs alone do not give exact full-vocabulary KL.

## 5. Other accuracy and compatibility findings

### P0: Model/weights/RoPE configuration is not matched

The checked-in target names Qwen3.5, W8A8 and MTP, and applies a YaRN ×4 override with `original_max_position_embeddings=262144` (`target.json:2,61–86`). The Qwen3.8 reference explicitly says native context 262,144 needs no YaRN (`qwen3.8-27b.sh:2–6`). Architecture compatibility does not imply interchangeable weights or rotations.

This is a confirmed checked-in discrepancy. A directory can be renamed or a deployed configuration overridden, so the path alone does not prove which weights produced the user's latest outputs. Record actual effective config/weight/tokenizer identity before assigning a score gap to INT2.

### P0: Current sibling native trees are incompatible with some port hooks

Concrete static findings:

1. The port calls `rejection_sample(..., target_logits_or_tuple=...)` (`integration/greedy_sampling.py:107–118`); the sibling Ascend function accepts `target_logits` (`sample/rejection_sampler.py:378–396`). This is an unsupported keyword if reached.
2. Sibling `rejection_greedy_sample_with_triton` accepts additional `uniform_probs`, `synthetic_conditional_rates`, and `synthetic_mode` arguments (`ops/triton/reject_sample.py:426–440`); the replacement accepts only the old signature (`integration/greedy_sampling.py:15–26`).
3. The port unconditionally patches `AscendGDNAttentionMetadataBuilder._fold_spec_sized_prefill_chunks_into_spec` (`plugin.py:362–371`). That method was not found in either current sibling native Python tree. `_patch` raises when a required method is missing (`plugin.py:59–68`).
4. The sibling runner now explicitly excludes unfinished hybrid prompt rows from uniform decode (`model_runner_v1.py:3427–3434`), while the port's custom prefill dispatch fix was written against an older behavior.

`audit_contracts.py` reproduces the signature/config findings without importing native frameworks. These are **compatibility failures**, not proof of a silent numerical bug in the user's older deployment. Pin and rebase rather than assuming a newer native version can accept all old monkey-patches.

### P1: Missing calibrated per-head transforms and clipping

This is the strongest identified **algorithmic** difference. Try the progression Hadamard → shared calibrated → per-head calibrated → per-head + centering, with matching clip/quantizer settings, rather than changing every factor together. Quantile ratios optimized with one basis need not be optimal for another.

At D=group_size=256, `Pbr` is a within-group coordinate permutation. Under ideal permutation-equivariant scalar quantization and matching inverse/query transforms, changing only this permutation does not create a fundamental quality benefit. The missing data-derived basis, head separation, centering, and clipping deserve much higher priority than blaming bit reversal alone.

### P1: GDN/MTP correctness extends beyond FULL attention kernels

Forty-eight of the model's 64 layers are GDN. The plugin preserves native GDN numerical kernels but also installs:

- GDN prefill classification wrappers;
- a batch-dispatch override for certain speculative-width prompt tails;
- MTP discard/slot-position wrappers;
- greedy-rejection sampling replacements.

See `plugin.py:154–174,362–398,434–477` and `integration/prefill_state_contract.py`. Consequently a plugin-on/plugin-off model comparison changes more than cache storage on the pinned stack. This matters when attributing a discrepancy.

**Check recurrent-state precision independently.** `tools/target_cli.py:46–47` forces both Mamba cache types to BF16. In SGLang, `Qwen3_5TextConfig` inherits `Qwen3NextConfig`; its state configuration uses `mamba2_state_dtype`, whose SSM default is **FP32**, with config/environment overrides (`configs/qwen3_5.py:15`, `configs/qwen3_next.py:312`, `configs/mamba_utils.py:47–107`). The reference shell does not override that dtype. Actual checkpoint/environment values remain unobserved, but the defaults are different. Recurrent-state rounding across 48 layers can affect long-context quality even with FULL KV quantization disabled. In vLLM, GDN `auto` follows the convolution state dtype, so merely removing the explicit BF16 SSM flag does not necessarily select FP32 (`vllm/model_executor/layers/mamba/mamba_utils.py:98–130`). Match SSM dtype explicitly and recompute hybrid-cache geometry when changing it.

The draft FULL layer currently uses explicit **identity** rotation (`runtime.py:746–767`) because target-only calibration does not sample it. This can degrade draft proposals/acceptance. It does **not**, by itself, prove final-target accuracy loss: exact speculative rejection preserves the target distribution when target evaluation, bookkeeping, and sampling are correct. Compare target logits under forced common tokens; treat MTP acceptance as a separate metric. Also keep optional approximate block/entropy verification off for a lossless-parity investigation.

### P1: Windows, partial prefills, and graph padding

Required invariants are already central to the port's design and should remain regression targets during migration:

- all logical positions covered exactly once by history/window/current sources;
- read old recent-window contents before writing a large new chunk;
- preserve `R + speculative_slack` rows through partial/all rejection;
- map global layer IDs 3,7,…,63 correctly, including clip and mean tables;
- map virtual block-128 metadata to physical pages correctly;
- never let padded rows write shared prefix/page-zero content;
- keep FULL and GDN prefix hits at a common valid boundary;
- graph replay must refresh lengths/positions/slots at stable addresses;
- pool reuse must not allow stale tags or stale per-step metadata to identify live rows.

Evidence: `docs/runtime_implementation.md:26–100`, `docs/prefix_caching_compatibility.md:94–111`, and `integration/impl.py:288–295`. The original SGLang driver documents past large score failures from padded writes corrupting shared prefixes (`eval_oscar_gpqa.sh:131–142`). This is a known class of failure, not a finding that the current port still has it.

### P1: Kernel parity is not model-quality acceptance

`configs/acceptance.json:14` still has null logits/task/MTP quality thresholds. Most local checks establish that an optimized kernel reproduces a **given quantized representation**, not that the representation preserves native-model quality.

There is direct historical evidence of this distinction: archive #148 records LongBenchv2 **53.54% at fe0 → 48.03% at 34639ab**, both completing all 127 requests, despite local numerical/performance gates. That change was reverted. The record explicitly does not establish the mathematical cause (`issue1_full_record.md:28488–28502`). It concerns the old Qwen3.5 setup and is not a Qwen3.8 score.

### P2: Calibration provenance and stale artifact reuse

Current automatic/runtime fingerprints hash config bytes plus a weight-index JSON, **not the actual weight contents**, and do not include effective `hf_overrides`, prompt IDs, clip policy, or quantizer mode (`prepare_rotations.py:35–40`, `runtime.py:736–742`). The separate stronger `model_fingerprint` helper is not what those paths call.

This is relatively harmless for dimension-only Hadamard math, but becomes significant when calibration is integrated. Bind a calibrated artifact to verified weight revision/digests, tokenizer/template, effective RoPE, QKV hook frame, head mapping, calibration positions, quantizer profile, and clip-table identity. A filename/fingerprint alone does not establish matching calibration.

### P2: Evaluation conditions can hide or amplify quantization error

- A first prefill chunk reads current BF16 K/V. Monolithic prefill prompt logprobs can therefore look healthy while compressed-history decode is poor.
- Smaller prefill chunks cause more queries to read INT2 history; a 512-token-chunk KL protocol is not equivalent to a 16K-chunk one.
- Reference KL is teacher-forced, full-vocabulary `KL(P_native || P_int2)`, scores later positions, and checks exact input-token/position alignment.
- Free-running generations diverge after the first sampled-token difference; compare common-prefix logits before interpreting later hidden-state drift.
- Match thinking mode, system prompt, tokenizer, stop/EOS behavior, reasoning effort, output budget, penalties, task subset, and grading. Qwen3.8's reference presence penalty is 0; do not inherit Qwen3.5's thinking-mode 1.5 recommendation.
- Short synthetic probe success, HTTP 200, or no NaNs cannot establish long-context answer quality.

## 6. Efficient diagnostic order

Use existing reports first. The following is the missing-evidence order for the Qwen3.8 migration, not a claim these measurements were performed or a demand to repeat old full benchmarks.

| Step | Comparison | What it isolates |
|---|---|---|
| 1 | Same Qwen3.8 checkpoint, native cache, SGLang vs Ascend | model/RoPE/tokenizer/native backend difference |
| 2 | Ascend native BF16 weights vs intended W8A8 weights, both native cache | weight quantization |
| 3 | Same captured QKV, rotate + exact inverse, no clipping/INT2 | transform/head/gate conventions |
| 4 | Same captured QKV/artifact, original scalar reference vs Ascend scalar reference | clip/metadata/rounding/packing semantics |
| 5 | Ascend kernel vs that scalar reference, including raw-window/LSE merge | implementation error |
| 6 | Native-cache model vs compressed-cache model, teacher-forced common tokens | accumulated compression error |
| 7 | Matched MTP off/on, APC cold/warm, eager/graph, and mixed-length cases | lifecycle/sampler/graph integration |
| 8 | Held-out task metrics with matched client/template/budget | application-level quality |

For step 6, retain a bounded set of diagnostic positions at 8K/32K/64K/128K, especially around 64/256 window transitions, physical-page boundaries, the first compressed-history read, and speculative rejection boundaries. Record per-head attention error/LSE, layer output relative-L2, full-vocabulary KL/NLL/top-1, and the first divergent layer/token. Obtain end-to-end data under the intended production chunk budget as well as a controlled small-chunk compression-stress protocol.

For calibrated PT comparison, also validate orthogonality/inverse identities and moment-fit objectives. Raw matrix element equality is not sufficient across eigensolvers: eigenvector signs and degenerate-subspace bases may differ. Compare transformed quantization/attention error on identical held-out QKV.

## 7. Delivered evidence and execution boundary

Files in `oscar_vllm-ascend/`:

- `QWEN38_OSCAR_MIGRATION_REVIEW.md`: this review and migration design.
- `audit_documentation.py`: reproducible Markdown corpus scan.
- `documentation_inventory.json`: complete-file inventory, hashes, headings, topic counts.
- `documentation_excerpts.md`: automated selected context, not a manual-read certificate.
- `audit_contracts.py`: dependency-free static configuration/API checks and scalar examples.
- `source_audit.json`: actual check output for the inspected revisions.

Executed successfully: documentation scan and static contract audit. The available `python3` cannot import `torch`; no torch numerical tests, model execution, NPU probes, PT generation, or accuracy benchmark was run. No runtime migration is claimed complete. The source repositories and frozen production configurations were not edited.

**Bottom line for the clarified scope:** prioritize calibrated/head-aware PTs, clipping, centering-aware LSE, and a defined OSCAR quantizer contract. Compare implementation error and compression error separately. The focused conclusions and implementation sequence are in [OSCAR_IMPLEMENTATION_REVIEW.md](OSCAR_IMPLEMENTATION_REVIEW.md).
