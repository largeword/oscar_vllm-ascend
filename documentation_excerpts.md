# Automated documentation excerpts

Coverage: full-text scan; selected context only.

## OSCAR/.agents/skills/clean-startup-log/SKILL.md
[...]
1: ---
2: name: clean-startup-log
3: description: Audit SGLang startup logs, save evidence, and propose cleanup for user review. With no arguments, run Qwen3-8B at TP1 and TP2 plus gpt-oss-20b at TP1.
4: disable-model-invocation: true
5: ---
[...]
18: | Case / log filename | Command |
19: |---|---|
20: | `qwen3-8b-tp1.log` | `uv run sglang serve --model-path Qwen/Qwen3-8B` |
21: | `qwen3-8b-tp2.log` | `uv run sglang serve --model-path Qwen/Qwen3-8B --tp 2` |
22: | `gpt-oss-20b-tp1.log` | `uv run sglang serve --model-path openai/gpt-oss-20b` |
23: 

## OSCAR/.agents/skills/cookbook-add-model/references/authoring-reference.md
[...]
16: **Path**: `docs/src/snippets/configs/<vendor>/<model>.jsx`. The vendor folder is
17: the HuggingFace org (`deepseek-ai`, `Qwen`, `moonshotai`, ...); the file
18: name is a short hyphenated model id (`deepseek-v4`, `qwen3.5`, ...).
19: 
20: **Shape**: must be a single `export const config = { ... }` literal. Do not
[...]
33: | `variants` | `{id, label, subtitle?}[]` | 2nd-dim option list. Use `default` / single-element if the model has no variant axis. |
34: | `quantizations` | `{id, label}[]` | 3rd-dim option list. |
35: | `strategies` | `{id, label}[]` | 4th-dim option list. Canonical ids: `low-latency` / `balanced` / `high-throughput` (never model-specific ids like `mtp`). **The count follows the page's operating points**: one recipe → a single `balanced`; two → `low-latency` + `high-throughput`; three → the full trio (the ideal). Tiers apply per (hw × variant × quant) combination — a single-recipe combination parks under its semantically honest tier (clear slant → that tier, e.g. DSv4's RTX 6000 → `low-latency`; no slant → `balanced`, e.g. Qwen3.5's Xeon); the page's list is the union and the engine greys unused chips per selection. Never invent a recipe just to fill chips. When two recipes differ by MTP / speculative decoding, the assignment is deterministic: spec ON → `low-latency`, spec OFF → `high-throughput` (at saturation the draft+verify overhead outweighs the speedup — same reason DSv4's high-throughput recipes disable MTP). The recurring markers in the other direction: dp-attention ON (MLA-attention models) and EP / DP+EP ON (MoE models) → `high-throughput`. |
36: | `nodesOptions` | `{id, label}[]` | 5th-dim option list. The `id` MUST be `single` or `multi-N` — the engine parses N from the id for `--nnodes`. |
37: | `cells` | `{match, verified?, verificationStatus?, nnodes?, env, flags}[]` | One per supported (hw × match-dim) combination. See §2.2. `nnodes` supplies the node count when the config declares no `nodes` dim (default 1). |
[...]
49: | `benchmarkCommands` | `{speed: string, accuracy: {[accKey]: string \| {[variant]: string}}, numPromptsByConc?: {[c]: number}}` | Powers the benchmark card's **"⚡ Reproduce"** modal. `speed` is ONE `bench_serving` template; the engine fills `{{DATASET}}`/`{{ISL}}`/`{{OSL}}` from each cell's `speed[].workload`, the chip-picked `{{MAX_CONCURRENCY}}`, and `{{NUM_PROMPTS}}` (resolved `workload.num_prompts ?? numPromptsByConc[c] ?? max(c*2, 200)`). `accuracy` maps an accuracy field (e.g. `gsm8k_pct`) to a per-eval template — a string, OR a `{flash, pro, …}` object keyed by variant when the command differs per variant (e.g. GPQA/AIME `--max-tokens`). The modal renders a chip per eval (one command area, like Speed). Both also use `{{MODEL_NAME}}` + `{{CURL_HOST}}`/`{{CURL_PORT}}` like `curl`. `speed` should carry `--flush-cache` (bench_serving's `random` prompts are deterministic — warm reruns hit the radix cache and inflate throughput; measure cache-cold). Optional; the button only appears when this AND `benchmarks` are present. |
50: | `defaultAccuracy` | `{[variant]: {[accKey]: number}}` | Model-level accuracy applied to **every** cell of a variant (e.g. GPQA Diamond / AIME25 — hardware-independent). Merged UNDER each cell's measured `accuracy` (a per-cell value wins), so you set a variant's score once instead of copying it onto every benchmark entry. Keys must match `accuracyLabels` (below) + `benchmarkCommands.accuracy`. |
51: | `accuracyLabels` | `[key, label, unit][]` | The eval set rendered in the benchmark card and the "⚡ Reproduce" modal — **the engine ships no default**, every config declares its own (e.g. DSv4: GPQA/AIME25/GSM8K; Qwen3.5: GSM8K/MMMU). Required whenever the benchmarks carry accuracy data; without it the accuracy rows silently don't render. Every key used in `benchmarks[].accuracy`, `defaultAccuracy`, and `benchmarkCommands.accuracy` must appear here. |
52: | `latencyPercentile` | `"Mean" \| "P50"` | Optional, **temporary**; the percentile the benchmark TTFT/TPOT values are. **Default `"P50"`** — the card renders `TTFT (<pct>)` / `TPOT (<pct>)`. Set `"Mean"` only for legacy data recorded as Mean (being re-measured to P50). A benchmarks entry may carry its own `latencyPercentile` to override the page value per cell (entry → config → `"P50"`). `tokens_per_sec_per_gpu` is stored as **total (in+out)/GPU** = `output tok/s/GPU × (isl+osl)/osl`, shown by the card as-is. |
53: | `github` | `{owner?, repo?, issueTemplate?, cookbookModel?}` | Overrides for the "Submit verified cell" CTA in the playground. Defaults: `sgl-project/sglang` + `3-playground-verified-cell.yml` + `"deepseek-ai/deepseek-v4"`. Set `cookbookModel` to the model's HF id (`<hf-org>/<model-slug>`); it prefills the issue template's free-form `model` input when the issue opens. **Don't prune this block** — without it the engine falls back to `deepseek-ai/deepseek-v4` and submissions from your page get mislabeled. |

## OSCAR/.agents/skills/cookbook-add-model/references/engine-axis.md
[...]
61: The axis id is the key in both `config.playgroundFeatures` and the
62: internal `deltas` object. Use camelCase, descriptive but short:
63: `mambaCache`, `attentionBackend`, `kvCacheDtype`.
64: 
65: The state shape is whatever `initState` returns. Common shapes:

## OSCAR/.agents/skills/cookbook-migrate-model/SKILL.md
[...]
17: 
18: Migration-specific references in this skill:
19: - [references/dimension-mapping.md](references/dimension-mapping.md) — legacy-control → new-dimension mapping rules, command rewrite table, per-family strategy sets, and the Qwen3.5 pilot as a worked example (PR #27848).
20: 
21: The round's per-model inventory (scope, batch order, quirks, measured-data
[...]
76:    (`--kv-cache-dtype`), mamba (`--mamba-radix-cache-strategy`), … — is already
77:    covered by the merged generic **`flagSelects`** axis: declare it in the
78:    config (a list of `{ id, title, stripPrefixes, options }`; see the Qwen3.5
79:    mamba example), **no engine PR**. Only a genuinely new control *shape* that
80:    `flagSelects` can't express would need a one-time generic primitive (never a
81:    model-named handler) on a separate prior PR (engine-axis.md).
82: 5. **`github.cookbookModel` must be set** (`<hf-org>/<page-slug>`, e.g.
83:    `qwen/qwen3.5`) and the block never pruned — without it Submit ↗ mislabels
84:    as deepseek-v4. The issue template itself needs NO edits (free-form input).
85: 6. **Strategy tiers are signal-driven.** A cell goes under `low-latency` /

## OSCAR/.agents/skills/cookbook-migrate-model/references/dimension-mapping.md
[...]
13: | model-size / model-name radio | `variants` | One variant per deployable checkpoint family; single `{id:"default"}` when there's no variant axis (then `modelNames` keys drop the variant half). |
14: | quantization radio | `quantizations` | Real precision ids (`bf16`/`fp8`/`fp4`/`int4`/…). One `fp4` id even when checkpoints differ per vendor — route via `hw\|variant\|quant` triple keys in `modelNames` (NVFP4 on Blackwell vs AMD MXFP4 is the precedent); per-hw greying falls out of which cells exist. |
15: | toggle that **couples** with other parts of the command (changes TP/mem/EP), OR one the legacy page labels with **operating-point words** | `strategies` | The Playground applies pure flag diffs — it cannot do coupled changes. Example: Qwen3.5's MTP toggle bumps TP on three H100 combos → strategies `low-latency` (MTP on) / `high-throughput` (MTP off). **Naming counts like coupling**: GLM-5.1's / Kimi-K2.6's `dpattention` adds only `--attn-dp-size N` (uncoupled), but its options are subtitled "Low Latency" / "High Throughput" — the page's own named operating-point split → strategies; a flag-only spec toggle riding alongside it stays a Playground axis and bakes per its legacy default. GPU-count radios (GLM-4.7, MiniMax-M2.5/2.7) → budget-tier strategies with the legacy SUPPORT matrix preserved by which cells exist. Strategy count follows the page's operating points: 1 → `balanced`, 2 → `low-latency`+`high-throughput`, 3 → the full trio (§4). |
16: | toggle that only adds/removes its own flags | Playground axis (+ bake, EXCEPT parsers and accuracy-degrading flags) | **Parsers (`--reasoning-parser` / `--tool-call-parser`) are NEVER baked into cells** — Deployment commands ship without them regardless of the legacy default or the measured command; the `parsers` axis adds them on top (DSv4 convention; cells mirror the legacy generator's parsers-OFF output). Accuracy-degrading toggles are never baked either — §2 caveats (axis-only, accuracy-safe cells). Other flag-only toggles: legacy default ON → bake into cells AND declare the axis so users can strip (red strikethrough); default OFF → keep cells clean, axis preset only. MTP/EAGLE presets → `speculative` axis; dp-attention → a strategy when the legacy page labels it as the operating-point split or when coupled (see the row above), else `attention.dpAttn`. **EVERY legacy control survives as an interactive control** (a dimension or a Playground axis), never a tips-only mention — but a model-specific control is **config DATA, not engine code**: the axis handler reads options/flags/env/gating straight from `config.playgroundFeatures` (MegaMoE W4A4 is entirely DSv4 config data on the existing `moe` axis — no per-model engine edit). A control that fits an existing axis's data schema is therefore pure config, full stop. A **titled single-select that strips a flag family** (e.g. Nemotron3's "KV Cache DType" `--kv-cache-dtype`) is covered by the merged generic **`flagSelects`** axis → **config-only**: declare a `flagSelects` list of `{ id, title, stripPrefixes, options }` (see the Qwen3.5 mamba example), **no engine PR**. Only a control whose *shape* `flagSelects` still can't express would need a new ONE-TIME generic primitive (never a model-named handler) on a prior engine PR; the backward-compat reasoning (opt-in per key, not in the opt-out set) is in engine-axis.md. |
17: | per-combo hidden option (e.g. spec hidden on Xeon) | absent cells | Don't create cells for combos the legacy widget couldn't produce; the engine greys them automatically. `# Error:` pseudo-commands → no cell + explanation in §2 tips and/or a chip `disable`/`disableReason`. |
18: | coupled secondary knob (e.g. mamba cache V1/V2) | cells + Playground axis | Bake the correct value per cell following the legacy coupling (Qwen3.5: MTP ⇒ `--mamba-radix-cache-strategy extra_buffer` on NVIDIA; AMD/Xeon ⇒ V1/no flag) and document the coupling in §2 tips — AND surface the knob as a Playground axis like every other legacy feature (row above; add the axis when none fits). Baking alone is NOT enough — the every-feature rule supersedes the pilot's cells+prose-only treatment of Qwen3.5's mamba knob (retrofit pending). The mamba knob is the same single-select shape as KV Cache DType, so it rides the merged generic **`flagSelects`** axis — Qwen3.6 / Qwen3-Coder-Next declare it purely in config (a `flagSelects` block), **no engine PR**. |
19: 
20: ## 2. Command rewrite table (the ONLY allowed normalizations)
[...]
78: **collapse aliases**: NEXTN is an alias of EAGLE (§2 rewrite table), so a page
79: benchmarked with NEXTN ships a single `eagle` preset, not both. (Pilot history:
80: Qwen3.5 once shipped both; corrected to EAGLE-only.)
81: 
82: **MTP `--max-running-requests` hint (engine, automatic):** when a cell's
[...]
96:   SKILL.md hard rule 3). Order `cells[]` so the verified flagship cell is
97:   **first** — `cells[0]` is the page's initial selection.
98: - When the measured command and the generator default disagree (Qwen3.5: bench
99:   ran `NEXTN` + `SGLANG_USE_CUDA_IPC_TRANSPORT=1`, generator emitted `EAGLE` +
100:   fusion flags), the verified cell mirrors the measurement; the generator
[...]
163: low-batch Marlin recipe — the recipe's own SGLang-legible content is the
164: evidence); a general-purpose recipe with no latency/throughput slant goes to
165: `balanced` (Qwen3.5's Xeon → `balanced`). Never park a no-slant recipe under
166: `low-latency`/`high-throughput` just because the page's toggle mapping lands
167: there — that reads as a semantic lie ("CPU = high-throughput?"). The page's
[...]
178: | Family | strategies | Notes |
179: |---|---|---|
180: | Gemma4 | `low-latency` (MTP on — the legacy toggle's own "Lower Latency" subtitle) / `high-throughput` (MTP off); mi300x hides the toggle → its single recipe → `balanced` (trio union, Qwen3.5 Xeon pattern) | variants = e2b/e4b/12b/31b/26b-a4b; checkpoint radio Standard(BF16)/QAT(q4_0) → quant ids via `modelNames`; §3.3 prose carries AMD recipes beyond the widget's mi300x — maintainer call on cells-from-prose vs tips; vision/audio invocation prose carries over (deployment matrix is text-standard); "gemma4 branch" version → speed drops, MMLU/GSM8K accuracy keeps (mind the few-shot vs run_eval harness footnote); dedicated multi-arch dev images verbatim |
181: | Nemotron3-Ultra | dpattention carries "Low latency"/"High throughput" subtitles (naming rule) but THREE perf controls stack — multi-value DP-Attention (2/4/8) × MTP × EP — design the tier mapping via the step-2 table; maintainer sign-off required | NVIDIA-only (h100→gb300) with a per-quant verified-hw SUPPORT matrix → absent cells; "Model" radio = the quant dim (BF16 / NVFP4 Blackwell-only); TP radio 8/16 — TP=16 is 2-node → `nodes` dim; **kvcache radio (None/fp8_e4m3/bf16) → `flagSelects` axis, config-only** (the generic primitive merged in #28128 — NO engine PR); `launch_server` + spec-V2 env prefix verbatim; dedicated `dev-nemotron3-ultra(+cu13)` images verbatim ("not in any stable release"); **"main branch" version is non-reproducible → drop the WHOLE measured result (speed AND accuracy)** unless it can be pinned to the support PR/commit (day-0 rule, §hard-rule-2) |
182: | GLM-4.5, GLM-4.6 | `low-latency` (TP, + MTP from the legacy checkbox) / `high-throughput` (TP+DP+EP) | |
[...]
186: | Kimi-K2 | `low-latency` (tp8) / `high-throughput` (dp4+ep4) | variants = instruct/thinking; reasoning chip `hide` on instruct |
187: | Kimi-K2.5, K2.6 | `low-latency` (dpattention off) / `high-throughput` (dpattention on) — same named-subtitle pattern as GLM-5.1 | K2.5 spec preset carries `--speculative-draft-model-path …eagle3-mla`, chip-gated to h200/b300; K2.6's live page has a NVIDIA-only spec toggle, default OFF → `speculative` axis only, no bake (missed by the survey) |
188: | Qwen3.6, Qwen3-Next | `low-latency` (MTP on, the legacy speculative toggle) / `high-throughput` (MTP off); Xeon hides the toggle → its single recipe → `balanced` (page ships the trio) | same pattern as the Qwen3.5 pilot |
189: | Kimi-Linear, MiniMax-M2, Qwen3, Qwen3-Coder, Qwen3-Coder-Next | single `balanced` — one recipe, no performance toggle (rule above: 1 operating point → `balanced`) | renders as one chip; Qwen3-Coder-Next has NO speculative dim on the live page (quant × toolcall × mambaCache only — an earlier sketch wrongly lumped it with Qwen3.6) |
190: | MiniMax-M2.5, M2.7 | `low-latency`(2) / `balanced`(4) / `high-throughput`(8=tp8+ep8) — confirm naming, tiers are GPU budgets | Xeon (M2.7) is a single no-slant recipe (fixed TP=6) → `balanced` (per-combination rule, Qwen3.5 Xeon precedent) |
191: | Qwen3.5 (DONE — pilot) | `low-latency` (MTP on) / `high-throughput` (MTP off); Xeon's single no-slant recipe → `balanced` (the page ships the full trio) | see §5 |
192: 
193: Qwen3 variant fan-out: variants = deployable checkpoints size-ordered
[...]
196: the ones the legacy page actually measured.
197: 
198: ## 5. Worked example — the Qwen3.5 pilot (PR #27848)
199: 
200: Decisions log, in the order they came up:
201: 
202: 1. **Strategy split over Playground toggle** because MTP couples with TP on
203:    three H100 combos (35B/27B BF16: tp2↔tp1+mem0.88; 122B FP8: tp4↔tp2).
204:    Canonical naming: `low-latency` = MTP on (legacy default), `high-throughput`
205:    = MTP off. Xeon has a single operating point (the legacy widget hid the MTP

## OSCAR/.agents/skills/cookbook-review-pr/SKILL.md
[...]
228: - **NVFP4** checkpoints are Blackwell-only (B200/B300/GB300) — never AMD. An AMD FP4 cell
229:   is legitimate ONLY when the vendor published an **MXFP4** checkpoint for it (e.g.
230:   `amd/Qwen3.5-397B-A17B-MXFP4` on MI355X) — verify the HF repo resolves; otherwise the
231:   AMD FP4 chip must be absent/`disabled`.
232: - BF16 / FP8 work on NVIDIA and AMD. `--kv-cache-dtype fp8_e4m3` in a cell is an

## OSCAR/.agents/skills/generate-profile/SKILL.md
[...]
21: ```
22: 
23: - Default model: `Qwen/Qwen3-8B` (good balance of speed and quality)
24: - Default port: `30000`
25: - The server runs in the background. Save the PID for cleanup.
[...]
50: ```
51: 
52: - Expected accuracy: **> 0.8** for capable models (Qwen3-8B, Llama-3.1-8B-Instruct, etc.)
53: - This is a quick sanity check, not a rigorous benchmark.
54: - If accuracy is unexpectedly low, something is wrong — do not proceed to profiling.
[...]
100: # 1. Launch server
101: source cleanup/bin/activate
102: CUDA_VISIBLE_DEVICES=1 sglang serve --model-path Qwen/Qwen3-8B --port 30000 &
103: 
104: # 2. Wait for ready

## OSCAR/.agents/skills/llm-torch-profiler-analysis/SKILL.md
[...]
125: | `Qwen/Qwen2.5-7B-Instruct` | `1x H100` | prefill `4090->1`, decode `1->2048` | generated separate traces; prefill kernel table captured 28-layer GEMM/FA3/RMSNorm work, decode captured 5-step graph launches, and fuse rows were split by stage |
126: | `Qwen/Qwen2.5-14B-Instruct` | `1x H100` | prefill `4090->1`, decode `1->2048` | generated separate traces; prefill kernel table captured 48-layer GEMM/FA3/RMSNorm work, decode captured 5-step graph launches, and fuse rows were split by stage |
127: | `Qwen/Qwen3-8B` | `2x H100`, TP=2 | prefill `4090->1`, decode `1->2048`, warmup 10/capture 5 | generated separate prefill/decode traces and all three tables; unique probe prompts avoided prefix-cache pollution in the prefill table |
128: | `mistralai/Mistral-7B-Instruct-v0.3` | `2x H100`, TP=2 | prefill `4090->1`, decode `1->2048`, warmup 10/capture 5 | generated separate prefill/decode traces and all three tables; server logs showed no repeated-prompt prefix-cache shortcut during the active prefill window |
129: 
[...]
137: The 2026-05-01 two-card validation artifacts for the additional models are:
138: 
139: - `/data/bbuf/validate/core_skill_validation_20260501/qwen3_8b/profiler`
140: - `/data/bbuf/validate/core_skill_validation_20260501/mistral_7b_instruct_v03/profiler`
141: 

## OSCAR/.agents/skills/llm-torch-profiler-analysis/references/fuse-overlap-catalog.md
[...]
76: | Fused sampling temperature + softmax | `fused_temperature_softmax*` | `python/sglang/srt/layers/fused_sampling.py`<br>`python/sglang/srt/layers/sampler.py` | Triton single-pass / multi-pass kernels fuse temperature scaling and softmax during decode | Separate temp-divide + softmax at decode batch sizes is often a missed existing fusion. |
77: | Fused logit softcap | `fused_softcap`<br>`final_logit_softcapping` | `python/sglang/srt/layers/elementwise.py`<br>`python/sglang/srt/layers/logits_processor.py` | Triton kernels fuse cast-to-float and softcap / tanh math for logits or generic elementwise softcapping | Treat exposed cast + softcap ladders as an existing Triton fuse family. |
78: | Linear-attention packed projection reshuffle | `fused_qkvzba_split_reshape_cat*`<br>`qkvz_proj`<br>`ba_proj`<br>`qkvabz_proj`<br>`fused_qkvbfg_a_proj` | `python/sglang/kernels/ops/attention/triton_gdn_fused_proj.py`<br>`python/sglang/srt/models/qwen3_next.py`<br>`python/sglang/srt/models/qwen3_5.py`<br>`python/sglang/srt/models/kimi_linear.py`<br>`python/sglang/srt/models/jet_nemotron.py` | GDN / Kimi / Jet-style linear-attn models pack multiple projections, then fuse split / reshape / cat into one kernel | Treat split reshape / transpose / cat ladders as an existing linear-attention fusion family. |
79: | Fused GDN gating prep | `fused_gdn_gating`<br>`softplus`<br>`beta_output` | `python/sglang/srt/layers/attention/fla/fused_gdn_gating.py` | Triton kernel computes GDN gate preparation such as `-exp(A_log) * softplus(...)` and `sigmoid(b)` together | On GDN traces, treat split gate-prep elementwise kernels as missing existing fusion first. |
80: | Fused RMSNorm-gated linear-attention output | `FusedRMSNormGated`<br>`layer_norm_gated_fwd` | `python/sglang/srt/layers/attention/fla/fused_norm_gate.py`<br>`python/sglang/srt/models/qwen3_next.py`<br>`python/sglang/srt/models/kimi_linear.py` | One Triton op covers residual-aware (RMS)Norm plus sigmoid / swish gating | If norm and output gate appear as separate kernels in GDN / Kimi-like blocks, first suspect a missing existing fusion. |
[...]
90: | --- | --- | --- | --- | --- |
91: | Single-batch overlap (SBO) | MoE combine, down-gemm, shared-expert work in nearby two-stream windows | `python/sglang/srt/batch_overlap/single_batch_overlap.py` | combine vs down-gemm overlap, combine vs shared-expert overlap, one-stream dispatch+shared overlap, explicit SM partitioning and events | If exposed MoE combine sits near neighboring compute, classify it against SBO before calling it new overlap. |
92: | Q and K normalization on different streams | Q-side norm and K-side norm on different streams | `python/sglang/srt/models/utils.py::apply_qk_norm`<br>`python/sglang/srt/models/qwen3.py`<br>`python/sglang/srt/models/qwen3_next.py`<br>`python/sglang/srt/models/qwen3_5.py` | Q stays on current stream, K can run on `alt_stream` in capture mode | Treat split Q / K norm as an existing overlap family when `alt_stream` is already wired. |
93: | DeepSeek shared-expert / routed-expert overlap | shared-expert GEMMs near DeepEP dispatch / combine | `python/sglang/srt/models/deepseek_v2.py`<br>`python/sglang/srt/batch_overlap/single_batch_overlap.py` | shared experts on `alt_stream`, overlap with dispatch / combine and down-gemm, Blackwell-specific env gating | This is an established routed-vs-shared branch overlap pattern, not a novel idea. |
94: | Llama4 shared branch vs routed branch overlap | shared expert branch plus routed MoE branch as adjacent windows | `python/sglang/srt/models/llama4.py` | shared expert on current stream, router + topk + routed experts on `alt_stream` | Use Llama4 as the first precedent for branch-level overlap in similar sparse models. |
[...]
145: | PR `#21491` FlashInfer TRTLLM FP8 MoE with fused shared experts | `num_fused_shared_experts`<br>`trtllm_fp8_block_scale_moe` | `PR #21491`<br>`python/sglang/srt/layers/moe/fused_moe_triton/fused_moe.py`<br>`python/sglang/srt/models/deepseek_v2.py` | FlashInfer TRTLLM FP8 MoE path can fuse shared experts inside the routed MoE kernel | On FP8 TRTLLM MoE discussions, treat fused shared experts as an upstream pattern that already has a concrete PR. |
146: | PR `#22005` fused add + RMSNorm + per-token FP8 quant | `fused_add_rmsnorm_per_token_quant`<br>`per_token_quant_fp8` | `PR #22005`<br>`python/sglang/kernels/jit/csrc/elementwise/fused_add_rmsnorm_per_token_quant.cuh`<br>`python/sglang/kernels/jit/fused_add_rmsnorm_per_token_quant.py` | CUDA JIT kernel keeps normed values in registers and emits BF16 + FP8 outputs plus per-token scales | If FP8 online-quant traces show add+norm followed by per-token quant, treat this as an in-flight upstream CUDA fuse family. |
147: | PR `#20667` Qwen3.5 fused QK norm + RoPE + KV cache write | `fused_qk_norm_rope_cache_pts_quant_shuffle`<br>`fused_qk_norm_mrope_3d_cache_pts_quant_shuffle`<br>`rotary_dim` | `PR #20667`<br>`python/sglang/srt/models/qwen3_5.py`<br>`python/sglang/srt/models/utils.py` | ROCm / AITER path fuses Q / K RMSNorm, partial or 3D RoPE, and direct KV cache write for Qwen3.5 attention | Treat split QK-norm + RoPE + cache-store on Qwen3.5 as a concrete in-flight upstream family, not a novel idea. |
148: | PR `#22392` CUTLASS FP8 GEMM replacing nvjet | `cutlass_scaled_mm`<br>`fp8_scaled_mm`<br>`nvjet`<br>`cudaMemsetAsync` | `PR #22392`<br>`python/sglang/kernels/aot/python/sgl_kernel/gemm.py`<br>`python/sglang/srt/layers/quantization/fp8_utils.py` | Runtime replacement swaps nvjet FP8 GEMMs for CUTLASS kernels, removing per-launch memset bubbles and extra output-copy kernels | Treat nvjet GEMM + memset bubble ladders as an in-flight SGLang linear-kernel family before calling them novel. |
149: | PR `#18612` NVFP4 CUTLASS MoE fused SiLU+Mul+quant | `silu_and_mul_scaled_nvfp4`<br>`nvfp4 expert quant`<br>`cutlass moe` | `PR #18612`<br>`python/sglang/srt/layers/moe/cutlass_w4a8_moe.py`<br>`python/sglang/kernels/ops/quantization/nvfp4_gemm_swiglu_nvfp4_quant.py` | Fuses MoE activation epilogue and NVFP4 expert quantization before the CUTLASS MoE second GEMM | Treat split SiLU+Mul then NVFP4 expert quant in CUTLASS MoE traces as an in-flight upstream SGLang family. |
[...]
306: | PR `#41441` DSV4 all-reduce plus `mhc_post` fusion | `DSV4`<br>`AR+mhc_post`<br>`allreduce`<br>`mhc_post` | `PR #41441`<br>`vllm/model_executor/models/deepseek_v2.py`<br>`vllm/compilation/passes/fusion` | Fuses or overlaps DSV4 all-reduce with post-MLA head-compute work | Treat all-reduce followed by `mhc_post` in DSV4 traces as an in-flight vLLM overlap/fusion family. |
307: | PR `#41446` AMD GatedDeltaNet FLA prefill kernels | `GatedDeltaNet`<br>`FLA prefill`<br>`AMD`<br>`Qwen3-Next` | `PR #41446`<br>`vllm/model_executor/models/qwen3_next.py`<br>`vllm/v1/attention` | Optimizes GatedDeltaNet / FLA prefill kernels on AMD linear-attention models | Treat split GDN prefill kernels on ROCm as an in-flight upstream family. |
308: | PR `#39748` dual-stream GDN input projection | `dual-stream`<br>`input projection`<br>`GatedDeltaNet`<br>`Qwen3.5` | `PR #39748`<br>`vllm/model_executor/models/qwen3_next.py` | Overlaps sibling input-projection branches for Qwen3 / Qwen3.5 GDN-style blocks | Treat serial GDN input projections as a known in-flight overlap opportunity. |
309: | PRs `#41433` / `#41434` / `#41429` / `#40561` GPU/CPU sync removal | `GPU->CPU sync`<br>`cpu sync`<br>`item()`<br>`non_blocking` | `PR #41433`<br>`PR #41434`<br>`PR #41429`<br>`PR #40561` | Removes or gates accidental GPU-to-CPU synchronization points and adds sync-detection coverage | Treat CPU gaps next to small GPU kernels as an upstream vLLM sync-removal family before proposing a kernel-only fix. |
310: | PR `#36823` vLLM IR `fused_add_rms_norm` overload | `vllm_ir`<br>`fused_add_rms_norm`<br>`maybe_inplace` | `PR #36823`<br>`vllm/compilation/passes/ir`<br>`vllm/compilation/passes/fusion/rms_quant_fusion.py` | Extends vLLM IR lowering so fused-add-RMSNorm variants remain visible to later compile-time fusions | Treat missing norm/quant compile fusion as potentially an IR-lowering visibility issue. |

## OSCAR/.agents/skills/llm-torch-profiler-analysis/references/overlap-catalog.md
[...]
47: | --- | --- | --- | --- | --- |
48: | Single-batch overlap (SBO) | MoE combine, down-gemm, shared-expert work in nearby two-stream windows | `python/sglang/srt/batch_overlap/single_batch_overlap.py` | combine vs down-gemm overlap, combine vs shared-expert overlap, one-stream dispatch+shared overlap, explicit SM partitioning and events | If exposed MoE combine sits near neighboring compute, classify it against SBO before calling it new overlap. |
49: | Q and K normalization on different streams | Q-side norm and K-side norm on different streams | `python/sglang/srt/models/utils.py::apply_qk_norm`<br>`python/sglang/srt/models/qwen3.py`<br>`python/sglang/srt/models/qwen3_next.py`<br>`python/sglang/srt/models/qwen3_5.py` | Q stays on current stream, K can run on `alt_stream` in capture mode | Treat split Q / K norm as an existing overlap family when `alt_stream` is already wired. |
50: | DeepSeek shared-expert / routed-expert overlap | shared-expert GEMMs near DeepEP dispatch / combine | `python/sglang/srt/models/deepseek_v2.py`<br>`python/sglang/srt/batch_overlap/single_batch_overlap.py` | shared experts on `alt_stream`, overlap with dispatch / combine and down-gemm, Blackwell-specific env gating | This is an established routed-vs-shared branch overlap pattern, not a novel idea. |
51: | Llama4 shared branch vs routed branch overlap | shared expert branch plus routed MoE branch as adjacent windows | `python/sglang/srt/models/llama4.py` | shared expert on current stream, router + topk + routed experts on `alt_stream` | Use Llama4 as the first precedent for branch-level overlap in similar sparse models. |

## OSCAR/README.md
[...]
1: <p align="center">
2:   <img src="materials/oscar_logo_kv_transparent.png" alt="OSCAR INT2 KV-Cache" width="180"/>
3: </p>
4: 
5: # OSCAR
6: 
7: ### Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization
[...]
9: <p align="center">
10:   <a href="https://arxiv.org/pdf/2605.17757"><img src="https://img.shields.io/badge/Paper-arXiv-b31b1b?logo=arxiv&logoColor=white" alt="Paper"/></a>
11:   <a href="https://oscar-quantize.github.io/"><img src="https://img.shields.io/badge/Website-oscar--quantize-1f77b4?logo=googlechrome&logoColor=white" alt="Website"/></a>
12:   <a href="https://huggingface.co/Zhongzhu/OSCAR-RotationZoo"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-RotationZoo-FFD21E" alt="HuggingFace RotationZoo"/></a>
13:   <br/>
14:   <a href="https://huggingface.co/Zhongzhu/OSCAR-LLAMACPP-Qwen3-32B-INT2-KV"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20GGUF%20Qwen3--32B-INT2%20KV-FFD21E" alt="GGUF Qwen3-32B INT2 KV"/></a>
15:   <a href="https://huggingface.co/Zhongzhu/OSCAR-LLAMACPP-Gemma-4-12B-it-INT2-KV"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20GGUF%20Gemma--4--12B--it-INT2%20KV-FFD21E" alt="GGUF Gemma 4 12B it INT2 KV"/></a>
16:   <a href="https://huggingface.co/Zhongzhu/OSCAR-LLAMACPP-Qwen3-4B-Thinking-2507-INT2-KV"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20GGUF%20Qwen3--4B--Thinking--2507-INT2%20KV-FFD21E" alt="GGUF Qwen3-4B Thinking 2507 INT2 KV"/></a>
17: </p>
18: 
19: OSCAR stores the bulk of the KV cache in **2 bits** and keeps only a small BF16 sink and recent window. Each (layer, KV head) gets a rotation built from attention-aware covariance (an eigenbasis followed by a Hadamard, so every channel carries a similar share of the energy), a key mean that is subtracted before quantization, and a clipping threshold, so that four levels per row are enough. The rotation is fit **at server start** or offline on a small calibration set. With the per-row scale and zero included this is 2.25–2.5 bits per element: **6–7× more KV tokens than BF16 in the same memory** on most models, 4× for MLA latents. At 128K context and batch 1 the INT2 decode runs at **1.03–1.16× FlashInfer BF16 on H100** for dense models and 0.73–0.94× on B200.
20: 
21: <p align="center">
22:   <img src="materials/OSCAR_pipeline.png" alt="OSCAR pipeline" width="720"/>
23: </p>
24: 
25: This repository is upstream SGLang `main` with the OSCAR low-bit KV cache added under `python/sglang/`. A llama.cpp port (Metal and CPU) lives on the [`zhongzhu/llamacpp`](https://github.com/FutureMLS-Lab/OSCAR/tree/zhongzhu/llamacpp) branch, and pre-fit rotations are on the [RotationZoo](https://huggingface.co/Zhongzhu/OSCAR-RotationZoo).
26: 
27: ## 🔥 Latest News
28: - **[2026-10-12]** Main results refreshed for **13 models** on the current tree (commit `9105559e8e`, upstream base `67eab57057`): GPQA-Diamond at a 64K budget, KL against BF16 at 128K on PG-19, and 128K decode on B200 and H100. On H100 the INT2 decode is **faster than FlashInfer BF16** on dense models (1.03–1.16× at 128K, batch 1); on B200 it is 0.73–0.94× after raising the default INT2 split cap to 256 and dequantizing with a bf16 bit trick. Most recipes now use per-(layer, KV head) rotations with key centering and a per-head K clip.
29: - **[2026-10-03]** OSCAR moved onto **upstream SGLang main** (base `67eab57057`, the official nightly of 2026-10-02): the repository root is upstream and OSCAR is the diff. Every INT2 arm runs the model's own attention (DSA for GLM-5.x, MSA for MiniMax-M3, MLA + KDA across two nodes for Kimi-K3). Rotations can be **fit at server start**, and 1-bit / 1.5-bit K via product quantization ships as an opt-in tier.
30: - **[2026-10-03]** Dense INT2 decode on B200 went from 2–3.9× to 1.2–1.5× of FlashInfer BF16 at 64K / batch 1: a separate INT2 split cap, a fused HP + INT2 stage-1, batched decode rotations, a parallel stage-2 and a parallel metadata build, all default-on and checked bit-for-bit against the two-launch path.
31: - **[2026-06-26]** OSCAR is PRing into **vLLM** too, bringing INT2 KV cache support to another high-throughput serving stack.
32: - **[2026-06-07]** OSCAR INT2 KV cache now runs **256K Gemma 4 12B under <code style="color : Red">!!16GB!!</code>** and **Qwen3** on the [`zhongzhu/llamacpp` llama.cpp fork](https://github.com/FutureMLS-Lab/OSCAR/tree/zhongzhu/llamacpp) — **~8× smaller KV at near-f16 quality**, with [pre-built `*-rot-kv.gguf` on Hugging Face](https://huggingface.co/Zhongzhu/OSCAR-LLAMACPP-Gemma-4-12B-it-INT2-KV). RUN GEMMA 4 / QWEN3 with LONG CONTEXT on your LOCAL MAC!
33:   <details>
34:   <summary> <b>MacBook M5 Max Gemma 4 12B OSCAR INT2 KV Local Run Video</b></summary>
35:   <img width="960" height="502" alt="Screen Recording 2026-06-08 at 00 47 11 - 2x" src="https://github.com/user-attachments/assets/72f7c51d-fb43-42b7-ac2b-1b5baaf256c5" />
36:   </details>
[...]
39: <summary><b>More news</b></summary>
40: 
41: - **[2026-06-05]** OSCAR now runs its INT2 KV cache through a fused mixed-precision Flash-Attention kernel on Apple Metal in the [`zhongzhu/llamacpp` llama.cpp fork](https://github.com/FutureMLS-Lab/OSCAR/tree/zhongzhu/llamacpp), making long-context decode up to ~15× faster (near-BF16) at ~7× less KV memory. Try to RUN QWEN-3-32B with LONG CONTEXT in your LOCAL MAC!
42:   <details>
43:   <summary><b>MacBook M5 Max Qwen3-32B OSCAR INT2 KV Local Run Screenshot</b></summary>
44:   <img width="1003" height="654" alt="Screenshot 2026-06-05 at 09 57 31" src="https://github.com/user-attachments/assets/8ea1ccf9-c2f0-4f3e-8232-7f0b2dbdd144" />
45:   </details>
46: - **[2026-06-04]** OSCAR now supports **Gemma 4 12B** with **SGLang INT2 KV cache** on the [`zhongzhu/gemma4-12b`](https://github.com/FutureMLS-Lab/OSCAR/tree/zhongzhu/gemma4-12b) branch.
47: - **[2026-05-31]** OSCAR is now runnable on the zhongzhu/llamacpp branch of **llama.cpp**. Feedback and suggestions are very welcome!
48: - **[2026-05-23]** OSCAR released the Qwen3.5 4B, 35B-A3B and MiniMax-M2.7 229B preview results (branch zhongzhu/hybrid-model at the time; these models now run from this tree).
49: - **[2026-05-18]** Full release: [paper](https://arxiv.org/pdf/2605.17757), code, [website](https://oscar-quantize.github.io/), and [RotationZoo](https://huggingface.co/Zhongzhu/OSCAR-RotationZoo) are all live — runs out of the box on **SGLang**.
50: 
51: </details>
[...]
66: |:---|:---|:---:|:---:|:---:|:---:|:---:|
67: | Qwen3-4B-Thinking-2507 | dense GQA | 66.7 → 60.1 | 0.096 | 124.7 / 157.8 (0.79×) | 111.0 / 96.0 (**1.16×**) | 6.4× |
68: | Qwen3-8B | dense GQA | 59.1 → 55.6 | 0.097 | 110.4 / 134.3 (0.82×) | 91.2 / 79.1 (**1.15×**) | 6.4× |
69: | Qwen3-32B | dense GQA | 62.6 → 64.1 | 0.087 | 72.9 / 87.3 (0.84×) | 55.5 / 53.2 (**1.04×**) | 6.4× |
70: | Qwen3-30B-A3B | MoE, dense GQA (4 KV heads) | 62.6 → 56.6 | 0.104 | 189.3 / 237.5 (0.80×) | 174.0 / 168.6 (**1.03×**) | 6.4× |
71: | Qwen3.5-4B | hybrid GatedDeltaNet + GQA | 76.3 → 76.8 | 0.031 | 232.7 / 276.7 (0.84×) | 193.6 / 185.4 (**1.04×**) | 7.1× |
72: | Qwen3.5-35B-A3B | hybrid GatedDeltaNet + GQA, MoE | 80.8 → 81.3 | 0.032 | 259.4 / 307.4 (0.84×) | 271.3 / 283.7 (0.96×) | 7.1× |
73: | Qwen3.8-27B | hybrid GatedDeltaNet + GQA | 88.4 → 86.9 | 0.029 | 125.5 / 139.4 (0.90×) | 79.9 / 79.7 (1.00×) | 7.1× |
74: | Gemma-4-12B-it | hybrid SWA, two head geometries | 64.1 → 62.6 | 0.175 | 98.9 / 165.1 (0.60×) ¹ | 73.5 / 30.0 ¹ | 5.1× |
75: | MiniMax-M2.7 | dense GQA, FP8 weights | 83.3 → 83.8 | 0.077 | 104.7 / 111.4 (0.94×) | 131.6 / 119.6 (**1.10×**) | 6.4× |
[...]
93: 
94: ```bash
95: git clone --recursive https://github.com/FutureMLS-Lab/OSCAR.git && cd OSCAR
96: mkdir -p ctx/oscar-src
97: git archive --format=tar HEAD | tar -x -C ctx/oscar-src
98: git -C third_party/simple_evals archive --format=tar HEAD | tar -x -C ctx/oscar-src/third_party/simple_evals
99: printf '%s %s\n' "$(git branch --show-current)" "$(git rev-parse --short HEAD)" > ctx/oscar-src/BUILT_FROM
100: hf download Zhongzhu/OSCAR-RotationZoo --local-dir ctx/rotations/zoo
101: docker build -f docker/Dockerfile.oscar --build-arg IMAGE_TAG="$(git rev-parse --short HEAD)" -t oscar-env:local ctx
102: ```
103: 
[...]
106: ```bash
107: docker run --gpus all --rm -it --shm-size 32g -p 30000:30000 \
108:   -v "$HOME/.cache/huggingface:/root/.cache/huggingface" -e HF_TOKEN oscar-env:local bash
109: 
110: # inside the container: the Qwen3-8B recipe's windows and clips
111: SGLANG_ENABLE_MIXED_KV_WINDOWS=1 \
112: SGLANG_MIXED_KV_PREFIX_TOKENS=128 SGLANG_MIXED_KV_RECENT_TOKENS=512 \
113: SGLANG_OSCAR_K_CLIP_RATIO=0.96 SGLANG_OSCAR_V_CLIP_RATIO=0.92 \
114: python -m sglang.launch_server --model-path Qwen/Qwen3-8B \
115:   --kv-cache-dtype int2 --kv-cache-quant-group-size 128 \
116:   --attention-backend triton --host 0.0.0.0 --port 30000
[...]
121: ```bash
122: curl http://localhost:30000/v1/chat/completions -H 'Content-Type: application/json' \
123:   -d '{"model": "Qwen/Qwen3-8B", "messages": [{"role": "user", "content": "What is 2-bit KV cache quantization?"}]}'
124: ```
125: 
[...]
127: 
128: ```bash
129: oscar-selfcheck                                        # image tag and the commit it was built from
130: bash /oscar/src/rotation/run/qwen3-8b.sh               # GPQA-Diamond with the INT2 KV cache
131: KV_MODE=bf16 bash /oscar/src/rotation/run/qwen3-8b.sh  # the paired BF16 control
132: bash /oscar/src/rotation/verify/all.sh qwen3-8b        # PASS/FAIL garbling smoke, radix cache and CUDA graphs on
133: ```
134: 
[...]
142: |:---|:---|:---|:---:|
143: | `Qwen/Qwen3-4B-Thinking-2507` | dense GQA | `rotation/run/qwen3-4b-thinking.sh` | 1 |
144: | `Qwen/Qwen3-8B` | dense GQA | `rotation/run/qwen3-8b.sh` | 1 |
145: | `Qwen/Qwen3-32B` | dense GQA | `rotation/run/qwen3-32b.sh` | 2 |
146: | `Qwen/Qwen3-30B-A3B` | MoE, dense GQA | `rotation/run/qwen3-30b-a3b.sh` | 2 |
147: | `Qwen/Qwen3.5-4B` | hybrid GatedDeltaNet + GQA | `rotation/run/qwen3.5-4b.sh` | 1 |
148: | `Qwen/Qwen3.5-35B-A3B` | hybrid GatedDeltaNet + GQA, MoE | `rotation/run/qwen3.5-35b-a3b.sh` | 4 |
149: | `Qwen/Qwen3.8-27B` | hybrid GatedDeltaNet + GQA | `rotation/run/qwen3.8-27b.sh` | 2 |
150: | `google/gemma-4-12B-it` | hybrid SWA, two head geometries | `rotation/run/gemma-4-12b.sh` | 1 |
151: | `MiniMaxAI/MiniMax-M2.7` | dense GQA, FP8 weights | `rotation/run/minimax-m2.7.sh` | 4 |
[...]
161: <summary><b>Build details and what is in the image</b></summary>
162: 
163: The build context holds this tree as `./oscar-src` and the rotations as `./rotations`; `git archive` leaves submodules out, so the GPQA scorer is archived separately. The build asserts that `import sglang` inside the image resolves to this tree and that the OSCAR modules parse. Kernels are Triton and compile at first use, so the build needs no GPU. Model weights are not in the image.
164: 
165: | Path in the image | Contents |
166: |---|---|
167: | `/sgl-workspace/sglang` (also `/oscar/src`) | this tree; the image's editable `sglang` install resolves here |
168: | `/oscar/rotations/zoo/<model>/` | K/V rotations from the RotationZoo |
169: | `/oscar/IMAGE_TAG`, `/oscar/BUILT_FROM` | the tag, and the branch and commit the tree came from, so a number from a cluster can be matched to the tree that produced it |
170: | `/usr/local/bin/oscar-selfcheck` | prints the tag and commit, torch and the CUDA device, then `OSCAR_SELFCHECK_OK` once `import sglang` resolves to this tree |
171: 
172: Run `oscar-selfcheck` on a GPU node before trusting a long job to an image: it is the one check that exercises the driver.
173: 
174: </details>
[...]
177: <summary><b>Without Docker</b></summary>
178: 
179: Any environment that runs upstream SGLang at commit `67eab57057` runs OSCAR: install this tree's `python/` package in place of `sglang`, with the sgl-kernel and flashinfer builds the official nightly pins (CUDA 13.0, torch 2.13, transformers 5.17, flashinfer 0.7, sglang-kernel 0.4.8). OSCAR adds no compiled extension of its own. If you lay the tree over an existing install by hand, keep that install's prebuilt Rust extensions (`python/sglang/srt/**/*.so`): without the radix-tree core, models on `UnifiedRadixCache` fail at startup. `docker/Dockerfile.oscar` shows the exact steps.
180: 
181: </details>
[...]
188: ```bash
189: SGLANG_ENABLE_MIXED_KV_WINDOWS=1 \
190: SGLANG_OSCAR_K_ROTATION_PATH=.../k_rotation_qqt_r_h_pbr.pt \
191: SGLANG_OSCAR_V_ROTATION_PATH=.../v_rotation_sst_r_h_pbr.pt \
192: SGLANG_OSCAR_K_CLIP_RATIO=0.96 \
193: SGLANG_OSCAR_V_CLIP_RATIO=0.92 \
194: SGLANG_MIXED_KV_PREFIX_TOKENS=128 \
195: SGLANG_MIXED_KV_RECENT_TOKENS=512 \
[...]
205: | Env | Server default | Recipes | Effect |
206: |---|---|---|---|
207: | `SGLANG_MIXED_KV_PREFIX_TOKENS` / `SGLANG_MIXED_KV_RECENT_TOKENS` | 32 / 128 | 64 / 256 (Qwen3-8B 128 / 512) | BF16 sink and recent window; everything else is INT2 in groups along head_dim |
208: | `SGLANG_OSCAR_K_CLIP_RATIO` / `SGLANG_OSCAR_V_CLIP_RATIO` | 0 / 0 (no clip) | 0.96 / 0.92 | per-row clipping before min-max quantization |
209: | `SGLANG_OSCAR_K_CLIP_PER_LAYER` | `` | | per-layer K clip: a comma list in layer order, or a JSON file `{layer: ratio}` |
210: | `SGLANG_OSCAR_K_CLIP_PER_HEAD` | `` | | per-(layer, KV head) K clip: a JSON file `{"<layer>,<kv head>": ratio}`; heads it does not name keep the layer value |
211: | `SGLANG_MIXED_KV_SCALE_DTYPE` | `float32` | `float32` | dtype of the per-row scale and zero |
212: | `SGLANG_OSCAR_ABSORB_V_ROTATION` | off | off | fold the V rotation into the weights instead of applying it at runtime |
213: 
214: </details>
[...]
218: 
219: ```bash
220: hf download Zhongzhu/OSCAR-RotationZoo --include "Qwen3-8B/*" --local-dir rotzoo
221: ROT=$(ls -1d rotzoo/Qwen3-8B/seq*_prompt*_group128 | tail -1)
222: export SGLANG_OSCAR_K_ROTATION_PATH=$ROT/k_rotation_qqt_r_h_pbr.pt
223: export SGLANG_OSCAR_V_ROTATION_PATH=$ROT/v_rotation_sst_r_h_pbr.pt
224: ```
225: 
[...]
231: <summary><b>Fit the rotation at server start</b></summary>
232: 
233: When the mixed pool is active and the rotation pair is unset or missing, the server fits it before it accepts traffic: the pool starts on identity rotations, a prefill-only pass over calibration prompts collects the moments in the attention layers, the scheduler reduces them over TP and decomposes them in FP64, and the rotations are installed in place (captured decode CUDA graphs stay valid). The pair is written atomically under a lock and later launches load it from `$HF_HOME/oscar-rotations/<model>-<digest>/`.
234: 
235: | Env | Default | Effect |
236: |---|---|---|
237: | `SGLANG_OSCAR_CALIBRATION_PROMPTS_PATH` | `` | JSONL of `{"messages": [...]}` prompts (or a GPQA CSV); empty = GPQA-Diamond |
238: | `SGLANG_OSCAR_CALIBRATION_TOKENS` | 30000 | prompt tokens observed per layer |
239: | `SGLANG_OSCAR_CALIBRATION_BATCH_SIZE` | 32 | prompts per calibration request |
240: | `SGLANG_OSCAR_CALIBRATION_TIMEOUT` | 1800 | seconds before the launch fails |
241: | `SGLANG_OSCAR_CALIBRATION_LOCK_DIR` | `/tmp/sglang-oscar-locks` | lock files that serialize pair publication |
242: | `SGLANG_OSCAR_CALIBRATION_SAVE_MOMENTS` | 0 | also save the per-(layer, KV head) moments, the input to the per-head fitter below |
243: 
244: Limits: single node, DP = PP = 1, no HiCache, no torch.compile, no explicit prefill CUDA-graph backend; the first launch keeps the V rotation at runtime. For long-context serving, calibrate on prompts as long as the contexts you serve: a rotation fit on short prompts degrades at positions it never saw.
[...]
257: | `k_mean` (K) | per-head key mean subtracted before the key rotation | every stored key; all logits of a request shift by one constant, so the softmax is unchanged |
258: 
259: Shapes follow `rotation`: `[hd, hd]` (shared) or `[kv_heads, hd, hd]` (per head). Launch once with `SGLANG_OSCAR_CALIBRATION_SAVE_MOMENTS=1`, then fit any variant from the saved moments:
260: 
261: ```bash
262: python rotation/tools/fit_oscar2_variants.py --moments-dir $CAL --out $OUT \
263:     --variants perhead,center,outaware_hr --model Qwen/Qwen3-8B
264: ROT_DIR=$OUT/center bash rotation/run/qwen3-8b.sh
265: ```
266: 
[...]
280: 
281: ```bash
282: bash rotation/qwen3-8B/save_qkv_8b.sh          # 1. dump Q/K/V on calibration prompts
283: bash rotation/qwen3-8B/compute_rotation.sh     # 2. fit {k,v}_rotation_*.pt from the dump
284: ROT_DIR=$(ls -1d rotation/qwen3-8B/GPQA/seq*_prompt*_group*/rotations | tail -1) \
285:   bash rotation/qwen3-8B/eval_gpqa.sh          # 3. GPQA against the new rotation
286: ```
287: 
[...]
304: 
305: ```bash
306: SGLANG_OSCAR_K_QUANTIZER=pq SGLANG_OSCAR_PQ_K_CODEBOOK=$ROT/codebooks/k_pq_n16_c256_d8.pt       # K 1.0 bit, V INT2
307: SGLANG_OSCAR_K_QUANTIZER=pq SGLANG_OSCAR_PQ_K_CODEBOOK=$ROT/codebooks/k_rvq_n16_c256x16_d8.pt   # K 1.5 bit (RVQ)
308: SGLANG_OSCAR_V_QUANTIZER=pq SGLANG_OSCAR_PQ_V_CODEBOOK=$ROT/codebooks/v_pq_n16_c256_d8.pt       # with K pq: V 1.0 bit too
309: python rotation/tools/train_pq_codebooks.py --dumps $CALIB/qkv_dumps/gpqa \
310:   --rotation $CALIB/rotations/k_rotation_qqt_r_h_pbr.pt --tensor k --out codebooks/k_pq_n16_c256_d8.pt
[...]
318: 
319: ```
320: python/sglang/                  upstream SGLang main + the OSCAR low-bit KV cache
321:   srt/mem_cache/unified_kv_pool.py                      mixed pool: BF16 sink/recent windows + INT2 tier
322:   srt/mem_cache/unified_kv_allocator.py, allocation.py  two-tier allocator, per-request layout and flush schedule
323:   srt/mem_cache/mla_packed_kv_pool.py                   packed 2-bit MLA latent (GLM-5.x, Kimi-K3)
324:   srt/mem_cache/minimax_int2_kv_pool.py                 MiniMax-M3 pool (INT2 rows staged to BF16 for MSA)
325:   srt/mem_cache/oscar_calibration.py                    startup calibration: moments, TP reduction, eigensolve
326:   srt/mem_cache/oscar_pq_codebooks.py                   1-bit / 1.5-bit product-quantized tier
327:   srt/layers/attention/triton_ops/decode_attention.py   INT2 decode kernels (fused BF16 + INT2 stage-1, split-KV)
328:   srt/layers/attention/triton_ops/mla_packed_decode.py  packed-latent MLA decode
329:   srt/layers/attention/quantized_kv_prefill.py          INT2 prefix dequant for extend and chunked prefill
330:   srt/entrypoints/oscar_startup_calibration.py          calibrate before the server takes traffic
331:   QuantKernel/                                          write-side kernels: rotate + clip + quantize, decode flush, PQ
332: rotation/
333:   run/<model>.sh                one recipe per model (KV_MODE=bf16 for the control)
334:   verify/all.sh                 garbling smoke
335:   eval_oscar_gpqa.sh            launch + GPQA driver that every recipe wraps
336:   <model>/                      offline calibration: save_qkv_*.sh, compute_rotation.sh, eval_gpqa.sh
337:   compute_kv_rotation.py        offline eigensolve and R·H·P_br composition
[...]
341:   tests/                        CPU and GPU tests
342:   examples/, porting/           recipe table; how to port a new model
343:   OSCAR-RotationZoo/            two sample rotation sets; the full zoo is on Hugging Face
344: docker/Dockerfile.oscar         the image: official SGLang nightly + this tree
345: sglang-dump-qkv/                vendored older SGLang used by the offline Q/K/V dump
346: third_party/simple_evals/       submodule: GPQA scorer (clone with --recursive)
[...]
350: ## Troubleshooting
351: 
352: - **Hybrid models (Qwen3.5, Qwen3.8, Kimi-K3).** Their prefix cache needs `--mamba-radix-cache-strategy extra_buffer` (the recipes set it); without it the Mamba radix cache asserts `page_size == 1`, which surfaces asynchronously as an illegal memory access.
353: - **Qwen3 dense models past 40,960 tokens.** The recipes enable Qwen's YaRN ×4 recipe when the requested context exceeds 32K. When launching by hand under transformers 5, pass the YaRN dict as both `rope_parameters` and `rope_scaling` and raise `max_position_embeddings`; `rope_scaling` alone is silently ignored.
354: - **Missing rotation file.** At 2 bits a missing rotation is collapse, not a mild regression; the recipes stop with `FATAL` instead of serving without one.
[...]
358: 
359: ```bibtex
360: @misc{zhou2026oscarofflinespectralcovarianceaware,
361:       title={OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization},
362:       author={Zhongzhu Zhou and Donglin Zhuang and Jisen Li and Ziyan Chen and Shuaiwen Leon Song and Ben Athiwaratkun and Xiaoxia Wu},
363:       year={2026},

## OSCAR/benchmark/kernels/all_reduce/README.md
[...]
48: ```bash
49: python -m sglang.launch_server \
50:     --model-path Qwen/Qwen3-8B \
51:     --tp-size 8 \
52:     --enable-mscclpp

## OSCAR/benchmark/uno/README.md
[...]
23: 
24: ```bash
25: export MODEL_PATH=Qwen/Qwen3-8B
26: export TOKENIZER_PATH=Qwen/Qwen3-8B
27: export UNO_LORA_PATH=s-sahoo/uno-qwen3-8B
28: export DATA_ROOT=/path/to/math-eval-data
29: export RESULT_ROOT=/path/to/math-eval-results
[...]
122:   --max-running-requests 64 \
123:   --speculative-algorithm DFLASH \
124:   --speculative-draft-model-path z-lab/Qwen3-8B-DFlash-b16 \
125:   --speculative-dflash-block-size 8 \
126:   --speculative-draft-attention-backend fa3

## OSCAR/python/sglang/kernels/kda_kernels/README.md
[...]
21: | LTX2 QK-norm split-RoPE | `ltx2_qknorm_split_rope_jit.py` | [sgl-project/sglang#29708](https://github.com/sgl-project/sglang/pull/29708), merge commit `fcb9f229b3` |
22: | FLUX.2 FP8 producer and QKV packing fusions | `layernorm_modulate_triton.py`, `flux2_qkv_epilogue_jit.py`, `flux2_token_cat_fp8_triton.py` | [sgl-project/sglang#37162](https://github.com/sgl-project/sglang/pull/37162), merge commit `1c3ad92438` |
23: | Qwen3.8 QSA packed-varlen decode on SM121 | `qwen38_qsa_sm121/` | [radixark/KDA-1.5#4](https://github.com/radixark/KDA-1.5/pull/4) at `414ce456e14a`; see the package README |
24: 
25: For JIT kernels, the Python entry module and the corresponding source under

## OSCAR/python/sglang/kernels/kda_kernels/qwen38_qsa_sm121/README.md
[...]
1: # Qwen3.8 QSA packed-varlen decode for SM121
2: 
3: This implementation was optimized by Codex and Kimi K3 agents through
[...]
9: 
10: The kernel is specialized for the packed QSA decode tensors captured from
11: `RadixArk/Qwen3.8-Flash-Next-NVFP4` on NVIDIA GB10 (SM121):
12: 
13: - BF16 query, key, value, and output with head dimension 256
[...]
26: without a host synchronization.
27: 
28: SM121 dispatch checks the exact Qwen3.8 contract and routes directly to this
29: kernel; it is the only packed-QSA attention implementation added by this PR.
30: The KDA replay passed all 15 TP1/TP2 production tensors on two independent GB10

## OSCAR/python/sglang/srt/mem_cache/storage/flexkv/README.md
[...]
10: ---
11: 
12: ## Quick start (single H20, single GPU, Qwen3-8B)
13: 
14: This walks through everything the verification on H20-GPU-11 actually
[...]
95:   SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1 \
96:   python3 -m sglang.launch_server \
97:     --model-path /raid/fly/model/Qwen3-8B \
98:     --port 30000 --tp-size 1 \
99:     --enable-flexkv \
[...]
182:   CUDA_VISIBLE_DEVICES=0 SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1 \
183:   python3 -m sglang.launch_server \
184:     --model-path /raid/fly/model/Qwen3-8B --port 30000 --tp-size 1 \
185:     --mem-fraction-static 0.45 > /tmp/sglang.log 2>&1
186: '
[...]
193:   CUDA_VISIBLE_DEVICES=0 SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1 \
194:   python3 -m sglang.launch_server \
195:     --model-path /raid/fly/model/Qwen3-8B --port 30000 --tp-size 1 \
196:     --enable-flexkv --flexkv-config-file /raid/fly/sglang-connector-dir/flexkv_min.yaml \
197:     --mem-fraction-static 0.45 > /tmp/sglang.log 2>&1
[...]
360: ## Status
361: 
362: * MP (synchronous) path — verified end-to-end on Qwen3-8B (H20-3e):
363:   output byte-equal to no-FlexKV baseline across short / medium / long
364:   prompts. ~30–46 GB/s observed for D2H stores and ~37 GB/s for H2D
[...]
387: ## Benchmarks
388: 
389: Setup: Qwen3-8B on 1× H20. Server flags:
390: 
391:     --attention-backend triton --mem-fraction-static 0.32

## OSCAR/python/sglang/srt/mem_cache/storage/nixl/README.md
[...]
197: The following setup was validated against a hybrid Mamba model with HiCache enabled:
198: 
199: - model: `Qwen/Qwen3.5-9B`
200: - storage backend: `nixl`
201: - NIXL plugin: `POSIX`
[...]
222: 
223: ~/ve_sgl_dev/bin/sglang serve \
224:   --model-path /workspace/LLM_models/Qwen3.5-9B \
225:   --served-model-name Qwen/Qwen3.5-9B \
226:   --host 127.0.0.1 \
227:   --tp 2 \

## OSCAR/rotation/GLM-5.2-FP8/README.md
[...]
3: MLA stores one compressed latent `c_kv` (512-d) shared by all heads, plus a
4: positional `k_pe`. Only `c_kv` is quantized; `k_pe` stays BF16. Per-head
5: rotations do not apply here — there is nothing per-head to rotate.
6: 
7: Rotation is `Rcov · P · Hblock` (covariance eigenvectors, bit-reversal
8: permutation, per-group Hadamard) with **Lloyd-Max** on, group 128.
9: 
10: The BF16 sink and recent windows apply here like everywhere else: sink 64,
[...]
15: you setting those vars changed nothing. **Every number in the table below
16: predates the windows** — read them as the no-window arm, not as the recipe;
17: the next section has the windowed GPQA numbers.
18: 
19: | Benchmark | BF16 | INT2 (no window) | Δ |
20: |---|:---:|:---:|:---:|
21: | GPQA @32K | 81.3 ± 0.0 | 68.7 ± 1.8 | −12.6 |
22: | HumanEval (≤16K) | 91.5 ± 1.2 | 88.2 ± 1.5 | −3.3 |
23: | AIME 2025 | 76.7 ± 3.3 | 75.6 ± 6.9 | −1.1 (n.s.) |
24: | MATH500 | 94.8 ± 0.8 | 93.8 ± 0.3 | −1.0 |
25: 
26: Only the GPQA row has been re-measured with the windows. The other three are
27: short-generation benchmarks where truncation is not the binding constraint, so
28: expect less from the windows there — but that is an expectation, not a
[...]
38: ## What the windows are worth here
39: 
40: Full GPQA-Diamond 198, B200 TP=8, CUDA graph on, `--kv-cache-dtype bfloat16`,
41: 32K budget, single seed. The BF16 arm is a genuine unquantized pass-through
42: through the same pool class and harness: its rotation path points at a
43: nonexistent directory, so `_latent_windows` is False *and* `self.rotations` is
44: empty, and both latent setters fall through to `parent_setter` untouched
45: (`windows=off` in its log is therefore expected, not a misconfiguration).
[...]
62: moved is truncation: 29.29 % → 19.70 %, mean generation 17 % shorter. Of the 15
63: questions 64/256 still loses to BF16, **13 (86.7 %) are its own truncations and
64: only 2 are answered wrong**; on the 155 both arms answer, accuracy is 96.8 % vs
65: 96.1 %. The residual gap is budget, not corrupted answers.
66: 
[...]
88: the same 40 questions in every arm *of this subset*):
89: 
90: > **Do not pool this table with the 198-question one.** `GPQAEval.__init__`
91: > draws `rng.sample(examples, num_examples)` from the *same* `random.Random(0)`
92: > before drawing each question's option permutation, so passing
[...]
155: intended. Read back per arm:
156: 
157: | arm | `disable_radix_cache` | rotation / windows as logged |
158: |---|:---:|---|
159: | BF16 full-198 | **False** (on) | `rotation_path .../glm52-rotations-none not found — no rotation`; `windows=off` |
160: | INT2 64/256 full-198 | **False** (on) | `loaded 78 rotations`, orthogonality residual 9.11e-04; `windows=sink=64/recent=256` |
161: | INT2 no-window full-198 | **True** (off) | `loaded 78 rotations`; **no `windows=` field at all** |
162: | BF16 40-subset | **True** (off) | no rotation |
163: 
164: Two consequences, and the first supersedes what this file used to say here:
[...]
197:   window comparison is internally valid regardless.
198: 
199: ## Do not expect a better rotation to close it
200: 
201: Measured on a real `c_kv` dump (functional error, lower is better):
202: 
203: | variant | error | vs no rotation |
204: |---|:---:|:---:|
205: | no rotation | 0.0845 | — |
206: | Hadamard | 0.0839 | ≈ 0 |
207: | **`Rcov·P·Hblock`** | **0.0523** | −0.72 dB |
208: | Hadamard + HP128 | 0.0447 | −2.74 dB |
209: 
210: Only the last row reaches BF16 parity, and it costs ~6.5 bits per element, which
211: defeats the point of 2-bit. The latent is a *trained* compressed representation —
212: it has no outlier structure for a rotation to flatten. `Rcov·P·Hblock` is the
213: best of the cheap options; take it and move on.
214: 
[...]
216: 
217: ```bash
218: # 1. dump c_kv on GPQA (TP=16, 2 nodes)
219: bash save_ckv_glm52.sh
220: 
221: # 2. fit the per-layer latent rotation
222: bash compute_rotation.sh     # -> rotations/layer_*.pt
223: ```
224: 
225: Fitted rotations are published as
226: `Zhongzhu/OSCAR-RotationZoo/GLM-5.2-FP8/c_kv_rcov_phblock_g128/` — download
227: rather than re-fit unless you are changing the recipe.
228: 
[...]
232: SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1 \
233: SGLANG_LLOYD_MAX=1 \
234: SGLANG_OSCAR_MLA_KV_ROTATION_PATH=<rotations-dir> \
235: SGLANG_OSCAR_MLA_KV_GROUP_SIZE=128 \
236: python -m sglang.launch_server --model-path zai-org/GLM-5.2-FP8 \
[...]
244: version of this file:
245: 
246: * `SGLANG_OSCAR_MLA_KV_ROTATION_PATH` is the name the pool reads. It is also
247:   what *creates* the pool — misspell it (this file said
248:   `SGLANG_OSCAR_MLA_ROTATION_DIR`) and the server starts, serves, and scores
249:   with a plain BF16 latent cache and no rotation at all.
250: * `--kv-cache-dtype bfloat16`, not `int2`. `int2` aborts at argument validation
251:   on a DSA model; the latent is fake-quantized into a float cache, so that

## OSCAR/rotation/MiniMax-M2.7/README.md
[...]
1: # MiniMax-M2.7 — INT2 KV recipe
2: 
3: **Status: INT2 is at parity with BF16 here (80.56 vs 78.96 on paired GPQA-198).
4: The previously reported −21.05 pp was a harness artifact — see the first
5: section. The batch-size defect that used to require `--cuda-graph-max-bs 12`
6: is fixed (`decode_attention.py::_safe_block_h`); serve at any max-bs.**
7: 
8: Dense MHA, 62 layers, 48 Q / 8 KV heads, head_dim 128. Shared per-layer rotation
9: (`qqt_r_h_pbr` for K, `sst_r_h_pbr` for V) with the **uniform** quantizer —
10: Lloyd-Max off. Note the checkpoint itself is FP8 (`quant_method: fp8`,
[...]
15: ## Read this first: INT2 is at parity here, and the -21 pp was a harness artifact
16: 
17: INT2 KV on this model is at parity with BF16 on full GPQA-198:
18: 
19: | arm | concurrency | full-198 seeds | mean |
[...]
22: | BF16 | 7 | 78.28 / 77.78 / 80.81 | 78.96 |
23: 
24: **INT2 − BF16 = +1.6 pp.** And 80.30 reproduces the published GPQA **80.3**
25: essentially exactly, from a different harness and session — the published INT2
26: number was right all along.
[...]
79:    stay broken against the 62.5 baseline.
80: 
81:    End-to-end after the fix, full GPQA-198 at **concurrency 16, max-bs 32**
82:    (graphs on, 84-87% of decode steps replay the bs=16 graph):
83: 
[...]
125: ## Superseded: the max-bs 32 / concurrency 15 measurements
126: 
127: The graph-off control that first exposed the defect, same session, same rotation,
128: same 64/256 windows, identical concurrency 15, varying only
129: `--cuda-graph-max-bs`, matched over the same ~88 questions, 3 seeds:
[...]
142: 
143: This also reconciles the historical numbers — SWE-bench 70.8, LCB v6 68.4,
144: AIME25 90.0 and GPQA 80.3 all ran max-bs 1 and single-stream, i.e. never on the
145: broken path, so they are plausible INT2 results rather than harness flukes.
146: 
[...]
195: | Benchmark | BF16 | INT2 | Δ |
196: |---|:---:|:---:|:---:|
197: | GPQA | 78.28 | 80.3 | +2.0 |
198: | HumanEval | 88.17 | 92.1 | +3.9 |
199: | AIME 2025 (95K budget) | 76.67 | 90.0 | +13.3 |
[...]
203: 
204: The **INT2 column stands** — every one of these ran `--cuda-graph-max-bs 1` and
205: single-stream, i.e. off the defective path, and the GPQA cell (80.3) has now been
206: reproduced at 80.30 in a paired run. Treat them as valid INT2 results.
207: 
208: What was wrong is only the **Δ column**: the BF16 numbers came from the model
209: authors under a different harness and seed count, and the GPQA +2.0 in particular
210: compared INT2 at concurrency 1 against a BF16 arm at concurrency 32. Re-pair
211: against same-harness BF16 arms rather than discarding the INT2 side. On a proper
[...]
218: Measured, so that nobody re-spends the GPU hours:
219: 
220: - **Rotation quality.** The calibrated rotation was fit on 10,000 tokens/layer
221:   with the full head axis present (8/8 KV, 48/48 Q — not a TP shard), spectrum
222:   participation ratio 10–29 of 128 and condition number 77–270, orthogonality
223:   2.6e-08, all in the same band as the shipped Qwen3-4B-Thinking Zoo rotation.
224:   Swapping in a **data-free Hadamard** scores 56.32 (2 seeds) against the
225:   calibrated 57.91 — a tie. Refitting cannot buy 13 pp.
226: - **Lloyd-Max**: 50.0, i.e. −7.9. Refuted here as on Gemma-4 and M3.
[...]
237:   it only clears this one bug.
238: - **The partial-RoPE boundary** (M2.7 is the only model here with
239:   `rotary_dim=64` of `head_dim=128`, so one rotation and one 2-bit scale span
240:   both the positional and static halves). Measured on the real dump: the halves
241:   have the *same* magnitude (rms 1.63 vs 1.47) and error is spread evenly
242:   (relerr 0.46 vs 0.52), so no shared scale is being swamped. A block-diagonal
243:   64+64 rotation that cannot mix the halves is **worse** offline (logit rel-err
244:   0.360 vs 0.330), because a full 128-dim Hadamard spreads outliers over 128
245:   coordinates while two 64-dim blocks spread over 64 — the same mechanism that
246:   made quant group 64 worse. Keeping dims 0–63 in BF16 does cut logit error to
[...]
248:   positional subspace does carry more logit signal), but it costs ~9 bits/element
249:   on K against 2 — a 4.5× increase — so it is a diagnostic, not a fix.
250:   Confirmed end-to-end: a block-diagonal 64+64 K rotation fitted per block from
251:   the same dump scores **49.49** (51.01 / 49.49 / 47.98) against the
252:   same-session 64/256 control's **52.53** (51.01 / 54.04 / 52.53) — −3.04 pp,
[...]
258:   model degenerates into repetition loops.
259: - **Budget 95K generation tokens.** M2.7 is a long-thinking model; a smaller
260:   budget measures truncation, not accuracy. AIME and LCB above both use 95K.
261:   But it must be varied in *both* arms, and doing so does **not** narrow the
262:   INT2 gap — it widens it. Measured, windows 64/256:
[...]
273:   score moves 57.91 → 60.10. A 95K INT2 number against a 32K BF16 number is the
274:   asymmetry that produced the implausible published AIME +13.3. Always report
275:   the full-denominator score, never accuracy conditioned on having answered.
276: 
277: ## Steps
278: 
279: ```bash
280: # 1. dump post-RoPE Q/K/V on GPQA (TP=4)
281: bash save_qkv_m27.sh
282: 
283: # 2. fit
284: bash compute_rotation.sh    # qqt_sst / r_h_pbr
285: ```
286: 
[...]
291: SGLANG_MIXED_KV_PREFIX_TOKENS=256 SGLANG_MIXED_KV_RECENT_TOKENS=1024 \
292: SGLANG_MIXED_KV_HP_DTYPE=bfloat16 SGLANG_MIXED_KV_SCALE_DTYPE=float32 \
293: SGLANG_OSCAR_ABSORB_V_ROTATION=0 SGLANG_LLOYD_MAX=0 \
294: SGLANG_OSCAR_K_CLIP_RATIO=0.96 SGLANG_OSCAR_V_CLIP_RATIO=0.92 \
295: SGLANG_OSCAR_K_ROTATION_PATH=<out>/k_rotation_qqt_r_h_pbr.pt \
296: SGLANG_OSCAR_V_ROTATION_PATH=<out>/v_rotation_sst_r_h_pbr.pt \
297: python -m sglang.launch_server --model-path MiniMaxAI/MiniMax-M2.7 \
298:   --tensor-parallel-size 4 \

## OSCAR/rotation/MiniMax-M3/README.md
[...]
1: # MiniMax-M3 — INT2 KV recipe
2: 
3: 428B VL-MoE. A single rotation shared per layer is **saturated** on this model:
4: an all-head calibrated rotation scores 85.35 % on GPQA against 84.85 % for plain
5: Hadamard, a one-question difference at n=198. Fit it anyway — the calibrated
6: rotation is measurably better on reconstruction error and costs nothing at serve
7: time — but do not expect calibration to be the lever here.
8: 
9: | KV | GPQA (198) | GPQA PPL | vs BF16 |
10: |---|:---:|:---:|:---:|
11: | BF16 | 88.38 % | 1.3140 | — |
12: | INT2, Hadamard | 84.85 % | – | – |
13: | INT2, rank-0 calib (**deficient dump**) | 84.85 % | – | – |
14: | **INT2, all-head calib** | **85.35 %** | 1.3479 | +2.6 % |
15: | INT2, all-head + Lloyd-Max | 84.85 % | 1.3672 | +4.0 % |
16: 
17: **Do not enable Lloyd-Max.** It is worse on both perplexity and GPQA.
18: 
19: ## The dump must cover every TP rank
[...]
21: This is the one trap specific to M3. The dump hook writes per rank, and a rank-0
22: dump captures **4 of 64 query heads and 1 of 4 KV heads** — an unrepresentative
23: head sample that fits a rotation no better than Hadamard, with nothing in the
24: logs to say so. Dump all 16 ranks and merge before fitting.
25: 
26: Reconstruction error on the merged data, INT2-asymmetric relL2:
27: 
28: | rotation | V | K |
29: |---|:---:|:---:|
30: | all-head | **0.4794** | ~0.49 |
31: | rank-0 only | 0.4937 | ~0.49 |
32: | Hadamard | 0.5000 | ~0.49 |
33: 
34: K stays flat because `qqt` targets the Q covariance, not raw-K error. Verify V
35: improves before trusting a fit; if it sits at 0.50 the dump is deficient.
36: 
37: Calibration token count is **not** a lever — the covariance converges by roughly
38: 5K tokens per layer.
39: 
[...]
52: 
53: # 3. fit
54: bash compute_rotation.sh          # qqt_sst / r_h_pbr, ~12K tok/layer
55: 
56: # 4. verify before spending an eval on it
57: python3 verify_rotation.py \
58:   --dump <dump-dir>/qkv_dumps_merged \
59:   --k-rotation <out>/k_rotation_qqt_r_h_pbr.pt \
60:   --v-rotation <out>/v_rotation_sst_r_h_pbr.pt
61: ```
62: 
[...]
67: SGLANG_MIXED_KV_PREFIX_TOKENS=64 SGLANG_MIXED_KV_RECENT_TOKENS=256 \
68: SGLANG_MIXED_KV_HP_DTYPE=bfloat16 SGLANG_MIXED_KV_SCALE_DTYPE=float32 \
69: SGLANG_OSCAR_ABSORB_V_ROTATION=0 SGLANG_LLOYD_MAX=0 \
70: SGLANG_OSCAR_K_CLIP_RATIO=0.96 SGLANG_OSCAR_V_CLIP_RATIO=0.92 \
71: SGLANG_OSCAR_K_ROTATION_PATH=<out>/k_rotation_qqt_r_h_pbr.pt \
72: SGLANG_OSCAR_V_ROTATION_PATH=<out>/v_rotation_sst_r_h_pbr.pt \
73: python -m sglang.launch_server --model-path MiniMaxAI/MiniMax-M3 \
74:   --tensor-parallel-size 16 --nnodes 2 --node-rank <0|1> \

## OSCAR/rotation/examples/README.md
[...]
1: # examples
2: 
3: ## GPQA under INT2 OSCAR KV
4: 
5: ```bash
6: rotation/examples/gpqa_int2_oscar.sh qwen3-8b
7: ```
8: 
9: Runs GPQA-Diamond (198 questions, scored by the vendored `simple_evals`) against
10: the model served with INT2 OSCAR KV, using that model's own recipe from
11: `rotation/run/<model>.sh`.
12: 
13: **The recipe is not shared between models.** The table below is the whole reason
[...]
16: | knob | which models |
17: |---|---|
18: | per-head rotation (V2) | **Qwen3-30B-A3B only** |
19: | Lloyd-Max codebook | MiniMax-M2.7, Qwen3-8B, Qwen3.5-35B-A3B |
20: | group size 256 | Qwen3.5-4B, Qwen3.5-35B-A3B (128 elsewhere) |
21: | published-Hadamard rotation file | MiniMax-M3 |
22: | packed 2-bit MLA latent | GLM-5.2, GLM-5.3, Kimi-K3 |
23: | `--mamba-radix-cache-strategy extra_buffer` | Qwen3.5-4B, Qwen3.5-35B-A3B (hybrid) |
[...]
25: 
26: Qwen3-30B-A3B is the sharpest case: its 4 KV heads are near orthogonal, so a
27: shared per-layer rotation collapses it — GPQA **43.9** against per-head's
28: **58.6**. Both rotation formats live in the same zoo directory, so the per-head
29: file has to be named explicitly rather than globbed.

## OSCAR/rotation/gemma-4-12B-it/README.md
[...]
11: ## Pipeline
12: 1. `PY=<py> bash save_qkv_gemma4_12b.sh`   # dump Q/K/V (eval-fork DUMP_KVCACHE hook)
13: 2. `PY=<py> bash compute_rotation.sh`       # per-layer rotations (256/512)
14: 3. `PY=<py> MODE=int2 bash eval_gpqa.sh`     # INT2 OSCAR GPQA (MODE=bf16 for baseline)
15: 
16: ## Status (2026-06-04) — DONE ✅
17: - BF16 GPQA-Diamond = **62.63%** (full 198).
18: - **INT2 OSCAR GPQA-Diamond = 62.63%** (full 198) — **Δ 0.0pp vs BF16**.
19:   The full-attention layers (head_dim 512) ARE quantized to INT2.
20: - INT2 serving uses a **two-geometry-group `UnifiedInt2HPKVPool`** (gemma is the first
[...]
22: - Key fix: sliding layers must be windowed in the mixed-KV **decode** path (not just
23:   prefill); without it INT2 scored 50.0% (sliding layers read full context in decode).
24: - Quant precision (Lloyd-Max) and V-rotation were ruled out as the cause via diagnostics.

## OSCAR/rotation/kimi-k3/README.md
[...]
20:    ```
21: 
22: 3. Generate and validate rotations:
23: 
24:    ```bash
25:    DUMP_PATH=<dump-dir> \
26:    OUTPUT_DIR=<rotation-dir> \
27:    MODEL_CONFIG=<config.json> \
28:    ./compute_rotation.sh
29:    ```
30: 
31: `validate_rotations.py` checks a fitted rotation before you serve with it: a
32: calibration that silently failed produces a loadable file that is no better than
33: Hadamard, and 2-bit needs the K relative error at or below 0.1.

## OSCAR/rotation/porting/PORTING.md
[...]
36: | 1 | KV-quant core: `--kv-cache-dtype int2`, `UnifiedInt2HPKVPool` + allocator, mixed HP windows, radix-cache tiers, scheduler flush, triton INT2 prefill/decode, QuantKernel, pool pricing, env knobs | Qwen3-8B INT2 at 8K ctx, radix + graph on | ported; CPU checks pass on the new base; smoke PASS on `67eab57057` (Qwen3-8B, radix + graph on) |
37: | 2 | MHA/GQA models: qwen3, qwen3_5 (hybrid GDN), qwen3_moe, gemma4_unified (two-group), minimax_m2.7 | each model's smoke | ported (all passed on the previous base; Gemma-4's first verdicts were the raw-prompt probe, fixed by the chat-template probe); all PASS on `67eab57057` |
38: | 3 | MLA packed latent (`MLAPackedInt2KVPool`, `NSAPackedInt2KVPool`, packed decode kernels) on upstream's DSA backend for GLM-5.2/5.3, trtllm_mla for Kimi-K3; MSA for MiniMax-M3 on upstream's native backend | GLM-5.2 recall probe past 2K tokens, then smoke | ported (all passed on the previous base: GLM under DSA with long-prompt recall OK, M3 under MSA with piecewise prefill graphs auto-disabled, K3 PP2 x TP8); on `67eab57057` GLM-5.2, GLM-5.3 and MiniMax-M3 PASS (92/90/91 graph shapes, prefix hits logged); Kimi-K3 PASS as well (probed inside its two-node GPQA job on `67eab57057`: 173 graph shapes, prefix hits logged) -- 12 of 12 |
39: | 4 | harness: `rotation/` paths, run scripts, verify sweep, bench | 12-model sweep | done: chat-template probe, serve wait scaled to model size, `SMOKE_ONLY=1` in the eval driver for the two-node K3, conda-free drivers |
40: | 5 | GPQA @64K + 64K decode speed for all 12, table and README | | GPQA@64K done for all 13 models and 64K decode done for 12 on `67eab57057` (README tables); Kimi-K3's three bench arms run one two-node JobSet at a time under a two-node cap. MiniMax-M3's first INT2 run (56.6) exposed the indexer keys not following the decode flush; fixed, re-run 88.9 vs 90.9, and the smoke gained the verbatim-quote retention probe |
41: 
42: ## Notes
[...]
45:   (passphrase recall OK at 1.2K tokens, garbage from 5.3K; identical for fused
46:   and unfused top-k and for trtllm vs flashmla_sparse decode). That is the
47:   defect behind the 33.8% sparse-mode GPQA, and the first thing phase 3 checks
48:   on the new tree is that upstream's DSA passes the same probe.
49: * MiniMax-M3's sparse prefill kernel asserts `gqa_group_size * block_size_q

## OSCAR/rotation/porting/port_checklist.md
[...]
15: | A | 1032 | 177 | `python/sglang/srt/mem_cache/unified_kv_pool.py` |
16: | A | 1002 | 151 | `python/sglang/srt/mem_cache/mla_packed_kv_pool.py` |
17: | A | 965 | 90 | `python/sglang/QuantKernel/oscar_rotation_clip_int2_kv.py` |
18: | A | 937 | 12 | `python/sglang/srt/models/kimi_k3_vl.py` |
19: | M | 811 | 195 | `python/sglang/srt/mem_cache/memory_pool.py` |
20: | A | 788 | 3 | `python/sglang/srt/layers/attention/minimax_sparse_kernels/prefill/flash_with_topk_idx.py` |
21: | A | 718 | 8 | `python/sglang/srt/models/minimax_m3.py` |
22: | A | 653 | 66 | `python/sglang/QuantKernel/fused_hadamard_int2_kv.py` |
23: | M | 628 | 260 | `python/sglang/srt/model_executor/model_runner_kv_cache_mixin.py` |
24: | A | 613 | 6 | `python/sglang/srt/layers/attn_residual.py` |
[...]
103: | A | 217 | `python/sglang/srt/layers/attention/vision_rope.py` |
104: | M | 216 | `python/sglang/srt/layers/attention/fla/fused_sigmoid_gating_recurrent.py` |
105: | M | 180 | `python/sglang/multimodal_gen/test/server/accuracy_utils.py` |
106: | M | 175 | `python/sglang/srt/layers/attention/linear/kernels/kda_triton.py` |
107: | M | 170 | `python/sglang/srt/layers/attention/fla/l2norm.py` |
[...]
116: | M | 107 | `python/sglang/multimodal_gen/test/run_suite.py` |
117: | M | 87 | `python/sglang/srt/layers/moe/topk.py` |
118: | M | 76 | `python/sglang/multimodal_gen/test/server/accuracy_hooks.py` |
119: | M | 76 | `python/sglang/multimodal_gen/test/server/component_accuracy.py` |
120: | A | 75 | `python/sglang/srt/layers/moe/triton_kernels_compat.py` |
121: | M | 72 | `python/sglang/srt/layers/quantization/mxfp4.py` |
[...]
147: | M | 14 | `python/sglang/srt/layers/attention/fla/wy_fast.py` |
148: | A | 14 | `python/sglang/srt/layers/dcp/planner.py` |
149: | M | 13 | `python/sglang/multimodal_gen/test/server/accuracy_config.py` |
150: | M | 12 | `python/sglang/srt/configs/qwen3_asr.py` |
151: | M | 12 | `python/sglang/srt/layers/attention/linear/gdn_backend.py` |

## OSCAR/rotation/qwen3-30B-A3B/README.md
[...]
1: # Qwen3-30B-A3B — INT2 KV recipe
2: 
3: This model needs **per-head rotations**. With one rotation shared across the
4: four KV heads, long generations degenerate into digit soup or repetition loops
5: (GitHub issue #16). The cause is not calibration quality: the four KV heads
6: want mutually near-orthogonal rotations (`mean |diag(R0ᵀR1)| ≈ 0.07`), so no
7: single matrix can serve them.
8: 
9: WikiText-2 perplexity through the fake-quant harness, vs BF16:
10: 
11: | rotation | PPL delta |
12: |---|---|
13: | shared per layer, calibrated (117 prompts) | +16.6 % |
14: | shared per layer, plain Hadamard | +26.6 % |
15: | shared per layer, 12-token junk dump | +15.3 % |
16: | **per KV head, calibrated** | **+0.35 %** |
[...]
18: The three shared rows land within a few points of each other while per-head is
19: an order of magnitude better, which is why re-running calibration does not help.
20: Qwen3-8B has 8 KV heads that tolerate a shared rotation, so this never showed up
21: before.
22: 
[...]
24: 
25: ```bash
26: # 1. dump post-RoPE Q/K/V on GPQA (~15 min, 1 GPU)
27: bash save_qkv_30b.sh
28: 
[...]
31: 
32: # 2b. shared per-layer fit, for comparison only
33: bash compute_rotation.sh
34: 
35: # 3. serve
[...]
39: Check step 1 before continuing: the script prints `ok=<n> err=<n>` and aborts
40: unless every prompt came back. A dump that silently captured a handful of tokens
41: still produces loadable rotation files that quietly serve garbage.
42: 
43: Confirm step 3 took the per-head path — the pool logs it at startup:
44: 
45: ```
46: [oscar] loaded K rotation ... [per-head: 4 kv heads]
47: ```
48: 
[...]
52: |---|---|
53: | `save_qkv_30b.sh` | Q/K/V dump for calibration |
54: | `fit_perhead.sh` | per-KV-head rotations (`format_version: 2`) |
55: | `compute_rotation.sh` | shared per-layer rotations (V1) |
56: | `serve.sh` | sglang launch with the full env |

## OSCAR/rotation/verify/README.md
[...]
3: Answers one question per model: **does it serve correctly with prefix cache and
4: CUDA graph both on?** Not "what does it score" — scores come from
5: `rotation/run/<model>.sh`, which drives the real evals.
6: 
7: ```
[...]
26: ## Things that bit us
27: 
28: - **Rotations are discovered by glob, not by name.** MiniMax-M3 ships
29:   `k_rotation_hadamard.pt`; a hardcoded `qqt_r_h_pbr` reported "no rotation",
30:   which reads as "model unsupported" when the files were present.
31: - **GPUs are drained before sizing.** A leftover allocation is charged to the
32:   next model — it once made a 12B report 79 GiB in use.
33: - **MLA pins `--kv-cache-dtype bfloat16`.** sglang picks `fp8_e4m3` for a DSA
34:   model on SM100+, which puts ~28% of every 512×512 rotation subnormal; that arm
35:   scored 5.56.
36: - **Each MLA model gets its own `HOME`/`TRITON_CACHE_DIR`.** Two GLM jobs sharing
[...]
49: ```bash
50: export OUT=/path/for/per-model-output V=/path/to/verdicts.txt
51: bash rotation/verify/all.sh            # every model, resumes from $V
52: bash rotation/verify/all.sh qwen3-8b   # just one
53: ```
54: 

## OSCAR/sglang-dump-qkv/docs/advanced_features/checkpoint_engine.md
[...]
38: ```bash
39: python -m sglang.launch_server \
40:     --model-path Qwen/Qwen3-8B \
41:     --tp 8 \
42:     --load-format dummy \
[...]
50: python -m sglang.srt.checkpoint_engine.update \
51:     --update-method broadcast \
52:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
53:     --inference-parallel-size 8
54: ```
[...]
59:     examples/checkpoint_engine/update.py \
60:     --update-method broadcast \
61:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
62:     --inference-parallel-size 8
63: ```
[...]
70: ```bash
71: python -m sglang.launch_server \
72:     --model-path Qwen/Qwen3-8B \
73:     --tp 8 \
74:     --load-format dummy \
[...]
83: python -m sglang.srt.checkpoint_engine.update \
84:     --update-method broadcast \
85:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
86:     --inference-parallel-size 8
87: ```
[...]
96:     examples/checkpoint_engine/update.py \
97:     --update-method broadcast \
98:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
99:     --inference-parallel-size 8
100: ```
[...]
105: ```bash
106: python -m sglang.launch_server \
107:     --model-path Qwen/Qwen3-8B \
108:     --tp 8 \
109:     --load-format dummy \
[...]
118: python -m sglang.srt.checkpoint_engine.update \
119:     --update-method broadcast \
120:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
121:     --inference-parallel-size 8
122: ```
[...]
131:     examples/checkpoint_engine/update.py \
132:     --update-method broadcast \
133:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
134:     --inference-parallel-size 8
135: ```
[...]
142: ```bash
143: python -m sglang.launch_server \
144:     --model-path Qwen/Qwen3-8B \
145:     --tp 8 \
146:     --load-format dummy \
[...]
158: python -m sglang.srt.checkpoint_engine.update \
159:     --update-method broadcast \
160:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
161:     --inference-parallel-size 16
162: ```
[...]
171:     examples/checkpoint_engine/update.py \
172:     --update-method broadcast \
173:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
174:     --inference-parallel-size 16
175: ```
[...]
180: ```bash
181: python -m sglang.launch_server \
182:     --model-path Qwen/Qwen3-8B \
183:     --tp 8 \
184:     --load-format dummy \
[...]
196: python -m sglang.srt.checkpoint_engine.update \
197:     --update-method broadcast \
198:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
199:     --inference-parallel-size 16
200: ```
[...]
209:     examples/checkpoint_engine/update.py \
210:     --update-method broadcast \
211:     --checkpoint-path /path/to/Qwen/Qwen3-8B/ \
212:     --inference-parallel-size 16
213: ```

## OSCAR/sglang-dump-qkv/docs/advanced_features/deterministic_inference.md
[...]
39: ```bash
40: python3 -m sglang.launch_server \
41:     --model-path Qwen/Qwen3-8B \
42:     --attention-backend fa3 \
43:     --enable-deterministic-inference
[...]
53: ### Example Configurations
54: 
55: #### Qwen3-8B
56: ```bash
57: python3 -m sglang.launch_server \
58:     --model-path Qwen/Qwen3-8B \
59:     --attention-backend flashinfer \
60:     --enable-deterministic-inference

## OSCAR/sglang-dump-qkv/docs/platforms/ascend_npu_support_models.md
[...]
96: | 	Qwen/Qwen2.5-Math-RM-72B                   | Qwen2.5 Reward - Math     | **<span style="color: green;">√</span>** | **<span style="color: green;">√</span>** |
97: | 	Howeee/Qwen2.5-1.5B-apeach                 | Qwen2.5 Reward - Sequence | **<span style="color: green;">√</span>** | **<span style="color: green;">√</span>** |
98: | 	AI-ModelScope/Skywork-Reward-Gemma-2-27B-v0.2    | Gemma 2-27B Reward  | **<span style="color: green;">√</span>** | **<span style="color: green;">√</span>** |
99: 
100: ## Rerank Models

## OSCAR/sglang-dump-qkv/docs/platforms/tpu.md
[...]
158: 6. `--max-prefill-tokens=8192` - Maximum number of tokens processed in the prefill phase
159: 
160: ### High-Performance Configuration: Qwen3-8B
161: 
162: For production workloads with optimal throughput:
[...]
164: ```bash
165: python3 -u -m sgl_jax.launch_server \
166:     --model-path Qwen/Qwen3-8B \
167:     --trust-remote-code \
168:     --tp-size=4 \

## OSCAR/sglang-dump-qkv/docs/supported_models/generative_models.md
[...]
33: | **Llama** (2, 3.x, 4 series)        | `meta-llama/Llama-4-Scout-17B-16E-Instruct`       | Meta's open LLM series, spanning 7B to 400B parameters (Llama 2, 3, and new Llama 4) with well-recognized performance. [SGLang provides Llama-4 model-specific optimizations](../basic_usage/llama4.md)  |
34: | **Mistral** (Mixtral, NeMo, Small3) | `mistralai/Mistral-7B-Instruct-v0.2`             | Open 7B LLM by Mistral AI with strong performance; extended into MoE (“Mixtral”) and NeMo Megatron variants for larger scale. |
35: | **Gemma** (v1, v2, v3)              | `google/gemma-3-1b-it`                            | Google’s family of efficient multilingual models (1B–27B); Gemma 3 offers a 128K context window, and its larger (4B+) variants support vision input. |
36: | **Phi** (Phi-1.5, Phi-2, Phi-3, Phi-4, Phi-MoE series) | `microsoft/Phi-4-multimodal-instruct`, `microsoft/Phi-3.5-MoE-instruct` | Microsoft’s Phi family of small models (1.3B–5.6B); Phi-4-multimodal (5.6B) processes text, images, and speech, Phi-4-mini is a high-accuracy text model and Phi-3.5-MoE is a mixture-of-experts model. |
37: | **MiniCPM** (v3, 4B)               | `openbmb/MiniCPM3-4B`                            | OpenBMB’s series of compact LLMs for edge devices; MiniCPM 3 (4B) achieves GPT-3.5-level results in text tasks. |

## OSCAR/sglang-dump-qkv/docs/supported_models/mindspore_models.md
[...]
31: ## Run Model
32: 
33: Current SGLang-MindSpore supports Qwen3 and DeepSeek V3/R1 models. This doc uses Qwen3-8B as an example.
34: 
35: ### Offline inference

## OSCAR/sglang-dump-qkv/docs/supported_models/multimodal_language_models.md
[...]
38: | **LLaVA-NeXT** (8B, 72B)   | `lmms-lab/llava-next-72b`                  | Improved LLaVA models (with an 8B Llama3 version and a 72B version) offering enhanced visual instruction-following and accuracy on multimodal benchmarks.                                                       |  |
39: | **LLaVA-OneVision**        | `lmms-lab/llava-onevision-qwen2-7b-ov`     | Enhanced LLaVA variant integrating Qwen as the backbone; supports multiple images (and even video frames) as inputs via an OpenAI Vision API-compatible format.                                                 |  |
40: | **Gemma 3 (Multimodal)**   | `google/gemma-3-4b-it`                     | Gemma 3's larger models (4B, 12B, 27B) accept images (each image encoded as 256 tokens) alongside text in a combined 128K-token context.                                                                        |  |
41: | **Kimi-VL** (A3B)          | `moonshotai/Kimi-VL-A3B-Instruct`          | Kimi-VL is a multimodal model that can understand and generate text from images.                                                                                                                                |  |
42: | **Mistral-Small-3.1-24B**  | `mistralai/Mistral-Small-3.1-24B-Instruct-2503` | Mistral 3.1 is a multimodal model that can generate text from text or images input. It also supports tool calling and structured output. |  |

## OSCAR/sglang-dump-qkv/docs/supported_models/reward_models.md
[...]
23: |---------------------------------------------------------------------------|-----------------------------------------------------|---------------------------------------------------------------------------------|
24: | **Llama (3.1 Reward / `LlamaForSequenceClassification`)**                   | `Skywork/Skywork-Reward-Llama-3.1-8B-v0.2`            | Reward model (preference classifier) based on Llama 3.1 (8B) for scoring and ranking responses for RLHF.  |
25: | **Gemma 2 (27B Reward / `Gemma2ForSequenceClassification`)**                | `Skywork/Skywork-Reward-Gemma-2-27B-v0.2`             | Derived from Gemma‑2 (27B), this model provides human preference scoring for RLHF and multilingual tasks.  |
26: | **InternLM 2 (Reward / `InternLM2ForRewardMode`)**                         | `internlm/internlm2-7b-reward`                       | InternLM 2 (7B)–based reward model used in alignment pipelines to guide outputs toward preferred behavior.  |
27: | **Qwen2.5 (Reward - Math / `Qwen2ForRewardModel`)**                         | `Qwen/Qwen2.5-Math-RM-72B`                           | A 72B math-specialized RLHF reward model from the Qwen2.5 series, tuned for evaluating and refining responses.  |

## gpt_new_oscar_kimi/AGENTS.md
[...]
6: - 本轮目标改为 32K 和 64K、300 请求、512 输出，两场景端到端性能均比同参数且完全禁用 OSCAR 的原生基线提升超过30%。完整客户端证据及两种30%口径见 `reports/stable_32k_64k_20261015/analysis.md`；旧120请求、2–4倍等目标不用于本轮验收。
7: - 本轮禁止以任何方式连接或使用真机；本地源码、CPU-debug、CANN编译与CAModel独立完成，最后交付一键命令由用户验证。不要索要已完成AISBench重跑，也不能把本地算子倍率写成整轮达标。
8: - 用户随后明确接纳完整stable→B1（3888161→3172246 ticks）进入主分支作为继续迭代基底；不因相对中间pipeline仅4.1%而剔除。每点不再机械要求1.15倍，保留真实净收益并按新基底去重计账，精度和协议门不变。继续叠加到两场景相对同参native端到端超过30%；完成后推主分支给用户验证，stable仅由用户验证后维护。
9: 
10: 先读 `oscar_ascend_agent_start.md`，按其档案引用制度执行。`issue1_full_record.md` 实际为173条（G1–G34、#1–#139），按标题定位；旧标题条数与旧行号存在漂移。
[...]
14: - 配置以本次 `configs/target.json` 为准：按本次启动文档附录 A/F 默认物理设备 `0,1,2,3`、SOC `ascend910b4`、端口 `8989`。不能从旧项目记忆或已有环境继承其他任务卡号；显式配置非法时仍报错。
15: - 用户另明确授权直启入口`install_serve.sh --rear-cards`本次使用物理设备`4,5,6,7`和端口`7878`；这是显式可选模式，默认配置和其他入口不变。
16: - 用户最新要求：保留真实 NPU 算子、CV/旋转和完整服务探针；移除默认部署中的环境清单、原生源码扫描、readiness 前置审计。正常流程为安装/编译/探针/自动旋转文件/服务探针/资源清理/正式服务，任何探针失败不得继续。该要求优先于启动文档旧的环境审计步骤。
17: - 部署阶段及服务子进程的输出和错误必须实时打印到当前终端，同时保留相位日志、状态和真实退出码；不能只把 traceback 写入文件后让用户手工查找（档案 #94/#95/#125）。
18: - `docs/checklist.md` 是42个稳定checkpoint；源码、CPU、CANN、设备完成、图捕获、图回放、质量、性能分别记录。
19: - CV/history/window、production RuntimeProvider、物理页精确快照、MTP位置修正和全服务probe已有实现。CANN VM编译与官方CPU-debug通过；node93已通过75项store/merge原语真NPU探针，后续日志已进入TP4/MTP模型加载，最新已完成编译/初次profiling与KV预算，后续已通过health与128→16短请求；后续128/16K/32K/50K串行请求均已完成；混合并发已现300s请求死线超时失败（心跳证明非死锁、为时间预算问题），性能未验收（#130/#131）；已支持none/align布局并区分物理存储与metadata128虚拟块，完整NPU/图/性能未验收，readiness或编译成功不能冒充这些证据。
20: - `ops/reference.py` 是独立测试oracle，绝不加入生产路由。精度冻结于 `configs/acceptance.json`，不能事后放宽。
21: - 凡修改CANN算子，先亲读档案同类条目与D.4完整原始打点，文件头加入档案引用及D.4四问。
22: - 新真机错误才追加档案；本机CPU测试或理论判断不能伪写为真机记录。

## gpt_new_oscar_kimi/README.md
[...]
3: 固定优化交付入口：`git pull --ff-only && bash scripts/install_serve.sh --variant candidate`。每轮实现均须同步编译、候选配置和实际算子路由；直启与probe共用`tools/serving_variants.py`候选预设。该直启命令仍不运行测试/probe/AISBench，后四卡只需追加`--rear-cards`。
4: 
5: 已实现 FULL 层 INT2 缓存、真正的 Cube/Vector attention、融合旋转/裁剪/写入、精确窗口、MTP 位置修正、固定图缓冲、外部插件及一键安装/探针/服务流程。GDN 使用原生状态和 reshape。新增代码不覆盖原生 vLLM/Ascend 源文件。
6: 
7: ## fe0 精度基准与历史复用实验
8: 
9: 用户最新candidate完整耗时约19分钟，8分钟目标尚未达到。本轮已实现q4/q1/C4共用的精确fast unpack候选（位平面布局和FP16 metadata批量转换），CANN编译与官方CPU-debug22/22通过；目标NPU精度/图/净收益仍须短probe。完整方案与边界见[fast unpack](docs/fast_unpack.md)。
10: 
11: 2026-09-28：已从用户实际负载中定位到MTP后两轮q1的历史任务偏载，新增独立调度实验。后续不再要求重跑AISBench；下一轮仅用短probe：
[...]
17: 此模式完成原算子/图/速度门及新增fast unpack门后退出，不加载模型。q1真机已逐位通过，N128/S3耗时下降69.39%、N16384/S1下降85.10%；完整服务收益不外推。下一轮关注`PERF_FAST_UNPACK`。已完成的q4诊断默认不再重复，显式`--diagnose-q4`可重新采证，见[q4诊断口径](docs/q4_diagnostic.md)与[本次实际负载分析](docs/observation_20260928.md)。
18: 
19: 当前以用户确认精度正确的`fe0e925`为基准。原`attention_cv.cpp`及store/rotate/merge等计算内核保持该版本字节一致；默认仍运行原算子。`codex/aisbench-stable`保持精确的fe0提交。新C4算子仅在显式候选模式中使用，冻结容差没有放宽，也未重新加入已回退的AR/位图或元数据向量化。
20: 
21: ### 一键验证候选并启动，用户自行运行 AISBench
[...]
49: 默认读取 `configs/target.json`：物理 NPU **0,1,2,3**、`ascend910b4`、TP=4、端口 **8989**，模型为 `/softwarePlatform/c00879303/Qwen3.5-27B-w8a8-mtp`。这些值来自本次启动文档附录 A/F；全部子进程使用同一配置，不继承其他任务卡号。脚本使用当前 `python3`，也可通过 `OSCAR_PYTHON` 指定已有解释器；node93 无需创建 `.venv`、安装 Lima 或运行 `validate_vm.sh`。
50: 
51: 默认流程：安装构建依赖/插件 → 编译算子 → 真 NPU 算子对拍及 CV/旋转探针 → 自动准备旋转文件 → TP4/MTP/长输入/图服务探针 → 回收本任务进程及 NPU 资源 → 正式服务并验证真实请求。**探针保留且失败即停止**；启动流程不执行环境清单、原生源码扫描或 readiness 前置审计。安装、编译、数值、服务或资源清理失败都会保留日志和退出码，不改走原生 FULL 或 CPU。每个阶段的输出、服务启动日志及 traceback 都实时显示在当前终端，同时写入 `logs/<本次运行>/`；失败时打印阶段名、退出码和日志路径，无需打开文件才能看到错误。该流程尚未在目标 NPU 全程执行。此次启动修订对应档案 #74–76/#94–98/#107/#117/#123–125；最新真机CV数值失败记录见 #126。
52: 
53: 已跑通过完整探针、只想重新编译安装并直接启动时（不运行任何测试或probe）：
[...]
57: ```
58: 
59: 它只执行安装构建依赖/插件 → 编译算子 → 自动准备旋转文件，全部成功后以 `tools.target_cli` 前台路径直接拉起正式服务（与 `scripts/serve_direct.sh` 同一启动入口）；任一相位失败即保留真实退出码并停止，不会拉起服务。该入口不执行算子/服务探针和配对性能门，不能充当验收证据；正式验收仍使用 `scripts/install_probe_serve.sh`。
60: 
61: `--variant candidate`生成本轮有效配置并启用C4历史复用、后续MTP q1调度和新fast unpack；新版本应先通过上面的真实NPU短probe。终端打印`SERVE_MODE variant=candidate C4=on Q1=on FAST_UNPACK=on`。它不启用独立q4 profile算子。`--variant baseline`使用fe0；省略该参数时遵循原配置，当前`configs/target.json`默认未启用这些实验路径。原配置文件不会被修改。
[...]
67: ```
68: 
69: 设备与端口写入本轮有效配置，安装/编译/旋转准备和服务统一使用该配置。省略`--rear-cards`时，默认仍为0,1,2,3和8989；不修改`configs/target.json`。
70: 
71: 不启动设备即可查看计划：
[...]
84: ```
85: 
86: **最新真机结果：128、16K、32K、50K四个串行请求均已生成16个token，并开始混合并发探针（#130）。** 32K和50K仍很慢，完整并发/质量/性能尚未验收。本轮将历史INT2与当前BF16的逐token搬运改为有界分块DMA，保持计算公式、精度阈值与固定UB/GM预算；提速幅度待目标实测。日志会明确debug_sync是否启用，并区分客户端等待、host事件及设备同步检查点。ArgSort转AiCPU告警已由用户确认基线也有，本轮未改该原生路径。[最新原文](reports/target_serial_50k_progress.txt)。
87: 
88: 当前运行的采证（只读本轮进程、日志、trace和所属PID的CANN日志，不启动模型、不接触设备、不发信号）：
[...]
114: 此命令在 Lima `oscar` VM 的独立 `/home/sunao2000.linux/gpt_new_oscar` 目录编译、链接，并运行同一份 AscendC kernel 的官方 CPU 调试器。首次配置可加 `--bootstrap`，仅安装该目录独立虚拟环境的依赖；不访问 VM 中旧项目代码。报告在 [reports/vm/validation.json](reports/vm/validation.json)，最新一轮共61个算子用例通过，另含 MTP/padding 元数据检查。
115: 
116: 一键性能诊断已并入 `git pull --ff-only && bash scripts/install_probe_serve.sh`：它自动依次启动原生和 OSCAR 服务，对同一组 **synthetic** 的 20K/23K/27K/30K 四路并发、每路64输出 token 测量 TTFT/TPOT/E2E 与吞吐，确认两轮资源释放，再按冻结的速度比值决定是否进入正式服务。终端仅打印少量阶段/资源状态、故障与最多8行配对 `PERF_*` 摘要；完整输出仍在本轮 `logs/`。只需把这些摘要或失败行直接贴回。`bash scripts/probe_concurrency.sh` 是省去完整安装/功能门的单命令快路径：它先校验AscendC构建签名，源码漂移则自动重编并跑真NPU CV/旋转数值门，然后自动跑原生→OSCAR两轮，无需第二条 `--native` 命令。正式服务就绪后等待 `OBSERVER_READY`，再用自己的压测程序发送32并发长请求；被动报告只观测该流量，不生成数据集或请求。单批 synthetic 速度门不是全工况性能验收。详见[服务探针](docs/service_probe.md)。
117: 
118: 一键配对中的原生阶段只用于明确的基线测量，OSCAR失败绝不会切换到原生服务。HTTP测量不伪造设备时间或MTP query长度；硬件、数值、显存、profiler证据齐全后才能做最终验收。[性能协议](benchmarks/README.md)与[分相位profiling](docs/profiling.md)给出数据格式和命令。
[...]
120: 算子采用独立 `ascendc_library` + 同流 direct-launch 的原生已有工程方式；交付两个共享库和带签名manifest，不安装custom OPP vendor。这一实现方式的差异见[算子设计](docs/ascendc_design.md)。Python wheel本身不含NPU二进制，目标入口首次使用本机CANN编译。扩展保留相邻 `lib` 的运行搜索路径，loader 使用 manifest 中校验过的 kernel 绝对路径加载，不要求手工设置本项目的 `LD_LIBRARY_PATH`（档案 #125）。后续源码、工具链、参数签名及产物指纹一致时复用已有产物，跳过 CMake 配置和编译；有变化或产物损坏时重新构建。
121: 
122: 默认旋转为论文明确支持的data-free Hadamard，在NPU生成、绑定模型/PR指纹，不能冒充样本校准。严格artifact加载、样本统计和旋转构造API另在 `rotations.py`；缺层不能静默identity，MTP draft采用档案#86的明确identity策略并告警。模型级质量容差仍须在目标实测前定义。
123: 
124: 详细状态：[检查清单](docs/checklist.md)、[全局设计](docs/design.md)、[原生接缝](docs/native_integration.md)、[运行时](docs/runtime_implementation.md)、[参考语义](docs/semantics.md)、[算子清单](docs/operator_inventory.md)、[服务探针](docs/service_probe.md)。`references/` 只读且不入新工程Git；目标部署不依赖它，本地完整native源码契约测试需要这些已提供的参考树。

## gpt_new_oscar_kimi/benchmarks/README.md
[...]
74: 其中 `q_len=null`；要求已知设备 q_len 的正式 `cases` 保持空数组，绝不从一次 HTTP
75: 请求复制出 1/2/3/4 四个所谓已测工况。`phase_ms={}`、`phase_status=needs_evidence`，
76: 也不会自动填入 accuracy、graph、route、memory 或 profiler 证据。
77: 
78: `--identity` 是可选的已核实服务器身份 JSON，包含 `software` 的全部字段（见下）和
[...]
191: | --- | --- |
192: | `npu` | `checks` 中 build/load/device_completion/graph_capture/graph_replay/tp4/mtp 全部 `passed` |
193: | `accuracy` | native 的 `checks.native_output=passed`；OSCAR 的 pack_unpack/store_dequant/fused_attention/prefill_window/model_quality 全部 `passed` |
194: | `route` | `backend` 精确等于 native/oscar；`ranks=[0,1,2,3]`，`all_full_layers=true`，`gdn_native=true`；native 还需 `oscar_plugin_disabled=true` |
195: | `memory` | OSCAR 必需；`full_history_bf16_restore_bytes=0`、`full_history_bf16_shadow_bytes=0` 必须为实测整数零 |
[...]
197: 任何 CPU 证据、缺数值验证、graph 未回放、route 并非 OSCAR、全历史 BF16 恢复/副本都会阻止
198: 通过。先验证这些证据，再计算该 case 的性能比值。数值容差由绑定的 acceptance 配置约束，
199: 相应精度 probe 负责实际验证，比较器不重新运行数值计算。
200: 
201: 文件 hash 证明内容完整性与配对绑定，**不能独立证明测量生产者诚实或硬件确实执行**。

## gpt_new_oscar_kimi/csrc/experiments/c16_anchor_skip_20261015/README.md
[...]
1: # C16 成功簇后的第二遍扫描跳步
2: 
3: 档案 #34/#36/#126/#129/#144/#145/#148/#152/#154/#157，启动文档 §0 与完整 D.4 已读。仅独立研究，不改生产核、冻结guard或精度配置，不新增在线主机回读。
4: 
5: 基底固定为 `c16_rv_reuse_20261015/c16_candidate.cpp`（SHA `9603817dddfba0e6357b42756a9956880137348ce8076c61aff58884acb6210b`）。Rv的独立数值/配对资格由它自己的报告裁决。后续性能只比较同库 **Rv vs Rv+finite+skip**，计划Q336/recent1/C320完整路径、原600秒/臂；不重跑旧stable/pipeline三臂，不乘旧倍率。组合由 `c16_b1_followup_20261015/generate.py` 按 `Rv -> apply_finite -> apply_skip` 唯一派生链生成，本目录不另占VM。
[...]
11: `token * (Hkv * 3 * splits) + (kv_head * 3 + kind) * splits + split_index`。
12: 
13: 请求来自原生 `query_start_loc / seq_lens / slot_mapping`。非单调或越界qstart、非法length/context、原生显式负slot、later-draft错误映射仍由原prepare/第一遍错误分支处理。新代码不从`qcount==0`或slot解析失败推断discard；第一遍所有padding、错误、follower status写回逐字保持，状态和精度门不删改。坏metadata/QR与同地址换context的NPU测试仍需原输出/LSE/status逐位和冻结oracle门。
14: 
15: **这个契约不是“允许任意伪造raw任务表”。** 重叠request的人工任务表可以伪造两组相互覆盖的成熟簇，并构成跳步反例；原生单调qstarts不能产生这种表，原核对此类重叠写回也没有合法数值契约。Host测试主动保留反例，拒绝声称任意raw-row输入等价。不能将本证明当作接受伪造表的校验。

## gpt_new_oscar_kimi/csrc/experiments/c16_b1_followup_20261015/README.md
[...]
26: D.4的全历史恢复6.5秒与store约209–215ms是旧结构失败红线；本方案只减少有界
27: 同步/元数据访问，不把旧毫秒当当前相位占比。#126/#145约束UB读写所有权，#134/#140
28: 约束原mask及pre-mask finite语义，#148/#154要求CPU与设备精度边界分别记录。
29: 
30: 完成记录：CANN/CPU构建10.933s；实际Softmax十二特殊值病例2.842s、完整C320两臂

## gpt_new_oscar_kimi/csrc/experiments/c16_l1_reuse_20261015/README.md
[...]
51: 
52: 同库stable/pipeline=1.177332、stable/B1=1.225681、pipeline/B1=1.041066。
53: 只计CV核；精度通过的是实际partial离线LSE合并，未测设备merge/BF16-copy全链时间。
54: scope为Q336/recent1/C65、一个16成员成熟簇、单history KV轮，不代表目标recent256、
55: 多KV或32K/64K。B1增量4.1%尚不足以支持比pipeline多35MiB/rank的默认资源成本，

## gpt_new_oscar_kimi/csrc/experiments/c16_member_pipeline/README.md
[...]
9: 归属、16 成员精确历史域和全部错误状态。将已资格 C4 的 H32 解包、两 score/P 槽
10: 流水、complete-K atomic 累积与下一 KV 预取推广到16成员；每成员 FP32、K128
11: 归约、softmax、归一化和最终旋转顺序不变。两个槽按 member%2 回用，跨核 flag
12: 数量不增加。其余 C1/window/current 路径保留原资格数学。
13: 
[...]
53: Q336/recent1/C65单KV机制形完成全部1008任务、20 AIC/40 AIV、原空间oracle与
54: partial/LSE/status/counters逐位门。stable CV task ticks3888161，pipeline3302518，
55: 局部倍率1.177332；模拟wall587.763/512.878秒。这只计CV核，离线LSE合并检查精度，
56: 未测设备merge/BF16copy全链。单KV接近600秒边界，不再启动C337双KV重试。
57: pipeline建议进入候选选择，B1额外4.1%不足以支持其新增35MiB/rank默认资源成本。

## gpt_new_oscar_kimi/csrc/experiments/c16_rv_reuse_20261015/README.md
[...]
2: 
3: 基底为用户接受的完整 C16 B1 组合，母源SHA固定于`pins.json`。档案#126/#145的
4: 读写所有权、#148/#154的CPU与设备精度边界及完整D.4已重新亲读。生产B1与包装器
5: 保持原样；本目录双臂只用于本地Lima官方CPU/CAModel，不访问真机。
6: 
7: 成熟簇最后16个成员仍依次做原FP32/K128逆旋转。唯一修改是把相同256KiB Rv的
8: `LoadResidentB(0,true)`提到final loop前一次；循环调用原`MatmulResidentB`。
9: 首次装载保留MTE1→MTE2保护上次PV的V读，MTE2→MTE1发布Rv；每成员的
[...]
21: 线程；parsim0、L2、硬件拓扑均与已完成基底一致。任何CPU或超时失败停止，不自动加时。
22: 
23: 计时仅CV核，实际partial离线LSE合并用于精度；不把它写成设备merge/BF16-copy全链。
24: 单KV机制形不代表recent256、多KV性能、32K/64K、NPU、图或整模型native30%目标。
25: 用户已放宽小正增量门，按同库完整净结果决定去留，不拼乘旧不同分母的倍率。

## gpt_new_oscar_kimi/csrc/experiments/c4_atomic_state/README.md
[...]
34: 物理 padding 行126/127使用±0 alpha，单列两路 padding 位差。所有病例有64 B首尾 guard。CPU driver在任何比较之前保存全部输入回读、PV、reference、atomic、三个actor状态，以及各自包含guard的完整字节文件。
35: 
36: **任何位差、输入变更、guard损坏、actor未完成、anti-K128数学见证失败都返回 rc2。** nonfinite 即使类别相同但payload不同，也照实记录位差并返回rc2，不默默忽略。该结果是否涉及完整 C4 的非法输入契约需后续判断，不能由这个独立原型宣布完整 C4 精度通过。
37: 
38: ## 已准备的入口

## gpt_new_oscar_kimi/csrc/experiments/c4_composed_long/README.md
[...]
1: # C4 完整组合：生产 H16 → H32 + member pipeline
2: 
3: 档案 #126/#129/#140/#145/#148/#154–156；启动 §0.7 与完整 D.4。只读取当前工程算子和既有独立实验，不改原生/GDN、服务参数或精度。**2026-10-13最新裁决：当前H16→完整H32/member流水同库CAModel为3540306→2671072 ticks，1.325425倍，通过1.15门，已进入两入口共用candidate。** 原始数学、全部1008任务、336query独立oracle及60actor均通过；CPU1341仍保留超时，CPU337完整证据与大形真实prepare单列。真实NPU/graph/整轮尚未验收，详见下方分后端资格段及`reports/c4_composed_long_20261013/selection.json`。基础设施审批超时期间未自行重复发起Lima操作，真实执行由主线程串行完成。
4: 
5: ## 为什么重开
[...]
25: H32与pipeline作为一个组合只计最终完整CV倍率。H32 helper2.346×不计入；本轮即使完整CV达到1.15，也还要扣除原生current与层外成本，不能直接宣称整轮2–4倍。
26: 
27: ## 资源与精度
28: 
29: - baseline：真实生产H16；workspace1839104 B/core、显式UB157632 B/AIV。
[...]
53: 2. CPU两臂全部完成且逐位/oracle通过后，CANN同库`liboscar_c4_composed_long.so`；`source_binding.json`由CMake配置时写在build根。
54: 3. 复用`tools/experiments/run_camodel_arm.py`，每臂用`cv_replay.py --variant baseline|candidate --fixture FIXTURE --prepared MATCHING_CPU_OUTPUT --library LIB --output NEW_OUTPUT`。prepared必须来自对应臂，不能把仅prepare或另一臂的回执冒充完整CPU资格。
55: 4. `cv_compare.py --old BASELINE --new CANDIDATE --old-control BASELINE_CONTROL --new-control CANDIDATE_CONTROL --output NEW_COMPARISON`。比较器验证同库、同输入/oracle、源绑定、20AIC/40AIV完整输出和真实deadline完成，再以完整task ticks判`old/new>=1.15`。低于门exit2，保留精度通过及实际倍率。
56: 
57: 上面的入口保留初始预声明与失败证据。得到下述完整结果后，统一服务flag才由research升为candidate；该选择不改变原生预算或默认prefix使能。
[...]
76: 两臂CAModel已真实完成：当前H16 **3540306**、H32/member pipeline **2671072** ticks，速度 **1.325425倍**（耗时降低约24.55%）。全部partial/LSE/status/clusterStats逐位一致、336query独立原空间oracle、全部1008任务及20AIC/40AIV完成门均通过。原始VM结果为`/tmp/oscar-c4-composed-backend-split-20261013/comparison.json`。小形CPU337完整、大形CPU1341仅prepare完成、其numeric超时仍保留；没有把它合并为CPU1341通过。
77: 
78: `tools/serving_variants.py`已把C4 flag从RESEARCH移入FEATURE；两个固定candidate命令实际选择已存在的`attention_cv_member_pipeline_cluster4_out`，不只是编译算子。默认C16共享arena无需增大。`tools/probe_c4_member_pipeline.py`改为1341及同地址1373：成熟簇必须执行5轮→6轮，保留全部query/source/错误域、图回放、2warmup/5交替median及1.15完整门，任何失败仍阻断observe服务。39项最小host接线/门契约通过；未改CANN生产源、GDN、status_guard或精度。
79: 
80: 这是C4局部完整路径收益，不能相乘q4/q1局部倍率或当作整轮2–4倍；真实NPU/graph和全模型证据仍待各自验收。

## gpt_new_oscar_kimi/csrc/experiments/c4_kvt_nz/README.md
[...]
1: # 完整 C4 Kt/Vt-NZ：一次有界发布链裁决
2: 
3: 独立研究，不注册生产。档案#126/#140/#145/#148/#154及完整D.4：禁止全历史恢复，保留精度、错误域和跨pipe所有权；工作限定当前KV256。
4: 
5: ## 同库两臂与真实成本

## gpt_new_oscar_kimi/csrc/experiments/c4_member_pipeline/README.md
[...]
14: - candidate：仅扩大 GM stride、增加第二个 KV256 和 score/P 槽、替换成熟 C4 的 `CubeCluster/VectorCluster`，新增槽选择、KV加载、atomic Matmul 三个 helper。
15: - `Process/IsClusterMember`、所有 C1/precise 数学和握手、Softmax、Matmul类型/config/K128顺序、HF32关闭、state spill/restore、输出/status发布均逐字保留。task/core归属、全部1008任务不变。
16: - 每请求仍按原 KV256 顺序更新 FP32 max/sum/acc；没有提前合并、原子多生产者竞争或数学精度变更。H32保留旧 alternating16-row lane错误域。
17: 
18: `generate.py --check` 先调用原 H32 生成器，再核对文件身份。新改动可逆恢复到该源；所有未改方法和 Matmul类型/config 整段逐字对照。`generate_entrypoints.py --check` 对已有完整 C4 的 driver 做明确有限变换并逆向恢复，保留 oracle/guards/status/完成/profile/比较门。

## gpt_new_oscar_kimi/csrc/experiments/c4_unpack32/README.md
[...]
1: # C4 HalfKv32 反量化原型（未启用生产）
2: 
3: 档案：#13–22（metadata/反量化/精度）、#70–73与完整D.4（6.5秒历史恢复禁区）、#126/#144–145/#148/#151/#154–156。只使用当前生产C4及decode padded helper，未读旧失败工程。
4: 
5: ## 现有证据与假设
[...]
9: 本实验只选32行：去掉legacy大plane/index分配，保留四个32B guard mask；natural行stride544B；compareRows64，scale取低32bit、zero取高32bit，liveMask覆盖0–32，scratch1024B。全C4显式UB157760B（旧157632B），acc64KiB不spill、score32KiB仍独立。
10: 
11: ## 精度与生命周期
12: 
13: - INT2位序、FP16 scale/zero、先FP32 Mul再Add不改，无FMA/BF16舍入或全历史恢复。

## gpt_new_oscar_kimi/csrc/experiments/decode_history_pipeline/README.md
[...]
24: | 11 PV ready | AIC FIX → both AIV | one PV result buffer |
25: | 12 norm ready | two AIV MTE3 → AIC | normalized accumulator in former Q plane |
26: | 13 rotation ready | AIC FIX → both AIV | final RvT result |
27: | 14 task done | two AIV MTE3 → AIC | output/LSE/status; all scratch can be reused |
28: 

## gpt_new_oscar_kimi/csrc/experiments/decode_mdl_load/README.md
[...]
2: 
3: 档案 G3–G13/#21/#81–85/#126/#129/#140/#145/#148/#154–156、startup D.4全文已亲读。
4: 独立research；无生产注册、native/GDN修改、AIV NZ publisher或精度放宽。
5: 
6: ## 2026-10-12 已完成结果

## gpt_new_oscar_kimi/csrc/experiments/decode_mmad_barrier/README.md
[...]
21: ## 输入与第一道否决门
22: 
23: `fixture.py`固定8例：M18/M24各正常QK/PV/Rv，以及两例K64/128/192边界抵消。正常链使用BF16输入→独立PR Hadamard旋转→原INT2量化器及FP16 metadata重建；保存codes、packed、metadata和中间P/PV。它是合成输入，不是用户数据集。全部A尾部为+0。
24: 
25: CPU driver逐臂保存输入回读、输出、status及前后guard。A/B未计算尾行必须保留poison，C补零尾行必须数值为0。**live输出只要相对A出现一个bit不同，即打印真实差异、保存结果并返回2；不以5e-3把这个快速否决改为通过。** 独立FP32 oracle仍按冻结5e-3检查；oracle失败会保留并使最终失败，但允许完成第一道old/new比较。CPU通过不能替代设备舍入、完整attention错误域或图验证。

## gpt_new_oscar_kimi/csrc/experiments/decode_task_overlap/README.md
[...]
1: # 同core双task流水 v1：限定协议
2: 
3: 母源为当前 `csrc/kernels/attention_cv_decode_bundle.cpp`，不是旧striped版本。档案#126/#140/#145/#148/#154–156与D.4全文已亲读；仅独立research，无生产、native、GDN或精度门修改。
4: 
5: ## 已执行证据（2026-10-11）

## gpt_new_oscar_kimi/csrc/experiments/finite_guard/README.md
[...]
22: error code itself**. If sentinel and Q bound are safe, only the redundant
23: per-real-row score ReduceSum is omitted. Real-row P, PV, masks, accumulator,
24: rotation, output and status logic stay old; precise source1/window and
25: source2/current always use the old path. No cross-AIV health flag, extra GM
26: workspace, or new synchronization protocol is introduced. At rows=64/128,

## gpt_new_oscar_kimi/csrc/experiments/fp32_bf16_mmad_ratio/README.md
[...]
29: ```
30: 
31: 比较要求两形状各自同库、同SIM、同来源母数据、同grid、相同FP32输出全位及完整180秒control/profile。分别报告R24_QK和R126_PV，不跨形状计算比率。R是**含SDK控制和搬运的完整Matmul任务比**，不是纯Cube峰值；未来分量拆分/重组与控制复用都未测。R较小可以筛掉直接多次完整Matmul拼接，不能伪证所有未知融合算法不可能；R较大也不构成任意FP32→BF16或多分量精度资格。
32: 
33: 当前仅host源码/输入检查。CANN、官方CPU、CAModel、NPU、graph和完整服务均待对应执行证据。

## gpt_new_oscar_kimi/csrc/experiments/fp32_dataflow_20261013/README.md
[...]
1: # q4 的混合 L1 B 数据流研究
2: 
3: 本目录独立于生产。分母固定为 `decode_mdl_load/attention_candidate.cpp`，SHA `f2047dde10aa464202c23c8a8d39a9806c712ac8eb090ff752d7346d1b723151`；FE0、原生源码、精度配置和两个服务入口未修改。所有新内核均由 `generate.py` 可逆生成。
4: 
5: ## 已完成的归因
[...]
45: 1. 对应 fused history dequant+FIA及精确源输入交付。
46: 2. D.4旧全历史恢复6499.8–6655.1ms、写入209–215ms是禁区；不是当前百分比。
47: 3. 固定KV256/单L1槽，无全历史恢复，数学与finite/错误域原样保留；#126/#145/#154决定跨pipe双向所有权，#129决定任务全覆盖，#148决定精度与模型证据边界，#157禁止改冻结guard。
48: 4. 真实GM逻辑字节不减少；收益假设来自消除ND2NZ历史装载与precise重排相抵的成本。只有完整新配对支持倍率，不乘旧Normal→MDL比例。长形资格不是20–64K全服务或native2–4倍验收；NPU、graph、模型质量和整轮性能未验。
49: 

## gpt_new_oscar_kimi/csrc/experiments/hadamard_batch8/README.md
[...]
1: # 紧凑 Batch8 Hadamard，独立研究
2: 
3: 档案 #13–22/#70–73/#126/#145/#148/#154–156 与 startup D.4。未改生产；本目录不注册算子或服务开关，VM由root排他安排。
[...]
5: ## 当前真实路径与差异
6: 
7: `impl.py:161–163` 的 Q 旋转仍调用canonical `rotate_out`；`rotate_clip_store.cpp:44–54` 每核重复4096个scalar索引/sign写入，`76–116` 仍逐row执行Hadamard。striped writer已合入向量Init和SIMD pack，但 `rotate_clip_store_striped.cpp:100–110` 的Transform仍逐row。不是重复计算此前writer1.796×收益。
8: 
9: 三臂writer：此前冻结 `writer_baseline.cpp`（old）、此前冻结 `writer_pack_init.cpp`（current，和当前生产逐字对应）、本目录 `writer_batch.cpp`（在current上仅改紧凑Transform及work容量）。三臂Q rotate：当前canonical原文件（old）、只向量Init的 `rotate_init.cpp`、向量Init＋紧凑Transform的 `rotate_batch.cpp`。
[...]
11: `generate.py --check`验证旧writer固定哈希、current与生产映射、新源逆向恢复；canonical与全部helper哈希写入构建绑定。不改旧A/B/C源码、fixture或报告。
12: 
13: ## 算法、空间、精度
14: 
15: 每stage执行所有row的原Gather到各自`work[row*D]`，一道PIPE_V；再逐row原Mul(sign)，一道PIPE_V；最后对`rows*D`一次Add，一道PIPE_V。每row的Gather→Mul→Add仍以distance1…D/2顺序执行，Gather只从该row输入读取；无跨row归约。最后统一Muls原FP32 normalization。阶段间所有数据依赖保留，MTE2/V/MTE3跨管道屏障与状态检查不变。
16: 
17: 每stage索引/sign仍各D个（D256总16KiB）。work从1KiB扩大为8KiB，索引Init数据量不变；未采用需要128KiB索引/sign的全展开方案。显式D256 Hadamard UB：engine50272B，完整writer61440B，RotateOnly51392B。非Hadamard仍分配原1KiB work并执行原generic Transform；本次不重做已测只有约0.3%整步收益的identity单点。
18: 
19: Full8/D256按源码发射数：
[...]
38: 
39: ```bash
40: python3 csrc/experiments/hadamard_batch8/generate.py --check
41: python3 csrc/experiments/hadamard_batch8/entrypoints.py --check
42: ```
43: 
44: CMake设置`ASCEND_HOME_PATH`、`SOC_VERSION=ascend910b4`。CPU加`OSCAR_BATCH8_CPU_DEBUG=ON`，writer为`oscar_batch8_store_cpu FIXTURE NEW_OUTPUT [0|1|2|all]`，默认只执行current(1)→batch8(2)，逐臂立即保存全部回读并按字节oracle/guards比较；显式1/2可分别运行，旧writer不重跑。`OSCAR_BATCH8_STORE_ONLY=ON`可只构建writer入口。CPU固定120s。完整库`liboscar_hadamard_batch8.so`含全部六臂；CAModel单臂固定180s，通过现有有界supervisor执行，不自动重试。
45: 
46: Writer fixture已导出：`/private/tmp/oscar-hadamard-batch8-writer-fixtures-20261010/`，N128/H1/D256 suffix-padding与N16/D64非零clip；独立oracle内容沿用已冻结writer fixture，只新增源绑定。
47: 
48: Query rotate fixture在`artifacts/hadamard_batch8_rotate_20261010/`：主N128/H6/D256，另7个紧凑例覆盖1/7/8/9rows、D64/128/256、BF16/FP16、partial/allpadding、±0与非有限值。CPU入口`oscar_batch8_rotate_cpu FIXTURE NEW_OUTPUT [ARM [BASELINE_DIR]]`；默认0old/1Init/2Batch8依次执行。单臂1/2必须带已经通过的0臂目录，并核输入/shape及完整output/status字节；独立finite2e-3沿冻结store_dequant，仅独立host oracle的NaN按类别核实，跨臂NaN payload/±0仍逐字节。
49: 
50: ```bash
51: python3 csrc/experiments/hadamard_batch8/replay_writer.py --arm current --fixture FIXTURE --output NEW_OUTPUT --library LIBRARY --simulator-config CONFIG
52: python3 csrc/experiments/hadamard_batch8/compare_writer.py --directory THREE_ARM_REPORT_DIRECTORY --output NEW_COMPARISON
53: ```
54: 
[...]
57: ## D.4四问
58: 
59: 对应rotate与phase1_stores；旧失败full-history恢复6499.8–6655.1ms不能重现。本方案只增加固定7KiB work，不读历史、不造完整BF16 KV、不改旋转或量化语义。源码发射削减不是NPU毫秒，完整算子与整轮结果仍以实际完成证据为准。

## gpt_new_oscar_kimi/csrc/experiments/request_window_decode_profile/README.md
[...]
43: | 13/15/17 | AIC等KV/P/AIV累加；history pipeline原来没有17，保持0 |
44: | 14/16/18 | 原Matmul helper的QK/PV/Rv阶段；含SDK搬运、提交和已有同步，不能称裸Cube busy |
45: | 19 | AIV归一化开始到函数结束，包含22旋转等待和21最终写回 |
46: | 20 | 所有LoadTask，包括padding/follower；marker统一归total，SYS_CNT计数在元数据读完后也记入读到的source |
47: | 21 | PublishRows，包括padding/错误行路径；保留所有status写入 |
48: | 22 | 原旋转/规范化/任务完成等待；按actor分别计 |
49: | 23 | actor Init+Process，不含诊断flush；只在total有值 |
50: 

## gpt_new_oscar_kimi/csrc/experiments/request_windows_attention/README.md
[...]
116: 
117: `tools/request_window_reader_gate.py` exports `REQUIRED_CAPABILITIES`,
118: `run_reader_gate`, and strict `validate_evidence`. Its result has `accuracy`
119: and `graph` dictionaries for the main `probe_request_windows.py` to attach.
120: The caller supplies the already selected real NPU, actual Cube count, full

## gpt_new_oscar_kimi/csrc/experiments/request_windows_store/README.md
[...]
31: ## 写入与竞争边界
32: 
33: `generate.py` 原样提取 `rotate_clip_store_striped.cpp` 的 RotationEngine、ClipQuantize，记录原文与 helper SHA。只改变 packed 目的地址：
34: 
35: ```text
[...]
52: CPU probe 对 packed/status 做三方比较：独立 PR golden、原 striped 核、实验 packed 核。原核通过等价 slot 映射把双段映为 `2*blocks` 个旧段，数值数学和最终地址一致。新窗口另与逻辑位置字典 oracle 的完整 BF16/tag 字节比较；包括未写 NaN payload、signed zero、prefix/gap/suffix guard。
53: 
54: 主机 fixture 共19例：小请求、非128对齐 segment、物理页跨界、请求重排、negative holes、rollback0–3、epoch复用、all-padding poison、多 head 数值/地址故障、D256 clipping+Hadamard、N128/32live/Hkv2、非法 epoch、重复 lease、position越域、非法 qstarts、正qstarts起点、正slot尾部、全部capture padding未发布map、128个非空request行中仅32行live且其余map未发布。
55: 
56: ```bash

## gpt_new_oscar_kimi/csrc/experiments/shared_fp32/README.md
[...]
7: The producer reads striped INT2 once into one at-most-8192-row rotated FP32 K/V buffer. It preserves stored FP16 metadata and FP32 multiply then add. The consumer retains the fe0 QK, KV256 softmax/PV recurrence, masks, per-lane status and final Rv transpose. Complete KV256 matrices go directly from shared GM to Cube. Each original task's incomplete last KV256 gets a private copy with zeros beyond its original `kvend`, so pre-mask checks and zero-times-NaN behavior retain the original domain. Producer row errors are consumed only within that task's original per-lane rows.
8: 
9: Raw FP32 accumulator, maximum and sum remain in UB within each 8K tile. Only these raw states and the error code are saved at the boundary; normalization and Rv transpose happen once after the last history tile. Query values reload on a new launch, but their original finite check executes only on the first block so a carried metadata error cannot be overwritten. Producer, consumer and next producer must use one ordered stream. The shared K/V capacity is 16 MiB plus a 32 KiB row-status buffer, independent of context length; per-query state grows with the number of query groups. No whole-history inverse rotation or BF16 restore is used.
10: 
11: D.4 comparison: this is the history expansion/FIA phase. The historical full restore cost 6499.8–6655.1 ms/card while FIA was about 18.7 ms. Sharing a bounded block removes repeated expansion and publication across query groups, while adding producer launches, query reloads and occasional state copies. Those structural changes do not establish target latency. Source0 performance must compare the sum of producer and all consumer work against the current striped C4/C16 route selected for the same shape; fe0 is only a numerical reference.

## gpt_new_oscar_kimi/csrc/experiments/striped_store_simd_pack/README.md
[...]
1: # Striped store：精确 SIMD pack 与 Hadamard Init 三臂研究
2: 
3: **本目录保留固定的已测研究三臂；候选writer源码已整合，尚未推送。** 2026-10-10，root已完成两个完整writer用例的CPU-debug三臂，以及同库、同输入N128/grid16完整writer的CAModel三臂；逐位、独立oracle、guards均通过。组合方案的完整writer CAModel为原来的0.5568倍耗时，即**1.79586倍局部加速**。目标NPU、图与完整服务收益尚未验收；不能把这一结果换算成整服务提速或原生基线达标。
[...]
9: `tools/serving_variants.py`统一候选配置；`cache_storage_ops.store_current`按实际cache_format选择：`striped_v1`调用`rotate_clip_store_striped_out`，`striped_request_window_v1`调用`rotate_clip_store_request_window_out`，`canonical_v1`调用`rotate_clip_store_out`。`active_identity_store`未注册生产CMake/contracts/selector，其2026-10-06局部证据不代表已经部署。
10: 
11: writer在校验slot前仍对K/V做旋转和量化；负slot最终覆盖status为0。`ClipQuantize`先做原FP32 ReduceSum检查、可选clip、min/max；scale/zero先FP16舍入再参与除法/加0.5/clamp/int32截断。冻结旧D256 writer每侧末尾pack有256次Scalar GetValue和64次byte SetValue，K/V合计512读+128写/token/head；本轮替换这一段。默认config的clip_ratio为0，不执行Sort32/MrgSort；不能把默认写延迟归于percentile排序。
12: 
13: request-window writer仍使用同一个量化/pack数学前缀；它有packed与window两个同stream launch，后者只发布至多323个精确窗口行，没有再量化。本轮仅将精确pack/Init接入两条striped writer，不改slot/epoch/MTP生命周期。
[...]
24: | CANN，同一个三臂库 | 构建完成，随后三臂均真实运行 | 不能替代目标NPU完成 |
25: | CANN，整合后的生产全库 | `tools.build_ops`干净重编通过；四个正式源SHA与host一致 | source signature `0687dfd3983614a05cb08498fcc6519dc9ccd8718c21230d2d1448b3bbbd3f4e`，不是NPU完成 |
26: | 官方CPU-debug，整合后的request-packed接缝 | `clipped_hadamard_d256`的正式striped、request-packed及window全部bytes identical通过 | 独立PR oracle、raw/tag/status/guard与新共享头整合 |
27: | CAModel，N128/Hkv1/D256/BF16，grid16，112 live/16 padding，Hadamard，clip0 | 下表三臂均通过bytes/oracle/guards/inputs、真实control、完整task/AIV profile及严格compare | 完整writer局部周期，可进入生产整合准备 |
28: | 目标NPU、NPU图、完整服务 | 本研究未执行 | 均待验收 |
29: 
[...]
44: | old | oscar_rotate_clip_store_striped_kernel | 冻结的旧生产原源码，见下方SHA |
45: | vector_pack | oscar_rotate_clip_store_striped_simd_pack_kernel | 只替换末尾整数pack |
46: | vector_pack_and_init | oscar_rotate_clip_store_striped_simd_pack_init_kernel | 上项加独立精确Hadamard索引/sign构造 |
47: 
48: 旧生产SHA固定为 `0515fd2a527812dc6e7c09e46ebae50fd19be62e7645705c8caffbb132a31d29`。`writer_baseline.cpp`只调整两条相对include，文件SHA为 `674b6115f93b1c8387bdc8ba8440218c7b1e78e3563cb4f76e37624e0eae62eb`；逆向include重定位后必须恢复旧生产SHA。`frozen_sources.json`同时锁定已测B/C、pack helper、CPU harness及共享依赖的SHA。B/C不再从变化中的生产writer生成，现有实测报告不改写。
[...]
50: `generate.py --check`检验固定三臂并可逆校验新生产writer等于已测C臂；`--check --frozen-only`用于独立复现旧实验，不要求未来生产仍停留在同一版本。CMake的CPU和CANN目标均编译`writer_baseline.cpp`，并在构建目录写`frozen_source_binding.json`。新fixture记录该来源；新replay要求库的构建清单相同，并报告实际编译源SHA。compare仅允许完整旧报告（原生产SHA与已测helper SHA均一致）或完整新冻结报告，拒绝混配，不能把更新后的生产源码重新标成old。
51: 
52: B保留原RotationEngine::Init；C只在Load前借用死input/work/red生成完全相同indices和±1 sign，Transform算术不变。本轮冻结仅通过host生成/哈希/可逆映射检查；没有重新编译或模拟，不新增性能结果。
53: 
54: 两候选都不改归约树、Div、量化bin、clip次序、half metadata、错误优先级、WriteRaw、tags或发布边界。保持原来“先两侧成功，后cache发布”，保留负slot/非法slot/负position的覆盖顺序。
[...]
66: 已生成 `artifacts/striped_store_simd_pack_20261010`：
67: 
68: 1. `n128_h1_d256_bf16_b128_suffix_padding`：Hadamard、112活跃/16负slot padding、grid16、clip0。
69: 2. `n16_h1_d64_bf16_b128_clip`：Hadamard、grid2、K clip0.75/V clip0.95，并覆盖D64两侧不对齐pack边界。
70: 
71: 继续使用既有独立PR rotation/quantizer oracle，只有这两个固定fixture的Hadamard选择在私有函数副本中显式设置，不修改旧oracle模块。比较完整packed、FP16 metadata、raw BF16 NaN poison、tags、status、输入和前后guards，任何字节差均失败。
72: 
73: pack-only另备D64/128/256各65536个word模式，在**每个word位置及K/V两侧**遍历完整16-bit域。不同位置使用不同可逆偏移，避免同值广播掩盖错位；metadata与邻接区为poison。该完整输入约D256 128MiB，输出10MiB；只准备入口，不自动运行长模拟，截止不超过180秒，失败不扩限。
[...]
110: ```
111: 
112: 比较器要求完整task与所有AIV profile、真实rc0/未timeout/清理完成、全部保存文件hash/guard/oracle相同。它只报告完整writer ticks；pack访问次数和Init局部7.11倍都不能替代该比较。已测完整writer局部1.79586倍；目标NPU、graph及整轮收益仍另验，不扩大这一结论或放宽任何精度门。
113: 
114: ## 最小生产整合（CANN/官方CPU完成，NPU门待验收）
115: 
116: 1. 已将资格版本`pack.h`和`hadamard_indices/vector_indices.h`映射到`csrc/kernels/striped_store_pack.h`与`hadamard_indices.h`。`tools/package_request_window_kernels.py`逐字校验仅include/来源注释改变且可逆；保持原Cast/ShiftLeft/Or、D64窄写回、Cast→Not依赖与全部barrier，不新增ABI、op或候选flag。既有`tools.build_ops`对全部`csrc/`做文件指纹，新头会触发重新构建。
117: 2. `csrc/kernels/rotate_clip_store_striped.cpp`已复用两个helper。`csrc/experiments/request_windows_store/generate.py`继承相同helper，再通过既有packager生成`csrc/kernels/rotate_clip_store_request_packed.cpp`；生成器新增`--check`校验生成体和共享头SHA，packager保持非include正文逐字一致。`rotate_clip_store_request_window.cpp`只负责窗口发布，本轮未改其正文。
118: 3. 真实主`rotate_out`位于`csrc/kernels/rotate_clip_store.cpp`（由`rotation_bindings.cpp`调用`rotate_launch`），本轮保持原样；canonical/fe0也未改。将来若共享Init，**须单独做旋转资格，不套用本轮writer证据**。它的canonical pack排列不同，不能使用striped pack helper。
119: 4. 保持`tools/serving_variants.py`与`cache_storage_ops.store_current`原有dispatch，无新增用户参数。完成后再确认`install_serve.sh --variant candidate`与`install_observe_serve.sh --variant candidate`均构建并实际装载相同新实现；后四卡只改变显式设备/端口。本研究当前没有修改任何服务入口。
120: 
121: ## 现有真NPU门只需补齐的边界
122: 
123: - **striped store的Hadamard分支（探针已补，设备未跑）**：旧`tools/probe_striped_cache.py::store_gate`及`_store_changed_input_graph`虽传Hadamard矩阵，调用参数实际为`hadamard=False`。本轮保留原dense分支，追加一次`True`的完整bytes/metadata/raw/tag/status/guard及同地址K/V改变图回放；不能把旧dense gate视为Init验收。host测试确认两种参数均传入op且Hadamard失败不会被吞掉。
124: - **D64的16B边界及D128对齐**：复用现有原语golden准备，给实际striped writer补D64夹值病例，逐位检查K/V相邻16B、metadata及poison；D128补短字节病例确认aligned分支。N128带padding的D256病例同时验证scratch复用，无需真机运行65536词长枚举。
125: - **request-window生命周期**：`tools/probe_request_windows.py::case_plan`已有`segment_boundary`、`reordered_hkv2`、`clipped_hadamard`的`hadamard=True`，`run_store_graph`也已有N128/32 live的True路径、全padding捕获→同地址live/lease/epoch/position变更。复用这些门与既有独立PR/poison检查，确认生成writer实际包含新helper即可；不得删掉非法状态、rollback、stale epoch等现有门，也不需要另造大型probe。
126: - **仅在主rotate_out也改Init时**：保留`tests/test_rotation_npu.py`已有D64/128/256×Hadamard开关、masked/error与两种clip的全部goldens；该文件当前不提供图验收，额外补一个真实主rotate的同地址输入/slot改变图回放与eager对拍。未改主rotate时不为此追加无关验证。
127: 
128: 本轮17项相关host测试及7项既有固定入口/候选选路回归通过；冻结研究生成器、request-packed生成器、packager的`--check`均通过。root随后完成生产全库干净CANN构建及`clipped_hadamard_d256`官方CPU接缝，实际记录位于`reports/quant_production_integration_20261010/integration-summary.json`与`request-packed-cpu-seam.log`；先前失败的增量编译日志也保留。当前未推送；上述证据不能替代NPU、图或整服务性能验收。

## gpt_new_oscar_kimi/csrc/experiments/window_batch_decode/README.md
[...]
26: BF16 K/V DMA; invalid or unvisited future rows are never fetched. The existing
27: FP32 destination is initialized to +0 as before. BF16-to-FP32 Cast keeps its dtype
28: and rounding mode; each valid row retains the original ReduceSum finite check.
29: 
30: Tag scanning for DMA does not publish errors. After loading, the second scalar

## gpt_new_oscar_kimi/docs/64k_120_optimization.md
[...]
5: 档案依据：#26–49/#69/#127–129/#137/#140/#142/#145/#148/#151–155、启动文档 D.4。工作从当前 `4defe20` 开始。本文随实现更新，不能将计划、字节推导或本机模拟写成真机通过。
6: 
7: **2026-10-12 当前目标**：单项完整相关路径相对当前基底至少1.15倍，精度/协议合格后可入组合；组合相对原生1342.4437259秒达到2–4倍，即335.61093148–671.22186295秒。默认prefix caching开启。旧2–3倍与none布局估算保留历史身份；不能拼乘单项或把helper收益当整轮通过。
8: 
9: **2026-10-10 历史验收目标（已更新）**：用户接受64K整轮相对原生提速2–3倍，并要求不同长度、并发和阶段通用。以已提供native1342.4437259秒为分母，目标为671.22186295–447.48124197秒（约11.19–7.46分钟）；此前4–5倍为历史目标。省略token-budget参数、FULL KV 6–7倍、原生GDN与冻结数值要求均保持。局部writer1.796×和unpack2.346×仍不能直接当作整轮预测。
[...]
42: ## 本轮范围与目标
43: 
44: 2026-10-09 用户新增优先级：重点压缩 OSCAR 量化/反量化及必要搬运成本。当前真实路径、待替换的标量打包、C4 16→32行方案，以及已完成的 Hadamard 索引向量化局部证据，集中记录于 `docs/quantization_hotpath_20261009.md`。元数据原型7.11×不作为完整写入、注意力或整轮收益。
45: 
46: - 只使用本轮 65,100 输入、512 输出、120 请求、客户端并发上限32的证据。LongBenchv2 后续仅作精度测试，不再用于性能研究。
47: - 原文：`reports/target_64k_120_20261009.txt`；SHA256 `03eb53109a97a3e82b02c91550b5661dc8cf0c3360585693f567a3217c7311bb`。用户提供数据，未生成或索取“真实数据集”。
48: - 保持 INT2 语义、冻结精度、原生 GDN 计算、MTP状态和外部插件边界；最终仍通过两个 candidate 一键入口交付。
49: - **用户已明确显存6–7倍以FULL注意力KV为目标，同时报告全部KV。** FULL KV、FULL+GDN/MTP KV、固定workspace与整卡HBM分开列账；并发峰值不能替代字节比，也不能推出等比例提速。
50: - **用户已明确速度分母为原生22.4分钟，最新接受2–4倍**：整轮目标335.61–671.22秒，相对历史当前OSCAR约需3.68–7.35倍改善。旧268.49–335.61秒属于已替换的4–5倍目标。
[...]
60: - [ ] T07：实现紧凑FULL页池及稳定请求身份的精确S/R/MTP窗口，消除按所有历史页重复付费。
61: - [ ] T08：验证FULL/GDN分配接缝与真实字节预算；必要时去除分配padding，保持GDN原始状态及计算。
62: - [ ] T09：校验MTP接受率下降的工作量影响；精度与性能分开，不能拿接受率改动充当无损优化。
63: - [ ] T10：冻结数值/非法输入/生命周期/跨页/释放复用/图检查；Lima CPU-debug与CAModel必须排他串行。
64: - [ ] T11：复算改后容量、整轮时间及长尾，标记是否达到相应目标；不足则继续结构优化。

## gpt_new_oscar_kimi/docs/64k_decode_transfer_audit.md
[...]
29: | PV(i) | 解包/写 V(i+1) 到另一 buffer，发下一 `KvReady` | 读 P、V(i)，PV→GM；`PvReady` | V 当前与下一份同时存活 |
30: | 累加 | 读 PV，加到 UB accumulator | 可开始下一 QK | 下一 `PReady` 必须晚于本次 PV 消费 |
31: | 最后 | FP32 normalize，写 GM accumulator | FP32 inverse rotation，再交 AIV | K/V 已死，可另行复用空间 |
32: 
33: 额外约束：`:658–665` 在前一个 PV 已累加后，按 K0,V0,K1,V1 原顺序提交预取错误；不能让下一 tile 的错误覆盖更早的 score 错误。`:547–554` 的 P 写回使用 **MTE3→MTE2**，防止下一次 score DMA 提前复用 UB；不能只换成 MTE3→V。这些是档案 #145/#154 同类问题的生产防线。
[...]
48: 这里的“1 MiB”是已写出的 GM 接口工作量，不等于 1 MiB HBM 访问；L2 可命中，SDK 内部也可能重复读。q4/q1 相对这部分字节的有效计算强度分别仅 6 / 1.5 FLOP/B；不能据此直接认定设备瓶颈，因为解包、softmax、同步、Cube 内部 padding 和 native 模型时间还在。
49: 
50: 另有 Q、score/P、PV、最终旋转及 metadata/status 流量。其精确值不能统一按活跃行计算：例如 `:453` 每个活跃 AIV 始终读16行 score，而 `:550` 只写实际活跃 P 行；q1 只有6行，q4有24行。K/V 的上述完整 tile 发布仍与 qcount 无关。
51: 
52: 上下文 C=65100、S=64、R=256、同请求 q4 从当前上下文起始时，历史候选区间为 `[64,64848)`，长度64784。生产 task 公式在 `csrc/kernels/attention_tasks.cpp:128–145`。S1 需要 `ceil(64784/256)=254` 单元；S3 按原生任务等宽划分需要 `3×ceil(ceil(64784/3)/256)=255` 单元。因此单 FULL 层/单请求/q4 的 K/V GM 交接为254或255 MiB；窗口/current、头尾 padding、Q/score/P 和旋转另外计算。S3 的活跃 packed 行仍只读64784×136 B；FP32 tail 仍按完整256发布。后续 token 的实际区间应代入对应 context，不把这个例子当整轮实测。
53: 
54: 单 core workspace 是：
[...]
61: ```
62: 
63: 四个 B 平面是两份 K 和两份 V。其余三个 M×D/M×B 区域用于 Q、score/P、PV/rotation；UB accumulator 跨256单元保留。权威公式也在 `csrc/include/oscar_attention_launch.h:24–27`。20 core 是本次设备形状假设，不应覆盖 runtime 实际 core 数。
64: 
65: ## 3. A2 与其他架构的证据边界
[...]
165: ### 门B：一次逻辑KV256，保住数学与错误契约
166: 
167: 在门A通过后才做K128两次QK列块、原score256/softmax/PV。与当前生产输出逐项比较：INT2恢复的K/V bit patterns、QK各score、P/FP32 max/sum、PV、partial、LSE、两AIV status、最终旋转；不要只比最终token。q1/q4、D256、GQA6、全零/极端finite/NaN/Inf注入、空源、KV尾1/127/128/129/255/256/257、非连续页、S1/S3、padding孔、两个不同请求、MTP拒绝回退均需覆盖。验收阈值取冻结配置；不为新分块放宽。
168: 
169: ### 门C：有限decode设备基准，确认收益确实来自传输
[...]
195: | q1，同case candidate | 同路径 `-candidate/...:90,101` | 相同 M6 编码 |
196: 
197: 将XT低36位按连续12位字段展开，分别为 `(24,128,64)` 与 `(6,128,64)`；结合已知QK/PV的M/N/K调用、basicN64/basicK128和后继累加对，可对应 **M24/M6、K128、N64**。高位的初始化/累加控制不同。完整q4 `core0.cubecore0.instr_log.dump.gz` 有104条MMAD，全部都是 `(24,128,64)`，其中两类控制值各52条；它对应6个KV单元的QK/PV共12次matmul，加一次Rv旋转，即 `13×(4个N64×2个K128)=104`。core1没有MMAD。该actor原始gzip完整，不能用只保留selected lines的txt去数总次数。
198: 
199: q1的现存core0样本明确是 `prefix_capped=true / complete_for_actor=false`，只支持所见指令M6，不支持完整kernel的MMAD计数或时间占比。上述样本是当前bundle之前、具有同一GM float Matmul配置与真实M参数的已存克隆；当前bundle的history保留这些参数及K128基础分块，新增tail逻辑只改变precise source的N/K。**本轮没有当前bundle的新反汇编或NPU MMAD trace**，因此不把旧样本冒充当前二进制逐指令身份认证。
[...]
245: packed DMA只占原actor总span的0.710% /0.660%。AIV0六次调用为630、2705、767、2525、1086、2534 tick；其范围包含buffer清零、Physical页表查询、DMA提交与MTE2完成等待，并非纯DMA引擎占用。没有逐burst服务时间、MTE排队、实际HBM/L2计数来证明瓶颈来自136 B行长。即使将旧AIV0该phase完全删除，单纯串行账的history理想值也仅 `1/(1−0.03097)=1.032×`，整个actor约1.007×；这只是该旧样本的条件上界，**不是bundle或64K预测**。两个AIV是并行生产者，不能把两者DMA cycles相加再声称翻倍的可省时间。
246: 
247: 其AIC history span317,698：QK25,773（8.112%）、PV33,751（10.624%）、rotation7,277（2.291%）；其余主要是等KV84,279、等P122,150、等AIV累加31,157及控制开销。QK/PV标记覆盖SDK提交、内部搬运和已有同步，并非裸MMAD执行份额。KV publish只有714 cycle也不代表512 KiB/单元的后端搬运免费：异步完成和排队可能由下游wait承受，不能把各类等待全部归因给GM写或“小行DMA”。
248: 
249: ### 9.3 大相位中哪些已经改掉

## gpt_new_oscar_kimi/docs/64k_latency_budget.md
[...]
96: - 28023个KV256恢复单位；相应FP32 K/V GM发布13.683GiB。
97: - 17856个簇-KVtile的在线状态restore/spill，GM读写70.295GiB。
98: - 对这些history单位的OSCAR QK/PV、softmax、flags和输出逆旋转路径；相同causal配对转由current FIA完成。
99: 
100: 这些是源码copy量与数学路径变化，不是实测HBM事务或节省秒数。实际120请求的chunk/Q/C/S轨迹未提供，不能把理想字节直接乘120、套某个带宽，再宣称整轮完成时间。
[...]
108: | GDN预填充 | 120×65100×48 = **374,976,000个layer-token位置**；不能取消状态计算或改变GDN数学 |
109: | 主模型与首draft的线性/MLP路径 | 相同Q假设下120×65100×65 = **507,780,000个layer-token位置**；矩阵维度/实际TFLOP率未随本轮日志提供，不能从“27B”直接伪造算力下界 |
110: | FULL持久化写入 | 120×65100×17 = **132,804,000个token-head/层位置/rank**；仍要精确窗口、旋转/量化/INT2编码 |
111: | 长上下文decode | 完整target q4及三轮MTP依然读取65100级历史；当前的request-window布局主要省物理字节，不删除这些读/解包/QK/PV |
112: 
[...]
122: |---|---|---|
123: | 完整whole65100准入＋bounded arena | 合法fresh域移除上述C16恢复与state traffic；短probe同时测完整P、首MTP、真实峰值HBM与decode邻居等待 | 不将13.683/70.295GiB换成假秒数；不把CPU调度契约当NPU已通过 |
124: | MTP显式identity旋转专化 | `runtime._prepare_rotations`明确draft identity但hadamard=False；`rotate_clip_store.cpp:103–113`通用分支对每列做Mul+ReduceSum。D256时每K/V token有2×256个向量dot reductions，完整首draft65100约33331200次此类reduction调用（不含其它相位） | 可研究精确identity专化，仍须保持有限值检查、负零/字节、clip与quant舍入；不能改MTP算法或旋转语义。此为源码机会，未引用旧实验耗时 |
125: | q4/q1历史解包与GM交换 | `attention_cv_decode_bundle.cpp:214–237,423`仍按KV256产生FP32 K/V再QK/PV；每token packed约136B，而发布FP32 K/V约2048B，另有score/P/PV。需新短profile给出unpack、发布、等待、Cube与GDN/MLP/通信时间 | 不能把INT2 7.53倍编码比当全历史device流量比；片上/L2命中未知，源码GM字节不等于DRAM字节 |
126: | MTP三轮与验证batch效率 | 本轮请求级事件可识别，完整K32 cycle未知；q4/q1/C16等路由已存在，N128/B32并非旧16K padding场景 | 不重复宣称已消除的padding收益，不关闭MTP，不降低精度或隐藏拒绝 |
127: | wrapper/prepare/status/量化写入融合 | 可以在外部边界减少自身重复metadata与launch；native GDN仍执行原有运算 | 尚无本轮host/device归因，不能把小相位优化算成整轮大幅收益 |
128: 
[...]
141: ```
142: 
143: 这次命令成功完成离线数据核算；没有生成或执行性能模拟，没有修改生产源码、CANN、GDN、默认配置或验收门槛。GPU/图/精度/完整服务/实际268–336秒目标均未由本报告验证。

## gpt_new_oscar_kimi/docs/64k_performance_source_audit.md
[...]
103: ```
104: 
105: `:305–374` 两阶段处理未成簇组与簇；`:920–954` 每 KV256 只执行一次 LoadPacked/Unpack/Publish，却对 16 个成员逐个 RestoreState/Softmax/PV/SpillState。`:478–501` 也保留独立 QK/PV 和最终逆旋转。因此“16 组复用”不是 attention 16 倍加速。
106: 
107: 在第 3 节的理想四块形状下，后三块 C=16384/32768/49152，H=C−64。前 12 组分别少 235,214,…,4 行，合计 1434；packed 恢复行数为 `76H−1434,76H−1434,70H−1434`，对应 KV256 恢复次数 **4861、9725、13437，共 28023**。
[...]
134: ```
135: 
136: 20 Cube、Hkv1 时 N128→S3，而 N≥16K→S1。拆出的 short prefix 保留 S1；later-MTP compact 同样保留原 N（`compact_later_mtp.py:145–147`）。这会保留原分段数学和 FP32 合并顺序；不能直接删掉字段后声称无精度影响。K32 的 32 个独立 history leader 也已能覆盖 20 核，S1 不是严格三倍浪费证明。
137: 
138: later-MTP 的 compact 条件是 `N>=1024 && N>=8*B`（`:25–28`），并严格限定真实 eager、后续 draft、模型/通信契约；`:148–162` 只把模型输入缩到 B，输出无需再扩 N。因此大 mixed prefill padding 已有处理。常规 decode N128/B32 不 compact，仍做两轮 q1 padded 模型调用；这是潜在小范围专化机会，不能引用旧 16K padding 成本把它夸成当前大头。
139: 
140: 长 history 在主模型 q4、首 MTP 以及后两轮 MTP q1 都真实存在。三个 MTP 调用不是由 first-MTP current FIA 消掉了整个 attention。MTP layer 明确用 identity（`runtime.py:390–406`），也不能把所有 hadamard=False 当可任意省略的旋转。
141: 
142: 若本轮 acceptance 较低，完成固定 512 输出需要更多完整 target+draft 迭代，长历史成本随之重复。应直接记录每个完成 step 的接受 token 数和实际输出数；打印的聚合 acceptance 窗口不能单独还原迭代次数，更不能据此判断量化是否超出冻结精度门。
143: 
144: ## 6. 结构候选与最小验证
[...]
146: | 优先候选 | 具体作用 | 最小有效验证（由主代理统一排他安排） |
147: |---|---|---|
148: | 65,100 fresh whole admission + workspace 联合设计 | 消除后三块的压缩历史 prefill，扩大现有合法 current-only 域；保留后续 INT2 store/decode。先算真实激活、GDN、KV 与 scratch 总预算，避免额外约 1,110 MiB/rank 的简单扩容损害并发。 | 纯调度契约覆盖65100、65024/65025、剩余预算、等待/恢复、K32与128保守预留；单个65100 fresh的完整FULL/current+store/首MTP短探针，逐级记录峰值内存与精度。再与decode并存的短服务probe比较TTFT/ITL，不能仅报prefill变快。 |
149: | C16 state/DMA 成本下降 | 保留每原KV256数学顺序与错误域，消除重复资格扫描；探索可变尾簇和更合适的 query 微批，联合优化 KV 复用、state 搬运和核占用。 | 当前 C16 的同源 phase 计数：unpack/publish、state restore/spill、QK/PV等待、softmax/acc、最终写回；记录 actor，不相加重叠相位。先同shape独立oracle与逐位旧新，再短同核/同input A/B。禁止全历史恢复或仅换更漂亮shape。 |
150: | 长历史 prefill 的服务准入/分块策略 | 控制长块插入造成的完整step延迟；whole 的吞吐收益与decode等待必须同时评估。mixed attention split 本身不等于请求级隔离。 | 仅针对65100上下文：采样连续几步scheduler输出（请求、Q、C、N、S、路由、实际接受/输出token）、CPU提交与NPU completion时间；覆盖decode-only、混合、fresh admission。不要再次跑AISBench。 |
[...]
155: ## 7. 归档约束
156: 
157: 已按启动文档 §0、档案索引、#129/#140/#142/#145/#148/#151–155 及完整 D.4 原始日志审阅。D.4 的全历史恢复、host 准备和逐 token 调度失败不应重现；#142 的 warmup/capture 判定、#145 的异步 UB 所有权、#148/#154 的独立 oracle 与冻结精度、#155 的 NaN/window 字节语义均须保留。
158: 
159: 本审计不提出原生 GDN 修改、不调用独立测试 oracle 到生产、不恢复整段 BF16 history、不放宽 `configs/acceptance.json`。编译、CPU、CAModel、真 NPU、图、短服务与完整负载性能是分别记录的门；本文只提供源码结论和待验证的结构方案。
[...]
219: - **大 forced dummy 确实存在于可选动态profiling路径**：Ascend `worker.py:847–852` 的 `profile_prefill_latency` 调 `_dummy_run(num_tokens, force_attention=True, profile_cpp=True)`，num_tokens只按整个input budget限幅。动态profiling须禁用；另外目标PP1本身也被原生 `ascend_config.py:69–74` 的profiling配置门排除。任何额外外部forced dummy超过history容量，仍必须显式失败，不能借本节的普通profile结论视为已通过。
220: 
221: 这些 host gates 建立了指定原生调度控制流的容量与事件契约。后续仍需实际worker batch重排后的current-only资格、TP4/MTP、设备graph地址、完整current/store精度、峰值内存及短服务验证，才能启用。不得从此结果宣称65,100请求性能或120请求总时长已经改善。

## gpt_new_oscar_kimi/docs/ascendc_design.md
[...]
1: # AscendC 算子 ABI、数值与真实缺口
2: 
3: 已实现七个独立AscendC符号，真实CANN9.1/Ascend910B4编译、链接和官方CPU-debug通过。完整CV与窗口/current路径见 `cv_implementation.md`，旋转融合见 `rotation_pipeline.md`，runtime见 `runtime_implementation.md`。本文件保留基础quant/merge ABI与硬件路线分析；真实NPU数值、图和性能均未通过本轮验收。
4: 
5: ## 档案与 PR 证据
[...]
9: - G2–G13/#87–#90：使用一个普通 C++ launch 声明头，kernel 参数仅 primitive/GM 指针，不跨 host stub 暴露 AscendC 类型、不同步复制 tiling POD。采取 direct launch，所以不产生未注册的 OPP tiling 函数。
10: - #3/#21/#81–#83/#91：目标固定 `ascend910b4`；无 `float↔unsigned` 数值强转；用向量 `Exp/Log`；归约采用 native 四参 `ReduceMax(dst,src,tmp,count)`，min 使用 `ReduceMax(-x)`；所有输出缓冲按最大 D 分配。
11: - G26/G27/#13–#20：精度 gate 不变；K/V 元数据顺序固定；源向量保持 FP32，只对 scale/zero 先 FP16 舍入。旧档案 #111 提到整向量 cast FP16，不能用于本 PR 的逐位兼容实现。
12: - G30–G34/#12：merge 每个输出/LSE行均有写入，全空行写 `0/-inf`，空 split 的 poisoned output 不参与乘法。
13: - #53–#69：不依赖 FIA 的可选 LSE 返回形状，不把空 LSE reshape 成有效结果；没有构造未知的 FIA 调用形态。
14: - #85/#98–#122：构建/安装/加载是分离判据，manifest 不是 `.so`，`.so` 存在不是 NPU执行成功。源码采用单一 direct-launch 接口，不加 OPP 备用路线。
15: 
16: 语义源：`references/oscar-vllm-pr46774/vllm/v1/attention/ops/triton_oscar_store.py` 与 `triton_oscar_decode.py`。每向量一组，`scale_fp16 = fp16(max((max-min)/3,1e-8))`、`zero_fp16=fp16(min)`；编码是 `clamp(int((x-fp32(zero_fp16))/fp32(scale_fp16)+0.5),0,3)`。INT2 为四个符号一字节、低位先行。K/V 分别拥有独立 scale/zero。旋转空间是 `Q@R_k`、`K@R_k`、`V@R_v`，输出最后乘 `R_v.T`。
17: 
18: **PR 零 scale 域问题**：`1e-8` 舍入到 FP16 是 0，常量/极窄向量会触发除零。CPU oracle 和本候选算子都显式拒绝这个未定义转换域，禁止暗中提高 epsilon。算子 status=3，缓存行不发布。这项必须在目标 PR CUDA 与 NPU 的具体转换行为上完成定案，尚不声称覆盖全部输入域。
[...]
51: `torch.ops.oscar_ascend_ops.store_int2_out(key_rot, value_rot, slot_mapping, raw, status, physical_block_tokens, physical_num_blocks, raw_ssm_offset, physical_page_stride) -> ()`
52: 
53: - `key_rot/value_rot`：连续 FP32 `[N,H,D]`，已旋转/裁剪，D∈{64,128,256}。
54: - `slot_mapping`：连续 int32/int64 `[N]`，slot<0 跳过，越界 status=1；调用方必须保证同一次并行 store 的非负 slot 唯一。
55: - `raw`：一维 uint8，原生 GDN SoA raw allocation 的 FULL SSM 区。
[...]
62: 原生 virtual128 子页映射 `v=b*(B/128)+i`，因此 `s=v*128+token_in_virtual` 自然还原 physical 页。SSM剩余空间与conv区不写。禁止追加完整 BF16 history allocation。
63: 
64: **D.4 四问**：相位是 phase1_stores；失败量级209–216ms/16K，原因是重复搬运和小算子堆积；当前 component 在一个 launch 内完成FP32归约/量化、UB位打包与一次准确136B scatter，不产生中间量化HBM张量；复杂度O(NHD)，UB固定<8KiB/core，目标显著低于215ms/16K但无实测。源代码尚用每向量16/32/64字节的有界scalar-UB pack，必须用profiler证实或替换为native vector gather/shift；它不能因写成C++就自动获得“高性能”结论。完整旋转/percentile clip已在rotate_clip_store.cpp融合；此standalone quant component仍可独立验证。
65: 
66: ## Merge ABI 与 D.4 对照
[...]
68: `merge_lse_out(partial_out, partial_lse, output, lse, status) -> ()`
69: 
70: 输入 FP32 `[R,S,D]`、FP32 `[R,S]`；输出 FP32 `[R,D]`、FP32 `[R]`、int32 `[R]`。S∈[1,128]，D同store。输入为已经归一化的各分段输出与自然对数LSE，所有分段必须在同一个V旋转空间。
71: 
72: `m=max(lse_s)`；`w_s=exp(lse_s-m)`；`out=sum(w_s*out_s)/sum(w_s)`；`lse=m+log(sum(w_s))`。空split用 `lse=-inf`；全空行返回0与-inf；NaN/+inf LSE为错误，不能伪装空split。非空partial_out必须有限；该条件由Stage1数值gate保证，Stage1由attention_cv.cpp提供，目标NPU验证仍独立进行。
[...]
76: ## C04 fused INT2 Cube/Vector：实现与硬件边界
77: 
78: 调度单元为(request,kv_head,query_tile,source_kind,history_split)，Mq64、KV tile32。一次压缩tile读取供GQA×MTP各query共用，QK、PV与历史输出逆旋转由真实Cube MatmulImpl执行，INT2 SIMD解包与FP32在线softmax由Vector执行，禁用HF32近似。源码在attention_cv.cpp，设备任务表在attention_tasks.cpp，完整ABI见cv_implementation.md。
79: 
80: A2的Vector→Cube使用每Cube固定 `(256*D+4096)*4` B GM通信（D256为278528B），显式AIV UB预算161024B。容量与历史L无关，没有[L,D]完整历史buffer；总通信流量仍线性，不能把有界tile staging说成零HBM。此差异如实保留。
81: 
82: D.4对应dequant+FIA：旧6500ms全历史dequant被流式解包/矩阵乘替换，不做历史逆旋转；输出逆旋转只对query partial做。目标是接近原生18.7ms相位，但当前只有真实CANN编译与官方CPU-debug证据，没有NPU时延证据。
83: 
84: CPU-debug覆盖GQA6/Q1/2/3/4/17、Hkv2、mixed batch、无序物理页、空历史/分段、非法tag/metadata/NaN，以及MTP后续draft从slot/BT纠正seq_lens。自适应S只依赖捕获shape，在同一arena内分块；S2/S20真实对拍通过，未宣称提速。

## gpt_new_oscar_kimi/docs/c4_complete_partition_budget.md
[...]
50: 
51: - `A/B`：逐核full256历史工作，见JSON完整job清单。
52: - `F`：query读取、两遍metadata/follower扫描、精确window、空current任务、初始state、最终旋转/归一化/写回、启动排空。重分配会改变各核固定任务数，不能假定仍一样。
53: - `T`：每个partial KV单元及M66/M78尾query代价差异。context20000成熟tail为224行；context65100为12行，不能套用已测193行tail比例。
54: - `P`：GPU work-plan创建、压缩、分配及额外metadata/计划读取/同步成本。尚未实现或测量，不能写零。

## gpt_new_oscar_kimi/docs/c4_cross_member_pipeline_budget.md
[...]
1: # C4 跨成员流水预算：只基于闭合循环，不放行截断 trace
2: 
3: 依据：档案 #132–135/#145/#148/#154/#155 与启动文档 D.4；当前源 `attention_cv_window_range_cluster4.cpp`。本轮只做宿主证据分析，没有修改 CANN、数学、dtype、精度门或原生预算。
4: 
5: ## 证据与范围

## gpt_new_oscar_kimi/docs/c4_tail_wave_budget_20261011.md
[...]
9: - query tile 为 `128/6=21` token，C4 bucket 为84 token。source0 的历史终点是 `min(context,max(sink,context+qbegin+qcount−recent))`。C4要求四成员全部21 token、同request/head/split/context/KV范围，且 `kvend=context`；因此第一个成熟 anchor 是252，不能把前3个 bucket 当成熟簇。
10: - 记 `G=ceil(Q/21)`、`B=floor(Q/84)`，在上述限定下成熟簇数为 `max(0,B−3)`；第一遍 source0 为12个前沿 C1，加末尾不足完整 bucket 的 query组。source0 C1组 g 的 owner 为 `g mod20`；source1组 g 为 `(G+g) mod20`；成熟簇 bucket b 为 `b mod20`。
11: - source1每组仍必须执行，候选 KV 数为 `64+max(0,255−21g)`，按256划分搬运单元；不能把它与空 current、followers、尾部、最终旋转等第一遍工作丢掉。source2是否压空必须按实际服务路由确认，本计数沿用已有报告的压空条件。
12: 
13: | 已完成计数的形状 | source0 query组 | 成熟C4簇 | 第一遍C1组 | source1账 | 当前热点及拆分边界 |
[...]
21: ## 准备组合基底上的参数式
22: 
23: 必须重新取得 **H32 + member-pipeline** 的成本。设同一历史范围内一个完整 C1 历史工作为 `A`，一个四成员 pipeline 簇为 `B`；它们包含实际KV循环与其同步，保留部分KV/部分query的单独成本。设 `F_i` 为第一遍source1、metadata/followers、空current、query/state初始化、末尾旋转/写回等不属于A/B的每核成本。拆分增加的 planner、元数据和固定成本记入 `P_i` 或 `F'_i`。
24: 
25: 通用式是 `T_old=max_i(H_i+F_i)`、`T_new=max_i(H'_i+F'_i+P_i)`，不能先把旧owners理想均衡。Q2048的一种已推导任务安排是：从core3移去anchor1932的C4，将其四个原始C1 leader分别交给原无第一遍C1的cores12–15。第一遍source1及所有其他task保持原owner；移走/新增query、旋转等固定工作仍须计入 `F'_i`。
26: 
27: 仅在统一固定成本F、所有C1不重于A、迁移后其他核不形成更大热点的理想模型中，才有：

## gpt_new_oscar_kimi/docs/c4_wide_matmul_feasibility_20261011.md
[...]
11: **条件预算首先要补回丢失的重叠。** [旧闭合循环预算](../reports/c4_phase_profile_q336_20261009/partial_c4_pipeline_budget.json) 的同一完整256-KV轮中，四次QK/PV合计192432 ticks，较慢AIV逐成员soft合计99966。按“四段QK完成→四段soft完成→宽PV”的新依赖，沿用这些服务成本、甚至忽略旗标和新增成本，需292398 ticks；原成员交错模型为220248。矩阵部分须先省 **72150 ticks，即37.5%** 才持平；尾轮同口径门槛约49.9%。这是**旧闭合片段的条件DAG门槛，不是当前C337实测预测或硬件下界**，不能与当前完整核1849738→1610282的已测收益重复计账，也不能把 wait 全当可删除。
12: 
13: **重开条件：** 先取得 M512 的实际 B 缓存/搬入证据，并让包含填零、状态通信、完整同步和丢失重叠的预算显示明显净贡献，再考虑单独研究；随后必须与当前 pipeline 完整配对。若只剩1–5%的增量或仅证明A/B加载次数下降，继续暂缓。#148要求保护数学与模型精度边界；D.4对应融合FIA内有界数据流，旧全历史dequant为6499.8–6655.1ms，本方向只能用固定tile共享规避重复，禁止全历史恢复；现阶段没有完整算子净提速上界或整轮达标承诺。
14: 
15: 源码绑定：`c4_candidate.cpp` SHA256 `da59a923a44cdb7ac0916596cd89f802a24fc1ffef4426952402d90b5d2e7b31`；SDK来源与哈希见 `artifacts/cann_sdk_matmul_move_20261010/provenance.json`。

## gpt_new_oscar_kimi/docs/checklist.md
[...]
16: | [x] A04 | passed | 读懂第 3.3 节调用链，记录 FULL/GDN、TP、KV 分组、MTP 和图模式的真实入口。 | docs/runtime_implementation.md；tests/test_runtime_native.py执行真实native分组、manager、reshape、MTP/图builder方法；目标worker执行另列D08。 |
17: | [ ] A05 | in_progress | 核实第 4 节全部歧义，给出层/组/Tensor/地址映射与字节来源。 | 动态C/M/P与B2304公式、真实native config/形状函数已验证；MTP3示例C30720/P817152；#127补齐prefix关闭的none模式，Bfull2816、GDN请求块262144，真实页初始化复验待回传。 |
18: | [x] A06 | passed | 读取 PR 的配置、旋转、量化和精度验证方法，完善本 Checklist，列出仍缺失的输入。 | docs/semantics.md；ops/reference.py、rotations.py与独立PR语义测试。 |
19: | [ ] A07 | in_progress | 任务开始时已把 `issue1_full_record.md`（含第三部分 [74]~[86]）完整读一遍并掌握其查表用法（症状速查表 → 条目跳转），并将其中与当前任务相关的故障模式登记进第 8.2 节回归检查；确认不会参考任何失败 OSCAR 实现的代码（第 0.2 节红线）。 | 已阅读启动文档全约束、D.4全文、档案速查/总索引与相关条目；子代理分别查读各子系统。未把26,251行档案逐字通读签成完成。 |
20: | [ ] B01 | in_progress | 产出 `docs/design.md`，列出外部新增文件/函数/类及其包装的原生入口。**结构必须符合第 5.0 节**：全局端到端架构（生命周期图/联动矩阵/时间线/两本账）先行，逐点展开固定六问，自审清单逐项打勾；碎片化设计视为 B 阶段未完成。 | 全局设计/矩阵/时间线/两本账/差异与D.4四问齐全；四条性质中的真实性能与H18仍未过。 |
21: | [ ] B02 | in_progress | 完成请求窗口、物理页、GDN 隔离、TP 分片、页生命周期和 MTP 提交/回滚设计。 | canonical物理页snapshot、MTP slot-derived位置、prefix/回滚方案已实现；真实native方法与CANN CPU-debug通过，NPU生命周期未运行。 |
22: | [ ] B03 | in_progress | 给出所有 payload、元数据、padding、workspace 和总 HBM 公式，证明压缩收益可落地。 | 真实native allocator/grouping/LCM/hash/manager与动态字节账已验证；实际NPU容量收益仍未测。 |
23: | [x] B04 | passed | 完成算子清单、AscendC 融合划分、Decode Stage1 伪代码和逐阶段读写流程。 | 七个AscendC符号完整源码、ABI、Cube/Vector/同步/UB与GM预算；docs/operator_inventory.md、cv_implementation.md、rotation_pipeline.md。 |
24: | [ ] B05 | blocked | 给出 decode 计算量、HBM 流量、MTP 跨 query 复用和 Host 调度预算。 | H18总历史读取亚线性与精确dense attention存在数学冲突，已提出澄清。 |
25: | [ ] B06 | in_progress | 固定功能、精度、性能测试方法和验收门槛，设计一键脚本及错误清理流程。 | PR容差未改，部署/故障处理/测量与profiler工具已实现；模型级质量门槛仍待实测前定义。 |
26: | [ ] C01 | in_progress | 独立插件/算子工程可安装、可编译、可加载，原生源码未修改，安装脚本不使用 `cp`。 | Python包及CANN9.1/910B4交叉编译/链接通过；独立direct-launch库采用源签名SONAME，非custom OPP vendor。node93后续构建及75项store/merge原语NPU执行通过，确认已越过#125加载故障；后续已完成TP4/MTP编译及KV预算，后续已通过短请求，长请求无进展（#129）。 |
27: | [ ] C02 | in_progress | 版本能力 probe、延迟注册和幂等 Hook 通过 CLI、API server、各 worker 初始化验证。 | 轻量可撤销hook、factory、binding、真实native类/方法契约通过；实际TP4 worker已走到缓存分配后的MTP metadata初始化；#128修复显式虚拟块副本，后续启动待真机确认。 |
28: | [ ] C03 | in_progress | 实现并验证 INT2 编码、旋转/裁剪/量化、KV store 与 Recent→History 增量迁移。 | AscendC rotate/clip/quant/pack/raw snapshot已实现，官方CPU-debug通过；node93的store原语及非法值/边界NPU用例通过，融合旋转/裁剪路径仍未验收。 |
29: | [ ] C04 | in_progress | 实现真实 fused INT2 CV Decode Stage1（CV=Cube/Vector，见 H07 注），并完成必要的分块/分段输出合并。 | 真正Cube QK/PV/逆旋转与Vector SIMD解包/softmax已编译、CPU-debug通过；node93首个CV用例D64/Q1/context17输出超差（#126）。已定位并修订query有效行→padding的MTE3→V同步缺口，目标复验/性能未完成，H18冲突保留。 |
30: | [ ] C05 | in_progress | Sink/Recent Attention、History Attention 和参考数学语义一致，数值稳定。 | 三source causal/GQA与稳定LSE真实CPU-debug通过；node93 merge原语NPU用例通过，但CV首用例输出超差，其LSE断言尚未到达（#126）；完整数值验收未通过。 |
31: | [ ] C06 | in_progress | 实现原生页表兼容的物理分配与视图，GDN 不受影响，HBM 中无冗余完整历史副本。 | 真实native grouping、BlockPool、Full/Mamba managers与GDN reshape执行通过；production raw分配与view已接通；#127修正none模式容量，保留GDN原对象、分组、原生状态数；最新真机已通过KV容量计算并进入分配后MTP初始化；#128元数据副本修复后需继续复验。 |
[...]
38: | [ ] D06 | in_progress | 混合长度和 prefill/decode/verify 混合调度正确，不依赖逐请求 Python 热循环。 | 设备批量metadata、mixed Q1/Q4、多KVhead、padding孔洞与17query跨tile CPU-debug通过；真实异步混合调度未跑。 |
39: | [ ] D07 | in_progress | 16K、32K、50K 长输入实际使用 OSCAR，跨页与跨窗口边界均正确。 | node93串行16K/32K/50K请求已HTTP完成（档案#130）；混合并发曾撞300s死线（#131），完整跨页/窗口数值对拍未验收。 |
40: | [ ] D08 | in_progress | TP=4、异步调度、目标图模式和 W8A8 权重量化共存，所有 rank 路由正确。 | TP4/MTP服务和图回放日志已出现（档案#129/#135/#138）；需保留图捕获返回、逐rank路由、真实回放及精度各自证据，不能以HTTP 200代替整项通过。 |
41: | [ ] D09 | in_progress | 前缀缓存、页共享/复用、请求取消/结束、抢占恢复等目标环境可达生命周期通过验证。 | 真实native block manager与canonical snapshot/回收代数已验证；全服务prefix/取消/抢占待NPU。 |
42: | [ ] E01 | in_progress | 核心算子对齐参考；覆盖 pack/unpack、量化边界、尾块和 attention 数值误差。 | CANN交叉编译、官方CPU-debug和CPU oracle通过；node93逻辑npu:0通过75项原语NPU探针（54store/21merge），随后首个CV数值用例失败；probe-cv的3项通过仅为Python/源码契约测试，其余CV/旋转用例因maxfail=1未由该日志证明完成。 |
43: | [ ] E02 | not_run | GDN 隔离检查通过；FULL 量化后的层输出、模型输出与约定质量指标达标。 | 真实目标环境尚未运行；所需生产核心或验证仍未完成。 |
44: | [ ] E03 | not_run | MTP 接受率、接受长度、输出正确性和有效生成吞吐完成对照。 | 真实目标环境尚未运行；所需生产核心或验证仍未完成。 |
[...]
48: | [ ] E07 | in_progress | 对照第 8.2 节验证历史故障防护，保存实际覆盖结果而非仅声明"已避免"。 | 历史故障约束已落实；本轮VM发现Log alias与Matmul Init重载问题并修复；CANN plog本任务PID诊断与失败保码通过本地测试。node93回传已登记#123–#126；后续75项原语NPU执行通过确认加载错误已越过，首个CV数值用例暴露query缓冲同步缺口；源码修订后的CV真机复验待回传。 |
49: | [ ] E08 | in_progress | **无回退逻辑验证**：静态审查 + 全量工况扫描证明代码中不存在任何回退/降级路径；16K/32K/50K 与各种 batch size 下 OSCAR 压缩路径全部实际命中（H13/H17），不存在静默走原生 BF16 全历史的分支。 | 静态/路由/错误注入通过；长序列真实压缩路径命中仍需目标probe。 |
50: | [ ] F01 | in_progress | 一条 Bash 命令完成安装、编译、所需校准、probe、资源清理和正式启动。 | 一键安装/编译/NPU算子与CV/旋转对拍/自动旋转文件/TP4服务probe/清理/正式服务；默认0–3卡和8989端口，实时输出并落盘。#138确认探针→清理→正式服务首度走通；后续性能实测严重退化，不能据流程完成宣称性能或精度通过。 |
51: | [ ] F02 | in_progress | 验证正常退出、失败退出和中断后的清理，重复执行不会遗留 worker 或加载旧产物。 | 真实CPU子进程/HTTP/超时/信号/释放失败与诊断故障注入通过；NPU资源回收尚无实证。 |
52: | [ ] F03 | in_progress | 正式服务按目标配置启动并完成真实请求，记录 OSCAR compressed decode/MTP 路由证据。 | #138一键流程已进入正式serve；用户随后通过service_direct.sh对OSCAR服务发出请求并获HTTP 200（#137），但正式服务的完整路由、质量与负载性能证据尚未验收。 |
53: | [ ] F04 | in_progress | 交付代码、设计、完整 Checklist、测试/性能/显存报告、日志及 README 中的一键命令。 | 源码、设计、VM日志/报告、README和测量工具已交付；真实模型精度/性能/容量报告尚缺。 |
54: | [x] F05 | passed | 检查所有硬约束和未完成项，最终结论准确列出已验证范围、失败项及阻塞项。 | 本表和reports/local_validation.json严格区分源码、编译、CPU-debug、NPU/图/性能；未测项保留未通过。 |
55: 
[...]
60: 2026-09-29（#152）：64K/120×512同任务，OSCAR3331.55s vs native1371.97s，E06失败；不重跑AISBench。新mixed四组设备oracle通过并确认N16384/S1 q4与带历史prefill CV开销。候选增加独立balanced/C16，保留fe0与已测fast/C4/q1算子；固定`install_serve.sh --variant candidate`自动启用新路由，新真实NPU AB/图/错误传播门接`--probe-only --diagnose-mixed`。本地证据与新NPU待验状态见`docs/mixed_cv_optimization.md`，不因源码/编译/CPU成功标E06通过。
61: 
62: 2026-09-28最新用户报告约16min，原生约8min；E06仍未通过。新片段中相同Running25/Waiting7时OSCAR生成17.2 tok/s、原生125.3 tok/s，而OSCAR prompt吞吐归零的三个窗口生成均值296.6 tok/s。线索集中于混合长prefill期间的推进速度，不能把峰值当作整程收益或把共用eager规则当作唯一根因。源码和计数口径见`docs/mixed_prefill_analysis.md`。新增可选`--probe-only --diagnose-mixed`只测实际candidate CV/current FIA/merge组合；NPU数据待回传，不新增算子精度或性能通过结论，直启candidate继续使用已交付优化。
63: 
64: 0677bcb fast unpack真机门已通过：五个热形状耗时降低11.34%–28.96%，精度/指定独立图/性能门passed，详见`reports/target_fast_unpack_pass_20260928.txt`。E06完整服务8分钟目标仍未验收。固定交付入口为`install_serve.sh --variant candidate`，已与probe共用候选预设并通过68项相关主机回归；每轮须同步实际路由，不能仅更新probe。默认与后四卡行为不改。
65: 
66: 最新用户反馈candidate约19min vs原生8min，E06仍未通过。本轮已实现三种独立fast unpack CV（q4/q1/C4），原FE0/C4/q1/profile文件字节未改；CANN及官方CPU-debug22/22通过，含65536×8整数码和21项整CV/特殊half/错误用例。目标NPU精度、图及5个热形状收益由新增fast-unpack门裁决，不能用本地通过宣称8分钟完成。源指纹`reports/fast_unpack_local_validation.json`，分析`docs/fast_unpack.md`；不再要求AISBench。
67: 
68: 用户指定的直启部署模式：`install_serve.sh --variant candidate --rear-cards`仅本轮使用物理卡4,5,6,7和端口7878，安装/编译/旋转准备/服务共享有效配置。原target.json及不带rear-cards时的行为不变；11项主机编排测试通过，不记为新真机验收或错误条目。
69: 
70: #151：928edb3真机q4原生与OSCAR oracle/profile比较已完成，native1.4509ms、CV+merge15.4011ms；关键历史AIV解包占其task span64.71%，AIC KV等待81.25%。最终报告被run_phase同名状态JSON覆盖导致父门失败；现分离`q4-hotpath-report.json`并以真实子进程回归（13 passed），不放宽证据门、不要求重跑。保留终端关键向量，完整被覆盖报告不可恢复，不能称已保存全部profile。E06仍未通过；下一优化依据见`reports/q4_hotpath_findings_20260928.json`。
71: 
72: 直启入口配置补齐（#148/#150，主机变更不记新真机错误）：`install_serve.sh --variant candidate`现在向安装/编译/旋转准备和正式服务统一传入启用C4/q1的本轮配置，并打印SERVE_MODE；不修改原target.json，不运行探针。省略variant遵循输入配置，baseline显式选fe0，q4内部profile不进入生产。6项主机编排测试通过；未以此新增设备或端到端验收结论。
73: 
74: 2026-09-28 q1真机复验：a13af95、`observe-20260928T031553.257802Z`全部短probe门通过；q1 N128/S3 45.112→13.807ms（独立图/逐位passed），N16384/S1 137.883→20.544ms（逐位passed、该形状graph未跑）。C4继续通过，q4 S3原fe0仍约15.3ms。新q1设备精度/指定独立图/局部收益分别有证据；完整TP4服务和E06的8分钟目标仍未完成。原文见`reports/target_q1_schedule_pass_20260928.txt`，不重跑AISBench。
75: 
76: q4诊断接入同一`--probe-only`：原生paged BF16 FIA与OSCAR CV+merge的未插桩Event对照、独立profile的每核/每引擎/每来源计数，分别验证oracle及fe0逐位。profile不进入生产，fe0/C4/q1三内核字节不变。CANN编译和CPU-debug2/2通过；新native API与profile真NPU仍待测，E06不因诊断工具通过而解锁。见`docs/q4_diagnostic.md`、`reports/q4_profile_local_validation.json`。
[...]
83: 
84: 1. H18复杂度口径；精确attention需要读取全部压缩历史。
85: 2. 已实现的CV/rotation/clip在目标NPU上的精度、图、性能验证。
86: 3. 已实现的prefix、GDN隔离、MTP和固定buffer在真实完整模型上验收。
87: 4. 本次配置已按附录 A/F 固定0–3卡、8989端口和ascend910b4；最新node93复跑进入service-probe并加载TP4/MTP模型；#127已被后续运行越过；#128的MTP虚拟块视图修复后需重新验证服务启动。
88: 5. 模型质量门槛在实测前冻结；paired基线、NPU精度/图/资源/性能逐项过门。
89: 
90: 本地构建/测试结果与失败细节见 `reports/local_validation.json`、`reports/pytest.xml`、`reports/build.json`、`reports/readiness.json`。档案#123–#126记录用户回传的node93真实故障与源码修订；#125加载故障已由后续75项原语NPU成功执行越过。最新原文保存在`reports/target_cv_failure_input.txt`，其中首个CV数值用例失败，完整模型、图和性能仍未验收。
[...]
116: #139：并发阶梯诊断快路径`scripts/probe_concurrency.sh`（--ladder模式，跳过安装/编译/功能相位）；心跳1秒间隔下用`summarize_progress`从心跳差重建每层驻留wall（臂窗口×reqs×KV分桶，跨臂空档单列）。一条命令出齐调度/算子/访存三层证据，诊断不冒充验收。
117: 
118: 2026-09-23复核（档案#130–#139；分析见`docs/performance_findings_2026-09-23.md`）：#137中“差异链闭合于CV、排除调度/MTP/GDN”和#139中“心跳差为每层算子/访存成本”的表述超出所贴生产日志。#134/#135的独立debug-sync运行确实把主要同步时间归于FIA，但与本轮生产负载不是同一计时；本轮16K阶梯K1=19.0秒、K4=76.5秒，每条请求恰好占满16384-token调度预算，约4倍墙钟不足以单独证明算子串行。`PROGRESS_BUCKET wall_s`是四rank宿主心跳间隔之和，含其他工作，不是设备算子时间或HBM访存量。用户32并发服务片段缺逐请求usage/TTFT、当前版本配对原生证据和模型级精度门；E06仍为failed，E02/E03未验收。此处为旧条目解释边界的更正，不追加新的真机错误编号。
119: 
120: 本轮探针改版（防档案#94/#95/#129/#131/#136/#138/#139）：`tools/service_probe.py`在正式一键功能门后发4条20/23/27/30K不等长的synthetic streaming请求，严格记录TTFT/TPOT、终态usage、metrics及失败；任一诊断请求或指标缺失即阻断正式serve。正式serve中的`benchmarks/passive.py`只观察用户原客户端负载；`tools/summarize_progress.py`明确区分四rank心跳累计与设备算子时间。独立`tools/probe_native_current_fia.py`仅为真机可行性实验，不进入生产路由。此轮本地全仓pytest 466 passed、124 skipped、6 subtests passed；未运行新一轮目标NPU，未修改AscendC、`references/`或冻结精度阈值，E06仍不通过。
121: 
122: 一键配对改版（用户要求一次启动、少量可复制日志；档案#70–73/#94/#95/#125/#131–139）：`scripts/install_probe_serve.sh`自动在同一次调用中先跑原生4路20/23/27/30K synthetic、确认进程和NPU释放，再跑OSCAR完整服务探针及相同4路synthetic；性能诊断每路输出64token，功能探针仍16token，300秒死线不变。`tools/paired_concurrency_probe.py`按冻结延迟/吞吐比值逐请求比较，任一失败或证据不足阻断正式serve；单批次、预热不完全配对，因此结果不解锁E06。终端默认compact，仅少量阶段/资源状态、失败和至多8条配对`PERF_*`摘要，完整日志/真实退出码落盘。`scripts/probe_concurrency.sh`作为省去完整安装/功能门的单命令快路径，自动核实签名复用或重建AscendC，新构建须先过真实NPU CV/旋转数值门和资源释放，之后顺序跑原生与OSCAR、每轮确认资源释放。正式一键流程强制本轮新鲜NPU数值探针一次，避免与快路径缓存证据混同。旧16K/16-token性能阶梯已移除；原有16-token功能门仍保留。此轮仍未在目标NPU运行，速度是否追平原生保持未验收。
123: 
124: #140 真机配对结果：同一脚本对20/23/27/30K、K4、64输出token分别跑原生/OSCAR，两边4/4完成且清理及NPU释放通过；原生14.7s、OSCAR182.5s，TTFT p50慢11.53倍，TPOT p50慢14.68倍，客户端性能门按冻结1.0阈值`rc=2`失败。E06从“未验收”进一步有了当前同轮**失败实证**，不能因服务和精度探针完成而启动性能通过结论。HCCL INFO、捕图期间STARTUP_WAIT及TBE关停EOF都不是这次真正失败点。原文及归因边界见档案#140和`docs/performance_findings_2026-09-23.md`；后续内核改动前仍需本轮设备相位/来源归因。
125: 
126: #140后的局部性能修订：CV在短query时只处理有效softmax行，并把四个32-token KV子块合成一次128-token有界工作单元，减少重复Cube调用与跨核握手；没有全历史物化、原生路径回退或精度阈值变更。`reports/kv128_local_validation.json`记录CANN ascend910b4编译及官方CPU-debug 27/27通过、源码指纹；**目标NPU精度、FULL_DECODE_ONLY图捕获/回放和20–30K/K4性能尚未运行**。快路径现先核实当前签名，必要时重建并跑真NPU CV/旋转数值门，避免用旧`.so`误报新内核速度；正式一键流程强制每轮新鲜数值门。E06继续保持失败/待复验，不能从静态约4倍tile轮次减少推导已经追平原生。
127: 
128: #141：用户新实测OSCAR K4墙钟约131.7s（前轮182.5s），有收益但仍比原生慢约9倍，E06未通过。本轮进一步改FP32 Cube basic64×64×128、解析mask、Brcb scale/zero、整块FP32 SoftmaxFlashV2及批量alpha；主模型eager prefill current改用原生causal FIA，与实际CV history/window合并，draft/graph decode仍CV。最终同一内核通过CANN ascend910b4编译和27/27官方CPU-debug；主机517 passed、127 skipped、6 subtests。源码哈希与证据在`reports/deep_attention_local_validation.json`和`reports/deep_attention_cv_cpu_debug.json`。一键脚本自动新增实际current/CV/merge的真NPU门，失败不拉模型。**本轮目标NPU精度、图、服务和追平原生的结果仍待实测**，不以SDK指令数量或本地对拍解锁性能。
129: 
130: #142：用户回传OSCAR捕图0/34时507035/vector trap。原生非capture的MTP dummy warmup标为ChunkedPrefill且slot全-1，新增current路由误启用真实slot guard；用外部`_dummy_run` ContextVar显式区分dummy，完整CV padding仍执行。49项相关主机回归通过（含原生预热编排与真实prefill恢复），AscendC及冻结配置未变。**修订后目标捕图/服务/性能仍待复验**；故障原文见`reports/target_graph_warmup_failure.txt`。
[...]
132: #143：用户回传真NPU数值门及current/CV/merge门通过，原生与OSCAR各4/4完成并释放；OSCAR墙钟从约131.7s降至43.3s，原生14.7s，E06仍未通过。保留实测有效计算路径。快路径增加同服务、仅退化时自动运行的独立K4 NPU事件诊断轮；正常速度比仍来自原始无事件轮。细分prefill/draft/整图回放及TP rank，捕图和dummy不插事件，缺失设备证据拒绝完整结论。新计时仅主机契约验证，**目标设备归因与追平仍待回传**。原文`reports/target_k4_43s_performance.txt`。
133: 
134: #144：目标诊断已将主要开销定位到带历史prefill CV（23.535s），空历史候选16层只106ms。用户自有127请求/32并发约31min对8min仅用作已提供的对照，禁止重跑。本轮M128×KV256、自然V连续写、位平面屏障合并及有效P行写回已完成；FP32累积仍在UB。CANN编译及33/33官方CPU-debug通过，含3个全NaN工作区案例。新旧同输入CV算子A/B加入重编前/后流程，数值/资源/速度退化阻断模型启动；仍保留原生K4门。**候选真NPU精度、图及达到原生速度尚待实测**。证据见`reports/history_cv_local_validation.json`，目标原文见`reports/target_history_cv_hotspot.txt`。
135: 
136: #145：cf97bb1真NPU CV门在D64/Q6/context511出现1024/2304 NaN，候选尚未进入模型性能比较。当前源码确认两个32行score块之间缺MTE3→MTE2所有权依赖；只替换这道事件方向，保留数学与冻结容差。重复NaN工作区回归覆盖36/66/102行。相关主机回归24 passed、28 NPU skipped；目标CV数值、图、性能必须由完整`git pull --ff-only && bash scripts/probe_concurrency.sh`重新验收，不能以CPU-debug通过解锁。C04/C05/E01仍未完成，E06仍失败/待复验。
[...]
138: #145本机复验：CANN ascend910b4编译通过，官方CPU-debug38/38；证据`reports/cv_score_handoff_validation.json`。该模拟也能通过修复前的同形Q6，故真机数值与完整K4速度结论仍由下一轮一键日志确认。
139: 
140: #148：用户确认fe0精度正确（自有LongBenchv2为53.54%、22:22）；后续34639ab为48.03%、20:15，已按用户要求回到fe0，不保留这些后续数学改动。新C4算子只复用四组完全同域历史的解包，fe0原生产kernel逐字节不变、默认仍fe0。CANN ascend910b4编译和官方CPU-debug51/51通过；相关主机95 passed、28 NPU skipped、4 subtests passed。证据`reports/history_reuse_cpu_validation.json`及`reports/target_longbench_regression.txt`。两个过重CPU模拟器配置超时记录保留，不写成NPU错误。新入口`install_observe_serve.sh --variant candidate`先过同输入逐位/冻结oracle/图/速度门再启动候选；被动观察用户负载，不自动重跑127题。C04/C05/E01的新候选NPU/图仍待测，E06追平原生仍未通过；用户已认可的fe0精度不因本候选未测而撤销。42个稳定checkpoint编号不变。设计、计时口径与一键命令见`docs/history_reuse_experiment.md`。
141: 
142: 
[...]
151: 2026-10-07持续迭代（非新增真机条目）：当前SIMD decode的显式指令标记确认部分KV块存在明显mask开销；同一q4历史任务三个Softmax区间为7178/5537/85416周期。CAModel的SYS_CNT恒零已识别，不用于相位归因；完整标记及嵌套时间核算见`reports/decode_marker_v2_camodel_20261007/`。组合保持FP32/KV256历史顺序，包含历史流水重叠、临时INT16行布局、窗口批量读取、精确区间mask和precise源补零工作裁剪。20项CPU整算子用例逐位/冻结oracle通过；另有当前striped base/balanced/C4/C16四条路径的完整CPU A/B通过。完整单请求20K周期2464632→1488538，完整四请求20/23/27/30K、N128/S3/20核周期3327234→2065063（1.6112倍），均保留全部source/task且输出逐位一致。它们不是32请求、NPU或整轮模型速度结论。
152: 
153: 实际部署CANN库与Torch扩展已通过完整编译链接，六个新设备入口已用符号表核实；来源签名和日志见`reports/decode_integrated_build_20261007/`。新增q4/q1图门、first-MTP current门和混合请求分流整forward门，检查真实设备完成、冻结精度、缓存字节、后续q1、完整case及产物签名，失败阻断服务。两条一键入口已共同提供有效特性/预算摘要，显式全组合配置的计划接线已验证；自动candidate推广仍待整体收益论证。原生GDN与参考树未修改，精度门未放宽，42个checkpoint编号不变；E06仍未通过。32请求完整模拟正在继续，状态与下一步见`reports/decode_progress_20261007.json`。
154: 
155: 2026-10-07用户要求本轮收口推送：完整K32 q4的部署库CAModel对照已通过，16,290,667→9,589,788周期（1.69875×），partial/LSE/status逐位、冻结oracle通过。用户随后明确停止扩大测速，采用当前方案进入真机认证。两个candidate一键入口现共同默认启用decode bundle、current-only、first-MTP current、later-MTP compact、mixed decode partition和whole-prefill；未验收的weighted-owner试验不纳入。216项关键本地主机回归通过；C04/C05/E01新真NPU/图与E06整轮8分钟仍待认证，不因用户授权推送而改为通过。交付说明见`docs/decode_candidate_20261007.md`。

## gpt_new_oscar_kimi/docs/compact_pool_64k_design.md
[...]
128: ```
129: 
130: 若ring在profiling前已经分配，budget中不再扣第二次；若在planner之后分配，就必须在以上预算中显式扣除。workspace/rotations按同一原则。NF包含FULL null block，三个GDN池各有自己的null，不再按旧全局池只计一次null。
131: 
132: R不能默默设为“Running26”或客户端32。可在显式compact容量政策下用本轮65100+512+3密度选出使 `min(R, floor((NF−1)/513))` 最大的R，同时不超过原配置max_num_seqs；还必须保证至少一个max_model_len262144请求可由NF容纳。R是状态池物理容量，max_num_seqs仍为原128的调度上限；池不足时等待，不修改请求长度或MTP语义。若政策要求保障128个短请求同时驻留，就必须真实支付128份GDN与ring成本，不能只按32份计账。
[...]
139: 2. **证明GDN原生等价**：tight raw经原生reshape得到相同dtype/shape/stride语义；MTP4状态索引、初态、accepted回滚、preempt/resume重算保持原生行为。这里不改GDN内核。
140: 3. **实现新ring ABI与全部路由**：固定generation所有权，q4/q1/C4/C16/first/later MTP/current-only全覆盖，长chunk只写唯一保留槽，失效tag fail-closed。有任一路由仍期待旧page snapshot则不允许启用compact。
141: 4. **短时真NPU验收**：仅用合成算子/图/短服务probe，验证所有权、非法输入、跨页、拒绝深度0–3、请求重排/复用、同址图变输入和真实分配字节；冻结oracle与精度不变。无需重跑已完成AISBench。
142: 5. **交付开关**：新能力通过前不进默认candidate；通过后由`tools/serving_variants.py`唯一开关同时驱动两个candidate入口。显式compact与prefix/align冲突则失败，旧合法模式仍使用其显式原配置，不运行期暗切。
143: 

## gpt_new_oscar_kimi/docs/current_dequant_unpack32_audit.md
[...]
1: # 当前反量化审计与 HalfKv32 候选
2: 
3: 2026-10-10；档案 #13–22/#70–73/#126/#144–145/#148/#151/#154–156，启动文档0.7与D.4。这里只分析当前本工程生产源与同源CAModel证据，没有读取失败工程代码、恢复全历史、降低精度或跳过非法metadata。
4: 
5: ## 当前确实存在的差异

## gpt_new_oscar_kimi/docs/cv_implementation.md
[...]
3: `attention_cv.cpp`、`attention_tasks.cpp` 和独立 torch registration使用 Ascend A2 `MIX_AIC_1_2`：一个 Cube 配两个 Vector。当前#144为M128×KV256；QK、PV、历史输出的 `Rv.T` 均由 `matmul::MatmulImpl` 执行；向量核处理 INT2 解包、精确 BF16 搬入、因果 mask、稳定 softmax 与分块累计。没有标量 dot 或调用 Python oracle 的生产路线。本文后半保留历史迭代记录，旧资源数字以各条目当时版本为限。
4: 
5: 源码、真实 CANN 编译、官方 CPU-debug、设备执行、图捕获、图重放、精度与性能是独立状态。此文件的资源/流量数字是源码推导，不能视为实测性能。
6: 
7: ## 档案、PR 与 SDK 对照
[...]
12: |---|---|
13: | G3–G13、#3/#21/#81–83/#87–92 | 原生 API + CANN 9.1 SDK 核实；单个 primitive-only launch 声明；`ascend910b4`；静态资源边界；不做 float/unsigned 数值强转 |
14: | G26–G34、#13–20 | PR136B(D256) slot；metadata 原样 FP16→FP32；解包是 4-per-byte LSB-first，SIMD bit-plane→自然顺序；没有重新量化或整向量 BF16 降精度 |
15: | G30–G34、#12 | padding/empty/source split 也必须写 output 与 `-inf` LSE；初始输出 poison 不可能当有效值复用 |
16: | #34/#36 | graph 固定 N/R/task/workspace 容量；qstarts、seq_lens、slot_mapping 每次从设备读取；Cube scalar metadata 在入口清 DCache，Vector 使用 DMA |
[...]
20: | #98–122 | direct-launch 单路径；不复制原生文件，不替换 OPP 环境，不把 config/符号存在当执行通过 |
21: 
22: 只读原生先例：`references/vllm-ascend/csrc/moe/hc_pre/op_kernel/hc_pre_m_k_split_core.h` 的 mode-2 CV flag 与固定 GM 通信；`hc_pre_cube_compute.h` 的 FP32 Cube 数据通路；`moe_grouped_matmul.h` 的 MatmulImpl；`add_rms_norm_bias_multi_n.h` 的 Gather。指定 PR：`triton_oscar_decode.py` 的 INT2 解包、FP32 score/PV 与自然对数 LSE；`oscar_attn.py` 的 window BF16 与历史输出逆旋转后合并。
23: 
24: CANN VM 中只读核实了 9.1 SDK 的 `matmul/constant_tiling.h`、`MatmulImplBase::SetSingleShape`、`SetHF32`、Gather/ShiftRight/cache 接口。`SetSingleShape` 调用 SetTail；normal config 的 `enableSetTail=true` 允许同一已初始化 matmul 使用 QK / PV / rotation 的实际形状。FP32 Cube 明确 `SetHF32Mode(false)`，不把 HF32 精度冒充 FP32。仍必须执行冻结容差数值门。
25: 
26: ## 可执行 ABI
[...]
35: - q_count=0 为同querytile的非leader task；q_count=-1 为padding/非法metadata，输出行由该token自己的task初始化。带负slot的请求不因dummy seq_len=0触发有效请求错误；querytile遇内部负slot截断，后续valid run单独成为leader，避免两个task覆盖同一输出行。
36: 
37: `attention_cv_out(query, query_rot, current_key, current_value, rotation_v, raw, block_table, window_key, window_value, window_tags, tasks, partial, lse, status, workspace, block_tokens, physical_blocks, raw_ssm_offset, physical_page_stride, sink_tokens, recent_tokens, speculative_tokens, splits, scale, cube_cores)`：
38: 
39: - query BF16 `[N,Hq,D]`、query_rot FP32同形；current K/V BF16 `[N,Hkv,D]`；Rv FP32 `[D,D]`。D64/128/256。
[...]
43: - workspace uint8 flat，至少 `cube_cores*(768*D+32768)*4` bytes；cube_cores∈[1,32]。同stream不做动态分配、主机值拷贝或同步。
44: 
45: 所有partial均为原始 V 空间。source0在整段online-softmax完成后，只对64query行的结果作Cube `@Rv.T`；不对历史K/V逆旋转。随后可把partial展平为 `[N*Hq,3*splits,D]`，交给已有 `merge_lse_out`。
46: 
47: **#144当前资源与收益边界**：以上逆旋转当前最多处理128个query/head行。每个256KV工作单元由8个32KV子块组成，K/V均为自然`[256,D]`；QK使用B转置，PV使用B不转置，V不再经Vector Gather与D个64B分散写。每AIV的64行FP32累积状态常驻UB，score按两个32行块处理，PV分16行读回；P只写实际M行。D256每Cube固定GM917504B、显式UB157184B/AIV。CANN编译及33/33官方CPU-debug通过，包括3例NaN workspace；真实净收益以新旧同输入NPU算子A/B及K4为准，不能由复用次数推导。以下128KV/64行描述属于#140及之前历史迭代。
48: 
49: ## 因果窗口与 query 复用
[...]
55: 每次仅对128个KV tokens构建FP32工作单元，不随全历史长度分配。两个AIV各负责32个query row；在每个32-token子块里，各AIV读取并解包16个KV row，四个子块按行写入K `[128,D]`，按列写入转置V `[D,128]`，每个INT2 slot只读取一次。SIMD Gather提取16bit编码字，8次Shift/And生成bit planes，再Gather还原维度顺序；scale/zero只在每向量应用，数据映射与PR保持一致。四个子块全部发布后，Cube只做一次QK和一次PV，Vector只做一次128列FP32在线softmax更新，跨核握手由每32列一轮变成每128列一轮。末尾不足128列仍写入K/V和P的零尾、每query精确因果mask与原始LSE/输出owner。
56: 
57: GM scratch的活跃区间明确互斥：Q `[64,D]`，K `[128,D]`，V `[D,128]`，score/P `[64,128]`，PV/最终`Rv^T`结果 `[64,D]`。QK的CubeReady在Vector覆盖score为P之前；PV读P只在VectorReady之后；PV被Vector累加后才用于最终旋转。K与V、score/P与PV区间不重叠。GraphWorkspace及C++ ABI用相同字节公式，不能让单独算子调用方传旧尺寸。
58: 
59: Softmax统计全程FP32：每row有running maximum与denominator，旧acc按max变化重标度，Cube完成 `P@V` 后累加。每个空tile概率置0；整段全空输出0/LSE-inf。Log采用不同输入/输出buffer，避免官方CPU-debug已发现的默认非原地API约束。
[...]
70: A2 Vector→Cube通信使用原生precedent的固定GM buffer，**没有把UB→GM→L1称作直接片上通路**。压缩源每token/head读136B(D256)；每tile仍写/读FP32 K/V通信，总通信量是Θ(LD)，只容量有界。严格H18“历史读取对L亚线性”与任意精确full attention冲突，本实现不声称满足o(L)，不以此停止其它可实现工作。
71: 
72: 当前通信是单buffer、显式阶段flag协议。它优先建立真实数值与无竞态基础；没有把源码中的CV分工当作性能证明。后续若profiler显示通信/解包/softmax吞吐不足，必须在相同冻结精度下优化流水，不可增大全历史workspace或降低精度。
73: 
74: ## 验证入口

## gpt_new_oscar_kimi/docs/cv_safe_finite_range.md
[...]
3: ## 状态与范围
4: 
5: **research：尚未实现、未编译、未做 CPU-debug/CAModel/NPU 验证。** 本文记录数学证明和只读源码/API 审查，不是数值或性能验收报告。没有修改生产 AscendC、SDK、GDN、服务候选开关或冻结精度门。
6: 
7: **后续决策：单独优化方向已淘汰，不实现。** C4 Q336插桩已完成数值与SDK task计时；两个actor的最终写回日志截断，整trace门仍失败，但所有`finite_reduce`叶子区间均完整、次数已逐actor对真实task/profile核对。core3两AIV的history分别为140861/133275 cycles，window9545/9362，总task为2660850 ticks；即使不计新增guard成本，也没有足够证据支持1.5倍完整核收益。详情见`reports/c4_phase_profile_q336_20261009/finite_leaf_evidence.json`及`partial_diagnostic_summary.json`。不将有限子范围证据扩写为完整相位验收。
[...]
9: 档案依据：#126 的 UB 复用所有权；#140 的客户端时间不可冒充内核归因；#145 的 MTE3→MTE2 依赖；#154 的 CPU 顺序模拟不能排除真 NPU 竞争。已重读启动文档完整 D.4 原始日志。D.4 的 6499.8–6655.1 ms 历史恢复、18.5–18.9 ms FIA、约 209 ms store 属于历史失败对照，不能用作当前相位时间。
10: 
11: 本研究只尝试省掉**已经能够证明结果为有限值的检查**。score、P、alpha、softmax、INT2 读写、FP32 计算和错误契约保持原样；不降低精度，不用逐元素 finite 冒充“求和不会溢出”。
12: 
13: ## 1. 当前代码确实存在的成本
[...]
151: - 已有 query/KV/page 错误：guard 不清除错误；原 ReduceSum 若会用 `error=2` 覆盖已有错误，必须由不安全路径继续作出同样更新。
152: - C4 `memberErrors`、kvError 和两个 AIV lane 的状态独立性不变；不能把一个 member 的 guard 结果写成另一个 member 的错误。
153: - ReduceSum 输出只供 finite 判断，不参与 P/alpha/LSE/输出计算。跳过的是一个已证明为真的谓词，不是用较低精度近似它的和。
154: 
155: 不允许用 guard 失败直接判 `error=2`：阈值外可能有很大的有限值相互抵消，而原归约仍有限。
[...]
164: 4. **完整错误域**：全不可见行坏值、部分不可见列坏值、padding poison、已有 metadata/query 错误及 C4 member/lane 混合错误。原/新 status 必须逐位一致；有效输出、P/partial、LSE 按原冻结门及适用的逐位门验证。
165: 5. **实际异步/图门**：真实 NPU 上同地址改变输入，使安全/不安全分支交替，检查 mask/临时 UB 无旧数据污染；CPU-debug/CANN 通过不得冒充此证据。
166: 6. **性能门最后执行**：同形输入、同精度、同图/运行方式比较正常原核与正常候选核；guard microprobe 时间只能解释成本，不能替代完整 kernel 时间。
167: 
168: 不新增真实用户数据集，不要求再次运行 AISBench；后续需要的目标验证仍是短时合成 probe。
[...]
189: 2. 历史失败：D.4 的全历史恢复约 6.5 秒、host enqueue 背压，以及 #145/#154 的缓冲复用竞争；不把其耗时套给本方案。
190: 3. 结构约束：仅固定最多 8-row/2048-score 临时位检查，不物化历史、不改 score/P、不重写归约树；阈值外原检查完整保留。
191: 4. 收益边界：当前未测。先用真实 C4 相位裁决是否值得做，再过原精度/错误/异步门和完整正常核 ≥1.5 倍门。

## gpt_new_oscar_kimi/docs/decode_candidate_20261007.md
[...]
1: # 2026-10-07 candidate 真机认证交付
2: 
3: 档案依据：#129/#140/#142/#145/#148/#151–155，以及启动文档 D.4。按用户最新指令停止扩大本地测速，交付已完成主要数值检查的组合方案；整轮 8 分钟与新版本真 NPU 精度仍由本轮真机结果认证。
4: 
5: ## 一键入口
[...]
17: ```
18: 
19: 两条命令共用 `tools/serving_variants.py`，实际启用相同组合。直启仍不运行 probe，不能把直启成功视作精度验收。默认物理设备 `0,1,2,3`、端口 `8989`；直启叠加 `--rear-cards` 使用 `4,5,6,7` / `7878`。启动时一行 `PERF_RUNTIME_CONFIG` 显示实际开关、token 预算和 scheduler。
20: 
21: ## 本轮启用
[...]
26: | 长/混合 C4、C16 | 同数学窗口批量读取及区间 mask |
27: | 零历史请求后缀 | 仅当前未压缩 K/V 用原生 current FIA，随后仍完整写入 INT2；设备 guard 验证零历史事实 |
28: | 首轮 MTP | 经原生调用链限定的 current 部分使用 FIA；历史保持 INT2，身份旋转不改 |
29: | 后续 MTP 大 padding | 仅已审计的 eager dense MTP 路径收缩到真实请求行；保留原 source split 与位置/slot 语义 |
30: | 混合批次 | FULL attention 内按请求边界分开短 decode 前缀与长后缀，保留原 split，不改 GDN |

## gpt_new_oscar_kimi/docs/design.md
[...]
15:  W --> A[causal attention / FP32统计]
16:  H --> A
17:  A --> O[稳定 LSE 合并与输出逆旋转]
18:  O --> M[原生 MTP acceptance / rejection]
19:  M --> S
[...]
35: | TP/W8A8 | runner 原生模型路径 | FULL attention 之外不替换 | 4 rank / ascend 权重量化保留 |
36: | prefix/抢占 | 原生 block 分配/共享 | 原生padding中的页边界精确snapshot | 无 owner 丢失后 INT2 替代 |
37: | 校准 | PR rotation.py; 论文 compute_kv_rotation.py | 模型/PR指纹 artifact | Hadamard 标明 data-free |
38: 
39: 接缝路径均相对 `references/vllm-ascend/vllm_ascend/`，vLLM 管理文件相对 `references/vllm/vllm/v1/`。详尽证据见 `native_integration.md`。
[...]
59: #128 补齐原生 `AttentionGroup.create_metadata_builders` 接缝：MTP会调用 `copy_with_new_block_size(128)` 为builder创建虚拟块视图。`OscarFullAttentionSpec` 通过显式 `metadata_block_view` 标记允许这个副本；`storage_block_size`、`layout`、真实payload与page字节数始终保留物理页值。原始group spec保持2304/2816，builder副本block_size为128；复制回物理块时移除标记。普通dataclass resize、未知块长、混合物理/虚拟spec merge仍报错，不改变池大小、GDN状态或数值路径。真实原生proposer初始化与AttentionGroup（含多个builder）回归覆盖none/align及不拆分分支；MTP slot更新回归采用实际初始化后的128块长。
60: 
61: 池 bytes=`num_tensors*nb*P`，包括原生尾padding `nb*(P-C-M)`；packed只使用实际SSM区，padding按物理页放精确snapshot（每页不超过原生已计费空间）。单请求 FULL token容量随 B_full 改变，但实际 capacity 还受3个 GDN group 的状态块、LCM、MTP、prefix占用制约。额外独立预算包括旋转常量、固定split workspace和当前chunk scratch；这些在model构造期预分配，计入原生profile，不能在KV预算确定后才偷分配。Snapshot BF16/tag已在P内，不重复计费。**不能仅根据136/1024宣布全模型显存收益。**
62: 
63: ## 5. 性能账与长度标尺
[...]
66: |---|---|---|---|
67: | prepare | 批量设备元数据 O(batch+new tokens) | 725ms host 异常 | 禁止逐请求 Python 热循环 |
68: | store | O(new/migrated tokens·D²) rotation，O(tokens·D) quant | 16K约215ms | rotate+clip+quant+pack+scatter已有融合实现 |
69: | history attention | Θ(LD/4) compressed读取，O(qLD)算术 | full dequant 6.5s、FIA18.7ms | 不准全历史BF16物化；CV未验收 |
70: | windows | O((S+R+q)D) | FIA子相位 | 只需精确有界BF16 |
[...]
92: |---|---|---|---|---|---|---|
93: | quant | PR store:41–77 | FP32输入、FP16 meta先舍入 | AscendC vector | 单head组、LSB-first尾块 | 非有限/零scale显式错误 | 独立oracle位级对拍 |
94: | rotation | PR attn:219–243 | x@R和abs quantile clip | AscendC融合算子 | 正交、来源可追溯 | artifact缺失或不匹配中止 | orthogonality+模型质量 |
95: | layout | runner:4696 | 压缩仅FULL | 外部spec/view | GDN地址隔离 | 无法容纳则显式错误 | byte区间与真实allocator |
96: | metadata | runner:3034 | 批量长度和slot | 独立builder | native容量与device不变 | 容量/形状契约错误 | capture/replay真机 |
97: | lifecycle | MTP/native blocks | BF16窗口不可遗失 | 原生页+canonical snapshot | prefix/COW/reject一致 | provider未就绪中止 | 状态机及真实调度 |
98: | attention | PR decode+LSE merge | 等价Q旋转/输出逆旋转 | 真实Cube/Vector kernel | causal/GQA/全长度 | 无production替代路径 | device→graph→TP4 |
99: | deployment | 原生serve参数 | 压缩路由确实命中 | 外部包+当前stream | 原生源码不变 | phase非零+资源清理 | 故障注入+硬件证据 |
100: 
[...]
104: |---|---|---|---|
105: |G1–G13/#3/#21/#79–85/#87–93|CANN编译/tiling/API/UB|单一ABI头、真实SOC、签名清build、原生先例|目标编译+加载+数值 |
106: |G14–G24/#23–25/#29–30/#84/#96–97|证书/校准/线程池|可信CA、采样一致性、fork前建池、显式artifact来源|本地环境记录+NPU校准 |
107: |G25–G34/#4–22/#53–69/#111|meta/数值/输出/LSE|独立PR oracle、冻结阈值、输出全部写入|CPU语义+NPU对拍 |
108: |#26–52/#74–78|导入/容量/事务|轻量hook、实际buffer容量、owner不伪造|fresh process+调度状态机 |
[...]
125: - [x] PR工程差异、数学冲突和历史失败未隐藏。
126: - [x] 原生页/snapshot/MTP可见性源码及原生方法、CPU-debug回归已完成；真机生命周期另列。
127: - [x] 真正fused CV、融合旋转裁剪、设备metadata和guard已实现并经CANN编译。
128: - [x] CANN编译和官方CPU-debug通过。
129: - [ ] 真实NPU数值、图回放、性能和实际容量通过。
[...]
136: |---|---|---|---|
137: | prepare | host约725ms | 一次设备metadata launch；后续draft由BT/slot定位，CPU不读长度值 | O(new_tokens log requests + metadata)，后续draft每req查有效表列；CPU-debug，NPU耗时未测 |
138: | rotate/fused store | 16K写约215ms | Hadamard蝶形或FP32 dense tile；精确sort percentile；只写新token和canonical snapshot | O(NHDlogD)或O(NHD²)，固定UB<64KiB；26个CPU-debug用例 |
139: | history/window/current CV | dequant6499.8–6655.1ms vs FIA18.5–18.9ms | 同一kernel流式读码、Vector解包/softmax、Cube QK/PV/输出逆旋转；Mq64容纳GQA6×MTP4 | INT2读取Θ(L)，每Cube固定278528B(D256) GM，显式UB161024B/AIV；无[L,D]恢复；实际NPU耗时未测 |
140: | merge | materialize约0.5ms | FP32稳定LSE，空split poison不参与，独立Log输出buf | O(N*Hq*splits*D)，CPU-debug S1/3/128 |
141: | guard | host/串行小op易累积 | 单设备核聚合四状态并Trap，替代eq/all/assert多launch | O(status元素)，无D2H；CPU-debug真错误注入通过 |
142: 
143: 每项更完整六问/ABI/同步与预算在 cv_implementation.md、rotation_pipeline.md、runtime_implementation.md；它们与本表共同构成本设计。Hadamard是明确算法选择，dense旋转也已实现，不是运行失败后的替代路线。默认无profiling事件；显式OSCAR_TIMING的host_s不写成device_ms，设备时间由真实NPU trace归因（profiling.md）。
144: 
145: 运行调用链为prepare→rotate→CV→merge→新KV store→guard；native源方法实际执行测试还验证了spec merge的AssertionError协议、17/16/16/16分组和共享页manager分配。C、M、P和GDN保留页数均动态读取。若假定三个GDN组保留全历史状态，Bfull由768到2304仅将总块数12L/2304降为10L/2304，理论上限约1.2倍而非3倍；align的实际保留与prefix/LRU另按原生manager核算；本次none配置则保留每个GDN组1+3状态，FULL块长2816，最终收益待实机。
[...]
151: 默认arena容量不变，设 `qtile=floor(64/GQA)`、`groups=ceil(n/qtile)*Hkv`，选择 `S=max(1,min(32,ceil(CubeCores/groups),floor(arena_token_capacity/n)))`。只读取已经给定的shape/设备属性；同一捕获n始终得到同S/地址/stride，不读取CPU seq_lens。原partial/LSE/tasks/status平面arena复用为3*S段，保证n*S不超预分配容量。实际20Cube/GQA6时n4→S20，n16384→S1，避免单请求历史只有一个task。新增S2/S20真实CPU-debug已证明互斥历史分区、query复用、empty splits与真实3*S merge的数值一致；没有因此宣称NPU提速。
152: 
153: #129 性能排查：D.4重新逐行对照。该算子对应dequant+FIA；历史全量恢复6499.8–6655.1ms而FIA18.5–18.9ms的结构仍禁止。本次没有增加历史恢复或另一路attention：仅改变任务归属顺序、移除因果上不可见的future-only tile。固定GM/UB预算、GQA querytile及数学精度不变；实际有效计算仍为精确attention复杂度，不声称亚线性。GQA6/Q16K/S1示例旧current任务只落在2/20核；新分配每核81–82个querytile。原始current源KVtile为839168，因果裁剪后为420761，见reports/prefill_work_analysis.json（按程序计算值为准）；这些是静态工作量，不是实测加速。新63项官方CPU-debug通过，仍需NPU逐相位证据及与原生0.6–1.1ms短步/18.5–18.9ms FIA量级比较。
154: 
155: #130/D.4：对应历史解包+FIA及current精确FIA。历史全量恢复曾6499.8–6655.1ms，而FIA18.5–18.9ms；本轮仍不恢复全历史。每个AIV半tile最多16行：history按虚拟128边界切连续段，用带head stride的2D DMA一次搬入，跨边界重新查表；current使用一次2D DMA与一次BF16→FP32 Cast，复用naturalBuf。逐行finite校验、量化metadata与FP32数学均保持，窗口tag路径不改，UB/GM预算不增加。减少的是DMA/Cast提交数量，最多16行合并，不等同16倍实测提速；仍需达到原生0.6–1.1ms短步和18.5–18.9ms FIA量级。67项官方CPU-debug（含多head/跨页/尾行）通过，真实设备性能尚待复验。用户确认ArgSort/AiCPU告警基线也存在，不据此归因OSCAR，也不修改原生排序类型。
[...]
175: 4条长度的注意力配对计算中，current源占比随每请求chunk上限4K/8K/16K约为15.5%/29.8%/55.9%；不能将最大值套用实际混合调度。新旧Matmul都可能在单次调用内完整装载A/B到L1；改basic块降低L1→L0、MMAD与barrier次数，不声称减少相同比例的GM/HBM流量。固定GM scratch和CV跨核同步仍存在。
176: 
177: 一键入口自动先校验当前构建及CV/旋转NPU精度，再检查实际current FIA、生产三源合并和任务改写，失败不启动服务。client K4比值门不放宽；本机CANN/CPU-debug只能排除编译与数值契约错误，不能证明NPU性能。
178: 
179: ### 9.3 根据已测历史CV热点修改（#144）
[...]
196: 4. **两本账**：符合条件的组，C4→C16可把解包/packed读取次数再降到1/4；QK/PV、softmax及逐组spill/restore不会降到1/4。每核workspace D256为4,997,120B，20核99,942,400B；较C4每卡增加63,160,320B，在原生KV预算前预留且跨FULL层复用。UB形状与fast C4相同，无全历史恢复缓存。前沿/尾部/短组仍完整执行同一INT2 C1数学，绝无BF16历史替换。
197: 5. **为什么不盲扩所有形状**：只有已知max_query_len≥8192才选C16（目标GQA6下有足够簇供20核）；较短或未知长query保留C4。later-MTP q1保留已验证fast_q1。原base路由只有N>128才选balanced。`experimental_mixed_cv`必须依赖history+fast；默认原配置/显式baseline仍保持既有fe0语义。candidate统一预设自动启用新两核，不把优化仅留在probe。
198: 6. **收益的反证条件**：冷mixed可能无C16簇，却仍有扫描成本；C16增加状态与判定开销，balanced增加outer workitems，均可能抵消收益。旧C4已有27%左右局部提升，继续扩大复用不能假定再快4倍；也没有证据证明这两项足以消掉整程58.82%耗时。短NPU门必须逐例对比当前fast基线和新算子，实际不同算子的CV及整个attention包络均不允许回退；若失败即停。只分析与验证这些有证据的结构改动，不调整模型/GDN/MTP语义、不降低FP32精度，不改用户完整AISBench负载。
199: 
200: ### D.4四问及验收边界
[...]
213: 原combined harness将fe0、C16、merge/oracle放入同一个120s预算，D256q336与非对齐q3+q336各出现过rc124。没有删除原例、缩小输入、放宽误差或调高120s。新`tools.run_mixed_cv_cpu_debug`先真实运行fe0并过oracle，写新建目录中的原始参考bytes，再独立运行C16逐位比/同oracle；每次执行仍限120s，核对golden及参考bytes SHA/尺寸且失败立即停止。相位计时证明D256 fe0 kernel约50.007s、C16约70.576s，两者相加已超过120s；含各自校验的两进程分别57.280/77.735s全部通过。非对齐完整例分别62.565/78.836s通过。旧超时日志与最终通过记录同时保存，不将模拟器耗时当NPU速度。该工具仅用于维护者本地CANN VM，不是真机部署前置命令。
214: 
215: 新balanced/C16的真NPU精度、独立图、速度仍未在本机验证；新增目标短门须过关。已有旧fast/C4/q1真NPU通过不会代替新核证据，更不代表已经追平8分钟或本次1371.969秒。
216: 
217: ## 2026-10-13：MDL q1 与 q4 组合，保持全部浮点数学
[...]
233: 依据档案 #34/#36/#126/#129/#145/#148/#151/#154–160 与 D.4，设计及资源明细见 [本轮设计](stable_optimization_20261015.md)。新增q4 hybrid仅按地址重排不可变Rv；C16 B1只在原16成员同请求/同历史域内复用一个固定256KiB B1，保持FP32/K128次序、错误域和INT2/精确窗口边界。元数据、GDN及原生源码不改。C16增加47.5MiB/rank（20核），Rv约4.25MiB/rank，均在原生KV profiling前分配。
234: 
235: D.4四问：①对应融合history dequant/FIA内部的浮点数据装载和同步；②规避旧全历史恢复约6.5秒、非融合store约215ms及异常host prepare约725ms，旧数值不作本轮分母；③固定KV256、单B1及16个固定score槽，没有历史长度大小的恢复张量，没有BF16精度替代或静默原生回退；④新增GM/L1、固定任务扫描、所有源及merge/copy均计入相应完整门，源码省字节不能宣称省时。CPU-debug、CANN编译、CAModel、真实NPU、图、模型质量和两场景整轮性能各自记录，不相互替代。

## gpt_new_oscar_kimi/docs/dual_bf16_residual_feasibility_20261011.md
[...]
1: # 双 BF16 残差、三项补偿：只读筛选（2026-10-11）
2: 
3: **状态：已提出、现有证据审查完成；暂缓，不入组合、不写核。** 直接三次完整 Matmul 拼接已无速度依据；未知融合实现尚无精度资格和足够大的完整净收益证据。未运行新实验，未修改精度或生产路径。档案 #148/#154 与 D.4继续约束模型精度、异步生命周期和有界工作区。
4: 
5: **方案与精度边界。** 对每个FP32输入设 `xh=BF16(x)`、`xl=BF16(x−FP32(xh))`，两侧均分解，再计算 `XhYh + XhYl + XlYh`，三项均FP32累加。它遗漏 `XlYl` 和残差再次舍入的误差；即使加第四项，也未自动消除表示误差及新的累加舍入。将三次点积再相加，或在每个K128内串行加入三项，均改变原FP32乘积/累加链；不能把它声明为保持原逐输出数学顺序的布局变换。
6: 
7: 在RNE、正常数且无溢出/下溢的假设下，BF16单位舍入误差 `u=2^-8`，两分量表示及遗漏低×低项的误差量级为 `O(u²)`；点积绝对误差仍受 `Σ|xk·yk|` 控制，抵消时没有统一的小相对误差保证。FP32有限极大值、subnormal、signed-zero/nonfinite和原错误优先级也不在该简化界内。必须对实际可达域独立论证，不能改oracle、放宽冻结门或新增静默单cast路径。
8: 
9: **不能直接单cast。** [已有有限值反例](../reports/single_bf16_cast_counterexample_20261009.json) 中，INT2可表示的K为1和1.0029296875，单BF16 cast均变1；FP32累加也救不回丢失输入，输出误差0.092667超过当点冻结门0.007963。[已存prefill压力报告](../reports/prefill_tile_stress_20260930.json) 有7个可由store到达的失败，且存在LSE过而输出失败。这些否定无条件单cast/已有dtype替换，**并不证明三项方案已失败**；两分量甚至可能修复该特定单cast反例，但尚无它自身的完整精度证据。
10: 
11: **现成速度证据只支持筛掉直接拼接。** [同形完整任务结果](../reports/fp32_bf16_mmad_ratio_20261010/decision.json) 为QK24 `19890→16399` ticks（1.212879倍），PV126 `34758→26214`（1.325933倍）。[微核源码](../csrc/experiments/fp32_bf16_mmad_ratio/kernel.cpp) 是单次Matmul、basic64/64/128、HF32关闭；输入本身可被BF16精确表示，没有残差分解或三项重组。若简单复用三次完整BF16调用，条件成本已为49197/78642 ticks，约为原FP32的2.47/2.26倍，尚未加producer与重组；这不是三项方案的新测量。个别MMAD驻留277→85、533→149含流水等待，不能求和成wall、当dtype峰值或取代完整分母。
[...]
15: **流量与空间不能按单BF16减半。** 两份BF16合计仍为4B/输入值，等于原FP32；无复用的三项消费者会合计读取每操作数6B/值，另有cast回FP32、减残差、再次cast、NZ布局和事件成本。若三份FP32部分积落GM，再读回合并，输出阶段是三写三读加一写，约28B/输出元素，相比单份4B显著增加；共用L0C可避免这部分GM流量，但必须证明容量、调度、累加和完成协议。上述是逻辑搬运账，真实HBM与L2命中分开计；不得把host预分解或免费packing藏在分母外。持久INT2压缩率不会因此再提升，新增workspace反而可能减少可驻留batch；MTP全部轮次的分解/计算/流量也须除以实际有效输出量核算。
16: 
17: **重开条件：** 独立精度论证覆盖冻结的实际可达域，且一个明确的融合数据流在真实producer、三项计算、重组和同步都计入后，仍有明显完整算子/step净贡献，才值得研究。只有dtype峰值、单cast通过样本、消除某次转换或1–5%小增量，均不重开。当前结论是证据与净收益不足，不能写成已证明所有多分量算法不可行。

## gpt_new_oscar_kimi/docs/fast_unpack.md
[...]
1: # 从19分钟继续压缩：三条CV路径的精确解包候选
2: 
3: 依据：启动文档D.4、档案#126/#129/#140–#151、q4真机分段证据及用户本轮最新19分钟反馈。用户确认的fe0精度基准保持有效；本轮没有要求或执行新的AISBench。
4: 
5: ## 目标预算与已确认的代码问题
[...]
16: 4. fe0/C4/q1/profile四个已有kernel源文件逐字节不变，始终可用于独立同输入对照；生产路由没有原生BF16全历史替代。
17: 
18: 显式UB增加448B，D256为157632B，小于A2可用188416B；GM工作区、缓存和图地址均不改变。整数码映射、半精度转换以及生产图分别验证，不把CPU结果代替NPU。
19: 
20: ## 已完成的验证
[...]
46: ## 0677bcb 真机复验
47: 
48: 用户回传`observe-20260928T064725.021030Z`，签名前缀`a1304fb6f1dd`；所有fast精度、独立图及性能门passed，正常`OBSERVE_PROBE_DONE service_started=false`结束。原文`reports/target_fast_unpack_pass_20260928.txt`。
49: 
50: | 场景 | 原路径ms | fast ms | 耗时下降 |

## gpt_new_oscar_kimi/docs/fp32_manual_matmul_feasibility_20261010.md
[...]
1: # A2 FP32低层Matmul：只读可行性审计
2: 
3: 当前未写CANN、未编译或执行。依据当前native A2源码、实际FP32 trace及root只读导出的CANN9.1 SDK（`artifacts/cann_sdk_matmul_move_20261010/provenance.json`记录来源与哈希）。档案#13–22/#70–73/#81–85/#126/#140/#145/#148/#154–156和startup D.4；不取arch35能力，不改精度/原生代码。
4: 
5: ## 结论
[...]
92: - 这是有限独立Matmul研究，不改生产、不宣称≥1.5或整轮2–3×；如果去通用调度后净收益不足就停止，不再做另一轮只有SetShape差异的长实验。
93: 
94: D.4对应fused FIA QK/PV/rotation；不增加历史长度相关的物化，只在当前KV256矩阵范围使用固定L1/L0。原失败全历史解包约6.5秒不能被这个局部研究掩盖。

## gpt_new_oscar_kimi/docs/history_reuse_experiment.md
[...]
1: # fe0 基准上的端到端诊断与 C4 历史复用
2: 
3: 依据：档案 #126/#129/#140–#145/#148、启动文档 D.4、当前项目 fe0 源码及用户回传。fe0已由用户确认精度正确；本轮不改变这一基准结论。
4: 
5: ## 为什么22分钟不能靠此前的小改动追到8分钟
[...]
13: ## 本轮实验改变什么
14: 
15: 新`attention_cv_cluster4_out`与原`attention_cv_out`是两个独立算子。旧kernel文件不改，新文件从本项目fe0复制其数学函数，保持Unpack、metadata校验、Softmax、QK/PV和最终旋转的原有计算方式。
16: 
17: 只将同一request、kvhead、source0、split、context、kvbegin、kvend的4个完整query组组成簇，且要求kvend=context。每个256KV历史块解包一次，给4组各自的QK→softmax→PV使用。每组独立保存FP32 accumulator/max/sum，并保持该组原KV遍历顺序；窗口/current源不共享。
[...]
28: - QK/PV浮点工作总量不变，spill/L2/任务扫描与并行损失可能抵消收益。因此同输入速度门严格执行，达不到就不启动候选服务。
29: 
30: ## 精度与收益门
31: 
32: `tools/probe_history_reuse.py`在同一签名扩展中运行fe0两次，再运行C4：
[...]
37: 4. 共享KV非法metadata、仅一组QR NaN、poison及同地址改输入的独立NPU图回放均覆盖。
38: 5. 正常2次预热、5次NPU Event测速，交替AB/BA顺序；原速度门不放宽。
39: 6. 候选服务仅接受本轮签名/产物/源码匹配且图和精度、速度门通过的报告。默认仍fe0；显式候选只用于用户评测，不等于生产质量或全场景速度验收。
40: 
41: 本地CANN编译与官方CPU-debug最终51项通过，包含C4实际参与时与fe0的逐字节对照。同一过重形状的两个CPU模拟器配置达到120s限制，已保留记录；以D64长多tile、D128双head、D256大维度的互补病例验证，未提高时限。相关主机回归95 passed、28 NPU skipped、4 subtests passed。完整记录见`reports/history_reuse_cpu_validation.json`。目标NPU、完整模型图、用户模型质量及8分钟性能仍需真机裁决。
[...]
45: 2026-09-28真机更新（#150）：9/9逐位病例、6个有效oracle及独立图捕获/回放通过；mature_20k的C4为56.1855ms、fe0为76.3791ms（耗时下降26.44%）。decode32无簇，40.2677ms对40.2259ms，仅差0.04184ms，原严格比值门因此关闭服务；单轮不足以区分这0.104%中的波动与真实调度开销。
46: 
47: 当前生产分流用原生host `max_query_len` 与总token形状判断必要条件：单请求不足4个完整query组（GQA6为84token）就直接调用fe0的OSCAR INT2算子，不记录C4扫描和计数。未知上界保守保留C4，所有可能复用的长请求仍由C4内部严查同域。无设备回读、不改AscendC和图数据地址。probe保留原始C4全部精度/图对照，性能部分使用与服务相同的分流；短请求两侧为同一fe0算子，保留实测时间/比值作重复性对照，标`identical_fe0_operator`，不把自比噪声当优化成败。实际选中的C4仍严格要求ratio≤1.0。该分流的目标是真实负载采证可继续，不把0.042ms宣称为追回14分钟的优化。
48: 
49: `install_observe_serve.sh`不替用户发AISBench请求。默认baseline为fe0，candidate显式选择C4，native禁用OSCAR数学路径；启动前锁定fe0原内核哈希，候选也保留这些原内核，并记录实验文件及构建签名。

## gpt_new_oscar_kimi/docs/innovation_competition_idea.md
[...]
3: **项目名称：OSCAR-Ascend——面向昇腾大模型推理的 INT2 KV 缓存压缩与融合计算方案**
4: 
5: **【场景描述】**：在长文档问答、多轮对话和多用户并发等场景中，大模型需要持续保存并读取历史上下文的 KV 缓存。随着上下文和并发规模增长，缓存占用与访存开销不断增加，限制了昇腾设备可承载的请求规模。超低比特压缩可以降低缓存开销，但直接量化容易损伤精度，先将全部历史解压后再计算又会引入额外搬运成本。因此，需要让低比特存储、精度保护与昇腾计算路径协同设计。
6: 
7: **【方案实现描述】**：本项目基于 OSCAR 的低比特 KV 缓存方法，面向昇腾实现“**历史 INT2 压缩、关键窗口 BF16 保留、分块融合 Attention**”的推理流程，以外部插件和独立 AscendC 算子接入 vLLM Ascend。
8: 
9: 1. **压缩历史，保留关键上下文。** 新 K/V 在本轮计算完成后，经正交旋转、可选裁剪和 INT2 量化，将每个元素编码为 2 bit，4 个值打包到 1 字节，并保存缩放与偏移参数。起始和最近窗口额外保留原始 BF16 值，当前输入块也直接使用 BF16，兼顾历史缓存容量与关键上下文精度。
10: 2. **边读边算，避免完整历史展开。** 读取历史时，AscendC 算子按块解包、反量化，由 Vector 单元处理数据转换和 Softmax、Cube 单元完成矩阵计算；历史分支在旋转域计算后将输出变换回原空间，再与精确窗口、当前块的结果按归一化权重合并。工作区按块复用，无需在显存中重建完整 BF16 历史。
11: 3. **接入真实服务，释放容量潜力。** 仅接管全注意力层的 KV 路径，保留混合模型中 GDN 线性注意力的原生状态与计算，并对接分页缓存、多卡并行和 MTP 多 token 预测流程。无需覆盖原生框架源码，为相同硬件承载更长上下文、更大并发批次提供基础。
12: 
[...]
14: flowchart TB
15:     A["全注意力层：本轮 Q / K / V"]
16:     R["本轮 Attention 完成后写缓存<br/>K/V 正交旋转 → 可选裁剪<br/>INT2 量化打包：4 个值 / 字节"]
17:     H[("历史 KV 缓存<br/>INT2 编码＋缩放 / 偏移参数")]
18:     W[("关键窗口缓存<br/>起始 / 最近上下文保留 BF16")]
19:     Q["历史分支的 Q 同步旋转"]
20:     F["昇腾分块融合 Attention<br/>Vector：解包 / 反量化 / Softmax<br/>Cube：矩阵计算"]
21:     B["BF16 Attention<br/>精确窗口、当前块分别计算"]
22:     T["历史结果逆旋转<br/>回到原始值域"]
23:     M["三路结果按归一化权重合并<br/>输出 Attention 结果"]
24: 
[...]
49: <!--
50: 文档核实日期：2026-10-13。本文为创新大赛方案简介，不将 OSCAR 已有算法本身声明为本项目首创。
51: 源码依据：oscar_ascend/integration/impl.py（历史/窗口/当前三路，旋转、LSE合并、先读后写）；
52: oscar_ascend/integration/cache_storage_ops.py（裁剪默认0）；oscar_ascend/layout.py::SlotLayout（136/1024字节）；
53: csrc/kernels/attention_tasks.cpp、attention_cv.cpp（分块CV与三路计算）；rotate_clip_store.cpp（旋转/量化/打包与BF16窗口）。
54: 档案引用：issue1_full_record.md #70–73与启动文档D.4约束完整历史展开；#126区分运行与数值通过；
55: #130–131约束长请求与并发验收；#156约束容量/吞吐外推；#157–158约束当前候选稳定性。

## gpt_new_oscar_kimi/docs/integration_review.md
[...]
1: # Independent integration review
2: 
3: Reviewed the newly written deployment, build, rotation preparation, primitive
4: probe, readiness reporting, and native hook code. Only this workspace's
5: authorized reference trees and archive logs were consulted. No failed OSCAR
[...]
60: ## Current implementation and target boundary
61: 
62: The concrete RuntimeProvider, AttentionImpl, allocator/GDN delegation, native page snapshots, MTP slot-derived positions, graph workspace, fused CV/rotation/store, status guard, service probes and cleanup are implemented. Official CANN CPU-debug and cross-compilation evidence is in reports/vm; additional real native method execution tests cover grouping, manager/hash/LCM, shape derivation and rejected-token draft updates.
63: 
64: Remaining acceptance: target NPU execution, actual capture/replay, model quality, memory benefit and paired performance. Direct launch is the chosen native-supported independent-library interface; no custom OPP vendor package is produced. H18 literal sublinear reads remains an explicit conflict.
[...]
78: in reports/pytest.log. CANN VM cross-compilation and official CPU debugging have
79: since passed. Target device completion, actual worker binding, graph capture,
80: graph replay, model accuracy and performance remain not run.

## gpt_new_oscar_kimi/docs/kimi_commit_review_20261013.md
[...]
33: 压缩减少的是持久 KV 容量；当前每历史 token 的 K/V 又展开成 2048 B FP32，并经有界 GM 工作区供给 Cube，写加读至少 4096 B 逻辑地址流量。这不等同真实 HBM 字节，但确实抵消了压缩存储的执行优势。当前完整多 KV 模拟显示 QK/PV 数据交付是主要关键链，不能只削减已被隐藏的解包时间。
34: 
35: 继续基于当前 MDL 母源评估直接 NZ 解包与消费，计入真实 publisher、精确窗口/current、旋转、全部任务和错误域。只把完整相关路径 `t_base/t_new >= 1.15` 且精度/协议合格的项纳入组合。最终目标仍为原生 2–4 倍；单项模拟结果不替代整轮认证。
36: 
37: 默认 prefix caching 开启，使用已有物理页拥有的精确快照；未完成跨请求恢复的 request-window 研究保持关闭。默认原生 token budget、GDN、冻结精度和两个 candidate 一键入口保持一致。
38: 
39: ## 077 修复支线继续闭环（2026-10-13，源码与主机证据）

## gpt_new_oscar_kimi/docs/mdl_decode_gate.md
[...]
15: ## q1 本地资格（2026-10-13，非NPU结果）
16: 
17: 当前Normal q1母源与MDL使用同一库、相同完整R2/N8/C1344,1376/S1输入；6组CPU数值/错误域通过，完整CAModel **948223→797943 ticks，1.188334254倍**。全部partial/LSE/status逐位、独立原空间oracle、三源/全部24任务及每臂6份完整指令日志通过。只增加已存在MDL q1符号的生产注册，未改数学、精度、workspace或跨核事件。
18: 
19: 完整指令证明B装载由232条减少到34条；history每次QK/PV从8×32KiB合为1×256KiB，FP32 MMAD参数序列相同。中间完整history周期中值39508.5→28352.5 ticks；实际GM逻辑字节没有减少，不能说HBM流量同比下降。每步MTP的q1频度与target q4不同，两个倍率不能相乘成整轮收益。[配对](../reports/q1_mdl_qualification_20261013/completed/comparison.json)、[完整装载分析](../reports/q1_mdl_qualification_20261013/load-analysis.json)。

## gpt_new_oscar_kimi/docs/mixed_cv_optimization.md
[...]
10: 4. **两本账**：符合条件的组，C4→C16可把解包/packed读取次数再降到1/4；QK/PV、softmax及逐组spill/restore不会降到1/4。每核workspace D256为4,997,120B，20核99,942,400B；较C4每卡增加63,160,320B，在原生KV预算前预留且跨FULL层复用。UB形状与fast C4相同，无全历史恢复缓存。前沿/尾部/短组仍完整执行同一INT2 C1数学，绝无BF16历史替换。
11: 5. **为什么不盲扩所有形状**：只有已知max_query_len≥8192才选C16（目标GQA6下有足够簇供20核）；较短或未知长query保留C4。later-MTP q1保留已验证fast_q1。原base路由只有N>128才选balanced。`experimental_mixed_cv`必须依赖history+fast；默认原配置/显式baseline仍保持既有fe0语义。candidate统一预设自动启用新两核，不把优化仅留在probe。
12: 6. **收益的反证条件**：冷mixed可能无C16簇，却仍有扫描成本；C16增加状态与判定开销，balanced增加outer workitems，均可能抵消收益。旧C4已有27%左右局部提升，继续扩大复用不能假定再快4倍；也没有证据证明这两项足以消掉整程58.82%耗时。短NPU门必须逐例对比当前fast基线和新算子，实际不同算子的CV及整个attention包络均不允许回退；若失败即停。只分析与验证这些有证据的结构改动，不调整模型/GDN/MTP语义、不降低FP32精度，不改用户完整AISBench负载。
13: 
14: ### D.4四问及验收边界
[...]
27: 原combined harness将fe0、C16、merge/oracle放入同一个120s预算，D256q336与非对齐q3+q336各出现过rc124。没有删除原例、缩小输入、放宽误差或调高120s。新`tools.run_mixed_cv_cpu_debug`先真实运行fe0并过oracle，写新建目录中的原始参考bytes，再独立运行C16逐位比/同oracle；每次执行仍限120s，核对golden及参考bytes SHA/尺寸且失败立即停止。相位计时证明D256 fe0 kernel约50.007s、C16约70.576s，两者相加已超过120s；含各自校验的两进程分别57.280/77.735s全部通过。非对齐完整例分别62.565/78.836s通过。旧超时日志与最终通过记录同时保存，不将模拟器耗时当NPU速度。该工具仅用于维护者本地CANN VM，不是真机部署前置命令。
28: 
29: 新balanced/C16的真NPU精度、独立图、速度仍未在本机验证；新增目标短门须过关。已有旧fast/C4/q1真NPU通过不会代替新核证据，更不代表已经追平8分钟或本次1371.969秒。

## gpt_new_oscar_kimi/docs/mixed_prefill_analysis.md
[...]
12: | `t=0…170 s` 生成采样积分 | ≈1,834 token；平均 10.8/s | ≈17,812 token；平均 104.8/s | OSCAR/原生≈0.103；不能外推 16/8 分钟。 |
13: | 同窗 Running/Waiting 采样均值 | 17.5 / 14.4 | 20.1 / 11.7 | 均值是调度状态采样，不是完成数。 |
14: | 同窗 MTP Accepted/Drafted 计数加权 | 1,162/1,941 = **59.9%**；推算平均接受长度≈2.80 | 12,298/16,488 = **74.6%**；推算≈3.24 | 每轮 3 个 draft 下，接受长度约差 14%；不能单独量化解释约 9.7 倍生成速率缺口，更不是模型精度。 |
15: | `t=140 s`，双方均 `Running=25, Waiting=7` | 07:28:31 输入 4,141.8/s、生成 **17.2/s**、KV 45.9%（80–81 行） | 03:14:07 输入 3,786.2/s、生成 **125.3/s**、KV 91.4%（213–214 行） | 相同队列计数和接近的输入速率仍伴约 7.3 倍生成速率差；请求阶段/长度组成未知，不能据此断定单一算子根因。 |
16: 
[...]
45: 4. 同一逻辑decode cohort加一条q16260、旧历史13740的prefill，最终长度30000；路径同上。
46: 
47: 每个形状核对冻结独立oracle，mixed验证source2抑制/写回；不要求数学实现不同的FIA与CV逐位一致。终端输出四条`PERF_MIXED_ATTENTION`及`PERF_MIXED_RESULT`，完整数据在`mixed-attention-report.json`。每相位无同步，结束Event确认设备完成；准备/旋转在测量区间外，current包含FIA及source2写回。这只覆盖单层主模型FULL attention，不包含其余模型算子、MTP draft、图回放或调度器。
48: 
49: 若对照2相对1明显变慢，才能定量支持padding/split工作分配优化；若形状4的CV主导、形状3较轻，则优先处理长prefill反复读取/解包历史；若CV较轻而current/其它相位主导，就不能用CV加速比例外推整步。不同形状中位数之差不是严格的独占prefill耗时，最终仍须保留同一步证据。旧mixed同一步的MTP draft0 CV约236ms、整步5732ms，也不足以独自解释16→8分钟（`reports/target_observation_20260928/snippet-2.txt`）。
50: 
51: 目前不直接缩小默认chunk：这可能增加后续chunk需要反复扫描的INT2历史，即使token间隔更短，总耗时仍可能变差。档案 #133 的HTTP profiler曾导致worker失败，本诊断沿用有界Event。常用`install_serve.sh --variant candidate`仍安装并启用C4/q1/fast unpack；本轮新增的是诊断，没有未经测量的新生产调度策略。完整模型精度、8分钟目标仍未新增验收。
52: 
53: 本地主机验证：`PYTHONPATH=. .venv/bin/python -m pytest -q tests/test_probe_mixed_attention.py tests/test_observe_serve.py tests/test_probe_history_reuse.py tests/test_install_serve.py tests/test_serving_variants.py`，60 passed。覆盖空历史fixture、同输入padding对照、生产相位顺序、报告与阶段状态不重名、失败退出码及资源释放失败不掩盖首错。Mac没有NPU，本轮四组新形状的设备数值与时间未测，不能把这60项测试当成设备或性能通过。

## gpt_new_oscar_kimi/docs/native_integration.md
[...]
5: attention runtime.** The plugin rejects enabled dense FULL routing until a
6: concrete runtime provider passes its readiness check. Compilation, kernel
7: accuracy, cache lifecycle, graph capture, graph replay, and performance are
8: separate pending acceptance states.
9: 
[...]
126: 
127: The physical pool budget is `nb * shared_tensors * P`, counted once. Add
128: the actual bounded window arena, rotations, metadata, graph and kernel
129: workspaces. `MemoryBudget` requires these quantities explicitly and labels
130: `nb*B` as a FULL capacity **upper bound**. Usable request capacity must subtract
131: the null block, native GDN reservations, per-request rounding, and all extras.
132: 
133: ## Runtime handoff interface

## gpt_new_oscar_kimi/docs/nz_column_owner_20261010.md
[...]
1: # NZ发布的D列分工备选：只读审查
2: 
3: 2026-10-10；只讨论当前striped source0，未写核/改精度/运行VM。档案#13–22/#70–73/#126/#145/#148/#154–156、startup D.4。等待预pack-B微测，再判断是否值得实现。
4: 
5: ## 可成立的布局与收益范围

## gpt_new_oscar_kimi/docs/nz_query_probability_layout_20261010.md
[...]
1: # A/P-NZ布局与生命周期：只读可行性
2: 
3: 2026-10-10；不改核/ABI/精度，不运行VM，等待同配置AB-NZ微测。档案#126/#140/#145/#148/#154–156、startup D.4。A/B保持FP32、HF32关闭，C/score/PV输出仍ND。
4: 
5: ## 1. 物理行跨度不能当成真实M

## gpt_new_oscar_kimi/docs/observation_20260928.md
[...]
45: ```
46: 
47: 只安装/编译和执行真实NPU门，之后退出；不启动模型、不发推理HTTP请求、不运行AISBench。新q1探针采用32独立历史、真实1token/请求，分别保留N128/S3和N16384/S1的padding；对同一task表做fe0逐位、冻结oracle、独立图同地址改输入回放以及2次预热/5次交替A/B。任何精度/图/速度门失败均停止，不放宽阈值。旧decode32算子probe固定S1，本轮已对齐生产S3并打印split来源；不能把旧40ms直接乘模型层数。
48: 
49: 这些短probe只能决定该调度候选是否有价值。目标图内部热点及完整服务8分钟目标仍须通过更小的合成诊断逐步定位，不再要求用户重跑AISBench。
[...]
51: ## 本轮本地验证
52: 
53: CANN ascend910b4编译通过；官方CPU-debug5/5通过，包含与fe0逐字节partial/LSE/status、独立oracle、padding/S1/S3/空历史/错误元数据/D256。N128/S3病例的source0任务96个，旧6核、新20核；这是CPU任务归属计数。相关主机回归119 passed、28真NPU skipped、4 subtests passed。编译源码指纹与边界见`reports/q1_schedule_local_validation.json`。新q1真NPU精度、图和速度均待上述短probe验证。
54: 
55: ## a13af95 真机短probe回传

## gpt_new_oscar_kimi/docs/operator_inventory.md
[...]
7: |store_int2_out|FP32[N,H,D]→136B/head/token(D256)，fp16 metadata，SSM SoA scatter|store_int2.cpp|D64/128/256，i32/i64，页边界/负slot/越界，CPU-debug逐位 |
8: |merge_lse_out|FP32 partial[R,S,D]+LSE[R,S]→FP32输出/LSE，所有空行写0/-inf|merge_lse.cpp|S1/3/128、poison空split，CPU-debug；修复真实Log禁止inplace问题 |
9: |rotate_out|BF16/FP16/FP32当前query→FP32旋转结果，原始/逆旋转均由R转置契约决定|rotate_clip_store.cpp|Hadamard蝶形与dense FP32，CPU-debug |
10: |rotate_clip_store_out|新K/V→旋转、精确percentile clip、quant/pack、BF16 page snapshot和tag|rotate_clip_store.cpp|26种旋转/融合写用例：精确码/meta/guard/tag；非法行不发布 |
11: |prepare_attention_tasks_out|device qstarts/seq_lens/slots→固定tasks/positions；后续draft从BT恢复真实位置|attention_tasks.cpp|dummy、padding孔洞、stale MTP seq_len、重复/缺失页，CPU-debug |
12: |attention_cv_out|INT2 history、BF16窗口/current→FP32分段输出/LSE；Cube QK/PV/逆旋转，Vector解包/softmax|attention_cv.cpp|Q1/2/3/4/17，GQA6、Hkv2、mixed batch、物理页置换、bad tags/metadata/NaN，CPU-debug |
13: |status_guard|同stream合并检查四组int32状态，错误触发AscendC::Trap，无D2H|status_guard.cpp|真实CPU-debug正例与故意坏status触发Trap负例 |
14: 
[...]
17: CV固定GM通信为每Cube `(256*D+4096)*4` B；Mq64同时容纳目标GQA6×MTP4=24行，历史tile跨query复用。A2的Vector→Cube需要此有界通信，总流量仍线性；不能宣称零HBM解包流量或H18字面亚线性。
18: 
19: 每个kernel头与[CV设计](cv_implementation.md)、[旋转设计](rotation_pipeline.md)、[主设计](design.md)均有D.4四问。性能目标未实测，不从压缩比或CPU调试时长推导NPU吞吐。
20: 
21: 独立NPU gates：`tools.probe_ops`、`tests/test_cv_contracts.py`、`tests/test_rotation_npu.py`（显式opt-in），随后完整TP4服务probe。NPU、graph capture/replay、32K/50K性能和模型精度分别保持未运行直到实际证据到位。

## gpt_new_oscar_kimi/docs/optimization_ledger.md
[...]
4: 
5: - 用户确认stable的APC开/关均可工作；`f96820f1`已快进同步主分支。固定stable全部vLLM参数、显式16384、原生调度器，默认APC关闭。新目标为32K/64K各自相对同参数原生端到端提速超过30%，覆盖下方历史2–4倍目标。禁止连接真机，不再请求AISBench。
6: - 用户明确接受B1作为主分支新基底并取消单项必须1.15倍的限制。按完整相关路径净收益逐项叠加，精度/协议不放宽；新设备门为不回退，最终30%不是局部倍率相加。仅用户验证后自行更新stable。
7: - 同库C65完整三臂：stable3888161、pipeline3302518、B1 3172246 ticks；B1/stable 1.22568倍，B1/pipeline 1.04107倍。1008任务/60actor/逐位及oracle通过。默认C16选择B1，q4选择已完整配对的hybrid L1，q1保留MDL、C4保留已有pipeline。B1增加47.5 MiB/rank固定workspace；此结果不含设备merge/copy，也不代表32K/64K整轮。
8: - 全库44能力CANN编译通过；CPU、CAModel、主机接缝分别记录。先前超时/ENOSPC/旧门裁决保留为历史；没有新增真机档案。详见[本轮范围与入口](stable_optimization_20261015.md)、[B1证据](../reports/c16_l1_reuse_20261015/summary.json)。
[...]
18: ### 小增量重开与metadata去重
19: 
20: - query Batch8已按用户新门重新纳入：当前Init68082→Batch864537，同库完整1.05493倍；每行FP32顺序不变，+7KiB/core Hadamard UB、GM0增量，writer Batch8仍不选。现有rotation NPU/graph门实际选择同一新源，未以本地证据标设备通过。[审查](../reports/query_batch8_reopen_20261015/independent_review.json)。
21: - mixed prepare跨FULL层复用已接candidate，并以现有arena两段分区保留short/long两张表。180项窄主机检查通过，实际任务/错误字段与层操作等价；observe新增真实NPU metadata on/off非回退门。32→2调用和96→6MiB写量只计结构工作，不领CV或模型倍率。[边界](../reports/mixed_prepare_reuse_20261015/summary.json)。
22: 
[...]
45: 三个性能候选分别有负责人，主代理统筹真实VM独占队列、兼容修复和两个一键入口；状态以完成回执为准。总目标仍为native2–4倍，当前尚未建立整轮达标证据。
46: 
47: > 2026-10-12组合门更新：单项完整路径 `t_base/t_new>=1.15`、精度/协议合格即可入组合；组合相对原生2–4倍。C4 H32→member pipeline已测1.148704倍，严格尚未达到新15%门，不向上取整；保留研究证据与必要依赖身份，待完整合并基底证据再裁决。兼容/正确性修复不要求独立速度倍率。
48: 
49: 更新：2026-10-11。按当前工作区源码和已保存报告核查；**不代表所有改动已经推送，也不代表真 NPU、graph 或整轮性能通过**。档案依据：`issue1_full_record.md` #126/#140/#145/#148/#154–156、启动文档 §0.7 与 D.4 完整日志。
50: 
51: 当前目标：65100 输入 / 512 输出 / 120 请求 / K32，相对已有 native 1342.4437259 秒实现 2–4 倍，即 335.61–671.22 秒；FULL KV 6–7 倍，同时报告全部 KV。原生 token 预算、GDN、冻结精度门不变。不同长度与低并发也须保留正确性和可用性。
52: 
53: **本轮后续进展**：已将H32＋C4 member pipeline打包为独立可测算子，并同步request-window reader、两入口共享flag、实际选核/ABI/workspace2494464B和专用成熟簇多KV NPU/图门；完整生产CANN/Torch编译通过，39项能力齐全。见[构建摘要](../reports/c4_member_pipeline_fullbuild_20261011/summary.json)与[Python接缝验证](../reports/c4_member_pipeline_python_20261011.json)。2026-10-12按新组合门收口：**已退为显式research开关，默认candidate不启用、未发布；同形H16→组合完整数据尚缺，真实NPU/图/整轮仍待认证**。专用gate固定要求完整路径至少1.15倍，既有1.148704倍不能四舍五入过门。跨请求decode流水长形仅1.137倍，暂不扩写triad；K/V连续NZ已完整测得回退并停止；当前根据多KV完整交付链研究AIC官方MDL大块装载，尚无性能通过声明。
[...]
61: - 隔离并归档日志后，candidate单臂仍在原120秒期限超时，cleanup完成、无完整数值输出。该失败原样保存在[完整证据归档](../reports/c4_b_nz_20261011/timeout-after-archive/evidence.tar.gz)，不据有限actor成功行声称完整CPU通过。
62: - 四个最终publisher方法逐字提取的独立CPU门已通过：history旧lane16与precise16各131072个K/V原始word、±0/NaN/Inf/subnormal/空间标签、输入不变和双guards。它只证明新增布局接缝，不证明完整C4、NPU或速度。
63: - 原`cv_replay.py`完整CPU前置门保持不变。新的**研究入口**`cv_replay_publisher.py`明确要求已成功的baseline完整CPU/真实prepare加独立publisher CPU门；完整candidate CPU仍标未完成。该入口在原600秒期限内完成两臂，完整输出/独立oracle/全部1008任务与状态/60actor门通过：**1608607→1743703 ticks，0.92252倍（慢约8.4%）**。已明确否决这个B-only完整版本，不进组合；[配对结果](../reports/c4_b_nz_20261011/completed/reports/camodel-valid/comparison.json)。没有更改冻结精度、生产探针或将CPU超时重标为成功。
64: - **Vᵀ-NZ也已完成并退出组合**：同库Q336/C337/S1/20core，**1610898→1734415 ticks，0.92878倍（慢约7.67%）**。两臂在600秒期限内rc0、cleanup完成；完整CAModel逐位/独立oracle/1008任务/60actor通过，publisher CPU原始位与guards通过；**完整candidate CPU未运行**。更少V发布burst没有转成完整核提速，未测分相位归因，不把回退武断归到单一Gather/DMA成本。[Vᵀ裁决](../reports/c4_b_nz_vt_20261011/decision.json)、[配对](../reports/c4_b_nz_vt_20261011/reports/vt-camodel-valid/comparison.json)。B-only的[裁决](../reports/c4_b_nz_20261011/decision.json)、CPU超时与全部原失败继续保留。
65: - 当前A2/CANN公开`DataCopyUB2L1Impl`及`DataCopyUB2L1ND2NZImpl`在AIV侧通过GM workspace软件模拟：先`copy_ubuf_to_gm`，再发送GM→L1消息，不能据API名字申领无GM直通收益。[SDK源码123–213行](../artifacts/cann_sdk_cube_public_20261010/impl/basic_api/dav_c220/kernel_operator_data_copy_impl.h)。**仅K/V的L1复用仍单独审查**，其可行性、所有权和净收益未定；两次布局回退不构成对该方向的否定。以上都是本机研究证据，NPU、graph与整轮目标未验收。
[...]
75: ## 一、当前 candidate 已存在的路径
76: 
77: | 方案、当前代码 | 结果与精度范围 / 收益分母 | 启用与组合边界 | 证据 |
78: | --- | --- | --- | --- |
79: | SIMD INT2 pack + Hadamard Init；`csrc/kernels/rotate_clip_store_striped.cpp`、`striped_store_pack.h`、`hadamard_indices.h` | 完整 writer 同库 old **173419** → pack **136213** → pack+Init **96566** ticks；old→组合 **1.79586×**。CPU 完整字节、oracle、guard；CANN/扩展完整编译，request-packed 接缝 CPU 通过 | **本地生产源已接入** striped writer；`rotate_clip_store_request_packed.cpp` 同步包含两项。Init 是 pack 后额外收益，不再另乘 Init helper 的 7.112×。Q优化改走独立可选算子，canonical FE0源码保持冻结；见下项当前选择 | [三臂完整 writer](../reports/quant_store_simd_pack_20261010/comparison.json)、[生产接缝](../reports/quant_production_integration_20261010/integration-summary.json)、[Init helper](../reports/quant_hadamard_indices_20261009/summary.json) |
80: | q4/q1 decode bundle；`attention_cv_decode_bundle.cpp`、`attention_striped_unpack_padded.h` | 包含 HalfKv64、两块有界 KV 流水、精确窗口批量读、区间 mask 等。完整合成 K32 / 20–30K / q4 对旧 striped SIMD：**16290667→9589788，1.69875×**，全部 tasks/source、partial/LSE/status 逐位、两臂独立 oracle | **candidate 已选择**；该组合内各单项不能再次计入新增收益。此长 q4 结果不是完整 K32 q1 或整轮目标证据 | [完整 q4 配对](../reports/decode_integrated_batch32_retry_after_oom_20261007/q4_r32_n128_20to30k_s3-comparison.json)、[交付索引](../reports/decode_candidate_delivery_20261007.json) |
81: | history C4/C16 复用、natural V 发布；`attention_cv_window_range_cluster4.cpp` 等、`ops/cv_dispatch.py` | 当前 C4 仍 HalfKv16；自然 `[KV,D]` V 配合非转置 PV，已消除旧 ND V 转置 Gather/散写。C16 仅 max_query_len≥8192 路由；不能把 native 小 chunk 当作 C16 | **candidate 已存在**。旧 natural V 收益不是新的 NZ 发布收益。C4/C16 与新 H32/pipeline 改同一 reader，须形成单一派生链 | [历史复用](history_reuse_experiment.md)、[mixed 路由](mixed_cv_optimization.md)、档案 #144/#150–154 |
[...]
84: ## 二、正收益路线的当前选择与历史记录
85: 
86: | 方案、当前代码 | 已有结果与精度范围 / 分母 | 生产与组合依赖、剩余门 | 证据 |
87: | --- | --- | --- | --- |
88: | canonical Q Hadamard Init + Batch8；`experiments/hadamard_batch8/rotate_init.cpp`、`rotate_batch.cpp` | 同库完整 N128/H6/D256 Q rotate：old **110343** → Init **68082** → Batch8 **64537**；old→最终 **1.70976×**，Init 后 Batch8 仍 **1.05493×**。输出/status 位一致；7 个 CPU 边界覆盖 D64/128/256、1/7/8/9 行、padding、±0/nonfinite | **当前只选Init，完整1.62074×；Batch8额外5.5%不列本次组合**。**本地已完成**独立`rotate_vector_init.cpp` / `rotate_vector_init_out`映射及源反向恢复；共享candidate开关已选此算子，canonical FE0与原ABI保持。未发布，fresh build/CPU seam/NPU/graph待验：[当前集成报告](../reports/quantization_bundle_integration_20261011.json) | [三臂完整 rotate](../reports/hadamard_batch8_20261010/reports/batch8-rotate-camodel128-v2/comparison.json)、[范围汇总](../reports/hadamard_batch8_20261010/summary.json) |
89: | writer Batch8；同目录 `writer_batch.cpp` | **已含 pack+Init** 的 current **95930** → Batch8 **92403**，完整 writer 净 **1.03817×**；CPU 两例完整字节/oracle/guards 通过 | **历史正收益，本次不交付**。3.8%增量过小；临时本地Batch8映射**已撤回**到已测pack+Init原快照，request-packed已同步重生；未发布/fresh build待验。保留原完整数值证据；禁止用另一库的旧96566与新92403拼倍率 | [完整 writer 配对](../reports/hadamard_batch8_20261010/reports/batch8-writer-camodel128/comparison.json) |
90: | C4 H32 padded unpack；`experiments/c4_unpack32/` | 193 helper CPU 用例逐位/oracle/guards；helper **98478→41974，2.34617×**。完整 Q336/C113 C4 **1355015→1346984，仅1.00596×**；CPU valid/bad80/bad96 全位一致 | **仅作下项pipeline必要依赖，未启用**。不单独交付/计入2.346× helper收益；保留旧 alternating16-row lane错误归属与Softmax scratch可见容量 | [helper](../reports/quant_unpack32_20261010/comparison.json)、[完整 C4](../reports/quant_unpack32_20261010/full_c4_camodel_comparison.json) |
91: | C4 member pipeline + atomic accState；`experiments/c4_member_pipeline/` | **两臂均已 H32**；完整 Q336/C337/R1/S1/20core、全部1008任务/source0+1：**1849738→1610282，1.14870×**。CPU C113/C337/bad336 全位；atomic v3 即时回读及 atomic→normal 也已通过 CPU/CAModel | **显式research，默认candidate不启用、未发布**。1.148704严格低于1.15门，不能向上取整；增量在H32之上，不能乘helper2.346，也不能跨C113/C337乘1.00596。新增640KiB/core；原C1/precise路径不变，NPU/graph/长形仍待组合门 | [完整核配对](../reports/c4_member_pipeline_20261010/reports/c4-pipeline-camodel337/comparison.json)、[bad336](../reports/c4_member_pipeline_20261010/reports/c4-pipeline-cpu-bad336/comparison.json)、[atomic](../reports/c4_atomic_state_recovery_20261010/summary.json) |
92: | static Matmul 配置；`experiments/decode_static_matmul/` | 完整 q4/R1/C20000/S3 在 history-pipeline 基底上 **2464632→2426161，1.01586×**；partial/LSE/status 逐位、两臂 oracle | **历史正收益，本次不交付**。1.6%增量过小；不是精度失败。若改用低层K-major将被替代，不能同时记两项收益 | [配对](../reports/decode_static_long_camodel_20261007/comparison.json) |
93: | active/identity writer；`experiments/active_identity_store/` | q1 identity 完整 writer 局部 **8.56288×**；已有835fc22片段中两次 q1 store 只占步 **0.266%**，不是当前整轮占比 | **历史备用，未列当前交付**。Hadamard和identity分支互补，但现有整步贡献证据小；identity的finite/±0/status不能未经资格直接用拷贝替换，暂不重跑同一micro | [完整 q1](../reports/active_identity_store_camodel_20261006/n128_h1_d256_bf16_b128_decode_q1_identity-g16-comparison.json)、[旧片段范围](../reports/active_identity_store_decode_cost_20261006.json) |
94: | 按实际短分区选 split；尚为方案，当前仍保留原 `cv_shape_tokens` | 源码确认小 R 可偏载。naive actual-N 的 q4 R5/N20 会 S20，不是 S4；同一条件预算含16层长 C4+短 q4+2次q1，长后缀 context63K 仅约1.038×（q1系数是假设） | **保留结构分析，未列当前交付/未实现/未测速度**。必须权衡新增task/merge固定成本、短context、split归约误差；不能用“5核变20核”冒充整步4×。预算不是实测正收益 | [全 mixed 条件预算](../reports/mixed_actual_split_budget_20261010.json) |
95: 
[...]
104: | 完整C4 B-NZ / Vᵀ-NZ；`experiments/c4_b_nz/`、`c4_b_nz_vt/` | 同库各自配对：B **1608607→1743703**（慢8.40%）；Vᵀ **1610898→1734415**（慢7.67%）。两例CAModel完整逐位/独立oracle/1008tasks/60actors通过，真实K/V publisher已计时，Rv一次256KiB位pack未计时 | **两版本均退出组合、未启用生产**。B完整candidate CPU仍120秒超时；Vᵀ完整candidate CPU未运行；两者publisher CPU通过。不能写成全CPU门完成，也不能跨库把两候选互相拼倍率 | [B裁决](../reports/c4_b_nz_20261011/decision.json)、[Vᵀ裁决](../reports/c4_b_nz_vt_20261011/decision.json) |
105: | 仅K/V的L1复用；另行只读审查 | 当前公开UB→L1接口经GM软件模拟，不能宣称无GM直通；Cube内已有K/V的L1复用是另一项资源/生命周期问题 | **未验证、未否决、未启用**。待确认实际可复用数据、L1容量、跨成员所有权和完整净收益；不重跑已回退的两个布局版本 | [SDK接口](../artifacts/cann_sdk_cube_public_20261010/impl/basic_api/dav_c220/kernel_operator_data_copy_impl.h)、[当前决策](quant_dequant_next_decision_20261011.md) |
106: | FP32 K-major低层Matmul；`experiments/fp32_kmajor_matmul/` | 当前独立源码与有限fixture；初始事件冲突、v2 PV的FMATRIX协议错误已修。v3 CPU/CAModel三例有限输入配对位、oracle与每输出K128顺序通过；qk24/cancel **13943→12557，1.11038×**，PV126 **18975→25853，0.73396×**。**本版本PV明显回退，不入组合、不扩形状**；根因仍查完整trace，不归咎精度。[完整配对](../reports/kmajor_20261011/v3/reports/kmajor-v3-camodel-v2/comparison.json)。针对真实重复A的L1→L0加载；全NZ L1、K外/N内/独立M64和M62，保持每输出K128顺序/HF32off/small-M屏障 | **未启用**。在NZ基底上评估增量，不再重复记ND2NZ收益。使用独立L1/L0资源、不与MatmulImpl共占；whole128 ZA子视图未证，首版改两次独立Load3D。预pack仍免费上限，之后须接完整publisher与attention | [独立原型](../csrc/experiments/fp32_kmajor_matmul/)、[API可行性](fp32_manual_matmul_feasibility_20261010.md) |
107: | C4尾波按代价拆回原C1；只读候选 | 当前R1/Hkv1/GQA6/S1条件下Q2048有21成熟簇，个别core两簇；Q1924无同样尾波，Q8192全拆会变慢。对当前pipeline用A/C1、B/C4和固定成本参数式，理想1.5×需`B≥A+F+3P` | **未实现/未测**；增加KV展开与总工作，必须以完整关键路径净收益选择，不能拿旧条件1.62×当新组合性能 | [尾波预算](c4_tail_wave_budget_20261011.md)、[大矩阵合并暂缓](c4_wide_matmul_feasibility_20261011.md) |
108: | 同core跨独立request流水；`experiments/decode_task_overlap/` | v1两UB状态/两GM上下文、相同轮数不同request配对已实现；CPU/CANN编译及q4/q1两请求短形逐位/oracle通过。完整短q4 **810475→775979，1.04445×**；完整31KV长q4 **3351197→2948283，1.13666×**，两臂完整位/oracle/task/actor通过；长CPU120秒未完成单列。K32实际prepare表配对80/96 history tasks | **独立研究，暂不入组合或扩写triad**。长形完整净收益不足以支撑旧条件1.56倍；不同轮数和奇数triad只有协议。需新的明显净贡献证据再增加复杂调度；不把局部13.7%变成整轮目标 | [实际裁决](../reports/decode_task_overlap_20261011/decision.json)、[执行记录](../csrc/experiments/decode_task_overlap/README.md)、[旧条件预算](../reports/roi_decode_overlap_20261010.json) |
109: 
110: Kt/Vt共同连续NZ发布的新实验：`experiments/c4_kvt_nz/`将K也改为物理`[D,KV]`/NZ，QK用非转置B、PV用转置B，K128/FP32归约维度保持。每完整KV发布528块→32连续块，新增64次index Cast仍在核内计费；UB182336→165952B。CPU/CANN编译、history/precise各131072原始word及guards通过；**完整C337配对逐位/oracle/1008任务/60actor通过，但1612253→1723131，慢6.88%，v1不入组合**。基线仍ND H32+pipeline；完整候选CPU未跑，旧B-only CPU超时保留。[实际裁决](../reports/c4_kvt_nz_20261011/decision.json)。后续uint32索引常驻UB版本也已完成：1611590→1709129，慢6.05%；精度/全部任务/actor通过，仍退出组合。移除转换没有扭转完整核退化，因此暂不继续扩展NZ布局。[原型与预声明门](../csrc/experiments/c4_kvt_nz/README.md)
111: 
112: ## 四、明确失败、受限或曾被误判的路线
[...]
115: | --- | --- | --- |
116: | A2 L2 `NORMAL` / `PERSISTENT` 参数微调 | **源码筛选排除当前调参方案，未改生产** | `GlobalTensor`默认NORMAL，当前work无显式bypass；所读A2设备分支仅DISABLE改变地址，PERSISTENT/LAST不提供新驻留行为。约8GiB是累计GM访问、非实测HBM；现CAModel L2关闭，真机命中率/回写未知，未猜L2容量。仅K/V的L1复用独立待审查；附录同时记录Python链路无大整区复制及merge FP32中转字节上限：[缓存与复制审计](../reports/quant_cache_policy_audit_20261011.json) |
117: | 双BF16残差＋三项补偿 | **只读筛选后暂缓，未实现/未数值否定** | 三次完整BF16 Matmul的条件成本已高于FP32；融合版改变累加链且需增加分解/重组/同步，尚无完整精度与明显净收益证据。只有实际融合成本和冻结数值资格同时成立才重开：[具体边界](dual_bf16_residual_feasibility_20261011.md) |
118: | 无条件BF16输入代替FP32历史；FP16 PR prefill dtype链 | **数值否定，生产未改** | FP32累加不能补回输入cast丢失；single-BF16有效值反例误差0.09267>冻结门；PR dtype链7个store可达stress失败。不得换oracle或放宽门：[BF16反例](../reports/single_bf16_cast_counterexample_20261009.json)、[prefill反例](../reports/prefill_tile_stress_20260930.json)。FP32/BF16两个可精确表示微形状的1.213/1.326×只是诊断：[dtype实测](../reports/fp32_bf16_mmad_ratio_20261010/decision.json) |
119: | M32/N128/K64 tiling消小M barrier | **当前具体方案已测回退，未启用** | 同形完整marked QK24 20724→27856，慢34.41%，虽8个BAR归零。不是禁止所有未来tiling：[原始裁决](../reports/decode_mmad_barrier_20261010/decision.json)。不要直接删SDK规定的小M屏障 |
[...]
130: | C4 Q1344/C769 normal 900s超时 | cleanup完成但无完成输出；不得取局部ticks或说数学已错。后续Q336是明确缩小的诊断点，不代表K32/2K饱和：[失败索引](../reports/c4_phase_profile_c769_20261009/summary.json) |
131: | Q336 C4 profile两个AIV末尾64MiB截断 | 整trace门仍失败；数值完成与有限闭合循环单列，不补finalize： [范围说明](../reports/c4_phase_profile_q336_20261009/partial_diagnostic_summary.json) |
132: | Batch8主query CPU日志填满tmpfs | 失败完整保留；不能伪称CPU主形通过。7个小边界CPU与后来完整query CAModel是独立证据：[汇总](../reports/hadamard_batch8_20261010/summary.json) |
133: | C4 CPU比较器误判bash-wrapper fixture路径 | 不重跑算子；严格解析受控exec、核prepared metadata/tasks/positions修复后另存verified报告，旧失败comparison保留：[修复后资格](../reports/c4_member_pipeline_20261010/comparison-cpu113-verified.json) |
134: | K-major 首例 CPU 初始 `M_MTE1(0)` 报 `set twice consecutively` | **本机CPU协议错误，数学尚未开始，不是真机条目或数值回归。** 真SDK `TPipe::Init` 在 arch2201 AIC 已 Alloc+Set 0/1/2（97–111行），析构会 Wait+Release（533–539）；不是前一 ICPU_RUN 污染，TBuf Init 本身未分配事件。自有3个free及2个ready必须逐个 `AllocEventID`，完成配对drain后 `ReleaseEventID`，不触碰TPipe保留0/1/2；`FetchEventID`不置占用位，不能连续Fetch充当并发槽。原CPU失败证据保留，修复后的完成另验；[SDK定义](../artifacts/cann_sdk_cube_public_20261010/impl/basic_api/kernel_tpipe_impl.h) |
[...]
150: - **Prefix caching 必需兼容**：修复显式配置未传到原生服务、开启时无必要地禁止 mixed decode split 两处源码缺口；用户追加后所有服务入口默认显式prefix=true，主动false诊断保留；native/baseline/candidate一致。188项主机生命周期/入口/分流检查通过，包括实际原生hash/共享/refcount/驱逐和正context的main/first-MTP；NPU、图与真实服务命中仍未验收。用户未提供错误栈，不能把两处源码问题认作其未知错误的根因。请求sidecar研究路径仍未具备跨请求prefix恢复，不默认启用。[实现和边界](prefix_caching_compatibility.md)、[host报告](../reports/prefix_caching_host_20261012.json)。
151: - **完整decode交付时序**：现有源d817的QK/PV方法提交标记后仍有MMAD/FIX执行。小型R2/q4/C1341、4完整KV+尾行的6文件完整completion/popped已完成：normal1072361/profile1093991 ticks，扰动2.017%，全部数学逐位/oracle与3actor通过。中间完整轮PV周期约44K，QK/PV结果交付约86.5%，softmax与P交接约13.5%，KV供给暴露等待为0；仅本小形，不是NPU或整轮占比。下一主线审查AIC B块ND2NZ装载的串行暴露，不重复AIV NZ发布失败路径。[当前审计](../reports/decode_cost_audit_20261012.md)。
152: - **一侧BF16残差＋仿射码值**：2/3分量在完整原空间identity抵消用例均超冻结门；三分量输入重构残差0仍失败，停止该具体算法，不泛化所有BF16路径。新增3倍MAC、仅减少22.37%逻辑GM工作，普通用例通过不能覆盖抵消失败。逆旋转后移只有约0.585%矩阵工作上界，GQA6跨head共享已存在，均不作为主线收益。[结构筛选](../reports/decode_structure_screen_20261012.md)、[CPU证据](../reports/affine_bf16_residual_screen_20261012.json)。
153: 
154: - **实际dequant FP32值的BF16平面积**：与仿射码值方案分开筛查。2×2/3×2在4个CPU完整oracle用例通过（含identity抵消），不代表普适精度。4/6倍MAC、理想GM增加23.7%/43.4%；已有同形完整Matmul FP32/BF16仅1.213/1.326倍，暂无明显净收益支持，未入组合。合法FP16 metadata不保证两BF16平面精确的表示反例已记录。[筛选](../reports/dequant_bf16_product_screen_20261012.json)。
155: 
156: - **默认APC align容量重新核算**：当前条件参考几何、65615 tokens、无共享时FULL2.96552×，计原生5页GDN峰值预留后全部KV2.29545×。工具已支持新默认并执行7项主机规则测试；未测HBM，6–7×仍待实现兼容APC的新布局，不能沿用none投影。[报告](../reports/memory_64k_prefix_align_20261012.json)。

## gpt_new_oscar_kimi/docs/performance_findings_2026-09-23.md
[...]
1: # 2026-09-23 长上下文并发性能实测判读
2: 
3: **状态：现有证据复核；尚未进行本轮新 NPU 测量，性能问题尚未解决，精度与性能均未验收。** 本文区分客户端墙钟、vLLM 周期日志、worker 心跳和带同步的设备归因。20–30K 输入长度、32 并发与“同一数据集”均是用户对其自有压测程序的陈述；项目没有该数据集或其逐请求记录。历史故障约束见档案 #70–#73、#130–#139；旧标题和索引行号有漂移，下列行号按当前条目标题定位。
4: 
5: ## 证据位置与适用范围
[...]
27: ### 静态工作量模型（仅代码推导，非 NPU 实测）
28: 
29: 当前目标 TP rank 的 GQA=6；CV 的 query tile 为 `floor(64/6)=10` 个 query token，KV tile 为 32 token（`csrc/kernels/attention_cv.cpp:55,137–145`；`docs/cv_implementation.md:47–53`）。对 16,384-token 首次 prefill，仓库的源代码调度分析报告给出 **420,761 个 current-source query×KV tile 对/主模型 FULL 层**（`reports/prefill_work_analysis.json`；`docs/design.md:149–151`）。每对在当前 Cube 路径执行 QK 与 PV 两次 matmul（`csrc/kernels/attention_cv.cpp:206–216`）；按主模型 16 个 FULL 层计算约 **6,732,176 对、13,464,352 次 matmul 调用**，不包括其他 source、旋转、store、GDN 或 MTP draft。20–30K 输入的因果扫描工作量更高，但实际分块、窗口和并发形状需逐步记录。这个数量级说明 CV 是值得优先验证的**结构性候选**；每对真实设备时延、CV 总占比以及优化后的加速比均不能从静态计数推出。
30: 
31: ## 当前可下的判断及边界
[...]
34: 2. **CV attention 是最强的既有设备侧线索。** 当前 `impl.py` 中相位名 `fia` 包住的是自研 `attention_cv_out`，不是原生 FIA。#132 的 host enqueue 背压不能分清设备内核；#134/#135 的独立 debug-sync 将主要同步时间归于该相位。生产运行是否仍由同一内核主导、其成本如何随请求数和历史长度变化，需本轮配对设备测量。档案 `issue1_full_record.md:28168–28283`；历史禁止全历史恢复见 #70–#73 与启动文档附录 D.4。
35: 3. **K=1→4 的约 4 倍 makespan 不能证明 CV 串行、调度器只处理一个请求或解码无扩展。** 当前 `max_num_batched_tokens=16384` 正好等于每条阶梯输入长度；四条输入至少需要四个满额 prefill token 预算的调度步，即使每步执行完全正常，总输入工作量也为四倍。A:7–27,62–63；`configs/target.json:12`。K=4 日志明确已有 2–4 个 Running（A:39,45,52）。要区分原因，必须记录每步实际调度的 prefill/decode token、请求数、设备执行与 host 等待。
36: 4. **不能据现有日志给出单请求 25K prefill 倍率、解码倍率、精度结论或内核级绝对时间。** 两份真实负载日志没有对应 request ID、到达/首 token/结束时间、实际 prompt/output usage；阶梯使用 `/v1/completions`（A:16,58–61），用户负载使用 `/v1/chat/completions`（B:7,14–47），且两次用户负载测试相隔约 16 天，版本和请求发送节奏未在附件中核对。两侧均出现 ArgSort AiCPU 告警（B:49–52,144–147）及原生 rejection sampler 的 fallback 警告（B:9,98），不能据此归因 OSCAR 增量。两侧 KV 使用率的容量分母不同，也不能把 7% 与 95% 直接解释为处理 token 比例。OSCAR 的 MTP 接受率日志仅含每段几次 draft（B:56,63,66），样本太小；HTTP 200 亦不证明模型质量。档案 #130/#137 `issue1_full_record.md:27980–28135,28303–28324` 中更强的归因表述应以本段边界为准。
37: 
38: ## 配对真机诊断决策树
39: 
40: 被动观测直接配合用户现有压测程序：项目采集服务端日志、`/metrics` 累计计数器、Running/Waiting 与 worker 相位信息，不生成压测输入。若该客户端可导出同一请求序列、到达时刻、token usage 与流式时间戳，才做严格逐请求配对；否则只比较可观测的服务端聚合量及其条件差异，逐请求 TTFT/TPOT 标“未测”。对照运行需保持同一模型、TP=4、MTP、图模式、`max_num_batched_tokens=16384` 与 API 路径，并记录代码版本、设备、OSCAR 旋转文件和 prefix hit。预热和重复次数按 `configs/acceptance.json:10` 的 2/5 及逐工况中位数要求执行。正式验收仍覆盖 `configs/acceptance.json:11–13` 的全部必测长度、并发和 q_len。#136 `issue1_full_record.md:28284–28302` 提醒探针报告与相位账本不能同名；#139 `issue1_full_record.md:28345–28351` 的阶梯快路径仅供诊断，不代替全服务与性能验收。
41: 
42: | 问题与控制工况 | 同时采集 | 如果出现的现象 → 下一步 |
[...]
48: 生产模式计时不得插入同步并把该结果当作吞吐对照。`OSCAR_DEBUG_SYNC=1` 只在单独的定位运行中使用；档案 #133 `issue1_full_record.md:28198–28225` 已记录目标栈通过 `/start_profile`、`/stop_profile` 导出时四 rank worker 崩溃，不能默认恢复该测量路径。设备事件若无可验证的完整记录，应标记为“未测”，不能用 host enqueue 或心跳墙钟代替。
49: 
50: ## 精度门与交付状态
51: 
52: 任何性能优化须保持真实 OSCAR INT2、CV、旋转、窗口、MTP 与图路径，并先通过独立 oracle 和 `configs/acceptance.json:5–9` 的冻结门：pack/unpack 位级精确、store↔dequant `atol/rtol=0.002`、fused attention `0.005`、prefill/window relative L2 `<0.02`、参考 staging eviction `0.0001`。逐工况比较原生性能必须遵守 `configs/acceptance.json:10–15`，不能放宽阈值或以均值掩盖慢项。模型级 logits/任务指标/MTP 接受率容差目前仍为 `null`（`configs/acceptance.json:14`）；必须在测量前定义并冻结，当前不能宣称模型质量已通过。图捕获、图回放、设备完成、质量、容量与性能分别记录。
53: 
54: 本文初稿只复核此前附件和档案；当时**未完成新的配对 NPU 运行，未证明任何性能修复**。后续同日真机配对结果补记如下。

## gpt_new_oscar_kimi/docs/prefix_caching_compatibility.md
[...]
50: ### 最小正确数据协议
51: 
52: 1. **不可变 checkpoint 与运行窗口分开**：可共享 prefix 由原生完整 FULL page/hash拥有不可变原始BF16窗口；请求私有 sidecar只保存本请求当前窗口。Checkpoint身份必须包括层/模型/旋转/布局版本、原生prefix-chain hash、物理page ID、allocation generation、logical end。request ID不能作为共享前缀身份。
53: 2. **只发布已提交边界**：完整FULL页末尾且原生已提交到该位置，才可使checkpoint有效。MTP尚未接受的写不能发布为可共享前缀。来源必须是原始BF16 current K/V或仍精确的旧窗口；禁止从INT2补回。跨越多个边界的长prefill必须在覆盖每个待发布边界时取其窗口，不能事后从最新ring寻找已覆盖的数据。
54: 3. **命中恢复**：在native FULL/GDN共同命中后、第一次读取窗口前，把该checkpoint的sink及recent+spec原始字节复制到新lease的sidecar。目标tag用新lease epoch重新编码；不能复制来源请求的epoch。每层最大323行（当前S64/R256/M3），与历史长度无关。任一source generation/tag缺失即失败，不能用zero或解量化补齐。
55: 4. **物理生命周期**：prefix查询与`touch`保留原生页refcount，restore ticket另保留checkpoint读引用。释放请求sidecar不删除共享checkpoint。native eviction/重分配更新generation且撤销旧hash/record；旧ticket或graph未完成时不得重用其checkpoint字节。reset先撤销可命中目录，再按原生running/reset规则排空/取消，之后允许复用；epoch不能回绕。
56: 5. **设备/图顺序**：writer写BF16内容→publish checkpoint generation/ready→同stream或明确event依赖→restore校验并复制→发布目标tag→attention。host enqueue或CPU协议通过都不证明这个顺序成立。固定restore描述符、lease map、buffer地址必须覆盖batch重排/多请求同时hit/MTP接受位置变化。若restore放在graph外，也必须在graph读取同sidecar前完成且遵守native输入准备事件。
57: 6. **scope一致性**：所有target FULL和draft FULL层的checkpoint及原生GDN状态必须对应同一最终命中长度与同一权重/旋转/布局版本。LoRA/cache_salt等身份继续通过原生prefix-chain hash，不可自创简化prompt hash。
58: 
59: ### 容量不能漏记checkpoint
[...]
109: 4. 在前一轮设备完成后模拟私有页释放再利用，用真实writer写入不同owner内容，再在同一graph中改metadata读回；此步骤检验存储复用，原生allocator/refcount规则仍由独立host合约验证。
110: 
111: 该门使用identity旋转隔离存储生命周期，实际Hadamard及其数值/性能由现有MDL/旋转门负责；不能把它说成全模型APC或原生GDN/MTP端到端运行。报告绑定算子源码/产物，设备完成、graph与精度分别标记，缺真实NPU必须失败。新增8项focused host测试通过；**新增NPU门尚未运行，模型级APC/质量/整轮2–4倍收益仍未验收**。这是正确性门，不领取性能倍率。

## gpt_new_oscar_kimi/docs/profiling.md
[...]
43: `tools/summarize_profile.py` 仅统计有NPU硬件process/设备属性/AI_CORE等明确证据的完整device事件。CPU包装函数即使同名`oscar_attention_cv_kernel`也不计设备时间。通过下列证据归因：
44: 
45: 1. 可识别真实device kernel名：prepare、rotation、CV、merge、store、guard；graph replay没有重新执行Python时仍能归因。
46: 2. trace显式flow将host record_function连接到device kernel。
47: 3. 唯一明确的correlation id连接host launch scope与device kernel。

## gpt_new_oscar_kimi/docs/q4_diagnostic.md
[...]
9: 同一离线随机输入回调分别填充原生BF16 cache和原有OSCAR INT2 fixture，物理页各自独立。原生页表用满足该诊断的最小合法列数，明确标为`minimal_legal_synthetic_width_not_service_stride`，不伪称原生hybrid服务的物理页/表宽完全复刻。
10: 
11: - 原生输出对BF16因果dense oracle；默认不产出LSE，单元素LSE占位不作精度证据。
12: - OSCAR输出对独立INT2/精确窗口oracle；两种缓存数学不同，不要求native与OSCAR彼此逐位相等。
13: - mask、workspace、输出、缓存、量化与任务全部在测速前准备。2次预热、5次交替Event，分别记录native FIA、OSCAR CV、CV+merge。每次测量完成后检查输出/状态，验证不计入事件区间。
14: - 原生主模型权重、GDN、旋转/store准备及全模型图均不在这些区间内。测得差距用于定位，不表示服务速度门已通过，不能直接乘16层变成实测图耗时。
15: 
16: ## 独立内部打点
17: 
18: `attention_cv_profile_out`是fe0数学的独立诊断副本，不进入生产路由。profile tensor为int64 `[Cube数,3引擎,4来源,24字段]`，64B对齐且各引擎独占cacheline；来源为history/window/current/total。记录query准备、packed读取、unpack、精确源读取、GM发布、QK/PV计算与等待、归一化/旋转/输出等。
19: 
20: 时钟为NPU原始SYS_CNT。诊断额外使用局部MTE2_S/V_S/MTE3_S/FIX_S完成栅栏，改变流水重叠；每个字段只能解释为插桩下该核/引擎的局部跨度。不能把跨核最大值相加成wall。unpack的bits/meta字段是子项，不能再与unpack_total相加；AIV rotation_wait属于finalize，AIC该等待是独立阶段。field23从该引擎Init开始到Process末、排除计数发布，不是完整kernel Event。
21: 
22: 新symbol先单独预热2次，再测一次profile Event，明确报告其相对正常CV中位数的扰动。profile及其预热都必须与未插桩fe0的全部partial/LSE/status逐位一致。正常CV和native FIA时间来自未插桩路径。

## gpt_new_oscar_kimi/docs/quant_dequant_remaining_redundancy_20261010.md
[...]
9: | 同位置draft重写K/V | 首draft来自新的target_hidden_states（native proposer:769–776），后续来自前一draft hidden/input token；writer位置相同不能证明输入相同 | 不能按已有tag跳过量化，尤其拒绝/重算后。先算量化再比较bytes不能省该量化成本 |
10: | C4簇之间重读相同历史 | `attention_cv_window_range_cluster4.cpp:328–353,901–910`每个成熟同域cluster重新解包；簇内4成员复用已存在，不能再次计收益。默认Q2048/S1有21簇，跨簇确有重复 | 理想去重最多把这些簇的解包从21份变1份，但QK/PV/softmax不减少；跨core消费者需有界生产/消费同步。已存闭合full256轮53896cycles KV准备/390694总轮，假定其他不变且KV准备全部免费也只1.160×该轮；不是长history全核上界。新pipeline已有nextKV重叠，不预记第二份收益。当前不值得单独做复杂全core共享 |
11: | draft identity Q/K/V旋转 | `runtime.py:668–681`显式identity且hadamard=False；canonical `rotate_clip_store.cpp:103–113`与striped `113–125`仍逐256列Mul/ReduceSum；cache_storage_ops无identity路由 | 数学冗余确实活跃，已有研究非生产。旧完整q1 writer8.563×不能套当前整步；历史835fc22片段两个q1 store仅1.138ms/428.101ms，即全消失仅1.00267×该步。保留为已知未接入项，不重跑小收益单点 |
12: | target Hadamard元数据与逐row屏障 | `impl.py:161–163`仍canonical rotate_out；canonical Init仍4096scalar写。striped writer只改了Init/pack，Transform仍逐row8stage | 紧凑stage-major原型是新增候选：保持每row算术、indices/sign16KiB，work增7KiB；满8行调用200→137、屏障200→25。完整writer当前96566ticks需净省32189才1.5，尚无内部Transform占比。详见`csrc/experiments/hadamard_batch8/README.md`；不拿次数当速度 |
13: | 每history split的最后Rv旋转 | `attention_cv_decode_bundle.cpp:695–698`每split执行密集Cube旋转。指定PR `triton_oscar_decode.py:5–13,254–270,336`是先合split，caller再逆旋转 | 实数线性可移到split合并后，但FP32顺序与现有partial/merge契约变化；不能假定逐位等价。S3最多省2/3该固定旋转，长history相对占比下降，没有大收益证据，暂不改 |
14: 
15: ## 已有优化明确剔除
[...]
17: q4/q1已是HalfKv64 padded unpack、单task next-KV预取；C4内四member已共享一次解包；H32完整短C4只有1.006×，不能重复报helper2.346×；writerSIMD pack和向量Init已进入本地candidate；first-draft current-only和native current FIA已存在。later-MTP compact在`compact_later_mtp.py:26–29,130–158`仅N≥1024且N≥8B时启用，不能再拿旧16K×2后续draft全padding当新收益；N128短路径仍有padding，但旧active-only writer样本仅1.001×，不据此追加新核。
18: 
19: ## 精度边界
20: 
21: dequant缓存必须绑定真实layer、request/epoch、physical page与写代际，保持FP16 metadata舍入→FP32 Mul/Add；不同请求/不同层不共享值。C4跨簇仅同KV域可共享，不能把宽域非法metadata错误传播给窄域C1。batch8仅改独立row调度，跨管道所有权屏障保留；identity若未来单独处理，finite/NaN/Inf/±0/subnormal和padding/status必须完整资格，不能把hadamard=False推断为identity。
22: 
23: 以上均无“FULL字节比→吞吐”的乘数；没有用旧片段推断当前全程占比。

## gpt_new_oscar_kimi/docs/quant_dequant_roofline_20261011.md
[...]
37: `有效输出吞吐 = B*a/T_step`。如果上述反量化、临时流量、FP32计算与同步使`T_step`随B近线性增加，更大batch的吞吐收益会被吃掉；若每步增长更快或a下降，还会变慢。**这解释了机制，但目前未证明其中哪项占真实整步的主要比例。** 下一步的决定性证据必须区分这几项的暴露成本，并在完整相关路径验证删除该成本后的净变化。
38: 
39: 当前优先主线是压缩域到计算单元的数据流和解包/消费成本。仅改变格式或隐藏局部等待已不能据此宣称解决：双请求流水长形约1.137倍，Kt/Vt-u32完整C4仍约6.1%回退；它们保留为局部证据，没有进入新增组合。已有writer/旋转/C4组合保持各自验收边界；不将小比例相乘包装成2–4倍。整数/仿射BF16分量路线已有完整原空间反例；先保留真实dequant值的BF16积方案在有限CPU样例通过，但成本不支持当前纳入。
40: 
41: ## 1. 明确采用组合方式提速
42: 
43: 本轮采用组合优化：量化写入、反量化与数据布局、历史复用/任务执行、紧凑 FULL KV 协同减少完整路径成本。单项有收益仍须核实它在当前组合中的**新增净贡献**；过小单项保留记录和重开条件，不装入当前组合。组合必须在同一母源、缓存格式、ABI、调度预算和冻结精度下成立，不能将不同实验的倍率相乘。
44: 
45: | 组合组成 | 要解决的问题 | 必须计入的代价 |
46: | --- | --- | --- |
47: | writer pack＋Init、Q Init | 降低量化打包和旋转准备成本 | 完整 writer/rotate，不用 helper 倍率代替 |
48: | 有界解包、复用、流水；布局研究另行裁决 | 减少反量化、格式转换和等待；保持数据及时到达计算单元 | Gather、padding、临时数据读写、索引、屏障、额外 UB/GM，及失去的重叠 |
49: | 紧凑 FULL 页＋请求级精确窗口 | 减少每页重复窗口占用，释放可用 KV 容量 | 全部 GDN/MTP 状态、sidecar、allocator padding、固定 workspace 与实际 HBM 峰值 |
[...]
76:         + 到达HBM的临时数据 + MTP所有实际轮次的相应流量
77: D_L2、D_L1分别统计经过这些层级的流量，不与D_HBM重复相加。
78: F_Cube[精度] = target + 所有实际draft轮次 + OSCAR额外Cube工作（按精度分列）
79: F_Vector = 量化/反量化/旋转/softmax/归约等实际Vector工作
80: 
81: 单阶段资源时间下界：
[...]
86: ```
87: 
88: 带宽和计算上限必须注明来自哪里、适用什么形状和精度；不可用无法达到的峰值给出乐观结论。串行阶段按顺序累加，重叠阶段按依赖图核算，不将 actor 或嵌套相位时间相加成 wall。只检查 Cube FLOPs/byte 不足以排除 Vector、标量或同步瓶颈。
89: 
90: 尤其不能把 W8A8、BF16 和 FP32/HF32-off 的运算量混在一起除以同一个 Cube 峰值；同一共享计算单元上的各精度服务成本分别核算。TP4使用每rank的实际工作、带宽和关键路径，另计通信；不能把全模型字节/运算量与单卡带宽或算力混用。
91: 
92: **OSCAR 必须避免压缩省下的访问被其他成本抵销**：当前有界 FP32 K/V 发布、Cube 重复读取、score/P/accState 中间流量都要入账；其中多少命中 L2、多少落到 HBM 不能猜。cache-off CAModel 可以比较其固定模型内两臂，不能直接证明真机访存瓶颈或实际 HBM 压缩倍率。

## gpt_new_oscar_kimi/docs/quantization_hotpath_20261009.md
[...]
7: | 路径 | 当前真实实现 | 本轮重点 |
8: | --- | --- | --- |
9: | candidate 新 KV 写入 | `integration/cache_storage_ops.py` 选择 `rotate_clip_store_striped_out` | Hadamard 准备、旋转、FP16 metadata 舍入、FP32 量化、INT2 打包 |
10: | request-window 研究写入 | 独立 packed/window 两个算子；packed 复制同一量化流程 | 合格的新量化实现必须覆盖此格式，不只改 probe |
11: | q4/q1 decode | `attention_cv_decode_bundle.cpp`，64 行 padded unpack 与有界预取 | 已有优化不能再次计入收益；检查剩余 metadata/位操作/等待 |
[...]
16: ## 已确认的浪费与独立原型
17: 
18: ### 1. Hadamard 索引初始化
19: 
20: 当前 `RotationEngine::Init` 在每个核、每次启动时按标量写 `D×log2(D)` 个索引与同样数量的符号。D256 为 **4096 次 SetValue**，与本次有效 token 数无关。
21: 
22: 研究实现 `csrc/experiments/hadamard_indices/vector_indices.h` 使用整数等差序列与按位运算生成同一索引；符号仍精确为 FP32 的 +1/-1。只在输入 Load 之前借用已有 input/work/red 缓冲，不增加工作区、参数或 launch，不改变旋转的 Gather/Mul/Add 顺序。
23: 
24: - 官方 CPU-debug：D64/D128/D256 的旧新字节、独立公式、padding 与 guards 全部通过。
[...]
26: - CAModel 单 AIV、D256、相同库与配置：原路径 **33393 ticks**，向量路径 **4695 ticks**，这个元数据原型约 **7.11×**。两臂均完成独立公式/guard/profile 检查，无超时。
27: - 两臂包含相同的输出拷贝。**这不是完整 store、目标 NPU、模型或整轮 7.11×**；完整写路径组合比较尚未完成。
28: - 原始结果：`reports/quant_hadamard_indices_20261009/reports/`；VM 原始指令 dump 仍保留，宿主回收数值、guard、profile 与监管报告。
29: 
30: ### 2. INT2 写入位打包
[...]
42: | 当前writer | 173419 | 1.000× |
43: | SIMD位打包 | 136213 | 1.273× |
44: | SIMD位打包 + 精确Hadamard初始化 | 96566 | **1.796×** |
45: 
46: 三臂保存的全部输出及输入回读逐位一致，独立oracle、前后guards、完整16个AIV和task周期、180秒监管/清理均通过。完整writer包含旋转、量化和窗口发布，未用单独pack或Init时间替代。结果在`reports/quant_store_simd_pack_20261010/comparison.json`。这是完整writer局部CAModel收益；目标NPU、图和整轮性能仍未验收。
47: 
48: 已将同一实现接入本地 candidate 的 striped writer 与研究 request-packed writer，共享 `striped_store_pack.h` / `hadamard_indices.h`。保持原算子名/ABI/selector，因此两个固定candidate入口安装后使用同一实现，无新增参数。源还原检查确认正式striped与已测C臂只差符号、include与说明，request-packed完整旋转/量化前缀逐字一致。旧基线已冻结，原canonical及主rotate_out未改。相关17+7项主机检查通过；实际生产源CANN与request-packed CPU接缝仍在验证，未推送。
49: 
50: ### 3. C4 扩大反量化批次
[...]
68: ## 交付条件
69: 
70: 合格组件需要组合后测完整算子，核对实际 selector，再接入两个固定 candidate 入口。局部微核倍数不能当整轮目标达到；未合格研究代码不进入默认生产。FP16 metadata 先舍入、FP32 Mul→Add、量化公式、INT2 位序、原生GDN与冻结精度门保持不变。
71: 
72: ## C4 跨成员流水的完整双轮结果（2026-10-10）
[...]
74: 同输入 Q336/R1/C337/S1/20core，两臂均保留全部1008任务及生产source2抑制，所有partial/LSE/status/cluster counters逐位相同，独立oracle及60actor完成门通过。完整CAModel周期1849738→1610282，**1.148704倍**；两臂均在原600s期限内正常结束。该形状有一个full256和17行tail，不是65K稳态或整轮性能。预取错误bad336的CPU边界门仍在进行，生产未启用；不凭该局部倍数推送达标版本。证据：`reports/c4_member_pipeline_20261010/reports/c4-pipeline-camodel337/comparison.json`。
75: 
76: ## 紧凑Batch8与Q旋转完整对照（2026-10-10）
77: 
78: 完整writer N128/Hkv1/D256/grid16：当前pack+Init 95930ticks，Batch8 92403，只有1.03817倍；D256与D64/clip CPU两组全输出字节相同，不合入生产。Q旋转N128/H6/D256/grid32：旧110343，单独Init68082，Batch8 64537；相对旧分别1.62074/1.70976倍，Batch8在Init之后只增加1.05493倍。三臂CAModel完整32actor、输入/guards、output/status全位一致及独立oracle通过。7个小CPU边界、21臂均逐位通过；主CPU形状因调试日志耗尽tmpfs失败，原错误/3.8GB原始记录已完整压缩归档，不能计作CPU主形状通过。源/设备模型/180s期限相同。以上仍是量化和旋转局部结果，未建立相对native整轮2–3倍依据；生产、NPU、graph未升级/验收。完整证据`reports/hadamard_batch8_20261010/summary.json`。

## gpt_new_oscar_kimi/docs/reference_manifest.md
[...]
14: 本地开发环境是 macOS arm64、Python3.12.6。独立 `.venv` 使用 torch2.14.0 做CPU oracle测试，**不代表目标torch2.10.0**。macOS本体没有CANN/NPU；本轮已发现并使用Lima oscar内的CANN9.1、bisheng15、aarch64 Linux与官方CPU调试库。VM独立环境为Torch2.12.0+cpu/torch_npu2.12.0/pybind11 3.1.0，与目标Torch2.10版本不同，不能代替目标运行。详见 reports/vm/validation.json 及 `reports/environment.json`、`local_environment.json`。
15: 
16: 目标模型位置、TP4、图、MTP等保留于 `configs/target.json`。真机连接方式未提供；模型config与权重不在本机，FULL层数/head_dim/GDN实际dtype形状必须由目标环境核实。设备与编译目标按本次启动文档附录 F 固定为物理卡0–3和ascend910b4，端口按附录 A 保留8989；其他项目记忆不构成本任务配置来源。用户回传的 node93 默认设备空值错误见档案 #123；最新复跑已通过 `probe-ops` 的75项 store/merge 原语 NPU 探针，越过 #125 的依赖库加载错误；随后首个 CV 数值用例失败，见 #126；更新后的日志进入TP4/MTP模型加载，因prefix关闭时将GDN请求跨度误作FULL页对齐而失败，见 #127。新日志未附前序CV/旋转探针完整结果，不能补造通过项。再下一轮已完成torch.compile/初次profiling并获得KV预算，#127不再出现；MTP调用原生copy_with_new_block_size(128)时被外部物理页检查拒绝，见#128。编译完成不等于捕图/回放通过。
17: 
18: ## 权威语义入口
19: 
20: - `references/oscar-vllm-pr46774/vllm/v1/attention/ops/triton_oscar_store.py:41`：FP32量化、先FP16 metadata、LSB-first编码。
21: - 同快照 `vllm/v1/attention/backends/oscar_attn.py:219`：旋转、裁剪；`:259`起窗口；`:745`起输出合并。PR工程限制见 `docs/semantics.md`。
22: - `references/oscar-paper/rotation/compute_kv_rotation.py`：真实数据二阶矩与data-free Hadamard两种明确方法。
23: - `docs/native_integration.md`：本轮核实的后端/spec/allocator/metadata/MTP/graph完整接缝。
24: - `docs/ascendc_design.md`：AscendC接口先例、D.4四问、官方A2数据通路与已实现CV的验证边界。
[...]
35: ## 仍缺少的输入/证据
36: 
37: 真机连接及完整执行日志（用户已回传配置失败、开发命令误用、加载失败及其后75项原语通过/首个CV数值失败片段）；同环境原生基线；实际模型config与权重指纹；质量评估数据和预先冻结的logits/任务指标/MTP容差；完整目标设备/图/profiler结果；H18复杂度冲突的需求结论。VM CANN交叉编译结果已经存在，不属于缺失项。

## gpt_new_oscar_kimi/docs/release_candidate_20261012.md
[...]
15: - 默认显式开启 prefix caching，使用物理页精确快照；未启用请求私有窗口研究布局。
16: - 省略 `--max-num-batched-tokens`，保持原生 GDN、调度预算及默认0–3卡/8989；直启可叠加 `--rear-cards` 使用4–7卡/7878。
17: - 启用合格量化/旋转组合和 MDL q4 数据装载；后续MTP q1及C4沿用原路径。
18: - MDL完整本地配对1079788→931042 ticks，1.1597629倍；CPU与CAModel逐位/oracle通过；完整40项CANN/Torch构建通过。此为局部算子结果，不是整轮2–4倍验收。
19: - Prefix及启动接缝已完成主机验证，真实NPU prefix、模型质量和整轮速度尚待目标机认证。

## gpt_new_oscar_kimi/docs/roi_decode_overlap_20261010.md
[...]
59: 单位是该 CAModel actor 时间域的 cycles，没有换成 NPU 毫秒。K/V 包沿用实测有界阶段，不能把所有 wait 都当作可删除成本。
60: 
61: 候选每对任务 Cube 顺序为 `QA, QB, PVA, PVB`；每个 AIV 顺序为 `K_A_next, S_A, S_B, V_A_next, K_B_next, C_A, V_B_next, C_B`。共享 packed UB 只在该任务 V 已用完后交给另一个任务。每请求下一 softmax 必须晚于自己的上一 PV 消费；PV 必须等待两 lane 的 PReady；下一 QK 等待自己的完整 KVReady。Cube 串行、各 AIV 串行，跨 actor 依赖保留上述实测延迟。查询加载、最终归一化/旋转/写回、任务切换和新增上下文开销另计，不能藏入重叠。
62: 
63: 以这些固定包重复递推 30 回合：原单请求单位周期 40582 cycles，两个请求一对周期 51841 cycles，相当于每请求 25920.5 cycles，history 条件比例 **1.565633×**。这只是这个候选顺序的估值，不是不可超越的上界。两请求 AIV 包的资源下界为 50060 cycles，说明这份估值对新增向量/调度成本很敏感。

## gpt_new_oscar_kimi/docs/rotation_pipeline.md
[...]
1: # 旋转、精确裁剪与双写流水线
2: 
3: 档案依据：G27（窗口必须保存原值），#13–22（metadata 舍入与位序错误），#37–49（prefix/MTP materialized KV 的生命周期），#70–71/D.4（写入与全量恢复延迟），#81–83/#91–92（A2 API 与 UB 边界），#111（旋转结果必须保留 FP32）。语义来自指定 PR `oscar_attn.py:235–243` 与 `ops/reference.py` 独立 oracle；未参考失败项目代码。
4: 
5: ## 接口与数值
6: 
7: `rotate_out(input, rotation_transposed, output, status, hadamard=False, slots=None)` 只写入预分配 FP32 输出与每行状态。输入 `[N,H,D]` 可以是 BF16、FP16 或 FP32；`D=64/128/256`。矩阵是 FP32 的 `R.T.contiguous()`。Q 使用 `Rk.T`，最终 value 输出使用 `Rv`，分别实现 `Q @ Rk` 与 `out @ Rv.T`。全程不降低乘法输入精度。可选 `slots` 是 NPU int64 `[N]`；负 slot 对应 token 的全部 head 在 UB 清零，输出和状态均为零，避免原生 padding 的 NaN 错触发有效行的数值闸。有效行的非有限值仍返回状态 2；`slots=None` 保持原有完整旋转语义。全 padding tile 直接跳过矩阵变换。
8: 
9: `rotate_clip_store_out(key, value, rk_transposed, rv_transposed, slots, positions, packed, raw_key, raw_value, raw_tags, status, block_tokens, blocks, ssm_offset, page_stride, sink_tokens, recent_capacity, k_clip, v_clip, hadamard=False)` 在一次 kernel launch 内完成新 token 的 K/V 旋转、绝对值百分位裁剪、INT2 量化和压缩页写入，并保存未旋转 BF16 原值到物理页 padding 的精确窗口。
10: 
11: 裁剪使用 `Sort32` 与最多两级 `MrgSort`，得到真正的相邻阶统计量，再按 FP32 rank 做线性插值；不是最大值乘比例，也不使用近似二分阈值。零比例按 PR 禁用裁剪。scale 和 zero 先舍入到 FP16，重新转 FP32 后参与除法；4 个 INT2 code 以 LSB-first 存入一个字节。FP16 scale 下溢为零时状态为 3；这保留已有的显式失败契约，不偷偷改 epsilon。
[...]
23: ## D.4 四问
24: 
25: 1. 对应 `phase0_store/phase1_stores`，query/output 旋转属于 attention 边界。
26: 2. D.4 原始日志 16K 写入为 215.1–216.0 ms；32K 续写为 208.6–209.3 ms。全历史 dequant 达 6499.8–6655.1 ms，CPU prepare 达 724.7–726.2 ms，不能复制这些访问结构。
27: 3. 本实现只访问本次新 K/V；旋转、排序、裁剪与量化在 UB 中完成，直接写终态压缩行。Hadamard 使用 `log2(D)` 级向量 butterfly；任意已校准 FP32 矩阵按 16 个输出通道分 tile，每次 matrix tile 被 8 行复用。设备内部行循环不会产生 Python token 循环或串行 torch kernel 链。精确 raw 窗口只写 sink 与每页本批最后 R 行，从不恢复历史。
28: 4. Hadamard 工作量为 `O(N H D log D)`；任意 dense 旋转为 `O(N H D²)`；UB 在两条分支都小于 64 KiB。目标是 decode 低于 D.4 的 0.6–1.1 ms 量级、16K 写入显著低于 215 ms。**这些是目标而非实测结论**；CPU 数学测试、CANN 编译、CANN CPU 仿真、NPU 数值与耗时分别记录，dense throughput 必须由真机打点验收。
29: 
30: `prepare_device_rotations` 仅在初始化时准备矩阵转置，并验证 Hadamard 的实际 Sylvester 符号模式后才允许 fast path。不得仅凭 artifact 的字符串标签启用不同数学操作。图回放使用持久 tensor 地址，不在热路径重新分配这些矩阵。

## gpt_new_oscar_kimi/docs/runtime_implementation.md
[...]
1: # Runtime 实现、页快照与验收边界
2: 
3: 档案引用：#26（窗口必须精确）、#27（安装不等于服务）、#28/#77/#78（延迟导入）、#31–33（不向 VllmConfig 增加字段）、#34/#36（实际图缓冲容量）、#37–49（请求身份、MTP materialized/commit 推断失配）、#69/#111（设备和 dtype）、#86/#97（模型与 draft 旋转）。本文件描述本次源码，不把历史档案的设备日志当本次验收证据。
4: 
5: ## 1. 全链调用与原生接缝
[...]
10:   A -->|GDN 组| G[原生 GDN conv / BF16 SSM]
11:   B -->|原生 GPU qstarts / seq_lens / slots| C[prepare_attention_tasks_out]
12:   C --> D[FP32 Q 旋转]
13:   D --> E[AscendC Cube / Vector attention]
14:   E -->|History INT2 / 全局精确窗口 / 当前 chunk BF16| F[FP32 LSE merge]
[...]
20: 原生 `model_runner_v1.py:4080` 定义分配、`:4351` 定义 reshape、`:4681` 保留 GDN SoA 视图、`:4735` 用 backend kernel block size 拆分虚拟页。本实现通过外部 hook 接入三个方法；原生 GDN 的 spec 对象、dtype、shape、页 ID 和 reshape 实现原样保留。OSCAR provider 保存在模块单例中，未扩展 `VllmConfig`。
21: 
22: 具体生产入口为 `AscendRuntimeProvider` 和 `OscarAttentionImpl.forward`。构造模型时就按真实 `Hq/Hkv/D` 预分配共享 scratch，并加载全部旋转常量，确保原生 KV 内存 profiling 看见这些分配；不能等 KV 池按 HBM 预算分配完才临时追加 workspace。注册阶段只保存 stdlib lazy factory，第一次原生 backend 请求才加载 torch/NPU/operator。
23: 
24: 当前 chunk 直接读取 projection BF16，引用 PR `oscar_attn.py:486–577`。续 chunk 的历史在 tile 内恢复，绝不生成 `[history_length,H,D]` BF16 Tensor。Qwen3NextAttention 的 V 来自 `qkv.split`（原生 `qwen3_next.py:312–337`），可能非连续，因此预分配仅覆盖当前 token budget 的 BF16 scratch，必要时 `copy_` 当前 Q/K/V。这不是历史副本，计入下文 scratch 账。
[...]
71: 原生 `resolve_kv_cache_block_sizes` 实际返回 scheduler LCM=2304、hash GCD=768；`BlockHashListWithBlockSize`按3个768-token hash组成一个2304-token hash。真实Ascend coordinator初始化保留native FullAttentionManager和AscendMambaManager，公共pool中的非null物理ID互不重叠。对一次4608 token输入加3 lookahead，实际native方法分配FULL 3个非null块，align模式每个GDN组首次分配1个当前状态+3个spec状态，历史索引用null占位，不应把这些null ID计成物理页。
72: 
73: 设可给KV池的预算为 `H - E`（E已包括模型、activation、旋转、workspace和图等独立开销），原生每pool block的真实字节为 `17*P`，因此：
74: 
75: `nb = floor((H-E)/(17*P))`。
[...]
94: 四段连续、不重叠、无缺口。History 使用 `q@Rk`，CV 中 FP32 解包/softmax，在写 partial 前乘 `Rv.T`，随后各段以稳定 LSE 合并。多个 query 共享 history tile，但逐 query 使用自己的 causal/窗口 mask。
95: 
96: PR 工程中的 staging eviction 后 INT2 替代、CPU 循环组装、完整历史 dequant、inverse rotation、拼接已被改变；数值目标为无 eviction 的精确全局窗口。MTP 原生 draft 层使用显式、可观察的 identity rotation（档案 #86）；target 层必须加载与模型 config+weight index 指纹匹配的 artifact。data-free Hadamard artifact 的 objective 不等于已经完成模型质量评估。
97: 
98: ## 5. 图与性能账
[...]
100: MetadataBuilder 直接保留 native GPU tensors；捕获时记录 pointer/shape/stride/dtype，后续相同图形状若地址改变立即拒绝。原生 `_dummy_run` 在 capture 分支不保证初始化 slots（`:3548`只在非capture分支fill），因此 capture builder 显式将合成输入 slots 置为-1，避免依赖 warmup 次数或旧缓冲内容；完整各算子仍被捕获，真实回放前由原生 `_prepare_inputs` 在同地址写入真实 slots。元数据 kernel 在回放时重新读取这些设备数据，不把 seq_lens 固化为 host attrs。原生 `acl_graph.py:270` 要求的 `update_graph_params` 接口保留；本实现没有 FIA 的 host task attrs 或 external-event waits，因此不需要更新一个不存在的 FIA task。GDN 图分支完全原生。
101: 
102: 设 token capacity 为 `N`、query heads为 `Hq`、KV heads为 `Hkv`、head dim为 `D`，`g.splits`为预分配容量乘数（配置 `attention_splits`，默认1）。task容量为 `3*N*Hkv*g.splits`，每行16个int64；partial arena容量为 `N*Hq*3*g.splits*D` 个FP32，LSE按同一行数计。scratch总量由 `WorkspaceGeometry.total_bytes`逐项计数，包括当前 Q/K/V 连续化缓冲、FP32 Q旋转、partial/LSE、merge输出、全部状态、slot/position及每Cube core工作区。所有层在同一原生执行流顺序复用一个同形 arena，不按17层重复分配。
103: 
104: 每次调用的实际source split数只由捕获的query形状决定，避免单请求长decode仅使用一个history Cube：
[...]
126: 每页用于 prefix 的持久精确快照不在此“参与当前注意力窗口”量中重复计数；其占用已经包含在原生P预算内。INT2读量与精确 dense attention 的历史长度线性增长，H18字面“读取亚线性”不能成立，必须与“不全量恢复”区分。store对当前输入量化一次，同时保留必要精确窗口/快照；没有每一步重扫、恢复或重新量化全历史。
127: 
128: D.4 对照：取消6.5s全历史dequant和逆旋转phase；prepare为设备批量任务构建；store仅当前token量；最后一个 `status_guard` AscendC kernel检查四组状态，遇错执行设备 Trap，避免每层多个Torch布尔/归约/断言小算子。attention的当前源码性能仍必须用目标机器按相同输入进行逐phase计时。Host不做请求级循环、KV数值处理或tensor读回。不可在没有NPU时声称目标32K性能已优于原生。
129: 
130: ## 6. 验收状态
131: 
132: 本机测试能验证地址、形状、metadata持久性、padding隔离、MTP窗口保留和Python派发约束。`tests/test_runtime_native.py` 还直接执行只读参考文件中未改写的KV spec/registry/metadata基类和原生GDN reshape方法，检查外部spec转换后原生GDN视图的实际dtype、shape、地址与内容不变；外部依赖以测试夹具提供，因此这是host接缝证据，不是完整vLLM实例。CANN编译/CPUdebug属于另一层证据。目标NPU设备完成、graph capture返回、真实请求graph replay、TP4/MTP/prefix服务、冻结精度及配对性能均独立记在 `docs/checklist.md`；本文件不把任何前一层通过等同于后一层。

## gpt_new_oscar_kimi/docs/semantics.md
[...]
1: # OSCAR 数值语义与旋转契约
2: 
3: 本文件仅记录本工作区从指定 PR/论文直接核实的语义，以及本机 oracle 的范围。
[...]
14: - 来源登记：`references/PROVENANCE.md:17-20`。这些是固定本地快照，未宣称当前上游状态。
15: - 未访问任何旧失败实现。档案只用于错误回归：G19/G20/G23（采样身份）、
16:   G25-G34/#4-#22（量化/LSE）、#23-#25（协方差与特征分解）、#86（层覆盖）、
17:   #96/#97（工具环境与旋转来源）。
18: 
19: ## 数值契约
[...]
21: | 运算 | 精确定义 | PR 证据 |
22: | --- | --- | --- |
23: | 旋转 | `x_rot = x.float() @ R.float()` | `oscar_attn.py:235-243` |
24: | clip | ratio 为零时不裁剪；否则 `t=quantile(abs(x_rot),ratio,dim=-1)`，截断到 `[-t,t]`，quantile 默认线性插值 | `oscar_attn.py:239-242` |
25: | 量化粒度 | 每 `(token, KV head)` 的完整 D 维向量一组，K/V 各自参数 | `triton_oscar_store.py:16-17,41-56` |
26: | scale/zero | `s=max((max(x)-min(x))/3,1e-8)`，`z=min(x)`；二者**先**舍入 fp16，再转回 fp32 参与编码 | `triton_oscar_store.py:44-53` |
[...]
31: | 反量化 | `x_deq=q.float()*s.float()+z.float()` | `triton_oscar_decode.py:104-114,133-141` |
32: | GQA | `kv_head = query_head // (num_query_heads/num_kv_heads)`，除法整除 | `triton_oscar_decode.py:58` |
33: | 历史 attention | Q 用 `Q@Rk`，量化 K/V 在旋转空间累积，历史输出用 `@Rv.T` 回到原空间 | `oscar_attn.py:599-616` |
34: | 分段合并 | natural-log `L=logsumexp(L_i)`，`O=sum(exp(L_i-L)*O_i)` | `oscar_attn.py:745-749` |
35: 
[...]
61:    可消除的是全历史 BF16 HBM 副本/恢复写回，而非宣称精确注意力历史读取亚线性。
62: 5. **论文模拟器不能替代 PR store oracle**：论文
63:    `rotation/compute_kv_rotation.py:139-147` 没有 fp16 meta 先舍入，精确编码以 PR 为准。
64: 
65: ## 旋转 artifact
66: 
67: 项目 schema 是对 PR 分开的 K/V checkpoint 的有指纹封装；不是声称上游可直接读取此文件：
[...]
70: format_version: 1
71: source_grouping: layer
72: objective: hadamard | identity | qqt_sst_r_h_pbr | 明确的外部来源
73: head_dim: D
74: model_fingerprint: SHA256(模型配置 + 已核实的权重清单 SHA256)
[...]
85: 有限性、正交性；不接受缺层。identity 必须在创建和加载时显式 `allow_identity=True`。
86: 如果目标 draft 层采用允许的 identity 策略，调用方仍需记录授权、显式层名与告警；
87: 不能将主模型缺层或名称解析失败处理成 identity。档案 #86 证明校准引擎不含 draft
88: 时只有 16 个 FULL 层，故真实 target/draft 覆盖必须由运行时发现并验证，不能硬猜 17。
89: 
90: `build_hadamard_artifact` 是论文 `compute_kv_rotation.py:299-312` 明示的
91: data-free 正交旋转，来源为 `hadamard`，`calibrated=False`。它不建立端到端质量结论。
92: 代码默认要求 NPU；CPU 只能显式 `device='cpu', testing=True`，产物带 `test_only=True`
93: 且不得进入生产。`save_artifact` 仅把已经计算好的小型旋转常量迁移 CPU 序列化，
94: 不将 Q/K/V 数据计算迁移 CPU。`load_artifact` 使用 `weights_only=True`。
95: 
96: ## 真实样本校准接口
97: 
98: `sample_covariances` 同时接收同一份 Q/K/V 与非空 sample id：
99: 
100: - Q 按 KV head 的 GQA 组展开，`Cq_h=Q_h.T@Q_h/Nq`，`Ck=mean_h(Cq_h)`。
101: - `w_t=k_t.T@Cq_h@k_t`，归一化到 `sum(w)=T`；
102:   `Cv=mean_h((sqrt(w)*V_h).T@(sqrt(w)*V_h)/T)`。
103: - 非有限样本、负权重、零总权重显式失败；协方差对称化后再次检查有限性。
104: - 不重跑两遍引擎获取 Q 与 K/V，避免档案 G19/G20/G23 的 sample identity 漂移。
105: 
106: `build_sample_artifact` 必须传入 `eigensolver`，验证返回设备、shape、有限性、特征残差
107: 与正交性。之后按论文 `:234-264` 的 **`R@H@P`** 顺序构建旋转；P 由降序特征值与
108: bit reversal 生成。论文 CLI 实際默认 `--composition plain`（`:343`），本接口明确
109: 命名 `qqt_sst_r_h_pbr`，不混淆默认值。
110: 
111: 该接口不包含真实模型采样 worker，也不提供已经证实 NPU 执行的 eigensolver。
112: NPU fp32 累积与论文 CPU fp64 有数值差异，需要单独对拍。正交 max-abs 门为 `5e-4`，
113: 相对 Frobenius 特征残差门为 `5e-4`；这两项是新工程检查、尚无目标 NPU 通过证据，
114: 不得称为论文精度验收。返回 NPU tensor 本身不证明算子内部无 CPU/AiCPU 路径，仍需 profiler。
115: 
116: ## 本机验证证据
117: 
118: 执行：`.venv/bin/python -m pytest -q tests/test_reference.py tests/test_rotations.py`。
119: 环境：macOS CPU，Python 3.12，torch 2.14.0；与目标 torch 2.10/NPU 环境不同。
120: 首次验证 **58 passed**，测试包括独立 `struct` fp16/byte oracle、half-bin ties、tail bits、
121: causal GQA 与 torch SDPA、分段 LSE、空 row、旋转等价链、window 边界、指纹/缺层/identity
122: 失败、论文独立 fp64 协方差公式及坏 eigensolver 反例。
123: 
124: 这些结果仅证明本机参考工具的行为。生产 kernel 编译、数值、图捕获、图回放、模型精度、
125: MTP 接受行为、HBM 节省、各长度性能均为 **NPU 未验证**。

## gpt_new_oscar_kimi/docs/service_probe.md
[...]
3: 2026-09-29当前candidate包含balanced/C16，详情见[`mixed_cv_optimization.md`](mixed_cv_optimization.md)。同一命令
4: `git pull --ff-only && bash scripts/install_observe_serve.sh --variant candidate --probe-only --diagnose-mixed`
5: 现在自动对比旧fast基线与新算子，覆盖原四形状、65K历史的三形状和第一轮MTP draft全current CV；只打印8条`PERF_MIXED_OPT`及`PERF_MIXED_OPT_RESULT`，报告为`mixed-optimization-report.json`。不同算子逐位精度、冻结oracle、指定独立图和CV/attention包络速度门全部通过才继续；不加载模型、不跑AISBench。此前只有观测的mixed诊断保留供旧配置使用，当前candidate不重复跑它。
6: 
7: 2026-09-28新增的混合长prefill诊断见[`mixed_prefill_analysis.md`](mixed_prefill_analysis.md)：
8: `git pull --ff-only && bash scripts/install_observe_serve.sh --variant candidate --probe-only --diagnose-mixed`。
9: 完成安装/算子门后只测31条q4 decode的两种padding/split及加入一条长prefill的冷/热历史组合，按CV/current FIA/merge计时并核对冻结oracle；不加载模型、不跑AISBench。终端重点为四条`PERF_MIXED_ATTENTION`与一条`PERF_MIXED_RESULT`。独立报告`mixed-attention-report.json`与阶段状态JSON分开，精度、签名或资源释放失败即停止。
10: 常用的`git pull --ff-only && bash scripts/install_serve.sh --variant candidate`继续安装并启用C4/q1/fast unpack后直接服务，不执行这个诊断。
11: 
[...]
48: ```
49: 
50: 快路径也只需执行一次；它先按当前源码/CANN/SOC签名检查算子产物，签名不变则复用，变更则自动重编，并在新构建后跑冻结oracle的真NPU CV/旋转数值探针及资源释放门，任何失败都会阻止服务启动。只有构建产物、选卡、验收配置和oracle指纹完全一致时，快路径才标注`reused_prior_evidence`复用前次NPU数值证据；正式一键流程始终要求本轮新鲜数值探针。随后依次拉起两只托管服务，对相同四条 synthetic streaming 请求测量，确认每轮进程与NPU资源释放，再自动比较。原生只是显式配对基线，OSCAR失败不会切换执行路由。终端只保留少量阶段/资源状态、错误和最多8行配对 `PERF_*` 摘要；完整日志与JSON在本轮`logs/paired-concurrency-*/`。`PROGRESS_BUCKET`若在详细报告中出现，只是跨TP rank的 **host 心跳间隔**，不是单步设备算子时间。快路径跳过完整功能门，不能代替正式部署。
51: 
52: 配对在脚本内自动完成：先核对target配置、模型指纹、精确prompt ID、输出长度、cache salt和到达方式，再列出TTFT/TPOT/E2E与吞吐比；SSE单次批量到达导致TPOT无法计时时明确报`needs_evidence`。终端的`PERF_STATUS`、`PERF_QUEUE`、`PERF_TTFT_MS`、`PERF_TPOT_MS`、`PERF_E2E_MS`、`PERF_THROUGHPUT`、`PERF_VERDICT`、`PERF_EVIDENCE`就是直接复制给维护者的重点行。完整证据路径在最后一行。
[...]
56: #144增加**同输入新旧CV算子A/B**，仍只需上面一条命令：重编前先测本项目5288b2e对应的已签名旧产物，重编及新数值门后再测候选。每侧是独立子进程，固定2次预热、5次事件中位数；场景包括4请求长prefill，以及32请求q4、20–30K独立随机历史（物理页互不共享）。这些是独立随机张量，不是用户的127条数据集。两侧输入hash必须一致，任务hash因tiling可不同，输出/LSE必须通过冻结oracle；若候选更慢则停在模型启动前。`PERF_CV_AB`给出两侧毫秒和比值；旧产物缺失或不能验证时标`not_comparable`，仅报告候选`PERF_CV_OP`时间，绝不伪造旧版结果。算子A/B不能替代随后native/OSCAR K4速度门。
57: 
58: #143后，`scripts/probe_concurrency.sh`还会在原始配对退化时，**复用同一OSCAR服务**自动跑一次独立诊断批次：相同20/23/27/30K与64输出，repeat1使用新cache_salt。原始批次没有NPU计时事件或相位同步；诊断批次每相位记录真实NPU Event区间并同步确认完成，明确标为`synchronized_diagnostic_only`，不参与速度比。它按TP rank、prefill/MTP draft、query/KV形状统计CV/旋转/current/merge/store/guard；整图回放只计整图，图内细项不推断。事件区间可能包含提交间隙和流依赖，不等同单kernel CANN trace，也不能把四rank之和当作墙钟。
59: 
60: 终端新增`PERF_DIAG_START`、`PERF_DIAG_EVENTS`、最多三行`PERF_DIAG_STAGE`和三行`PERF_DIAG_CV`，与原有`PERF_*`一并复制即可。CV行给出关键rank、query/KV形状、split、次数与p50/p95；`max_seq_len=0`明确表示上下文未知，maxseq与maxquery相等也只是无旧上下文候选。完整事件在OSCAR本轮trace目录`device-events-<pid>.jsonl`，摘要在`oscar/diagnostic/device-event-summary.json`。无须另开命令、重载第三次模型或操作profiler HTTP端点；#133的崩溃路径不再使用。dummy和capture不插入事件；只有正常轮结束后模型入口才读取武装标记，相位内部不轮询文件。若继承了`OSCAR_DEBUG_SYNC/TIMING/PROFILER=1`，正常测速明确拒绝，防止同步数据混入速度对比。
[...]
64: 被动 `/metrics` 无法得知客户端恰好提交了 32 条、每条实际 token 长度、请求级 TTFT/ITL/E2E 或失败率；这些要从用户原压测程序的结果、请求清单与终态统计并入配对分析。首次采样已在流量中、metrics 缺计数器或采样有断点时，窗口标 `partial`，不报告完整窗口吞吐。原生对照须显式拉起同配置的 native 服务、跑**同一客户端与数据集**，再比较相同窗口；设备相位成本另需独立 device timing。健康、图回放、CPU 测试或 synthetic 请求均不推出性能追平。
65: 
66: 每次服务启动使用唯一 `OSCAR_TRACE_DIR=.../trace-<uuid>`，不会把旧 trace 当成此次执行的证据。图回放事件只声称 launch 返回；真实请求完成记录为另一个状态。HTTP 输出不建立 kernel 精度门、logits/任务质量、MTP 质量对照或性能通过，这些字段仍为 `not_run`。
67: 
68: `attention_dispatched`/`cache_layout` 等 `emit_once` 证据按签名去重，长 prefill 或 decode 期间不再重复写入。为让 REQUEST_WAIT 的 worker 进展不冻结在旧签名上，每个 FULL 层还按 `OSCAR_PROGRESS_INTERVAL_SECONDS`（默认 5 秒）写入 `attention_progress` 心跳，`wall_time` 与 `max_seq_len` 随 chunk 推进刷新。FULL_DECODE_ONLY 图回放绕过 Python attention 路径，decode 阶段的存活心跳由图回放包装器以同间隔写入 `graph_replay_progress`。心跳只证明宿主侧存活与推进，不是设备完成或性能证据。逐请求的 REQUEST_WAIT/REQUEST_ERROR 和 worker 明细保存在相位日志、`status.json` 与 trace 目录；默认一键终端仅显示故障、`PERF_*` 和每60秒的阶段进度，不刷常规心跳。host相位打点写入`timing-<pid>.jsonl`。

## gpt_new_oscar_kimi/docs/stable_optimization_20261015.md
[...]
5: ## 2026-10-15 用户裁决
6: 
7: B1进入主分支candidate，作为后续叠加的比较基底。用户明确取消每个优化点必须达到1.15倍的规则；今后检查完整相关路径的净收益及资源代价，设备门保留不回退要求，冻结精度不变。历史1.15门的原始失败记录保留，不改写成当时通过。继续迭代后只推主分支，stable由用户真机确认后自行更新。
8: 
9: ## 启动与验收分母
[...]
19: 固定16384预算使大query走C16。此前的C4成员流水、q4/q1 MDL都不替换C16；旧C16每个成熟KV256块给16个成员分别做FP32 QK/PV，重复把同一K/V装入L1。条件32K→64K下，历史chunk工作量可从一份16K扩为16K+32K+48K，约6倍，不能据此推算实际秒数。
20: 
21: C16 B1方案保留16成员的INT2解包共享与逐输出FP32/K128顺序，将同一KV的K、V各装入单个256KiB B1一次，16个score/P槽保存成员结果。四组score/P通知轮转并确认消费，最后完整排空；覆盖B1前保留MTE1→MTE2及反向屏障。每成员的softmax、在线状态、错误域和最终Rv旋转保持。实际选择只替换原C16 reader，不改变请求、调度、GDN、prefix所有权或缓存格式。
22: 
23: q4 hybrid L1复用已有完整同库配对：MDL 2658960→2214530 ticks（1.200688倍，约8K历史机制形），短形约1.109倍。它只替换q4；q1继续MDL，C4继续既有已资格成员流水。Rv按FP32 NZ地址排列在模型加载时一次性生成，原始数值不变；旧路径继续使用natural Rv，禁止在forward临时打包或缺失时回退。新NPU门另含32K/64K短合成算子病例。
[...]
25: ## B1 基底后的第一轮
26: 
27: 主分支本地基底提交为`b6f8666`。最终Rv改为在C16簇的既有B1中加载一次，16个成员继续执行原FP32/K128旋转和原跨核确认。新同库B1对B1+Rv为3168844→3045844 ticks，1.0403829倍，资源增加0。C337两KV及末成员QR错误隔离CPU完整通过；C65完整CAModel逐位、oracle、1008任务/60actor通过。这是相对B1的独立配对，不与前一库倍率相乘，也未证明32K/64K端到端30%。[配对记录](../reports/c16_rv_reuse_20261015/completed/rv-camodel-c65/comparison.json)。
28: 
29: 64K目标探针的完整672-query主机oracle也已构造通过，20个原参考样本逐位一致，7.41秒、峰值2.20GiB；只是探针准备验证，[记录](../reports/c16_l1_reuse_20261015/long_oracle_64k_guarded_once/result.json)。
[...]
35: ## 后续独立接缝
36: 
37: Q Hadamard重新纳入已测Batch8：同库Init68082→64537 ticks（1.05493倍），固定Hadamard UB每核增加7168B，不增加GM；每行原FP32运算顺序保持。仍由既有`rotate_vector_init_out`与共享quantization开关选择，FE0及writer字节保持；原数值/同址图设备门保留。[源与证据复核](../reports/query_batch8_reopen_20261015/independent_review.json)。
38: 
39: mixed prepare通过真实ForwardContext、stream、父metadata和固定token span绑定两段任务表，重叠写/跨step/draft/capture/current-only均失效。在默认16K、16FULL层合成形下prepare调用32→2、descriptor写96→6MiB；这是工作量，不是速度倍率。candidate自动启用，observe新增真实NPU `mixed_prepare_reuse`门，完整比较所有task字段/positions、同址32K→64K及非法length刷新，双臂相同consumer复制计入速度。无NPU不能通过；CV/GDN/rotate/store/guard仍逐层执行。[实现与验证边界](../reports/mixed_prepare_reuse_20261015/summary.json)。
[...]
54: 1. 新reader对应融合history dequant/FIA内部的浮点数据装载和成员等待；不是新增全历史dequant阶段。
55: 2. 历史失败边界是约6.5秒全历史恢复、约215ms写路径及725ms主机prepare；这些旧数字不作本轮分母。
56: 3. 本版仅有固定KV256、单个B1与固定score槽；FP32精度、错误域、真实物理页与metadata虚拟块边界保留，没有CPU oracle生产路由、全历史BF16恢复或静默原生回退。
57: 4. 成本收益必须由完整算子配对与目标设备门决定。C16普通流水Q672/recent256 CPU120秒和CAModel基线900秒超时，保留失败，无倍率；该大形失败不代表后续小形未完成；普通流水作为B1依赖与研究基线，默认选择B1。prepare复用后续已扩大到安全的mixed两region并进入candidate；主机等价检查完成，observe新增真实prepare on/off完整metadata路径门，尚未取得设备速度证据。
58: 

## gpt_new_oscar_kimi/docs/striped_cache_candidate.md
[...]
7: 旧候选真实 NPU q4（32 请求、20–30K、N128/S3）CV 约 11.28ms；同期 native BF16 FIA 约 1.45ms。64K 完整已提供结果为相同 120 请求、7,812,000 输入及 61,440 输出 token，OSCAR 3331.55s、native 1371.97s；OSCAR 平均 TTFT 较低，但首 token 后明显更慢。当前代码每个历史 KV256 块仍分八个小批展开、重排两次大向量并逐行读取元数据。故此次重点覆盖每轮 target q4 和后续 MTP q1，而非仅优化少量成熟 prefill 簇。
8: 
9: 之前 B4 的设备精度失败版本已完整回退到 `3615f04`。新候选不包含 B4/延迟 alpha 数学变化。原生 GDN 未修改。
10: 
11: ## 数据与执行变化
[...]
13: D256 每槽仍为 136B、每元素仍是原来两个 bit、四个 FP16 元数据逐字节保留。旧槽 `[K64,Kmeta4,V64,Vmeta4]` 改为 `[K64,V64,Kmeta4,Vmeta4]`；每个 16-bit code word 中的八个量化码重排为维度 `i+32*b`。写入时直接生成新排列，读取时 Shift/And 直达自然维序，免去原大 Gather/plane staging。没有全历史 BF16 展开或额外历史缓存。
14: 
15: 短 query 使用 M32 有界工作区（实际 q4/GQA6=24 行），释放 UB 后每 lane 解包 64KV，KV256 的批次由 8 变 2；元数据有效性用 FP16 原始位的精确向量比较，保持 NaN/Inf/正 scale 检查。FP32 QK、softmax、PV、旋转和 Mul→Add 顺序保留。PV 读回明确限制在各 lane 的 16 行范围。prefill 的 generic/balanced/C4/C16 采用相同格式的 reader，仍保留已有调度与数学。
16: 
17: `LayerState.cache_format` 在创建时固定；配置改变、错误格式、非 D256 均显式报错。全部服务读者和 `rotate_clip_store_striped_out` 成对选择。GQA>8 使用同格式 M128 reader，不进入 M32。旧 fe0 内核与默认配置不变。当前只读原生 `model_runner_v1.py:3399` 的 uniform decode 使用 `uniform_decode_query_len`（本配置 MTP3 即4），外部 metadata 原样传递 `max_query_len`；因此该 q4 选择同时作用于图捕获，而不只作用于 eager probe。
[...]
50: ```
51: 
52: observe 保留原有真实算子、CV/旋转及候选门，并增加 `striped-cache`：同输入新旧 writer 原始字节/窗口对照，q4/q1 的 20–30K 与65K、padding、split、非对齐、C4/C16、非法 metadata、同地址改变输入的图回放；速度为2预热+5次NPU Event交替测量。report 与相位账本分开命名；任何精度/图/速度或释放失败停止服务，控制台只打印关键 `PERF_STRIPED` 行及错误。
53: 
54: 只需短算子门时可在 observe 命令附加 `--probe-only`，不加载模型、不生成 AISBench 请求。此项供必要的真机最终认证，不能用 CPU 替代 NPU。真实 NPU 数值、图、完整服务性能和模型质量在新候选上仍待认证；原已确认 fe0 精度保持其原证据范围。

## gpt_new_oscar_kimi/issue1_full_record.md
[...]
8: > 3. 每条目结构固定：**一行结论 → 关键报错信息（整行摘录）→ 原文全文（完整日志，零截断）**；只看摘要读"关键报错信息"块即可，需要完整上下文再读"原文全文"。
9: >
10: > **环境基线**：昇腾 NPU 服务器（8×昇腾 910B4，CANN 9.1.0，bisheng/clang 15.0.5 编译器）。项目 oscar-ascendc = AscendC 自研算子库 + vLLM/vLLM-Ascend 插件，TP4 + MTP 投机解码，模型 `Qwen3.5-27B-w8a8-mtp`。迭代方式：`git pull && bash scripts/install_probe_serve.sh`（安装脚本分 install / configure / build / prepare-rotations / native-calibration / operators-quick / window-pipeline / service-integration / whole-service-probe 等 phase，失败时打印 `FAILED phase=...`）。
11: >
12: > **编号规则**：[G1]~[G34] 为前半段（2026-09-14 ~ 09-16 上午），[1]~[73] 为后半段（2026-09-16 ~ 09-18），两段是同一台机器上时间无缝衔接的连续调试记录；[74]~[86] 为第三部分（2026-09-18，**kimi_oscar 项目**真机首轮 13 轮迭代，来源 gitcode issue #1）。条目结论中 "#N" 指后半段编号，"G N" 指前半段编号。
[...]
50: | 失败摘要打印后为空（相位日志 0 字节，脚本自己的行只进 trace.log） | 35、95 |
51: | `Failed to load the backend extension: torch_npu. You can disable extension auto-loading with TORCH_DEVICE_BACKEND_AUTOLOAD=0.`（import torch 期，纯 CPU 工具被带崩） | 96 |
52: | `[oscar] FAILED phase=prepare-rotations: 未提供旋转检查点`（脚本没有就地产出检查点的能力） | 97 |
53: | `[probe] FAIL: AscendC operator symbols missing: [...]` + `kernel_lib=None`（build 成功但算子包从未安装、torch 扩展丢失） | 98 |
54: | `[probe] FAIL: installed op package is missing aclnn entry points` / probe 只报 symbols 缺失无法定位 | 99 |
[...]
85: | 报错关键字 | 条目 |
86: |-----------|------|
87: | `SSL: CERTIFICATE_VERIFY_FAILED`（自签名证书，prepare-rotations 下载 rotations.pt 失败） | G14、G15 |
88: | c10 `pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 ... Invalid thread pool!`（OpenMP 线程池） | G15、G16、G17、29、30 |
89: | `OSError: liboscar_ascend_kernels.so: cannot open shared object file`（dlopen，4 个 TP rank） | G18 |
[...]
103: | `aclnnFusedInferAttentionScoreV3 failed, error code 561002` ＋ `EZ1008 Failed to execute tiling function`（CANN FIA 算子） | 55、56、66 |
104: 
105: ## D. 算子数值精度 / 校准数值
106: 
107: | 报错关键字 | 条目 |
[...]
111: | `test_npu_cv_matches_independent_dense_pr_oracle[64-1-17]`，64/384元素超差、max_abs 0.6885956525802612、最大误差位于head5 | 126 |
112: | `AssertionError: Tensor-likes are not equal!`（window_k vs k，2044/2048 不匹配，max_abs 0.90625，rel 808） | G27 |
113: | `eigensolver_known_spectrum` 特征值误差 7.90 / 71.14 / **139.44**（dim 8/64/128） | G28、G29 |
114: | `history_attention` max_abs_error 超阈（0.010~0.104；后期降到 0.010~0.042 仍判 failed） | G28~G30、G32~G34、4、5、13~16 |
115: | `lse_max_abs_error=Infinity`（LSE 数组含 ±Infinity）；个别档 3.6934 | G30、G32、G33、G34 |
[...]
118: | `inline_dequant_rows`：`selftest_table dtype/rank mismatch` → 行级反量化误差 k_err≈0.98、v_err≈1.195；meta scale 不一致 | 17、18、19、20 |
119: | `RuntimeError('selftest_history dtype/rank mismatch')`（primitive_selftest） | 22 |
120: | eigh/协方差全 NaN：`orthogonality_max_error=nan`、`residual_max_error=nan`、`non-finite covariance before eigh absmax=nan`、`weighted_nan=65536`、`last_tile_weight_min=-100.0133` | 23、24、25 |
121: | `two-pass sample identity` 两遍校准 Q/K/V 指纹不一致（relative fingerprint delta 0.33~2.0） | G19、G20、G23 |
122: | NPU eigensolver validation 数值超阈（layers.11.self_attn.attn/k） | G24 |
123: | prefill relative-L2 超阈（阈值 0.02）：`nan not less than 0.02` / 1.408 / 1.4637 | 63、64、65、66 |
124: 
[...]
163: | `ld.lld ... unknown file type`（merge_aiv/aic_obj_text，增量污染复现 G7/G8 同类） | 85 |
164: | `pool INTERNAL ASSERT FAILED ... Invalid thread pool!`（fork 前父进程未建池；vLLM 分支被 OMP pin 跳过） | 84 |
165: | `found 16 FULL attention layers ... but expect_layers=17`（校准层数口径） | 86 |
166: 
167: ## F. 性能定位与最终基线（结论性条目）
[...]
178: |------|---------|------|
179: | 前半段①编译期 | G1~G13 | 12 轮 build 失败→修通：缺头文件 / `__host__` 误用 / BT 宏冲突 / bf16 cast / 类型二义 / ld.lld / host_stub 缺声明 |
180: | 前半段②校准环境期 | G14~G24 | SSL 证书 / OpenMP 线程池 / dlopen / 显存不足 / npu-smi 解析死循环 / two-pass 指纹不一致 / eigensolver 超阈 |
181: | 前半段③首批算子快测 | G25~G34 | build 首过后算子全失败：not close / not equal / 特征值误差 139 / LSE ±Infinity / 300s 超时 |
182: | 后半段① | 1~2 | NPU 设备同步失败 507015（aicore 异常） |
183: | 后半段② | 3、21 | AscendC 编译错回潮（SymbolOverrideAdd / 浮点无符号互转禁令） |
184: | 后半段③ | 4~20 | 算子精度超阈（轮次最多）：history_attention / window_attention_twin / unwritten_lse_rows / inline_dequant_rows |
185: | 后半段④ | 22~25 | 校准 eigh/协方差全 NaN |
186: | 后半段⑤ | 26~33 | vLLM 集成连环错：DeviceOperator 循环导入 / `_oscar_attention_runtime` 字段缺失 / OpenMP 再现 |
187: | 后半段⑥ | 34~50（51、52 为挂起观察） | 图捕获 metadata capacity 三处打满 + 窗口 KV 事务状态机错误（code=7 → code=1） |
188: | 后半段⑦ | 53~69 | CANN FIA 算子失败 561002/EZ1008 + softmax_lse 0/1 元素 + 缺 causal mask + CPU/NPU 张量混用 |
189: | 后半段⑧ | 70~73 | 性能定位（dequant ~6.5s/卡）与原生基线跑通 |
190: | 第三部分 | 74~86 | kimi_oscar 首轮：前置检查误杀（74~77）→ 探测导入顺序/路径（78）→ CANN 环境变量与 pybind 组件（79~80）→ AscendC 首编 API 面与 SOC 头文件族（81~83）→ 线程池 fork（84）→ merge 增量污染（85）→ 校准层数口径（86） |
191: 
192: ---
[...]
209: | [G12] | L1856 | build 失败：auto_gen/host_stub.cpp:135/136 error: 'AscendC' does not name a type |
210: | [G13] | L2014 | build 失败：auto_gen/host_stub.cpp:128/129 error: 'kTilingBytes' was not declared in this scope |
211: | [G14] | L2232 | 进入新阶段即报错：prepare-rotations 下载 rotations.pt 失败——urlopen SSL CERTIFICATE_VERIFY_FAILED（自签名证书链） |
212: | [G15] | L2268 | prepare-rotations SSL 错误仍在 + native-calibration 失败：c10 pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 … Invalid thread pool! |
213: | [G16] | L2490 | native-calibration：同 c10 Invalid thread pool → RuntimeError: Engine core initialization failed … Failed core proc(s): {'EngineCore': 1}（calibration_failed） |
214: | [G17] | L2661 | native-calibration：c10 Invalid thread pool 在多个 worker/EngineCore 反复出现 |
[...]
217: | [G20] | L3355 | two-pass sample identity：calibration passes disagree beyond numeric replay wobble（relative fingerprint delta 8.640e-01 / 1.999e+00） |
218: | [G21] | L3559 | Worker 初始化失败：ValueError: Free memory on device (15.75/29.49 GiB) < 需求 0.9×26.54 GiB → Engine core initialization failed |
219: | [G22] | L3714 | prepare-rotations 卡在等待释放死循环：npu-smi memory field not recognized（npu 4~7）；用户 Ctrl-C 后贴 npu-smi info——8×910B4，各卡 HBM 已占 ~29.6/32 GB |
220: | [G23] | L3808 | two-pass sample identity：calibration passes disagree beyond numeric replay wobble（relative fingerprint-sum delta 3.251e-01 / 3.613e-01） |
221: | [G24] | L4006 | native-calibration：a TP rank failed NPU eigensolver validation at layers.11.self_attn.attn/k：local=[0.0, 32.0, 0.1817, 23.25, 5.05, 208.05, 208.05, 4.0]（数值超阈） |
222: | [G25] | L4216 | build 首次通过、operators-quick 首跑即 failed（rank_0.json；日志仅两条 Warning，无 CHECK 明细） |
223: | [G26] | L4277 | operators-quick：AssertionError: Tensor-likes are not close!（47/768 不匹配 6.1%，最大绝对差 0.0533 vs 允许 0.005，最大相对差 12.62） |
224: | [G27] | L4396 | operators-quick：AssertionError: Tensor-likes are not equal!（window_k vs k：2044/2048 不匹配 99.8%，最大绝对差 0.90625，最大相对差 808） |
225: | [G28] | L4585 | operators-quick：报告汇总 history_attention(64/128/256×q_len1~4) 全失败 + eigensolver_known_spectrum(8/64/128) eigenvalue_max_abs_error 7.90/71.14/139.44 + stage_and_prefix_restore(256) |
226: | [G29] | L4742 | 同 G28（同一份失败清单） |
227: | [G30] | L4897 | operators-quick：history_attention lse_max_abs_error=Infinity（LSE 数组出现 ±Infinity 项），max_abs_error 最高 0.2806 |
[...]
233: | [2] | L5980 | 复跑仍失败：同样的 507015 aicore 异常（npuSynchronizeDevice/ERR00100） |
234: | [3] | L6184 | build 阶段 C++ 编译错误：oscar_history_cv.cpp 大量 'SymbolOverrideAdd<float>' 非法二元运算、Duplicate/VExp/LoadKv 不匹配（exit 2） |
235: | [4] | L6660 | operators-quick 精度失败：history_attention max_abs_error 0.010~0.101、lse_max_abs_error≈3.7~4.0 超阈值 |
236: | [5] | L6846 | 同上：history_attention 精度失败（max_abs_error 0.039~0.104，lse≈3.7~4.0） |
237: | [6] | L7064 | history_attention 与 window_attention_twin 双双精度失败（twin max_abs 0.272/0.266、lse 1.91/2.05） |
238: | [7] | L7316 | 两算子精度继续失败（同 #6 量级） |
239: | [8] | L7527 | 两算子精度继续失败（q_len 1~4 全档位） |
240: | [9] | L7780 | window_attention_twin head_dim 64/128/256 全失败（max_abs 0.272/0.266/0.823；lse 1.91/2.05/2.01），日志新增 call_ms 计时 |
241: | [10] | L8005 | window_attention_twin 三档 head_dim 继续失败（max_abs 0.272/0.266/0.336） |
[...]
253: | [22] | L11072 | primitive_selftest 失败：RuntimeError('selftest_history dtype/rank mismatch') |
254: | [23] | L11247 | native-calibration 失败：TP rank NPU 特征分解校验 non-finite——orthogonality_max_error=nan、residual_max_error=nan、finite=False（solver=npu_torch_eigh，layers.11.self_attn.attn/v） |
255: | [24] | L11600 | native-calibration：RuntimeError non-finite covariance before eigh（absmax=nan） |
256: | [25] | L11965 | 同 #24 且 weighted_nan=65536、weight_sum_finite=False、last_tile_weight_min=-100.0133 |
257: | [26] | L12353 | window-pipeline 单测失败：AssertionError: 1.0 not less than 0.6（fallback 与 k0 前 4 行范数差） |
[...]
308: # 总总结：两个 issue 合起来到底报了什么错（整理者综述）
309: 
310: **背景**：项目作者在昇腾 NPU 服务器 node93（8×910B4，CANN 9.1.0，bisheng/clang 15.0.5 编译器）上，用 `git clone` + `bash scripts/install_probe_serve.sh`（后续 `git pull && ...`）反复迭代 oscar-ascendc 项目——以 AscendC 自研算子库 + vLLM/vLLM-Ascend 插件，在 TP4、MTP 投机解码配置下跑 `Qwen3.5-27B-w8a8-mtp`。前 34 条（前半段，09-14~09-16 上午）是**工程第一次跑起来的"点火周"**：先是 12 轮 build 失败把编译链修通（G1~G13）——缺头文件 `oscar_tiling.h`、`__host__` 函数被 `__aicore__` 核调用、`BT` 宏与 CANN 内置头冲突、bisheng 后端 "not support bf16 type cast"、`HistoryPlan`/`CalibrationShape` 类型二义性、`oscar_restore_launch`/`oscar_calib_q_moments_launch` 声明冲突、ld.lld 报 .o "unknown file type"、生成的 host_stub.cpp 里 `AscendC`/`kTilingBytes` 未声明；接着校准阶段连环撞环境与数值问题（G14~G24）——下载 rotations 撞自签名证书 SSL 错、c10 `pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 Invalid thread pool!`、`liboscar_ascend_kernels.so` dlopen 找不到、"two-pass sample identity" 两次校准指纹不一致（delta 0.33~2.0）、`Free memory on device (15.75/29.49 GiB)` 低于 0.9×26.54GiB 需求、npu-smi 显存字段解析不出导致等待死循环（各卡 HBM 已占 ~29.6/32 GB）、NPU eigensolver 校验超阈；最后首次算子快测全军覆没（G25~G34）——`Tensor-likes are not close!`（6.1% 不匹配）与 `not equal!`（99.8% 不匹配、最大绝对差 0.906）、`eigensolver_known_spectrum` 特征值误差高达 7.9/71.1/**139.4**、`lse_max_abs_error=Infinity`（LSE 数组出现 ±Infinity）、一轮 `Timed out after 300s`（SIGTERM）。
311: 
312: 前半段记录到此（09-16 09:16 +08）戛然而止，22 分钟后后半段记录接棒（09-16 09:38 +08），进入 **后半段的 73 轮（八阶段）**：**①** AI Core 执行异常致设备同步失败（error 507015、ERR00100、retCode=0x26）→ **②** 又两轮 AscendC 编译错（`SymbolOverrideAdd<float>` 非法运算、浮点/无符号整型互转禁令）→ **③** 大篇幅算子精度超阈（history_attention/window_attention_twin 误差最高 0.82、LSE 未写行致 NaN、反量化 k_err/v_err≈1.0）→ **④** eigh/协方差全 NaN（`weighted_nan=65536`、权重 -100 级异常值）→ **⑤** vLLM 集成层连环错（DeviceOperator 循环导入、OpenMP Invalid thread pool 再现、`Field '_oscar_attention_runtime' not found in VllmConfig`）→ **⑥** 图捕获容量打满（metadata capacity exceeded rows/tokens/block-table 三处同时到顶）与窗口 KV 事务状态机错误（code=7 → code=1 "commit exceeds materialized pending K/V"）→ **⑦** CANN FIA 算子失败（error 561002 + EZ1008 tiling 失败、LSE 0/1 元素、缺 native causal mask、CPU/NPU 张量混用）→ **⑧** 性能定位与原生基线（oscar-timing 发现 **dequant 每卡 ~6.5 秒** 是 prefill 绝对瓶颈；禁用 OSCAR 的 native TP4 基线先踩 `FileNotFoundError`（输出目录未建）后**跑通**：boot 309.6s、长输入 31897 tokens @ 6869.5 tok/s）。
313: 
314: **第三部分（[74]~[86]，2026-09-18 kimi_oscar 首轮）**：新项目（OSCAR INT2 KV 外部插件 + AscendC 算子包）在吸取前 107 条全部教训后首跑真机，仍打出 13 轮失败——但性质与前两部分的"踩坑"不同：约半数是**前置检查/脚手架自身的实现错误**（把真机预期组成当污染、set -e 命令替换陷阱、检查逻辑自污染假阳性、探测导入顺序不当、build 目录增量污染），而非算法错误；另一半是档案已收录的同族问题的**新触发面**（bf16 类型/转换面在 dav_m200 vs dav-220 头文件族的差异、线程池 fork 语义、merge 链接）。全部 13 轮均在当轮修复并推送（修复 commit 链见 git log；最终 build 全链通过、TP=4 校准引擎起来、collective_rpc 打通至插件 worker 方法）。**核心教训：真机现状即基线——环境前置检查一律"记录制"不得阻塞；涉及编译/链接/SOC 的决策必须先在档案与参照物（vllm-ascend 同栈代码）中核实再写码。**
315: 
316: **一句话概括**：这两个 issue 合起来是同一个昇腾 AscendC→vLLM-Ascend 全链路移植的完整调试史——从编译都过不去（缺头文件/类型冲突/链接器不认 .o），到校准环境错（SSL/OpenMP/dlopen/显存），到算子数值错（特征值误差 139、LSE ±Infinity、精度超阈），到服务集成错（配置字段/图容量/窗口事务状态机/FIA 561002），最终以"禁用 OSCAR 的原生基线跑通、定位出 dequant 是每卡 ~6.5 秒的主要瓶颈"告一段落。
317: 
318: ---
[...]
324: | # | 类型 | 评论 ID | 时间(UTC) | 一行结论 |
325: |---|------|---------|-----------|----------|
326: | G1 | 正文 | — | 2026-09-14T11:53:56 | 首帖：git clone 后首次运行 install_probe_serve.sh，build 阶段即失败（cmake --build exit 2） || G2 | 评论 | 5663558206 | 2026-09-14T12:01:11 | build 失败：oscar_common.h:3:10 fatal error: 'oscar_tiling.h' file not found（aic/aiv/precompile 多个编译单元） || G3 | 评论 | 5663597083 | 2026-09-14T12:04:45 | build 失败：oscar_vector.cpp:33 no matching function for call to 'Align'（__host__ 函数不能从 __aicore__ 调用）；oscar_history_cv.cpp:9 'BT' 重定义与 cce_aicore_intrinsics.h 冲突 || G4 | 评论 | 5663652333 | 2026-09-14T12:09:34 | build 失败：bisheng 后端 fatal error: error in backend: not support bf16 type cast（clang frontend exit 70）；oscar_prefix.cpp:224 'oscar_restore_launch' conflicting types || G5 | 评论 | 5663725321 | 2026-09-14T12:15:28 | build 失败：oscar_history_cv.cpp 大量 reference to 'HistoryPlan' is ambiguous / variable has incomplete type 'HistoryPlan' || G6 | 评论 | 5663762524 | 2026-09-14T12:18:24 | build 失败：no matching function for call to 'oscar_history_cv_kernel' / 'oscar_history_reduce_kernel' / 'oscar_window_cv_kernel'（26 warnings and 4 errors） || G7 | 评论 | 5663974520 | 2026-09-14T12:32:35 | build 失败：ld.lld（-m aicorelinux）merge_aiv_obj_text 链接步骤 Error 1 || G8 | 评论 | 5664016781 | 2026-09-14T12:35:37 | build（--clean-first）失败：ld.lld error: oscar_vector.cpp.o: unknown file type（aic/aiv 两路 merge 均失败） || G9 | 评论 | 5664068352 | 2026-09-14T12:39:12 | build 失败：oscar_calibration.cpp 'CalibrationShape' is ambiguous / incomplete type；'oscar_calib_q_moments_launch' conflicting types || G10 | 评论 | 5664114744 | 2026-09-14T12:42:23 | build 失败：oscar_ascend_kernels_merge_obj 目标 ld.lld Error 1（设备对象合并链接失败） || G11 | 评论 | 5664166920 | 2026-09-14T12:46:09 | 同 G10（merge_obj 链接失败） || G12 | 评论 | 5664212780 | 2026-09-14T12:49:44 | build 失败：auto_gen/host_stub.cpp:135/136 error: 'AscendC' does not name a type || G13 | 评论 | 5664309695 | 2026-09-14T12:56:52 | build 失败：auto_gen/host_stub.cpp:128/129 error: 'kTilingBytes' was not declared in this scope || G14 | 评论 | 5664352166 | 2026-09-14T12:59:54 | 进入新阶段即报错：prepare-rotations 下载 rotations.pt 失败——urlopen SSL CERTIFICATE_VERIFY_FAILED（自签名证书链） || G15 | 评论 | 5672668103 | 2026-09-15T00:14:14 | prepare-rotations SSL 错误仍在 + native-calibration 失败：c10 pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 … Invalid thread pool! || G16 | 评论 | 5672733873 | 2026-09-15T00:20:04 | native-calibration：同 c10 Invalid thread pool → RuntimeError: Engine core initialization failed … Failed core proc(s): {'EngineCore': 1}（calibration_failed） || G17 | 评论 | 5672877875 | 2026-09-15T00:37:12 | native-calibration：c10 Invalid thread pool 在多个 worker/EngineCore 反复出现 || G18 | 评论 | 5672997028 | 2026-09-15T00:52:29 | native-calibration：OSError: liboscar_ascend_kernels.so: cannot open shared object file: No such file or directory（4 个 TP rank dlopen 失败） || G19 | 评论 | 5673116334 | 2026-09-15T01:08:12 | native-calibration：two-pass sample identity——real NPU Q/K/V changed between calibration passes（layers.11.self_attn.attn） || G20 | 评论 | 5673326397 | 2026-09-15T01:34:19 | two-pass sample identity：calibration passes disagree beyond numeric replay wobble（relative fingerprint delta 8.640e-01 / 1.999e+00） || G21 | 评论 | 5673386074 | 2026-09-15T01:42:07 | Worker 初始化失败：ValueError: Free memory on device (15.75/29.49 GiB) < 需求 0.9×26.54 GiB → Engine core initialization failed || G22 | 评论 | 5673467244 | 2026-09-15T01:52:22 | prepare-rotations 卡在等待释放死循环：npu-smi memory field not recognized（npu 4~7）；用户 Ctrl-C 后贴 npu-smi info——8×910B4，各卡 HBM 已占 ~29.6/32 GB || G23 | 评论 | 5673593187 | 2026-09-15T02:09:03 | two-pass sample identity：calibration passes disagree beyond numeric replay wobble（relative fingerprint-sum delta 3.251e-01 / 3.613e-01） || G24 | 评论 | 5673718926 | 2026-09-15T02:24:11 | native-calibration：a TP rank failed NPU eigensolver validation at layers.11.self_attn.attn/k：local=[0.0, 32.0, 0.1817, 23.25, 5.05, 208.05, 208.05, 4.0]（数值超阈） || G25 | 评论 | 5677052337 | 2026-09-15T08:20:44 | build 首次通过、operators-quick 首跑即 failed（rank_0.json；日志仅两条 Warning，无 CHECK 明细） || G26 | 评论 | 5677140126 | 2026-09-15T08:28:13 | operators-quick：AssertionError: Tensor-likes are not close!（47/768 不匹配 6.1%，最大绝对差 0.0533 vs 允许 0.005，最大相对差 12.62） || G27 | 评论 | 5677191345 | 2026-09-15T08:32:28 | operators-quick：AssertionError: Tensor-likes are not equal!（window_k vs k：2044/2048 不匹配 99.8%，最大绝对差 0.90625，最大相对差 808） || G28 | 评论 | 5690165913 | 2026-09-16T00:26:51 | operators-quick：报告汇总 history_attention(64/128/256×q_len1~4) 全失败 + eigensolver_known_spectrum(8/64/128) eigenvalue_max_abs_error 7.90/71.14/139.44 + stage_and_prefix_restore(256) || G29 | 评论 | 5690288622 | 2026-09-16T00:42:04 | 同 G28（同一份失败清单） || G30 | 评论 | 5690318464 | 2026-09-16T00:45:59 | operators-quick：history_attention lse_max_abs_error=Infinity（LSE 数组出现 ±Infinity 项），max_abs_error 最高 0.2806 || G31 | 评论 | 5690414229 | 2026-09-16T00:58:50 | operators-quick：Timed out after 300s（进程组被 SIGTERM，returncode -15） || G32 | 评论 | 5690457271 | 2026-09-16T01:04:42 | 同 G30（Infinity LSE；max_abs_error 最高 0.3611） || G33 | 评论 | 5690501522 | 2026-09-16T01:10:35 | 混合表现：个别档 lse_max_abs_error=3.6934、多数仍 Infinity；max_abs_error 0.048~0.093 || G34 | 评论 | 5690542637 | 2026-09-16T01:16:03 | 同 G30/G32（Infinity LSE + request1_lse_invalid_heads 1~8 计数） |
327: 
328: ### 前半段 阶段小记（报了什么错）
329: 
330: - **G1~G13 编译期（12 轮 build 失败）**：缺 `oscar_tiling.h`；`Align` 是 `__host__` 不能在 `__aicore__` 里调；`BT` 宏与 `cce_aicore_intrinsics.h` 重定义冲突；bisheng 后端 "not support bf16 type cast"（exit 70）；`oscar_restore_launch`、`oscar_calib_q_moments_launch` 声明冲突；`HistoryPlan`/`CalibrationShape` 二义/不完整类型；核函数无匹配重载；ld.lld "unknown file type"；生成的 `host_stub.cpp` 里 `AscendC`、`kTilingBytes` 未声明。
331: - **G14~G24 校准期**：rotations 下载 SSL 自签名证书失败；c10 OpenMP "Invalid thread pool!"（EngineCore 起不来）；`liboscar_ascend_kernels.so` dlopen 失败；"two-pass sample identity" 两遍校准 Q/K/V 指纹不一致（delta 0.33~2.0）；空闲显存 15.75/29.49 GiB 低于 0.9 利用率需求；npu-smi 显存字段解析不出 → 等待释放死循环（HBM 实占 ~29.6/32 GB）；NPU eigensolver 校验数值超阈。
332: - **G25~G34 首批算子测试**：`Tensor-likes are not close!/not equal!`（最大绝对差 0.906、相对差 808）；`eigensolver_known_spectrum(8/64/128)` 特征值误差 7.90/71.14/139.44；`lse_max_abs_error=Infinity`；一轮 300s 超时被 SIGTERM。
333: 
334: ### 逐条详情（原文全文，零截断）
[...]
2304: <!-- ENTRY src=gh idx=14 id=5664352166 chars=1371 -->
2305: 
2306: **一行结论**：进入新阶段即报错：prepare-rotations 下载 rotations.pt 失败——urlopen SSL CERTIFICATE_VERIFY_FAILED（自签名证书链）
2307: 
2308: ### 关键报错信息（原文整行摘录，未折行/未截断）
2309: `````text
2310: [oscar-ascendc] FAILED phase=prepare-rotations: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1010)>
2311: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260914T125327339013Z/status.json
2312: `````
[...]
2330: [oscar-ascendc] configure; log: /workspace/codex_oscar_c/logs/20260914T125327339013Z/configure.log
2331: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260914T125327339013Z/build.log
2332: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
2333: [oscar-ascendc] FAILED phase=prepare-rotations: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1010)>
2334: Full logs: /workspace/codex_oscar_c/logs/20260914T125327339013Z
2335: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260914T125327339013Z/status.json
[...]
2340: <!-- ENTRY src=gh idx=15 id=5672668103 chars=17200 -->
2341: 
2342: **一行结论**：prepare-rotations SSL 错误仍在 + native-calibration 失败：c10 pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 … Invalid thread pool!
2343: 
2344: ### 关键报错信息（原文整行摘录，未折行/未截断）
2345: `````text
2346: [oscar-ascendc] FAILED phase=prepare-rotations: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1010)>
2347: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260914T125327339013Z/status.json
2348: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/4431cd9ab760cbc1d3eb36a282770a3100e28b0669697d0cb4693fbe78e6d024/.prepare-qbag8el9/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/4431cd9ab760cbc1d3eb36a282770a3100e28b0669697d0cb4693fbe78e6d024/.prepare-qbag8el9/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260914T125808041310Z/native-calibration.log
2349: [oscar-ascendc] ----- error context -----
2350:     40| terminate called after throwing an instance of 'c10::Error'
[...]
2382: [oscar-ascendc] configure; log: /workspace/codex_oscar_c/logs/20260914T125327339013Z/configure.log
2383: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260914T125327339013Z/build.log
2384: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
2385: [oscar-ascendc] FAILED phase=prepare-rotations: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1010)>
2386: Full logs: /workspace/codex_oscar_c/logs/20260914T125327339013Z
2387: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260914T125327339013Z/status.json
[...]
2398:  configs/calibration.json                    |    3 +-
2399:  configs/calibration_corpus/README.md        |   14 +
2400:  configs/calibration_corpus/gpqa_diamond.csv | 9429 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
2401:  oscar_ascend/calibration_data.py            |    8 +-
2402:  4 files changed, 9452 insertions(+), 2 deletions(-)
2403:  create mode 100644 configs/calibration_corpus/README.md
2404:  create mode 100644 configs/calibration_corpus/gpqa_diamond.csv
2405: [oscar-ascendc] install; log: /workspace/codex_oscar_c/logs/20260914T125808041310Z/install.log
2406: [oscar-ascendc] configure; log: /workspace/codex_oscar_c/logs/20260914T125808041310Z/configure.log
2407: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260914T125808041310Z/build.log
2408: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
2409: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260914T125808041310Z/native-calibration.log
2410: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/4431cd9ab760cbc1d3eb36a282770a3100e28b0669697d0cb4693fbe78e6d024/.prepare-qbag8el9/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/4431cd9ab760cbc1d3eb36a282770a3100e28b0669697d0cb4693fbe78e6d024/.prepare-qbag8el9/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260914T125808041310Z/native-calibration.log
2411: Full logs: /workspace/codex_oscar_c/logs/20260914T125808041310Z
2412: 
[...]
2566: ### 关键报错信息（原文整行摘录，未折行/未截断）
2567: `````text
2568: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/e64d222908ff050cef05be7809f2b805860e4850372930ae889228b88b5df435/.prepare-uvc4xrv0/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/e64d222908ff050cef05be7809f2b805860e4850372930ae889228b88b5df435/.prepare-uvc4xrv0/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T001247441131Z/native-calibration.log
2569: [oscar-ascendc] ----- error context -----
2570:     41| terminate called after throwing an instance of 'c10::Error'
[...]
2586: [oscar-ascendc] configure; log: /workspace/codex_oscar_c/logs/20260915T001247441131Z/configure.log
2587: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T001247441131Z/build.log
2588: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
2589: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T001247441131Z/native-calibration.log
2590: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/e64d222908ff050cef05be7809f2b805860e4850372930ae889228b88b5df435/.prepare-uvc4xrv0/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/e64d222908ff050cef05be7809f2b805860e4850372930ae889228b88b5df435/.prepare-uvc4xrv0/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T001247441131Z/native-calibration.log
2591: Full logs: /workspace/codex_oscar_c/logs/20260915T001247441131Z
2592: 
[...]
2737: ### 关键报错信息（原文整行摘录，未折行/未截断）
2738: `````text
2739: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-bofuiz32/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-bofuiz32/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T001834379751Z/native-calibration.log
2740: [oscar-ascendc] ----- error context -----
2741:     44| terminate called after throwing an instance of 'c10::Error'
[...]
2790: [oscar-ascendc] configure; log: /workspace/codex_oscar_c/logs/20260915T001834379751Z/configure.log
2791: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T001834379751Z/build.log
2792: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
2793: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T001834379751Z/native-calibration.log
2794: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-bofuiz32/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-bofuiz32/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T001834379751Z/native-calibration.log
2795: Full logs: /workspace/codex_oscar_c/logs/20260915T001834379751Z
2796: 
[...]
2963: ### 关键报错信息（原文整行摘录，未折行/未截断）
2964: `````text
2965: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-t53jethu/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-t53jethu/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T003755438613Z/native-calibration.log
2966: [oscar-ascendc] ----- error context -----
2967:    432| ERROR 09-15 00:46:12 [multiproc_executor.py:987]                    ^^^^^^^^^^^^^^^^^^^^^^^^^
[...]
3023: [oscar-ascendc] configure; log: /workspace/codex_oscar_c/logs/20260915T003755438613Z/configure.log
3024: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T003755438613Z/build.log
3025: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3026: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T003755438613Z/native-calibration.log
3027: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-t53jethu/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/e3da650c7009818124727e12b442a1204d413e44b4403c0e5e317b90e94c62d4/.prepare-t53jethu/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T003755438613Z/native-calibration.log
3028: Full logs: /workspace/codex_oscar_c/logs/20260915T003755438613Z
3029: 
[...]
3232: ### 关键报错信息（原文整行摘录，未折行/未截断）
3233: `````text
3234: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/00dc474f3ac5a0847430dc1da8321a3b2dff9174141696794cb5613b0ce5675c/.prepare-4j4x9qjd/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/00dc474f3ac5a0847430dc1da8321a3b2dff9174141696794cb5613b0ce5675c/.prepare-4j4x9qjd/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T005053919953Z/native-calibration.log
3235: [oscar-ascendc] ----- error context -----
3236:    523| ERROR 09-15 00:59:31 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 61, in oscar_calibration_agree
[...]
3294: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T005053919953Z/build.log
3295: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
3296: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3297: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T005053919953Z/native-calibration.log
3298: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/00dc474f3ac5a0847430dc1da8321a3b2dff9174141696794cb5613b0ce5675c/.prepare-4j4x9qjd/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/00dc474f3ac5a0847430dc1da8321a3b2dff9174141696794cb5613b0ce5675c/.prepare-4j4x9qjd/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T005053919953Z/native-calibration.log
3299: Full logs: /workspace/codex_oscar_c/logs/20260915T005053919953Z
3300: 
[...]
3431: ### 关键报错信息（原文整行摘录，未折行/未截断）
3432: `````text
3433: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/b25f943e2a10b2040a7a0402ae826939aa2f9f78d539a42b7ca19584547dc589/.prepare-qmoko0tj/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/b25f943e2a10b2040a7a0402ae826939aa2f9f78d539a42b7ca19584547dc589/.prepare-qmoko0tj/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T011047696189Z/native-calibration.log
3434: [oscar-ascendc] ----- error context -----
3435:    529| ERROR 09-15 01:19:13 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
[...]
3492: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T011047696189Z/build.log
3493: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
3494: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3495: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T011047696189Z/native-calibration.log
3496: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/b25f943e2a10b2040a7a0402ae826939aa2f9f78d539a42b7ca19584547dc589/.prepare-qmoko0tj/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/b25f943e2a10b2040a7a0402ae826939aa2f9f78d539a42b7ca19584547dc589/.prepare-qmoko0tj/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T011047696189Z/native-calibration.log
3497: Full logs: /workspace/codex_oscar_c/logs/20260915T011047696189Z
3498: 
[...]
3635: ### 关键报错信息（原文整行摘录，未折行/未截断）
3636: `````text
3637: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-70z2sq20/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-70z2sq20/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T013134680378Z/native-calibration.log
3638: [oscar-ascendc] ----- error context -----
3639:     89| (Worker pid=63814) ERROR 09-15 01:34:41 [multiproc_executor.py:888]                   ^^^^^^^^^^^^^^^^^^^
[...]
3670: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T013134680378Z/build.log
3671: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
3672: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3673: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T013134680378Z/native-calibration.log
3674: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-70z2sq20/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-70z2sq20/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T013134680378Z/native-calibration.log
3675: Full logs: /workspace/codex_oscar_c/logs/20260915T013134680378Z
3676: 
[...]
3786: <!-- ENTRY src=gh idx=22 id=5673467244 chars=7393 -->
3787: 
3788: **一行结论**：prepare-rotations 卡在等待释放死循环：npu-smi memory field not recognized（npu 4~7）；用户 Ctrl-C 后贴 npu-smi info——8×910B4，各卡 HBM 已占 ~29.6/32 GB
3789: 
3790: ### 关键报错信息（原文整行摘录，未折行/未截断）
3791: `````text
3792: ^C[oscar-ascendc] FAILED phase=prepare-rotations:
3793: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260915T014329723204Z/status.json
3794: `````
[...]
3808: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T014329723204Z/build.log
3809: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
3810: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3811: [oscar-ascendc] task devices below the calibration free-memory threshold; waiting for release: [{'npu': 4, 'reason': 'npu-smi memory field not recognized'}, {'npu': 5, 'reason': 'npu-smi memory field not recognized'}, {'npu': 6, 'reason': 'npu-smi memory field not recognized'}, {'npu': 7, 'reason': 'npu-smi memory field not recognized'}]
3812: ^C[oscar-ascendc] FAILED phase=prepare-rotations: 
3813: Full logs: /workspace/codex_oscar_c/logs/20260915T014329723204Z
3814: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260915T014329723204Z/status.json
[...]
3871: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T014556949674Z/build.log
3872: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
3873: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3874: [oscar-ascendc] task devices below the calibration free-memory threshold; waiting for release: [{'npu': 4, 'reason': 'npu-smi memory field not recognized'}, {'npu': 5, 'reason': 'npu-smi memory field not recognized'}, {'npu': 6, 'reason': 'npu-smi memory field not recognized'}, {'npu': 7, 'reason': 'npu-smi memory field not recognized'}]
3875: 
[...]
3884: ### 关键报错信息（原文整行摘录，未折行/未截断）
3885: `````text
3886: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-39ix4a8q/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-39ix4a8q/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T015421878029Z/native-calibration.log
3887: [oscar-ascendc] ----- error context -----
3888:    535| ERROR 09-15 02:02:49 [multiproc_executor.py:987]     raise RuntimeError(f"{label}: {local_error or 'another TP rank failed validation'}")
[...]
3939: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T015421878029Z/build.log
3940: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
3941: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
3942: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T015421878029Z/native-calibration.log
3943: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-39ix4a8q/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/34f1e81529d6ad7a3d5ba597a2c76dd459af3a36182fd7cff827d559e4f2d357/.prepare-39ix4a8q/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T015421878029Z/native-calibration.log
3944: Full logs: /workspace/codex_oscar_c/logs/20260915T015421878029Z
3945: 
[...]
4078: <!-- ENTRY src=gh idx=24 id=5673718926 chars=20572 -->
4079: 
4080: **一行结论**：native-calibration：a TP rank failed NPU eigensolver validation at layers.11.self_attn.attn/k：local=[0.0, 32.0, 0.1817, 23.25, 5.05, 208.05, 208.05, 4.0]（数值超阈）
4081: 
4082: ### 关键报错信息（原文整行摘录，未折行/未截断）
4083: `````text
4084: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/d081d7975726d6a3a9b0904a71ab1340b0daf884803334488a7d9c3e0c167590/.prepare-b8_w_8q6/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/d081d7975726d6a3a9b0904a71ab1340b0daf884803334488a7d9c3e0c167590/.prepare-b8_w_8q6/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T020711166171Z/native-calibration.log
4085: [oscar-ascendc] ----- error context -----
4086:    515| (Worker_TP0 pid=85083) (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
4087:    516| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4088:    517| (Worker_TP0 pid=85083) (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4089:    518| (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.18173030018806458, 23.246463775634766, 5.052907466888428, 208.05174255371094, 208.05177307128906, 4.0]
4090:    519| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] WorkerProc hit an exception.
4091:    520| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
[...]
4093:    528| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] WorkerProc hit an exception.
4094:    529| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4095:    530| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]
4096:    531| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4097:    532| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] Traceback (most recent call last):
4098:    540| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4099:    541| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4100:    542| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4101:    543| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.18173030018806458, 23.246463775634766, 5.052907466888428, 208.05174255371094, 208.05177307128906, 4.0]
4102:    544| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4103:    545| ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.04314088076353073, 25.810955047607422, 1.460277795791626, 191.0, 63.0, 4.0]
4104:    546| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4105:    547| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]
4106:    551| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4107:    552| ERROR 09-15 02:15:53 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
4108:    553| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4109:    554| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.017421741038560867, 21.9497127532959, 1.5419570207595825, 190.0, 62.0, 4.0]
4110:    555| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4111:    556| ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]
4112:    557| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] Traceback (most recent call last):
4113:    558| ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4114:    562| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4115:    563| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4116:    564| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4117:    565| ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.04314088076353073, 25.810955047607422, 1.460277795791626, 191.0, 63.0, 4.0]
4118:    566| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 305, in oscar_calibration_finish
4119:    567| ERROR 09-15 02:15:53 [multiproc_executor.py:987]
4120:    568| (Worker_TP3 pid=85687) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4121:    569| (Worker_TP3 pid=85687) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.017421741038560867, 21.9497127532959, 1.5419570207595825, 190.0, 62.0, 4.0]
4122:    570| (Worker_TP3 pid=85687) ERROR 09-15 02:15:53 [multiproc_executor.py:987]
4123:    571| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] Invocation of collective_rpc method failed
[...]
4143: [oscar-ascendc] build; log: /workspace/codex_oscar_c/logs/20260915T020711166171Z/build.log
4144: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
4145: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
4146: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260915T020711166171Z/native-calibration.log
4147: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/d081d7975726d6a3a9b0904a71ab1340b0daf884803334488a7d9c3e0c167590/.prepare-b8_w_8q6/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/d081d7975726d6a3a9b0904a71ab1340b0daf884803334488a7d9c3e0c167590/.prepare-b8_w_8q6/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260915T020711166171Z/native-calibration.log
4148: Full logs: /workspace/codex_oscar_c/logs/20260915T020711166171Z
4149: 
[...]
4154:      3| INFO 09-15 02:08:35 [__init__.py:46] - ascend -> vllm_ascend:register
4155:    515| (Worker_TP0 pid=85083) (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
4156:    516| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4157:    517| (Worker_TP0 pid=85083) (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4158:    518| (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.18173030018806458, 23.246463775634766, 5.052907466888428, 208.05174255371094, 208.05177307128906, 4.0]
4159:    519| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] WorkerProc hit an exception.
4160:    520| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
[...]
4162:    528| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] WorkerProc hit an exception.
4163:    529| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4164:    530| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]
4165:    531| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4166:    532| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] Traceback (most recent call last):
4167:    540| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4168:    541| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4169:    542| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4170:    543| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.18173030018806458, 23.246463775634766, 5.052907466888428, 208.05174255371094, 208.05177307128906, 4.0]
4171:    544| (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4172:    545| ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.04314088076353073, 25.810955047607422, 1.460277795791626, 191.0, 63.0, 4.0]
4173:    546| (Worker_TP1 pid=85270) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4174:    547| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987] 
4175:    551| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4176:    552| ERROR 09-15 02:15:53 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
4177:    553| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4178:    554| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.017421741038560867, 21.9497127532959, 1.5419570207595825, 190.0, 62.0, 4.0]
4179:    555| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4180:    556| ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]
4181:    557| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) (Worker_TP0 pid=85083) ERROR 09-15 02:15:53 [multiproc_executor.py:987] Traceback (most recent call last):
4182:    558| ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4183:    562| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
4184:    563| ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4185:    564| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
4186:    565| ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.04314088076353073, 25.810955047607422, 1.460277795791626, 191.0, 63.0, 4.0]
4187:    566| (Worker_TP3 pid=85687) (Worker_TP2 pid=85477) ERROR 09-15 02:15:53 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 305, in oscar_calibration_finish
4188:    567| ERROR 09-15 02:15:53 [multiproc_executor.py:987] 
4189:    568| (Worker_TP3 pid=85687) ERROR 09-15 02:15:53 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
4190:    569| (Worker_TP3 pid=85687) ERROR 09-15 02:15:53 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.017421741038560867, 21.9497127532959, 1.5419570207595825, 190.0, 62.0, 4.0]
4191:    570| (Worker_TP3 pid=85687) ERROR 09-15 02:15:53 [multiproc_executor.py:987] 
4192:    571| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] Invocation of collective_rpc method failed
[...]
4194:    596| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
4195:    597| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413]     raise RuntimeError(
4196:    598| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]', please check the stack trace above for the root cause
4197:    599| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] Invocation of collective_rpc method failed
4198:    600| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] Traceback (most recent call last):
[...]
4200:    624| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
4201:    625| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413]     raise RuntimeError(
4202:    626| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.18173030018806458, 23.246463775634766, 5.052907466888428, 208.05174255371094, 208.05177307128906, 4.0]', please check the stack trace above for the root cause
4203:    627| INFO 09-15 02:15:53 [core_client.py:652] [shutdown] MPClient: start timeout=60s
4204:    628| INFO 09-15 02:15:53 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
4224:    624| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
4225:    625| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413]     raise RuntimeError(
4226:    626| (EngineCore pid=84850) ERROR 09-15 02:15:53 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.18173030018806458, 23.246463775634766, 5.052907466888428, 208.05174255371094, 208.05177307128906, 4.0]', please check the stack trace above for the root cause
4227:    627| INFO 09-15 02:15:53 [core_client.py:652] [shutdown] MPClient: start timeout=60s
4228:    628| INFO 09-15 02:15:53 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
4262:    662|   File "/usr/local/python3.12.13/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
4263:    663|     raise self._exception
4264:    664| Exception: Call to collective_rpc method failed: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]', please check the stack trace above for the root cause
4265:    665| {"status": "calibration_failed", "error": "Call to collective_rpc method failed: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/k: local=[0.0, 32.0, 0.3128969371318817, 17.361129760742188, 1.5416613817214966, 191.0, 63.0, 4.0]', please check the stack trace above for the root cause"}
4266: [oscar-ascendc] ===== end native-calibration.log =====
4267: 
[...]
4437:      5|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
4438:      6|   "model_graph": "not_run",
4439:      7|   "model_accuracy": "not_run",
4440:      8|   "performance": "not_run",
4441:      9|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
4626:    609|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
4627:    610|   "model_graph": "not_run",
4628:    611|   "model_accuracy": "not_run",
4629:    612|   "performance": "not_run",
4630:    613|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
4657: <!-- ENTRY src=gh idx=28 id=5690165913 chars=8399 -->
4658: 
4659: **一行结论**：operators-quick：报告汇总 history_attention(64/128/256×q_len1~4) 全失败 + eigensolver_known_spectrum(8/64/128) eigenvalue_max_abs_error 7.90/71.14/139.44 + stage_and_prefix_restore(256)
4660: 
4661: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
4665:   1132|       "eigenvalue_max_abs_error": 71.13726043701172,
4666:   1150|       "eigenvalue_max_abs_error": 139.4446563720703,
4667:   1160|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
4668: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260916T001956363279Z/status.json
4669: `````
[...]
4731:   1099|     },
4732:   1100|     {
4733:   1101|       "name": "eigensolver_known_spectrum",
4734:   1102|       "dim": 8,
4735:   1103|       "status": "failed",
[...]
4745:   1113|       ],
4746:   1114|       "eigenvalue_max_abs_error": 7.8952412605285645,
4747:   1115|       "rotation_orthogonality": 12.370697975158691,
4748:   1116|       "eigenpair_residual": 69.82677459716797
4749:   1117|     },
4750:   1118|     {
4751:   1119|       "name": "eigensolver_known_spectrum",
4752:   1120|       "dim": 64,
4753:   1121|       "status": "failed",
[...]
4763:   1131|       ],
4764:   1132|       "eigenvalue_max_abs_error": 71.13726043701172,
4765:   1133|       "rotation_orthogonality": 1.946983814239502,
4766:   1134|       "eigenpair_residual": 53.44618606567383
4767:   1135|     },
4768:   1136|     {
4769:   1137|       "name": "eigensolver_known_spectrum",
4770:   1138|       "dim": 128,
4771:   1139|       "status": "failed",
[...]
4781:   1149|       ],
4782:   1150|       "eigenvalue_max_abs_error": 139.4446563720703,
4783:   1151|       "rotation_orthogonality": 0.6758062243461609,
4784:   1152|       "eigenpair_residual": 128.8831787109375
4785:   1153|     }
[...]
4787:   1155|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
4788:   1156|   "model_graph": "not_run",
4789:   1157|   "model_accuracy": "not_run",
4790:   1158|   "performance": "not_run",
4791:   1159|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
4792:   1160|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
4793:   1161| }
4794: [oscar-ascendc] ----- aux log /workspace/codex_oscar_c/build/ascendc/oscar_ascend_kernels_host-prefix/src/oscar_ascend_kernels_host-build/install_manifest.txt (last 40 lines) -----
[...]
4819: `````text
4820: [oscar-ascendc] FAILED phase=operators-quick: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.probe', '--library', '/workspace/codex_oscar_c/build/ascendc/liboscar_ascend_ops.so', '--output', '/workspace/codex_oscar_c/logs/20260916T003422808952Z/operators-quick']; full log: /workspace/codex_oscar_c/logs/20260916T003422808952Z/operators-quick.log
4821:   1401|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
4822: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260916T003422808952Z/status.json
4823: `````
[...]
4890:   1344|     },
4891:   1345|     {
4892:   1346|       "name": "forensics_eigh_single_rotation",
4893:   1347|       "dim": 8,
4894:   1348|       "diagnostic": [
[...]
4942:   1396|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
4943:   1397|   "model_graph": "not_run",
4944:   1398|   "model_accuracy": "not_run",
4945:   1399|   "performance": "not_run",
4946:   1400|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
4947:   1401|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
4948:   1402| }
4949: [oscar-ascendc] ----- aux log /workspace/codex_oscar_c/build/ascendc/oscar_ascend_kernels_host-prefix/src/oscar_ascend_kernels_host-build/install_manifest.txt (last 40 lines) -----
[...]
4986:     13| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 3, "splits": 3, "max_abs_error": 0.09390450268983841, "per_token_max_abs_error": [0.0939, 0.08776, 0.08637, 0.00027, 0.00028, 0.00029], "lse_max_abs_error": Infinity, "workspace_bytes": 13 ...<middle clipped>... Infinity, 0.0035, 3.1366, -Infinity], "request1_max_abs_error": 0.07119952142238617, "request1_lse": [-Infinity, 0.0, -Infinity, -Infinity, -Infinity, 0.0, 3.6604, -Infinity, -Infinity, 3.668, 0.0, -Infinity, 0.0, 0.0, 3.6874, 0.0, 3.6839, 3.6845]}, "worst_token": 0, "worst_sample": {"position": 20, "actual": [-0.00598, -0.00348, -0.02101], "reference": [-0.04494, -0.09739, -0.05527], "actual_lse": [-Infinity, -Infinity, 3.03323, -0.01825], "reference_lse": [3.05467, 3.04568, 3.03323, 3.04598]}}
4987:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.2474944293498993, "per_token_max_abs_error": [0.08117, 0.07657, 0.24749, 0.14427, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "wo ...<middle clipped>... _max_abs_error": 0.07619991898536682, "request1_lse": [3.6052, 3.6123, 0.0, 0.1677, -0.0826, -0.099, 3.6379, -0.0308, -Infinity, 0.0124, -Infinity, -Infinity, -0.1829, 3.6663, 0.1594, 0.0851, -0.0421, 3.6676, 0.0865, -Infinity, 0.2273, -0.396, -0.0314, -Infinity]}, "worst_token": 2, "worst_sample": {"position": 21, "actual": [0.20151, -0.05587, -0.01137], "reference": [-0.04598, -0.07889, -0.05829], "actual_lse": [-Infinity, 0.0, 0.0, 0.0], "reference_lse": [3.10555, 3.09151, 3.09309, 3.09648]}}
4988:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [0.0, 32.0, 0.001356137334369123, 10.950979232788086, 1.7010799646377563, 8.56676959991455, 8.566770553588867, 4.0], "eigenvalue_max_abs_error": 8.449307441711426, "rotation_orthogonality": 16.647916793823242, "eigenpair_residual": 30.1107177734375}
4989:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.04002726078033447, 64.40208435058594, 0.8674041032791138, 45.0, 13.0, 4.0], "eigenvalue_max_abs_error": 69.73066711425781, "rotation_orthogonality": 0.48579269647598267, "eigenpair_residual": 56.68622589111328}
4990:     18| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.1957131028175354, 79.8985595703125, 1.4636231660842896, 377.9741516113281, 377.97412109375, 4.0], "eigenvalue_max_abs_error": 139.0587921142578, "rotation_orthogonality": 3.5218372344970703, "eigenpair_residual": 965.84814453125}
4991:   1401|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
4992: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260916T003911865364Z/status.json
4993: `````
[...]
5034:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.2474944293498993, "per_token_max_abs_error": [0.08117, 0.07657, 0.24749, 0.14427, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "wo ...<middle clipped>... _max_abs_error": 0.07619991898536682, "request1_lse": [3.6052, 3.6123, 0.0, 0.1677, -0.0826, -0.099, 3.6379, -0.0308, -Infinity, 0.0124, -Infinity, -Infinity, -0.1829, 3.6663, 0.1594, 0.0851, -0.0421, 3.6676, 0.0865, -Infinity, 0.2273, -0.396, -0.0314, -Infinity]}, "worst_token": 2, "worst_sample": {"position": 21, "actual": [0.20151, -0.05587, -0.01137], "reference": [-0.04598, -0.07889, -0.05829], "actual_lse": [-Infinity, 0.0, 0.0, 0.0], "reference_lse": [3.10555, 3.09151, 3.09309, 3.09648]}}
5035:     15| CHECK {"name": "stage_and_prefix_restore", "head_dim": 256, "status": "failed", "failures": ["staged values differ: Mismatched elements: 2044 / 2048 (99.8%); Greatest absolute difference: 0.90625 at index (2, 0, 178); Greatest relative difference: 808.0 at index (4, 0, 169)"], "lossy_rows_on_eviction": 12}
5036:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [0.0, 32.0, 0.001356137334369123, 10.950979232788086, 1.7010799646377563, 8.56676959991455, 8.566770553588867, 4.0], "eigenvalue_max_abs_error": 8.449307441711426, "rotation_orthogonality": 16.647916793823242, "eigenpair_residual": 30.1107177734375}
5037:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.04002726078033447, 64.40208435058594, 0.8674041032791138, 45.0, 13.0, 4.0], "eigenvalue_max_abs_error": 69.73066711425781, "rotation_orthogonality": 0.48579269647598267, "eigenpair_residual": 56.68622589111328}
5038:     18| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.1957131028175354, 79.8985595703125, 1.4636231660842896, 377.9741516113281, 377.97412109375, 4.0], "eigenvalue_max_abs_error": 139.0587921142578, "rotation_orthogonality": 3.5218372344970703, "eigenpair_residual": 965.84814453125}
5039:     19| CHECK {"name": "forensics_stage_only", "owner": [0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0], "per_row_max_abs_diff_after_stage": [0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
5040:     20| CHECK {"name": "forensics_restore_only", "state": [5, 16, 0, 0], "lossy": 0, "window_rows_vs_expected": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, null, null, null, null], "window_row_absolute_max": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0]}
5041:     21| CHECK {"name": "forensics_eigh_diagonal", "dim": 8, "diagnostic": [1.0, 0.0, 0.0, 8.0, Infinity, Infinity, Infinity, 2.0], "eigenvalues": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], "vectors_8x8": [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3.3778807652328923e+22, -3.3778807652328923e+22]]}
5042:     22| CHECK {"name": "forensics_eigh_single_rotation", "dim": 8, "diagnostic": [0.0, 32.0, 6.766607384633971e-06, 10.37387752532959, 3.522202253341675, 106.6173324584961, 106.61734008789062, 4.0], "eigenvalues": [-0.477, -0.244, -0.061, 0.052, 0.53, 2.738, 9.436, 10.374], "expected_top2": [3.0, 1.0], "vectors_first2rows": [[-0.244, 0.0, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0], [-0.0, -0.477, 0.0, 0.0, 0.0, -0.0, -0.0, -0.0]]}
5043:     23| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T003911865364Z/operators-quick/rank_0.json"}
5044: [oscar-ascendc] ===== end operators-quick.log =====
[...]
5081:   1344|     },
5082:   1345|     {
5083:   1346|       "name": "forensics_eigh_single_rotation",
5084:   1347|       "dim": 8,
5085:   1348|       "diagnostic": [
[...]
5133:   1396|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
5134:   1397|   "model_graph": "not_run",
5135:   1398|   "model_accuracy": "not_run",
5136:   1399|   "performance": "not_run",
5137:   1400|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
5138:   1401|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5139:   1402| }
5140: [oscar-ascendc] ----- aux log /workspace/codex_oscar_c/build/ascendc/oscar_ascend_kernels_host-prefix/src/oscar_ascend_kernels_host-build/install_manifest.txt (last 40 lines) -----
[...]
5261:     13| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 3, "splits": 3, "max_abs_error": 0.09738925844430923, "per_token_max_abs_error": [0.09739, 0.0831, 0.08637, 0.00027, 0.00028, 0.00029], "lse_max_abs_error": Infinity, "workspace_bytes": 13 ...<middle clipped>...  0.0, -0.0376, -Infinity, 0.0845, 0.0043, -Infinity, 3.1258, -0.0157, -Infinity, 3.1366, 3.1283], "request1_max_abs_error": 0.07267675548791885, "request1_lse": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.669, -Infinity, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.6839, 0.0]}, "worst_token": 0, "worst_sample": {"position": 20, "actual": [0.0, 0.0, 0.0], "reference": [-0.04494, -0.09739, -0.05527], "actual_lse": [-0.0342, -Infinity, -0.02862, -Infinity], "reference_lse": [3.05467, 3.04568, 3.03323, 3.04598]}}
5262:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.14427033066749573, "per_token_max_abs_error": [0.08117, 0.07502, 0.1428, 0.14427, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "wo ...<middle clipped>... uest1_max_abs_error": 0.04618284851312637, "request1_lse": [-Infinity, 0.0, 0.0, 0.1677, 3.6129, -Infinity, 0.043, -Infinity, 3.6485, 3.6421, -Infinity, 0.2788, -0.1829, 0.0963, 0.1594, 0.0851, -Infinity, -Infinity, 0.0865, 0.0431, 0.2273, 3.6951, -0.0314, 3.6828]}, "worst_token": 3, "worst_sample": {"position": 22, "actual": [0.08464, 0.06991, -0.11195], "reference": [-0.02142, -0.07436, -0.04786], "actual_lse": [0.0, -Infinity, 0.0, 0.0], "reference_lse": [3.13887, 3.12977, 3.12406, 3.13912]}}
5263:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [1.0, 32.0, 6.206837497302331e-07, 10.263310432434082, 4.606581211090088, 104.33554077148438, 104.33554077148438, 4.0], "eigenvalue_max_abs_error": 7.718110084533691, "rotation_orthogonality": 19.549348831176758, "eigenpair_residual": 83.08710479736328}
5264:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.008128796704113483, 62.12407684326172, 0.9693370461463928, 47.0, 15.0, 4.0], "eigenvalue_max_abs_error": 69.70418548583984, "rotation_orthogonality": 0.7028315663337708, "eigenpair_residual": 58.833805084228516}
5265:     18| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.019999440759420395, 130.7913818359375, 0.9263933300971985, 95.0, 31.0, 4.0], "eigenvalue_max_abs_error": 140.62074279785156, "rotation_orthogonality": 2.3389534950256348, "eigenpair_residual": 99.04846954345703}
5266:   1731|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5267: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260916T005809320071Z/status.json
5268: `````
[...]
5307:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.14427033066749573, "per_token_max_abs_error": [0.08117, 0.07502, 0.1428, 0.14427, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "wo ...<middle clipped>... uest1_max_abs_error": 0.04618284851312637, "request1_lse": [-Infinity, 0.0, 0.0, 0.1677, 3.6129, -Infinity, 0.043, -Infinity, 3.6485, 3.6421, -Infinity, 0.2788, -0.1829, 0.0963, 0.1594, 0.0851, -Infinity, -Infinity, 0.0865, 0.0431, 0.2273, 3.6951, -0.0314, 3.6828]}, "worst_token": 3, "worst_sample": {"position": 22, "actual": [0.08464, 0.06991, -0.11195], "reference": [-0.02142, -0.07436, -0.04786], "actual_lse": [0.0, -Infinity, 0.0, 0.0], "reference_lse": [3.13887, 3.12977, 3.12406, 3.13912]}}
5308:     15| CHECK {"name": "stage_and_prefix_restore", "head_dim": 256, "status": "failed", "failures": ["staged values differ: Mismatched elements: 2044 / 2048 (99.8%); Greatest absolute difference: 0.90625 at index (2, 0, 178); Greatest relative difference: 808.0 at index (4, 0, 169)"], "lossy_rows_on_eviction": 12}
5309:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [1.0, 32.0, 6.206837497302331e-07, 10.263310432434082, 4.606581211090088, 104.33554077148438, 104.33554077148438, 4.0], "eigenvalue_max_abs_error": 7.718110084533691, "rotation_orthogonality": 19.549348831176758, "eigenpair_residual": 83.08710479736328}
5310:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.008128796704113483, 62.12407684326172, 0.9693370461463928, 47.0, 15.0, 4.0], "eigenvalue_max_abs_error": 69.70418548583984, "rotation_orthogonality": 0.7028315663337708, "eigenpair_residual": 58.833805084228516}
5311:     18| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.019999440759420395, 130.7913818359375, 0.9263933300971985, 95.0, 31.0, 4.0], "eigenvalue_max_abs_error": 140.62074279785156, "rotation_orthogonality": 2.3389534950256348, "eigenpair_residual": 99.04846954345703}
5312:     19| CHECK {"name": "forensics_stage_only", "owner": [0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0], "per_row_max_abs_diff_after_stage": [0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
5313:     20| CHECK {"name": "forensics_restore_only", "state": [5, 16, 0, 0], "lossy": 0, "window_rows_vs_expected": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, null, null, null, null], "window_row_absolute_max": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0]}
5314:     21| CHECK {"name": "forensics_eigh_diagonal", "dim": 8, "diagnostic": [1.0, 0.0, 0.0, 8.0, Infinity, Infinity, Infinity, 2.0], "eigenvalues": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], "vectors_8x8": [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0 ...<middle clipped>... 0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]], "rotation": [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, -2.388522342972775e+22, 2.388522342972775e+22, 2.388522342972775e+22, -2.388522342972775e+22]]}
5315:     22| CHECK {"name": "forensics_eigh_single_rotation", "dim": 8, "diagnostic": [0.0, 32.0, 6.537394074257463e-05, 10.05366039276123, 4.352434158325195, 100.07608795166016, 100.07608795166016, 4.0], "eigenvalues": [-1.621, -0.676, -0.246, -0.13, 2.099, 3.23 ...<middle clipped>... ace_A_first4": [[178.089, 7.0, 9.486, 9.486, 7.944, 3.0, 0.983, 0.983], [-0.0, -0.13, -0.0, -0.0, 0.0, -0.0, -0.0, -0.001], [0.0, -0.0, 6.88, 0.0, 4621.475, 100.0, 100.076, 100.076], [0.0, -0.0, 0.0, -0.246, 1.73, 144.0, 0.543, 0.543]], "workspace_B_first4": [[-0.265, -0.128, 0.539, -0.506, -0.2, 0.571, 0.02, 0.033], [0.342, 0.3, 0.654, 0.527, -0.269, -0.023, 0.118, 0.005], [-0.007, -0.009, -0.068, -0.09, 0.061, 0.0, 0.991, -0.031], [-0.506, -0.175, -0.406, 0.421, -0.488, 0.363, 0.034, -0.036]]}
5316:     23| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T005809320071Z/operators-quick/rank_0.json"}
5317: [oscar-ascendc] ===== end operators-quick.log =====
[...]
5406:   1726|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
5407:   1727|   "model_graph": "not_run",
5408:   1728|   "model_accuracy": "not_run",
5409:   1729|   "performance": "not_run",
5410:   1730|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
5411:   1731|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5412:   1732| }
5413: [oscar-ascendc] ----- aux log /workspace/codex_oscar_c/build/ascendc/oscar_ascend_kernels_host-prefix/src/oscar_ascend_kernels_host-build/install_manifest.txt (last 40 lines) -----
[...]
5457:     13| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 3, "splits": 3, "max_abs_error": 0.09266635775566101, "per_token_max_abs_error": [0.09267, 0.08813, 0.08413, 0.00027, 0.00028, 0.00029], "lse_max_abs_error": Infinity, "workspace_bytes": 1 ...<middle clipped>... ity, -0.0968, 0.1404, 0.1843, -0.0883, 0.5244, -Infinity], "request1_max_abs_error": 0.07415026426315308, "request1_lse": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -Infinity, -Infinity, 3.669, 0.0124, -0.1414, 0.2788, -0.1829, 0.0963, 0.1594, 3.6697, -Infinity, 3.6845]}, "worst_token": 0, "worst_sample": {"position": 20, "actual": [-0.00543, -0.00348, -0.01918], "reference": [-0.04722, -0.09614, -0.05678], "actual_lse": [0.0, 0.0, -Infinity, 3.04599], "reference_lse": [3.05467, 3.04568, 3.03323, 3.04598]}}
5458:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.10107141733169556, "per_token_max_abs_error": [0.10107, 0.09536, 0.08878, 0.08519, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "w ...<middle clipped>... .1417, 0.437], "request1_max_abs_error": 0.07619991898536682, "request1_lse": [-Infinity, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -Infinity, -0.0379, 3.6421, 0.0827, 0.0018, -Infinity, -0.046, -0.0179, 0.0032, 0.0384, -0.0389, 3.6831, 0.0137, -Infinity, 0.014, -0.0343, -0.0206]}, "worst_token": 0, "worst_sample": {"position": 19, "actual": [-0.00011, 0.00272, 0.00297], "reference": [-0.04086, -0.09835, -0.03594], "actual_lse": [0.0, 0.0, 0.0, 3.00609], "reference_lse": [2.9922, 2.97853, 2.9961, 3.00609]}}
5459:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [0.0, 32.0, 4.235400047036819e-05, 9.844669342041016, 1.022064447402954, 15.365175247192383, 15.365175247192383, 4.0], "eigenvalue_max_abs_error": 8.010442733764648, "rotation_orthogonality": 14.63931655883789, "eigenpair_residual": 82.03277587890625}
5460:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.009135013446211815, 41.70900344848633, 0.8844026923179626, 46.0, 14.0, 4.0], "eigenvalue_max_abs_error": 71.27883911132812, "rotation_orthogonality": 0.7090206146240234, "eigenpair_residual": 39.58089828491211}
5461:     18| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.004507057368755341, 144.95187377929688, 2.5757856369018555, 21010.10546875, 21010.103515625, 4.0], "eigenvalue_max_abs_error": 138.4685516357422, "rotation_orthogonality": 165.45921325683594, "eigenpair_residual": 2237.6796875}
5462:   2247|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5463: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260916T010353698213Z/status.json
5464: `````
[...]
5480:  oscar_ascend/calibration_data.py    |  4 ++--
5481:  oscar_ascend/calibration_worker.py  | 59 +++++++++++++++++++++++++++++++++++++++++++++--------------
5482:  oscar_ascend/prepare_rotations.py   | 10 ++++++----
5483:  oscar_ascend/probe.py               | 43 +++++++++++++++++++++++++++++++++++++++++++
5484:  tests/test_calibration_contracts.py |  2 +-
[...]
5509:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.10107141733169556, "per_token_max_abs_error": [0.10107, 0.09536, 0.08878, 0.08519, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "w ...<middle clipped>... .1417, 0.437], "request1_max_abs_error": 0.07619991898536682, "request1_lse": [-Infinity, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -Infinity, -0.0379, 3.6421, 0.0827, 0.0018, -Infinity, -0.046, -0.0179, 0.0032, 0.0384, -0.0389, 3.6831, 0.0137, -Infinity, 0.014, -0.0343, -0.0206]}, "worst_token": 0, "worst_sample": {"position": 19, "actual": [-0.00011, 0.00272, 0.00297], "reference": [-0.04086, -0.09835, -0.03594], "actual_lse": [0.0, 0.0, 0.0, 3.00609], "reference_lse": [2.9922, 2.97853, 2.9961, 3.00609]}}
5510:     15| CHECK {"name": "stage_and_prefix_restore", "head_dim": 256, "status": "failed", "failures": ["staged values differ: Mismatched elements: 2044 / 2048 (99.8%); Greatest absolute difference: 0.90625 at index (2, 0, 178); Greatest relative difference: 808.0 at index (4, 0, 169)"], "lossy_rows_on_eviction": 12}
5511:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [0.0, 32.0, 4.235400047036819e-05, 9.844669342041016, 1.022064447402954, 15.365175247192383, 15.365175247192383, 4.0], "eigenvalue_max_abs_error": 8.010442733764648, "rotation_orthogonality": 14.63931655883789, "eigenpair_residual": 82.03277587890625}
5512:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.009135013446211815, 41.70900344848633, 0.8844026923179626, 46.0, 14.0, 4.0], "eigenvalue_max_abs_error": 71.27883911132812, "rotation_orthogonality": 0.7090206146240234, "eigenpair_residual": 39.58089828491211}
5513:     18| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.004507057368755341, 144.95187377929688, 2.5757856369018555, 21010.10546875, 21010.103515625, 4.0], "eigenvalue_max_abs_error": 138.4685516357422, "rotation_orthogonality": 165.45921325683594, "eigenpair_residual": 2237.6796875}
5514:     19| CHECK {"name": "forensics_stage_only", "owner": [0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0], "per_row_max_abs_diff_after_stage": [0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
5515:     20| CHECK {"name": "forensics_restore_only", "state": [5, 16, 0, 0], "lossy": 0, "window_rows_vs_expected": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, null, null, null, null], "window_row_absolute_max": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0]}
5516:     21| CHECK {"name": "forensics_eigh_diagonal", "dim": 8, "diagnostic": [1.0, 0.0, 0.0, 8.0, 0.30372506380081177, 4.0, 0.9303445219993591, 4.0], "eigenvalues": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], "vectors_8x8": [[-0.328, 0.108, -0.079, 0.193, -0.039, ...<middle clipped>... ], "rotation": [[-0.195, 0.078, -0.294, -0.206, 0.07, -0.306, 0.01, -0.085], [0.141, 0.033, 0.132, 0.199, -0.109, -0.341, 0.332, 0.648], [0.235, 0.236, 0.069, -0.12, -0.273, -0.172, -0.1, 0.123], [-0.325, -0.11, -0.023, -0.008, 0.113, 0.237, 0.173, 0.056], [0.04, -0.049, -0.168, 0.05, -0.236, 0.039, -0.008, 0.076], [0.089, 0.052, 0.003, -0.101, -0.061, -0.118, -0.062, 0.165], [-0.097, 0.122, 0.199, 0.137, -0.098, 0.048, 0.008, -0.01], [-0.084, 0.001, 0.21, 0.278, -0.045, 0.062, -0.038, -0.052]]}
5517:     22| CHECK {"name": "forensics_eigh_single_rotation", "dim": 8, "diagnostic": [1.0, 24.0, 3.2060771815167755e-09, 10.007521629333496, 0.23482568562030792, 5.0, 1.0, 4.0], "eigenvalues": [-0.325, -0.268, -0.1, 0.109, 0.232, 0.269, 7.002, 10.008], "expected ...<middle clipped>...  -0.0, 0.0, -0.0]], "workspace_A_first4": [[7.0, 3.0, 5.0, 1.0, 0.339, 3.0, 0.894, 0.894], [0.0, -0.325, -0.0, -0.0, 3.357, 64.0, 0.946, 0.946], [5.513, 81.0, 0.928, 0.928, -0.0, 0.0, 0.0, -0.0], [-0.0, -0.0, 0.0, 0.232, 0.04, 144.0, 0.99, 0.99]], "workspace_B_first4": [[-0.149, 0.018, 0.021, 0.855, -0.183, 0.462, -0.004, -0.009], [0.822, 0.438, 0.0, 0.19, 0.311, 0.019, 0.001, -0.002], [-0.0, 0.0, 0.0, 0.005, -0.005, -0.003, 1.0, 0.0], [0.044, -0.204, 0.012, -0.368, 0.343, 0.838, 0.006, 0.008]]}
5518:     23| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T010353698213Z/operators-quick/rank_0.json"}
5519: [oscar-ascendc] ===== end operators-quick.log =====
[...]
5608:   2242|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
5609:   2243|   "model_graph": "not_run",
5610:   2244|   "model_accuracy": "not_run",
5611:   2245|   "performance": "not_run",
5612:   2246|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
5613:   2247|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); stage_and_prefix_restore(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5614:   2248| }
5615: [oscar-ascendc] ----- aux log /workspace/codex_oscar_c/build/ascendc/oscar_ascend_kernels_host-prefix/src/oscar_ascend_kernels_host-build/install_manifest.txt (last 40 lines) -----
[...]
5693:     13| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 3, "splits": 3, "max_abs_error": 0.09390450268983841, "per_token_max_abs_error": [0.0939, 0.08869, 0.08637, 0.03922, 0.03872, 0.03919], "lse_max_abs_error": Infinity, "workspace_bytes": 13 ...<middle clipped>... 5562936067581, "request1_lse_max_abs_error": Infinity, "request1_lse_invalid_heads": 3, "request1_lse": [-Infinity, 0.0, -Infinity, 0.0, -Infinity, 0.0, 3.6604, 3.6608, -0.1272, 0.0124, -0.1414, 0.2788, -0.1829, 0.0963, 0.1594, 0.0851, -0.0421, 3.6845]}, "worst_token": 0, "worst_sample": {"position": 20, "actual": [-0.00598, -0.00348, -0.02101], "reference": [-0.04494, -0.09739, -0.05527], "actual_lse": [3.05466, -Infinity, 0.0, -Infinity], "reference_lse": [3.05467, 3.04568, 3.03323, 3.04598]}}
5694:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.09826861321926117, "per_token_max_abs_error": [0.06732, 0.09827, 0.0893, 0.08328, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "wo ...<middle clipped>... finity, "request1_lse_invalid_heads": 4, "request1_lse": [-Infinity, 0.0, 0.0, 0.0, 0.0, 0.0, -Infinity, 0.0, -0.0379, -0.0104, 0.0827, 0.0018, -0.1071, -Infinity, -0.0179, 0.0032, 0.0384, -0.0389, 0.0266, -Infinity, 0.0281, 0.014, -0.0343, -0.0206]}, "worst_token": 1, "worst_sample": {"position": 20, "actual": [-0.00428, -0.00318, -0.01993], "reference": [-0.04533, -0.10145, -0.05469], "actual_lse": [-Infinity, 3.04281, 3.69425, -Infinity], "reference_lse": [3.03853, 3.0428, 3.03703, 3.03647]}}
5695:     15| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [0.0, 32.0, 0.0017188957426697016, 8.664765357971191, 2.7871901988983154, 24.64197540283203, 24.64197540283203, 4.0], "eigenvalue_max_abs_error": 8.347458839416504, "rotation_orthogonality": 14.13027572631836, "eigenpair_residual": 87.11943817138672}
5696:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.026881039142608643, 48.8866081237793, 1.007185459136963, 47.0, 28.78778076171875, 4.0], "eigenvalue_max_abs_error": 68.64413452148438, "rotation_orthogonality": 1.2790820598602295, "eigenpair_residual": 84.73745727539062}
5697:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.0037972615100443363, 117.559326171875, 1.0219292640686035, 129.12066650390625, 129.1206817626953, 4.0], "eigenvalue_max_abs_error": 138.7627716064453, "rotation_orthogonality": 2.3519809246063232, "eigenpair_residual": 135.701171875}
5698:   2293|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5699: [oscar-ascendc] result: /workspace/codex_oscar_c/logs/20260916T010855698115Z/status.json
5700: `````
[...]
5739:     13| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 3, "splits": 3, "max_abs_error": 0.09390450268983841, "per_token_max_abs_error": [0.0939, 0.08869, 0.08637, 0.03922, 0.03872, 0.03919], "lse_max_abs_error": Infinity, "workspace_bytes": 13 ...<middle clipped>... 5562936067581, "request1_lse_max_abs_error": Infinity, "request1_lse_invalid_heads": 3, "request1_lse": [-Infinity, 0.0, -Infinity, 0.0, -Infinity, 0.0, 3.6604, 3.6608, -0.1272, 0.0124, -0.1414, 0.2788, -0.1829, 0.0963, 0.1594, 0.0851, -0.0421, 3.6845]}, "worst_token": 0, "worst_sample": {"position": 20, "actual": [-0.00598, -0.00348, -0.02101], "reference": [-0.04494, -0.09739, -0.05527], "actual_lse": [3.05466, -Infinity, 0.0, -Infinity], "reference_lse": [3.05467, 3.04568, 3.03323, 3.04598]}}
5740:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.09826861321926117, "per_token_max_abs_error": [0.06732, 0.09827, 0.0893, 0.08328, 0.00028, 0.00025, 0.00026, 0.00024], "lse_max_abs_error": Infinity, "wo ...<middle clipped>... finity, "request1_lse_invalid_heads": 4, "request1_lse": [-Infinity, 0.0, 0.0, 0.0, 0.0, 0.0, -Infinity, 0.0, -0.0379, -0.0104, 0.0827, 0.0018, -0.1071, -Infinity, -0.0179, 0.0032, 0.0384, -0.0389, 0.0266, -Infinity, 0.0281, 0.014, -0.0343, -0.0206]}, "worst_token": 1, "worst_sample": {"position": 20, "actual": [-0.00428, -0.00318, -0.01993], "reference": [-0.04533, -0.10145, -0.05469], "actual_lse": [-Infinity, 3.04281, 3.69425, -Infinity], "reference_lse": [3.03853, 3.0428, 3.03703, 3.03647]}}
5741:     15| CHECK {"name": "eigensolver_known_spectrum", "dim": 8, "status": "failed", "diagnostic": [0.0, 32.0, 0.0017188957426697016, 8.664765357971191, 2.7871901988983154, 24.64197540283203, 24.64197540283203, 4.0], "eigenvalue_max_abs_error": 8.347458839416504, "rotation_orthogonality": 14.13027572631836, "eigenpair_residual": 87.11943817138672}
5742:     16| CHECK {"name": "eigensolver_known_spectrum", "dim": 64, "status": "failed", "diagnostic": [0.0, 32.0, 0.026881039142608643, 48.8866081237793, 1.007185459136963, 47.0, 28.78778076171875, 4.0], "eigenvalue_max_abs_error": 68.64413452148438, "rotation_orthogonality": 1.2790820598602295, "eigenpair_residual": 84.73745727539062}
5743:     17| CHECK {"name": "eigensolver_known_spectrum", "dim": 128, "status": "failed", "diagnostic": [0.0, 32.0, 0.0037972615100443363, 117.559326171875, 1.0219292640686035, 129.12066650390625, 129.1206817626953, 4.0], "eigenvalue_max_abs_error": 138.7627716064453, "rotation_orthogonality": 2.3519809246063232, "eigenpair_residual": 135.701171875}
5744:     18| CHECK {"name": "forensics_stage_only", "owner": [0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0], "per_row_max_abs_diff_after_stage": [0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
5745:     19| CHECK {"name": "forensics_restore_only", "state": [5, 16, 0, 0], "lossy": 0, "window_rows_vs_expected": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, null, null, null, null], "window_row_absolute_max": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0]}
5746:     20| CHECK {"name": "forensics_eigh_diagonal", "dim": 8, "diagnostic": [1.0, 0.0, 0.0, 8.0, 0.22182972729206085, 4.0, 0.9999603033065796, 4.0], "eigenvalues": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], "vectors_8x8": [[0.002, -0.001, -0.004, -0.0, -0.005,  ...<middle clipped>... rotation": [[0.003, 0.003, 0.005, -0.005, 0.001, 0.002, 0.001, -0.004], [-0.003, -0.001, 0.001, 0.004, -0.002, 0.0, -0.001, -0.001], [-0.0, -0.001, -0.003, -0.003, -0.007, -0.0, 0.002, 0.003], [0.005, -0.004, 0.004, -0.0, 0.004, -0.002, -0.002, -0.002], [0.009, -0.0, -0.001, -0.002, 0.004, -0.004, 0.002, 0.005], [0.003, -0.001, 0.004, -0.004, -0.001, 0.006, -0.004, -0.003], [0.002, 0.003, -0.002, -0.002, -0.003, 0.002, 0.0, -0.003], [-0.003, -0.004, -0.003, 0.001, -0.002, 0.001, -0.001, 0.007]]}
5747:     21| CHECK {"name": "forensics_eigh_single_rotation", "dim": 8, "diagnostic": [0.0, 32.0, 1.240551773662446e-05, 10.999738693237305, 1.38542640209198, 119.99425506591797, 119.99425506591797, 4.0], "eigenvalues": [-0.002, -0.0, 0.0, 0.006, 2.499, 8.0, 9.0, ...<middle clipped>... , 0.006, 0.0, 0.0, -0.0, -0.0, 0.0, -0.0]], "workspace_A_first4": [[39.115, 7.0, 5.246, 5.246, 4.685, 3.0, 1.0, 1.0], [0.0, 0.006, -0.0, 0.0, 0.0, -0.0, 0.0, -0.0], [0.0, -0.0, -0.002, 0.0, -0.0, 0.0, -0.0, 0.0], [484.049, 121.0, 119.994, 119.994, 0.0, 144.0, 1.0, 1.0]], "workspace_B_first4": [[0.001, -0.001, 0.0, -0.0, 1.0, 0.0, -0.0, -0.0], [-0.457, 0.394, 0.0, 0.797, 0.001, 0.0, -0.0, -0.0], [-0.327, 0.755, -0.0, -0.568, 0.001, -0.0, 0.0, -0.0], [0.001, 0.0, -0.0, 0.0, -0.0, 1.0, 0.0, -0.0]]}
5748:     22| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T010855698115Z/operators-quick/rank_0.json"}
5749: [oscar-ascendc] ===== end operators-quick.log =====
[...]
5838:   2288|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
5839:   2289|   "model_graph": "not_run",
5840:   2290|   "model_accuracy": "not_run",
5841:   2291|   "performance": "not_run",
5842:   2292|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
5843:   2293|   "error": "history_attention(64); history_attention(64); history_attention(64); history_attention(64); history_attention(128); history_attention(128); history_attention(128); history_attention(128); history_attention(256); history_attention(256); history_attention(256); history_attention(256); eigensolver_known_spectrum(8); eigensolver_known_spectrum(64); eigensolver_known_spectrum(128)"
5844:   2294| }
5845: [oscar-ascendc] ----- aux log /workspace/codex_oscar_c/build/ascendc/oscar_ascend_kernels_host-prefix/src/oscar_ascend_kernels_host-build/install_manifest.txt (last 40 lines) -----
[...]
5874: | # | 类型 | 评论 ID | 时间(+08:00) | 一行结论 |
5875: |---|------|---------|--------------|----------|
5876: | 1 | 正文 | — | 2026-09-16T09:38:32 | 首轮运行：operators-quick 阶段 NPU 设备同步失败——npuSynchronizeDevice AclrtSynchronizeDeviceWithTimeout error 507015（aicore 异常，ERR00100，kernel retCode=0x26） || 2 | 评论 | 189908202 | 2026-09-16T09:44:06 | 复跑仍失败：同样的 507015 aicore 异常（npuSynchronizeDevice/ERR00100） || 3 | 评论 | 189909856 | 2026-09-16T09:49:59 | build 阶段 C++ 编译错误：oscar_history_cv.cpp 大量 'SymbolOverrideAdd<float>' 非法二元运算、Duplicate/VExp/LoadKv 不匹配（exit 2） || 4 | 评论 | 189914092 | 2026-09-16T10:05:02 | operators-quick 精度失败：history_attention max_abs_error 0.010~0.101、lse_max_abs_error≈3.7~4.0 超阈值 || 5 | 评论 | 189923015 | 2026-09-16T10:35:10 | 同上：history_attention 精度失败（max_abs_error 0.039~0.104，lse≈3.7~4.0） || 6 | 评论 | 189926667 | 2026-09-16T10:45:34 | history_attention 与 window_attention_twin 双双精度失败（twin max_abs 0.272/0.266、lse 1.91/2.05） || 7 | 评论 | 189929096 | 2026-09-16T10:52:55 | 两算子精度继续失败（同 #6 量级） || 8 | 评论 | 189931575 | 2026-09-16T10:59:57 | 两算子精度继续失败（q_len 1~4 全档位） || 9 | 评论 | 189938708 | 2026-09-16T11:21:17 | window_attention_twin head_dim 64/128/256 全失败（max_abs 0.272/0.266/0.823；lse 1.91/2.05/2.01），日志新增 call_ms 计时 || 10 | 评论 | 189943158 | 2026-09-16T11:34:21 | window_attention_twin 三档 head_dim 继续失败（max_abs 0.272/0.266/0.336） || 11 | 评论 | 189945260 | 2026-09-16T11:40:39 | window_attention_twin 继续失败（lse_max_abs_error 1.84~1.96） || 12 | 评论 | 189961005 | 2026-09-16T13:59:04 | 新症状：unwritten_lse_rows（15~43 行未写）→ window_attention_twin lse_max_abs_error=NaN（实际 LSE 数组含 NaN） || 13 | 评论 | 189962640 | 2026-09-16T14:07:03 | history_attention 误差降至 0.010~0.042、lse≈2.4e-07，但仍判 failed；forensics_eigh* 标记 skipped_retired；附 kernels_sha256 || 14 | 评论 | 189964600 | 2026-09-16T14:15:41 | 同 #13：误差 0.010~0.042 仍失败 || 15 | 评论 | 189967664 | 2026-09-16T14:26:27 | 同 #13/#14 || 16 | 评论 | 189969544 | 2026-09-16T14:32:20 | 同 #13/#14/#15 || 17 | 评论 | 189973183 | 2026-09-16T14:43:52 | 新增 inline_dequant_rows 失败：RuntimeError('selftest_table dtype/rank mismatch') || 18 | 评论 | 189974630 | 2026-09-16T14:48:23 | inline_dequant_rows 行级误差超限：k_err 最大 0.98、v_err 最大 1.195（head_dim 64/128/256 全失败） || 19 | 评论 | 189977882 | 2026-09-16T14:58:35 | 同 #18，且 meta_got 与 meta_ref 第 4 元 scale 不一致（如 -0.527344 vs -0.57421875） || 20 | 评论 | 189981818 | 2026-09-16T15:11:21 | 同 #18/#19 || 21 | 评论 | 189985537 | 2026-09-16T15:23:12 | build 再次失败：oscar_common.h:33/36 'cast between floating and unsigned integer variable is not allowed in aicore function'（2 errors，aic/aiv 双份） || 22 | 评论 | 189986793 | 2026-09-16T15:27:06 | primitive_selftest 失败：RuntimeError('selftest_history dtype/rank mismatch') || 23 | 评论 | 189993327 | 2026-09-16T15:44:20 | native-calibration 失败：TP rank NPU 特征分解校验 non-finite——orthogonality_max_error=nan、residual_max_error=nan、finite=False（solver=npu_torch_eigh，layers.11.self_attn.attn/v） || 24 | 评论 | 189998166 | 2026-09-16T15:57:57 | native-calibration：RuntimeError non-finite covariance before eigh（absmax=nan） || 25 | 评论 | 190005071 | 2026-09-16T16:17:02 | 同 #24 且 weighted_nan=65536、weight_sum_finite=False、last_tile_weight_min=-100.0133 || 26 | 评论 | 190013525 | 2026-09-16T16:36:59 | window-pipeline 单测失败：AssertionError: 1.0 not less than 0.6（fallback 与 k0 前 4 行范数差） || 27 | 评论 | 190022536 | 2026-09-16T17:05:32 | service-integration 阶段直接判定：'Service implementation is not complete'（固定地址图元数据更新与真实捕获模型集成未完成） || 28 | 评论 | 190086906 | 2026-09-17T08:37:43 | whole-service-probe：ImportError 无法从 vllm_ascend.device.device_op 导入 DeviceOperator（循环导入）；ERR99999 || 29 | 评论 | 190087339 | 2026-09-17T08:51:50 | whole-service-probe：c10::Error 'pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 … Invalid thread pool!'（set_num_threads） || 30 | 评论 | 190087604 | 2026-09-17T08:56:56 | 同 #29，并出现 'Engine core initialization failed … Failed core proc(s): EngineCore:1'；ERR99999 || 31 | 评论 | 190088352 | 2026-09-17T09:04:42 | WorkerProc 启动失败：ValueError: Field '_oscar_attention_runtime' not found in VllmConfig（多个 TP rank） || 32 | 评论 | 190089622 | 2026-09-17T09:12:28 | 同 #31（TP0/TP1/TP2 均报 _oscar_attention_runtime 字段缺失） || 33 | 评论 | 190094226 | 2026-09-17T09:32:35 | 同 #31/#32 || 34 | 评论 | 190109314 | 2026-09-17T10:25:18 | CUDA graph 捕获期间 ValueError: OSCAR metadata capacity exceeded → RuntimeError: NPUModelRunner failed || 35 | 评论 | 190109411 | 2026-09-17T10:25:37 | 仅贴到 whole-service-probe 阶段启动日志路径（本轮未贴出失败上下文） || 36 | 评论 | 190122990 | 2026-09-17T11:04:52 | 阶段在引擎失败后挂起被提前截断：ValueError: OSCAR metadata capacity exceeded rows=128/128 tokens=512/16384 block-table columns=2052/2048 || 37 | 评论 | 190127457 | 2026-09-17T11:18:17 | 窗口事务错误 code=7 (unknown window error)：layer=mtp.layers.0.self_attn.attn → EngineCore fatal error || 38 | 评论 | 190135821 | 2026-09-17T11:41:26 | 窗口事务错误 code=7 (prefix staging mirror missing for exact restore) position=0 || 39 | 评论 | 190146934 | 2026-09-17T12:42:27 | 窗口事务错误 code=1 (commit exceeds materialized pending K/V) state_before=(epoch=1, committed=0) || 40 | 评论 | 190148415 | 2026-09-17T12:55:13 | 同 #39（committed=1） || 41 | 评论 | 190151663 | 2026-09-17T13:27:41 | 同 #39 + 追加 forward_shapes 诊断信息 || 42 | 评论 | 190152766 | 2026-09-17T13:40:22 | 同 #39 + 追加完整 P/F 调用序列诊断（calls=[P(...23...), P(...1...), P(...1...), F...]） || 43 | 评论 | 190154055 | 2026-09-17T13:55:00 | 同 #39（committed=25）+ 更长的 calls 诊断 || 44 | 评论 | 190156757 | 2026-09-17T14:12:00 | window-pipeline 单测失败：AssertionError: 0 != 1（transactions[0,3] 期望 error=1 未置位） || 45 | 评论 | 190160121 | 2026-09-17T14:22:59 | EngineCore fatal：窗口事务错误 code=1 波及 layers.3 与 layers.7（committed=45），附 SchedulerOutput dump || 46 | 评论 | 190165619 | 2026-09-17T14:38:49 | 窗口事务错误 code=1（layers.3）+ identity_handoffs 诊断 || 47 | 评论 | 190165982 | 2026-09-17T14:39:39 | EngineCore fatal error dump（同 #46 根因，附 SchedulerOutput） || 48 | 评论 | 190170350 | 2026-09-17T14:51:44 | 窗口事务错误 code=1（layers.3）+ identity_handoffs 诊断 || 49 | 评论 | 190170918 | 2026-09-17T14:53:22 | EngineCore fatal error dump（同 #48 根因） || 50 | 评论 | 190180735 | 2026-09-17T15:20:25 | 超长日志（恰 65535 字符，疑被平台截断）：sample_tokens/合并 draft 经 torch_npu npugraph_ex/acl_graph 执行时 WorkerProc 异常 || 51 | 评论 | 190190426 | 2026-09-17T15:45:59 | tail -f 观察：引擎启动后反复出现 'No available shared memory broadcast block found in 60 seconds'（疑似挂起，无显式报错） || 52 | 评论 | 190198904 | 2026-09-17T16:07:25 | tail -f 观察：同 #51（另一时间戳日志） || 53 | 评论 | 190203427 | 2026-09-17T16:18:50 | operators-quick：window_attention_out() is missing value for argument 'raw'（torch 算子 schema 不匹配，head_dim 三档全失败） || 54 | 评论 | 190207997 | 2026-09-17T16:31:02 | window-pipeline 多个测试 NameError: name 'torch' is not defined || 55 | 评论 | 190211678 | 2026-09-17T16:41:32 | FIA 调用失败：npu_fused_infer_attention_score_out_symint … aclnnFusedInferAttentionScoreV3 failed, error code 561002；EZ1008 Failed to execute tiling function || 56 | 评论 | 190214013 | 2026-09-17T16:48:12 | 同 #55（561002/EZ1008 tiling 失败） || 57 | 评论 | 190216667 | 2026-09-17T16:55:30 | 507015 aicore 异常 + RuntimeError: shape '[10, 4]' is invalid for input of size 1 || 58 | 评论 | 190220727 | 2026-09-17T17:06:40 | 507015 aicore 异常 + RuntimeError: output dtype/rank mismatch || 59 | 评论 | 190231603 | 2026-09-17T17:38:23 | 同 #58 || 60 | 评论 | 190244374 | 2026-09-17T18:51:38 | 507015 + ValueError: FIA returned softmax_lse of 0 elements (shape (0,))，expected n*h=40 || 61 | 评论 | 190245276 | 2026-09-17T18:57:23 | 507015 + ValueError: FIA left softmax_lse at 1 elements (shape (1,))（op-plugin 未 resize eager LSE 输出） || 62 | 评论 | 190247794 | 2026-09-17T19:09:38 | 全部用例 RuntimeError: output dtype/rank mismatch || 63 | 评论 | 190251355 | 2026-09-17T19:22:07 | AssertionError: nan not less than 0.02（prefill: PR window relative-L2 阈值） || 64 | 评论 | 190253335 | 2026-09-17T19:28:59 | AssertionError: 1.4083268642425537 / 1.4637478590011597 not less than 0.02（prefill relative-L2） || 65 | 评论 | 190255209 | 2026-09-17T19:36:18 | 同 #64 || 66 | 评论 | 190257525 | 2026-09-17T19:44:20 | FIA 561002 tiling 失败 + relative-L2 1.4637 失败 || 67 | 评论 | 190261267 | 2026-09-17T19:57:30 | whole-service：ValueError: prefill-like shape reached FIA without the native causal mask（该 CANN 对非零 sparse mode 必须提供 mask） || 68 | 评论 | 190264839 | 2026-09-17T20:10:35 | tail -f 观察：引擎启动后 shm broadcast 60 秒不可用（挂起迹象） || 69 | 评论 | 190274249 | 2026-09-17T20:43:26 | RuntimeError: Expected all tensors to be on the same device（npu:0 vs cpu，matmul）；另有 ArgSort int32/int64 落到 AiCpu 的警告 || 70 | 评论 | 190315227 | 2026-09-18T08:54:47 | 一行提示命令：tail -f logs/<最新时间戳>/whole-service-probe.log \| grep --line-buffered oscar-timing || 71 | 评论 | 190315785 | 2026-09-18T09:00:21 | oscar-timing 计时日志：dequant 每卡设备耗时 ~6.5 秒占绝对主导（fia 仅 ~18.7ms，materialize ~0.5ms，phase1_stores ~209ms，wall ~6.8~7.0s） || 72 | 评论 | 190317191 | 2026-09-18T09:10:01 | native_baseline.py 崩溃：FileNotFoundError 'logs/20260918T004637419752Z/native-baseline/native-baseline.json'；ERR99999 || 73 | 评论 | 190320161 | 2026-09-18T09:23:37 | 最终成功：native TP4 timing baseline（OSCAR 插件禁用）baseline_passed_engine_stopped——boot 309.6s，长输入 31897 tokens prefill 4.6s（6869.5 tok/s） |
5877: 
5878: ### 后半段 阶段小记（报了什么错，八阶段）
[...]
5882: **② AscendC C++ 编译错误（#3、#21）**：`oscar_history_cv.cpp` 里 `SymbolOverrideAdd<float>` 与 int 做二元运算不合法、`Duplicate`/`VExp`/`LoadKv` 无匹配重载；`oscar_common.h:33/36` 报 "cast between floating and unsigned integer variable is not allowed in aicore function"，aic/aiv 两份目标各 2 errors，cmake --build exit 2。
5883: 
5884: **③ 自定义算子数值精度失败（#4~#20，轮次最多的阶段）**：`history_attention` 在 head_dim 64/128/256 × q_len 1~4 全档位 max_abs_error 0.010~0.104、lse_max_abs_error≈3.7~4.1 远超阈值；`window_attention_twin` max_abs_error 最高 0.82、lse 偏差 ~2.0；一度出现 `unwritten_lse_rows`（LSE 有 15~43 行未写导致 lse_max_abs_error=NaN）；#13 起误差降到 0.010~0.042、lse≈2.4e-07 但仍判 failed（forensics_eigh* 改为 skipped_retired：生产改用 torch_npu eigh）；随后 `inline_dequant_rows` 又暴露 k_err≈0.98 / v_err≈1.20 的反量化行级误差与 `RuntimeError('selftest_table dtype/rank mismatch')`，且 meta scale 第 4 元与参考不一致。
5885: 
5886: **④ 校准/特征分解全 NaN（#22~#25）**：`primitive_selftest` 报 `RuntimeError('selftest_history dtype/rank mismatch')`；native-calibration 阶段 `npu_torch_eigh` 特征分解校验 `orthogonality_max_error=nan, residual_max_error=nan, finite=False`，继而 `RuntimeError: non-finite covariance before eigh ... absmax=nan`，并定位到 `weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-100.0133`——协方差权重里出现 -100 级别的异常值把整个 eigh 污染成 NaN。
5887: 
5888: **⑤ 服务集成层连环错（#26~#33）**：window-pipeline 单测断言失败（`AssertionError: 1.0 not less than 0.6`）；service-integration 阶段直接判 "Service implementation is not complete"；whole-service-probe 先后撞上 `ImportError: cannot import name 'DeviceOperator' ... (circular import)`、c10 的 `pool INTERNAL ASSERT FAILED at ParallelOpenMP.cpp:64 ... Invalid thread pool!`（附 "Engine core initialization failed"）、`ValueError: Field '_oscar_attention_runtime' not found in VllmConfig`（多个 TP worker 起不来）。
[...]
5890: **⑥ 图捕获容量与窗口事务状态机错误（#34~#50）**：CUDA graph 捕获时 `ValueError: OSCAR metadata capacity exceeded`（rows=128/128、tokens=512/16384、block-table columns=2052/2048 三处同时打满，阶段一度挂起后被探测脚本提前截断）；随后进入轮次最长的一段——`RuntimeError: OSCAR NPU window state reported transaction errors`，错误码先是 code=7（unknown window error / prefix staging mirror missing for exact restore），后稳定为 code=1（**commit exceeds materialized pending K/V**），分布在 mtp.layers.0 与 language_model.layers.3/7，日志逐步追加 forward_shapes、P/F 调用序列、identity_handoffs 等诊断字段；EngineCore 数次 fatal 并 dump SchedulerOutput；#50 的巨型日志（恰 65535 字符）显示 sample_tokens/合并 draft 经 torch_npu npugraph_ex/acl_graph 执行时 WorkerProc 异常。
5891: 
5892: **⑦ FIA（aclnnFusedInferAttentionScoreV3）与 mask/精度问题（#53~#69）**：算子 schema 变更引发 `oscar_ascend::window_attention_out() is missing value for argument 'raw'`；测试代码 `NameError: name 'torch' is not defined`；随后大量 `npu_fused_infer_attention_score_*` 失败——error code **561002** + `Execution_Error(EZ1008): Failed to execute tiling function`、507015 aicore 异常、`RuntimeError: output dtype/rank mismatch`、`ValueError: FIA returned softmax_lse of 0 elements`、`ValueError: FIA left softmax_lse at 1 elements ... did not resize the eager LSE output`、`RuntimeError: shape '[10, 4]' is invalid for input of size 1`；链路精度上 `AssertionError: nan not less than 0.02` 与 `1.4083268642425537 / 1.4637478590011597 not less than 0.02`；整机又报 `ValueError: prefill-like shape reached FIA without the native causal mask; this CANN requires one for nonzero sparse modes`；此段还有一次 CPU/NPU 张量混用（`Expected all tensors to be on the same device ... npu:0 ... cpu`）。
5893: 
5894: **⑧ 性能定位与原生基线（#70~#73，09-18）**：oscar-timing 打点发现每卡 prefill 中 **dequant 设备耗时 ~6.5 秒**（6499.8~6655.1 ms）占绝对主导，fia 仅 ~18.7ms、materialize ~0.5ms、phase1_stores ~209ms（wall ~6.8~7.0s）；关闭 OSCAR 插件跑 native TP4 timing baseline 时先踩 `FileNotFoundError: 'logs/20260918T004637419752Z/native-baseline/native-baseline.json'`（输出目录未创建），修复后基线**通过**：boot 309.6s、长输入 31897 tokens 的 prefill 4.6s（≈6869.5 tok/s）、短请求 ~21 tok/s——issue 停在这条成功报文上。
[...]
6024:      5|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
6025:      6|   "model_graph": "not_run",
6026:      7|   "model_accuracy": "not_run",
6027:      8|   "performance": "not_run",
6028:      9|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
6187:      5|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
6188:      6|   "model_graph": "not_run",
6189:      7|   "model_accuracy": "not_run",
6190:      8|   "performance": "not_run",
6191:      9|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
6732: <!-- ENTRY src=gc idx=4 id=189914092 chars=18194 -->
6733: 
6734: **一行结论**：operators-quick 精度失败：history_attention max_abs_error 0.010~0.101、lse_max_abs_error≈3.7~4.0 超阈值
6735: 
6736: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
6793:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.10121169686317444, "per_token_max_abs_error": [0.10024, 0.09363, 0.10121, 0.08943, 0.03307, 0.05013, 0.04505, 0.04276], "lse_max_abs_error": 3.7063252925 ...<middle clipped>... 745072841644287, "request1_lse_invalid_heads": 0, "request1_lse": [0.0, 0.0, 0.0, 3.6115, 3.6129, 3.6195, 0.0, 3.6244, -0.0467, -0.0193, 0.0739, 3.6331, -0.116, -0.0548, -0.0268, -0.0056, 0.0296, -0.0478, 3.6831, 0.0048, 3.6831, 0.0051, -0.0432, 3.6828]}, "worst_token": 2, "worst_sample": {"position": 21, "actual": [-0.03196, -0.01302, -0.0437], "reference": [-0.0543, -0.08122, -0.0565], "actual_lse": [-0.01988, 0.08032, 0.09433, -0.03063], "reference_lse": [3.10555, 3.09151, 3.09309, 3.09648]}}
6794:     15| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
6795:     16| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
6796:     17| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T015433119498Z/operators-quick/rank_0.json"}
6797: [oscar-ascendc] ===== end operators-quick.log =====
[...]
6871:   1661|     },
6872:   1662|     {
6873:   1663|       "name": "eigensolver_known_spectrum",
6874:   1664|       "status": "skipped_retired",
6875:   1665|       "reason": "production uses torch_npu eigh"
[...]
6881:   1671|     },
6882:   1672|     {
6883:   1673|       "name": "forensics_eigh_single_rotation",
6884:   1674|       "status": "skipped_retired",
6885:   1675|       "reason": "production uses torch_npu eigh"
[...]
6888:   1678|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
6889:   1679|   "model_graph": "not_run",
6890:   1680|   "model_accuracy": "not_run",
6891:   1681|   "performance": "not_run",
6892:   1682|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
6918: <!-- ENTRY src=gc idx=5 id=189923015 chars=19587 -->
6919: 
6920: **一行结论**：同上：history_attention 精度失败（max_abs_error 0.039~0.104，lse≈3.7~4.0）
6921: 
6922: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
6980:     14| CHECK {"name": "history_attention", "head_dim": 256, "q_len": 4, "splits": 3, "max_abs_error": 0.10121169686317444, "per_token_max_abs_error": [0.10024, 0.09363, 0.10121, 0.08943, 0.04897, 0.04794, 0.04462, 0.04494], "lse_max_abs_error": 3.7209713459 ...<middle clipped>... r": 0.0504569411277771, "request1_lse_max_abs_error": 3.7092957496643066, "request1_lse_invalid_heads": 0, "request1_lse": [0.0, 3.6123, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.6421, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.6729, 0.0, 0.0, 0.0, 0.0, 3.6951, 0.0, 0.0]}, "worst_token": 2, "worst_sample": {"position": 21, "actual": [-0.03196, -0.01302, -0.0437], "reference": [-0.0543, -0.08122, -0.0565], "actual_lse": [0.07853, 0.03338, 0.04575, 0.08186], "reference_lse": [3.10555, 3.09151, 3.09309, 3.09648]}}
6981:     15| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
6982:     16| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
6983:     17| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T022750580269Z/operators-quick/rank_0.json"}
6984: [oscar-ascendc] ===== end operators-quick.log =====
[...]
7056:   2093|     },
7057:   2094|     {
7058:   2095|       "name": "eigensolver_known_spectrum",
7059:   2096|       "status": "skipped_retired",
7060:   2097|       "reason": "production uses torch_npu eigh"
[...]
7066:   2103|     },
7067:   2104|     {
7068:   2105|       "name": "forensics_eigh_single_rotation",
7069:   2106|       "status": "skipped_retired",
7070:   2107|       "reason": "production uses torch_npu eigh"
[...]
7073:   2110|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
7074:   2111|   "model_graph": "not_run",
7075:   2112|   "model_accuracy": "not_run",
7076:   2113|   "performance": "not_run",
7077:   2114|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
7136: <!-- ENTRY src=gc idx=6 id=189926667 chars=25784 -->
7137: 
7138: **一行结论**：history_attention 与 window_attention_twin 双双精度失败（twin max_abs 0.272/0.266、lse 1.91/2.05）
7139: 
7140: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
7227:     41| CHECK {"name": "window_attention_twin", "head_dim": 256, "max_abs_error": 0.8227498531341553, "lse_max_abs_error": 2.0055928230285645, "status": "failed", "actual_lse": [0.5224, 0.0208, -0.0534, -0.0177, 0.1858, -0.1975, -0.1936, -0.0995, -0.0863, 0.4018, 0.1545, 0.2651, 0.2768, -0.0638, 0.0234, 0.0167, 0.0829, 0.1438, 0.0181, -0.1482, -0.1224, 0.039, 0.0551, 0.0622], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
7228:     42| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7229:     43| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7230:     44| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T023801721236Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "0b4427a619bcb1bc21b78b969c7af942cbfd0c256bb4a379977045f31264a54e"}}
7231: [oscar-ascendc] ===== end operators-quick.log =====
[...]
7300:   2270|     },
7301:   2271|     {
7302:   2272|       "name": "eigensolver_known_spectrum",
7303:   2273|       "status": "skipped_retired",
7304:   2274|       "reason": "production uses torch_npu eigh"
[...]
7310:   2280|     },
7311:   2281|     {
7312:   2282|       "name": "forensics_eigh_single_rotation",
7313:   2283|       "status": "skipped_retired",
7314:   2284|       "reason": "production uses torch_npu eigh"
[...]
7317:   2287|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
7318:   2288|   "model_graph": "not_run",
7319:   2289|   "model_accuracy": "not_run",
7320:   2290|   "performance": "not_run",
7321:   2291|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
7388: <!-- ENTRY src=gc idx=7 id=189929096 chars=23166 -->
7389: 
7390: **一行结论**：两算子精度继续失败（同 #6 量级）
7391: 
7392: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
7479:     41| CHECK {"name": "window_attention_twin", "head_dim": 256, "max_abs_error": 0.8227498531341553, "lse_max_abs_error": 2.0055928230285645, "status": "failed", "actual_lse": [0.5224, 0.0208, -0.0534, -0.0177, 0.1858, -0.1975, -0.1936, -0.0995, -0.0863, 0.4018, 0.1545, 0.2651, 0.2768, -0.0638, 0.0234, 0.0167, 0.0829, 0.1438, 0.0181, -0.1482, -0.1224, 0.039, 0.0551, 0.0622], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
7480:     42| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7481:     43| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7482:     44| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T024612140651Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "bdaf2792b2d9b819a547238d9e3271fe45a0db3f48616fa3637cf6aa3d970a03"}}
7483: [oscar-ascendc] ===== end operators-quick.log =====
[...]
7552:   2270|     },
7553:   2271|     {
7554:   2272|       "name": "eigensolver_known_spectrum",
7555:   2273|       "status": "skipped_retired",
7556:   2274|       "reason": "production uses torch_npu eigh"
[...]
7562:   2280|     },
7563:   2281|     {
7564:   2282|       "name": "forensics_eigh_single_rotation",
7565:   2283|       "status": "skipped_retired",
7566:   2284|       "reason": "production uses torch_npu eigh"
[...]
7569:   2287|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
7570:   2288|   "model_graph": "not_run",
7571:   2289|   "model_accuracy": "not_run",
7572:   2290|   "performance": "not_run",
7573:   2291|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
7599: <!-- ENTRY src=gc idx=8 id=189931575 chars=25786 -->
7600: 
7601: **一行结论**：两算子精度继续失败（q_len 1~4 全档位）
7602: 
7603: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
7691:     41| CHECK {"name": "window_attention_twin", "head_dim": 256, "max_abs_error": 0.8227498531341553, "lse_max_abs_error": 2.0055928230285645, "status": "failed", "actual_lse": [0.5224, 0.0208, -0.0534, -0.0177, 0.1858, -0.1975, -0.1936, -0.0995, -0.0863, 0.4018, 0.1545, 0.2651, 0.2768, -0.0638, 0.0234, 0.0167, 0.0829, 0.1438, 0.0181, -0.1482, -0.1224, 0.039, 0.0551, 0.0622], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
7692:     42| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7693:     43| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7694:     44| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T025249912880Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "382be61141c91b0c25b67c4a3512390e7249f6b214f6a67b694b62ce4072d034"}}
7695: [oscar-ascendc] ===== end operators-quick.log =====
[...]
7764:   2270|     },
7765:   2271|     {
7766:   2272|       "name": "eigensolver_known_spectrum",
7767:   2273|       "status": "skipped_retired",
7768:   2274|       "reason": "production uses torch_npu eigh"
[...]
7774:   2280|     },
7775:   2281|     {
7776:   2282|       "name": "forensics_eigh_single_rotation",
7777:   2283|       "status": "skipped_retired",
7778:   2284|       "reason": "production uses torch_npu eigh"
[...]
7781:   2287|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
7782:   2288|   "model_graph": "not_run",
7783:   2289|   "model_accuracy": "not_run",
7784:   2290|   "performance": "not_run",
7785:   2291|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
7957:     53| CHECK {"name": "window_attention_twin", "head_dim": 256, "max_abs_error": 0.8227498531341553, "lse_max_abs_error": 2.0055928230285645, "status": "failed", "actual_lse": [0.5224, 0.0208, -0.0534, -0.0177, 0.1858, -0.1975, -0.1936, -0.0995, -0.0863, 0.4018, 0.1545, 0.2651, 0.2768, -0.0638, 0.0234, 0.0167, 0.0829, 0.1438, 0.0181, -0.1482, -0.1224, 0.039, 0.0551, 0.0622], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
7958:     54| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7959:     55| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
7960:     56| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T031430670208Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "5947bc75f0f7d65f10ab466eb306637cc48c585b8d10efd68b99cec886220f2e"}}
7961: [oscar-ascendc] ===== end operators-quick.log =====
[...]
8030:   2282|     },
8031:   2283|     {
8032:   2284|       "name": "eigensolver_known_spectrum",
8033:   2285|       "status": "skipped_retired",
8034:   2286|       "reason": "production uses torch_npu eigh"
[...]
8040:   2292|     },
8041:   2293|     {
8042:   2294|       "name": "forensics_eigh_single_rotation",
8043:   2295|       "status": "skipped_retired",
8044:   2296|       "reason": "production uses torch_npu eigh"
[...]
8047:   2299|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
8048:   2300|   "model_graph": "not_run",
8049:   2301|   "model_accuracy": "not_run",
8050:   2302|   "performance": "not_run",
8051:   2303|   "library_sha256": "65b1a86b10a21fd424e8d74212028e0fa3b4d8674ddfa60ac002014cd6467d09",
[...]
8184:     53| CHECK {"name": "window_attention_twin", "head_dim": 256, "max_abs_error": 0.3355640172958374, "lse_max_abs_error": 1.8442678451538086, "status": "failed", "actual_lse": [-0.0216, 0.0439, -0.0173, -0.0106, -0.0074, -0.0635, 0.0282, 0.0226, -0.0451, -0.045, 0.0149, -0.0091, 0.0202, -0.0609, 0.0045, 0.0023, 0.0038, 0.0922, 0.0075, 0.0306, -0.0085, -0.0083, -0.0303, 0.0139], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
8185:     54| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8186:     55| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8187:     56| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T032447080843Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "e542d0e242173499c8489ec8737f1aceb4fe3470537e231b9462d36e7d1ebd35"}}
8188: [oscar-ascendc] ===== end operators-quick.log =====
[...]
8258:   2288|     },
8259:   2289|     {
8260:   2290|       "name": "eigensolver_known_spectrum",
8261:   2291|       "status": "skipped_retired",
8262:   2292|       "reason": "production uses torch_npu eigh"
[...]
8268:   2298|     },
8269:   2299|     {
8270:   2300|       "name": "forensics_eigh_single_rotation",
8271:   2301|       "status": "skipped_retired",
8272:   2302|       "reason": "production uses torch_npu eigh"
[...]
8275:   2305|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
8276:   2306|   "model_graph": "not_run",
8277:   2307|   "model_accuracy": "not_run",
8278:   2308|   "performance": "not_run",
8279:   2309|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
8452:     53| CHECK {"name": "window_attention_twin", "head_dim": 256, "max_abs_error": 0.3355640172958374, "lse_max_abs_error": 1.8442678451538086, "status": "failed", "actual_lse": [-0.0216, 0.0439, -0.0173, -0.0106, -0.0074, -0.0635, 0.0282, 0.0226, -0.0451, -0.045, 0.0149, -0.0091, 0.0202, -0.0609, 0.0045, 0.0023, 0.0038, 0.0922, 0.0075, 0.0306, -0.0085, -0.0083, -0.0303, 0.0139], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
8453:     54| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8454:     55| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8455:     56| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T033407751955Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "5ba156409fd38e7155dbb77457f3d9d50948bea1595e2c39be9213caaeb9eea2"}}
8456: [oscar-ascendc] ===== end operators-quick.log =====
[...]
8525:   2291|     },
8526:   2292|     {
8527:   2293|       "name": "eigensolver_known_spectrum",
8528:   2294|       "status": "skipped_retired",
8529:   2295|       "reason": "production uses torch_npu eigh"
[...]
8535:   2301|     },
8536:   2302|     {
8537:   2303|       "name": "forensics_eigh_single_rotation",
8538:   2304|       "status": "skipped_retired",
8539:   2305|       "reason": "production uses torch_npu eigh"
[...]
8542:   2308|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
8543:   2309|   "model_graph": "not_run",
8544:   2310|   "model_accuracy": "not_run",
8545:   2311|   "performance": "not_run",
8546:   2312|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
8679:     53| CHECK {"name": "window_attention_twin", "head_dim": 256, "unwritten_lse_rows": 16, "max_abs_error": 0.1200944259762764, "lse_max_abs_error": NaN, "status": "failed", "actual_lse": [1.5751, NaN, NaN, NaN, NaN, 1.5738, NaN, NaN, NaN, 1.7689, NaN, 1.7952, NaN, NaN, NaN, NaN, 1.6374, 1.5882, NaN, NaN, NaN, 1.7923, 1.775, NaN], "reference_lse": [1.5751, 1.6189, 1.6201, 1.6313, 1.6206, 1.5738, 1.812, 1.7972, 1.7992, 1.7689, 1.7732, 1.7952, 1.617, 1.6168, 1.635, 1.6081, 1.6374, 1.5882, 1.8128, 1.8021, 1.8234, 1.7923, 1.775, 1.7775]}
8680:     54| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8681:     55| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8682:     56| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T055027541649Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "b2b67b9a3f188286c62f3f540b8ce5c5058768a7428c019a1fbba3c20193f274"}}
8683: [oscar-ascendc] ===== end operators-quick.log =====
[...]
8752:   2318|     },
8753:   2319|     {
8754:   2320|       "name": "eigensolver_known_spectrum",
8755:   2321|       "status": "skipped_retired",
8756:   2322|       "reason": "production uses torch_npu eigh"
[...]
8762:   2328|     },
8763:   2329|     {
8764:   2330|       "name": "forensics_eigh_single_rotation",
8765:   2331|       "status": "skipped_retired",
8766:   2332|       "reason": "production uses torch_npu eigh"
[...]
8769:   2335|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
8770:   2336|   "model_graph": "not_run",
8771:   2337|   "model_accuracy": "not_run",
8772:   2338|   "performance": "not_run",
8773:   2339|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
8940:     50| DIGEST slots {"got": [[-0.122, -0.21, -0.161], [-0.127, -0.215, -0.161], [-0.129, -0.212, -0.162]], "ref": [[2.05, 2.073, 1.439], [2.038, 2.085, 1.371], [2.081, 2.081, 1.381]]}
8941:     51| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8942:     52| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
8943:     53| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T060011374386Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "efd94c624f905329b086495ccf179e3923a38b941f93451aa715d68ea4a9cd8d"}}
8944: [oscar-ascendc] ===== end operators-quick.log =====
[...]
9013:   2162|     },
9014:   2163|     {
9015:   2164|       "name": "eigensolver_known_spectrum",
9016:   2165|       "status": "skipped_retired",
9017:   2166|       "reason": "production uses torch_npu eigh"
[...]
9023:   2172|     },
9024:   2173|     {
9025:   2174|       "name": "forensics_eigh_single_rotation",
9026:   2175|       "status": "skipped_retired",
9027:   2176|       "reason": "production uses torch_npu eigh"
[...]
9030:   2179|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
9031:   2180|   "model_graph": "not_run",
9032:   2181|   "model_accuracy": "not_run",
9033:   2182|   "performance": "not_run",
9034:   2183|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
9190:     74| DIGEST rowlse actual=[3.1056, 3.0915, 3.0931, 3.0965] ref=[3.1056, 3.0915, 3.0931, 3.0965]
9191:     75| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9192:     76| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9193:     77| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T060830830952Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "efd94c624f905329b086495ccf179e3923a38b941f93451aa715d68ea4a9cd8d"}}
9194: [oscar-ascendc] ===== end operators-quick.log =====
[...]
9263:   2162|     },
9264:   2163|     {
9265:   2164|       "name": "eigensolver_known_spectrum",
9266:   2165|       "status": "skipped_retired",
9267:   2166|       "reason": "production uses torch_npu eigh"
[...]
9273:   2172|     },
9274:   2173|     {
9275:   2174|       "name": "forensics_eigh_single_rotation",
9276:   2175|       "status": "skipped_retired",
9277:   2176|       "reason": "production uses torch_npu eigh"
[...]
9280:   2179|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
9281:   2180|   "model_graph": "not_run",
9282:   2181|   "model_accuracy": "not_run",
9283:   2182|   "performance": "not_run",
9284:   2183|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
9451:     74| DIGEST rowlse actual=[3.1056, 3.0915, 3.0931, 3.0965] ref=[3.1056, 3.0915, 3.0931, 3.0965]
9452:     75| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9453:     76| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9454:     77| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T061737046159Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "efd94c624f905329b086495ccf179e3923a38b941f93451aa715d68ea4a9cd8d"}}
9455: [oscar-ascendc] ===== end operators-quick.log =====
[...]
9525:   2186|     },
9526:   2187|     {
9527:   2188|       "name": "eigensolver_known_spectrum",
9528:   2189|       "status": "skipped_retired",
9529:   2190|       "reason": "production uses torch_npu eigh"
[...]
9535:   2196|     },
9536:   2197|     {
9537:   2198|       "name": "forensics_eigh_single_rotation",
9538:   2199|       "status": "skipped_retired",
9539:   2200|       "reason": "production uses torch_npu eigh"
[...]
9542:   2203|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
9543:   2204|   "model_graph": "not_run",
9544:   2205|   "model_accuracy": "not_run",
9545:   2206|   "performance": "not_run",
9546:   2207|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
9675:     74| DIGEST rowlse actual=[3.1056, 3.0915, 3.0931, 3.0965] ref=[3.1056, 3.0915, 3.0931, 3.0965]
9676:     75| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9677:     76| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9678:     77| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T062546275327Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "efd94c624f905329b086495ccf179e3923a38b941f93451aa715d68ea4a9cd8d"}}
9679: [oscar-ascendc] ===== end operators-quick.log =====
[...]
9748:   2402|     },
9749:   2403|     {
9750:   2404|       "name": "eigensolver_known_spectrum",
9751:   2405|       "status": "skipped_retired",
9752:   2406|       "reason": "production uses torch_npu eigh"
[...]
9758:   2412|     },
9759:   2413|     {
9760:   2414|       "name": "forensics_eigh_single_rotation",
9761:   2415|       "status": "skipped_retired",
9762:   2416|       "reason": "production uses torch_npu eigh"
[...]
9765:   2419|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
9766:   2420|   "model_graph": "not_run",
9767:   2421|   "model_accuracy": "not_run",
9768:   2422|   "performance": "not_run",
9769:   2423|   "library_sha256": "9ac310a824cadf64ba7bb00e5caa7671f2c0d60689f8144d35fdafeac740293c",
[...]
9946:     79| CHECK {"name": "inline_dequant_rows", "head_dim": 256, "status": "failed", "error": "RuntimeError('selftest_table dtype/rank mismatch')"}
9947:     80| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9948:     81| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
9949:     82| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T063714721629Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "0111adc77b77215e5a50a9e4681f0e80948e0a19f2734f58984f3217b77eefc8"}}
9950: [oscar-ascendc] ===== end operators-quick.log =====
[...]
10019:   2440|     },
10020:   2441|     {
10021:   2442|       "name": "eigensolver_known_spectrum",
10022:   2443|       "status": "skipped_retired",
10023:   2444|       "reason": "production uses torch_npu eigh"
[...]
10029:   2450|     },
10030:   2451|     {
10031:   2452|       "name": "forensics_eigh_single_rotation",
10032:   2453|       "status": "skipped_retired",
10033:   2454|       "reason": "production uses torch_npu eigh"
[...]
10036:   2457|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
10037:   2458|   "model_graph": "not_run",
10038:   2459|   "model_accuracy": "not_run",
10039:   2460|   "performance": "not_run",
10040:   2461|   "library_sha256": "42488b0ce5769aa9cda38010209fcfc717c1db10cc6a56f97c255ed54186c796",
[...]
10203:     82| CHECK {"name": "inline_dequant_rows", "head_dim": 256, "rows": [{"req": 0, "pos": 0, "k_err": 0.0, "v_err": 0.1484375, "v_bias": 0.148438, "v_spread": 0.0}, {"req": 0, "pos": 22, "k_err": 0.980224609375, "v_err": 1.00390625, "v_bias": 0.057261, "v_spread": 1.061168}, {"req": 1, "pos": 39, "k_err": 0.7890625, "v_err": 1.195068359375, "v_bias": 0.067633, "v_spread": 1.127436}], "status": "failed"}
10204:     83| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
10205:     84| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
10206:     85| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T064140362996Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "0111adc77b77215e5a50a9e4681f0e80948e0a19f2734f58984f3217b77eefc8"}}
10207: [oscar-ascendc] ===== end operators-quick.log =====
[...]
10276:   2515|     },
10277:   2516|     {
10278:   2517|       "name": "eigensolver_known_spectrum",
10279:   2518|       "status": "skipped_retired",
10280:   2519|       "reason": "production uses torch_npu eigh"
[...]
10286:   2525|     },
10287:   2526|     {
10288:   2527|       "name": "forensics_eigh_single_rotation",
10289:   2528|       "status": "skipped_retired",
10290:   2529|       "reason": "production uses torch_npu eigh"
[...]
10293:   2532|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
10294:   2533|   "model_graph": "not_run",
10295:   2534|   "model_accuracy": "not_run",
10296:   2535|   "performance": "not_run",
10297:   2536|   "library_sha256": "b07117c7520dfd6313ddaaaf5d55009e5b9f7bca502518ecfb704b4dbf792d78",
[...]
10426:     82| CHECK {"name": "inline_dequant_rows", "head_dim": 256, "rows": [{"req": 0, "pos": 0, "k_err": 0.0, "v_err": 0.1484375, "v_bias": 0.148438, "v_spread": 0.0, "meta_got": [0.444092, -0.550781, 0.455811, -0.550781], "meta_ref": [0.444091796875, -0.550781 ...<middle clipped>... .444091796875, -0.55078125, 0.455810546875, -0.69921875]}, {"req": 0, "pos": 22, "k_err": 0.0, "v_err": 0.18359375, "v_bias": 0.183594, "v_spread": 0.0, "meta_got": [0.321533, -0.4375, 0.390625, -0.4375], "meta_ref": [0.321533203125, -0.4375, 0.390625, -0.62109375]}, {"req": 1, "pos": 39, "k_err": 0.0, "v_err": 0.00390625, "v_bias": 0.003906, "v_spread": 0.0, "meta_got": [0.351562, -0.507812, 0.398438, -0.507812], "meta_ref": [0.3515625, -0.5078125, 0.3984375, -0.51171875]}], "status": "failed"}
10427:     83| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
10428:     84| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
10429:     85| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T065153709725Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "4336bbff182b556ef225c9a81a7d7a3ce9b5e01de16296850b84f5a2cce524c4"}}
10430: [oscar-ascendc] ===== end operators-quick.log =====
[...]
10499:   2623|     },
10500:   2624|     {
10501:   2625|       "name": "eigensolver_known_spectrum",
10502:   2626|       "status": "skipped_retired",
10503:   2627|       "reason": "production uses torch_npu eigh"
[...]
10509:   2633|     },
10510:   2634|     {
10511:   2635|       "name": "forensics_eigh_single_rotation",
10512:   2636|       "status": "skipped_retired",
10513:   2637|       "reason": "production uses torch_npu eigh"
[...]
10516:   2640|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
10517:   2641|   "model_graph": "not_run",
10518:   2642|   "model_accuracy": "not_run",
10519:   2643|   "performance": "not_run",
10520:   2644|   "library_sha256": "878156e3009dc6a13c5dc16ca322064150111da7ebc9d423fe668087b752d3ea",
[...]
10649:     82| CHECK {"name": "inline_dequant_rows", "head_dim": 256, "rows": [{"req": 0, "pos": 0, "k_err": 0.0, "v_err": 0.1484375, "v_bias": 0.148438, "v_spread": 0.0, "meta_got": [0.444092, -0.550781, 0.455811, -0.550781], "meta_ref": [0.444091796875, -0.550781 ...<middle clipped>... .444091796875, -0.55078125, 0.455810546875, -0.69921875]}, {"req": 0, "pos": 22, "k_err": 0.0, "v_err": 0.18359375, "v_bias": 0.183594, "v_spread": 0.0, "meta_got": [0.321533, -0.4375, 0.390625, -0.4375], "meta_ref": [0.321533203125, -0.4375, 0.390625, -0.62109375]}, {"req": 1, "pos": 39, "k_err": 0.0, "v_err": 0.00390625, "v_bias": 0.003906, "v_spread": 0.0, "meta_got": [0.351562, -0.507812, 0.398438, -0.507812], "meta_ref": [0.3515625, -0.5078125, 0.3984375, -0.51171875]}], "status": "failed"}
10650:     83| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
10651:     84| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
10652:     85| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T065729484953Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "e7c1cfce9d597627af998f3f576a433b7def32aa3105df1e1f97b54132af01e8"}}
10653: [oscar-ascendc] ===== end operators-quick.log =====
[...]
10722:   2623|     },
10723:   2624|     {
10724:   2625|       "name": "eigensolver_known_spectrum",
10725:   2626|       "status": "skipped_retired",
10726:   2627|       "reason": "production uses torch_npu eigh"
[...]
10732:   2633|     },
10733:   2634|     {
10734:   2635|       "name": "forensics_eigh_single_rotation",
10735:   2636|       "status": "skipped_retired",
10736:   2637|       "reason": "production uses torch_npu eigh"
[...]
10739:   2640|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
10740:   2641|   "model_graph": "not_run",
10741:   2642|   "model_accuracy": "not_run",
10742:   2643|   "performance": "not_run",
10743:   2644|   "library_sha256": "878156e3009dc6a13c5dc16ca322064150111da7ebc9d423fe668087b752d3ea",
[...]
11199:     19| CHECK {"name": "primitive_selftest", "status": "failed", "error": "RuntimeError('selftest_history dtype/rank mismatch')"}
11200:     20| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
11201:     21| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
11202:     22| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260916T071932053870Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "0288c784f1ba3749afb39c78a0aa496bb4f06bb5b2acee5d9976ff52bd609fe6"}}
11203: [oscar-ascendc] ===== end operators-quick.log =====
[...]
11272:    511|     },
11273:    512|     {
11274:    513|       "name": "eigensolver_known_spectrum",
11275:    514|       "status": "skipped_retired",
11276:    515|       "reason": "production uses torch_npu eigh"
[...]
11282:    521|     },
11283:    522|     {
11284:    523|       "name": "forensics_eigh_single_rotation",
11285:    524|       "status": "skipped_retired",
11286:    525|       "reason": "production uses torch_npu eigh"
[...]
11289:    528|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
11290:    529|   "model_graph": "not_run",
11291:    530|   "model_accuracy": "not_run",
11292:    531|   "performance": "not_run",
11293:    532|   "library_sha256": "878156e3009dc6a13c5dc16ca322064150111da7ebc9d423fe668087b752d3ea",
[...]
11323: ### 关键报错信息（原文整行摘录，未折行/未截断）
11324: `````text
11325: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/d4a4159698b6b748ac1b66ad20a27d5c42783a5dc592b58056ca946a137d04cd/.prepare-0qioifeu/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/d4a4159698b6b748ac1b66ad20a27d5c42783a5dc592b58056ca946a137d04cd/.prepare-0qioifeu/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260916T072613664068Z/native-calibration.log
11326: [oscar-ascendc] ----- error context -----
11327:    528| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11328:    529| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11329:    530| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11330:    531| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11331:    532| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11332:    533| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11333:    534| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11334:    546| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11335:    547| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11336:    548| ERROR 09-16 07:35:43 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11337:    549| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11338:    550| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11339:    551| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 336, in oscar_calibration_finish
11340:    552| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 336, in oscar_calibration_finish
11341:    556| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11342:    557| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11343:    558| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11344:    559| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11345:    560| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11346:    561| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11347:    562| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11348:    568| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 336, in oscar_calibration_finish
11349:    569| (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11350:    570| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11351:    571| (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11352:    572| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11353:    573| (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]
11354:    574| ERROR 09-16 07:35:43 [multiproc_executor.py:987]
[...]
11356:    600| (EngineCore pid=67421) ERROR 09-16 07:35:43 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11357:    601| (EngineCore pid=67421) ERROR 09-16 07:35:43 [core.py:1413]     raise RuntimeError(
11358:    602| (EngineCore pid=67421) ERROR 09-16 07:35:43 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause
11359:    603| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] Invocation of collective_rpc method failed
11360:    604| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] Traceback (most recent call last):
[...]
11362:    628| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11363:    629| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413]     raise RuntimeError(
11364:    630| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause
11365: [整理者注] 以上为前 40 条不重复匹配行；本条原文共匹配 65 行（完全重复行已合并），其余见下方全文，无任何丢失。
11366: `````
[...]
11375: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
11376: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260916T072613664068Z/operators-quick.log
11377: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
11378: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260916T072613664068Z/native-calibration.log
11379: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/d4a4159698b6b748ac1b66ad20a27d5c42783a5dc592b58056ca946a137d04cd/.prepare-0qioifeu/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/d4a4159698b6b748ac1b66ad20a27d5c42783a5dc592b58056ca946a137d04cd/.prepare-0qioifeu/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260916T072613664068Z/native-calibration.log
11380: Full logs: /workspace/codex_oscar_c/logs/20260916T072613664068Z
11381: 
[...]
11385:      2| INFO 09-16 07:27:49 [__init__.py:44] Available plugins for group vllm.platform_plugins:
11386:      3| INFO 09-16 07:27:49 [__init__.py:46] - ascend -> vllm_ascend:register
11387:    528| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11388:    529| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11389:    530| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11390:    531| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11391:    532| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11392:    533| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11393:    534| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11394:    546| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11395:    547| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11396:    548| ERROR 09-16 07:35:43 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11397:    549| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11398:    550| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11399:    551| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 336, in oscar_calibration_finish
11400:    552| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 336, in oscar_calibration_finish
11401:    556| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11402:    557| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11403:    558| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
11404:    559| (Worker_TP3 pid=68250) (Worker_TP2 pid=68042) (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11405:    560| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11406:    561| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11407:    562| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11408:    568| ERROR 09-16 07:35:43 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 336, in oscar_calibration_finish
11409:    569| (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11410:    570| ERROR 09-16 07:35:43 [multiproc_executor.py:987]     raise RuntimeError(f"a TP rank failed NPU eigensolver validation at {name}/{side}: local={values}")
11411:    571| (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11412:    572| ERROR 09-16 07:35:43 [multiproc_executor.py:987] RuntimeError: a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}
11413:    573| (Worker_TP0 pid=67651) (Worker_TP1 pid=67836) ERROR 09-16 07:35:43 [multiproc_executor.py:987] 
11414:    574| ERROR 09-16 07:35:43 [multiproc_executor.py:987] 
[...]
11416:    600| (EngineCore pid=67421) ERROR 09-16 07:35:43 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11417:    601| (EngineCore pid=67421) ERROR 09-16 07:35:43 [core.py:1413]     raise RuntimeError(
11418:    602| (EngineCore pid=67421) ERROR 09-16 07:35:43 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause
11419:    603| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] Invocation of collective_rpc method failed
11420:    604| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] Traceback (most recent call last):
[...]
11422:    628| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11423:    629| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413]     raise RuntimeError(
11424:    630| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause
11425:    631| INFO 09-16 07:35:44 [core_client.py:652] [shutdown] MPClient: start timeout=60s
11426:    632| INFO 09-16 07:35:44 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
11446:    628| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11447:    629| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413]     raise RuntimeError(
11448:    630| (EngineCore pid=67421) ERROR 09-16 07:35:44 [core.py:1413] RuntimeError: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause
11449:    631| INFO 09-16 07:35:44 [core_client.py:652] [shutdown] MPClient: start timeout=60s
11450:    632| INFO 09-16 07:35:44 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
11484:    666|   File "/usr/local/python3.12.13/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
11485:    667|     raise self._exception
11486:    668| Exception: Call to collective_rpc method failed: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause
11487:    669| {"status": "calibration_failed", "error": "Call to collective_rpc method failed: Worker failed with error 'a TP rank failed NPU eigensolver validation at language_model.model.layers.11.self_attn.attn/v: local={'solver': 'npu_torch_eigh', 'orthogonality_max_error': nan, 'residual_max_error': nan, 'finite': False}', please check the stack trace above for the root cause"}
11488: [oscar-ascendc] ===== end native-calibration.log =====
11489: 
[...]
11672: <!-- ENTRY src=gc idx=24 id=189998166 chars=22215 -->
11673: 
11674: **一行结论**：native-calibration：RuntimeError non-finite covariance before eigh（absmax=nan）
11675: 
11676: ### 关键报错信息（原文整行摘录，未折行/未截断）
11677: `````text
11678: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/0fb01ee2c8fba41dbce49f3be17c5cfff18d52cc3a0e136c9ef83611f7e7a9d3/.prepare-f89vczq9/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/0fb01ee2c8fba41dbce49f3be17c5cfff18d52cc3a0e136c9ef83611f7e7a9d3/.prepare-f89vczq9/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260916T074211378124Z/native-calibration.log
11679: [oscar-ascendc] ----- error context -----
11680:    522| ERROR 09-16 07:50:53 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 298, in oscar_calibration_finish
11681:    523| (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11682:    524| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11683:    525| (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11684:    526| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11685:    527| (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
11686:    528| ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
[...]
11688:    546| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11689:    547| (Worker_TP1 pid=79432) (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11690:    548| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11691:    549| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11692:    550| ERROR 09-16 07:50:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11693:    551| (Worker_TP1 pid=79432) (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 298, in oscar_calibration_finish
[...]
11697:    555| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11698:    556| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11699:    557| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11700:    558| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11701:    559| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
11702:    560| ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
[...]
11704:    569| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11705:    570| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11706:    571| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11707:    572| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11708:    573| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]
11709:    574| ERROR 09-16 07:50:53 [multiproc_executor.py:987]
[...]
11711:    600| (EngineCore pid=79014) ERROR 09-16 07:50:53 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11712:    601| (EngineCore pid=79014) ERROR 09-16 07:50:53 [core.py:1413]     raise RuntimeError(
11713:    602| (EngineCore pid=79014) ERROR 09-16 07:50:53 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan', please check the stack trace above for the root cause
11714:    603| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413] Invocation of collective_rpc method failed
11715:    604| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413] Traceback (most recent call last):
[...]
11738: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
11739: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260916T074211378124Z/operators-quick.log
11740: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
11741: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260916T074211378124Z/native-calibration.log
11742: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/0fb01ee2c8fba41dbce49f3be17c5cfff18d52cc3a0e136c9ef83611f7e7a9d3/.prepare-f89vczq9/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/0fb01ee2c8fba41dbce49f3be17c5cfff18d52cc3a0e136c9ef83611f7e7a9d3/.prepare-f89vczq9/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260916T074211378124Z/native-calibration.log
11743: Full logs: /workspace/codex_oscar_c/logs/20260916T074211378124Z
11744: 
[...]
11751:    523| (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11752:    524| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11753:    525| (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11754:    526| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11755:    527| (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
11756:    528| ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
[...]
11758:    546| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     output = func(*args, **kwargs)
11759:    547| (Worker_TP1 pid=79432) (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11760:    548| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11761:    549| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11762:    550| ERROR 09-16 07:50:53 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
11763:    551| (Worker_TP1 pid=79432) (Worker_TP2 pid=79637) (Worker_TP3 pid=79844) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 298, in oscar_calibration_finish
[...]
11767:    555| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11768:    556| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11769:    557| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11770:    558| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11771:    559| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
11772:    560| ERROR 09-16 07:50:53 [multiproc_executor.py:987] Traceback (most recent call last):
[...]
11774:    569| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11775:    570| ERROR 09-16 07:50:53 [multiproc_executor.py:987]     raise RuntimeError(
11776:    571| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11777:    572| ERROR 09-16 07:50:53 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan
11778:    573| (Worker_TP1 pid=79432) (Worker_TP0 pid=79247) ERROR 09-16 07:50:53 [multiproc_executor.py:987] 
11779:    574| ERROR 09-16 07:50:53 [multiproc_executor.py:987] 
[...]
11781:    600| (EngineCore pid=79014) ERROR 09-16 07:50:53 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11782:    601| (EngineCore pid=79014) ERROR 09-16 07:50:53 [core.py:1413]     raise RuntimeError(
11783:    602| (EngineCore pid=79014) ERROR 09-16 07:50:53 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan', please check the stack trace above for the root cause
11784:    603| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413] Invocation of collective_rpc method failed
11785:    604| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413] Traceback (most recent call last):
[...]
11787:    628| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11788:    629| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413]     raise RuntimeError(
11789:    630| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan', please check the stack trace above for the root cause
11790:    631| INFO 09-16 07:50:54 [core_client.py:652] [shutdown] MPClient: start timeout=60s
11791:    632| INFO 09-16 07:50:54 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
11811:    628| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
11812:    629| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413]     raise RuntimeError(
11813:    630| (EngineCore pid=79014) ERROR 09-16 07:50:54 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan', please check the stack trace above for the root cause
11814:    631| INFO 09-16 07:50:54 [core_client.py:652] [shutdown] MPClient: start timeout=60s
11815:    632| INFO 09-16 07:50:54 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
11849:    666|   File "/usr/local/python3.12.13/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
11850:    667|     raise self._exception
11851:    668| Exception: Call to collective_rpc method failed: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan', please check the stack trace above for the root cause
11852:    669| {"status": "calibration_failed", "error": "Call to collective_rpc method failed: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan', please check the stack trace above for the root cause"}
11853: [oscar-ascendc] ===== end native-calibration.log =====
11854: 
[...]
12041: ### 关键报错信息（原文整行摘录，未折行/未截断）
12042: `````text
12043: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/52fb0f96e4fab39ab57baba88feedc465239ff4937fa2bfc11c6d1ae6b6e8423/.prepare-l3jom13_/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/52fb0f96e4fab39ab57baba88feedc465239ff4937fa2bfc11c6d1ae6b6e8423/.prepare-l3jom13_/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260916T075650844657Z/native-calibration.log
12044: [oscar-ascendc] ----- error context -----
12045:    515| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]              ^^^^^^^^^^^^^^^^^^^^^
12046:    516| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12047:    517| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12048:    518| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-100.01329040527344
12049:    519| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12050:    520| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12053:    523| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12054:    524| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12055:    525| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-100.01329040527344
12056:    526| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]
12057:    527| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
12059:    532| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12060:    533| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12061:    534| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-179.481689453125
12062:    535| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12063:    536| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12066:    539| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12067:    540| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12068:    541| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-179.481689453125
12069:    542| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]
12070:    543| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
12072:    548| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12073:    549| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12074:    550| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125
12075:    551| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12076:    552| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12079:    555| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12080:    556| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12081:    557| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125
12082:    558| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]
12083: [整理者注] 以上为前 40 条不重复匹配行；本条原文共匹配 89 行（完全重复行已合并），其余见下方全文，无任何丢失。
[...]
12104: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
12105: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260916T075650844657Z/operators-quick.log
12106: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
12107: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260916T075650844657Z/native-calibration.log
12108: [oscar-ascendc] FAILED phase=native-calibration: Phase failed (exit 1): ['/usr/local/python3.12.13/bin/python3', '-m', 'oscar_ascend.calibrate', '--request', '/workspace/codex_oscar_c/artifacts/rotations/52fb0f96e4fab39ab57baba88feedc465239ff4937fa2bfc11c6d1ae6b6e8423/.prepare-l3jom13_/request.json', '--output', '/workspace/codex_oscar_c/artifacts/rotations/52fb0f96e4fab39ab57baba88feedc465239ff4937fa2bfc11c6d1ae6b6e8423/.prepare-l3jom13_/rotations.pt']; full log: /workspace/codex_oscar_c/logs/20260916T075650844657Z/native-calibration.log
12109: Full logs: /workspace/codex_oscar_c/logs/20260916T075650844657Z
12110: 
[...]
12117:    516| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12118:    517| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12119:    518| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-100.01329040527344
12120:    519| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12121:    520| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12124:    523| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12125:    524| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12126:    525| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-100.01329040527344
12127:    526| (Worker_TP3 pid=91046) ERROR 09-16 08:05:29 [multiproc_executor.py:987] 
12128:    527| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
12130:    532| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12131:    533| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12132:    534| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-179.481689453125
12133:    535| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12134:    536| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12137:    539| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12138:    540| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12139:    541| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-179.481689453125
12140:    542| (Worker_TP2 pid=90838) ERROR 09-16 08:05:29 [multiproc_executor.py:987] 
12141:    543| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
12143:    548| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12144:    549| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12145:    550| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125
12146:    551| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12147:    552| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12150:    555| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12151:    556| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12152:    557| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125
12153:    558| (Worker_TP0 pid=90444) ERROR 09-16 08:05:29 [multiproc_executor.py:987] 
12154:    559| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
12156:    564| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12157:    565| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12158:    566| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-135.803466796875
12159:    567| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
12160:    568| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
12163:    571| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987]   File "/workspace/codex_oscar_c/oscar_ascend/calibration_worker.py", line 300, in oscar_calibration_finish
12164:    572| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987]     raise RuntimeError(
12165:    573| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987] RuntimeError: non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-135.803466796875
12166:    574| (Worker_TP1 pid=90632) ERROR 09-16 08:05:29 [multiproc_executor.py:987] 
12167:    575| (EngineCore pid=90211) ERROR 09-16 08:05:29 [core.py:1413] Invocation of collective_rpc method failed
[...]
12169:    600| (EngineCore pid=90211) ERROR 09-16 08:05:29 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
12170:    601| (EngineCore pid=90211) ERROR 09-16 08:05:29 [core.py:1413]     raise RuntimeError(
12171:    602| (EngineCore pid=90211) ERROR 09-16 08:05:29 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125', please check the stack trace above for the root cause
12172:    603| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413] Invocation of collective_rpc method failed
12173:    604| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413] Traceback (most recent call last):
[...]
12175:    628| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
12176:    629| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413]     raise RuntimeError(
12177:    630| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-135.803466796875', please check the stack trace above for the root cause
12178:    631| INFO 09-16 08:05:30 [core_client.py:652] [shutdown] MPClient: start timeout=60s
12179:    632| INFO 09-16 08:05:30 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
12199:    628| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
12200:    629| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413]     raise RuntimeError(
12201:    630| (EngineCore pid=90211) ERROR 09-16 08:05:30 [core.py:1413] RuntimeError: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-135.803466796875', please check the stack trace above for the root cause
12202:    631| INFO 09-16 08:05:30 [core_client.py:652] [shutdown] MPClient: start timeout=60s
12203:    632| INFO 09-16 08:05:30 [core_client.py:654] [shutdown] MPClient: stopping engine manager
[...]
12237:    666|   File "/usr/local/python3.12.13/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
12238:    667|     raise self._exception
12239:    668| Exception: Call to collective_rpc method failed: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125', please check the stack trace above for the root cause
12240:    669| {"status": "calibration_failed", "error": "Call to collective_rpc method failed: Worker failed with error 'non-finite covariance before eigh at language_model.model.layers.11.self_attn.attn/v: absmax=nan, weighted_finite=False, weighted_nan=65536, weight_sum_finite=False, last_tile_weight_min=-1434.328125', please check the stack trace above for the root cause"}
12241: [oscar-ascendc] ===== end native-calibration.log =====
12242: 
[...]
12455: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
12456: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260916T081736976018Z/operators-quick.log
12457: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
12458: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260916T081736976018Z/native-calibration.log
12459: [W916 08:26:58.755134840 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
12460: [oscar-ascendc] rotations generated: /workspace/codex_oscar_c/artifacts/rotations/52fb0f96e4fab39ab57baba88feedc465239ff4937fa2bfc11c6d1ae6b6e8423/rotations.pt
12461: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260916T081736976018Z/operators-ranks4.log
12462: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260916T081736976018Z/window-pipeline.log
[...]
12573: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
12574: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260916T084952049123Z/operators-quick.log
12575: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
12576: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260916T084952049123Z/native-calibration.log
12577: [W916 08:59:07.400051030 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
12578: [oscar-ascendc] rotations generated: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
12579: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260916T084952049123Z/operators-ranks4.log
12580: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260916T084952049123Z/window-pipeline.log
[...]
12623: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
12624: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T002953975654Z/operators-quick.log
12625: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
12626: [W917 00:31:22.867429150 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
12627: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
12628: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T002953975654Z/operators-ranks4.log
12629: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T002953975654Z/window-pipeline.log
[...]
12770: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
12771: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T004335284515Z/operators-quick.log
12772: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
12773: [W917 00:45:03.978628140 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
12774: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
12775: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T004335284515Z/operators-ranks4.log
12776: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T004335284515Z/window-pipeline.log
[...]
12983: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
12984: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T004801494133Z/operators-quick.log
12985: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
12986: [W917 00:49:31.347481810 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
12987: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
12988: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T004801494133Z/operators-ranks4.log
12989: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T004801494133Z/window-pipeline.log
[...]
13176: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
13177: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T005401657824Z/operators-quick.log
13178: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
13179: [W917 00:55:30.256063550 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
13180: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
13181: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T005401657824Z/operators-ranks4.log
13182: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T005401657824Z/window-pipeline.log
[...]
13444: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
13445: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T010159828698Z/operators-quick.log
13446: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
13447: [W917 01:03:27.678741490 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
13448: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
13449: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T010159828698Z/operators-ranks4.log
13450: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T010159828698Z/window-pipeline.log
[...]
13754: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
13755: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T011002730602Z/operators-quick.log
13756: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
13757: [W917 01:11:31.626871230 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
13758: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
13759: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T011002730602Z/operators-ranks4.log
13760: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T011002730602Z/window-pipeline.log
[...]
14112: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
14113: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T015159540895Z/operators-quick.log
14114: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
14115: [W917 01:53:29.867603540 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
14116: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
14117: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T015159540895Z/operators-ranks4.log
14118: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T015159540895Z/window-pipeline.log
[...]
14196: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
14197: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T024807645324Z/operators-quick.log
14198: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
14199: [W917 02:49:35.281526890 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
14200: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
14201: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T024807645324Z/operators-ranks4.log
14202: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T024807645324Z/window-pipeline.log
[...]
14957: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
14958: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T042922025320Z/operators-quick.log
14959: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
14960: [W917 04:30:50.578198720 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
14961: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
14962: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T042922025320Z/operators-ranks4.log
14963: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T042922025320Z/window-pipeline.log
[...]
15213: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
15214: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T044213504386Z/operators-quick.log
15215: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
15216: [W917 04:43:41.820316180 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
15217: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
15218: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T044213504386Z/operators-ranks4.log
15219: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T044213504386Z/window-pipeline.log
[...]
15609: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
15610: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T045436643987Z/operators-quick.log
15611: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
15612: [W917 04:56:05.753908860 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
15613: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
15614: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T045436643987Z/operators-ranks4.log
15615: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T045436643987Z/window-pipeline.log
[...]
15868: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
15869: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T052719556713Z/operators-quick.log
15870: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
15871: [W917 05:28:47.008216160 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
15872: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
15873: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T052719556713Z/operators-ranks4.log
15874: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T052719556713Z/window-pipeline.log
[...]
16224: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
16225: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T054149676092Z/operators-quick.log
16226: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
16227: [W917 05:43:18.951038160 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
16228: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/587e660a2fdd8d0081b8b8766c27370a06e31cdf2d43cfdd6b4bf522678161b9/rotations.pt
16229: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T054149676092Z/operators-ranks4.log
16230: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T054149676092Z/window-pipeline.log
[...]
16546: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
16547: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T055654075703Z/operators-quick.log
16548: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
16549: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260917T055654075703Z/native-calibration.log
16550: [W917 06:06:06.692201800 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
16551: [oscar-ascendc] rotations generated: /workspace/codex_oscar_c/artifacts/rotations/e02253e075e30a05b9a9e8984a4b28b6188396d6d6fe9fa6ab02641ef0cf73e5/rotations.pt
16552: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T055654075703Z/operators-ranks4.log
16553: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T055654075703Z/window-pipeline.log
[...]
16806: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
16807: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T062533985057Z/operators-quick.log
16808: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
16809: [W917 06:27:02.773943390 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
16810: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/e02253e075e30a05b9a9e8984a4b28b6188396d6d6fe9fa6ab02641ef0cf73e5/rotations.pt
16811: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T062533985057Z/operators-ranks4.log
16812: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T062533985057Z/window-pipeline.log
[...]
17180: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
17181: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T063829947178Z/operators-quick.log
17182: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
17183: [W917 06:39:56.895294210 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
17184: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/e02253e075e30a05b9a9e8984a4b28b6188396d6d6fe9fa6ab02641ef0cf73e5/rotations.pt
17185: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T063829947178Z/operators-ranks4.log
17186: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T063829947178Z/window-pipeline.log
[...]
18199:     20| CHECK {"name": "window_attention_twin", "head_dim": 256, "status": "failed", "error": "RuntimeError(\"oscar_ascend::window_attention_out() is missing value for argument 'raw'. Declaration: oscar_ascend::window_attention_out(Tensor query, Tensor key, Tensor value, Tensor window_k, Tensor window_v, Tensor window_positions, Tensor row_to_window, Tensor qsl, Tensor query_positions, Tensor(a!) output, Tensor(b!) lse, float scale, Tensor(c!) workspace, int max_query_len, int raw) -> ()\")"}
18200:     21| CHECK {"name": "forensics_eigh_diagonal", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
18201:     22| CHECK {"name": "forensics_eigh_single_rotation", "status": "skipped_retired", "reason": "production uses torch_npu eigh"}
18202:     23| {"rank": 0, "status": "failed", "report": "/workspace/codex_oscar_c/logs/20260917T080928188701Z/operators-quick/rank_0.json", "kernels_sha256": {"lib/liboscar_ascend_kernels.so": "c91bd78d2565c63aa2e858a0f28875d99fda832dcb6d6c22dd75bc5b925b4bd5"}}
18203: [oscar-ascendc] ===== end operators-quick.log =====
[...]
18272:    509|     },
18273:    510|     {
18274:    511|       "name": "eigensolver_known_spectrum",
18275:    512|       "status": "skipped_retired",
18276:    513|       "reason": "production uses torch_npu eigh"
[...]
18282:    519|     },
18283:    520|     {
18284:    521|       "name": "forensics_eigh_single_rotation",
18285:    522|       "status": "skipped_retired",
18286:    523|       "reason": "production uses torch_npu eigh"
[...]
18289:    526|   "scope": "independent small NPU operators; not model TP4/MTP/prefix/graph acceptance",
18290:    527|   "model_graph": "not_run",
18291:    528|   "model_accuracy": "not_run",
18292:    529|   "performance": "not_run",
18293:    530|   "library_sha256": "b967f6909cac5d573e5c702653a1c78ce5d65d28c7e3be795e16b9ee2acacff6",
[...]
18399: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
18400: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T081512424574Z/operators-quick.log
18401: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
18402: [oscar-ascendc] native-calibration; log: /workspace/codex_oscar_c/logs/20260917T081512424574Z/native-calibration.log
18403: [W917 08:24:36.138780800 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
18404: [oscar-ascendc] rotations generated: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
18405: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T081512424574Z/operators-ranks4.log
18406: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T081512424574Z/window-pipeline.log
[...]
18617: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
18618: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T082816432129Z/operators-quick.log
18619: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
18620: [W917 08:29:44.680729780 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
18621: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
18622: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T082816432129Z/operators-ranks4.log
18623: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T082816432129Z/window-pipeline.log
[...]
18848: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
18849: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T084020405665Z/operators-quick.log
18850: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
18851: [W917 08:41:49.745393570 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
18852: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
18853: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T084020405665Z/operators-ranks4.log
18854: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T084020405665Z/window-pipeline.log
[...]
19084: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
19085: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T084513555690Z/operators-quick.log
19086: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
19087: [W917 08:46:41.017788320 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
19088: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
19089: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T084513555690Z/operators-ranks4.log
19090: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T084513555690Z/window-pipeline.log
[...]
19337: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
19338: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T085556428411Z/operators-quick.log
19339: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
19340: [W917 08:57:23.596538960 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
19341: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
19342: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T085556428411Z/operators-ranks4.log
19343: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T085556428411Z/window-pipeline.log
[...]
19629: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
19630: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T090330416812Z/operators-quick.log
19631: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
19632: [W917 09:04:57.248120720 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
19633: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
19634: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T090330416812Z/operators-ranks4.log
19635: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T090330416812Z/window-pipeline.log
[...]
19921: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
19922: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T093449989981Z/operators-quick.log
19923: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
19924: [W917 09:36:19.449786600 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
19925: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
19926: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T093449989981Z/operators-ranks4.log
19927: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T093449989981Z/window-pipeline.log
[...]
20208: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
20209: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T104842430522Z/operators-quick.log
20210: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
20211: [W917 10:50:12.777287210 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
20212: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
20213: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T104842430522Z/operators-ranks4.log
20214: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T104842430522Z/window-pipeline.log
[...]
20439: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
20440: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T110214484213Z/operators-quick.log
20441: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
20442: [W917 11:03:43.899296830 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
20443: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
20444: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T110214484213Z/operators-ranks4.log
20445: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T110214484213Z/window-pipeline.log
[...]
20628: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
20629: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T110655331805Z/operators-quick.log
20630: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
20631: [W917 11:08:21.410610850 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
20632: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
20633: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T110655331805Z/operators-ranks4.log
20634: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T110655331805Z/window-pipeline.log
[...]
20803: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
20804: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T112135239555Z/operators-quick.log
20805: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
20806: [W917 11:23:03.027367140 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
20807: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
20808: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T112135239555Z/operators-ranks4.log
20809: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T112135239555Z/window-pipeline.log
[...]
20936: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
20937: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T112853727343Z/operators-quick.log
20938: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
20939: [W917 11:30:21.255473700 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
20940: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
20941: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T112853727343Z/operators-ranks4.log
20942: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T112853727343Z/window-pipeline.log
[...]
21116: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
21117: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T113653158344Z/operators-quick.log
21118: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
21119: [W917 11:38:21.413653670 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
21120: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
21121: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T113653158344Z/operators-ranks4.log
21122: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T113653158344Z/window-pipeline.log
[...]
21311: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
21312: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T114409465188Z/operators-quick.log
21313: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
21314: [W917 11:45:39.988533220 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
21315: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
21316: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T114409465188Z/operators-ranks4.log
21317: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T114409465188Z/window-pipeline.log
[...]
21620: [oscar-ascendc] kernel library directories on LD_LIBRARY_PATH: ['/workspace/codex_oscar_c/build/ascendc/lib']
21621: [oscar-ascendc] operators-quick; log: /workspace/codex_oscar_c/logs/20260917T123559110624Z/operators-quick.log
21622: [oscar-ascendc] checking model-matched rotations.pt; missing/invalid auto-cache triggers native calibration
21623: [W917 12:37:26.394242740 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
21624: [oscar-ascendc] rotations reused: /workspace/codex_oscar_c/artifacts/rotations/a7167ed349839596c3ebb19a01a0dcee4bcbe3bf61fad8a9804f5b3535ff8612/rotations.pt
21625: [oscar-ascendc] operators-ranks4; log: /workspace/codex_oscar_c/logs/20260917T123559110624Z/operators-ranks4.log
21626: [oscar-ascendc] window-pipeline; log: /workspace/codex_oscar_c/logs/20260917T123559110624Z/window-pipeline.log
[...]
21637:     30| Traceback (most recent call last):
21638:     31|   File "/workspace/codex_oscar_c/tests/test_npu_window_pipeline.py", line 274, in test_prefill_continuation_matches_dense_golden
21639:     32|     ref_k[4:8] = torch.matmul(dk[4:8], self.rotation.t()).to(torch.bfloat16)
21640:     33|                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
21641:     34| RuntimeError: Expected all tensors to be on the same device, but got other is on npu:0, different from other tensors on cpu (when checking argument in method wrapper_NPU__matmul)
[...]
21674:     30| Traceback (most recent call last):
21675:     31|   File "/workspace/codex_oscar_c/tests/test_npu_window_pipeline.py", line 274, in test_prefill_continuation_matches_dense_golden
21676:     32|     ref_k[4:8] = torch.matmul(dk[4:8], self.rotation.t()).to(torch.bfloat16)
21677:     33|                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
21678:     34| RuntimeError: Expected all tensors to be on the same device, but got other is on npu:0, different from other tensors on cpu (when checking argument in method wrapper_NPU__matmul)
[...]
22182: | [82] | build 第二轮：unknown type name 'bfloat16_t' ×26 |
22183: | [83] | build 第三轮 |
22184: | [84] | build 全链通过后 prepare-rotations FAIL：c10 pool INTERNAL ASSERT FAILED 'Invalid thread pool!' |
22185: | [85] | build 第四轮：merge_aiv/aic_obj_text 链接失败 ld.lld unknown file type |
22186: | [86] | prepare-rotations：collective_rpc 打通但 oscar_calib_begin fail-closed |
22187: 
22188: ## 逐条详情（原文全文，零截断；评论 4/6 为平台 65535 截断，已标注）
[...]
24706: <!-- ENTRY src=gc idx=84 id=190446656 chars=25828 -->
24707: 
24708: **一行结论**：build 全链通过后 prepare-rotations FAIL：c10 pool INTERNAL ASSERT FAILED 'Invalid thread pool!'（档案 G15~G17/#29/#30 同族）——根因：vLLM multiproc_executor 只在 OMP_NUM_THREADS 未设置时才在父进程建池，我们 pin 了 OMP 反而跳过其建池分支，fork 出的 worker 首触池即炸（修法：父进程 fork 前显式 pin_torch_threads_for_fork() 建池）
24709: 
24710: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
24769: CHECK build_manifest PASS: 5 个产物，manifest=/workspace/kimi_oscar/build/ascendc/build_manifest.json
24770: [oscar-ascend] 2026-09-18T08:45:11Z build phase 完成：LIB_DIR=/workspace/kimi_oscar/build/ascendc/lib OPP_DIR=/workspace/kimi_oscar/build/ascendc/opp/vendors/oscar_ascend
24771: [oscar-ascend] prepare-rotations; log: /workspace/kimi_oscar/logs/20260918T084309Z/prepare-rotations.log
24772: [oscar-ascend] 2026-09-18T08:45:12Z 旋转 checkpoint 缺失，启动 NPU 校准（TP=4 引擎；全流程 NPU；单 pass 确定性采样）
24773: [oscar-calib] 2026-09-18T08:45:13Z NPU 空闲显存校验通过: {0: '2894/32768MB', 1: '2893/32768MB', 2: '2892/32768MB', 3: '2891/32768MB'}（每卡需求 ≥24.0GiB）
24774: [W918 08:45:15.375512150 FunctionLoader.cpp:48] Warning: LD_PRELOAD detected, FunctionLoader prefers RTLD_DEFAULT for symbol resolution. (function operator())
[...]
24887:   warnings.warn('resource_tracker: There appear to be %d '
24888: Traceback (most recent call last):
24889:   File "/workspace/kimi_oscar/tools/calibrate_rotations.py", line 431, in <module>
24890:     main()
24891:   File "/workspace/kimi_oscar/tools/calibrate_rotations.py", line 427, in main
24892:     cmd_calibrate(args)
24893:   File "/workspace/kimi_oscar/tools/calibrate_rotations.py", line 308, in cmd_calibrate
24894:     llm = build_llm(args)
24895:           ^^^^^^^^^^^^^^^
24896:   File "/workspace/kimi_oscar/tools/calibrate_rotations.py", line 185, in build_llm
24897:     return LLM(**kwargs)
24898:            ^^^^^^^^^^^^^
[...]
24925: RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {'EngineCore': 1}
24926: [ERROR] 2026-09-18-08:46:26 (PID:6244, Device:-1, RankID:-1) ERR99999 UNKNOWN applicaiton exception
24927: [oscar-ascend] 2026-09-18T08:46:29Z ERROR: FAILED phase=prepare-rotations: exit=1
24928: [oscar-ascend] 2026-09-18T08:46:29Z ERROR: Full logs: /workspace/kimi_oscar/logs/20260918T084309Z
24929: [oscar-ascend] 2026-09-18T08:46:29Z ERROR: status: /workspace/kimi_oscar/logs/20260918T084309Z/status.json
[...]
24976:  oscar_ascend/envs.py           | 19 +++++++++++++++++++
24977:  tests/npu/test_layout_probe.py |  3 +++
24978:  tools/calibrate_rotations.py   |  3 +++
24979:  4 files changed, 26 insertions(+), 1 deletion(-)
24980: [oscar-ascend] 2026-09-18T08:55:32Z OMP_NUM_THREADS pinned=1（import torch 前定死，子进程继承同一值）
[...]
25154: <!-- ENTRY src=gc idx=86 id=190453861 chars=15645 -->
25155: 
25156: **一行结论**：prepare-rotations：collective_rpc 打通但 oscar_calib_begin fail-closed——expect_layers=17 与校准引擎（无 speculative_config）只有 16 个 FULL 层不符（修法：校准 16 模型层，MTP draft 层按 PR 语义 identity 回退；draft 在 max_tokens=1 校准时从不触发，协方差必为空矩阵）
25157: 
25158: ### 关键报错信息（原文整行摘录，未折行/未截断）
[...]
25162: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25163: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25164: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25165: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
25166: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
25169: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25170: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25171: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25172: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] 
25173: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
25184: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25185: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25186: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25187: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
25188: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
25191: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25192: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25193: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25194: (Worker_TP1 pid=8695) ERROR 09-18 09:05:29 [multiproc_executor.py:987] 
25195: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
25200: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25201: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25202: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25203: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
25204: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
25207: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25208: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25209: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25210: (Worker_TP0 pid=8693) ERROR 09-18 09:05:29 [multiproc_executor.py:987] 
25211: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
25216: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25217: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25218: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25219: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
25220: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
25223: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25224: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25225: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25226: (Worker_TP2 pid=8697) ERROR 09-18 09:05:29 [multiproc_executor.py:987] 
25227: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987] WorkerProc hit an exception.
[...]
25232: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25233: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25234: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25235: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987] Traceback (most recent call last):
25236: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 982, in worker_busy_loop
[...]
25239: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987]   File "/workspace/kimi_oscar/oscar_ascend/calibration.py", line 278, in oscar_calib_begin
25240: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987]     raise OscarError(
25241: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987] oscar_ascend.errors.OscarError: OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).
25242: (Worker_TP3 pid=8699) ERROR 09-18 09:05:29 [multiproc_executor.py:987] 
25243: (EngineCore pid=8686) ERROR 09-18 09:05:29 [core.py:1413] Invocation of collective_rpc method failed
[...]
25268: (EngineCore pid=8686) ERROR 09-18 09:05:29 [core.py:1413]   File "/vllm-workspace/vllm/vllm/v1/executor/multiproc_executor.py", line 391, in get_response
25269: (EngineCore pid=8686) ERROR 09-18 09:05:29 [core.py:1413]     raise RuntimeError(
25270: (EngineCore pid=8686) ERROR 09-18 09:05:29 [core.py:1413] RuntimeError: Worker failed with error 'OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).', please check the stack trace above for the root cause
25271: [oscar-calib] ERROR oscar_calib_begin 失败: Exception("Call to collective_rpc method failed: Worker failed with error 'OSCAR calib: found 16 FULL attention layers ([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]) but expect_layers=17. Note: the MTP draft FULL layer only exists when the engine loads the draft model (speculative_config); without it only the 16 model layers are present and the draft layer's rotation falls back to identity at serve time (PR semantics).', please check the stack trace above for the root cause")
25272: (EngineCore pid=8686) INFO 09-18 09:05:29 [core.py:1178] [shutdown] EngineCore: trigger received signal=SIGTERM
25273: (EngineCore pid=8686) INFO 09-18 09:05:29 [core.py:1297] [shutdown] EngineCore: start mode=abort timeout=0s
[...]
25278: (EngineCore pid=8686) INFO 09-18 09:05:32 [multiproc_executor.py:433] [shutdown] Executor: all workers exited gracefully
25279: WARNING 09-18 09:05:34 [utils.py:607] [shutdown] Process manager: force killing remaining processes count=1
25280: [oscar-ascend] 2026-09-18T09:05:39Z ERROR: FAILED phase=prepare-rotations: exit=5
25281: [oscar-ascend] 2026-09-18T09:05:39Z ERROR: Full logs: /workspace/kimi_oscar/logs/20260918T090112Z
25282: [oscar-ascend] 2026-09-18T09:05:39Z ERROR: status: /workspace/kimi_oscar/logs/20260918T090112Z/status.json
[...]
25524: ---
25525: 
25526: ## [96] 真机条目（oscar-ascend 项目，2026-09-21T04:39:55Z）· phase=prepare-rotations
25527: 
25528: **症状**：torch_npu 装不完整时 import torch 在设备后端自动加载阶段抛异常，把"只需要一个 Hadamard 矩阵"的工具整段带崩
25529: 
25530: **命中的历史同族条目**：#74/#76
[...]
25538: ### 根因
25539: 
25540: torch 2.x 在 import 期自动加载设备后端扩展；该环境里 torch_npu 注册不完整，于是 import torch 本身就失败。失败点与工具意图无关，却让 prepare_rotations / check_rotations 等纯 CPU 工具无法运行，进而把一键脚本的相位带崩（档案 #74/#76：前置检查应记录制，不该因环境组成差异误杀）
25541: 
25542: ### 修法
25543: 
25544: 新增 tools/oscar_tool_env.py：在任何 import torch 之前 setdefault("TORCH_DEVICE_BACKEND_AUTOLOAD","0")（torch 官方开关，只影响 import 期后端注册，**不改变任何数值语义、也不会把张量降级到 CPU**）；prepare_rotations/check_rotations/probe_ascendc_ops 启动即 bootstrap；需要 NPU 的场景可用 OSCAR_ALLOW_TORCH_DEVICE_BACKEND=1 反向 opt-in
25545: 
25546: ### 证据
25547: 
25548: oscar-ascend/logs/phases/prepare-rotations.log
25549: 
25550: ---
25551: 
25552: ## [97] 真机条目（oscar-ascend 项目，2026-09-21T04:39:55Z）· phase=prepare-rotations
25553: 
25554: **症状**：一键脚本在拿到旋转检查点之前就停下：现场手上没有检查点，而流程没有任何"就地产出"的能力
25555: 
25556: **命中的历史同族条目**：（无，属新增族，请在症状速查表补一行）
[...]
25559: 
25560: ``````text
25561: [oscar] FAILED phase=prepare-rotations: 未提供旋转检查点
25562: ``````
25563: 
25564: ### 根因
25565: 
25566: prepare-rotations 相位只做"校验已有检查点"或"identity"，缺"缺检查点时就地产出"这一分支；而仓库本来就有 tools/prepare_rotations.py（默认 data-free Hadamard，与论文权威脚本的 --method hadamard 数学一致），只是没接进流程
25567: 
25568: ### 修法
25569: 
25570: prepare-rotations 增加就地分支：未提供检查点时用 tools/prepare_rotations.py --mode hadamard 产出（head_dim/层数可经 OSCAR_HEAD_DIM/OSCAR_NUM_LAYERS 覆盖）并立即过 check_rotations 门禁；旋转来源写入日志与 logs/status.json（rotation=provided|identity|hadamard(data-free)），并在收尾 banner 明确提示"要报端到端精度必须换论文校准检查点"
25571: 
25572: ### 证据
25573: 
25574: oscar-ascend/logs/phases/prepare-rotations.log
25575: 
25576: ---
[...]
25932: ### 修法
25933: 
25934: dtype 收口放在**适配层** oscar_ops_npu.store_int2：非 fp16 的 K/V 显式 .to(torch.float16)（确定性的一次 rounding，且量化本来就发生在 fp16 精度面上）；bf16 仍显式拒绝（不在编译时 dtype 集合内，静默转换会掩盖配置错误）。选择适配层而非调用方的理由：它是 Python 与算子之间唯一的接缝，ops.store_kv 的契约（已旋转+已裁剪）并未规定精度。新增契约测试断言该转换存在且 bf16 仍被拒绝，并核对 def.cpp 的 K/V 只声明 DT_FLOAT16（含反向验证）
25935: 
25936: ### 证据
[...]
26287: ### 修法
26288: 
26289: 本项目默认设备改为 `[0,1,2,3]`，SOC 使用本次附录 F 的 `ascend910b4`，端口保留附录 A 的 `8989`；子进程统一使用本项目配置，不继承其他任务卡号。按用户“不要任何真机上的环境检查”及随后“探针要的”的要求，默认部署移除环境清单、原生源码扫描和 readiness 前置审计，保留真实 NPU 算子、CV/旋转、TP4/MTP/长输入/图服务探针及资源回收；探针失败必须停止。配置本身非法、实际编译或运行失败仍保留错误与退出码。
26290: 
26291: ### 证据与复验边界
[...]
26416: - loader 在正常导入 torch_npu 后，使用 manifest 中经过指纹校验的 kernel **绝对路径**执行 `ctypes.CDLL`，采用 `RTLD_NOW | RTLD_LOCAL` 并保留句柄，再导入 Python 扩展。库缺失、加载或符号解析失败继续报错，不把错误转换为 CPU 或原生 FULL 路由。
26417: - 相位和服务子进程的输出实时转发到当前终端，并保留原始日志；Python 子进程使用无缓冲输出。启动、结果、traceback、失败阶段、退出码和日志路径均可见，超时/中断仍清理本任务进程组。
26418: - 保留真实 NPU 算子、CV/旋转及完整服务探针；任何探针失败不得进入后续正式服务，不重新加入环境清单或 readiness 前置审计。
26419: 
26420: ### 证据与复验边界
[...]
26443: - 本条原始日志属于`/workspace/gpt_new_oscar`，直接保存于`reports/target_cv_failure_input.txt`，共18162字节，SHA256为`87d314470d6428ad1e0f9c6f92d6ab1404afc2480e0d21e78292c696bbb16e2a`。该文件逐字节保留用户附件；没有使用其他项目日志。
26444: - `build-ops`返回0；`probe-ops`报告`primitive_probe_passed`、`device=npu:0`、`device_name=Ascend910B4`。解析其cases数组共有75项（54项store、21项merge），每项`device_completion=passed`，覆盖D64/D128/D256、边界、非法数值及地址复用。它们仅在逻辑设备`npu:0`运行，不是TP4多卡验收。这证明原语调用实际完成，并确认#125加载故障已越过。
26445: - `probe-cv`调用真实NPU算子并同步。失败发生在输出与独立dense PR oracle比较；此前status全零及positions比较通过，但这不能代表输出精度通过。测试在输出断言处终止，后续LSE正确性不能据此签成通过。
26446: - `--maxfail=1`使测试在首个失败后停止：本轮`1 failed, 3 passed`，返回码1。前3项是Python/源码契约测试，不是3项CV真NPU用例通过。其余CV用例、旋转探针、自动旋转文件、完整服务探针及正式服务未由这份日志证明执行或通过。
26447: - 原语报告明确`graph_capture=not_run`、`graph_replay=not_run`、`full_service_acceptance=not_run`、`performance=not_run`。本次不能把原语成功或status零记作完整NPU/图/性能验收。
26448: 
[...]
26459: 在padding分支的`Duplicate`之前增加`MTE3 → V`事件等待，确保上一行的MTE3搬出完成后才在Vector上清零复用缓冲。改动只约束固定query tile内的已有缓冲生命周期：不增加历史恢复量，不新增全历史BF16存储，不加入Host逐head处理或CPU数值替代路径。按启动文档D.4继续保留CV融合路径和有界workspace，性能仍由真机实测判定。
26460: 
26461: 保留`configs/acceptance.json`冻结容差及失败用例，并以有效行转padding行的边界作为同步回归。任何源码修订、CPU或CANN VM验证都单独记账；目标CV数值、旋转、图、服务与性能仍需修订后的真机日志逐项确认。默认部署在本次探针失败后立即停止，真实退出码及traceback保持实时可见。回归项登记在`docs/design.md`第7节。
26462: 
26463: ### 用户回传日志全文
[...]
27034: RESULT {"phase": "probe-ops", "command": ["/usr/local/python3.12.13/bin/python3", "-m", "tools.probe_ops", "--output", "/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/operators.json"], "returncode": 0, "elapsed_seconds": 13.41138, "timed_out": false, "interrupted": false, "log": "/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/probe-ops.log", "cleanup_complete": true}
27035: [oscar] PASSED phase=probe-ops rc=0 log=/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/probe-ops.log
27036: START phase=probe-cv cwd=/workspace/gpt_new_oscar command=["/usr/local/python3.12.13/bin/python3", "-m", "pytest", "-q", "--maxfail=1", "/workspace/gpt_new_oscar/tests/test_cv_contracts.py", "/workspace/gpt_new_oscar/tests/test_rotation_npu.py", "--junitxml=/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/cv-npu.xml"]
27037: ...F
27038: =================================== FAILURES ===================================
[...]
27086: !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
27087: 1 failed, 3 passed, 14 warnings in 9.83s
27088: RESULT {"phase": "probe-cv", "command": ["/usr/local/python3.12.13/bin/python3", "-m", "pytest", "-q", "--maxfail=1", "/workspace/gpt_new_oscar/tests/test_cv_contracts.py", "/workspace/gpt_new_oscar/tests/test_rotation_npu.py", "--junitxml=/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/cv-npu.xml"], "returncode": 1, "elapsed_seconds": 14.112283, "timed_out": false, "interrupted": false, "log": "/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/probe-cv.log", "cleanup_complete": true}
27089: [oscar] FAILED phase=probe-cv rc=1 log=/workspace/gpt_new_oscar/logs/20260922T033934.426635Z/probe-cv.log
27090: root@node93:/workspace/gpt_new_oscar#
[...]
27112: ### 证据边界
27113: 
27114: 此次日志进入service-probe，显示4个TP worker和MTP模型加载，但未附前序CV/旋转探针结果，不能凭此补写逐项NPU通过证据。当前错误发生在缓存spec初始化，尚未证明图捕获、回放或真实请求成功。源码修复后的目标复跑待回传。
27115: 
27116: ### 用户原文全文
[...]
27604: ### 修复
27605: 
27606: 外部spec实现该原生复制方法：只有受支持的kernel128或原物理块长可被复制；metadata副本带显式标记，保留physical layout、storage_block_size、GDN字段及page字节数。原始group spec不变，普通物理页resize和非法块长仍拒绝。真实原生proposer与AttentionGroup方法、外部builder共同执行的回归覆盖none/align、kernel128/无kernel override、多个独立builder、复制恢复及MTP虚拟slot更新。未修改原生源码、CANN算子、精度阈值或启动参数。
27607: 
27608: ### 证据边界
[...]
27686: (EngineCore pid=8050) INFO 09-22 05:20:38 [kv_cache_utils.py:1744] GPU KV cache size: 2,779,715 tokens
27687: (EngineCore pid=8050) INFO 09-22 05:20:38 [kv_cache_utils.py:1745] Maximum concurrency for 262,144 tokens per request: 10.60x
27688: (Worker_TP0 pid=8100) /workspace/gpt_new_oscar/oscar_ascend/runtime.py:320: RuntimeWarning: OSCAR MTP rotation is explicit PR identity: mtp.layers.0.self_attn.attn
27689: (Worker_TP0 pid=8100)   warnings.warn(f"OSCAR MTP rotation is explicit PR identity: {name}", RuntimeWarning)
27690: (Worker_TP2 pid=8194) /workspace/gpt_new_oscar/oscar_ascend/runtime.py:320: RuntimeWarning: OSCAR MTP rotation is explicit PR identity: mtp.layers.0.self_attn.attn
27691: (Worker_TP2 pid=8194)   warnings.warn(f"OSCAR MTP rotation is explicit PR identity: {name}", RuntimeWarning)
27692: (Worker_TP3 pid=8254) /workspace/gpt_new_oscar/oscar_ascend/runtime.py:320: RuntimeWarning: OSCAR MTP rotation is explicit PR identity: mtp.layers.0.self_attn.attn
27693: (Worker_TP3 pid=8254)   warnings.warn(f"OSCAR MTP rotation is explicit PR identity: {name}", RuntimeWarning)
27694: (Worker_TP1 pid=8136) /workspace/gpt_new_oscar/oscar_ascend/runtime.py:320: RuntimeWarning: OSCAR MTP rotation is explicit PR identity: mtp.layers.0.self_attn.attn
27695: (Worker_TP1 pid=8136)   warnings.warn(f"OSCAR MTP rotation is explicit PR identity: {name}", RuntimeWarning)
27696: (Worker_TP0 pid=8100) ERROR 09-22 05:20:39 [multiproc_executor.py:987] WorkerProc hit an exception.
27697: (Worker_TP0 pid=8100) ERROR 09-22 05:20:39 [multiproc_executor.py:987] Traceback (most recent call last):
[...]
27985: **历史同族**：#17–20（packed layout与stride）、#70–73/D.4（逐相位性能与禁止全历史恢复）。
27986: 
27987: 源码仍在每个token执行页表DMA和KV DMA，current每行单独Cast。此次按虚拟128页边界合并history连续行搬运，current使用按head stride的2D DMA和整半tile Cast，复用原UB，保持数学、校验及精度阈值。未改GDN、图参数或原生排序。用户明确“ArgSort转AiCPU告警基线也有，跟你没关系”，所以不将其判作本项目新错误。
27988: 
27989: 日志workers=[]不能证明没有worker或已经卡死；新增debug标志及最后host事件显示，host提交不能当设备完成。CANN编译、67项官方CPU-debug及438项本地测试通过，目标优化后性能仍待实测。
[...]
28179: **结论**：每层组（3 GDN+1 FULL）设备成本随KV近似线性增长——16K约1.5s、32K约4.4s、49K约7.4s+，与chunk墙钟20/38/95s吻合；CV历史扫描是随KV增长的主项。背压块是设备队列的累积排空点，不是逐kernel归因；GDN与FULL attention的设备时间拆分host打点无法给出，需要设备级trace。
28180: 
28181: **下一步与边界**：用原生TorchNPUProfilerWrapper窗口（profiler=torch+torch_profiler_dir，/start_profile与/stop_profile夹住一个32K/50K请求）或独立ProfileSession采集，再用tools/summarize_profile --require-complete做逐kernel归因。300s死线、PROBE_LENGTHS、精度阈值均未动；host记录本身不证明任何设备时间结论。
28182: 
28183: ### 用户日志摘录（非完整文件）
[...]
28359: **关停日志判读**：`platform.py:1277` 的HCCL 1836秒/RPC 3000秒提示是INFO，且两边都出现。`STARTUP_WAIT` 位于图捕获期间，之后两边请求均完成。`tbe/common/repository_manager/utils/multiprocess_util.py` 的 `EOFError` 在主动`[shutdown]`之后、`CLEANUP_END`之前出现；原生与OSCAR均同形，随后的清理及NPU释放为passed。宿主resource_tracker的124 semaphore/6 shared_memory警告与#135同族，不是本次性能门失败的原因。终端compact过滤若把这些INFO/关停噪声误当启动错误，须修终端呈现而非改变模型数据路径。
28360: 
28361: **归因边界与下一步**：这轮证实长请求多并发有严重端到端退化；`PERF_TPOT`是SSE客户端时间，不是单个设备内核时间。#134/#135另一次debug-sync将当时主要相位时间归于自研CV attention（相位名`fia`），但不能把它当作这轮逐source设备计时。下一轮应在同一长请求形状下区分current/window/history的CV成本与GDN/调度间隙，冻结算子精度不变；不得靠加宽300秒请求死线或回退原生BF16历史制造通过。旧#139的16K阶梯已从当前脚本移除；当前快路径是一条命令原生→OSCAR配对。
28362: 
28363: ### 用户回传关键行（完整日志为本轮用户附件；此处非完整文件）
[...]
28415: ## [143] 真机条目（gpt_new_oscar_kimi，2026-09-24 用户回传）· K4降至43.3s，剩余3倍差距需设备分相位测量
28416: 
28417: **原文**：`reports/target_k4_43s_performance.txt`完整保留本轮附件。运行`paired-concurrency-20260924T003530.842905Z`，构建复用、真NPU CV/旋转门fresh通过，实际current/CV/merge门通过，current16K设备事件中位数6.59586ms。原生与OSCAR均4/4完成、无超时、资源释放passed；#142捕图前的启动故障不再阻止请求执行。性能门仍failed/rc2。
28418: 
28419: | 同一K4/20,23,27,30K/64输出 | 原生 | OSCAR | OSCAR/原生 |
[...]
28428: **判断**：相对#141约131.7s，OSCAR墙钟缩短约67%，相对#140的182.5s缩短约76%；已有收益应保留。接受长度变化只对应约6.7%的预估验证轮次差（假设每轮成本不变），不能单独解释近3倍墙钟差。peak Running=4、Waiting=2是采样峰值，不等于设备批处理效率相同。两类吞吐共享同一墙钟分母，不是两份独立瓶颈证据。原生EOF/EngineDeadError位于主动shutdown之后，最终请求与释放均passed，不是本轮性能门的失败原因。
28429: 
28430: **只读深查结论，非设备归因**：CV空源仍加载Q、归一化并逐行写partial/LSE；16K/GQA6/S1的三源约4917个leader，任务表49152行，非leader仍有metadata/status访问。短query的统一20个source split使4-token current有大量空split。写路径默认clip=0不执行Sort；每D256 K/V行仍有64次标量字节组装，另有小块slot/position DMA。Hadamard输入旋转仍需保留；每个history split末尾的稠密Rv约占25K/q4/S20的QK/PV+Rv MMAD次数9%，不能独自解释3倍差距。未依据这些静态计数修改已通过真NPU的计算内核。
28431: 
28432: **本轮处置**：一键快路径先跑原生与OSCAR原始K4，原始轮不创建NPU计时事件；若配对退化，在同一OSCAR服务上自动运行一次独立repeat1，输入及64输出不变，使用新的cache_salt。仅该轮用原生NPU Event时间戳与end.synchronize记录prepare/rotate/CV/current/merge/store/guard，按prefill、MTP draft和整图回放、TP rank及query/KV形状汇总。整图事件包在replay外，不给图内相位伪造耗时；dummy/capture不插事件。标记在模型入口读取，相位热路径不轮询文件。避开#133已造成四worker崩溃的HTTP profiler。同步诊断改变时序，不能替代正常轮速度比；缺rank/必要相位/整图回放明确needs_evidence。
[...]
28450: | N11504/R4/maxQ11492/maxSeq30000，CV16次 | p50 493.71ms，合计7895.12ms |
28451: 
28452: **先确认问题存在，再质疑收益**：已部署源码的query/head tile确为64，GQA6每组最多10个query；每组重复解包自己的完整历史区间。V每16行先Gather为[D,16]，再以D个64B小块写[D,128]；D256一个128KV单元产生2048个分散64B写块。INT2八个位平面互相独立，却各自Shift/barrier/And/barrier。这些开销确实位于已测的带历史CV热路径。相反，空历史候选仅约106ms、写入与旋转也不足以单独解释大差距，因此没有把空任务清零、写kernel或MTP接受率当作主要根因。
28453: 
28454: **本轮生产修改**：M128×KV256让21个GQA6 query复用历史；V自然布局[KV,D]直接连续写，PV用同一MatmulImpl的运行期B不转置。SDK的static B=true允许运行期true/false，原生chunk GDN同一mm1已有两种用法。八次Shift合并到一道barrier前，八次And合并到另一道前。每AIV保留64行FP32累积状态在UB，以32行块算softmax，复用失活dequant空间读PV；拒绝了M256把累积状态反复写GM的方案。query任务、slot组缓存、workspace与测试同步使用共享常量。
[...]
28458: **直接收益门**：一键快路径在重编前，若旧产物与本项目5288b2e的csrc指纹、构建签名、CANN/SOC/包版本及二进制SHA全部匹配，先用隔离子进程测旧CV；新构建通过数值门后再用相同输入测新CV。主场景为合成的4请求长prefill；另有32条独立随机历史、互不共享物理页的q4 decode，防止只看prefill改善而漏掉decode退化。两侧均预热2次、测5次中位数，比较输入hash并检查冻结输出/LSE。旧产物不存在则明确not_comparable；有对照且候选更慢则停止模型启动。算子A/B通过仍不等于原生速度达标，随后继续正常native/OSCAR K4门。
28459: 
28460: **本机证据**：最终生产内核SHA `6565a8dfc9c7dcb47de4798ea5f4a3167d277a84cac636ebca8165382d5b2af8`，CANN910B4编译通过；官方CPU-debug33/33，含Q21/Q22/Q43边界与3个NaN workspace病例；相关主机回归通过。`reports/history_cv_local_validation.json`分别记录生产编译源与后加CPU-only poison harness指纹，未伪称两者完整源码快照相同。新NPU精度、图回放、算子净收益与端到端追平尚待一键实测；未运行用户的127条数据集。
28461: 
28462: ## [145] 真机条目（gpt_new_oscar_kimi，2026-09-24 用户回传）· M128 的第二个 softmax 块覆盖未完成写回的 score 缓冲
[...]
28486: **本机复验结果**：同一最终kernel SHA `febd753f3bc1bb67639e3ab24cf7f4742608eaada3e835e52d04b92b235c0ec4` 通过CANN ascend910b4编译；官方CPU-debug 38/38通过（含新增3个poison边界），相关主机24 passed/28 NPU skipped。证据`reports/cv_score_handoff_validation.json`和`reports/cv_score_handoff_cpu_debug.json`。修订后的目标NPU/图/性能尚未执行，不把这些本机结果写成真机已修好。
28487: 
28488: ## [148] 真机条目（gpt_new_oscar_kimi，2026-09-27 用户回传）· 局部加速未追平且模型精度下降，回到 fe0 后独立验证历史复用
28489: 
28490: **编号说明**：用户要求回退到fe0后，本工作树恢复到#145；#146/#147位于被回退的本项目提交历史，不复用其编号。本条保留用户新提供的真实LongBenchv2退化，后面的本地实验明确单列，不写成目标机结果。
28491: 
28492: **原始证据与用户裁决**：完整材料存于`reports/target_longbench_regression.txt`。用户提供fe0e925的自有127请求结果为22:22、accuracy53.54%，34639ab为20:15、accuracy48.03%，两轮均127/127、FAIL=0。用户明确确认fe0精度OK，并要求撤销后续修改；本轮开始前已将开发分支和稳定分支恢复到fe0。HTTP完成和独立算子数值门通过不能抵销模型结果退化。尚无逐请求输出/logits，不能从7题净差直接确定是哪一道数学改动造成；因此不捏造数值根因，也不保留被撤销的改法。
28493: 
28494: **性能证据边界**：34639ab材料中的CV局部中位数183.133→161.942ms、decode14.240→11.937ms，K4原生14.7s/OSCAR26.2s，与用户完整负载8分钟/22:22的计时范围不同。不得用这些局部百分比相加、换算862秒归因，也不得把不同核心的原始tick最大值相加成wall。完整负载追平约480s需要从1342s消掉约862s、64.2%；只消除metadata/行检查等局部工作没有证明能达到此预算。
[...]
28496: **当前fe0中已确认的结构性重复**：M128/GQA6每组21个query，组间独立重扫相同历史。256KV/D256单元读取34816B packed K/V及元数据，再发布524288B FP32 K/V给Cube；相邻组重复同样的INT2展开与GM通信。分块使峰值workspace有界，却没有消除累计重复工作。这里是源码字节账，不是实测HBM流量。该路径与#144带历史prefill CV热点一致；仍需要用户相同负载的阶段计时确定其端到端占比，不能断言它解释全部差距。
28497: 
28498: **新实验与D.4四问**：①属于历史INT2恢复与CV；②D.4失败方案仅全历史dequant已6499.8–6655.1ms/卡，高于原生整段prefill，故必须减少重复恢复而非继续修边角；③独立C4算子仅让同request/head/split/context/kvbegin/kvend、kvend=context的四个完整query组共用一次有界KV256解包，其余任务仍原OSCAR INT2计算；四组各自保存FP32累积，原QK/PV/softmax/旋转/有限性检查和KV顺序不变。尤其不把不同域union后mask，因为fe0在mask前检查有限性。原生产kernel逐字节保持fe0，候选只通过显式选项启用；④合格簇展开次数最多4→1，QK/PV算量不变且增加FP32状态通信、调度扫描；新workspace每Cube D256为1839104B，旧917504B。以上不足以宣称净提速，必须逐位与设备速度门判决。
28499: 
28500: **验收入口**：`git pull --ff-only && bash scripts/install_observe_serve.sh --variant candidate`安装/编译、原有NPU原语/CV/旋转/current门、候选fe0同输入逐位/冻结oracle/图回放/速度门和资源清理后才启动服务。候选门失败即打印错误并保留真实rc，不切换其他路径。baseline保留fe0，native禁用OSCAR数学路径；无自动推理POST，无私有数据集生成，无自动重跑127题。被动采样按rank/step/stream求事件区间并集，覆盖target/MTP/attention/整图，未完成Event不强制同步，图内和跨stream不明细项写missing。该稀疏采样仍可能有扰动，不能替代最终无观测速度验收。
28501: 
28502: **本地证据，非新真机结论**：CANN ascend910b4编译通过，官方CPU-debug51/51通过，含C4实际参与的逐字节partial/LSE/status、独立oracle、非法共享metadata和单组QR NaN。同一D256/Hkv2/q168/context641的2/20核心CPU模拟器配置分别达到120s；保留超时，以D64长多tile、D128双head与D256大维度的互补病例验证，未提高时限。证据`reports/history_reuse_cpu_validation.json`。新候选的真NPU逐位、图、模型质量和追平8分钟均待用户执行；用户已认可的fe0精度保持有效。
28503: 
28504: ## [149] 真机条目（gpt_new_oscar_kimi，2026-09-28 用户回传）· 候选统计逐核恒等式越过内核两阶段归属，首次真NPU候选门在计数契约处关闭
[...]
28508: **定位**：失败的逐核条件是 `row[6]==row[1]`（original_schedule_skips==grouped_leaders）。C4内核两遍调度的计数归属不同：第一遍按CvTaskSchedule的workId条带，把被推迟成员记到其query tile所属核——一簇4个成员在连续4个tile上、最多落到4个不同核；第二遍按#129改造后的84-token bucket重映射，把4个grouped_leaders记到受理该bucket的单个核。逐核相等一般不成立，恒等式只在全局和成立。以首个病例mature_20k（4096 token、queryTile=21、bucket=84、20 Cube）核算：core0第二遍受理簇k∈{0,20,40}→row[1]=12；第一遍仅k≡0(mod 5)的成员tile 4k落在core0→row[6]=10，确定性报"owner 0 inconsistent"，与观测逐字一致。
28509: 
28510: **为何此前未见**：该相位为f5fd2b3新增，本轮是候选首次真NPU执行（#148已记"真NPU逐位/图均待用户执行"）。官方CPU-debug（`csrc/cpu/cv_probe.cpp`）只核对跨核求和后的恒等式，口径本就正确；D256的2/20核CPU模拟配置在#148保留120s超时，多核计数分布从未完整执行；主机单测只喂逐核自洽合成行。bitwise partial/LSE/status与冻结oracle等真实精度门位于计数检查之前且已通过——本失败是宿主侧契约过严，不是C4内核数值错误，也不是设备残留。
28511: 
28512: **修法与边界**：`_check_cluster_stats`逐核循环只保留同点累加恒等式（grouped==4*clusters、avoided==3*shared_tiles、anchors==clusters），skips==grouped保留在全局和校验，与CPU-debug totals oracle口径一致；新增两阶段归属回归测试。未改任何CANN算子及fe0/C4数值路径，无须重编译。真NPU复验（全部病例、图回放、速度门及服务）仍待用户重跑同一命令，本条不宣称候选已合格。
[...]
28518: **当前代码核实**：服务仅按workspace候选开关选C4，不检查单请求query上界。C4要求4个完整query组，Hq6/Hkv1时至少单请求84个query；decode32每请求4个，总计128个不能跨请求组簇，但仍执行候选成员判断、第二遍任务扫描和计数发布。因此存在无收益的额外工作。不过一次41.84微秒差值不足以证明这些工作的真实时长，不能排除测量波动，更不能用来解释约14分钟差距。用户亦明确指出本项与整体目标关系很小。
28519: 
28520: **修法**：共享host形状选择函数用于服务和probe。已知max_query_len或总token不足四组时，直接调用既有fe0 OSCAR INT2核；候选工作区足够容纳原核，其余输入和ABI不变，无NPU回读或新增图节点。未知上界保守保留C4。probe原始C4数值/图病例全部保留；速度轮验证实际生产分流的逐位结果，短query两侧为相同fe0算子，时间和比值原样记录作重复性对照，标`identical_fe0_operator`而非伪造ratio=1或快于基线。被实际选中的C4继续原ratio≤1.0门，精度阈值未改。此项只是移除无收益路径并解除采证阻断，真正目标仍是实际负载端到端占比和约8分钟性能。
28521: 
28522: **本地验证边界**：57项相关主机测试通过，覆盖32×q4与图padding、83/84边界、GQA变化、未知上界、真实forward ABI和长query仍选C4。未修改任何AscendC算子，无新CANN编译必要；修订后的真机分流、服务和用户负载待同一一键命令复验。用户已有fe0精度结论保持有效。
28523: 
28524: ### #150 后续真机回传：门通过并运行实际负载，MTP q1 调度偏载有了同一步证据
[...]
28534: ### #150 q1修订真机复验通过（a13af95）
28535: 
28536: 用户在node93执行同一`--variant candidate --probe-only`，run=`observe-20260928T031553.257802Z`，签名`9357b546136a`；原文`reports/target_q1_schedule_pass_20260928.txt`。N128/S3 q1：45.112041→13.807460ms、ratio0.306070、逐位精度及独立图capture/replay passed；N16384/S1 q1：137.882706→20.543880ms、ratio0.148995、逐位精度passed，该形状图not_run。C4 9例逐位/6例oracle/图继续通过，成熟20K 76.349716→55.855301ms。q4同fe0 S3自比15.278180/15.301980ms，标identical_fe0_operator；不是新退化。`candidate_evaluation_allowed=true`、q1五门passed、最后`OBSERVE_PROBE_DONE service_started=false`确认短probe正常结束。这是设备验证成功，续记原问题，不另追加错误编号。
28537: 
28538: 此结果支持保留q1调度改动，但不是完整服务或AISBench新时长。下一项针对仍约15ms的q4 CV，与原生实际paged BF16 FIA做同逻辑输入的独立oracle/正常Event对照；独立profile原始时钟仅供找阶段瓶颈。不能恢复已否定的“把不同核ticks最大值相加为wall”口径，不改已有fe0/C4/q1数学，不再要求AISBench。
[...]
28560: ### #151 fast unpack真机复验通过与固定启动入口约定
28561: 
28562: 0677bcb、`observe-20260928T064725.021030Z`全部fast precision/graph/performance门passed，failed_cases为空，正常短probe结束；原文`reports/target_fast_unpack_pass_20260928.txt`。q4 N128/S3 15.297940→11.281520ms；q1 N128/S3 13.854560→9.842060ms；q1 N16384/S1 20.468300→15.765760ms；C4 mature20K 55.009899→48.772461ms；mixed q1/q4/long 19.301439→15.852880ms。五例逐位通过，q4/q1指定独立图passed，其余行graph not_run。记录实测，不另立错误编号，也不外推完整模型总时长。
28563: 
28564: 用户明确要求每轮均同步到`git pull --ff-only && bash scripts/install_serve.sh --variant candidate`。当前该路径已启用C4/q1/fast；本轮统一候选预设供直启与probe共同调用，补计划/子进程/实际路由回归并写入AGENTS。默认配置与后四卡模式保持各自既有行为；直启不因该约定变成自动跑测试或AISBench。
[...]
28573: **同输入短NPU事实**：`observe-20260929T020143.804953Z`算子/图门正常完成。31q4 N128/S3 CV11.328500ms、总11.395780ms；同cohort N16384/S1 CV34.971642ms、总36.737999ms；cold mixed CV35.655781ms、current6.973760ms、总46.415298ms；13740旧历史+16260新token mixed CV125.104156ms、current7.015120ms、总137.670563ms，oracle全部passed。N/S同时变化，不能将3.087倍全部归给某一变量；短形状不是55分钟各相位占比。原fast/C4/q1门继续通过。
28574: 
28575: **源码核对与本轮候选**：querytile21按token桶分配使N16384/S1的31q4历史leader集中6核；独立balanced核用4token遍历仍逐task唯一、数学querytile不改。长prefill C4仍为每四个同域query组重新展开相同KV，新增独立C16保留原FP32数学顺序/错误域，max_query_len≥8192才选择；每卡额外有界scratch约63MB，在KV预算前共享分配。新kernel与独立真实NPU AB门均接candidate，旧fe0/fast/C4/q1文件保持原样。CANN、CPU-debug和主机测试另记，不冒充本条真机验收；新NPU精度/图/性能仍待该短门裁决。方案与反证条件见`docs/mixed_cv_optimization.md`。
28576: 
28577: **本地验证后续（非新增真机验收）**：CANN编译通过；135项主机关键回归通过。CPU-debug原大D256/非对齐combined例各120s超时已定位并修复为有完整参考字节绑定的分段对拍；原例、数值和单次120s限时均未改变，最终9例完整通过。D256两段57.280/77.735s、非对齐62.565/78.836s，原超时记录仍保留。全部证据`reports/mixed_cv_local_validation.json`；真NPU与端到端速度待新短门，不能标通过。
[...]
28585: **修法**：向 `torch_bindings.cpp` 能力表与 `meta.py` 可选表补登两个算子名；新增主机源码对拍回归，要求C++能力表、CMake清单模板与 `SOURCE_CAPABILITIES` 集合恒等，meta可选表恒等于 SOURCE−PRODUCTION，今后任何一处漏登在推送前即失败。未修改任何CANN算子数学/ABI/布局，不适用D.4四问；绑定编译单元变更后真机必须重新编译，加载器源码指纹本来也会拒绝旧产物。
28586: 
28587: **本地验证边界**：676项主机测试通过（含两项新对拍回归），140项按设计跳过（真NPU门opt-in）。本机CPU结果不冒充真机证据；真机仍需用户以同一一键命令复验 operator-cv-npu 及后续mixed短门，通过前新balanced/C16算子的精度、图与性能保持未验收。
28588: 
28589: 
28590: ## [154] 真机条目（2026-09-30）· batched4 通过 CPU 模拟但真 NPU 独立 oracle 失败，端到端仍约16分钟
28591: 
28592: **原文**：`reports/target_batched_history_failure_20260930.txt`；`observe-20260930T002546.268708Z`，用户运行最新candidate。旧history/q1/fast/mixed各门继续通过，batched-history首例在 `_run_case` → `mixed._oracle` 失败：876/32256（2.7%）元素超冻结0.005门，最大绝对误差0.0895615；子进程rc2，正式服务未启动。用户另用直启测得LongBenchv2仍约16分钟。直启没有精度门，该耗时不能作为B4精度合格的证据。
28593: 
28594: **已确认与未确认**：12af4f7已把B4开关接入两个入口；B4只覆盖主模型满足条件的历史prefill，稳态decode和MTP均不走它。真实设备数值失败已否定该版本的交付资格；CPU逐位与CANN编译不构成NPU通过。现有日志不足以把最大误差唯一归因为某条硬件同步或Matmul指令，不能伪写根因已定位。
28595: 
28596: **处置**：完整撤销12af4f7，恢复9bd3345的已回传算子路径与候选预设，不放宽冻结精度门。后续优化须覆盖实际长历史prefill与q4/q1，并单列数学/布局证明、CPU、CANN、设备与模型性能证据。
28597: 
28598: **本轮源码进一步审查（候选根因，非真机复验）**：12af4f7 的 `ApplyDeferredAlpha` 在 MTE2 读入共享 `tmp` 后执行 Brcb/Mul，结尾只有 `PipeBarrier<PIPE_V>`；下一 rowBase 又由 MTE2 覆写同一 `tmp`，缺少 V→MTE2 的跨管道所有权屏障。SDK 语义与 #145 同族，CPU 顺序模拟不能覆盖这一竞态。它是可定位的同步缺口，但尚无设备首错时序证明这是本条全部失配的唯一原因；B4保持撤销，不把补一个屏障写成性能达标。
[...]
28607: **修法**：store窗口与store图/eager专用比较对BF16/FP16按int16、FP32按int32视图比较，整数按整数比较；NaN payload、正负零及所有有效字节都保持严格，不使用equal_nan或放宽容差。新增NaN payload不同必须失败、signed-zero不同必须失败与原fixture精确clone通过回归。旧/新store的window写入控制流相同，首错本身不能证明device race；修正后新真NPU writer/reader/图/性能仍待验。AscendC和GDN均未因此修改。
28608: 
28609: **性能解释修正**：上一轮4K/8K、单请求S1 CV模拟1.98/2.10倍只能证明该算子路径的周期收益；实测16→14为1.143倍。新probe在writer比较处提前失败，所以本条没有striped真NPU算子比值。必须从全程日志建立prefill混合/纯decode/爬坡及排空分布，校准原生480秒与候选840秒，并固定校准参数后评价源码变更；不能把混合区间时长称为attention占比或用两个锚点唯一推定各相位时间。
28610: 
28611: ## [156] 真机条目（2026-10-09 用户回传）· 65100输入/512输出/K32/120请求的容量与性能差距
28612: 
28613: **原文证据**：`reports/target_64k_120_20261009.txt`，263011字节，SHA256 `03eb53109a97a3e82b02c91550b5661dc8cf0c3360585693f567a3217c7311bb`。用户同时提供OSCAR/原生服务端日志及客户端完整指标表；未提供启动SHA、实际KV pool字节或设备逐相位trace。用户要求以后不再研究LongBenchv2性能，本轮仅处理本64K负载；模型质量与算子精度门保持冻结。
28614: 
28615: **已测现象**：两侧均120/120成功，总输入7812000、输出61440；OSCAR/原生墙钟2467.1275737/1342.4437259秒，平均TTFT208.9315/230.3687秒，平均E2E649.3244/335.9201秒，平均TPOT861.8/206.6毫秒，P99 ITL13.4451/2.8731秒。服务端Running采样峰值实际27/12（26是用户粗估）；OSCAR首token后的平均时间约为原生4.172倍。完整已打印Spec窗口（含暖机、缺失不补）接受率63.7857%/92.9660%，不能将其直接当引擎step数或模型质量结论。
[...]
28627: **归因确认（与 #142 同一 Trap）**：`status_guard.cpp` 自 f8735233（2026-09-22）起未变，#142 已把同一 0x264 偏移映射到该内核的 Trap()；本工程只有该内核含 Trap()。所以本次是 fail-closed guard 检测到某族 status 非零，按设计中止；生产 Trap 不带段信息，日志本身无法指出是哪一族。
28628: 
28629: **已排除（源码+日志证据）**：①命中率先 0.0% ⇒ 无任何跨请求共享页读取，APC 共享内容路径（错误3/4）不在场；②崩溃窗口 generation≈0 ⇒ 纯 chunked prefill，MDL 未在长历史形状上运行（其单次 matmul 形状与历史长度无关，且短请求 decode 已多次执行）；③`rotate_vector_init` 与已 64K 真机验证的 `rotate_out` 全 diff 仅向量化 Hadamard Init 一处，该 builder 已被 striped writer 的 64K 真机负载共享证明；④生产内核与插件无 2816 旧几何残留，align 几何（页2304/虚拟128×18）全部参数化；⑤原生 slot/padding（-1 填充、qstart 镜像）不变量核实成立。四 rank 同步同址 trap ⇒ 秩对称条件：主机元数据或经 TP 集合通信扩散的数据。
28630: 
28631: **修法（保持两个新算子默认开启，不动 fe0 冻结集）**：`status_guard.cpp` 属 fe0 字节冻结集合（`tools/observe_serve.py::FE0_KERNEL_SHA256`，自 #148 起无更新先例），不改。新增 `oscar_ascend/integration/guard_diag.py`：默认路径仍是原来的单次融合 trap 启动、零改动；`OSCAR_GUARD_HOST_SYNC=1` 时把同一冻结内核按族（attention/rotate/merge/store 及各调用点族名单）逐个启动并逐族 `torch.npu.synchronize()`，trap 即从具体族的调用行抛出，异常链含 `site=`/`family=`。图捕获路径保持融合启动（capture 期间禁止 host 同步），dummy/capture 语义不变。全部 7 个 `status_guard` 调用点（impl 主站、current_only×3、current_slots、mixed_decode×2、compact_later_mtp、request_window store）改经 `run_status_guard`。

## gpt_new_oscar_kimi/oscar_ascend_agent_start.md
[...]
3: > **2026-10-15 当前要求覆盖下方旧目标/启动设置**：以用户确认可用的 stable `f96820f1` 为主分支优化基底；APC 默认关闭且保留显式开关、token budget 16384、原生调度器及全部 vLLM argv 冻结。32K/64K、各300请求/512输出，均须比同参原生提升超过30%；本轮不连接真机，由用户最后验证。完整原始指标、来源和范围见 [`reports/stable_32k_64k_20261015/analysis.md`](reports/stable_32k_64k_20261015/analysis.md)，主机冻结回归使用独立保存的 stable argv。下方旧省略预算、默认开启APC及2–4倍目标保留为历史，不适用于本轮。
4: 
5: > **2026-10-12 单项与组合新门槛**：单项完整相关路径在当前优化基底上至少1.15倍（速度提升15%），精度和必要协议通过后即可进入组合；不要求每个点独立达到1.5倍或2倍。最终组合相对原生目标2–4倍，越快越好。保持默认prefix caching开启、原生预算和冻结精度；总MD统一裁决，不拼乘或向上取整局部倍率。
6: 
7: > **2026-10-12 新增兼容要求**：所有服务启动入口默认显式开启 prefix caching，固定 candidate 命令无需额外参数；prefix caching 必须在 OSCAR 上正确工作，覆盖共享压缩页、精确窗口、分叉写、释放复用、原生 GDN 与 MTP 命中边界；不能以关闭该功能解决。按[总 MD](skills/oscar-quant-optimization/SKILL.md)的 prefix caching 节与专项实现闭环执行。用户未提供错误栈，源码发现不得冒充该次真机错误根因。
[...]
9: > **2026-10-11 用户第一指示**：OSCAR已增加可驻留batch，却没有获得吞吐收益、反而更慢；必须定位并消除当前OSCAR执行路径中抵消容量优势的主要成本。按[总MD第一节](skills/oscar-quant-optimization/SKILL.md)组织全部后续工作，以实际batch、有效输出/步和包含MTP的step时间闭合因果，优先核反量化后的浮点展开、分层搬运、计算及同步；不再以局部微优化或容量比替代核心问题的解决。
10: 
11: > **2026-10-11 优化执行 SOP**：本工程量化/反量化性能迭代使用 [`skills/oscar-quant-optimization/SKILL.md`](skills/oscar-quant-optimization/SKILL.md)，以当前源码核实、增量净收益、冻结精度、组合去重、两个一键入口实际启用和真机反馈形成闭环。成功、失败、暂缓与未完成方向统一索引于 [`docs/optimization_ledger.md`](docs/optimization_ledger.md)；过小增量保留证据与重开条件，不装入本次组合。skill 不替代下方档案及 D.4 阅读要求，也不把局部模拟结果视为整轮达标。
12: 
13: > **2026-10-11 用户补充的提速机制**：明确采用组合优化。64K下以INT2降低实际KV访存和容量占用，让OSCAR容纳更大的实际decode批次；按原生访存受限的前提，要求组合仍由访存主导，量化/反量化及MTP不能成为新的计算瓶颈。按实际batch、每步有效输出和step时间核算decode吞吐倍率，再计混合prefill、爬坡/排空对整轮的影响。详见[`docs/quant_dequant_roofline_20261011.md`](docs/quant_dequant_roofline_20261011.md)；这是设计目标与有条件机制，不能只用KV压缩比或Running峰值宣布实现。
[...]
17: > **2026-10-09 用户最新启动约束**：所有服务入口省略 `--max-num-batched-tokens`，使用 vLLM Ascend 自己解析的默认值，不硬编码2048，也不通过OSCAR调度器或其他配置抬高预算。此前whole32K/whole64K方案退出服务入口；两个固定candidate命令不需要新参数。下方附录A的16384参数保留为历史证据，不再是当前启动设置。工作区必须读取实际引擎容量，原生GDN计算不变。
18: 
19: > v2 变更（2026-09-19）：第 0 节重写为「档案驱动开发、无回退铁律与一遍过工程要求」（新增 0.4 全阶段档案强制引用制 / 0.5 无回退判例 / 0.6 一遍过 10 条工程根因 / **0.7 算子开发两原则：精度第一 + 反复对照附录 D.4 打点日志**，并在 §6.3 强制每个内核交付 D.4 对照段）；新增 **5.0 设计方案总要求**（全局端到端架构先行：生命周期图/联动矩阵/时间线/两本账 → 逐点展开固定六问 → 四条验收性质[PR 语义 100% 兼容且精度准 / 与 vllm-ascend 100% 兼容 / 全链路无等待慢点 / 无回退] → 设计自审清单）；新增附录 E（kimi_oscar 首轮 13 轮真机故障速查）与附录 F（真机环境与版本声明）。调试档案 issue1_full_record.md 已扩至 120 条（新增第三部分 [74]~[86]，即本项目首轮真机记录）。v2.1（2026-09-19）：新增「阅读与执行路线」；修正过时引用（107→120、CV=Cube/Vector 核实注释）；各节补本项目已核实结论指针（§3.2/§4/§7/§8.2/§9-A07）。
20: 
21: > 目标模型：`Qwen3.5-27B-w8a8-mtp`。目标环境：Ascend NPU、4 卡、TP=4。实现方式：外部适配插件 + 独立 AscendC 算子包。
[...]
34: > **三条最高优先级铁律（细则见第 0 节，先于一切任务执行）**：
35: > ① **任务一开始，先把当前工作区下的 `issue1_full_record.md` 完整读一遍，建立整体印象**——那是 OSCAR 与真机交互的完整调试档案（现 120 条：前 107 条为上一版失败实现全过程，第三部分 [74]~[86] 为本项目首轮 13 轮迭代，覆盖编译、环境、数值、集成到性能定位全过程）；之后在任务中遇到任何不会的、不确定的、拿不准的、或真机报出的错误，必须再回该档案按报错关键字查表定位。真机交互记录是比推测可靠的一手资料；
36: > ② 严禁参考、阅读、复制任何失败 OSCAR 实现的代码（防污染红线）。允许使用的失败遗产只有两类：上述档案中的报错日志（用于避坑），以及附录 D 的性能对照数据（用于校准目标）。
37: > ③ **牢记上一版失败根因（附录 D.3）**：32K 标准输入下，失败 OSCAR 单个 prefill 步仅 dequant 一个算子就花 6.5s/卡（wall 6.8~7.0s），比原生整段 prefill（4.6s @ 6869.5 tok/s）还慢；attention 本身不慢（FIA 32K 步仅 ~18.7ms），瓶颈 100% 在"全历史 dequant 恢复后再做 attention"的反量化路径。因此本次实现：**不准有任何回退逻辑；必须完整实现原生 OSCAR 语义；各种序列长度、各种 batch size 都必须兼容；任何算子/相位的耗时绝对不允许差于同拉起方式的原生基线**。
38: >
[...]
60: 
61: - 上一版 OSCAR 实现已经失败（最终因 dequant 路径性能崩盘未通过验收，实测数据见附录 D）。**严禁访问、阅读、复制或改写该失败实现的任何代码**——它会污染设计判断。本地任何失败的相关代码仓同理（与 H03 互为补充）。
62: - 允许使用的"失败遗产"只有两类，且都已整理在当前工作区内：① `issue1_full_record.md` 中的**报错日志**（用于避坑，不用于抄实现）；② **附录 D** 的**性能对照数据**（用于校准性能目标）。
63: - 判断基准：看报错日志是为了"不再犯同一个错、快速定位同类报错"，不是为了"沿用它的做法"。凡涉及实现选型的决定（缓存布局、算子划分、反量化路径、集成方式），一律以指定 PR reference、原生 vLLM Ascend 源码和第 5/6 节的设计要求为准。
64: 
[...]
69: - **原生基线**：31,897 tokens 整段 prefill **4.6s**（6869.5 tok/s）。
70: - **上一版失败 OSCAR**：单个 prefill 步仅 **dequant 一个算子就花 6.5s/卡**（占该步 wall 6.8~7.0s 的 95.4%）——**单步单算子比原生整段 prefill 还慢**。
71: - **attention 本身不慢**：FIA 在 32K 步仅 ~18.7ms、16K 步仅 ~7ms。瓶颈 100% 在反量化路径——上一版把历史 INT2 全量 dequant 恢复后再做 attention，正中 H09 禁止项（每步全历史 `full_dequant + inverse rotation`）。
72: 
73: 由此得出本次实现的**三条不可退让的性能红线**（与 H17/H18 互为约束，验收见第 9/10 节）：
[...]
101: | --- | --- | --- |
102: | 1. 路径选择 | 不支持的场景抛 `OscarError` 并中止 | 静默走原生 BF16 路径、按序列长度/batch/相位跳过 OSCAR、"暂不支持"降级 |
103: | 2. 缺失输入 | 缺旋转 checkpoint 时显式要求 `--identity-rotation-ok` 才可用 identity 并全程醒目 WARN | 缺输入时静默使用 identity/默认值继续跑 |
104: | 3. 异常处理 | 异常向上抛、带上下文中止；可重试的瞬时错误**有限次**重试并记录每次失败 | `except: pass`、捕获后打印"跳过注入/降级运行"、无限重试直到"碰巧过" |
105: | 4. 检查与验收 | 质量闸（数值/性能/显存）不合格即 FAIL 并定位 | 环境**基线事实**（版本、源码树组成、能力探测结果）可"记录制"落盘不阻塞——这是观测不是回退；但**质量闸**（probe 数值、32K 门、MTP 对照、显存收益）绝不合格判 FAIL |
106: | 5. 精度/容差 | 门槛在调优前冻结（写进 `configs/acceptance.json`） | 事后按实测结果放宽容差/门槛、用平均值掩盖单项失败 |
107: | 6. 超时与挂起 | 有界超时 + fail-fast + 各 rank 进展可见 | 加大超时掩盖挂起、kill 重来直到"碰巧过" |
108: | 7. 测试断言 | 断言从 PR/原生证据/档案条目推导 | 把断言改成"和实现一致"（拿实现当参照）、删掉失败的用例 |
[...]
123: 7. **fork 前父进程建 torch 池**：vLLM 只在 OMP_NUM_THREADS 未设置时才在父进程 `torch.set_num_threads(1)`；若环境预 pin 了 OMP，必须在创建 LLM/EngineCore 前显式 `torch.set_num_threads(pin值)`，否则 worker fork 后 `Invalid thread pool!`。（[84]）
124: 8. **build 目录配置漂移即清**：构建状态签名（源码指纹+CANN+参数+SOC）变化 → 清空 build 目录重 configure；构建失败 → 自动干净重试一次再报错。（[85]）
125: 9. **校准层数口径**：校准引擎（无 speculative_config）只有 16 个 FULL 层；MTP draft 层 `max_tokens=1` 校准时从不触发、协方差必为空矩阵——校准 16 模型层，draft 层按 PR 语义 identity 回退并醒目 WARN。（[86]）
126: 10. **一切"待核实"显式列出**：任何未在真机复核的假设（布局不变量、版本差异、API 先例）必须写进 `docs/checklist.md` 并配真机复核脚本，禁止"先假定对了再说"。
127: 
128: ### 0.7 【铁律】算子开发两原则：精度第一 + 反复对照附录 D.4 打点日志（快且准）
129: 
130: > 本条与 0.3 性能红线互为表里，针对**每一个 AscendC 算子的设计与编写**（含所有子代理）。前人已经在真机上把"慢算子"和"不准算子"的坑全部踩过一遍——**不反复对照 D.4 原始打点日志就写算子，等于蒙着眼重走失败路。**
131: 
132: #### 0.7.1 第一原则：精度必须准确，且先于一切性能诉求
133: 
134: 1. **语义逐位对齐 PR**：INT2 编码映射、4-per-byte LSB-first 位序、fp16 先舍入的 scale/zero、量化公式 `q=clamp(int((x-zero)/scale+0.5),0,3)`、per-(token,head) 单向量单组粒度、旋转正交等价链（Q 侧 `q@R_k`、输出侧 `@R_v^T`）——任何一条与 PR 不一致，该算子即判失败，**不存在"差不多就行"**。
135: 2. **验收门槛冻结在前**：pack/unpack 位级精确；store↔dequant atol/rtol=2e-3；fused attention vs 参考 5e-3；prefill/window relL2<2e-2；staging 全驱逐一致 1e-4（均出自 PR 测试，见 `configs/acceptance.json`）。**数值门槛不过，禁止进入任何性能比较**；事后放宽容差即判失败（0.5-判例 5）。
136: 3. **参考实现对拍先行**：每个算子先写纯 torch 参考实现（`ops/reference.py` 语义镜像），算子与参考对拍通过后，才允许谈性能；数值诊断必须区分**系统性恒定偏置**（scale/meta 布局错）与随机误差（档案 #13~#16 的 bias_mean/spread 方法）。
137: 4. **性能绝不用语义换**：禁止以降低累加精度、跳过窗口段、改近似量化器、省掉边界处理等方式换速度；快而错的算子 = 失败，慢而准的算子才有优化资格。
138: 
139: #### 0.7.2 第二原则：设计/编写每一个 AscendC 算子，必须反复对照附录 D.4 原始打点
[...]
170: 以下指令是对**主代理及其派生的每一个子代理**的同等约束，主代理在派发任何算子相关任务时必须**逐字**包含它：
171: 
172: > 「写的算子的时候第一精度一定要准确，第二你和包括你的subagent在设计和编写每一个ascendc算子的时候一定要反复去reference "D.4 失败 OSCAR 32K 算子打点原始日志（完整保留）"，前人已经给你踩过坑了，要去避免这种慢的算子，想办法设计出来速度快，然后精准的还原原生oscar逻辑的算子。」
173: 
174: 子代理据此必须做到（缺一即退回重做）：
175: 
176: 1. **先读档案再动手**（0.4-2）：先读 `issue1_full_record.md` 症状速查表与其子系统全部相关条目；写算子前**必须重读附录 D.4 原始打点日志全文**（逐行 JSON，不是只看 D.2/D.3 的结论数字——要看到前人每个相位真实的时间戳形态：dequant 6499.8~6655.1ms 是怎么吃掉 95.4% 的、phase1_stores ~209~215ms 是怎么堆出来的、fia 为什么只有 7~18.7ms）。
177: 2. **精度第一**：任何实现先逐位对齐 PR 语义并通过纯 torch 参考对拍（冻结容差，禁止事后放宽），再谈性能；禁止以降低累加精度、跳过窗口段、改近似量化器、省边界处理换速度。
178: 3. **D.4 四问交付**：每个 kernel 头注释与 `docs/design.md` 对应小节必须含「D.4 对照段」——对应哪个相位、前人在该相位怎么死、本实现凭什么结构性不死、预期量级 vs D.4/原生基线。
179: 4. **禁止慢算子结构**：任何随历史长度线性增长的全量恢复/搬运（全历史 dequant、物化 BF16 历史、逐行 inline dequant）、写路径小算子拼接、host 热路径逐请求循环/`.item()`，在设计评审时即否决，不得进入实现。
[...]
194: 7. **可审计**：每个完成的 Checkpoint 都有代码位置、相关代码片段、解释和适用的测试或性能证据。没有执行的验证必须明确标记为未运行。
195: 
196: **不得将以下状态报告为完成**：仅完成设计；仅 Python reference 正确；仅编译成功；仅 HTTP 返回 200；仅短序列可运行；未进入 OSCAR 路径；MTP 被关闭；长序列回退；**存在任何回退/降级逻辑**（静默回退原生路径、特定序列长度或 batch size 下跳过 OSCAR、以显式报错之外的方式降级）；显存收益未落地；性能或精度未验收；**任何算子/相位耗时差于附录 D.1 原生基线**。
197: 
198: ## 2. 执行边界与要求优先级
[...]
204: | H01 | 不修改、覆盖或替换真机 vLLM Ascend 原始源码文件；适配代码放在独立工程。不要通过修改原生 vLLM 文件绕过此限制。 |
205: | H02 | 保留用户原限制：**“不准任何 cp”**。交付脚本不得使用 `cp` 命令，也不得用其他复制、写入或替换手段覆盖原生代码以实现适配。插件和算子通过独立工程的安装、构建和加载机制集成。 |
206: | H03 | **严禁参考、阅读、复制本地任何失败的 OSCAR 实现及其相关代码仓**（防污染红线，详见第 0.2 节）。失败遗产中允许使用的只有：当前工作区 `issue1_full_record.md` 的报错日志（避坑用）与附录 D 的性能数据（校准目标用）。 |
207: | H04 | 新增的量化、反量化、旋转、逆旋转、裁剪、移位、打包、解包及相关 KV 数据搬运均在 NPU 上执行，核心数据路径用 AscendC 实现。 |
208: | H05 | 不通过 `.cpu()`、`.to("cpu")`、NumPy 或逐元素 Python 运算处理在线 KV 数据；热路径不得增加逐请求 Python 循环、`.item()` 等同步开销。 |
209: | H06 | 仅替换 FULL 层所需的缓存布局与读写/Attention 路径；保留 GDN 状态和原生页号、层号、组共享页的逻辑对应关系。 |
210: | H07 | 必须重写 Decode Stage1 为真正的 **fused INT2 CV kernel**；CV 的含义与计算分工以指定 PR 和目标硬件实现为准，不能只改函数名。**（v2 核实：OSCAR 上游无 "CV" 术语——两个 OSCAR 参考仓中均不存在；在目标硬件上 CV = Ascend 的 Cube/Vector 双计算单元分工，参见 references/vllm-ascend `attention/dsa_v1.py` 与 `docs/design.md` §5.2 的落地。）** |
211: | H08 | 不保留冗余的完整 BF16 History、重复 Sink/Recent staging 或重复历史 MTP shadow cache；不得用 KV 双写抵消压缩收益。 |
212: | H09 | Decode/verify 不得每步执行全历史 `full_dequant + inverse rotation`，不得把完整历史恢复到 HBM 后再调用普通 Attention。 |
213: | H10 | chunked prefill 不重复搬运或压缩已完成处理的历史；首次 prefill 尽量减少不必要的压缩及压缩后立即恢复。 |
214: | H11 | MTP 必须遵循原生 vLLM Ascend 的计算、提交和回滚语义；不能误把 verify 当成普通 prefill，不能增加重复计算。 |
[...]
216: | H13 | 16K–50K 输入长度必须实际进入并使用 OSCAR，不得静默回退；必须兼顾混合长度 batch。 |
217: | H14 | 必须保持附录 A 的目标启动参数，包括 TP=4、MTP、异步调度、图模式、W8A8 权重量化和 GDN cache dtype；不能通过关闭功能获得验收通过。 |
218: | H15 | 每次 probe、校准或临时服务结束后，先确认本任务创建的 worker 和 NPU 资源已释放，再启动正式服务。 |
219: | H16 | 任务一开始先把当前工作区下的 `issue1_full_record.md` 完整读一遍建立整体印象；执行中遇到任何不会的、不确定的、拿不准的或真机报错，必须再回该档案按开头症状速查表定位条目，然后才决定下一步；禁止凭猜测硬试（详见第 0.1 节）。 |
220: | H17 | **不准有任何回退逻辑**：任何序列长度、任何 batch size、任何阶段（prefill / chunked prefill / decode / MTP verify）都必须走完整的原生 OSCAR 语义压缩路径；不得静默回退到原生 BF16 全历史、不得跳过 OSCAR、不得降级。确实不可达的场景必须显式报错，而不是降级（详见第 0.3 节）。 |
[...]
262: - 模型配置中的层类型、层数、KV head 数、head dimension、TP 后各 rank 的本地维度、GDN 状态形状和 dtype。
263: - 当前生效的 block size、KV cache spec、分组规则、Attention 后端、MTP 路由和图捕获机制。
264: - PR 的旋转矩阵或检查点来源、量化参数、校准流程、已有精度测试和配置方式。
265: - 公平对照需要的输入数据、输出长度、并发、采样参数、重复次数和质量验收指标。
266: 
[...]
271: 阅读与任务有关的完整调用链，包括接口、调用者、元数据结构和测试，形成带文件/函数位置的说明：
272: 
273: 1. OSCAR：配置 → Sink/History/Recent 状态管理 → 旋转/裁剪/量化 → cache store → prefill/decode → 输出合并。
274: 2. vLLM KV 管理：`kv_cache_utils.py` → cache spec/层分组 → block 分配与生命周期 → block table/slot mapping。
275: 3. vLLM Ascend：`model_runner_v1.py` → 物理分配与视图 → FULL/GDN 后端 → worker 初始化和算子调用。
[...]
333: 
334: 1. **端到端生命周期图**：**一个或一组 batch 请求**（必须同时覆盖：单请求；以及混合 batch——长短序列不一、prefill / decode / MTP verify 共存、请求动态加入与退出）从 API 进入 → scheduler 调度与块分配（分组/块表/页；batch 内每个请求的窗口与历史范围如何分别推导） → worker/model_runner 前向 → FULL 层 OSCAR 后端与 GDN 层原生后端的各自路径 → 各阶段（首次 prefill / chunked prefill 续 chunk / decode / MTP draft+verify）的 KV 写入与读取 → 输出与页回收。图上每个节点标注：**数据形态**（BF16 / INT2 slot / staging BF16 / 元数据）、**所在设备与流**、**同步点**、**触发的原生符号与插件接缝**；混合 batch 的元数据必须展示批量向量化推导（无逐请求 Python 循环），且任意一条 batch 情形（短序列/空 History/跨页/混合长度/各种 batch size）都能在图上被指认。
335: 2. **维度联动矩阵**：行 = OSCAR 的关注点（spec/布局、store、history attention、window、merge、旋转/clip/量化、校准、MTP、显存收益），列 = 原生机制（平台后端选择、KV spec 注册、分配/视图、块表与 slot mapping、调度块大小 LCM、prefix cache、Mamba/GDN 状态、MTP proposer、图捕获 FULL_DECODE_ONLY、TP 通信、异步调度、W8A8）。每格写清：原生行为（file:line 证据）/ OSCAR 如何接入（注册/wrap/子类/受控 patch，不改源码）/ 必须保持的不变量。
336: 3. **关键时间线**：① 一个 token 从 projection 产出 → 旋转 → clip/量化/打包落盘（+staging）→ 被 decode/verify/续 chunk 的 fused kernel 消费 → 页回收的完整旅程；② MTP 一轮（draft 3 步 → verify(q_len=4) → 全接受/部分接受/全拒绝）的缓存可见性与窗口推导时间线；③ 抢占→恢复后各状态（INT2 页、staging owner、GDN conv/ssm）的一致性时间线。
337: 4. **全局账两本**：(a) **显存/容量推导链**——从模型配置（层数/层型/head 维度/TP）→ spec 与分组（48 GDN + 17 FULL → 3 mamba 组 + 1 FULL 组 → 17 共享张量）→ 张量内布局（conv/ssm/尾切 K-V 区）→ 池块数与可用 token 容量（INT2 + 块大小机制的收益落点），全链路公式，不给局部孤式；(b) **性能预算表**——每个相位（prepare/store/history_attn/window_attn/merge/host）的 HBM 流量与计算量上界，对照附录 D.4 与 D.1 原生基线，host/device 分工与异步边界。
338: 5. **长度标尺表（长度通用性，强制）**：短序列自不待言（L<S、L<S+R、空 History 已在窗口语义内覆盖）；**本项目的长序列工作负载 30K–60K 起步，向上直至 `max_model_len=262144`**。设计的每一点都必须给出一行长度标尺：在 16K / 32K / 50K / 100K / 262144 下，该点的**行为**（窗口边界、跨页、元数据形状、workspace 占用、kernel tiling 与 grid、块表列宽、打点形态）与**量级**（HBM 流量、计算量、耗时上界）各是什么。禁止任何"按长度分叉"的逻辑（某长度以上走不同分支=回退，0.5 判例 1）；确实随长度变化的量（split 数、tile 数、workspace）必须是**连续公式**而非分段分支。
[...]
351: ### 5.0.3 设计必须证明的四条性质（评审判据）
352: 
353: 1. **OSCAR 原生逻辑 100% 兼容、精度准确——但 PR 是按 vLLM（CUDA/上游）思维写的，其工程设计在 vllm-ascend 上必须重设计并允许优化**：
354:    - **必须 100% 对齐的是数值语义**：INT2 编码映射与位序、量化器公式与 fp16 舍入自洽、窗口（Sink/History/Recent）定义、旋转正交等价链（`q@R_k` / `@R_v^T`）、clip 语义、精度口径与验收容差。
355:    - **必须重设计/优化的是工程实现**（PR 原生思维是 CUDA/Triton 与上游调度，不是 Ascend）：Triton kernel 形态 → AscendC fused kernel（tile 内解包/在线 softmax/Cube-Vector 分工）；PR `supports_spec_as_decode=False`（verify 被归类 prefill 全量反量化——本任务 H09/D.3 明令禁止）→ Ascend 原生支持 q_len=4 verify 且历史 tile 跨 query 复用；PR `_cudagraph_support=NEVER` → 目标 `FULL_DECODE_ONLY` 图模式（UNIFORM_BATCH + 固定 split + 预分配 workspace）；PR 续 chunk 全量反量化+逆旋转物化 → 续 chunk 直接 fused INT2 attention（零物化）；PR 边界层 skip 等"allocator 机制未就绪"的权宜 → 在 Ascend 布局内正面解决或显式登记；staging arena 的原子协议 → 按 NPU 能力重证等价。
356:    - **每一项"PR 工程设计 → Ascend 重设计"都必须证明语义等价**（数学等价链/数值对拍）并登记进差异表（差异 = 实现形态差异，不是语义差异）；PR 快照未覆盖的语义（spec decode 融合、hybrid 混合模型、图模式、MLA 真集成）不是"差异"，是 Ascend 侧必须补全的设计自由度——按 OSCAR 语义自行设计并自证，标"PR 未覆盖 + 自证方式"；PR 未定义清的地方标"待核实"并给复核路径；数值门槛冻结在前，事后放宽即判设计失败。
357: 2. **与 vllm-ascend 100% 兼容**：只经允许接缝接入、不改原生文件（H01/H02）；GDN 的 conv/SSM 状态与原生页号/层号/组共享页关系不变；调度块大小 LCM、prefix cache、页复用/抢占、MTP proposer 语义不变；FULL_DECODE_ONLY + 异步调度 + TP=4 + W8A8 + mamba cache dtype 共存；插件注入失败即显式中止，不冒充成功。
[...]
377: ```text
378: Sink    : 固定的初始 tokens，BF16
379: History : 历史 tokens，旋转 + 裁剪后量化为 INT2
380: Recent  : 最近 tokens，BF16
381: 
[...]
384: ```
385: 
386: 以上读路径描述数学语义，不意味着每个 decode/verify step 都要在 HBM 中生成完整 BF16 历史。必须研究 PR 中旋转、Query 变换、Attention 累加和输出逆变换的具体关系，证明融合实现与参考算法一致，再确定哪些变换可以合并或移动。不能未经证明就把 K/V 的逆旋转随意换到 Query 或输出侧。
387: 
388: `--quantization ascend` 对应的现有模型权重量化配置必须保留；OSCAR KV 量化配置按 PR 的方式通过外部适配接入，避免覆盖或混淆 W8A8 权重量化。
[...]
429: ```
430: 
431: 上式仅是 payload 下界；若逐 head/group 单独打包，应按真实打包单元分别取整后求和。继续展开 scale、zero point（若 PR 使用）、旋转参数、分组描述、长度、页表及 padding 的布局和对齐。明确元数据按 token、group、page、layer 还是 rank 计费，防止漏算或重复计费。
432: 
433: 原稿示例在 `E_K = E_V = 256` 时：
[...]
446: 
447: M_cache_total = 所有真实物理缓存分配的总和
448: M_runtime_extra_peak = 旋转常量 + 算子 workspace + MTP 必要暂存
449:                      + 图捕获相关缓冲及其他新增分配的实际峰值
450: ```
[...]
475: | 算子/能力 | 必须处理的问题 |
476: | --- | --- |
477: | `rotate_clip_quant_int2` | 旋转、裁剪、scale/量化参数、量化、位打包和写入的融合；K/V 参数分别核实。 |
478: | INT2 pack/unpack | 2-bit 编码、位序、尾部元素、head/group 边界、对齐、并发写入。 |
479: | KV Store / Recent→History | Sink/Recent 正确写入、窗口迁移、页地址映射，避免 staging 和双写。 |
[...]
491: 
492: - **先把上一版的失败数字当作设计前提（附录 D.3）**：32K 步 dequant 单算子 6.5s/卡、占该步 95.4%，而原生整段 32K prefill 才 4.6s。任何会产生"随历史长度线性增长的全量恢复/搬运"的设计，在写代码前就必须被否决。
493: - 不能每个 verify step 对全部历史做显式 `full_dequant + inverse rotation`。原稿指出稠密逆旋转可能额外引入 `O(LD²)` 计算；必须给出实际实现的计算量和带宽分析。
494: - 不将历史长度为 `L` 的完整 BF16 K/V 写回 HBM，再用另一个 kernel 读取做 Attention。
495: - MTP 不为每个 query 单独扫描同一份历史 INT2 HBM。设计历史 tile 的读取与跨 query 复用，量化 `q_len` 增长时的历史读取量。
[...]
502: ### 6.3 每个核心内核的设计交付内容
503: 
504: 给出 AscendC 伪代码及最终实现，解释全局内存/片上缓冲布局、tile 选择、硬件计算单元分工、异步搬运与同步、累加精度、mask、边界处理、跨核归约和 workspace 生命周期。
505: 
506: **每个内核还必须交付一个「D.4 对照段」**（第 0.7 节铁律）：① 该内核对应附录 D.4 打点的哪个相位；② 前人在该相位的失败模式（逐行 inline dequant / 全历史物化 / 写路径冗余搬运 / host 异常开销）；③ 本实现结构性规避的具体机制（tile 融合、UB 内解包、一次性 136B/token 历史读取、行级复用、融合 scatter、无 host 热循环）；④ 预期量级与 D.4 基线/原生基线的对比结论。**没有 D.4 对照段的内核设计视为未完成。**
507: 
508: **精度门槛先行**：内核进入性能对照前，必须先通过与纯 torch 参考实现的对拍（位级或 `configs/acceptance.json` 冻结容差）；数值不达标即返工，禁止带错跑分。
509: 
510: 图捕获所需的固定地址、workspace、算子注册与动态长度元数据必须与目标 `FULL_DECODE_ONLY` 路径兼容；MTP 中 `enforce_eager=true` 的实际作用域以原生行为为准，不能擅自把整个服务改成 eager。
[...]
551:   → 检查 NPU、依赖、编译器和接口能力
552:   → 安装外部插件并编译/加载 AscendC 算子
553:   → 若 PR 要求，生成或验证旋转/校准检查点
554:   → 执行算子、集成、TP=4 和目标路径 probe
555:   → 关闭临时引擎/worker，清理本任务资源
[...]
563: - 在关键步骤失败时以非零退出码退出，打印阶段、错误、完整日志位置；probe 失败或资源未清理完毕时不得继续拉起正式服务。
564: - 可重复执行，记录插件/算子/配置版本和构建结果，避免加载旧产物。
565: - 用清晰的进程生命周期和退出处理管理本任务的 API server、EngineCore、worker、校准进程及共享内存。
566: - “清理 NPU”指释放本任务创建的进程和资源，并验证释放结果；不能只调用 `empty_cache()` 后假定 worker 已退出，不能无差别终止他人任务或重置整机设备。
567: - 对编译、worker 初始化、probe、退出等待和健康检查设置可诊断的超时，输出每个 rank 的进展。
[...]
577: | --- | --- |
578: | #151 history解包64.71%，用户candidate整轮仍约19分钟 | 新整数布局/half转换保持旧数学和live/padding检查，原核保留独立对照；65536码穷举、特殊half逐位、NPU图和同形2+5速度门必过，局部份额不能外推整体19→8。 |
579: | #151 q4测量已完成却最终缺证据：阶段状态覆盖同名结果 | 子进程输出不得占用run_phase的`<phase>.json`；保留数据/退出状态两个文件，用真实子进程回归验证，不仅mock phase。失败显示具体缺失字段，不降低精度/签名门。 |
580: | #150 q1局部收益通过后，q4目标图占比仍未拆解 | 保留已验证内核；q4用实际paged BF16 FIA对照，并将正常Event与独立插桩分开。只按同核/引擎/来源解释SYS_CNT，不将跨核最大值、重叠区间或单算子×层数当全图实测；不重跑AISBench。 |
581: | #150后续：MTP q1/N128/S3 CV约48.5ms，q4约14.8ms；实际history仅6核参与 | 后续MTP的host q1标记允许独立逐token调度，但保留全部padding/task/数学/地址。真NPU同形逐位、图、2+5设备测速门先行；不用AISBench重跑，不把核数比或单样本份额当全程收益。 |
582: | #150 decode32无复用簇仍运行C4，0.104%差值阻断服务 | 用单请求query上界证明不可能成簇时选择既有fe0 INT2核；生产/probe共享分流，保留原始C4数值/图门。相同算子自比记重复性，实际C4仍执行ratio≤1.0；小差值不得冒充端到端根因。 |
583: | #148 局部 CV/K4 加速而用户 LongBenchv2 精度下降，整批仍远慢于原生 | 保留用户确认精度正确的 fe0 原内核；候选独立入口须同输入逐位、冻结 oracle、图回放和速度门全部通过。局部时间不得折算为用户整批占比；用同 rank/step/stream 的异步区间并集观察真实负载，完整模型精度与约8分钟目标仍由用户验收。 |
584: | #145 M128 CV在D64/Q6/context511出现NaN，Q1/Q4通过 | 同一score UB从MTE3读出切换到MTE2覆写必须建立MTE3→MTE2依赖；重复NaN工作区覆盖32行块及双lane边界。CPU-debug串行DMA不替代真NPU数值门；一键继续完整热点与native/OSCAR长请求并发性能门。 |
585: | `Unsupported vllm-ascend version: 0.23.1.dev0+g5cb98caaa.d20260822` | 区分目标版本与开发构建版本，核实 commit/接口兼容性，不误拒绝，也不盲目放行。 |
586: | `DeviceOperator` partially initialized / circular import | 调整外部插件导入依赖和注册时机，测试全新进程启动；不能捕获后跳过 OSCAR 注入。 |
587: | `Device string must not be empty` | 在创建 LLM/校准引擎前确认平台识别成功；定位先前导入失败，不用硬填 device 字符串掩盖问题。 |
588: | `LD_PRELOAD detected`、`Invalid thread pool!`、`ParallelOpenMP.cpp:64`、递归 terminate | 记录动态库和线程池环境，检查初始化、进程启动和线程设置顺序；通过复现诊断，不盲目增加预加载库或反复修改线程数。 |
589: | `No module named 'vllm._C'` | 按 Ascend 实际路径判断是否缺少必需能力，不能照搬 CUDA 扩展修复方式，也不能把所有 warning 都当作可忽略。 |
590: | Breakable cudagraph 被 Ascend 禁用的提示 | 区分原生平台能力提示与 OSCAR 新增故障，验证目标 `FULL_DECODE_ONLY` 实际执行路径。 |
591: | 旋转检查点生成时 NPU OOM | 历史记录为 NPU 0 总量 29.49 GiB、已分配 28.97 GiB、尝试再分配 172 MiB。核实 TP、残留进程、重复加载和校准峰值，不得用单卡加载整个模型或在服务占卡时重复加载模型。 |
592: | `'LLM' object has no attribute 'model'` | 使用当前版本实际支持的 worker/model 访问机制，不能假设前端 `LLM` 暴露内部模型。 |
593: | `function is not serializable`，提示 `VLLM_ALLOW_INSECURE_SERIALIZATION=1` | 核实 RPC 支持的消息/方法机制，优先使用已注册方法与可序列化数据；不能只因报错提示就默认打开不安全序列化绕过。 |
[...]
600: | #157 默认APC首轮candidate服务四rank同步507035 vector trap | trap即冻结status_guard发现某族status非零（与#142同一Trap偏移0x264，内核未变）；后续定位到MTP attention族，具体错误码尚无回传。prefix hit=0不能排除APC align/自身窗口，低generation不能判定内部无draft。归因用默认关闭的 `OSCAR_GUARD_HOST_SYNC=1` 给出 site/family，不回读内容、不动fe0冻结集；later-draft仅按原生明确discard掩码隔离，活行非法slot保留给guard。详见2026-10-13复审。 |
601: 
602: 旋转检查点若需生成，必须复用正确的权重量化与 TP 配置，明确其与模型/层/rank/维度/PR 版本的对应关系，避免重复校准和错误复用。校准中的旋转、量化及大规模数据计算同样遵守 NPU 约束，不能因处于离线阶段就转移到 CPU 处理。
603: 
604: ## 9. 端到端 Checklist 与证据规则
[...]
622: - [ ] **A04** 读懂第 3.3 节调用链，记录 FULL/GDN、TP、KV 分组、MTP 和图模式的真实入口。
623: - [ ] **A05** 核实第 4 节全部歧义，给出层/组/Tensor/地址映射与字节来源。
624: - [ ] **A06** 读取 PR 的配置、旋转、量化和精度验证方法，完善本 Checklist，列出仍缺失的输入。
625: - [ ] **A07** 任务开始时已把 `issue1_full_record.md`（含第三部分 [74]~[86]）完整读一遍并掌握其查表用法（症状速查表 → 条目跳转），并将其中与当前任务相关的故障模式登记进第 8.2 节回归检查；确认不会参考任何失败 OSCAR 实现的代码（第 0.2 节红线）。
626: 
[...]
632: - [ ] **B04** 完成算子清单、AscendC 融合划分、Decode Stage1 伪代码和逐阶段读写流程。
633: - [ ] **B05** 给出 decode 计算量、HBM 流量、MTP 跨 query 复用和 Host 调度预算。
634: - [ ] **B06** 固定功能、精度、性能测试方法和验收门槛，设计一键脚本及错误清理流程。
635: 
636: 阶段 B 通过后直接进入实现；不必重复等待用户批准已授权的实现工作。
[...]
640: - [ ] **C01** 独立插件/算子工程可安装、可编译、可加载，原生源码未修改，安装脚本不使用 `cp`。
641: - [ ] **C02** 版本能力 probe、延迟注册和幂等 Hook 通过 CLI、API server、各 worker 初始化验证。
642: - [ ] **C03** 实现并验证 INT2 编码、旋转/裁剪/量化、KV store 与 Recent→History 增量迁移。
643: - [ ] **C04** 实现真实 fused INT2 CV Decode Stage1（CV=Cube/Vector，见 H07 注），并完成必要的分块/分段输出合并。
644: - [ ] **C05** Sink/Recent Attention、History Attention 和参考数学语义一致，数值稳定。
[...]
658: - [ ] **D09** 前缀缓存、页共享/复用、请求取消/结束、抢占恢复等目标环境可达生命周期通过验证。
659: 
660: ### 阶段 E：精度、性能与显存验收
661: 
662: - [ ] **E01** 核心算子对齐参考；覆盖 pack/unpack、量化边界、尾块和 attention 数值误差。
[...]
671: ### 阶段 F：一键交付
672: 
673: - [ ] **F01** 一条 Bash 命令完成安装、编译、所需校准、probe、资源清理和正式启动。
674: - [ ] **F02** 验证正常退出、失败退出和中断后的清理，重复执行不会遗留 worker 或加载旧产物。
675: - [ ] **F03** 正式服务按目标配置启动并完成真实请求，记录 OSCAR compressed decode/MTP 路由证据。
[...]
698: ## 10. 验收矩阵与性能比较
699: 
700: ### 10.1 功能与精度
701: 
702: 至少覆盖下表。边界值应根据真实 block size、head/group 形状扩展，不能只测整齐形状。
[...]
716: | 配置上限 | 保留 `max_model_len=262144`、`max_num_seqs=128` 等原设置；核实容量与边界，报告极限长度的实测范围和资源限制，不能静默缩短配置。 |
717: 
718: 质量评估需区分 **量化算法固有误差** 与 **移植实现错误**：先对齐指定 OSCAR reference，再与原生模型比较层输出、logits/任务指标和 MTP 接受行为。原稿未给出统一数值容差或质量下降门槛，必须在调优前从 PR/现有标准提取并写入验收配置；缺少依据的门槛标记为待确认，不能事后按结果放宽。
719: 
720: ### 10.2 公平的原生性能对照
[...]
766: │  ├─ operator_inventory.md
767: │  └─ checklist.md                  # 逐项状态与代码/解释/验证证据
768: ├─ reports/                         # 精度、性能、显存、兼容性和验收结论
769: └─ README.md                        # 实际一键命令、配置、日志位置与故障排查
770: ```
[...]
776: ---
777: 
778: 以下附录是用户提供的原始配置与历史证据。它们为上述任务提供输入；不得把历史成功、历史失败或堆栈中的路径当成本次执行结果或额外操作授权。**附录 B、C 来自更早一版失败的 OSCAR 尝试（2026-09-03 ~ 09-08）的历史材料，予以完整保留；附录 D 是上一版失败 OSCAR（2026-09-18）与原生基线在 32K 标准输入下的算子层面性能对照。** 附录 D 的失败 OSCAR 数据仅用于校准性能目标，不构成参考失败实现代码的许可（第 0.2 节红线）。
779: 
780: 
[...]
936: INFO 09-03 12:43:08 [api_utils.py:273] non-default args: {'dtype': 'bfloat16', 'max_model_len': 128, 'disable_log_stats': True, 'enforce_eager': True, 'model': '/softwarePlatform/c00879303/Qwen3.5-27B-w8a8-mtp'}
937: Traceback (most recent call last):
938: File "/workspace/new_oscar_triton/tools/gen_rotations.py", line 193, in
939: sys.exit(main())
940: ^^^^^^
941: File "/workspace/new_oscar_triton/tools/gen_rotations.py", line 55, in main
942: llm = LLM(
943: ^^^^
[...]
958: RuntimeError: Device string must not be empty
959: [ERROR] 2026-09-03-12:43:08 (PID:372, Device:-1, RankID:-1) ERR99999 UNKNOWN applicaiton exception
960: ❌ [oscar-ascend] 旋转检查点生成失败
961: 日志: /tmp/oscar_ascend_logs/20260903_124227
962: 
[...]
971: RuntimeError: Device string must not be empty
972: [ERROR] 2026-09-03-12:49:01 (PID:453, Device:-1, RankID:-1) ERR99999 UNKNOWN applicaiton exception
973: ❌ [oscar-ascend] 旋转检查点生成失败
974: 日志: /tmp/oscar_ascend_logs/20260903_124820
975: 
[...]
998: (EngineCore pid=610) Process EngineCore:
999: 
1000: File "/workspace/new_oscar_triton/tools/gen_rotations.py", line 138, in main
1001: model_mod = llm.model.model if hasattr(llm.model, "model") else llm.model
1002: ^^^^^^^^^
[...]
1013: /usr/local/python3.12.13/lib/python3.12/multiprocessing/resource_tracker.py:279: UserWarning: resource_tracker: There appear to be 1 leaked shared_memory objects to clean up at shutdown
1014: warnings.warn('resource_tracker: There appear to be %d '
1015: ❌ [oscar-ascend] 旋转检查点生成失败
1016: 
1017: File "/workspace/new_oscar_triton/tools/gen_rotations.py", line 134, in main
1018: per_rank = llm.llm_engine.apply_model(calib.capture_cov)
1019: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[...]
1065: ## 附录 D：失败 OSCAR 与原生基线的性能对照（32K 标准输入，完整保留）
1066: 
1067: **32K 输入长度是本项目的标准验收长度。** 以下两组数据来自同一台机器、同一拉起方式（附录 A 目标启动命令）的真机实测：一组是禁用 OSCAR 插件的原生 TP4 基线（验收参照系），一组是上一版失败 OSCAR 的算子级打点（`oscar-timing`）。**它们仅用于校准性能目标与定位禁区，不代表本次执行结果，更不构成参考失败实现代码的许可（第 0.2 节红线）。**
1068: 
1069: ### D.1 原生 TP4 基线（OSCAR 插件禁用）
[...]
1088: 
1089: - 同一 32K 级输入的算子层面对比：原生整体 prefill **4.6s**（31,897 tokens，6869.5 tok/s）；失败 OSCAR **单个 prefill 步仅 dequant 一个算子就花 6.5s/卡**（wall 6.8~7.0s）——单步单算子比原生整段 prefill 还慢。
1090: - attention 本身不慢：FIA 在 32K 步仅 ~18.7ms、16K 步仅 ~7ms。瓶颈 100% 在反量化路径——该实现把历史 INT2 全量 dequant 恢复后再做 attention，正中 H09 禁止项（每步全历史 `full_dequant + inverse rotation`）。
1091: - 对本次实现的硬性启示：
1092:   1. 任何路径（prefill / decode / verify）都不得做全历史恢复（H09），历史读取与恢复量必须对历史长度亚线性，并用同级别打点自证；
[...]
1471: | [84] | `Invalid thread pool!`（EngineCore worker 启动即炸） | vLLM 只在 OMP 未设时才在父进程建池；预 pin OMP 跳过其建池分支 | e1e8852（fork 前父进程显式建池） |
1472: | [85] | merge 链接 `ld.lld unknown file type`（G7/G8 回潮） | build 目录被多配置增量复用，ExternalProject 子工程喂陈旧 .o | 253d740（配置漂移清目录 + 一次干净重试） |
1473: | [86] | `found 16 FULL layers but expect_layers=17` | 校准引擎无 speculative_config，draft 层不存在且校准时永不触发 | b56597a（校准 16 模型层，draft identity 回退） |
1474: 
1475: **教训汇总（写码前先默念）**：①前置检查一律记录制；②环境/脚手架代码和算子代码同等级别地查档案、写测试；③凡涉及 CANN/SOC/编译链的决定，先在参照物（vllm-ascend 同栈代码）里找先例；④任何修复必须回填档案与回归表（本表即范例）。

## gpt_new_oscar_kimi/reports/decode_critical_chain_20261012.md
[...]
42: ## 下一实现主线：AIC侧整块/大块ND→L1装载
43: 
44: **保持AIV现有FP32 GM publisher和原FP32/K128数学顺序，只改变AIC将这些块搬到L1的形状/驻留策略。** 目标是消除目前8个跨行32KiB ND2NZ载入的串行暴露；它不是重新尝试失败的AIV NZ重排，也不改变scale/zero或矩阵归约精度。
45: 
46: 官方已存SDK `matmul_config_utils.h::IsBFullLoad` 要求 `stepN*baseN>=N` 且 `stepKb*baseK>=K`；`data_copy_wrapper_nd.h::CopyND2NZ`由真实tile height/width生成Nd2NzParams；`scheduler_norm.h`通过CopyCubeInB加载。必须继续核合法GetMatmulApiTiling配置是否能让完整256×256 B一次/少次载入，再由原K128/MMAD消费，不能手捏tiling字段或仅看源名称宣称全载入。

## gpt_new_oscar_kimi/reports/host_prepare_reuse_20261015/review.md
[...]
7: - `metadata.from_common` 已按 native common 对象缓存 CPU cumulative，不能重复申领“移除每层CPU列表重建”的收益。
8: - `draft_discard` 已在 builder 处理原生显式 discard 和逻辑拒绝边界；本轮未改变它、MTP或GDN。later-draft 的冻结 prepare 仍会在设备检查虚拟块表，未以跳过活行检查换速度。
9: - `GraphWorkspace` 按 device/geometry 共用；普通 FULL 层重复生成的任务仅依赖 native metadata、Hq/Hkv、sink/recent 和 split 数，不读取各层物理 raw 或旋转内容。每层 Q/K/V 投影、rotation、attention、FIA、merge、KV 写入和 status_guard 均保持。
10: - 除 `impl.forward`，另一个生产 prepare writer 是 `current_only_dispatch`；mixed 分区递归进入 `impl.forward`。这两条提前返回路径均在入口与 finally 使租约失效，分区自身禁止复用。
11: 

## gpt_new_oscar_kimi/reports/mixed_prepare_reuse_20261015/design.md
[...]
35: Host验证覆盖：16K典型混合步、不同split数/Hkv、int32/int64 slots；区域地址/容量与不相交性；完整descriptor/positions/输出等价；prepare32→2且其他逐层调用不减少；层与region顺序变换；相同地址的新ForwardContext；注册owner变化；CPU镜像在创建tuple后变化；whole/current-only等writer后的失效；非法长度与原guard保留。既有mixed/APC页域及discard回归保留，未改物理页语义。
36: 
37: `tests/test_mixed_prepare_reuse.py` 执行只读reference的完整ForwardContext类及get/override代码，16K metadata链使用CPU算子替身；实际 `OscarAttentionImpl.forward` + mixed dispatch 的512长段完成数值对拍，16K长段用shape-only QKV和真实CPU任务表检查默认selector每层进入hybrid与B1。前者不是NPU精度，后者不是模型数学验证。
38: 
39: `tools/probe_mixed_prepare_reuse.py` 是独立可执行NPU门：同一固定地址16384token/31q4+16260long/16FULL层，off每层两次prepare，on每区域一次；真实native ForwardContext每step新建，layer名跨step不重叠，故刷新不能依靠重复首层碰巧命中。依次32K→64K→非法long length，逐位比较全部16列descriptor与positions，独立检查非法long域error1保留。使用冻结prepare/source2抑制/边界guard，不执行CV、模型或AISBench。

## gpt_new_oscar_kimi/reports/simulator_b4_evidence_20260930/README.md
[...]
12: 同一 source0 AIV/core0 历史路径在 4K→8K 增加 16 个 KV256 tile 时，每增加一 tile 的模拟周期分别为旧 fast `95,057`、基础 striped `60,096`、SIMD striped `45,108` ticks；旧/SIMD 增量比约 `2.107×`。4K SIMD 整核临界已移至 source1/window，因此不能用整核 4K→8K 增量冒充同一历史 actor 斜率。
13: 
14: **模型方向校准。** 同一 4K fixture 的 fe0 与 fast 输出逐字节一致；CAModel `2,465,188→1,674,968` ticks（fast/fe0 `0.679`）。已回传的真 NPU 是另一形状 q4 N128/S3、20–30K 历史，`15.29794→11.28152ms`（`0.737`）。方向相同，比例并不相等，所以本报告不把 CAModel ticks 换算为真机毫秒或整轮收益。
15: 
16: **最小重放。** 已存在的本机 VM fixture 与库路径写在 [`replay_ctx8191_triplet.py`](replay_ctx8191_triplet.py)；[输入清单](fixtures/synthetic_q4_ctx8191.json) 绑定 `make_fixture` 固定种子、`raw_to_striped` 的逐位排列及各文件 SHA256。以下命令从当前工程根运行，调用本机 Lima 127.0.0.1，不连目标机器：
[...]
32: **边界。** 单请求 S1 的 4K/8K 合成算子不代表实际 32 并发 N128/S3、20–30K/65K、MTP、GDN、图或队列；实际长期性能及模型质量仍须用户侧 NPU 门裁决。不能从 `2.095×` 算子模拟比推定 LongBenchv2 八分钟或 64K 四百四十秒。
33: 
34: 模拟使用的 VM 编译库 SHA256 是本次精确产物身份。[源码等价记录](source_equivalence.json)证实四个 striped decode 核/解包头中，两个头逐字节相同、两个 `.cpp` 仅注释变化；去 C++ 注释后的 token 序列与 SHA256 均相同，所测数学执行体与当前文件一致。最终接线、绑定和重新构建的实际产物仍需精度、图与真 NPU 速度门，不能把 CAModel 周期自动转签为服务性能。

## gpt_new_oscar_kimi/reports/stable_32k_64k_20261015/analysis.md
[...]
52: 4. **q4有额外已完成但未集成的研究证据，应独立核清资格。** `fp32_dataflow_20261013` hybrid L1长q4同库完整2658960→2214530 ticks（1.200688倍），短形约1.109倍。只可作为q4候选局部证据；不外推C16/整模型/目标设备。该路径和C16互补，优先复用已有完整报告，不重复跑无关micro。
53: 
54: 以上源码机制不是新真机根因记录，故未追加故障档案。精度、CANN/CPU-debug、模拟配对、NPU完成、图、模型质量、容量、整轮性能分别裁决，任何本地结果都不宣称两个30%门已通过。

## gpt_new_oscar_kimi/skills/oscar-quant-optimization/SKILL.md
[...]
1: ---
2: name: oscar-quant-optimization
3: description: 在 gpt_new_oscar_kimi 工程优化 OSCAR INT2 量化、反量化及相关 attention 数据流，按现存源码、配对证据、冻结精度和一键候选交付形成闭环。用于该工程的性能迭代与真机反馈处理，不用于其他 OSCAR 工程或通用模型调优。
4: ---
5: 
[...]
10: 以 stable `f96820f1` 的全部已工作机制和默认启动方式为主分支基底，冻结完整 vLLM argv：默认 APC 关闭、显式预算16384、原生调度器，保留显式APC开关。下方旧默认APC开启/省略预算/120请求2–4倍要求被本条覆盖。本轮32K与64K均为300请求、512输出，目标同参原生端到端性能提升超过30%；证据见 `reports/stable_32k_64k_20261015/analysis.md`。禁止任何方式使用真机；独立完成必要本地实现/编译/模拟并交付一键入口，由用户最后认证。局部算子倍数不能冒充整轮目标，启动参数不能作为优化变量。
11: 
12: 用户随后接纳stable→B1完整1.2256808倍（单KV CV核范围）作为新主分支基底；pipeline→B1仅1.0410662倍不再构成剔除理由。下方历史单项1.15硬门被覆盖：允许小而真实的净收益累积，但须完整路径不退化、精度/协议不放宽、资源开销显式、在最新基底去重。旧实验原门与失败记录保留，不倒改历史。最终目标仍是同参native的32K和64K端到端超过30%，不能把局部22.6%相加成该目标。完成后推主分支供用户验证，stable由用户验证后更新。
13: 
14: ## 第一指示：找到并消除抵消 batch 收益的主要成本
[...]
21: 4. 每个候选必须回答：**针对哪个已确认的主要成本；可减少多少实际工作/暴露等待；新增什么成本；组合后是否足以恢复 batch 吞吐收益。** 减少指令、burst 或搬运次数本身不等于净提速；完整结果不支持时保存证据并换方向，不持续堆叠小改动或扩大复杂协议。
22: 5. 正常工作目标是让压缩节省的访存与容量发挥作用，避免反量化、浮点展开、MTP或同步成为新的限制。访存受限必须按资源层级取证；GM地址流量不能直接当HBM流量，也不能靠增加无用访问把算子变成访存受限。
23: 6. 保持冻结精度和两个一键入口。数学改动必须与项目真正的完整原空间 oracle 对照；旋转域局部差异、CPU归约树差异不能冒充完整算子或真NPU精度失败。局部提速不得替代整轮目标；证据不足则继续定位这个主要成本，不以整理文档或一个小优化结束任务。
24: 
25: 当前事实、字节账和未解决归因见 `docs/quant_dequant_roofline_20261011.md` 的“容量收益为何没有变成吞吐”节；该专项始终服从本总 MD。
[...]
46: 2. 用当前代码确认台账中的问题、路由和源版本仍存在；记录最小版本/源哈希与调用点。历史热点或旧 README 的待测状态不能覆盖更新的报告。先检查既有失败、完成结果、复用条件，避免重复同一实验。
47: 3. 当前整轮目标是相对 native **1342.4437259秒达到2–4倍**，即 **335.61–671.22秒**；FULL注意力KV目标6–7倍，同时报告全部KV。以 `docs/64k_120_optimization.md`、`reports/evidence_64k_120_20261009.json` 和用户后续指令核实适用负载与分母，不据小形状结果声称整轮达标。
48: 4. **单项与组合门（2026-10-12）**：完整相关算子/路径相对当前优化基底 `S=t_base/t_new >= 1.15`（速度提升至少15%），冻结精度与必要协议门通过即可进入组合评估，不再要求每个单项自身达到1.5倍或2倍。先计新增开销、适用频度和重复收益；不能只用helper15%领取完整路径资格，也不能把14.87%四舍五入为15%。正确性/兼容修复和合格项的必要依赖不受速度门拦截，但不能单领倍率。最终组合相对原生目标 **2–4倍，越快越好**。
49: 5. **本轮明确以组合方式提速**：量化写入、反量化/布局/复用、OSCAR缓存容量与任务执行效率协同减少完整路径成本。每项须有明确净贡献或必要依赖关系，过小单项不加入；最后验证实际组合，不能拼乘各自倍率。
50: 
[...]
73: - 原故障修复与性能组合同时推进，主代理负责资源、交叉审查、统一入口与即时交付；候选分别指派明确负责人，不能把“已交准备材料”说成“仍在执行”。并发按工具真实上限安排，满额时明确谁排队或由主代理承接，不虚报活跃子代理数。
74: - 每路固定当前母源、一个可证伪假设、完整路径收益门和下一决定性动作。达到门才集成；失败保存首错和真实状态，解释后切换，不堆小改动。兼容修复不等性能实验结束才推送，两入口同步。
75: - 复用已有精度、编译和完整配对；续跑先读该任务的完成回执，不重跑已完成实验。档案按相关标题读取，长 JSON 只提取所需字段，原始大 trace 留文件，不刷屏或反复塞入上下文。
76: - 源码分析/实现可并行；同一 VM 周期测量使用独占锁。子代理报告仅给新增事实、改动范围、结果、下一命令或阻塞；无新增信息不反复发送长摘要。
77: - 只做覆盖实际改动风险的验证；不以全量测试、无关 Git/stat 对齐或重复写长报告代替实现。运行前一次核对官方 CANN 环境与输出位置，源树/小容量 tmpfs 不承接大量调试日志。
[...]
85: - 不乘不相关局部倍率，不将FULL字节比、running数量或理想并行度换成吞吐。helper倍率只是helper范围；布局微测若host预pack免费，必须另扣实际publisher成本。
86: - **64K decode的主要机制按roofline核算**：INT2减少实际访存并释放KV容量，允许更大的实际decode批次；按用户提出的原生访存受限前提设计，要求OSCAR量化/反量化、临时数据搬运和MTP工作没有将组合推成计算或同步瓶颈。分别核算HBM/L2流量、Cube/Vector计算及关键依赖；容量增长不自动等于有效batch增长，驻留/Running也不等于当步decode batch。稳态条件下用 `X=(B_oscar/B_native)*(有效输出/请求/步_oscar÷有效输出/请求/步_native)*(T_step_native/T_step_oscar)` 估算decode吞吐比，并列MTP接受率、调度与屋顶测量的不确定性。目标的访存受限状态必须取证，不能凭压缩比宣称已实现；完整机制与边界见项目 `docs/quant_dequant_roofline_20261011.md`。
87: - 用已有native/OSCAR日志与真实工作量约束校准后冻结仿真；候选只改变源码证实的成本/任务量/依赖，不反调参数追目标。MTP轮数与native chunk数按证据或区间推算，不能用HTTP200或prompt吞吐为0判断完成/纯decode。
88: - 不机械丢弃所有小正收益，也不机械堆叠凑目标。用户当前门为**单项至少1.15倍**；达到此门且精度/协议合格的可组合，低于门的保留证据及重开条件。已测基底之间有重叠时去重计账；必要依赖可保留但不单领倍率。
89: 
90: 需要新实验时才读技能内 [实验卡](references/experiment-template.md)，把问题、方案、预先声明的门和最终结果放进同一小记录；已有报告满足字段时直接引用，不另造重复长文档。
[...]
103: ## 记录、交付、反馈再闭环
104: 
105: - 每项成功、失败、未完成均更新 `docs/optimization_ledger.md`：当前源码存在/启用状态、实验分母、精度范围、报告路径、组合依赖、当前选择、重开条件。原失败和真实rc不覆盖；本机失败不写成真机档案。新增真机错误才按档案制度追加。
106: - 保留清晰的精简终端摘要，同时保存完整相位日志、状态、真实退出码。不要让用户翻长文件；失败和清理结果必须可见。
107: - 最终候选由 `tools/serving_variants.py`统一，实际同步到：

## gpt_new_oscar_kimi/skills/oscar-quant-optimization/references/experiment-template.md
[...]
12: - **量化口径**：完整算子 `S_op=t_base/t_new`。仅对串行、互斥且不重复计费的阶段，`T_pred=T_fixed+Σ(N_i*t_i_new)+新增开销`；整轮对原生 `S_native=T_native/T_pred`，与对当前OSCAR的倍率分母不同。明确配对测量已包含哪些开销，只有未包含的新增开销另加，防止重复扣费。流水按DAG关键路径计算，不求actor/父子相位总和。缺调用数或份额时只给明确条件区间及待补证，不给单点整轮承诺。
13: - **可达上界**：只优化当前整轮互斥份额`f`时，`S_max_current=1/(1-f)`；若`T_fixed>=T_native/目标倍数`，单独优化该方向不能达标，继续找其他OSCAR主成本。它仍可凭明显净贡献成为组合项，不能把1.8倍writer当成2–4倍native。
14: - **校准冻结**：先用已有两侧日志及真实工作量约束校准模型，冻结参数后再预测；候选只改变源码证实的成本、任务量或依赖，不为命中目标反调占比/吞吐。MTP接受率对应轮数、native预算对应chunk数量按证据或区间计算；HTTP200、日志prompt吞吐为0不证明请求完成或纯decode阶段。
15: - **组合判断**：列相对当前组合节省的绝对秒数、比例、适用频度和测量波动/预测区间；未知波动不得写成稳定复现。核对与已选方案重叠/冲突及接入维护成本，再决定本轮纳入、仅作依赖或暂缓。用户现已规定单项 `S_op>=1.15` 可入组合；完整相关路径必须含新增成本并通过精度/协议门。不到门的保留重开条件，不能四舍五入凑15%。正确性/兼容修复和必要依赖不单领倍率；组合相对原生2–4倍，独立倍率不得直接相乘。
16: - **roofline与decode吞吐账**：分列FULL/全部KV字节、可驻留请求数、实际调度decode batch；列每个有效输出token对应的weights、KV、临时workspace、metadata、MTP访存，以及Cube/Vector工作和同步关键路径。给出原生与组合各自memory/compute-bound的证据或待证范围、MTP输出效率与批次扩张后的计算上限；不能把batch比直接写为吞吐比。对混合prefill/decode与排空阶段另计，不能把稳态decode倍率当成整轮倍率。
17: - **预声明执行**：同输入/同库/同配置绑定；需要覆盖的oracle/逐位/status/guards/任务计数；完整结果门；期限、空间预算、owned控制文件、日志位置。按改动风险选短/长、K1/多并发、q1/q4/mixed边界，不扩成无穷矩阵。没有阶段因果证据时先采最小必要闭合片段，不盲跑完整大形。

## vllm/.agents/skills/model-recipes/SKILL.md
[...]
35: the same path plus `.json`. Paths use the full Hugging Face ID, preserving
36: case; do not substitute `meta.slug` or a display title. For example,
37: `Qwen/Qwen3.8-27B` maps to
38: [recipes.vllm.ai/Qwen/Qwen3.8-27B](https://recipes.vllm.ai/Qwen/Qwen3.8-27B).
39: 
40: Recipe JSON is often over 20 KB, mostly the `guide`. Instead of printing it,
[...]
52: ```bash
53: curl -fsSL https://recipes.vllm.ai/models.json |
54:   jq --arg q 'qwen 27b' '
55:     ($q | ascii_downcase | [scan("\\S+")]) as $words | .[] |
56:     ([.hf_id, .title, .provider] | join(" ") | ascii_downcase) as $text |
[...]
75: read_recipe=.agents/skills/model-recipes/scripts/read_recipe.sh
76: recipe=$(mktemp)
77: curl -fsSL https://recipes.vllm.ai/Qwen/Qwen3.8-27B.json -o "$recipe"
78: "$read_recipe" "$recipe"
79: ```

## vllm/README.md
[...]
55: - Decoder-only LLMs (e.g., Llama, Qwen, Gemma)
56: - Mixture-of-Expert LLMs (e.g., Mixtral, DeepSeek-V3, Qwen-MoE, GPT-OSS)
57: - Hybrid attention and state-space models (e.g., Mamba, Qwen3.5)
58: - Multi-modal models (e.g., LLaVA, Qwen-VL, Pixtral)
59: - Embedding and retrieval models (e.g., E5-Mistral, GTE, ColBERT)

## vllm/docs/README.md
[...]
68: - Decoder-only LLMs (e.g., Llama, Qwen, Gemma)
69: - Mixture-of-Expert LLMs (e.g., Mixtral, DeepSeek-V3, Qwen-MoE, GPT-OSS)
70: - Hybrid attention and state-space models (e.g., Mamba, Qwen3.5)
71: - Multi-modal models (e.g., LLaVA, Qwen-VL, Pixtral)
72: - Embedding and retrieval models (e.g., E5-Mistral, GTE, ColBERT)

## vllm/docs/benchmarking/cli.md
[...]
1092: 
1093: ```bash
1094: vllm serve Qwen/Qwen3.5-2B \
1095: --host 127.0.0.1 --port 8000
1096: ```
[...]
1103: #https://raw.githubusercontent.com/kvcache-ai/Mooncake/main/FAST25-release/traces/conversation_trace.jsonl 
1104: 
1105: vllm bench serve --model Qwen/Qwen3.5-2B \  
1106: --dataset-name=timed_trace --num-prompts 100 --host 127.0.0.1 \
1107: --port 8000 --dataset-path ./conversation_trace.jsonl \

## vllm/docs/configuration/conserving_memory.md
[...]
117: # Don't accept images. Just text.
118: llm = LLM(
119:     model="google/gemma-3-27b-it",
120:     limit_mm_per_prompt={"image": 0},
121: )

## vllm/docs/configuration/optimization.md
[...]
290: 
291: ```console
292: VLLM_USE_FASTOKENS=1 vllm serve Qwen/Qwen3-8B
293: ```
294: 
[...]
300: 
301: from vllm import LLM
302: llm = LLM(model="Qwen/Qwen3-8B")
303: ```
304: 

## vllm/docs/design/cuda_graphs_multimodal.md
[...]
26: | `Qwen2_5_VLForConditionalGeneration` | `Qwen2.5-VL` | ✅︎ | ✅︎ | ❌︎ |
27: | `Qwen3VLForConditionalGeneration` | `Qwen3-VL` | ✅︎ | ✅︎ | ❌︎ |
28: | `Qwen3_5ForConditionalGeneration` | `Qwen3.5`, `Qwen3.6` | ✅︎ | ✅︎ | ❌︎ |
29: | `Qwen3_5MoeForConditionalGeneration` | `Qwen3.5-MoE`, `Qwen3.6-MoE` | ✅︎ | ✅︎ | ❌︎ |
30: | `Step3VLForConditionalGeneration` | `Step3-VL` | ✅︎ | ❌︎ | ✅︎ |
31: | `MiniCPMV` | `MiniCPMV2.5` | ✅︎ | ❌︎ | ❌︎ |

## vllm/docs/design/hybrid_kv_cache_manager.md
[...]
111: ### Case 3: same `kv_hidden_size` and no regular pattern
112: 
113: Unfortunately, not all models have such a beautiful ratio, and approach in Case 2 will produce too many small groups. For example, Gemma-3-27b has 52 sliding window attention layers and 10 full attention layers. With the constraints in case 2, it would be 26 sliding window groups and 5 full attention groups, each contains 2 layers. The allocation is still inefficient. To reduce the number of kv cache groups, we group layers using the smallest layer count among all attention types. For example, min(52, 10)=10 layers per group in Gemma-3-27b. Then the grouping result is:
114: 
115: - Group 0: 10 full attention layers (full.0 - full.9)

## vllm/docs/design/mm_processing.md
[...]
95: | `qwen3-vl`                 | `Qwen3VLForConditionalGeneration`          | `Qwen/Qwen3-VL-4B-Instruct`, etc.                     |
96: | `qwen3-vl-moe`             | `Qwen3VLMoeForConditionalGeneration`       | `Qwen/Qwen3-VL-30B-A3B-Instruct`, etc.                |
97: | `qwen3.5`                  | `Qwen3_5ForConditionalGeneration`          | `Qwen/Qwen3.5-0.8B`, etc.                             |
98: | `qwen3.5-moe`              | `Qwen3_5MoeForConditionalGeneration`       | `Qwen/Qwen3.5-35B-A3B`, etc.                          |
99: | `qwen4-exp`                | `Qwen4ExpForConditionalGeneration`         | `Qwen/Qwen3.8-Flash-Next`                             |
100: 
101: #### Key Properties and Gains

## vllm/docs/features/batch_invariance.md
[...]
125: 
126: - **DeepSeek series**: `deepseek-ai/DeepSeek-V3`, `deepseek-ai/DeepSeek-V3-0324`, `deepseek-ai/DeepSeek-R1`, `deepseek-ai/DeepSeek-V3.1`
127: - **Qwen3 (Dense)**: `Qwen/Qwen3-1.7B`, `Qwen/Qwen3-8B`, `Qwen/Qwen3-4B-AWQ`, `Qwen/Qwen3-8B-AWQ`
128: - **Qwen3-VL (Vision-Language)**: `Qwen/Qwen3-VL-2B-Instruct`, `Qwen/Qwen3-VL-4B-Instruct` (single image and video inputs)
129: - **Qwen3 (MoE)**: `Qwen/Qwen3-30B-A3B`, `Qwen/Qwen3-Next-80B-A3B-Instruct`, `Qwen/Qwen3-30B-A3B-Thinking-2507-FP8`

## vllm/docs/features/quantization/fp8_vit_attn.md
[...]
10: !!! note
11:     - Currently supports Qwen3-VL family models only (`qwen3_vl`, `qwen3_vl_moe`,
12:       `qwen3_5`, `qwen3_5_moe`, and other models using Qwen3 ViT).
13:     - Dynamic scaling is not compatible with ViT full CUDA graphs.
14:     - Performance gains are mostly visible at QHD/4K resolutions or multi-image

## vllm/docs/features/quantization/inc.md
[...]
71: 
72: ```bash
73: vllm serve Intel/DeepSeek-R1-0528-Qwen3-8B-int4-AutoRound \
74:     --gpu-memory-utilization 0.8 \
75:     --max-model-len 4096
[...]
80: ```bash
81: lm_eval --model vllm \
82:   --model_args pretrained="Intel/DeepSeek-R1-0528-Qwen3-8B-int4-AutoRound,max_model_len=8192,max_num_batched_tokens=32768,max_num_seqs=128,gpu_memory_utilization=0.8,dtype=bfloat16,max_gen_toks=2048" \
83:   --tasks gsm8k \
84:   --num_fewshot 5 \

## vllm/docs/features/quantization/online.md
[...]
27: # MXFP4 MOE-only weight and activation quantization
28: llm = LLM(
29:     "Qwen/Qwen3.5-35B-A3B",
30:     quantization="mxfp4",
31:     quantization_config={"linear": {"activation": None, "weight": None}}
[...]
41: vllm serve meta-llama/Llama-3.1-8B --quantization mxfp4
42: 
43: vllm serve Qwen/Qwen3.5-35B-A3B --quantization mxfp4 \
44:     --quantization-config '{"linear":{"activation":null,"weight":null}}'
45: ```
[...]
149: 
150: ```bash
151: vllm serve amd/Qwen3.5-35B-A3B-MXFP4 \
152:   --quantization-config.linear mxfp8
153: ```
[...]
226: 
227: llm = LLM(
228:     "Qwen/Qwen3.5-35B-A3B",
229:     quantization="online",
230:     quantization_config={
[...]
244: 
245: ```bash
246: vllm serve Qwen/Qwen3.5-35B-A3B \
247:   --quantization online \
248:   --quantization-config '{"targets":{"model.layers.0.self_attn.o_proj":"fp8_per_tensor","re:.*self_attn\\.qkv_proj.*":"mxfp8","*mlp.experts*":"mxfp4"}}'

## vllm/docs/features/quantization/quark.md
[...]
303: - amd/Llama-2-70b-chat-hf-WMXFP4FP8-AMXFP4FP8-AMP-KVFP8
304: - amd/Mixtral-8x7B-Instruct-v0.1-WMXFP4FP8-AMXFP4FP8-AMP-KVFP8
305: - amd/Qwen3-8B-WMXFP4FP8-AMXFP4FP8-AMP-KVFP8
306: 
307: ### 2. inference the quantized mixed precision model in vLLM
[...]
374: ONLINE_QUANT_CONFIG='{"online_quant_config": {"global_quant_config": "ptpc_fp8", "exclude_layer": ["lm_head"]}}'
375: 
376: vllm serve Qwen/Qwen3-8B \
377:   --trust-remote-code \
378:   --tensor-parallel-size 1 \

## vllm/docs/features/reasoning_outputs.md
[...]
222: 
223: ```bash
224: vllm serve Qwen/Qwen3-8B \
225:     --reasoning-parser qwen3 \
226:     --default-chat-template-kwargs '{"enable_thinking": false}'

## vllm/docs/features/sleep_mode.md
[...]
112: 
113: ```bash
114: VLLM_SERVER_DEV_MODE=1 vllm serve Qwen/Qwen3.8-27B --enable-sleep-mode \
115:     --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
116:     --sleep-preserve-parameter-names 'draft.*'
[...]
144: 
145: ```python
146: llm = LLM("Qwen/Qwen3-8B", enable_sleep_mode=True, sleep_mode_offload_cudagraph=True)
147: ```
148: 
[...]
165: 
166: ```python
167: llm = LLM("Qwen/Qwen3-8B", enable_sleep_mode=True, enable_nccl_comm_suspend=True)
168: ```
169: 

## vllm/docs/features/speculative_decoding/README.md
[...]
165: 
166:   llm = LLM(
167:       model="Qwen/Qwen3-8B",
168:       speculative_config={                               
169:           "method": "draft_model",

## vllm/docs/features/speculative_decoding/draft_model.md
[...]
10: 
11: llm = LLM(
12:     model="Qwen/Qwen3-8B",
13:     tensor_parallel_size=1,
14:     speculative_config={
[...]
88: 
89:   llm = LLM(
90:       model="Qwen/Qwen3-8B",
91:       speculative_config={                               
92:           "method": "draft_model",

## vllm/docs/features/speculative_decoding/extract_hidden_states.md
[...]
19: with tempfile.TemporaryDirectory() as tmpdir:
20:     llm = LLM(
21:         model="Qwen/Qwen3-8B",
22:         speculative_config={
23:             "method": "extract_hidden_states",
[...]
57: 
58: ```bash
59: vllm serve Qwen/Qwen3-8B \
60:     --speculative_config '{"method": "extract_hidden_states", "num_speculative_tokens": 1, "draft_model_config": {"hf_config": {"eagle_aux_hidden_state_layer_ids": [1, 2, 3, 4]}}}' \
61:     --kv_transfer_config '{"kv_connector": "ExampleHiddenStatesConnector", "kv_role": "kv_producer", "kv_connector_extra_config": {"shared_storage_path": "/dev/shm/hidden_states"}}'
[...]
93: ```json
94: {
95:     "model": "Qwen/Qwen3-8B",
96:     "messages": [{"role": "user", "content": "Hello"}],
97:     "max_tokens": 32,

## vllm/docs/features/speculative_decoding/n_gram.md
[...]
11: 
12: llm = LLM(
13:     model="Qwen/Qwen3-8B",
14:     tensor_parallel_size=1,
15:     speculative_config={

## vllm/docs/features/speculative_decoding/parallel_draft_model.md
[...]
12: 
13: llm = LLM(
14:     model="Qwen/Qwen3-8B",
15:     tensor_parallel_size=1,
16:     speculative_config={

## vllm/docs/features/speculative_decoding/suffix.md
[...]
20: 
21: llm = LLM(
22:     model="Qwen/Qwen3-8B",
23:     tensor_parallel_size=1,
24:     speculative_config={

## vllm/docs/models/hardware_supported_models/cpu.md
[...]
51: | Qwen/Qwen3-1.7B | Qwen3ForCausalLM | ✅ | [Xeon 6](https://recipes.vllm.ai/Qwen/Qwen3-1.7B?hardware=xeon6) |
52: | Qwen/Qwen3-4B | Qwen3ForCausalLM | ✅ | [Xeon 6](https://recipes.vllm.ai/Qwen/Qwen3-4B?hardware=xeon6) |
53: | Qwen/Qwen3-8B | Qwen3ForCausalLM | ✅ | [Xeon 6](https://recipes.vllm.ai/Qwen/Qwen3-8B?hardware=xeon6) |
54: | Qwen/Qwen3-14B | Qwen3ForCausalLM | ✅ | [Xeon 6](https://recipes.vllm.ai/Qwen/Qwen3-14B?hardware=xeon6) |
55: | Qwen/Qwen3-14B-FP8 | Qwen3ForCausalLM | ✅ | [Xeon 6](https://recipes.vllm.ai/Qwen/Qwen3-14B?hardware=xeon6&variant=fp8) |

## vllm/docs/models/hardware_supported_models/xpu.md
[...]
58: | Qwen/Qwen2.5-VL-32B-Instruct  | Qwen2VLForConditionalGeneration      | BF16/Online FP8 |
59: | Qwen/Qwen3-VL-32B-Instruct    | Qwen3VLForConditionalGeneration      | BF16/Online FP8 |
60: | Qwen/Qwen3.5-35B-A3B          | Qwen3_5MoeForConditionalGeneration   | BF16/Online FP8 |
61: | google/gemma-3-27b-it         | Gemma3ForConditionalGeneration       | BF16/Online FP8 |
62: | google/gemma-4-31B-it         | Gemma4ForConditionalGeneration       | BF16/Online FP8 |
63: | google/gemma-4-26B-A4B-it     | Gemma4ForConditionalGeneration       | BF16/Online FP8 |

## vllm/docs/models/pooling_models/specific_models.md
[...]
80: | - | - | - |
81: | `ColQwen3` | Qwen3-VL | `TomoroAI/tomoro-colqwen3-embed-4b`, `TomoroAI/tomoro-colqwen3-embed-8b` |
82: | `OpsColQwen3Model` | Qwen3-VL | `OpenSearch-AI/Ops-Colqwen3-4B`, `OpenSearch-AI/Ops-Colqwen3-8B` |
83: | `Qwen3VLNemotronEmbedModel` | Qwen3-VL | `nvidia/nemotron-colembed-vl-4b-v2`, `nvidia/nemotron-colembed-vl-8b-v2` |
84: 
[...]
197: - Reranking (text + multi-modal): [examples/pooling/score/colqwen3_rerank_online.py](../../../examples/pooling/score/colqwen3_rerank_online.py)
198: 
199: ## ColQwen3.5 Multi-Modal Late Interaction Models
200: 
201: ColQwen3.5 is based on [ColPali](https://arxiv.org/abs/2407.01449), extending ColBERT's late interaction approach to **multi-modal** inputs. It uses the Qwen3.5 hybrid backbone (linear + full attention) and produces per-token L2-normalized vectors for MaxSim scoring.
202: 
203: | Architecture | Backbone | Example HF Models |
204: | - | - | - |
205: | `ColQwen3_5` | Qwen3.5 | `athrael-soju/colqwen3.5-4.5B` |
206: 
207: Start the server:
208: 
209: ```shell
210: vllm serve athrael-soju/colqwen3.5-4.5B --max-model-len 4096
211: ```
212: 
[...]
215: ```shell
216: curl -s http://localhost:8000/rerank -H "Content-Type: application/json" -d '{
217:     "model": "athrael-soju/colqwen3.5-4.5B",
218:     "query": "What is machine learning?",
219:     "documents": [
[...]
229: ```shell
230: curl -s http://localhost:8000/score -H "Content-Type: application/json" -d '{
231:     "model": "athrael-soju/colqwen3.5-4.5B",
232:     "text_1": "What is the capital of France?",
233:     "text_2": ["The capital of France is Paris.", "Python is a programming language."]
[...]
235: ```
236: 
237: An example can be found here: [examples/pooling/score/colqwen3_5_rerank_online.py](../../../examples/pooling/score/colqwen3_5_rerank_online.py)
238: 
239: ## Llama Nemotron Multimodal

## vllm/docs/models/pooling_models/token_embed.md
[...]
62: | `ColPaliForRetrieval` | ColPali | T / I | `vidore/colpali-v1.3-hf` | | |
63: | `ColQwen3` | Qwen3-VL | T / I | `TomoroAI/tomoro-colqwen3-embed-4b`, `TomoroAI/tomoro-colqwen3-embed-8b` | | |
64: | `ColQwen3_5` | ColQwen3.5 | T + I + V | `athrael-soju/colqwen3.5-4.5B-v3`, `vultr/VultronRetrieverPrime-Qwen3.5-8B` | | |
65: | `OpsColQwen3Model` | Qwen3-VL | T / I | `OpenSearch-AI/Ops-Colqwen3-4B`, `OpenSearch-AI/Ops-Colqwen3-8B` | | |
66: | `Qwen3VLNemotronEmbedModel` | Qwen3-VL | T / I | `nvidia/nemotron-colembed-vl-4b-v2`, `nvidia/nemotron-colembed-vl-8b-v2` | ✅︎ | ✅︎ |
67: | `*ForConditionalGeneration`<sup>C</sup>, `*ForCausalLM`<sup>C</sup>, etc. | Generative models | \* | N/A | \* | \* |

## vllm/docs/models/supported_models.md
[...]
400: | `FalconH1ForCausalLM` | Falcon-H1 | `tiiuae/Falcon-H1-34B-Base`, `tiiuae/Falcon-H1-34B-Instruct`, etc. | ✅︎ | ✅︎ |
401: | `GemmaForCausalLM` | Gemma | `google/gemma-2b`, `google/gemma-1.1-2b-it`, etc. | ✅︎ | ✅︎ |
402: | `Gemma2ForCausalLM` | Gemma 2 | `google/gemma-2-9b`, `google/gemma-2-27b`, etc. | ✅︎ | ✅︎ |
403: | `Gemma3ForCausalLM` | Gemma 3 | `google/gemma-3-1b-it`, etc. | ✅︎ | ✅︎ |
404: | `Gemma3nForCausalLM` | Gemma 3n | `google/gemma-3n-E2B-it`, `google/gemma-3n-E4B-it`, etc. | | |
[...]
459: | `Qwen2ForCausalLM` | QwQ, Qwen2 | `Qwen/QwQ-32B-Preview`, `Qwen/Qwen2-7B-Instruct`, `Qwen/Qwen2-7B`, etc. | ✅︎ | ✅︎ |
460: | `Qwen2MoeForCausalLM` | Qwen2MoE | `Qwen/Qwen1.5-MoE-A2.7B`, `Qwen/Qwen1.5-MoE-A2.7B-Chat`, etc. | ✅︎ | ✅︎ |
461: | `Qwen3ForCausalLM` | Qwen3 | `Qwen/Qwen3-8B`, etc. | ✅︎ | ✅︎ |
462: | `Qwen3MoeForCausalLM` | Qwen3MoE | `Qwen/Qwen3-30B-A3B`, etc. | ✅︎ | ✅︎ |
463: | `Qwen3NextForCausalLM` | Qwen3NextMoE | `Qwen/Qwen3-Next-80B-A3B-Instruct`, etc. | ✅︎ | ✅︎ |
[...]
554: | `Ernie4_5_VLMoeForConditionalGeneration` | Ernie4.5-VL | T + I<sup>+</sup>/ V<sup>+</sup> | `baidu/ERNIE-4.5-VL-28B-A3B-PT`, `baidu/ERNIE-4.5-VL-424B-A47B-PT` | | ✅︎ |
555: | `Exaone4_5_ForConditionalGeneration` | EXAONE-4.5 | T + I<sup>E+</sup> | `LGAI-EXAONE/EXAONE-4.5-33B`, etc. | ✅︎ | ✅︎ |
556: | `Gemma3ForConditionalGeneration` | Gemma 3 | T + I<sup>E+</sup> | `google/gemma-3-4b-it`, `google/gemma-3-27b-it`, etc. | ✅︎ | ✅︎ |
557: | `Gemma3nForConditionalGeneration` | Gemma 3n | T + I + A | `google/gemma-3n-E2B-it`, `google/gemma-3n-E4B-it`, etc. | | |
558: | `Gemma4ForConditionalGeneration` | Gemma 4 | T + I<sup>+</sup> + V + A<sup>*</sup> | `google/gemma-4-E2B-it`, etc. | ✅︎ | ✅︎ |
[...]
624: | `Qwen2_5_VLForConditionalGeneration` <sup>Q</sup> | Qwen2.5-VL | T + I<sup>E+</sup> + V<sup>E+</sup> | `Qwen/Qwen2.5-VL-3B-Instruct`, `Qwen/Qwen2.5-VL-72B-Instruct`, etc. | ✅︎ | ✅︎ |
625: | `Qwen2_5OmniThinkerForConditionalGeneration` | Qwen2.5-Omni | T + I<sup>E+</sup> + V<sup>E+</sup> + A<sup>+</sup> | `Qwen/Qwen2.5-Omni-3B`, `Qwen/Qwen2.5-Omni-7B` | ✅︎ | ✅︎ |
626: | `Qwen3_5ForConditionalGeneration` | Qwen3.5 | T + I<sup>E+</sup> + V<sup>E+</sup> | `Qwen/Qwen3.5-9B-Instruct`, etc. | ✅︎ | ✅︎ |
627: | `Qwen3_5MoeForConditionalGeneration` | Qwen3.5-MOE | T + I<sup>E+</sup> + V<sup>E+</sup> | `Qwen/Qwen3.5-35B-A3B-Instruct`, etc. | ✅︎ | ✅︎ |
628: | `Qwen3VLForConditionalGeneration` <sup>Q</sup> | Qwen3-VL | T + I<sup>E+</sup> + V<sup>E+</sup> | `Qwen/Qwen3-VL-4B-Instruct`, etc. | ✅︎ | ✅︎ |
629: | `Qwen3VLMoeForConditionalGeneration` <sup>Q</sup> | Qwen3-VL-MOE | T + I<sup>E+</sup> + V<sup>E+</sup> | `Qwen/Qwen3-VL-30B-A3B-Instruct`, etc. | ✅︎ | ✅︎ |

## vllm/docs/serving/integrations/codex.md
[...]
25: ## Starting the vLLM Server
26: 
27: Start vLLM with a tool-calling capable model - here's an example using `Qwen/Qwen3-27B`:
28: 
29: ```bash
30: vllm serve Qwen/Qwen3.6-27B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder
31: 
32: ```

## vllm/docs/serving/online_serving/structured_decisions.md
[...]
133: ## Clef-Flash
134: 
135: [Clef-Flash](https://huggingface.co/Cloudflare/clef-flash) uses a Qwen3.5-9B
136: backbone and a joint schema head to score all questions in one forward pass.
137: vLLM detects the head and serves the checkpoint as a pooling model.
[...]
150:   A schema that exceeds this bound returns 400.
151: - `images` and `videos` are placed before the state. Videos are sampled at
152:   2 fps and processed by the Qwen3.5 vision processor. Audio inputs return
153:   400, and video soundtracks are ignored.
154: - Each request performs one pooling read. `usage.input_tokens` counts the

## vllm/examples/features/openai_batch/README.md
[...]
70: ```bash
71: cat results.jsonl
72: {"id":"vllm-383d1c59835645aeb2e07d004d62a826","custom_id":"request-1","response":{"id":"cmpl-61c020e54b964d5a98fa7527bfcdd378","object":"chat.completion","created":1715633336,"model":"meta-llama/Meta-Llama-3-8B-Instruct","choices":[{"index":0,"message":{"role":"assistant","content":"Hello! It's great to meet you! I'm here to help with any questions or tasks you may have. What's on your mind today?"},"logprobs":null,"finish_reason":"stop","stop_reason":null}],"usage":{"prompt_tokens":25,"total_tokens":56,"completion_tokens":31}},"error":null}
73: {"id":"vllm-42e3d09b14b04568afa3f1797751a267","custom_id":"request-2","response":{"id":"cmpl-f44d049f6b3a42d4b2d7850bb1e31bcc","object":"chat.completion","created":1715633336,"model":"meta-llama/Meta-Llama-3-8B-Instruct","choices":[{"index":0,"message":{"role":"assistant","content":"*silence*"},"logprobs":null,"finish_reason":"stop","stop_reason":null}],"usage":{"prompt_tokens":27,"total_tokens":32,"completion_tokens":5}},"error":null}
74: ```

## vllm/tests/evals/qwen4_exp/README.md
[...]
1: # Qwen4Exp accuracy evaluation
2: 
3: This suite starts a Qwen3.8-Flash-Next-FP8 OpenAI-compatible server once and
4: uses EvalScope to evaluate GSM8K and AIME25.
5: 

## vllm-ascend/.agents/skills/vllm-ascend-model-adapter/references/deliverables.md
[...]
19:    - optional eager fallback command
20:    - optional `TORCHDYNAMO_DISABLE=1` fallback command (if relevant)
21: 4. Test config YAML at `tests/e2e/models/configs/<ModelName>.yaml` — must include `model_name`, `hardware`, `tasks` with accuracy metrics (name + value), and `num_fewshot`. Use accuracy results from evaluation to populate metric values. Follow the schema of existing configs (e.g. `Qwen3-8B.yaml`).
22: 5. Tutorial doc at `docs/source/tutorials/models/<ModelName>.md` — must follow the standard template: Introduction, Supported Features, Environment Preparation (with docker tabs for A2/A3), Deployment (with serve script), Functional Verification (with curl example), Accuracy Evaluation, Performance. Fill in model-specific details (HF path, hardware requirements, TP size, max-model-len, served-model-name, sample curl, accuracy table).
23: 6. Post SKILL.md content or AI-assisted workflow summary as a comment on the originating GitHub issue.

## vllm-ascend/.agents/skills/vllm-ascend-model-adapter/references/workflow-checklist.md
[...]
240: - Generate `tests/e2e/models/configs/<ModelName>.yaml` using accuracy results from evaluation.
241: - Must include: `model_name` (HF path), `hardware` (e.g. "Atlas A2 Series"), `tasks` (list with `name` and `metrics` containing `name` + `value`), `num_fewshot`.
242: - Follow the schema of existing configs (e.g. `Qwen3-8B.yaml`).
243: 
244: ### Tutorial doc generation

## vllm-ascend/.agents/skills/vllm-ascend-release/SKILL.md
[...]
679: 🆕 Qwen VL模型支持`w8a8_mxfp8`量化
680: 🚀 Triton算子重编译优化，提升算子性能
681: 🚀 Qwen3.5/Qwen3-Next GDN prefill路径优化，预构建chunk metadata减少h2d同步开销
682: 🚀 FIA prefill context merge路径简化，提升运行时效率
683: 🐞 TorchNPU 和 triton-ascend 依赖版本更新，请参考官方release note

## vllm-ascend/benchmarks/README.md
[...]
13:     - Output length: 128 tokens.
14:     - Batch size: fixed (8).
15:     - Models: Qwen2.5-7B-Instruct, Qwen3-8B.
16:     - Evaluation metrics: end-to-end latency (mean, median, p99).
17: 
[...]
20:     - Output length: the corresponding output length of these 200 prompts.
21:     - Batch size: dynamically determined by vllm to achieve maximum throughput.
22:     - Models: Qwen2.5-VL-7B-Instruct, Qwen2.5-7B-Instruct, Qwen3-8B.
23:     - Evaluation metrics: throughput.
24: - Serving tests
[...]
27:     - Batch size: dynamically determined by vllm and the arrival pattern of the requests.
28:     - **Average QPS (query per second)**: 1, 4, 16 and inf. QPS = inf means all requests come at once. For other QPS values, the arrival time of each query is determined using a random Poisson process (with fixed random seed).
29:     - Models: Qwen2.5-VL-7B-Instruct, Qwen2.5-7B-Instruct, Qwen3-8B.
30:     - Evaluation metrics: throughput, TTFT (time to the first token, with mean, median and p99), ITL (inter-token latency, with mean, median and p99).
31: 

## vllm-ascend/benchmarks/scripts/perf_result_template.md
[...]
5: - Batch size: dynamically determined by vllm and the arrival pattern of the requests.
6: - **Average QPS (query per second)**: 1, 4, 16 and inf. QPS = inf means all requests come at once. For other QPS values, the arrival time of each query is determined using a random Poisson process (with fixed random seed).
7: - Models: Qwen/Qwen3-8B, Qwen/Qwen2.5-VL-7B-Instruct
8: - Evaluation metrics: throughput, TTFT (median time to the first token ), ITL (median inter-token latency) TPOT(median time per output token).
9: 
[...]
17: - Output length: 128 tokens.
18: - Batch size: fixed (8).
19: - Models: Qwen/Qwen3-8B, Qwen/Qwen2.5-VL-7B-Instruct
20: - Evaluation metrics: end-to-end latency.
21: 
[...]
27: - Output length: the corresponding output length of these 200 prompts.
28: - Batch size: dynamically determined by vllm to achieve maximum throughput.
29: - Models: Qwen/Qwen3-8B, Qwen/Qwen2.5-VL-7B-Instruct
30: - Evaluation metrics: throughput.
31: 

## vllm-ascend/docs/source/_templates/feature_template.md
[...]
90: | Deployment Scenario | Supports PD disaggregated deployment, does not support PD co-location |
91: | Engine | Only supports vLLM (only applicable to MindIE products) |
92: | Model | Verified Qwen3-8B, Qwen3-30B-A3B, DeepSeek-V3.1-W8A8 |
93: | Feature Mutual Exclusion | Does not support simultaneous use with xx feature |
94: | Software Dependencies | CANN >= 8.5.0, HDK >= 25.5, Mooncake >= 0.3.11.post1 |
[...]
135: 
136: ```bash
137: vllm serve Qwen/Qwen3-8B \
138:   --additional-config '{"xxx_config": {"enabled": true}}'
139: ```
[...]
151: 
152: llm = LLM(
153:     model="Qwen/Qwen3-8B",
154:     additional_config={
155:         "xxx_config": {

## vllm-ascend/docs/source/_templates/feature_template_zh.md
[...]
90: | 部署场景 | 支持 PD 分离部署，不支持 PD 混部 |
91: | 引擎 | 仅支持 vLLM（仅 MindIE 产品涉及此项） |
92: | 模型 | 已验证 Qwen3-8B、Qwen3-30B-A3B、DeepSeek-V3.1-W8A8 |
93: | 特性互斥 | 不支持与 xx 特性同时使用 |
94: | 软件依赖 | CANN >= 8.5.0、HDK >= 25.5、Mooncake >= 0.3.11.post1 |
[...]
135: 
136: ```bash
137: vllm serve Qwen/Qwen3-8B \
138:   --additional-config '{"xxx_config": {"enabled": true}}'
139: ```
[...]
151: 
152: llm = LLM(
153:     model="Qwen/Qwen3-8B",
154:     additional_config={
155:         "xxx_config": {

## vllm-ascend/docs/source/community/contributors.md
[...]
54: | 562 | [@Thiagor2002](https://github.com/Thiagor2002) | 2026/08/31 | [75133ed](https://github.com/vllm-project/vllm-ascend/commit/75133ed739e1ea62e4bc6ef8c76ec5b7963bc278) |
55: | 561 | [@hotTea123](https://github.com/hotTea123) | 2026/08/29 | [d2f6d37](https://github.com/vllm-project/vllm-ascend/commit/d2f6d37a81a533a4f12b40f0eddb731b2e096a45) |
56: | 560 | [@chenzhh69](https://github.com/chenzhh69) | 2026/08/28 | [e20c2b0](https://github.com/vllm-project/vllm-ascend/commit/e20c2b061fa72cc581b6513cbc3e2995527b934f) |
57: | 559 | [@lsjfy-open-com](https://github.com/lsjfy-open-com) | 2026/08/28 | [3827486](https://github.com/vllm-project/vllm-ascend/commit/3827486f19db928809af401ea0121ca7d487448f) |
58: | 558 | [@Abstrey](https://github.com/Abstrey) | 2026/08/28 | [6b52b11](https://github.com/vllm-project/vllm-ascend/commit/6b52b112e63109e124abd75dc2f67edb769874b6) |
[...]
197: | 419 | [@Biuapha](https://github.com/Biuapha) | 2026/06/01 | [c50023e](https://github.com/vllm-project/vllm-ascend/commit/c50023e347505badaa1c72d8f123d87a70be8d14) |
198: | 418 | [@vladimirevmenoff](https://github.com/vladimirevmenoff) | 2026/05/30 | [928fa1d](https://github.com/vllm-project/vllm-ascend/commit/928fa1d862a99230e3cfc69c394dcb8a01c334be) |
199: | 417 | [@ningjingbengxiaohai](https://github.com/ningjingbengxiaohai) | 2026/05/30 | [2a77209](https://github.com/vllm-project/vllm-ascend/commit/2a77209accf9a49845716cf79d4227bb9237ef32) |
200: | 416 | [@xszbuaa](https://github.com/xszbuaa) | 2026/05/29 | [3d0fafd](https://github.com/vllm-project/vllm-ascend/commit/3d0fafda9a0e46ad275ca2e062936d658f9d319a) |
201: | 415 | [@ZRICHARD9527](https://github.com/ZRICHARD9527) | 2026/05/28 | [7372661](https://github.com/vllm-project/vllm-ascend/commit/737266135913650ca27e6a9726492e99764d225d) |
[...]
355: | 261 | [@wjunLu](https://github.com/wjunLu) | 2025/12/25 | [fca2f94](https://github.com/vllm-project/vllm-ascend/commit/fca2f948c101c9d520f1a381a6b705d9e11c042e) |
356: | 260 | [@cookieyyds](https://github.com/cookieyyds) | 2025/12/25 | [2da8038](https://github.com/vllm-project/vllm-ascend/commit/2da8038dd2d30f813c00b37ba2cd9abeaaf3d0f3) |
357: | 259 | [@chenaoxuan](https://github.com/chenaoxuan) | 2025/12/25 | [6d25372](https://github.com/vllm-project/vllm-ascend/commit/6d25372baaa0ef018a75b427b387fab8dd2e92b4) |
358: | 258 | [@changdawei1](https://github.com/changdawei1) | 2025/12/25 | [a9fccbe](https://github.com/vllm-project/vllm-ascend/commit/a9fccbeb300fd4753f8e54aaddf02abf59d7429c) |
359: | 257 | [@TmacAaron](https://github.com/TmacAaron) | 2025/12/24 | [5018f2d](https://github.com/vllm-project/vllm-ascend/commit/5018f2d8fd6dc11240900e38049150619895570d) |
[...]
395: | 221 | [@h1074112368](https://github.com/h1074112368) | 2025/12/06 | [7403399](https://github.com/vllm-project/vllm-ascend/commit/74033999ed98fcf02db0a2512d019177d0843791) |
396: | 220 | [@GuoRen868](https://github.com/GuoRen868) | 2025/12/06 | [4bd1030](https://github.com/vllm-project/vllm-ascend/commit/4bd1030842a3831109ccfb136056459cd83c1441) |
397: | 219 | [@AlvisGong](https://github.com/AlvisGong) | 2025/12/06 | [a5163c8](https://github.com/vllm-project/vllm-ascend/commit/a5163c8c369e046c53e6127bbbcee23392cec069) |
398: | 218 | [@MingYang119](https://github.com/MingYang119) | 2025/12/03 | [18b90b5](https://github.com/vllm-project/vllm-ascend/commit/18b90b501d6aad1d9426dcdee1ccfbe8139dd47d) |
399: | 217 | [@amy-why-3459](https://github.com/amy-why-3459) | 2025/12/03 | [26e8e58](https://github.com/vllm-project/vllm-ascend/commit/26e8e58cea8ba5cc5edaef19e72d0ddc4e9f1c1c) |
[...]
435: | 181 | [@wlf-darkmatter](https://github.com/wlf-darkmatter) | 2025/10/23 | [097173e](https://github.com/vllm-project/vllm-ascend/commit/097173e50fc9efe2bf4e46bf7d59b8f5e06f2679) |
436: | 180 | [@HuaJiaHeng](https://github.com/HuaJiaHeng) | 2025/10/23 | [062257f](https://github.com/vllm-project/vllm-ascend/commit/062257f624486d15315013b624ce71e1a388ee20) |
437: | 179 | [@destinysky](https://github.com/destinysky) | 2025/10/23 | [427b17e](https://github.com/vllm-project/vllm-ascend/commit/427b17e2da1d6d967e7581b40b6bd169cdb324c8) |
438: | 178 | [@KyrieDrewWang](https://github.com/KyrieDrewWang) | 2025/10/22 | [60e2be1](https://github.com/vllm-project/vllm-ascend/commit/60e2be1b366975f7183c38cd158da811969b9230) |
439: | 177 | [@HF-001](https://github.com/HF-001) | 2025/10/22 | [bc30874](https://github.com/vllm-project/vllm-ascend/commit/bc30874f8b6212ff8eb45b2546c360660c49c9c1) |
[...]
538: | 78 | [@weiguihua2](https://github.com/weiguihua2) | 2025/06/23 | [e112317](https://github.com/vllm-project/vllm-ascend/commit/e1123172d12afa15f306ba6e1e4c9d0c6d1d799e) |
539: | 77 | [@lyj-jjj](https://github.com/lyj-jjj) | 2025/06/23 | [5177bef](https://github.com/vllm-project/vllm-ascend/commit/5177bef87a21331dcca11159d3d1438075cbd74e) |
540: | 76 | [@zhoux77899](https://github.com/zhoux77899) | 2025/06/21 | [a927bee](https://github.com/vllm-project/vllm-ascend/commit/a927bee4f098e7b95a255a064c95adea73ee2a50) |
541: | 75 | [@yuancaoyaoHW](https://github.com/yuancaoyaoHW) | 2025/06/20 | [00ae250](https://github.com/vllm-project/vllm-ascend/commit/00ae250f3ced68317bc91c93dc1f1a0977aa0b94) |
542: | 74 | [@shikang-hangzhou](https://github.com/shikang-hangzhou) | 2025/06/20 | [f1353d5](https://github.com/vllm-project/vllm-ascend/commit/f1353d51b32ddf22444b0608b3d7f60fed048ac4) |
[...]
581: | 35 | [@paulyu12](https://github.com/paulyu12) | 2025/04/17 | [697908f](https://github.com/vllm-project/vllm-ascend/commit/697908f5cd7c65a3a917ec1a962b0886efc98c7e) |
582: | 34 | [@eeethenQ](https://github.com/eeethenQ) | 2025/04/15 | [44a8301](https://github.com/vllm-project/vllm-ascend/commit/44a8301424ded94dae83e13b837f5bfc0a1bfc15) |
583: | 33 | [@wxsIcey](https://github.com/wxsIcey) | 2025/04/10 | [d05ea17](https://github.com/vllm-project/vllm-ascend/commit/d05ea17427b82a506b97409a7de8359f18f565f7) |
584: | 32 | [@yx0716](https://github.com/yx0716) | 2025/04/08 | [5d62393](https://github.com/vllm-project/vllm-ascend/commit/5d6239306be9b0f5ac6dbaa137048c372a92ff20) |
585: | 31 | [@antonlisq](https://github.com/antonlisq) | 2025/04/07 | [2b765dc](https://github.com/vllm-project/vllm-ascend/commit/2b765dcc4974b1bafc26ff5da817ce7e652f0eb0) |

## vllm-ascend/docs/source/community/slash-commands.md
[...]
61: **Common test case names (A2):**
62: 
63: `test_custom_op`, `test_custom_op_multi_card`, `qwen3-vl-32b-instruct-w8a8`, `qwen3-32b-int8`, `MiniMax-M2.5-w8a8-QuaRot-A2`, `Qwen3.5-27B-w8a8-A2`, `Qwen3.5-397B-A17B-w4a8-mtp`, `accuracy-group`
64: 
65: **Common test case names (A3):**

## vllm-ascend/docs/source/developer_guide/contribution/doc_writing.md
[...]
77: ```yaml
78: test_cases:
79:   - name: qwen3-8b-single
80:     model: Qwen/Qwen3-8B
81:     envs:
82:       HCCL_BUFFSIZE: "1024"
[...]
102: ````md
103: ```model-code
104: :block_name: qwen3_8b_single_node
105: :converter_tag: single_node
106: :test_case_path: tests/e2e/nightly/single_node/models/configs/your_model.yaml
[...]
119: export SERVER_PORT=8000
120: 
121: vllm serve Qwen/Qwen3-8B \
122:   --tensor-parallel-size 1 \
123:   --port $SERVER_PORT \

## vllm-ascend/docs/source/developer_guide/contribution/nightly_ci_test.md
[...]
132: | `qwen3-vl-32b-instruct-w8a8` | Qwen3-VL-32B-Instruct W8A8 |
133: | `qwen3-32b-int8` | Qwen3-32B INT8 quantization |
134: | `Qwen3.5-27B-w8a8-A2` | Qwen3.5-27B W8A8 |
135: | `Qwen3.5-397B-A17B-w4a8-mtp` | Qwen3.5-397B-A17B W4A8 + MTP |
136: 
137: **Multi-node tests** (`a2.multi_node.test_config`):
[...]
147: | Test name | Description | Scope |
148: |-----------|-------------|-------|
149: | `accuracy-group-1` | Qwen3-VL-8B, Qwen3-8B, Qwen2-Audio-7B, etc. | nightly |
150: | `accuracy-group-2` | ERNIE-4.5, Molmo-7B, Llama-3.2-3B, etc. | nightly |
151: | `accuracy-group-3` | Qwen3-30B-A3B, Qwen3-VL-30B-A3B, etc. | nightly |
[...]
182: | `deepseek-r1-0528-w8a8-prefix-cache` | DeepSeek-R1-0528-W8A8 prefix cache |
183: | `kimi-k2.5` | Kimi-K2.5 |
184: | `Qwen3.5-397B-A17B-w8a8-mtp` | Qwen3.5-397B-A17B W8A8 + MTP |
185: | `Qwen3.5-27B-w8a8-A3` | Qwen3.5-27B W8A8 |
186: | `Qwen3.5-122B-A10B-W8A8-A3` | Qwen3.5-122B-A10B W8A8 |
187: | `DeepSeek-V4-Flash-W8A8-A3` | DeepSeek-V4-Flash W8A8 |
188: 
[...]
235: 
236: ```text
237: /nightly accuracy-group-1/Qwen3-8B
238: ```
239: 

## vllm-ascend/docs/source/developer_guide/performance_and_debug/performance_benchmark.md
[...]
117: ```bash
118: export VLLM_USE_MODELSCOPE=True
119: vllm serve Qwen/Qwen3-8B
120: ```
121: 
[...]
128: vllm bench serve \
129:   --backend vllm \
130:   --model Qwen/Qwen3-8B \
131:   --endpoint /v1/completions \
132:   --dataset-name sharegpt \
[...]
147:       --endpoint /v1/completions \
148:       --backend vllm \
149:       --model Qwen/Qwen3-8B \
150:       --dataset-name sharegpt \
151:       --dataset-path <your data path>/ShareGPT_V3_unfiltered_cleaned_split.json \
[...]
187: export VLLM_USE_MODELSCOPE=True
188: vllm bench throughput \
189:   --model Qwen/Qwen3-8B \
190:   --dataset-name random \
191:   --input-len 128 \

## vllm-ascend/docs/source/tutorials/features/pd_disaggregation_mooncake_multi_node.md
[...]
430:     - The launcher validates only argument types and required options. Check the remaining constraints before deployment.
431:     - If speculative decoding is enabled, `num_speculative_tokens` should be subject to one of the following conditions:
432:         1. Hybrid Mamba models (e.g., Qwen-Next and Qwen3.5 series): `num_speculative_tokens` should be equal on P nodes and D nodes.
433:         2. Other models: `num_speculative_tokens` on P nodes should be 1, and `num_speculative_tokens` on D nodes should be greater or equal to 1.
434: 

## vllm-ascend/docs/source/tutorials/models/Qwen3-Dense.md
[...]
28: | Qwen3-1.7B | 1 Atlas A3 inference products (64GB × 16), 1 Atlas A2 inference products (64GB × 8) | [Modelers](https://modelers.cn/models/Modelers_Park/Qwen3-1.7B) |
29: | Qwen3-4B | 1 Atlas A3 inference products (64GB × 16), 1 Atlas A2 inference products (64GB × 8) | [Modelers](https://modelers.cn/models/Modelers_Park/Qwen3-4B) |
30: | Qwen3-8B | 1 Atlas A3 inference products (64GB × 16), 1 Atlas A2 inference products (64GB × 8) | [Modelers](https://modelers.cn/models/Modelers_Park/Qwen3-8B) |
31: | Qwen3-14B | 1 Atlas A3 inference products (64GB × 16), 1 Atlas A2 inference products (64GB × 8) | [Modelers](https://modelers.cn/models/Modelers_Park/Qwen3-14B) |
32: | Qwen3-32B | 1 Atlas A3 inference products (64GB × 16), 1 Atlas A2 inference products (64GB × 8) | [Modelers](https://modelers.cn/models/Modelers_Park/Qwen3-32B) |
[...]
43: | Model | Quantization | Hardware Requirement | Download |
44: |-------|-------------|---------------------|----------|
45: | Qwen3-8B-W8A8SC | W8A8SC | Atlas 300I DUO (TP1) | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3-8B-w8a8sc-310-vllm) |
46: | Qwen3-14B-W8A8SC | W8A8SC | Atlas 300I DUO (TP1) | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3-14B-w8a8sc-310-vllm) |
47: | Qwen3-32B-W8A8SC | W8A8SC | Atlas 300I DUO (TP4) | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3-32B-w8a8sc-310-vllm) |
[...]
270: === "Atlas 300I DUO"
271: 
272:     Qwen3-8B-W8A8SC:
273: 
274:     ```bash
[...]
277: 
278:     # Ensure the model path matches the directory recorded during download
279:     vllm serve Eco-Tech/Qwen3-8B-w8a8sc-310-vllm/TP1/Qwen3-8B-w8a8sc-310-vllm-tp1 \
280:         --host 127.0.0.1 \
281:         --port 8080 \

## vllm-ascend/docs/source/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.md
[...]
1: # Qwen3.5-27B & Qwen3.6-27B
2: 
3: ## 1 Introduction
[...]
9:     **For the production environment on the customer side, [MindIE Motor](https://www.hiascend.com/document/detail/en/mindie/latest/quickstart/docs/en/user_guide/quick_start.md) + vLLM-Ascend is recommended.**
10: 
11: Qwen3.5-27B and Qwen3.6-27B are dense hybrid Mamba-Transformer language models in the Qwen3.5/Qwen3.6 family, integrating breakthroughs in architectural efficiency, reinforcement learning scale, and global accessibility. They share the same hybrid attention design (GDN + full attention), so deployment on Ascend NPUs follows the same pattern for both models. They are suitable for general-purpose text generation tasks such as dialogue, content creation, and code generation running on Ascend NPUs.
12: 
13: This document will demonstrate the main validation steps for the models, including supported features, feature configuration, environment preparation, single-node and multi-node deployment, as well as accuracy and performance evaluation.
14: 
15: It is **strongly recommended to use the latest release candidate (rc) version or the latest official version** of `vllm-ascend`. As a minimum-version requirement, `Qwen3.5-27B` is first supported in `vllm-ascend:v0.17.0rc1`, and `Qwen3.6-27B` is first supported in `vllm-ascend:v0.18.0rc1`. Support for Atlas 300I DUO and 950DT Products starts from `vllm-ascend:v0.23.0rc1`.
16: 
17: ## 2 Supported Features
[...]
27: |  Weight Version | Hardware Requirements | Download Links |
28: |-----------------|-----------------------|----------------|
29: | `Qwen3.5-27B` (BF16 version) | 1 Atlas 800 A3 (64GB × 16) node or 1 Atlas 800 A2 (64GB × 8) node or Atlas 300I DUO | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.5-27B) \| [Hugging Face](https://huggingface.co/Qwen/Qwen3.5-27B) |
30: | `Qwen3.5-27B-w8a8` (Quantized version) | 1 Atlas 800 A3 (64GB × 16) node or 1 Atlas 800 A2 (64GB × 8) node or Atlas 300I DUO | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.5-27B-w8a8-mtp) |
31: | `Qwen3.6-27B` (BF16 version) | 1 950DT Products(96GB × 8) node or 1 Atlas 800 A3 (64GB × 16) node or 1 Atlas 800 A2 (64GB × 8) node or Atlas 300I DUO | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.6-27B) \| [Hugging Face](https://huggingface.co/Qwen/Qwen3.6-27B) |
32: | `Qwen3.6-27B-w8a8` (Quantized version) | 1 Atlas 800 A3 (64GB × 16) node or 1 Atlas 800 A2 (64GB × 8) node | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.6-27B-w8a8) |
33: | `Qwen3.6-27B-w8a8-mxfp8` (Quantized version) | 1 950DT Products (96GB × 8) node | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.6-27B-w8a8-mxfp8) |
34: | `Qwen3.6-27B-w8a8-310p`(Quantized version) | 1 Atlas 300I DUO | [ModelScope](https://modelscope.cn/models/Eco-Tech/Qwen3.6-27B-W8A8-310P) |
35: 
36: It is recommended to download the model weight to the shared directory of multiple nodes, such as `/root/.cache/`.
[...]
48: Select an image based on your machine type and start the docker image on your node, refer to [using docker](../../getting_started/installation.md#installation-prebuilt-image).
49: 
50: It is **recommended to use the latest release candidate (rc) version or the latest official version** of the `vllm-ascend` image to ensure the best compatibility and access to the latest features. As a minimum-version requirement, use `vllm-ascend:v0.17.0rc1` (or a later version) for `Qwen3.5-27B`, and `vllm-ascend:v0.18.0rc1` (or a later version) for `Qwen3.6-27B`. For `Qwen3.6-27B` on Atlas 800 A3, please use the matching `v0.18.0rc1-a3` (or a later `-a3`) image. For Atlas 300I DUO, use `vllm-ascend:v0.23.0rc1-310p` (or a later `-310p`) image.
51: 
52: === "A3 series"
[...]
225: ### 5.1 Single-Node Online Deployment
226: 
227: Single-node deployment completes both Prefill and Decode within the same node, suitable for development, testing, and medium-scale inference scenarios. The `Qwen3.5-27B`, `Qwen3.5-27B-w8a8`, `Qwen3.6-27B`, and `Qwen3.6-27B-w8a8` models can all be deployed on 1 Atlas 800 A3 (64GB × 16), 1 Atlas 800 A2 (64GB × 8). On Atlas 300I DUO, at least 2 devices are required. The `Qwen3.6-27B`, and `Qwen3.6-27B-w8a8-mxfp8` models can all be deployed on 1 950DT Products (96GB × 8). The quantized versions need to start with the `--quantization ascend` parameter.
228: 
229: Both `Qwen3.5-27B` and `Qwen3.6-27B` share the same MTP head design, so the `qwen3_5_mtp` speculative decoding method can be used for both.
230: 
231: === "Atlas 800 A3 / Atlas 800 A2"
[...]
233:     The following examples are for Atlas 800 A3 / Atlas 800 A2. Quantized versions need `--quantization ascend`.
234: 
235:     === "Qwen3.5-27B-w8a8"
236: 
237:         Startup Command:
[...]
240:         #!/bin/sh
241:         # Load model from ModelScope to speed up download
242:         export MODEL_PATH=Eco-Tech/Qwen3.5-27B-w8a8-mtp
243:         export VLLM_USE_MODELSCOPE=True
244:         export HCCL_BUFFSIZE=512
[...]
247:         # Size of the shared buffer (in MB) used by HCCL for NPU-to-NPU collective communication
248: 
249:         # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.5-27B-w8a8-mtp) or a local directory path
250:         # Ensure the model path matches the directory recorded during download
251: 
[...]
257:             --seed 1024 \
258:             --quantization ascend \
259:             --served-model-name qwen3.5 \
260:             --max-num-seqs 32 \
261:             --max-model-len 133000 \
[...]
264:             --gpu-memory-utilization 0.90 \
265:             --no-enable-prefix-caching \
266:             --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
267:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
268:             --additional-config '{"enable_cpu_binding":true}'
269:         ```
270: 
271:     === "Qwen3.6-27B-w8a8"
272: 
273:         Startup Command:
[...]
276:         #!/bin/sh
277:         # Load model from ModelScope to speed up download
278:         export MODEL_PATH=Eco-Tech/Qwen3.6-27B-w8a8
279:         export VLLM_USE_MODELSCOPE=True
280:         export HCCL_BUFFSIZE=512
[...]
283:         # Size of the shared buffer (in MB) used by HCCL for NPU-to-NPU collective communication
284: 
285:         # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.6-27B-w8a8) or a local directory path
286:         # Ensure the model path matches the directory recorded during download
287: 
[...]
300:             --gpu-memory-utilization 0.90 \
301:             --no-enable-prefix-caching \
302:             --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
303:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
304:             --additional-config '{"enable_cpu_binding":true}'
[...]
308: 
309:     - `--data-parallel-size 1` and `--tensor-parallel-size 2` are common settings for data parallelism (DP) and tensor parallelism (TP) sizes.
310:     - `--max-model-len` represents the context length, which is the maximum value of the input plus output for a single request. The Qwen3.6-27B model supports up to 262144.
311:     - `--max-num-seqs` indicates the maximum number of requests that each DP group is allowed to process. If the number of requests sent to the service exceeds this limit, the excess requests will remain in a waiting state and will not be scheduled. Note that the time spent in the waiting state is also counted in metrics such as TTFT and TPOT. Therefore, when testing performance, it is generally recommended that `--max-num-seqs` * `--data-parallel-size` >= the actual total concurrency.
312:     - `--max-num-batched-tokens` represents the maximum number of tokens that the model can process in a single step. Currently, vLLM v1 scheduling enables ChunkPrefill/SplitFuse by default, which means:
[...]
317:     - `--no-enable-prefix-caching` disables prefix caching in the example above. For workloads with long shared prefixes, finer-grained hybrid prefix matching can be enabled with `--enable-prefix-caching --prefix-match-unit 16`. The match unit must divide every KV cache group's block size. A smaller unit can reuse more of a partial physical page, at the cost of additional hash metadata, copy-on-write operations, and an extra prefill split at the final matching boundary.
318:     - `--quantization ascend` indicates that quantization is used. To disable quantization, remove this option.
319:     - `--speculative-config` uses `qwen3_5_mtp` for both `Qwen3.5-27B` and `Qwen3.6-27B` because they share the same MTP head design.
320:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
321:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
326:     Currently only the **TP** scenario is supported. Choose **TP=2** or **TP=4** according to the available devices. Replace `MODEL_PATH` with a ModelScope model id or a local directory path.The quantized versions need to start with the `--quantization ascend` parameter.
327: 
328:     === "Qwen3.5-27B-w8a8"
329: 
330:         Startup Command:
[...]
333:         #!/bin/sh
334:         # Load model from ModelScope to speed up download
335:         export MODEL_PATH=Eco-Tech/Qwen3.5-27B-w8a8-mtp
336:         export VLLM_USE_MODELSCOPE=True
337: 
338:         # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.5-27B-w8a8-mtp) or a local directory path
339:         # Ensure the model path matches the directory recorded during download
340: 
[...]
343:             --port 8000 \
344:             --tensor-parallel-size 4 \
345:             --served-model-name qwen3.5 \
346:             --max-num-seqs 128 \
347:             --max-model-len 16384 \
348:             --trust-remote-code \
349:             --gpu-memory-utilization 0.90 \
350:             --mamba-ssm-cache-dtype float16 \
351:             --dtype float16 \
352:             --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}' \
353:             --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}' \
354:             --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
355:         ```
356: 
357:     === "Qwen3.6-27B-w8a8"
358: 
359:         Startup Command:
[...]
362:         #!/bin/sh
363:         # Load model from ModelScope to speed up download
364:         export MODEL_PATH=Eco-Tech/Qwen3.6-27B-w8a8-310p
365:         export VLLM_USE_MODELSCOPE=True
366: 
367:         # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.6-27B-w8a8) or a local directory path
368:         # Ensure the model path matches the directory recorded during download
369: 
[...]
377:             --trust-remote-code \
378:             --gpu-memory-utilization 0.90 \
379:             --mamba-ssm-cache-dtype float16 \
380:             --dtype float16 \
381:             --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}' \
382:             --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}' \
383:             --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
[...]
387: 
388:     - `--tensor-parallel-size` sets the tensor parallel size. Choose **TP=2** or **TP=4** according to the available devices.
389:     - `--max-model-len` represents the context length, which is the maximum value of the input plus output for a single request. Configure it based on the actual workload and available memory; The Qwen3.6-27B model supports up to 262144.
390:     - `--max-num-seqs` indicates the maximum number of concurrent requests. Configure it as needed—setting it too high may cause OOM.
391:     - `--gpu-memory-utilization` represents the proportion of HBM that vLLM will use for actual inference. Configure this value according to the actual device memory; setting it too high may cause OOM. The default value is `0.9`.
392:     - `--mamba-ssm-cache-dtype` sets the data type of the Mamba SSM cache. On Atlas 300I DUO, only `float16` is supported.
393:     - `--dtype float16` must be set on Atlas 300I DUO. These devices only support the FP16 data type.
394:     - `--speculative-config` uses `qwen3_5_mtp` for both `Qwen3.5-27B` and `Qwen3.6-27B` because they share the same MTP head design. On Atlas 300I DUO, it is recommended to set `num_speculative_tokens` to `1`.
395:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
396:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
402:     The following example is for 950DT Products. Quantized versions need `--quantization ascend`.
403: 
404:     === "Qwen3.6-27B-w8a8-mxfp8"
405: 
406:         Startup Command:
[...]
409:         #!/bin/sh
410:         # Load model from ModelScope to speed up download
411:         export MODEL_PATH=Eco-Tech/Qwen3.6-27B-w8a8-mxfp8
412:         export VLLM_USE_MODELSCOPE=True
413:         export HCCL_BUFFSIZE=512
[...]
416:         # Size of the shared buffer (in MB) used by HCCL for NPU-to-NPU collective communication
417: 
418:         # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.6-27B-w8a8-mxfp8) or a local directory path
419:         # Ensure the model path matches the directory recorded during download
420: 
[...]
433:             --gpu-memory-utilization 0.90 \
434:             --no-enable-prefix-caching \
435:             --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
436:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
437:             --additional-config '{"enable_cpu_binding":true}'
[...]
441: 
442:     - `--data-parallel-size 1` and `--tensor-parallel-size 1` are common settings for data parallelism (DP) and tensor parallelism (TP) sizes.
443:     - `--max-model-len` represents the context length, which is the maximum value of the input plus output for a single request. The Qwen3.6-27B model supports up to 262144.
444:     - `--max-num-seqs` indicates the maximum number of requests that each DP group is allowed to process. If the number of requests sent to the service exceeds this limit, the excess requests will remain in a waiting state and will not be scheduled. Note that the time spent in the waiting state is also counted in metrics such as TTFT and TPOT. Therefore, when testing performance, it is generally recommended that `--max-num-seqs` * `--data-parallel-size` >= the actual total concurrency.
445:     - `--max-num-batched-tokens` represents the maximum number of tokens that the model can process in a single step. Currently, vLLM v1 scheduling enables ChunkPrefill/SplitFuse by default, which means:
[...]
448:         - Generally, if `--max-num-batched-tokens` is set to a larger value, the overall latency will be lower, but the pressure on HBM memory (activation value usage) will be greater.
449:     - `--gpu-memory-utilization` represents the proportion of HBM that vLLM will use for actual inference. Its essential function is to calculate the available kv_cache size. During the warm-up phase (referred to as profile run in vLLM), vLLM records the peak HBM memory usage during an inference process with an input size of `--max-num-batched-tokens`. The available kv_cache size is then calculated as: `--gpu-memory-utilization` * HBM size - peak HBM memory usage. Therefore, the larger the value of `--gpu-memory-utilization`, the more kv_cache can be used. However, since the HBM memory usage during the warm-up phase may differ from that during actual inference (e.g., due to uneven EP load), setting `--gpu-memory-utilization` too high may lead to OOM (Out of Memory) issues during actual inference. The default value is `0.9`.
450:     - `--no-enable-prefix-caching` indicates that prefix caching is disabled. The current implementation of hybrid kv cache for Qwen3.6-27B may result in a very large effective `block_size` when prefix caching is enabled (e.g., 2048), which means any prefix shorter than `block_size` will never be cached. If your workload has many short repeated prefixes, consider keeping prefix caching disabled. For related issues, see the [Public FAQs](../../faqs.md).
451:     - `--quantization ascend` indicates that quantization is used. To disable quantization, remove this option.
452:     - `--speculative-config` uses `qwen3_5_mtp` for `Qwen3.6-27B` because it shares the same MTP head design as `Qwen3.5-27B`.
453:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
454:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
487: - **Decode nodes** focus on low-latency token generation, optimized for memory bandwidth (e.g., enabling full-decode aclgraph).
488: 
489: For `Qwen3.5-27B-w8a8` and `Qwen3.6-27B-w8a8`, a typical **1P1D** configuration requires **2 Atlas 800 A3 (64GB × 16) nodes** (1 Prefill node + 1 Decode node), with **TP=2** and **DP=8** on each node, which fully utilizes all 16 NPUs of an Atlas A3. The example below uses `Qwen3.5-27B-w8a8`; for `Qwen3.6-27B-w8a8`, replace the model path with `Eco-Tech/Qwen3.6-27B-w8a8` and adjust `--served-model-name` to `qwen3.6` (and `--max-model-len` to 262144 if needed).
490: 
491: > **Why TP=2 + DP=8 (DP-first strategy)?** The `Qwen3.5-27B-w8a8` (and `Qwen3.6-27B-w8a8`) model is only ~30 GB, which easily fits in a single NPU (each NPU has 64 GB HBM). **TP > 1 is mainly needed for models that do not fit in one NPU.** For a 27 B model, `TP=2` is sufficient to balance operator-dispatch overhead across NPUs, while **maximizing DP** keeps all 16 NPUs of an Atlas A3 busy with independent request batches, fully utilizing the hardware. This **DP-first parallelism strategy** is the standard practice for small dense models (e.g., Qwen3.5-27B, Qwen3.6-27B, Llama-3-8B) and has been validated by the [Qwen3.5-27B B200 benchmark](https://thenextgentechinsider.com/pulse/qwen-35-27b-delivers-11m-tokenssecond-on-nvidia-b200-cluster), where switching from TP=8 to DP=8 lifted per-node throughput from 9.5k to 95k tokens/s.
492: >
493: > **Note**: Since `Qwen3.5-27B` and `Qwen3.6-27B` fit in a single node, multi-node PD separation is only recommended for high-concurrency production deployments. For the Mooncake deployment specifics, please refer to the [Mooncake Multi-Node PD Disaggregation Guide](../features/pd_disaggregation_mooncake_multi_node.md).
494: 
495: To run the vllm-ascend Prefill-Decode Disaggregation service, you need to:
[...]
530: 
531:     # Ensure the model path matches the directory recorded during download
532:     vllm serve Eco-Tech/Qwen3.5-27B-w8a8-mtp \
533:       --host 0.0.0.0 \
534:       --port $2 \
[...]
540:       --seed 1024 \
541:       --quantization ascend \
542:       --served-model-name qwen3.5 \
543:       --trust-remote-code \
544:       --max-num-seqs 4 \
[...]
548:       --gpu-memory-utilization 0.95 \
549:       --enforce-eager \
550:       --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
551:       --additional-config '{"enable_cpu_binding":true}' \
552:       --kv-transfer-config \
[...]
585: 
586:     # Ensure the model path matches the directory recorded during download
587:     vllm serve Eco-Tech/Qwen3.5-27B-w8a8-mtp \
588:       --host 0.0.0.0 \
589:       --port $2 \
[...]
595:       --seed 1024 \
596:       --quantization ascend \
597:       --served-model-name qwen3.5 \
598:       --trust-remote-code \
599:       --max-num-seqs 16 \
[...]
604:       --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
605:       --additional-config '{"recompute_scheduler_enable":true,"enable_cpu_binding":true}' \
606:       --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
607:       --kv-transfer-config \
608:       '{"kv_connector": "MooncakeConnectorV1",
[...]
679:     -H "Content-Type: application/json" \
680:     -d '{
681:         "model": "qwen3.5",
682:         "messages": [
683:             {"role": "user", "content": "The future of AI is"}
[...]
689: ```
690: 
691: > **Note**: For `Qwen3.6-27B-w8a8`, change the `model` field above to `"qwen3.6"` and the `--served-model-name` of the Prefill/Decode nodes to `qwen3.6`.
692: 
693: Expected Result: The proxy returns HTTP 200 OK. The JSON response contains the `choices` field with the generated text, confirming that Prefill nodes have successfully processed the prompt and Decode nodes have generated the response.
[...]
697: ## 6 Functional Verification
698: 
699: After the service is started, the model can be invoked by sending a prompt. Two API interfaces are supported: `completions` and `chat.completions`. Use the `--served-model-name` you configured (`qwen3.5` for `Qwen3.5-27B` or `qwen3.6` for `Qwen3.6-27B`).
700: 
701: **Completions API:**
[...]
705:     -H "Content-Type: application/json" \
706:     -d '{
707:         "model": "qwen3.5",
708:         "prompt": "The future of AI is",
709:         "max_tokens": 50,
[...]
712: ```
713: 
714: > **Note**: For `Qwen3.6-27B`, set `"model": "qwen3.6"` in the request body.
715: 
716: **Chat Completions API:**
[...]
720:     -H "Content-Type: application/json" \
721:     -d '{
722:         "model": "qwen3.5",
723:         "messages": [
724:             {"role": "user", "content": "The future of AI is"}
[...]
730: ```
731: 
732: > **Note**: For `Qwen3.6-27B`, set `"model": "qwen3.6"` in the request body.
733: 
734: Expected Result: The service returns HTTP 200 OK. The JSON response contains the `choices` field with generated text. Example output for the completions API (content truncated for brevity):
[...]
739:     "object": "text_completion",
740:     "created": 1780971952,
741:     "model": "qwen3.5",
742:     "choices": [
743:         {
[...]
764: 1. Refer to [Using AISBench](../../developer_guide/evaluation/using_ais_bench.md) for details.
765: 
766: 2. After execution, you can get the result. Here is the result of `Qwen3.5-27B-w8a8` in `vllm-ascend:v0.17.0rc1` for reference only. The accuracy result of `Qwen3.6-27B-w8a8` can be obtained in the same way and is not listed here.
767: 
768: **Accuracy Evaluation Config File:**
[...]
779:         abbr="vllm-api-general-chat",
780:         path="your_model_path",
781:         model="qwen3.5",
782:         request_rate=0,
783:         retry=2,
[...]
801: ```
802: 
803: > For `Qwen3.6-27B-w8a8`, change `model` to `qwen3.6` and `path` to the corresponding model weight path.
804: 
805: | dataset | version | metric | mode | vllm-api-general-chat |
[...]
809: ### 7.2 Using Language Model Evaluation Harness
810: 
811: Using the `gsm8k` dataset as an example test dataset, run the accuracy evaluation for `Qwen3.5-27B-w8a8` in online mode.
812: 
813: 1. For `lm_eval` installation, please refer to [Using lm_eval](../../developer_guide/evaluation/using_lm_eval.md).
[...]
815: 
816: ```shell
817: # For Qwen3.5-27B-w8a8
818: export VLLM_USE_MODELSCOPE=True
819: vllm serve Eco-Tech/Qwen3.5-27B-w8a8-mtp \
820:     --served-model-name qwen3.5 \
821:     --trust-remote-code \
822:     --quantization ascend \
[...]
830: lm_eval \
831:   --model local-completions \
832:   --model_args model=qwen3.5,base_url=http://127.0.0.1:8000/v1/completions,tokenized_requests=False,trust_remote_code=True \
833:   --tasks gsm8k \
834:   --output_path ./
[...]
843: ### 8.2 Using vLLM Benchmark
844: 
845: Run performance evaluation of `Qwen3.5-27B-w8a8` or `Qwen3.6-27B-w8a8` as an example.
846: 
847: Refer to [vllm benchmark](https://docs.vllm.ai/en/latest/benchmarking/) for more details.
[...]
857: ```bash
858: export VLLM_USE_MODELSCOPE=True
859: # For Qwen3.5-27B-w8a8:
860: vllm bench serve --model Eco-Tech/Qwen3.5-27B-w8a8-mtp --dataset-name random --random-input 200 --num-prompts 200 --request-rate 1 --save-result --result-dir ./
861: # For Qwen3.6-27B-w8a8:
862: vllm bench serve --model Eco-Tech/Qwen3.6-27B-w8a8 --dataset-name random --random-input 200 --num-prompts 200 --request-rate 1 --save-result --result-dir ./
863: ```
864: 
[...]
871: > **Note**: The following configurations are validated in specific test environments and are for reference only. The optimal configuration depends on factors such as maximum input/output length, prefix cache hit rate, precision requirements, and deployment machine ratios. It is recommended to refer to [Section 9.2](#92-tuning-guidelines) for tuning based on actual conditions.
872: >
873: > **Parallelism Strategy**: `Qwen3.5-27B-w8a8` and `Qwen3.6-27B-w8a8` are only ~30 GB and easily fit in a single NPU (64 GB HBM per NPU). Following the **DP-first** principle, **TP=2 is the recommended default** for most scenarios, and the remaining NPUs should be allocated to DP for parallel request batches. **TP=8 is only recommended for ultra-long context (256k+) scenarios**, where it shards the KV cache across 8 NPUs to maximize the available context window per rank. For `Qwen3.6-27B-w8a8`, you can also raise `--max-model-len` up to 262144 in the same TP/DP layout.
874: >
875: > **Atlas 300I DUO**: Currently only the TP scenario is supported. Choose **TP=2** or **TP=4** according to the available devices. With **TP=4**, `--max-model-len` can support **128k** and **256k** long-sequence scenarios; configure `--max-num-seqs` as needed—setting it too high may cause OOM.
876: >
877: > **950DT Products**: The `Qwen3.6-27B-w8a8-mxfp8` model weight easily fits in a single NPU (96 GB HBM per NPU). Following the **DP-first** principle, **TP=1 is the recommended default** for most scenarios, and the remaining NPUs should be allocated to DP for parallel request batches. For `Qwen3.6-27B-w8a8-mxfp8`, `--max-model-len` can support up to **262144** in the same TP=1 + DP=8 layout.
878: 
879: #### Table 1: Scenario Overview
[...]
881: | Scenario | Deployment Mode | *Total NPUs | Weight Version | Key Considerations |
882: |----------|----------------|-------------|----------------|---------------------|
883: | High Throughput<br>(128k context) | Single-Node (A2) | 8 (A2) | Qwen3.5-27B-w8a8 / Qwen3.6-27B-w8a8 | TP=2 + DP=4 fully utilizes all 8 NPUs for parallel request batches |
884: | High Throughput<br>(128k context) | Single-Node (A3) | 16 (A3) | Qwen3.5-27B-w8a8 / Qwen3.6-27B-w8a8 | TP=2 + DP=8 fully utilizes all 16 NPUs for parallel request batches |
885: | Low Latency<br>(128k context) | Single-Node (A3) | 16 (A3) | Qwen3.5-27B-w8a8 / Qwen3.6-27B-w8a8 | TP=2 + DP=8 reduces per-layer Allreduce overhead for small interactive batches |
886: | Long Context<br>(256k+ context) | Single-Node (A3) | 16 (A3) | Qwen3.5-27B-w8a8 / Qwen3.6-27B-w8a8 | TP=8 + DP=2 shards the KV cache across 8 NPUs to maximize the available context window |
887: | High Throughput<br>(128k context) | Single-Node (950DT Products) | 8 (950DT Products) | Qwen3.6-27B-w8a8-mxfp8 | TP=1 + DP=8 fully utilizes all 8 NPUs for parallel request batches |
888: | Long Context<br>(256k+ context) | Single-Node (950DT Products) | 8 (950DT Products) | Qwen3.6-27B-w8a8-mxfp8 | TP=1 + DP=8 maximizes the available context window while keeping all 8 NPUs busy |
889: 
890: > `*Total NPUs` indicates the total number of NPUs used across all nodes. 1 Atlas 800 A3 node = 16 NPUs, 1 Atlas 800 A2 node = 8 NPUs, 1 950DT Products node = 8 NPUs.

## vllm-ascend/docs/source/tutorials/models/Qwen3.5-397B-A17B.md
[...]
1: # Qwen3.5-397B-A17B
2: 
3: ## 1 Introduction
[...]
9:     **For the production environment on the customer side, [MindIE Motor](https://www.hiascend.com/document/detail/en/mindie/latest/quickstart/docs/en/user_guide/quick_start.md) + vLLM-Ascend is recommended.**
10: 
11: Qwen3.5-397B-A17B is a large-scale Qwen3.5 MoE model that combines multimodal capability, long-context inference, MTP speculative decoding, and W8A8 quantized deployment for production serving on Ascend hardware.
12: 
13: This document describes the main validation steps for the model, including supported features, prerequisites, installation, single-node online deployment, multi-node deployment, Prefill-Decode (PD) disaggregation, functional verification, accuracy and performance evaluation, performance tuning, and FAQs.
14: 
15: The `Qwen3.5-397B-A17B` model is first supported in `vllm-ascend:v0.17.0rc1`. Use `v0.17.0rc1` or later for this model. For Ascend95DT, the model is supported from `vllm-ascend:v0.23.0rc1`. The examples below use the version placeholder configured by the documentation build system.
16: 
17: ## 2 Supported Features
[...]
31: |  Weight Version | Hardware Requirements | Download Links |
32: |-----------------|-----------------------|----------------|
33: | `Qwen3.5-397B-A17B` (BF16 version) | 2 950DT Products(96GB x 8) nodes or 2 Atlas 800 A3 (64GB x 16) nodes or 4 Atlas 800 A2 (64GB x 8) nodes | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.5-397B-A17B) |
34: | `Qwen3.5-397B-A17B-w8a8` (quantized version) | 1 Atlas 800 A3 (64GB x 16) node or 2 Atlas 800 A2 (64GB x 8) nodes | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp) |
35: | `Qwen3.5-397B-A17B-w4a8` (quantized version) | 1 Atlas 800 A3 (64GB x 16) node or 2 Atlas 800 A2 (64GB x 8) nodes | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.5-397B-A17B-w4a8-mtp) |
36: | `Qwen3.5-397B-A17B-w8a8-mxfp8` (quantized version) | 1 950DT Products(96GB x 8) node | [ModelScope](https://modelscope.cn/models/Eco-Tech/Qwen3.5-397B-A17B-w8a8-mxfp8) |
37: | `Qwen3.5-397B-A17B-w4a4-mxfp4` (quantized version) | 1 950DT Products(96GB x 8) node | [ModelScope](https://modelscope.cn/models/Eco-Tech/Qwen3.5-397B-A17B-w4a4-mxfp4) |
38: 
39: It is recommended to download the model weight to a shared directory across multiple nodes, such as `/root/.cache/`, so that all serving nodes can load the same path.
[...]
51: Select an image based on your machine type and start the docker image on your node, refer to [using docker](../../getting_started/installation.md#installation-prebuilt-image).
52: 
53: The `Qwen3.5-397B-A17B` model is first supported in `vllm-ascend:v0.17.0rc1`. Use `v0.17.0rc1` or later for this model.For Ascend95DT, the model is supported from `vllm-ascend:v0.23.0rc1`.
54: 
55: === "950DT Products"
[...]
186: === "950DT Products"
187: 
188:     Run the following script to execute online inference on 1 950DT Products (96G x 8). The quantized versions (`Qwen3.5-397B-A17B-w8a8-mxfp8` and `Qwen3.5-397B-A17B-w4a4-mxfp4`) can be deployed on a single 950DT Products node, needs `--quantization ascend`.
189: 
190:     ```shell
[...]
202: 
203:     # Ensure the model path matches the directory recorded during download
204:     vllm serve Eco-Tech/Qwen3.5-397B-A17B-w4a4-mxfp4 \
205:       --host 0.0.0.0 \
206:       --port 8000 \
[...]
211:       --seed 1024 \
212:       --quantization ascend \
213:       --served-model-name qwen3.5 \
214:       --max-num-seqs 128 \
215:       --max-model-len 133000 \
[...]
219:       --gpu-memory-utilization 0.95 \
220:       --async-scheduling \
221:       --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3}' \
222:       --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
223:       --additional-config '{"enable_cpu_binding":true}'
[...]
245:     
246:     # Ensure the model path matches the directory recorded during download
247:     vllm serve Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp \
248:       --host 0.0.0.0 \
249:       --port 8000 \
[...]
253:       --seed 1024 \
254:       --quantization ascend \
255:       --served-model-name qwen3.5 \
256:       --max-num-seqs 128 \
257:       --max-model-len 133000 \
[...]
260:       --gpu-memory-utilization 0.90 \
261:       --enable-prefix-caching \
262:       --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
263:       --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
264:       --additional-config '{"enable_cpu_binding":true, "enable_fused_mc2":1}'
[...]
279: - `--max-num-batched-tokens` is the maximum number of tokens processed in one scheduler step. A larger value can improve prefill efficiency but consumes more activation memory.
280: - `--gpu-memory-utilization` controls how much HBM vLLM can use to calculate KV cache capacity. A higher value increases KV cache size but can trigger OOM if runtime memory is higher than the profile run.
281: - `--enable-prefix-caching` enables prefix caching. For Qwen3.5, short prefixes may not be cached when the hybrid KV cache manager adjusts the block size to a large value.
282: - `--quantization ascend` enables Ascend quantization for the W8A8 model. Remove this option when deploying the BF16 model.
283: - `--speculative-config` enables Qwen3.5 MTP speculative decoding. Reduce `num_speculative_tokens` or remove this option if the workload is sensitive to first-token latency or if MTP is unstable in your environment.
284: - `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'` enables full decode ACLGraph replay to reduce dispatch overhead.
285: - `--additional-config` enables Ascend-specific optimizations. `enable_fused_mc2` enables MoE fused operators, and `enable_cpu_binding` enables Ascend-native CPU binding.
[...]
289: Multi-node MP deployment uses vLLM data parallelism across nodes and tensor parallelism within each node. It is recommended for the W8A8 model on 2 Atlas 800 A2 (64GB x 8) nodes.
290: 
291: Assume you have 2 Atlas 800 A2 nodes and want to deploy `Qwen3.5-397B-A17B-w8a8-mtp` across them. Replace `nic_name`, `local_ip`, and `node0_ip` with the actual network interface and IP addresses in your environment.
292: 
293: Run the following script on node 0.
[...]
309: 
310: # Ensure the model path matches the directory recorded during download
311: vllm serve Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp \
312:   --host 0.0.0.0 \
313:   --port 8000 \
[...]
318:   --data-parallel-rpc-port 13389 \
319:   --seed 1024 \
320:   --served-model-name qwen3.5 \
321:   --tensor-parallel-size 8 \
322:   --enable-expert-parallel \
[...]
328:   --no-enable-prefix-caching \
329:   --quantization ascend \
330:   --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3}' \
331:   --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
332:   --additional-config '{"enable_cpu_binding":true, "multistream_overlap_shared_expert": true}'
[...]
356: 
357: # Ensure the model path matches the directory recorded during download
358: vllm serve Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp \
359:   --host 0.0.0.0 \
360:   --port 8000 \
[...]
367:   --seed 1024 \
368:   --tensor-parallel-size 8 \
369:   --served-model-name qwen3.5 \
370:   --max-num-seqs 16 \
371:   --max-model-len 32768 \
[...]
376:   --no-enable-prefix-caching \
377:   --quantization ascend \
378:   --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3}' \
379:   --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
380:   --additional-config '{"enable_cpu_binding":true, "multistream_overlap_shared_expert": true}'
[...]
409: ### 5.3 Multi-Node Deployment with Ray
410: 
411: For Ray-based distributed deployment, refer to [Ray Distributed (Qwen/Qwen3-235B-A22B)](../features/ray.md). The same model weight, communication verification, and parameter tuning principles apply to Qwen3.5-397B-A17B.
412: 
413: Common Issues Tip: If Ray workers cannot discover each other, check Ray cluster status first, then verify the same HCCL and network interface settings used in MP deployment.
[...]
419: We recommend using Mooncake for deployment. Refer to [Mooncake](../features/pd_disaggregation_mooncake_multi_node.md) for the general PD disaggregation workflow.
420: 
421: For Atlas 800 A3 (64G x 16), we recommend deploying 1P1D with 2 nodes for `Qwen3.5-397B-A17B-w8a8-mtp`:
422: 
423: - 1 Prefill node: 1 Atlas 800 A3 (64G x 16).
[...]
454: 
455: # Ensure the model path matches the directory recorded during download
456: vllm serve Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp \
457:   --host ${IP_ADDRESS} \
458:   --port 30060 \
[...]
468:   --seed 1024 \
469:   --distributed-executor-backend mp \
470:   --served-model-name qwen3.5 \
471:   --max-model-len 16384 \
472:   --max-num-batched-tokens 4096 \
[...]
474:   --quantization ascend \
475:   --no-disable-hybrid-kv-cache-manager \
476:   --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
477:   --additional-config '{"enable_cpu_binding": true}' \
478:   --gpu-memory-utilization 0.9 \
[...]
525: 
526: # Ensure the model path matches the directory recorded during download
527: vllm serve Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp \
528:   --host ${IP_ADDRESS} \
529:   --port 30050 \
[...]
539:   --seed 1024 \
540:   --distributed-executor-backend mp \
541:   --served-model-name qwen3.5 \
542:   --max-model-len 16384 \
543:   --max-num-batched-tokens 128 \
[...]
545:   --quantization ascend \
546:   --no-disable-hybrid-kv-cache-manager \
547:   --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3}' \
548:   --additional-config '{"recompute_scheduler_enable": true, "enable_cpu_binding": true}' \
549:   --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
[...]
584: ### 5.5 Prefill-Decode Disaggregation (950DT Products)
585: 
586: For 950DT Products (96G x 8), we recommend deploying 1P1D with 2 nodes for `Qwen3.5-397B-A17B-w4a4-mxfp4`:
587: 
588: - 1 Prefill node: 1 950DT Products (96G x 8). Runs an independent service with DP=1, TP=8.
[...]
623: 
624: # Ensure the model path matches the directory recorded during download
625: vllm serve Eco-Tech/Qwen3.5-397B-A17B-w4a4-mxfp4 \
626:   --host 0.0.0.0 \
627:   --port 30060 \
[...]
635:   --seed 1024 \
636:   --distributed-executor-backend mp \
637:   --served-model-name qwen3.5 \
638:   --max-model-len 133000 \
639:   --max-num-batched-tokens 8192 \
[...]
644:   --async-scheduling \
645:   --enforce-eager \
646:   --speculative-config '{"num_speculative_tokens": 1, "method": "qwen3_5_mtp", "enforce_eager": true}' \
647:   --additional-config '{"enable_cpu_binding": true, "multistream_overlap_shared_expert": true, "recompute_scheduler_enable": true}' \
648:   --kv-transfer-config \
[...]
698: 
699: # Ensure the model path matches the directory recorded during download
700: vllm serve Eco-Tech/Qwen3.5-397B-A17B-w4a4-mxfp4 \
701:   --host 0.0.0.0 \
702:   --port 30050 \
[...]
711:   --seed 1024 \
712:   --distributed-executor-backend mp \
713:   --served-model-name qwen3.5 \
714:   --max-model-len 133000 \
715:   --max-num-batched-tokens 240 \
[...]
719:   --quantization ascend \
720:   --async-scheduling \
721:   --speculative-config '{"num_speculative_tokens": 3, "method": "qwen3_5_mtp"}' \
722:   --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
723:   --additional-config '{"enable_cpu_binding": true, "multistream_overlap_shared_expert": true, "recompute_scheduler_enable": true, "ascend_compilation_config": {"enable_npugraph_ex": false}}' \
[...]
799:   -H "Content-Type: application/json" \
800:   -d '{
801:     "model": "qwen3.5",
802:     "prompt": "The future of AI is",
803:     "max_tokens": 50,
[...]
815: 
816: 1. Refer to [Using AISBench](../../developer_guide/evaluation/using_ais_bench.md) for details.
817: 2. After execution, you can get the result. The following result of `Qwen3.5-397B-A17B-w8a8` on `vllm-ascend:v0.17.0rc1` is for reference only.
818: 
819: | dataset | version | metric | mode | vllm-api-general-chat |
[...]
828: lm_eval \
829:   --model local-completions \
830:   --model_args model=qwen3.5,base_url=http://127.0.0.1:8000/v1/completions,tokenized_requests=False,trust_remote_code=True \
831:   --tasks gsm8k \
832:   --output_path ./
[...]
841: ### 8.2 Using vLLM Benchmark
842: 
843: Run performance evaluation of `Qwen3.5-397B-A17B-w8a8` as an example. Refer to [vLLM benchmark](https://docs.vllm.ai/en/latest/benchmarking/) for more details.
844: 
845: There are three `vllm bench` subcommands:
[...]
855: 
856: vllm bench serve \
857:   --model Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp \
858:   --served-model-name qwen3.5 \
859:   --dataset-name random \
860:   --random-input 200 \
[...]
909: | AddRMSNormQuant fusion | Enabled by default | Fuses normalization and quantization to reduce memory access. | Applies to quantized paths. |
910: | Zero-like elimination | Enabled by default | Removes unnecessary zero-like tensor operations in attention. | No extra configuration is required. |
911: | Qwen3.5 MTP speculative decoding | `--speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}'` | Improves decode throughput when acceptance rate is good. | Reduce speculative tokens if latency or stability regresses. |
912: | Full decode ACLGraph | `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'` | Reduces operator dispatch overhead and stabilizes decode performance. | Recommended for decode-heavy serving. |
913: | Fused MC2 | `--additional-config '{"enable_fused_mc2": 1}'` | Enables MoE fused operators to improve MoE prefill/decode efficiency. | If accuracy or performance regresses in multi-DP large-token scenarios, disable it and compare. |
[...]
918: ## 10 FAQ
919: 
920: For common environment, installation, and general parameter issues, refer to [Public FAQs](../../faqs.md). This section only covers model-specific issues for Qwen3.5-397B-A17B.
921: 
922: ### Q1: Why does the service report OOM during startup or soon after accepting requests?
[...]
924: **Phenomenon:** The service fails during profile run, or it starts successfully but reports OOM when real traffic arrives.
925: 
926: **Cause:** Qwen3.5-397B-A17B has high weight and KV cache memory requirements. Large `--max-model-len`, large `--max-num-seqs`, large `--max-num-batched-tokens`, or high `--gpu-memory-utilization` can leave insufficient HBM headroom. Runtime expert load imbalance can also make real inference use more memory than the profile run.
927: 
928: **Solution:** Use the W8A8 model with `--quantization ascend` when possible, lower `--max-model-len`, lower `--max-num-seqs`, lower `--max-num-batched-tokens`, or reduce `--gpu-memory-utilization`. Keep `PYTORCH_NPU_ALLOC_CONF=expandable_segments:True`. For BF16 or larger context, use the required number of A2/A3 nodes.

## vllm-ascend/docs/source/tutorials/models/Qwen3.5-Dense.md
[...]
1: # Qwen3.5-Dense (Qwen3.5-2B/4B/9B)
2: 
3: ## 1 Introduction
4: 
5: Qwen3.5-2B, Qwen3.5-4B, and Qwen3.5-9B are dense hybrid Mamba-Transformer language models in the Qwen3.5 family. They share the same hybrid attention design (GDN + full attention) and are suitable for general-purpose text generation tasks such as dialogue, content creation, and code generation.
6: 
7: This document describes deployment and verification of these models on **Atlas 300I DUO** and **Atlas 200I Pro**, including environment preparation, Docker installation, single-node online deployment, functional verification, and tuning notes.
8: 
9: It is **strongly recommended to use the latest release candidate (rc) version or the latest official version** of `vllm-ascend`. Support for Qwen3.5-2B/4B/9B on Atlas 300I DUO and Atlas 200I Pro starts from `vllm-ascend:v0.23.0rc1`.
10: 
11: ## 2 Supported Features
[...]
21: | Model | Version | Hardware Requirement | Download |
22: |-------|---------|----------------------|----------|
23: | Qwen3.5-2B | FP16 | Atlas 300I DUO or Atlas 200I Pro | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.5-2B) |
24: | Qwen3.5-4B | FP16 | Atlas 300I DUO or Atlas 200I Pro | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.5-4B) |
25: | Qwen3.5-9B | FP16 | Atlas 300I DUO or Atlas 200I Pro | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.5-9B) |
26: | Qwen3.5-2B-W8A8-310P | INT8 | Atlas 300I DUO or Atlas 200I Pro | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.5-2B-W8A8-310P) |
27: | Qwen3.5-4B-W8A8-310P | INT8 | Atlas 300I DUO or Atlas 200I Pro | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.5-4B-W8A8-310P) |
28: | Qwen3.5-9B-W8A8-310P | INT8 | Atlas 300I DUO or Atlas 200I Pro | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.5-9B-W8A8-310P) |
29: 
30: It is recommended to download the model weight to a local directory such as `/root/.cache/` or `/home/data/`.
[...]
173: ### 5.1 Single-Node Online Deployment
174: 
175: Single-node deployment completes both Prefill and Decode within the same node. `Qwen3.5-2B`, `Qwen3.5-4B`, and `Qwen3.5-9B` can be deployed on Atlas 300I DUO or Atlas 200I Pro.
176: 
177: > **Parallelism note**: These platforms currently support the **TP** scenario. Choose **TP=1** or **TP=2** according to the available devices. On Atlas 200I Pro with a single visible NPU, use **TP=1**.
[...]
179: The following examples use FP16 weights from ModelScope. Replace `MODEL_PATH` with your local directory if needed.
180: 
181: === "Qwen3.5-2B"
182: 
183:     Startup Command:
[...]
190:     # Model weight path; can be a ModelScope model id or a local directory path
191:     # Ensure the model path matches the directory recorded during download
192:     export MODEL_PATH=Qwen/Qwen3.5-2B
193: 
194:     vllm serve $MODEL_PATH \
[...]
196:     --port 8080 \
197:     --tensor-parallel-size 1 \
198:     --served-model-name qwen3.5 \
199:     --max-num-seqs 32 \
200:     --max-model-len 16384 \
201:     --trust-remote-code \
202:     --gpu-memory-utilization 0.90 \
203:     --mamba-ssm-cache-dtype float16 \
204:     --dtype float16 \
205:     --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}' \
206:     --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}' \
207:     --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
208:     ```
209: 
210: === "Qwen3.5-4B"
211: 
212:     Startup Command:
[...]
219:     # Model weight path; can be a ModelScope model id or a local directory path
220:     # Ensure the model path matches the directory recorded during download
221:     export MODEL_PATH=Qwen/Qwen3.5-4B
222: 
223:     vllm serve $MODEL_PATH \
[...]
225:     --port 8080 \
226:     --tensor-parallel-size 1 \
227:     --served-model-name qwen3.5 \
228:     --max-num-seqs 32 \
229:     --max-model-len 16384 \
230:     --trust-remote-code \
231:     --gpu-memory-utilization 0.90 \
232:     --mamba-ssm-cache-dtype float16 \
233:     --dtype float16 \
234:     --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}' \
235:     --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}' \
236:     --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
237:     ```
238: 
239: === "Qwen3.5-9B"
240: 
241:     Startup Command:
[...]
248:     # Model weight path; can be a ModelScope model id or a local directory path
249:     # Ensure the model path matches the directory recorded during download
250:     export MODEL_PATH=Qwen/Qwen3.5-9B
251: 
252:     vllm serve $MODEL_PATH \
[...]
254:     --port 8080 \
255:     --tensor-parallel-size 1 \
256:     --served-model-name qwen3.5 \
257:     --max-num-seqs 32 \
258:     --max-model-len 16384 \
259:     --trust-remote-code \
260:     --gpu-memory-utilization 0.90 \
261:     --mamba-ssm-cache-dtype float16 \
262:     --dtype float16 \
263:     --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}' \
264:     --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}' \
265:     --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
[...]
273: - `--gpu-memory-utilization` represents the proportion of HBM that vLLM will use for actual inference. On Atlas 300I DUO and Atlas 200I Pro, configure this value according to the actual device memory; setting it too high may cause OOM. The default value is `0.9`.
274: - `--dtype float16` must be set on Atlas 300I DUO and Atlas 200I Pro. These devices only support the FP16 data type.
275: - `--mamba-ssm-cache-dtype` sets the data type of the Mamba SSM cache. On Atlas 300I DUO and Atlas 200I Pro, only `float16` is supported.
276: - `--speculative-config` uses `qwen3_5_mtp` for Qwen3.5 Dense models that include an MTP head. It is recommended to set `num_speculative_tokens` to `1`.
277: - `--compilation-config` contains configurations related to the aclgraph graph mode:
278:     - `"cudagraph_mode"`: `"FULL_DECODE_ONLY"` is recommended.
[...]
294: ## 6 Functional Verification
295: 
296: After the service is started, the model can be invoked by sending a prompt. Two API interfaces are supported: `completions` and `chat.completions`. Use the `--served-model-name` you configured (for example, `qwen3.5`). If you used `--port 8080` or `-p 8080:8080`, adjust the URL accordingly.
297: 
298: **Completions API:**
[...]
302:     -H "Content-Type: application/json" \
303:     -d '{
304:         "model": "qwen3.5",
305:         "prompt": "The future of AI is",
306:         "max_completion_tokens": 50,
[...]
315:     -H "Content-Type: application/json" \
316:     -d '{
317:         "model": "qwen3.5",
318:         "messages": [
319:             {"role": "user", "content": "The future of AI is"}
[...]
333: 1. Refer to [Using AISBench](../../developer_guide/evaluation/using_ais_bench.md) for details.
334: 
335: 2. After execution, you can get the result. Here are the accuracy results of `Qwen3.5-2B`, `Qwen3.5-4B`, and `Qwen3.5-9B` on Atlas 300I DUO for reference only.
336: 
337: **Accuracy Evaluation Config File:**
[...]
348:         abbr="vllm-api-general-chat",
349:         path="your_model_path",
350:         model="qwen3.5",
351:         request_rate=0,
352:         retry=2,
[...]
368: | Model | dataset | version | metric | mode | vllm-api-general-chat |
369: |-------|---------|---------|--------|------|------------------------|
370: | Qwen3.5-2B | gsm8k | - | accuracy | gen | 77.71 |
371: | Qwen3.5-2B | textvqa | - | accuracy | gen | 76.09 |
372: | Qwen3.5-4B | gsm8k | - | accuracy | gen | 93.18 |
373: | Qwen3.5-4B | textvqa | - | accuracy | gen | 79.08 |
374: | Qwen3.5-9B | gsm8k | - | accuracy | gen | 95.30 |
375: | Qwen3.5-9B | textvqa | - | accuracy | gen | 82.33 |
376: 
377: ## 8 Performance Evaluation

## vllm-ascend/docs/source/tutorials/models/Qwen3.6-35B-A3B.md
[...]
9:     **For the production environment on the customer side, [MindIE Motor](https://www.hiascend.com/document/detail/en/mindie/latest/quickstart/docs/en/user_guide/quick_start.md) + vLLM-Ascend is recommended.**
10: 
11: Qwen3.6-35B-A3B is a sparse MoE model in the Qwen3.6 family, with 35B total parameters and about 3B activated parameters per token. It uses the hybrid attention architecture used by Qwen3.5-style models, and is suitable for long-context online serving on Ascend hardware.
12: 
13: This document describes the main validation steps for the model, including supported features, prerequisites, installation, single-node online deployment, functional verification, accuracy and performance evaluation, performance tuning, and FAQs.
[...]
376: | Shared expert overlap | `--additional-config '{"multistream_overlap_shared_expert": true}'` | Overlaps shared expert computation in MoE workloads. | Recommended for throughput scenarios. |
377: | Prefix caching | `--enable-prefix-caching` | Improves repeated-prefix workloads. | Monitor HBM usage for long-context workloads. |
378: | Qwen3.6 MTP speculative decoding | `--speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}'` | Can improve decode throughput when stable and accepted tokens are high. | Validate stability, TTFT, TPOT, and throughput for your workload. |
379: 
380: ## 10 FAQ

## vllm-ascend/docs/source/tutorials/models/Qwen3.8-2.4T-A95B.md
[...]
1: # Qwen3.8-2.4T-A95B
2: 
3: ## 1 Introduction
[...]
9:     **For the production environment on the customer side, [MindIE Motor](https://www.hiascend.com/document/detail/en/mindie/latest/quickstart/docs/en/user_guide/quick_start.md) + vLLM-Ascend is recommended.**
10: 
11: Qwen3.8-2.4T-A95B is a large-scale MoE model with 2400 billion total
12: parameters and 95 billion activated parameters. It is built on the Qwen3.5
13: architecture and improves coding, professional work, scientific research, and
14: long-horizon agent tasks.
[...]
21: 
22: This document is validated and written based on **vLLM-Ascend 0.23.0**. The
23: current model (Qwen3.8-2.4T-A95B) is first supported in this version.
24: 
25: ## 2 Supported Features
[...]
39: |  Weight Version                 | Hardware Requirements                               | Download Links |
40: |---------------------------------|-----------------------------------------------------|----------------|
41: | `Qwen3.8-2.4T-A95B` (FP16/BF16) | approximately 4.89 TB of storage and weight memory  | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.8-2.4T-A95B) |
42: | `Qwen3.8-2.4T-A95B-w8a8`        | approximately 2.33 TiB of storage and weight memory | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-2.4T-A95B-w8a8) |
43: | `Qwen3.8-2.4T-A95B-w4a8`        | approximately 1.21 TiB of storage and weight memory | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-2.4T-A95B-w4a8) |
44: 
45: This guide includes the following validated deployment configurations:
[...]
76: 
77:     ```bash
78:     export IMAGE=quay.io/ascend/vllm-ascend:qwen3.8-a3
79:     export NAME=vllm-ascend
80: 
[...]
117: 
118:     ```bash
119:     export IMAGE=quay.io/ascend/vllm-ascend:qwen3.8-a2
120:     export NAME=vllm-ascend
121: 
[...]
194:         ```shell
195:         # Values that must be adapted to the target environment.
196:         export MODEL_PATH=<QWEN3_8_MODEL_PATH>
197:         export TOKENIZER_PATH=<QWEN3_8_TOKENIZER_PATH>
198:         export LOCAL_IP=<NODE0_LOCAL_IP>
199:         export NIC_NAME=<NODE0_NIC_NAME>
[...]
219:             --host 0.0.0.0 \
220:             --port $PORT \
221:             --served-model-name qwen3.8 \
222:             --tokenizer $TOKENIZER_PATH \
223:             --trust-remote-code \
[...]
235:             --max-num-batched-tokens 16384 \
236:             --gpu-memory-utilization 0.85 \
237:             --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":1}' \
238:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
239:             --additional-config '{"enable_cpu_binding":true,"enable_fused_mc2":1}'
[...]
247:         ```shell
248:         # Values that must be adapted to the target environment.
249:         export MODEL_PATH=<QWEN3_8_MODEL_PATH>
250:         export TOKENIZER_PATH=<QWEN3_8_TOKENIZER_PATH>
251:         export LOCAL_IP=<WORKER_LOCAL_IP>
252:         export NODE0_IP=<NODE0_LOCAL_IP>
[...]
275:             --host 0.0.0.0 \
276:             --port $PORT \
277:             --served-model-name qwen3.8 \
278:             --tokenizer $TOKENIZER_PATH \
279:             --trust-remote-code \
[...]
292:             --max-num-batched-tokens 16384 \
293:             --gpu-memory-utilization 0.85 \
294:             --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":1}' \
295:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
296:             --additional-config '{"enable_cpu_binding":true,"enable_fused_mc2":1}'
[...]
323:     | `--gpu-memory-utilization 0.85` | Reserves HBM headroom for runtime memory. |
324:     | `--enable-prefix-caching` | Enables automatic prefix caching. |
325:     | `--speculative-config` | Enables one Qwen3.5 MTP speculative token. |
326:     | `--compilation-config` | Uses `FULL_DECODE_ONLY` ACL Graph replay. |
327:     | `--additional-config` | Enables CPU binding and Fused MC2. |
[...]
334: 
335:     The validated mixed deployment uses eight Atlas 800 A2 (64GB × 8) nodes
336:     with the `Qwen3.8-2.4T-A95B-w4a8` checkpoint. Data parallelism spans the
337:     eight nodes, each node runs one DP rank, tensor parallelism uses all 8
338:     NPUs in the node, and the resulting topology is DP8/TP8/EP64.
[...]
350:         ```shell
351:         # Values that must be adapted to the target environment.
352:         export MODEL_PATH=<QWEN3_8_MODEL_PATH>
353:         export TOKENIZER_PATH=<QWEN3_8_TOKENIZER_PATH>
354:         export LOCAL_IP=<NODE0_LOCAL_IP>
355:         export NIC_NAME=<NODE0_NIC_NAME>
[...]
383:             --host 0.0.0.0 \
384:             --port $PORT \
385:             --served-model-name qwen3.8 \
386:             --tokenizer $TOKENIZER_PATH \
387:             --trust-remote-code \
[...]
399:             --max-num-batched-tokens 4096 \
400:             --gpu-memory-utilization 0.92 \
401:             --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":1}' \
402:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
403:             --additional-config '{"enable_cpu_binding":true,"enable_fused_mc2":1}'
[...]
412:         ```shell
413:         # Values that must be adapted to the target environment.
414:         export MODEL_PATH=<QWEN3_8_MODEL_PATH>
415:         export TOKENIZER_PATH=<QWEN3_8_TOKENIZER_PATH>
416:         export LOCAL_IP=<WORKER_LOCAL_IP>
417:         export NODE0_IP=<NODE0_LOCAL_IP>
[...]
448:             --host 0.0.0.0 \
449:             --port $PORT \
450:             --served-model-name qwen3.8 \
451:             --tokenizer $TOKENIZER_PATH \
452:             --trust-remote-code \
[...]
465:             --max-num-batched-tokens 4096 \
466:             --gpu-memory-utilization 0.92 \
467:             --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":1}' \
468:             --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
469:             --additional-config '{"enable_cpu_binding":true,"enable_fused_mc2":1}'
[...]
496:     | `--gpu-memory-utilization 0.92` | Reserves HBM headroom for the weights and activation peak on 64GB nodes. |
497:     | `--enable-prefix-caching` | Enables automatic prefix caching. |
498:     | `--speculative-config` | Enables one Qwen3.5 MTP speculative token. |
499:     | `--compilation-config` | Uses `FULL_DECODE_ONLY` ACL Graph replay. |
500:     | `--additional-config` | Enables CPU binding and Fused MC2. |
[...]
532:   -H "Content-Type: application/json" \
533:   -d '{
534:     "model": "qwen3.8",
535:     "messages": [
536:       {"role": "user", "content": "Write a Python function to merge two sorted linked lists."}
[...]
571: 2. After execution, you can get the result. Here are the GPQA Diamond results
572:    of
573:    [Qwen3.8-2.4T-A95B-w4a8](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-2.4T-A95B-w4a8)
574:    and
575:    [Qwen3.8-2.4T-A95B-w8a8](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-2.4T-A95B-w8a8)
576:    for reference only.
577: 
578: | dataset | model | metric | mode | vllm-api-general-chat |
579: | --- | --- | --- | --- | ---: |
580: | GPQA Diamond | Qwen3.8-2.4T-A95B-w4a8 | accuracy | gen | 91.92% |
581: | GPQA Diamond | Qwen3.8-2.4T-A95B-w8a8 | accuracy | gen | 93.75% |
582: 
583: ## 8 Performance Evaluation
[...]
602: ### 8.3 Run the Tests
603: 
604: Run performance evaluation of `Qwen3.8-2.4T-A95B` as an example. Refer to
605: [vLLM benchmark](https://docs.vllm.ai/en/latest/benchmarking/) for more details.
606: 
607: ```shell
608: vllm bench serve \
609:   --model Qwen/Qwen3.8-2.4T-A95B \
610:   --served-model-name qwen3.8 \
611:   --base-url http://<server_ip>:8000 \
612:   --dataset-name random \
[...]
686: | Chunked Prefill | Enabled by the vLLM V1 scheduler | Splits long prefill inputs to reduce per-step memory peaks. | Tune with `--max-num-batched-tokens`. |
687: | Prefix Cache | `--enable-prefix-caching` | Reuses KV state for repeated prefixes. | The benefit depends on the prefix cache hit rate. |
688: | Qwen3.5 MTP speculative decoding | `--speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":1}'` | Improves decode throughput when the acceptance rate is good. | Tune the speculative token count for the target workload. |
689: | Full decode ACL Graph | `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'` | Reduces operator dispatch overhead during decode. | Used by the validated configuration. |
690: | Fused MC2 | `--additional-config '{"enable_fused_mc2":1}'` | Enables fused MoE communication and computation. | Used by the validated configuration. |
[...]
699: ### Q1: Which inputs are supported by the open-weight model?
700: 
701: Qwen3.8-2.4T-A95B is a text-only model. It does not support multimodal input.
702: 
703: ### Q2: Can thinking mode be disabled?

## vllm-ascend/docs/source/tutorials/models/Qwen3.8-27B.md
[...]
1: # Qwen3.8-27B
2: 
3: ## 1 Introduction
[...]
9:     **For the production environment on the customer side, [MindIE Motor](https://www.hiascend.com/document/detail/en/mindie/latest/quickstart/docs/en/user_guide/quick_start.md) + vLLM-Ascend is recommended.**
10: 
11: Qwen3.8-27B is the 27-billion-parameter dense member of the Qwen3.8 family, the most capable generation in the Qwen open-model family to date. Built on the architectural foundation of Qwen3.5, it shares the same hybrid-attention backbone as the 2.4T MoE flagship: of its 64 layers, only 16 run full (gated) attention (`full_attention_interval: 4`) while the other 48 run linear attention (Gated DeltaNet) with a constant recurrent state. It is a native vision-language model — the architecture is `Qwen3_5ForConditionalGeneration` and `config.json` carries a `vision_config` — that understands images and videos, and it ships with a built-in MTP (Multi-Token Prediction) draft head and a native 262,144-token context window extensible up to 1,000,000 tokens.
12: 
13: Delivering substantial gains over Qwen3.5/Qwen3.6 across coding, professional work, research, and long-horizon agentic tasks, Qwen3.8-27B features stronger autonomous planning, more reliable end-to-end task completion, and broader downstream compatibility with popular harnesses and development tools. Thinking mode is on by default and can be disabled per request; reasoning depth is tunable via `reasoning_effort` (`xhigh`/`medium`/`low`), and reasoning context from historical messages is retained via `preserve_thinking`.
14: 
15: This document focuses on text serving on Ascend NPUs. It describes the main validation steps for the model, including supported features, prerequisites, installation, multi-node deployment, functional verification, accuracy and performance evaluation, performance tuning, and FAQs.
16: 
17: This document is validated and written based on **vLLM-Ascend 0.23.0**. The current model (Qwen3.8-27B) is first supported in this version.
18: 
19: ## 2 Supported Features
[...]
31: |  Weight Version                              | Hardware Requirements | Download Links |
32: |----------------------------------------------|-----------------------|----------------|
33: | `Qwen3.8-27B` (BF16 version)                 | 1 950DT Products (96GB × 8) node or 1 950PR Products (128GB × 8) node or 1 Atlas 800 A3 (64GB × 16) node <br>or 1 Atlas 800 A2 (64GB × 8) node | [ModelScope](https://www.modelscope.cn/models/Qwen/Qwen3.8-27B) |
34: | `Qwen3.8-27B-w8a8` (Quantized version)       | 1 950PR Products (128GB × 8) node or 1 Atlas 800 A3 (64GB × 16) node or 1 Atlas 800 A2 (64GB × 8) node | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-27B-w8a8) |
35: | `Qwen3.8-27B-w8a8-mxfp8` (Quantized version) | 1 950DT Products (96GB × 8) or 1 950PR Products (128GB × 8) node | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-27B-w8a8-mxfp8) |
36: | `Qwen3.8-27B-w8a8-310p` (Quantized version)  | 1 Atlas 300I DUO  | [ModelScope](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-27B-w8a8-310p) |
37: 
38: It is recommended to download the model weight to the shared directory of multiple nodes, such as `/root/.cache/`.
[...]
51: 
52:     ```bash
53:     export IMAGE=quay.io/ascend/vllm-ascend:qwen3.8-a5
54:     export NAME=vllm-ascend
55: 
[...]
88: 
89:     ```bash
90:     export IMAGE=quay.io/ascend/vllm-ascend:qwen3.8-a3
91:     export NAME=vllm-ascend
92: 
[...]
129: 
130:     ```bash
131:     export IMAGE=quay.io/ascend/vllm-ascend:qwen3.8-a2
132:     export NAME=vllm-ascend
133: 
[...]
231:     #!/bin/sh
232:     # Load model from ModelScope to speed up download
233:     export MODEL_PATH=Eco-Tech/Qwen3.8-27B-w8a8-mxfp8
234:     export VLLM_USE_MODELSCOPE=True
235:     export HCCL_BUFFSIZE=512
[...]
238:     # To reduce memory fragmentation and avoid out of memory
239: 
240:     # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.8-27B-w8a8-mxfp8) or a local directory path
241:     # Ensure the model path matches the directory recorded during download
242: 
[...]
247:         --tensor-parallel-size 1 \
248:         --quantization ascend \
249:         --served-model-name qwen3.8 \
250:         --max-num-seqs 32 \
251:         --max-model-len 131072 \
[...]
254:         --enable-prefix-caching \
255:         --gpu-memory-utilization 0.85 \
256:         --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
257:         --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
258:         --additional-config '{"enable_cpu_binding":true}'
[...]
271:     - `--quantization ascend` indicates that quantization is used. To disable quantization, remove this option.
272:     - `--enable-prefix-caching` enables automatic prefix caching.
273:     - `--speculative-config` uses `qwen3_5_mtp` for `Qwen3.8-27B` because it shares the same MTP head design as `Qwen3.5-27B`.
274:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
275:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
278: === "950PR Products"
279: 
280:     The following example is for 950PR Products. Quantized versions need `--quantization ascend`. On 950PR Products, `Qwen3.8-27B-w8a8` is the current recommended weight; switch to `Qwen3.8-27B-w8a8-mxfp8` later after further optimization.
281: 
282:     ```bash
[...]
289:     export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
290: 
291:     # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.8-27B-w8a8) or a local directory path
292:     # Ensure the model path matches the directory recorded during download
293:     export MODEL_PATH=Eco-Tech/Qwen3.8-27B-w8a8
294: 
295:     vllm serve $MODEL_PATH \
[...]
299:         --tensor-parallel-size 1 \
300:         --quantization ascend \
301:         --served-model-name qwen3.8 \
302:         --max-num-seqs 32 \
303:         --max-model-len 256000 \
[...]
306:         --enable-prefix-caching \
307:         --gpu-memory-utilization 0.9 \
308:         --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
309:         --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
310:         --additional-config '{"enable_cpu_binding":true}'
[...]
323:     - `--quantization ascend` indicates that quantization is used. To disable quantization, remove this option.
324:     - `--enable-prefix-caching` enables automatic prefix caching.
325:     - `--speculative-config` uses `qwen3_5_mtp` for `Qwen3.8-27B` because it shares the same MTP head design as `Qwen3.5-27B`.
326:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
327:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
336:     #!/bin/sh
337:     # Load model from ModelScope to speed up download
338:     export MODEL_PATH=Eco-Tech/Qwen3.8-27B-w8a8
339:     export VLLM_USE_MODELSCOPE=True
340:     export HCCL_BUFFSIZE=512
[...]
343:     # To reduce memory fragmentation and avoid out of memory
344: 
345:     # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.8-27B-w8a8) or a local directory path
346:     # Ensure the model path matches the directory recorded during download
347: 
[...]
352:         --tensor-parallel-size 2 \
353:         --quantization ascend \
354:         --served-model-name qwen3.8 \
355:         --max-num-seqs 32 \
356:         --max-model-len 131072 \
[...]
359:         --enable-prefix-caching \
360:         --gpu-memory-utilization 0.85 \
361:         --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3, "enforce_eager": true}' \
362:         --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}' \
363:         --additional-config '{"enable_cpu_binding":true}'
[...]
376:     - `--quantization ascend` indicates that quantization is used. To disable quantization, remove this option.
377:     - `--enable-prefix-caching` enables automatic prefix caching.
378:     - `--speculative-config` uses `qwen3_5_mtp` for `Qwen3.8-27B` because it shares the same MTP head design as `Qwen3.5-27B`.
379:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
380:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
385:     Currently only the **TP** scenario is supported. Choose **TP=2** or **TP=4** according to the available devices. Replace `MODEL_PATH` with a ModelScope model id or a local directory path. The quantized version needs to start with the `--quantization ascend` parameter.
386: 
387:     === "Qwen3.8-27B-w8a8"
388: 
389:         Startup Command:
[...]
394:         export VLLM_USE_MODELSCOPE=True
395: 
396:         # Model weight path; can be a ModelScope model id (e.g., Eco-Tech/Qwen3.8-27B-w8a8) or a local directory path
397:         # Ensure the model path matches the directory recorded during download
398:         export MODEL_PATH=Eco-Tech/Qwen3.8-27B-w8a8-310p
399: 
400:         vllm serve $MODEL_PATH \
[...]
402:             --port 8000 \
403:             --tensor-parallel-size 4 \
404:             --served-model-name qwen3.8 \
405:             --max-num-seqs 128 \
406:             --max-model-len 16384 \
407:             --trust-remote-code \
408:             --gpu-memory-utilization 0.90 \
409:             --mamba-ssm-cache-dtype float16 \
410:             --dtype float16 \
411:             --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}' \
412:             --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}' \
413:             --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
[...]
417: 
418:     - `--tensor-parallel-size` sets the tensor parallel size. Choose **TP=2** or **TP=4** according to the available devices.
419:     - `--max-model-len` represents the context length, which is the maximum value of the input plus output for a single request. Configure it based on the actual workload and available memory; `Qwen3.8-27B` supports up to 262144.
420:     - `--max-num-seqs` indicates the maximum number of concurrent requests. Configure it as needed—setting it too high may cause OOM.
421:     - `--gpu-memory-utilization` represents the proportion of HBM that vLLM will use for actual inference. Configure this value according to the actual device memory; setting it too high may cause OOM. The default value is `0.9`.
422:     - `--mamba-ssm-cache-dtype` sets the data type of the Mamba SSM cache. On Atlas 300I DUO, only `float16` is supported.
423:     - `--dtype float16` must be set on Atlas 300I DUO. These devices only support the FP16 data type.
424:     - `--speculative-config` uses `qwen3_5_mtp` for `Qwen3.8-27B` because it shares the same MTP head design as `Qwen3.5-27B`. On Atlas 300I DUO, it is recommended to set `num_speculative_tokens` to `1`.
425:     - `--compilation-config` contains configurations related to the aclgraph graph mode. The most significant configurations are `"cudagraph_mode"` and `"cudagraph_capture_sizes"`, which have the following meanings:
426:         - `"cudagraph_mode"`: represents the specific graph mode. Currently, `"PIECEWISE"` and `"FULL_DECODE_ONLY"` are supported. The graph mode is mainly used to reduce the cost of operator dispatch. Currently, `"FULL_DECODE_ONLY"` is recommended.
[...]
439: ## 6 Functional Verification
440: 
441: After the service is started, the model can be invoked by sending a prompt. Two API interfaces are supported: `completions` and `chat/completions`. Use the `--served-model-name` you configured (`qwen3.8` for `Qwen3.8-27B`).
442: 
443: **Completions API:**
[...]
447:     -H "Content-Type: application/json" \
448:     -d '{
449:         "model": "qwen3.8",
450:         "prompt": "The future of AI is",
451:         "max_tokens": 50,
[...]
460:     -H "Content-Type: application/json" \
461:     -d '{
462:         "model": "qwen3.8",
463:         "messages": [
464:             {"role": "user", "content": "The future of AI is"}
[...]
477:     "object": "text_completion",
478:     "created": 1780971952,
479:     "model": "qwen3.8",
480:     "choices": [
481:         {
[...]
502: 1. Refer to [Using AISBench](../../developer_guide/evaluation/using_ais_bench.md) for details.
503: 
504: 2. After execution, you can get the result. Here are the results of `Qwen3.8-27B`, `Qwen3.8-27B-w8a8` and `Qwen3.8-27B-w8a8-mxfp8` in `vllm-ascend:v0.23.0rc1` for reference only.
505: 
506: | dataset | model | metric | mode | vllm-api-general-chat |
507: |----- | ----- | ----- | ----- | -----|
508: | GPQA Diamond | Qwen3.8-27B | accuracy | gen | 90.40 |
509: | GPQA Diamond | Qwen3.8-27B-w8a8 | accuracy | gen | 89.90 |
510: | GPQA Diamond | Qwen3.8-27B-w8a8-mxfp8 | accuracy | gen | 89.39 |
511: 
512: ## 8 Performance Evaluation
[...]
518: ### 8.2 Using vLLM Benchmark
519: 
520: Run performance evaluation of `Qwen3.8-27B-w8a8` as an example.
521: 
522: Refer to [vllm benchmark](https://docs.vllm.ai/en/latest/benchmarking/) for more details.
[...]
538: ```bash
539: export VLLM_USE_MODELSCOPE=True
540: # For Qwen3.8-27B-w8a8:
541: vllm bench serve --model Eco-Tech/Qwen3.8-27B-w8a8 --dataset-name random --random-input 200 --num-prompts 200 --request-rate 1 --save-result --result-dir ./
542: ```
543: 
[...]
548: ### 9.1 Recommended Configurations
549: 
550: > **Note**: The current documentation focuses on the rapid adaptation and validation of the Qwen3.8-27B model on Ascend NPUs. Performance tuning results have not yet been fully verified. Recommended configurations for typical scenarios (e.g., long context, low latency, and high throughput) will be supplemented and updated here once the corresponding validation is completed. In the meantime, please refer to [Section 9.2](#92-tuning-guidelines) for general tuning guidance.
551: >
552: > **Atlas 300I DUO**: Currently only the TP scenario is supported. Choose **TP=2** or **TP=4** according to the available devices. With **TP=4**, `--max-model-len` can support **128k** and **256k** long-sequence scenarios; configure `--max-num-seqs` as needed—setting it too high may cause OOM.
[...]
576: | --- | --- | --- | --- | --- |
577: | Prefix Cache | Scenarios with repeated prefixes (e.g., shared system prompts, few-shot examples) | `--enable-prefix-caching` | Reuses cached KV state for repeated prefixes, avoiding redundant prefill computation. | The benefit depends on the prefix cache hit rate. |
578: | Qwen3.5 MTP Speculative Decoding | Decode-heavy workloads with acceptable acceptance rate | `--speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":3}'` | Uses the built-in MTP draft head to speculate multiple tokens per step and verifies them in a single forward pass. | Tune the speculative token count for the target workload; benefit depends on the acceptance rate. |
579: 
580: ## 10 FAQ

## vllm-ascend/docs/source/tutorials/models/Qwen3.8-Flash-Next.md
[...]
1: # Qwen3.8-Flash-Next (Experimental)
2: 
3: ## 1 Introduction
[...]
9:     **For the production environment on the customer side, [MindIE Motor](https://www.hiascend.com/document/detail/en/mindie/latest/quickstart/docs/en/user_guide/quick_start.md) + vLLM-Ascend is recommended.**
10: 
11: Qwen3.8-Flash-Next is a multimodal Mixture-of-Experts (MoE) model and an experimental preview of the architecture that will underpin Qwen4. Its language model combines Gated DeltaNet and Qwen Sparse Attention (QSA), gated residual connections, Position Learning Enhancement (PLE), and a native Multi-Token Prediction (MTP) head.
12: 
13: The current version supports only Atlas A3 series hardware. Atlas A2 series hardware and Ascend 950DT and 950PR products are not yet supported and will be enabled progressively in future releases. This tutorial describes the W8A8 deployment on Atlas 800 A3. Text and multimodal input have been validated on Atlas 800 A3.
14: 
15: This document is validated and written based on **vLLM-Ascend 0.26.0rc release**. The current model (Qwen3.8-Flash-Next) is first supported in this version.
16: 
17: !!! warning
18: 
19:     Automatic Prefix Caching is experimental for Qwen3.8-Flash-Next. Enable it
20:     with `--enable-prefix-caching --mamba-cache-mode align` and revalidate NPU
21:     memory capacity for the target context length and concurrency.
[...]
33: The following model weights are available:
34: 
35: - `Qwen3.8-Flash-Next-w8a8-mtp` (Quantized version): requires 1 Atlas 800 A3 (64GB × 8) node. [https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-Flash-Next-w8a8-mtp](https://www.modelscope.cn/models/Eco-Tech/Qwen3.8-Flash-Next-w8a8-mtp)
36: 
37: It is recommended to download the model weight to the shared directory of multiple nodes, such as /root/.cache/.
[...]
43: The pre-built images listed below have been validated for this tutorial.
44: 
45: A pre-built Qwen3.8 A3 image is available in the [vllm-ascend repository](https://quay.io/repository/ascend/vllm-ascend?tab=tags&tag=latest). Select the image that matches the host operating system:
46: 
47: - openEuler: `quay.io/ascend/vllm-ascend:qwen3.8-next-a3-openeuler`
48: - Ubuntu: `quay.io/ascend/vllm-ascend:qwen3.8-next-a3`
49: 
50: The following example uses the AArch64 image and exposes 8 devices on an Atlas 800 A3 node. The service command in Section 5.1 uses the first eight devices.
[...]
55: 
56:     ```bash
57:     export IMAGE=quay.io/ascend/vllm-ascend:qwen3.8-next-a3
58:     export NAME=vllm-ascend-qwen38-flash-next
59: 
60:     docker pull "$IMAGE"
[...]
127:     source /usr/local/Ascend/nnal/atb/set_env.sh
128: 
129:     export MODEL_PATH=/models/Qwen3.8-Flash-Next-w8a8-mtp
130:     export VLLM_ASCEND_ENABLE_QSA_LIGHTNING_INDEXER=1
131:     export VLLM_ASCEND_ENABLE_QSA_E3V=1
[...]
135:         --host 0.0.0.0 \
136:         --port 8088 \
137:         --served-model-name qwen3.8-flash-next \
138:         --trust-remote-code \
139:         --quantization ascend \
[...]
153:         --reasoning-parser qwen3 \
154:         --compilation-config '{"cudagraph_capture_sizes":[4,8,12,16,20,24,28,32],"cudagraph_mode":"FULL_DECODE_ONLY"}' \
155:         --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":3,"enforce_eager":true}' \
156:         --additional-config '{"enable_cpu_binding":true,"ascend_compilation_config":{"fuse_norm_quant":false}}'
157:     ```
[...]
174: ## 6 Functional Verification
175: 
176: After the service is started, the model can be invoked by sending a prompt. The `chat/completions` API is supported. Use the `--served-model-name` you configured (`qwen3.8-flash-next` for `Qwen3.8-Flash-Next`).
177: 
178: ### 6.1 Basic Chat Completion
[...]
182:     -H "Content-Type: application/json" \
183:     -d '{
184:         "model": "qwen3.8-flash-next",
185:         "messages": [
186:             {"role": "user", "content": "Who are you?"}
[...]
201:     -H "Content-Type: application/json" \
202:     -d '{
203:         "model": "qwen3.8-flash-next",
204:         "messages": [
205:             {
[...]
240:     -H "Content-Type: application/json" \
241:     -d '{
242:         "model": "qwen3.8-flash-next",
243:         "messages": [
244:             {
[...]
282: ```
283: 
284: Qwen3.8-Flash-Next uses thinking mode by default. To request reasoning explicitly, set `enable_thinking` to `true` (or omit it). The parser returns the reasoning separately from the final answer:
285: 
286: ```bash
[...]
288:     -H "Content-Type: application/json" \
289:     -d '{
290:         "model": "qwen3.8-flash-next",
291:         "messages": [
292:             {
[...]
312:     -H "Content-Type: application/json" \
313:     -d '{
314:         "model": "qwen3.8-flash-next",
315:         "messages": [
316:             {
[...]
334: 1. Refer to [Using AISBench](../../developer_guide/evaluation/using_ais_bench.md) for evaluation setup and usage.
335: 
336: 2. After execution, you can get the result. Here are the results of `Qwen3.8-Flash-Next` in `vllm-ascend:v0.26.0rc` for reference only.
337: 
338: The A3 W8A8 deployment described in Section 5.1 was validated on GPQA Diamond with the following result.

## vllm-ascend/docs/source/user_guide/configuration/additional_config.md
[...]
31: 
32: ```bash
33: vllm serve Qwen/Qwen3-8B --additional-config='{"config_key":"config_value"}'
34: ```
35: 
[...]
39: from vllm import LLM
40: 
41: LLM(model="Qwen/Qwen3-8B", additional_config={"config_key":"config_value"})
42: ```
43: 
[...]
104: 
105: ```bash
106: vllm serve Qwen/Qwen3-8B --additional-config '{
107:   "runtime_config_path": "/data/runtime/config/runtime_config.json",
108:   "runtime_config_hot_reload": true,

## vllm-ascend/docs/source/user_guide/feature_guide/batch_invariance.md
[...]
113: 
114: ```bash
115: VLLM_BATCH_INVARIANT=1 vllm serve Qwen/Qwen3-8B \
116:     --no-enable-chunked-prefill \
117:     --no-enable-prefix-caching \
[...]
132: # regardless of batch size or order
133: response = client.completions.create(
134:     model="Qwen/Qwen3-8B",
135:     prompt="The future of AI is",
136:     max_tokens=100,
[...]
165: 
166: llm = LLM(
167:     model="Qwen/Qwen3-8B",
168:     tensor_parallel_size=1,
169:     enable_prefix_caching=False,
[...]
203: | --- | :---: | :---: | :---: |
204: | `Qwen/Qwen3-1.7B` | ✅ | ✅ | ✅ |
205: | `Qwen/Qwen3-8B` | ✅ | ✅ | ✅ |
206: | `Qwen/Qwen3-30B-A3B` | ✅ | ✅ | ✅ |
207: | `Qwen/Qwen3-235B-A22B` | ✅ | ✅ | ✅ |
208: | `Qwen/Qwen3.5-35B-A3B` | ✅ | ✅ | ❌ |
209: 
210: Other models may also work, but these have been explicitly validated. If you encounter issues with a specific model, please report them on the [GitHub issue tracker](https://github.com/vllm-project/vllm-ascend/issues/new/choose).

## vllm-ascend/docs/source/user_guide/feature_guide/flash_attention.md
[...]
71: 
72: ```bash
73: vllm serve Qwen/Qwen3-8B \
74:   --additional-config '{"rl_config": {"enabled": true, "enable_training_consistency": true}}' \
75:   --compilation-config '{"cudagraph_mode": "PIECEWISE"}'
[...]
87: 
88: response = client.completions.create(
89:     model="Qwen/Qwen3-8B",
90:     prompt="The future of AI is",
91:     max_tokens=100,
[...]
117: 
118: llm = LLM(
119:     model="Qwen/Qwen3-8B",
120:     tensor_parallel_size=1,
121:     additional_config={
[...]
155: FA3 has been tested and verified on the following models:
156: 
157: - **Qwen3 (Dense)**: `Qwen/Qwen3-0.6B`, `Qwen/Qwen3-1.7B`, `Qwen/Qwen3-8B`
158: - **Qwen3 (MoE)**: `Qwen/Qwen3-30B-A3B`
159: 

## vllm-ascend/docs/source/user_guide/feature_guide/lora.md
[...]
56: ## Usage Example
57: 
58: ### Qwen3.5-27B
59: 
60: ```bash
61: vllm serve /path/to/Qwen3.5-27B \
62:     ... \
63:     --enable-lora \
64:     --max-loras 1 \
65:     --max-lora-rank 8 \
66:     --lora-modules '{"name": "mix-lora", "path": "/path/to/Qwen3.5-27B-lora", "base_model_name": "Qwen/Qwen3.5-27B"}'
67: ```
68: 
[...]
79:     -H "Content-Type: application/json" \
80:     -d '{
81:         "model": "Qwen3.5-27B",
82:         "messages": [
83:             {"role": "user", "content": "Introduce LoRA in one sentence."}
[...]
103: ```
104: 
105: `Qwen3.5-27B` is the served base name from this example. If the launch sets `--served-model-name`, use that string instead. A successful call returns HTTP 200 and a non-empty `choices[0].message.content`.
106: 
107: ## Dynamic LoRA

## vllm-ascend/docs/source/user_guide/feature_guide/preempt_offload_connector.md
[...]
275: * Current D2H and H2D transfers use basic torch copy operations. They are
276:   correctness-oriented and not yet optimized for transfer throughput.
277: * Qwen3.5 with async scheduling is not fully supported yet. Disable async
278:   scheduling when using preempt offload with Qwen3.5 models.
279: * If CPU memory capacity is insufficient, the connector skips offload for that
280:   request and the scheduler falls back to the original recompute behavior.

## vllm-ascend/docs/source/user_guide/feature_guide/quantization.md
[...]
105: ### 3. Native FP8 checkpoints (no quantization step needed)
106: 
107: Many models are now published directly in FP8, for example [Qwen/Qwen3.8-27B-FP8](https://modelscope.cn/models/Qwen/Qwen3.8-27B-FP8) and [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash). Their `config.json` carries `"quant_method": "fp8"` together with a `weight_block_size`, meaning every quantized weight is stored as `float8_e4m3fn` plus one `float32` scale per weight block. vLLM Ascend detects and serves these checkpoints as published, so no offline re-quantization is required:
108: 
109: ```bash
110: vllm serve /path/to/Qwen3.8-27B-FP8 --trust-remote-code
111: vllm serve /path/to/GLM-5.3-Flash --tensor-parallel-size 8 --trust-remote-code
112: ```

## vllm-ascend/docs/source/user_guide/feature_guide/rl.md
[...]
248: 
249: ```bash
250: vllm serve Qwen/Qwen3-8B \
251:     --additional-config '{"rl_config": {"enabled": true, "enable_batch_invariant": true}}' \
252:     --compilation-config '{"cudagraph_mode": "PIECEWISE"}'
[...]
316: 
317: ```bash
318: vllm serve Qwen/Qwen3-8B \
319:     --enable-auto-tool-choice \
320:     --tool-call-parser hermes
[...]
360: VLLM_USE_V2_MODEL_RUNNER=1 \
361: VLLM_ENABLE_SCALE_OUT_ENDPOINTS=1 \
362: vllm serve Qwen/Qwen3-8B \
363:     --enable-trace-replay
364: ```

## vllm-ascend/docs/source/user_guide/feature_guide/runtime_guard.md
[...]
16: 
17: ```bash
18: vllm serve Qwen/Qwen3-8B --additional-config '{
19:   "runtime_config_hot_reload": true,
20:   "runtime_config": {
[...]
30: 
31: ```bash
32: vllm serve Qwen/Qwen3-8B --additional-config '{
33:   "runtime_config_path": "/data/runtime/config/runtime_config.json",
34:   "runtime_config_hot_reload": true

## vllm-ascend/docs/source/user_guide/feature_guide/speculative_decoding.md
[...]
33:     > **Note**: For PD Separation deployment, `num_speculative_tokens` should be subject to one of the following conditions:
34:     >
35:     > 1. Hybrid Mamba models (e.g., Qwen-Next and Qwen3.5 series): `num_speculative_tokens` should be equal on P nodes and D nodes.
36:     > 2. Other models: `num_speculative_tokens` on P nodes should be 1, and `num_speculative_tokens` on D nodes should be greater or equal to 1.
37: - **`model`** (str, optional): Path or HF repo ID for the draft model. Required for `eagle`, `eagle3`, `dflash`, `medusa`, and `draft_model`. Automatically resolved for `mtp` (reuses target model), `ngram`, `suffix`, and `extract_hidden_states`.
[...]
236: 
237:     llm = LLM(
238:         model="Qwen/Qwen3-8B",
239:         tensor_parallel_size=1,
240:         distributed_executor_backend="mp",
[...]
245:         speculative_config={
246:             "method": "dflash",
247:             "model": "z-lab/Qwen3-8B-DFlash-b16",
248:             "num_speculative_tokens": 7,
249:         },
[...]
261: 
262:     ```shell
263:     vllm serve Qwen/Qwen3-8B \
264:       --tensor-parallel-size 1 \
265:       --max-model-len 4096 \
[...]
268:       --no-enable-prefix-caching \
269:       --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
270:       --speculative-config '{"method": "dflash", "model": "z-lab/Qwen3-8B-DFlash-b16", "num_speculative_tokens": 7}'
271:     ```
272: 
[...]
282: There is no separate `dflash2` method value: keep `"method": "dflash"` — when
283: the draft checkpoint's architecture is `DFlash2DraftModel` (e.g.
284: `z-lab/Qwen3.8-27B-DFlash2`), the DFlash2 drafter is selected automatically.
285: 
286: - Offline inference
[...]
296: 
297:     llm = LLM(
298:         model="Qwen/Qwen3.8-27B",
299:         tensor_parallel_size=2,
300:         max_model_len=2048,
[...]
303:         speculative_config={
304:             "method": "dflash",
305:             "model": "z-lab/Qwen3.8-27B-DFlash2",
306:             "num_speculative_tokens": 8,
307:         },
[...]
321: 
322:     ```shell
323:     vllm serve Qwen/Qwen3.8-27B \
324:       --tensor-parallel-size 2 \
325:       --max-model-len 2048 \
[...]
328:       --no-enable-prefix-caching \
329:       --compilation-config '{"cudagraph_mode": "PIECEWISE", "cudagraph_capture_sizes": [9]}' \
330:       --speculative-config '{"method": "dflash", "model": "z-lab/Qwen3.8-27B-DFlash2", "num_speculative_tokens": 8}'
331:     ```
332: 
[...]
359: 
360:     ```shell
361:     VLLM_USE_V2_MODEL_RUNNER=1 vllm serve Qwen/Qwen3.8-27B \
362:       --tensor-parallel-size 2 \
363:       --max-model-len 2048 \
364:       --no-enable-prefix-caching \
365:       --speculative-config '{"method": "dflash", "model": "z-lab/Qwen3.8-27B-DFlash2", "num_speculative_tokens": 8, "enforce_eager": true}'
366:     ```
367: 
[...]
399: 
400:     llm = LLM(
401:         model="Qwen/Qwen3-8B",
402:         tensor_parallel_size=1,
403:         distributed_executor_backend="mp",
[...]
408:         speculative_config={
409:             "method": "dspark",
410:             "model": "deepseek-ai/dspark_qwen3_8b_block7",
411:             "num_speculative_tokens": 7,
412:             "enforce_eager": True,
[...]
425: 
426:     ```shell
427:     vllm serve Qwen/Qwen3-8B \
428:       --tensor-parallel-size 1 \
429:       --max-model-len 4096 \
[...]
432:       --no-enable-prefix-caching \
433:       --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
434:       --speculative-config '{"method": "dspark", "model": "deepseek-ai/dspark_qwen3_8b_block7", "num_speculative_tokens": 7, "enforce_eager": true}'
435:     ```
436: 
[...]
446: 
447: ```shell
448: VLLM_USE_V2_MODEL_RUNNER=1 vllm serve Qwen/Qwen3-8B \
449:   --speculative-config '{
450:     "method": "dspark",
451:     "model": "deepseek-ai/dspark_qwen3_8b_block7",
452:     "num_speculative_tokens": 7,
453:     "enable_adaptive_verification": true
[...]
607:         with tempfile.TemporaryDirectory() as tmpdir:
608:             llm = LLM(
609:                 model="Qwen/Qwen3-8B",
610:                 tensor_parallel_size=1,
611:                 speculative_config={
[...]
654: 
655:     ```shell
656:     vllm serve Qwen/Qwen3-8B \
657:       --tensor-parallel-size 1 \
658:       --speculative-config '{"method": "extract_hidden_states", "num_speculative_tokens": 1, "draft_model_config": {"hf_config": {"eagle_aux_hidden_state_layer_ids": [2, 18, 34]}}}' \
[...]
717: 
718: llm = LLM(
719:     model="Qwen/Qwen3-8B",
720:     tensor_parallel_size=1,
721:     distributed_executor_backend="mp",
[...]
726:     speculative_config={
727:         "method": "dspark",
728:         "model": "deepseek-ai/dspark_qwen3_8b_block7",
729:         "num_speculative_tokens": 7,
730:     },

## vllm-ascend/docs/source/user_guide/release_notes.md
[...]
3: ## v0.30.0rc1 - 2026.10.11
4: 
5: This is vLLM Ascend v0.30.0rc1, a model-focused release built on the v0.29 release line and aligned with upstream vLLM v0.30.0 via the main2main pipeline. This release focuses on four flagship models: **DeepSeek V4.1**, **GLM-5.3**, **GLM-5.3-Flash**, and **Qwen3.8-27B**, and hardens the shared execution stacks they rely on (Model Runner V2, PCP/DCP parallelism, KV Cache Pool, and speculative decoding). Model or hardware combinations outside the scope declared below are not part of the release claims. Please follow the [official documentation](https://docs.vllm.ai/projects/ascend/en/v0.30.0rc1/) to get started.
6: 
7: ### Highlights
[...]
10: - **GLM-5.3**: Enabled sparse SFA C8 (INT8 packed KV cache) for GLM-5.3-Flash and indexer MXFP4 for GLM-5.2, fixed GLM MRV2 issues and GLM-5.2 DSpark sequence lengths/per-request FIA bounds, fixed GLM-5.3-Flash small slot page inflation, and backported always-on reasoning for GLM-5.3. [#17115](https://github.com/vllm-project/vllm-ascend/pull/17115) [#17949](https://github.com/vllm-project/vllm-ascend/pull/17949) [#18060](https://github.com/vllm-project/vllm-ascend/pull/18060) [#17613](https://github.com/vllm-project/vllm-ascend/pull/17613) [#17571](https://github.com/vllm-project/vllm-ascend/pull/17571) [#17545](https://github.com/vllm-project/vllm-ascend/pull/17545) [#17876](https://github.com/vllm-project/vllm-ascend/pull/17876)
11: - **GLM-5.3-Flash**: Added KV Pool support for non-layerwise pooling and Mamba in Mooncake layerwise, added layerwise memcache DRAM/SSD pooling, optimized Triton KPool and gated norm, supported GQA decode context parallelism and SFA-only DSA CP, and provided P/D and KV cache pool deployment guides. [#16945](https://github.com/vllm-project/vllm-ascend/pull/16945) [#17287](https://github.com/vllm-project/vllm-ascend/pull/17287) [#17698](https://github.com/vllm-project/vllm-ascend/pull/17698) [#17542](https://github.com/vllm-project/vllm-ascend/pull/17542) [#16478](https://github.com/vllm-project/vllm-ascend/pull/16478) [#17990](https://github.com/vllm-project/vllm-ascend/pull/17990) [#17987](https://github.com/vllm-project/vllm-ascend/pull/17987) [#17773](https://github.com/vllm-project/vllm-ascend/pull/17773) [#17946](https://github.com/vllm-project/vllm-ascend/pull/17946)
12: - **Qwen3.8-27B**: Supported non-contiguous KV cache in hybrid linear-attention models, respected per-layer KV cache dtype and kept KV cache contiguous for paged attention, restored C8 V scales on hybrid cache page reassignment, restored Mamba block tables before deferred PP postprocessing, added the FLA NPU backend for GDN prefill, and fixed 310P performance and kernel compatibility for quantized deployment. [#14340](https://github.com/vllm-project/vllm-ascend/pull/14340) [#17924](https://github.com/vllm-project/vllm-ascend/pull/17924) [#18003](https://github.com/vllm-project/vllm-ascend/pull/18003) [#17956](https://github.com/vllm-project/vllm-ascend/pull/17956) [#17954](https://github.com/vllm-project/vllm-ascend/pull/17954) [#17565](https://github.com/vllm-project/vllm-ascend/pull/17565) [#17534](https://github.com/vllm-project/vllm-ascend/pull/17534) [#16420](https://github.com/vllm-project/vllm-ascend/pull/16420) [#17964](https://github.com/vllm-project/vllm-ascend/pull/17964) [#17278](https://github.com/vllm-project/vllm-ascend/pull/17278)
13: - **Platform & Execution**: Aligned the plugin with upstream vLLM v0.30.0 via the main2main pipeline, extended Model Runner V2 with fine-grained TP (MLP, embedding, o_proj in graph mode) and async CPP scheduling (default-on was evaluated and rolled back pending further hardening), landed the EPLB STAIR placement policy, enhanced PCP (sharded embedding/LM head and O projection weights, PCP+DCP stacking, graph-executed decode sharding). [#16527](https://github.com/vllm-project/vllm-ascend/pull/16527) [#17361](https://github.com/vllm-project/vllm-ascend/pull/17361) [#16967](https://github.com/vllm-project/vllm-ascend/pull/16967) [#17380](https://github.com/vllm-project/vllm-ascend/pull/17380) [#17661](https://github.com/vllm-project/vllm-ascend/pull/17661) [#17514](https://github.com/vllm-project/vllm-ascend/pull/17514) [#17512](https://github.com/vllm-project/vllm-ascend/pull/17512) [#17511](https://github.com/vllm-project/vllm-ascend/pull/17511) [#17509](https://github.com/vllm-project/vllm-ascend/pull/17509) [#17510](https://github.com/vllm-project/vllm-ascend/pull/17510) [#17508](https://github.com/vllm-project/vllm-ascend/pull/17508) [#17159](https://github.com/vllm-project/vllm-ascend/pull/17159) [#17502](https://github.com/vllm-project/vllm-ascend/pull/17502) [#17598](https://github.com/vllm-project/vllm-ascend/pull/17598) [#17456](https://github.com/vllm-project/vllm-ascend/pull/17456) [#17958](https://github.com/vllm-project/vllm-ascend/pull/17958) [#17940](https://github.com/vllm-project/vllm-ascend/pull/17940) [#18065](https://github.com/vllm-project/vllm-ascend/pull/18065) [#17112](https://github.com/vllm-project/vllm-ascend/pull/17112) [#17150](https://github.com/vllm-project/vllm-ascend/pull/17150) [#17157](https://github.com/vllm-project/vllm-ascend/pull/17157)
14: 
[...]
32: - Supported GQA decode context parallelism and SFA-only DSA CP for GLM-5.3 Flash. [#17990](https://github.com/vllm-project/vllm-ascend/pull/17990) [#17987](https://github.com/vllm-project/vllm-ascend/pull/17987)
33: - Supported Top-K transport across PP stages. [#15614](https://github.com/vllm-project/vllm-ascend/pull/15614)
34: - Supported non-contiguous KV cache in hybrid models like Qwen3.5. [#14340](https://github.com/vllm-project/vllm-ascend/pull/14340) [#17924](https://github.com/vllm-project/vllm-ascend/pull/17924)
35: - Added GLM-5.2 V2 sparse KV offload with PP and DSpark, plus a fused quant lightning indexer manage operator for sparse KV cache offloading. [#17900](https://github.com/vllm-project/vllm-ascend/pull/17900) [#17444](https://github.com/vllm-project/vllm-ascend/pull/17444)
36: - Added GLM-5.3-Flash layerwise memcache DRAM/SSD pooling in KV Pool. [#17698](https://github.com/vllm-project/vllm-ascend/pull/17698)
[...]
58: | GLM-5.3 | Atlas 800I A3 (128GB x 8), Atlas 800I A2 | W8A8C8 multi-node serving; sparse SFA C8 packed KV cache, speculative decoding (DSpark) |
59: | GLM-5.3-Flash | Atlas 800I A3 (128GB x 8), Atlas 800I A2 | W8A8 on A3/A2; P/D disaggregation and KV Cache Pool deployment |
60: | Qwen3.8-27B | Atlas 800I A3, Atlas 800I A2, Atlas 300I DUO (W8A8-310P) | BF16 and W8A8; hybrid linear-attention serving with non-contiguous KV cache |
61: 
62: ### Performance
[...]
77: - Skipped repeated MRV2 idle-DP indexer work for MiniMax-M3. [#17538](https://github.com/vllm-project/vllm-ascend/pull/17538)
78: - Committed only dirty block-table ranges in MRV1 (later reverted for correctness; see Known Issues). [#17066](https://github.com/vllm-project/vllm-ascend/pull/17066) [#17470](https://github.com/vllm-project/vllm-ascend/pull/17470)
79: - Fixed a 310P performance issue for Qwen3.5-2B. [#17278](https://github.com/vllm-project/vllm-ascend/pull/17278)
80: - Enabled torch.compile for DeepSeek V4.1. [#18081](https://github.com/vllm-project/vllm-ascend/pull/18081)
81: - Used bf16 router GEMM with fp32 accumulation for bf16-origin weights in MoE. [#17068](https://github.com/vllm-project/vllm-ascend/pull/17068)
[...]
256: 
257: - Expanded Ascend 950 supports: MXFP quant for token dispatch, and CPU binding with topo clusters. [#11614](https://github.com/vllm-project/vllm-ascend/pull/11614) [#11717](https://github.com/vllm-project/vllm-ascend/pull/11717)
258: - Expanded Atlas 300I DUO support: disabled npugraph_ex by default, added Qwen3.5-Dense documentation, and fixed 310P spec decoding accuracy. [#10874](https://github.com/vllm-project/vllm-ascend/pull/10874) [#12077](https://github.com/vllm-project/vllm-ascend/pull/12077) [#11918](https://github.com/vllm-project/vllm-ascend/pull/11918)
259: - Added operator supports: KV quant sparse flash attention, and Triton SwiGLuStep kernel (replaced AscendC‑based fused_gdn_gating). [#11626](https://github.com/vllm-project/vllm-ascend/pull/11626) [#11467](https://github.com/vllm-project/vllm-ascend/pull/11467) [#12035](https://github.com/vllm-project/vllm-ascend/pull/12035)
260: 
[...]
317: 
318: - Fixed GDN state and graph-dispatch accuracy regressions across P/D, PCP, MTP, and DCP. [#11195](https://github.com/vllm-project/vllm-ascend/pull/11195) [#11893](https://github.com/vllm-project/vllm-ascend/pull/11893) [#12027](https://github.com/vllm-project/vllm-ascend/pull/12027)
319: - Fixed Qwen3.5 PCP + chunked prefill accuracy and small-chunk problems. [#11508](https://github.com/vllm-project/vllm-ascend/pull/11508) [#11807](https://github.com/vllm-project/vllm-ascend/pull/11807)
320: - Fixed DeepSeek V4 MXFP routing precision and W4A16MXFP communication accuracy. [#11663](https://github.com/vllm-project/vllm-ascend/pull/11663) [#12585](https://github.com/vllm-project/vllm-ascend/pull/12585)
321: - Fixed KV-transfer ordering, Mooncake grouping, and AscendStore hash/lease handling. [#11887](https://github.com/vllm-project/vllm-ascend/pull/11887) [#12252](https://github.com/vllm-project/vllm-ascend/pull/12252) [#12012](https://github.com/vllm-project/vllm-ascend/pull/12012)
[...]
345: - Qwen3-235B-A22B W8A8 and Qwen3-235B W4A8 may show lower performance than the baseline in some A3 PD-mixed aclgraph scenarios. [#15296](https://github.com/vllm-project/vllm-ascend/issues/15296)
346: - GLM5.1-W4A4C8-mxfp4 may show a performance regression on Ascend 950 due to CPU-binding and load-balancing effects. [#15268](https://github.com/vllm-project/vllm-ascend/issues/15268)
347: - Qwen3.6-27B DFlash with mixed sliding-window and full attention requires the V2 model runner. [#15650](https://github.com/vllm-project/vllm-ascend/issues/15650)
348: - DeepSeek-V3.2-W8A8 may show a partial performance regression in A3 single-node mixed deployment. [#15651](https://github.com/vllm-project/vllm-ascend/issues/15651)
349: - DeepSeek-V4 sleep mode with `sleep_mode_extra_cleanup` may fail to recover after wakeup. Sleep mode is mainly intended for training scenarios. [#15648](https://github.com/vllm-project/vllm-ascend/issues/15648)
[...]
360: 
361: - **Ascend 950 and DeepSeek V4**: Added end-to-end DeepSeek V4 support on Ascend 950, including DSA attention, MTP, piecewise graph execution, distributed inference, sparse attention, CPU binding, and MXFP quantization and communication paths. [#9757](https://github.com/vllm-project/vllm-ascend/pull/9757) [#9935](https://github.com/vllm-project/vllm-ascend/pull/9935) [#10236](https://github.com/vllm-project/vllm-ascend/pull/10236) [#11014](https://github.com/vllm-project/vllm-ascend/pull/11014)
362: - **Model and hardware coverage**: Expanded support and deployment guidance for GLM-5.2, GLM-4.7-Flash, Qwen3.5/Qwen3.6, Qwen3-ASR, Qwen3-Omni, Bailing MoE, Gemma4, Step3, and MiniMax 2.x models across A2, A3, Ascend 950, and Atlas 300I DUO. GLM-5.2 supports long-sequence inference up to 1M tokens on Atlas 800 A3. [#8657](https://github.com/vllm-project/vllm-ascend/pull/8657) [#9560](https://github.com/vllm-project/vllm-ascend/pull/9560) [#10441](https://github.com/vllm-project/vllm-ascend/pull/10441) [#10697](https://github.com/vllm-project/vllm-ascend/pull/10697) [#11091](https://github.com/vllm-project/vllm-ascend/pull/11091) [#11264](https://github.com/vllm-project/vllm-ascend/pull/11264) [#12115](https://github.com/vllm-project/vllm-ascend/pull/12115)
363: - **Context parallelism and sparse attention**: Added SFA DCP with a replicated indexer, compact KV gather, C8 support, and device-side metadata paths for long-context and P/D-disaggregated deployments. [#9638](https://github.com/vllm-project/vllm-ascend/pull/9638) [#9809](https://github.com/vllm-project/vllm-ascend/pull/9809) [#11819](https://github.com/vllm-project/vllm-ascend/pull/11819) [#11871](https://github.com/vllm-project/vllm-ascend/pull/11871) [#11981](https://github.com/vllm-project/vllm-ascend/pull/11981)
364: - **KV-cache lifecycle and offload**: Added hybrid/Mamba attention prefix caching; CPU and SSD offload in AscendStore that covers all backends. [#8743](https://github.com/vllm-project/vllm-ascend/pull/8743) [#9533](https://github.com/vllm-project/vllm-ascend/pull/9533) [#9731](https://github.com/vllm-project/vllm-ascend/pull/9731) [#10393](https://github.com/vllm-project/vllm-ascend/pull/10393)
[...]
376: 
377: - Added and optimized recurrent GDN, causal Conv1D, sparse-attention, LightningIndexer, compressor, and fused quantization operators. [#7798](https://github.com/vllm-project/vllm-ascend/pull/7798) [#7926](https://github.com/vllm-project/vllm-ascend/pull/7926) [#9382](https://github.com/vllm-project/vllm-ascend/pull/9382) [#9491](https://github.com/vllm-project/vllm-ascend/pull/9491) [#9825](https://github.com/vllm-project/vllm-ascend/pull/9825) [#10730](https://github.com/vllm-project/vllm-ascend/pull/10730)
378: - Expanded Atlas 300I DUO support for Qwen3.5, Qwen3.6, Qwen3-ASR, Qwen3-VL, quantized MoE paths, MTP, and graph execution. [#7674](https://github.com/vllm-project/vllm-ascend/pull/7674) [#7725](https://github.com/vllm-project/vllm-ascend/pull/7725) [#10309](https://github.com/vllm-project/vllm-ascend/pull/10309) [#12115](https://github.com/vllm-project/vllm-ascend/pull/12115) [#13262](https://github.com/vllm-project/vllm-ascend/pull/13262)†
379: - Added Python 3.12 support and moved release images to Python 3.12. [#9558](https://github.com/vllm-project/vllm-ascend/pull/9558)
380: 
[...]
390: - Reduced PCP/DCP KV-cache all-gather traffic by selecting the required blocks before communication. Enable PCP or DCP with `--prefill-context-parallel-size` or `--decode-context-parallel-size`; no separate optimization switch is needed. [#8050](https://github.com/vllm-project/vllm-ascend/pull/8050)
391: - Optimized `split_qkv_tp_rmsnorm_rope` kernels for supported quantized model paths. Kernel selection is automatic; no manual setting is needed. [#8059](https://github.com/vllm-project/vllm-ascend/pull/8059) [#9830](https://github.com/vllm-project/vllm-ascend/pull/9830)
392: - Removed prefill host-device synchronization in Qwen3-Next and Qwen3.5 paths. It applies automatically to those models. [#7967](https://github.com/vllm-project/vllm-ascend/pull/7967)
393: - Reduced SFA prefill KV all-gather communication for PCP/DCP. Enable the corresponding context-parallel mode; the optimized communication path is automatic. [#8043](https://github.com/vllm-project/vllm-ascend/pull/8043)
394: - Added a Triton penalty kernel for requests using repetition, frequency, or presence penalties. It is selected automatically when penalties are requested. [#7569](https://github.com/vllm-project/vllm-ascend/pull/7569)
[...]
420: - Added asynchronous all-gather for DSA-CP output-projection TP weights. Enable FlashComm1 and `additional_config.enable_dsa_cp=true`; the asynchronous path is automatic. [#10694](https://github.com/vllm-project/vllm-ascend/pull/10694)
421: - Improved DeepSeek V4 prefix-cache hit rates when MTP is enabled. Prefix caching is enabled by default in vLLM V1; no flag is needed unless it was previously disabled. [#11107](https://github.com/vllm-project/vllm-ascend/pull/11107)
422: - Reused prebuilt chunk host metadata to reduce synchronization overhead for Qwen3.5 and MiniMax-M2.5 workloads. It applies automatically to the affected model paths. [#9310](https://github.com/vllm-project/vllm-ascend/pull/9310)
423: - Parallelized Mooncake KV receive handling for P/D-disaggregated deployments. Configure the Mooncake KV-transfer connector; receive parallelism is automatic. [#10548](https://github.com/vllm-project/vllm-ascend/pull/10548)
424: - Optimized AscendStore key construction and KV Pool miss handling to reduce host overhead. Configure `AscendStoreConnector`; the optimized paths are selected automatically. [#12783](https://github.com/vllm-project/vllm-ascend/pull/12783)†
[...]
428: 
429: - Fixed GDN state and graph-dispatch accuracy regressions across P/D, PCP, MTP, and DCP, including one-token stateful prefill handling. [#11195](https://github.com/vllm-project/vllm-ascend/pull/11195) [#11893](https://github.com/vllm-project/vllm-ascend/pull/11893) [#12027](https://github.com/vllm-project/vllm-ascend/pull/12027) [#12255](https://github.com/vllm-project/vllm-ascend/pull/12255)†
430: - Fixed Qwen3.5/Qwen3.6 speculative-decoding accuracy, Mamba prefix-cache corruption, block-table overflow, and Atlas 300I DUO graph failures. [#11337](https://github.com/vllm-project/vllm-ascend/pull/11337) [#11408](https://github.com/vllm-project/vllm-ascend/pull/11408) [#11353](https://github.com/vllm-project/vllm-ascend/pull/11353) [#11659](https://github.com/vllm-project/vllm-ascend/pull/11659) [#11920](https://github.com/vllm-project/vllm-ascend/pull/11920) [#12038](https://github.com/vllm-project/vllm-ascend/pull/12038)
431: - Fixed GLM-5.1 IndexCache weight loading and a GLM-4.7-Flash first-request `IndexError` with MTP and layerwise Memcache. [#11363](https://github.com/vllm-project/vllm-ascend/pull/11363) [#11829](https://github.com/vllm-project/vllm-ascend/pull/11829)
432: - Fixed Qwen MoE routing overflow and shared-expert gate failures, Qwen3-Omni ModelSlim W8A8 checkpoint loading, and Qwen3-VL rotary-embedding copy races on Atlas 300I DUO. [#11391](https://github.com/vllm-project/vllm-ascend/pull/11391) [#11730](https://github.com/vllm-project/vllm-ascend/pull/11730) [#12321](https://github.com/vllm-project/vllm-ascend/pull/12321) [#11679](https://github.com/vllm-project/vllm-ascend/pull/11679) [#12132](https://github.com/vllm-project/vllm-ascend/pull/12132)
[...]
490: - On Ascend 950, context parallelism is not supported with SFA; context-parallel MLA and GQA paths are experimental. [#13303](https://github.com/vllm-project/vllm-ascend/pull/13303)†
491: - In v0.23.0, combining GLM-5.2 DCP with Sparse Flash Attention C8 (`enable_sparse_sfa_c8`) has known issues, including performance degradation, and is not recommended. [#14011](https://github.com/vllm-project/vllm-ascend/pull/14011)†
492: - On Atlas 300I DUO or Atlas 200I Pro (310P), Qwen3.5-2B-W8A8 GSM8K accuracy can fluctuate by more than 1% compared with the floating-point model. [#14335](https://github.com/vllm-project/vllm-ascend/issues/14335)
493: - DeepSeek V4 on A2 or A3 can experience 1-2 second TPOT spikes under high concurrency when varying input shapes trigger Triton kernel recompilation. [#14324](https://github.com/vllm-project/vllm-ascend/issues/14324)
494: - DeepSeek V4 Flash and GLM-5.1 SWE benchmark results can vary because of intermittent evaluation failures, including container crashes, timeouts, dependency-download failures, and agent nondeterminism. [#14326](https://github.com/vllm-project/vllm-ascend/issues/14326)
[...]
510: ### Highlights
511: 
512: - **Expanded model support**: Added GLM-5.2 support on A2 and A3, and Ascend 310P support for Qwen3-ASR-1.7B, Qwen3.5, and Qwen3.6. [#10441](https://github.com/vllm-project/vllm-ascend/pull/10441) [#11264](https://github.com/vllm-project/vllm-ascend/pull/11264) [#10257](https://github.com/vllm-project/vllm-ascend/pull/10257) [#12115](https://github.com/vllm-project/vllm-ascend/pull/12115)
513: - **Sparse attention and context parallelism**: Added SFA DCP with a replicated indexer, compact KV gather, and C8 support. [#11819](https://github.com/vllm-project/vllm-ascend/pull/11819) [#11981](https://github.com/vllm-project/vllm-ascend/pull/11981) [#11846](https://github.com/vllm-project/vllm-ascend/pull/11846) [#11871](https://github.com/vllm-project/vllm-ascend/pull/11871)
514: - **KV-cache lifecycle and offload**: Added recompute KV-cache offload for P/D decoder nodes, AscendStore coordination, and layerwise KV Pooling with a Memcache backend. [#10742](https://github.com/vllm-project/vllm-ascend/pull/10742) [#10393](https://github.com/vllm-project/vllm-ascend/pull/10393) [#11585](https://github.com/vllm-project/vllm-ascend/pull/11585)
[...]
536: 
537: - Fixed GLM-5.1 IndexCache weight loading and a GLM-4.7-Flash `IndexError` on the first request with MTP and layerwise MemCache. [#11363](https://github.com/vllm-project/vllm-ascend/pull/11363) [#11829](https://github.com/vllm-project/vllm-ascend/pull/11829)
538: - Fixed Qwen3.5 GDN accuracy regressions across PCP, MTP, and DCP graph replay, including a mixed-length PCP out-of-bounds crash, while restoring the previous model-runner dispatch behavior. [#11195](https://github.com/vllm-project/vllm-ascend/pull/11195) [#11893](https://github.com/vllm-project/vllm-ascend/pull/11893) [#12027](https://github.com/vllm-project/vllm-ascend/pull/12027) [#12283](https://github.com/vllm-project/vllm-ascend/pull/12283)
539: - Fixed Qwen3.5 speculative-decoding accuracy, garbled output, and out-of-bounds failures on Ascend 310P with MTP/EAGLE and full-graph execution. [#11337](https://github.com/vllm-project/vllm-ascend/pull/11337) [#11408](https://github.com/vllm-project/vllm-ascend/pull/11408) [#11920](https://github.com/vllm-project/vllm-ascend/pull/11920)
540: - Fixed Qwen MoE routing overflow and shared-expert gate matrix-multiplication failures on Ascend 310P. [#11391](https://github.com/vllm-project/vllm-ascend/pull/11391) [#11730](https://github.com/vllm-project/vllm-ascend/pull/11730)
541: - Fixed Qwen3-Omni ModelSlim W8A8 checkpoint loading failures caused by mismatched weight names and unquantized embedding metadata. [#12321](https://github.com/vllm-project/vllm-ascend/pull/12321)
[...]
544: - Fixed DeepSeek V4 Flash W4A8-MXFP4 all-gather EP inference on Ascend 950 by preserving routing-weight precision. [#11498](https://github.com/vllm-project/vllm-ascend/issues/11498) [#11663](https://github.com/vllm-project/vllm-ascend/pull/11663) [#11718](https://github.com/vllm-project/vllm-ascend/pull/11718)
545: - Fixed malformed streamed tool-call arguments and TP8+EP startup compatibility for MiniMax-M2 and MiniMax-M2.5. [#11505](https://github.com/vllm-project/vllm-ascend/pull/11505)
546: - Fixed silent prefix-cache output corruption and block-table overflow for Qwen3-Next, Qwen3.5, and other hybrid Mamba models using MTP/EAGLE, plus a 310P Mamba align-postprocess hang. [#11353](https://github.com/vllm-project/vllm-ascend/pull/11353) [#11659](https://github.com/vllm-project/vllm-ascend/pull/11659) [#12038](https://github.com/vllm-project/vllm-ascend/pull/12038)
547: - Fixed Mooncake KV-transfer grouping for Kimi-K2.7 Code with Kimi-K2.5-DFlash when P/D nodes use unequal TP sizes and target/draft models have different global KV-head counts. [#11887](https://github.com/vllm-project/vllm-ascend/pull/11887)
548: - Fixed the AscendStore parent-block hash chain when a KV block group is only partially missing. [#12252](https://github.com/vllm-project/vllm-ascend/pull/12252)
[...]
585: - Qwen3-30B-A3B floating-point serving can show a 1-2 ms TPOT regression at batch size 1 in the reported TP4 full-graph configuration. [#12337](https://github.com/vllm-project/vllm-ascend/issues/12337)
586: - In the reported DeepSeek V4 Flash W8A8 MTP P/D-disaggregated deployment, the second aisbench round can cause a worker process from another card to appear on an NPU device. [#12338](https://github.com/vllm-project/vllm-ascend/issues/12338)
587: - On Ascend 950, Qwen3.5-397B-W8A8-MXFP8-FULL_QUANT in a P/D-disaggregated deployment without MTP can alternate between correct and incorrect outputs. [#12339](https://github.com/vllm-project/vllm-ascend/issues/12339)
588: - DeepSeek V4 Pro on A3 and Ascend 950 Products can show continuously increasing memory usage in both P/D-disaggregated and co-located deployments, eventually causing OOM or service instability. [#12345](https://github.com/vllm-project/vllm-ascend/issues/12345)
589: - DeepSeek-V3.1-Terminus can show about a 15% output-throughput regression against the reported v0.18.0 baseline in high-throughput P/D-disaggregated deployments; the regression was reported on an A3 four-node 2P1D setup and an A2 large-EP setup. [#12349](https://github.com/vllm-project/vllm-ascend/issues/12349)
[...]
616: 
617: - Optimized `split_qkv_tp_rmsnorm_rope` with grid-stride loading and host-side reciprocal precomputation; the PR reports about a 5x kernel speedup on the tested MiniMax-M2.5 W8A8 QuaRot prefill workload. [#9830](https://github.com/vllm-project/vllm-ascend/pull/9830)
618: - Reused prebuilt chunk host metadata for Ascend chunk ops to reduce host-device synchronization overhead on Qwen3.5 workloads. [#9310](https://github.com/vllm-project/vllm-ascend/pull/9310)
619: - Skipped `compute_slot_mapping` for Mamba groups to reduce unnecessary work in hybrid cache paths. [#10492](https://github.com/vllm-project/vllm-ascend/pull/10492)
620: - Enabled multistream DSV4 DSA overlap and removed redundant DSA v1 code paths. [#10518](https://github.com/vllm-project/vllm-ascend/pull/10518)
[...]
655: - Added MXFP8 FlashCommV3 support on Ascend 950. [#9671](https://github.com/vllm-project/vllm-ascend/pull/9671)
656: - Added NZ layout support for W4A8 MoE compressed tensors and C8 quantization (GQA). [#9625](https://github.com/vllm-project/vllm-ascend/pull/9625) [#9721](https://github.com/vllm-project/vllm-ascend/pull/9721)
657: - Added Mooncake Connector hybrid PCP/DCP support for QWen3.5. [#9809](https://github.com/vllm-project/vllm-ascend/pull/9809)
658: - Added D2D NetLoader weight loading for draft models in speculative decoding. [#9893](https://github.com/vllm-project/vllm-ascend/pull/9893)
659: - Added Mooncake Connector hybrid attention support. [#8850](https://github.com/vllm-project/vllm-ascend/pull/8850)
[...]
672: - Added batch_invariant_ops setup for reinforcement learning scenarios. [#10034](https://github.com/vllm-project/vllm-ascend/pull/10034)
673: - Adapted load balance proxy example to shared scheduler workers. [#9645](https://github.com/vllm-project/vllm-ascend/pull/9645)
674: - [310P] Added Qwen3.5 MTP and graph mode support. [#10309](https://github.com/vllm-project/vllm-ascend/pull/10309)
675: 
676: ### Hardware and Operator Support
[...]
705: - Fixed empty `tool_calls` being emitted in OpenAI-format chat responses. [#9791](https://github.com/vllm-project/vllm-ascend/pull/9791)
706: - Backported MiniMax M2 tool call streaming support. [#9742](https://github.com/vllm-project/vllm-ascend/pull/9742)
707: - Repaired 310P Qwen3.5 ACLGraph precision. [#9727](https://github.com/vllm-project/vllm-ascend/pull/9727)
708: - Fixed precision of the `causal_conv1d_v310` operator on 310P. [#9720](https://github.com/vllm-project/vllm-ascend/pull/9720)
709: - Fixed ACL dtype mapping table for correct dtype conversions. [#9826](https://github.com/vllm-project/vllm-ascend/pull/9826)
[...]
732: - Fixed 310P Qwen3-Embedding and Qwen3-VL-Embedding run failures. [#9854](https://github.com/vllm-project/vllm-ascend/pull/9854)
733: - Removed legacy capture-size pruning in `update_aclgraph_sizes`. [#9962](https://github.com/vllm-project/vllm-ascend/pull/9962)
734: - Fixed `fused_gdn_gating` unavailability on Ascend 950 for Qwen3.5. [#10083](https://github.com/vllm-project/vllm-ascend/pull/10083)
735: - Fixed DSA v1 W8A8 dynamic conflict in attention. [#9476](https://github.com/vllm-project/vllm-ascend/pull/9476)
736: - Fixed DeepSeek-V4 compressed prefix lookup in prefix cache. [#10297](https://github.com/vllm-project/vllm-ascend/pull/10297)
[...]
789: - Added a dedicated `additional_config.enable_dsa_cp` switch to decouple DSA-CP from FC1. DSA-CP now requires both FC1 and DSA-CP to be explicitly enabled, allowing FC1 to stay enabled while DSA-CP is disabled when needed. [#9878](https://github.com/vllm-project/vllm-ascend/pull/9878)
790: - Added merged graph support for DFlash workloads. [#9074](https://github.com/vllm-project/vllm-ascend/pull/9074)
791: - Added LoRA support for Qwen3.5 dense models. [#9023](https://github.com/vllm-project/vllm-ascend/pull/9023)
792: - Added KV pool adaptation for DeepSeek V4 and separated MTP-layer KV cache sharding for DeepSeek V4 speculative decoding. [#9385](https://github.com/vllm-project/vllm-ascend/pull/9385) [#9367](https://github.com/vllm-project/vllm-ascend/pull/9367)
793: 
[...]
797: - Enabled MXFP4 flatquant and row parallel support on Ascend 950 Products. [#9391](https://github.com/vllm-project/vllm-ascend/pull/9391)
798: - Enabled MC2 dispatch and combine support for MXFP4/MXFP8 quantization on Ascend 950 Products. [#9365](https://github.com/vllm-project/vllm-ascend/pull/9365) [#9328](https://github.com/vllm-project/vllm-ascend/pull/9328)
799: - Improved 310P support by optimizing fused operators for Qwen3.5 Dense ACLGraph and simplifying the 310P RMSNormGated path. [#9104](https://github.com/vllm-project/vllm-ascend/pull/9104) [#9489](https://github.com/vllm-project/vllm-ascend/pull/9489)
800: 
801: ### Performance
[...]
925: - Add preemption guidance in FAQs. [#8136](https://github.com/vllm-project/vllm-ascend/pull/8136)
926: - Update the deployment and support documentation for GLM5, including parameter descriptions, best practices, and FAQs. [#7963](https://github.com/vllm-project/vllm-ascend/pull/7963) [#7909](https://github.com/vllm-project/vllm-ascend/pull/7909)
927: - Update the Qwen3.5 user guide. [#7934](https://github.com/vllm-project/vllm-ascend/pull/7934)
928: - Update the document configuration for DeepSeek-V3.2. [#7970](https://github.com/vllm-project/vllm-ascend/pull/7970)
929: - Clean up documentation wording and grammar. [#8073](https://github.com/vllm-project/vllm-ascend/pull/8073)
[...]
986: - **Minitron-8B-Base Support**: Verified and supported nvidia/Minitron-8B-Base model ([#8157](https://github.com/vllm-project/vllm-ascend/pull/8157))
987: - **Bailing Model Support**: Full support for Bailing MoE model with linear adaptation and ModelSlim quantization configuration ([#8657](https://github.com/vllm-project/vllm-ascend/pull/8657), [#8709](https://github.com/vllm-project/vllm-ascend/pull/8709))
988: - **Qwen3.5 MoE Flash Comm**: Support Flash Comm for Qwen3.5 MoE models ([#7486](https://github.com/vllm-project/vllm-ascend/pull/7486))
989: - **Initial MoE Support for MRv2**: Add initial MoE models support for Model Runner V2 ([#7922](https://github.com/vllm-project/vllm-ascend/pull/7922))
990: - **Xlite Backend Expansion**:
[...]
1013: 
1014: - **310P Enhancements**:
1015:     - Qwen3.5 model adaptation synchronized with main ([#8009](https://github.com/vllm-project/vllm-ascend/pull/8009))
1016:     - Support W8A8 dynamic linear method ([#7725](https://github.com/vllm-project/vllm-ascend/pull/7725))
1017:     - Support shared experts path in fused MoE for Qwen3.5 ([#7674](https://github.com/vllm-project/vllm-ascend/pull/7674))
1018:     - Add npu_causal_conv1d_310 AscendC Custom Op ([#7798](https://github.com/vllm-project/vllm-ascend/pull/7798))
1019:     - Add recurrent_gated_delta_rule_310 AscendC Custom Op ([#7926](https://github.com/vllm-project/vllm-ascend/pull/7926))
[...]
1031: - **Operator Optimizations**:
1032:     - Optimize split_qkv_tp_rmsnorm_rope ops ([#8059](https://github.com/vllm-project/vllm-ascend/pull/8059))
1033:     - Optimize host-device sync problem in prefill phase for Qwen3Next/Qwen3.5 ([#7967](https://github.com/vllm-project/vllm-ascend/pull/7967))
1034:     - Reduce prefill KV all-gather communication for PCP/DCP (SFA) ([#8043](https://github.com/vllm-project/vllm-ascend/pull/8043))
1035:     - Add penalty-related Triton kernel for better performance of penalties ([#7569](https://github.com/vllm-project/vllm-ascend/pull/7569))
[...]
1061:     - GLM4.7 documentation update ([#8450](https://github.com/vllm-project/vllm-ascend/pull/8450))
1062:     - GLM5 documentation with parameters and FAQs ([#7958](https://github.com/vllm-project/vllm-ascend/pull/7958), [#7850](https://github.com/vllm-project/vllm-ascend/pull/7850))
1063:     - Qwen3.5 user guide update ([#7866](https://github.com/vllm-project/vllm-ascend/pull/7866))
1064:     - Kimi-K2.5 documentation update ([#7901](https://github.com/vllm-project/vllm-ascend/pull/7901))
1065:     - Qwen3-Omni-30B-A3B-Thinking documentation ([#8628](https://github.com/vllm-project/vllm-ascend/pull/8628))
[...]
1082: - **DSV3.1 W4A8 TTFT**: Revert change of `balance_flag` to fix DSV3.1 W4A8 TTFT degradation ([#8675](https://github.com/vllm-project/vllm-ascend/pull/8675))
1083: - **DSV3.1 Service Startup**: Fix DeepSeek-V3.1 service failed to start ([#8208](https://github.com/vllm-project/vllm-ascend/pull/8208))
1084: - **Qwen3.5 MoE High Concurrency**: Fix Qwen3.5 MoE FC1 error under high concurrency when dp>1 ([#8396](https://github.com/vllm-project/vllm-ascend/pull/8396))
1085: - **Qwen3.5 MoE Flash Comm**: Fix Qwen3.5 MoE flash comm v1 shared expert shape error of mtp layer on A2 ([#7683](https://github.com/vllm-project/vllm-ascend/pull/7683))
1086: - **Graph Capture OOM**: Fix the graph capturing OOM in model_runner_v2 ([#8111](https://github.com/vllm-project/vllm-ascend/pull/8111))
1087: - **DeepSeek 3.2 C8 Precision**: Fix DeepSeek 3.2 C8 precision by reverting quantization layers ([#7628](https://github.com/vllm-project/vllm-ascend/pull/7628))
[...]
1179: 
1180: - Optimized Triton operator recompilation to reduce redundant rebuilds and unnecessary recompilation triggered by function parameter optimization. [#7647](https://github.com/vllm-project/vllm-ascend/pull/7647) [#7645](https://github.com/vllm-project/vllm-ascend/pull/7645)
1181: - Optimized the Qwen3.5 and Qwen3-Next GDN prefill path by prebuilding chunk metadata, reducing host-device synchronization overhead. [#7487](https://github.com/vllm-project/vllm-ascend/pull/7487)
1182: - Simplified the FIA prefill context merge path for better runtime efficiency. [#7293](https://github.com/vllm-project/vllm-ascend/pull/7293)
1183: 
[...]
1214: 
1215: - Auto-detect quantization format from model files, and remote model IDs (e.g., `org/model-name`) are also supported. `--quantization ascend` is not required now. [#7111](https://github.com/vllm-project/vllm-ascend/pull/7111)
1216: - Qwen3.5 is supported from this version on.
1217: - FlashLB algorithm for EPLB: supports per-step heat collection and multi-stage load balancing for better expert parallelism efficiency. [#6477](https://github.com/vllm-project/vllm-ascend/pull/6477)
1218: - LoRA with tensor parallel and `--fully-sharded-loras` is now fixed and working. [#6650](https://github.com/vllm-project/vllm-ascend/pull/6650)
[...]
1242: - Fix ngram graph replay accuracy error on 310P. [#7134](https://github.com/vllm-project/vllm-ascend/pull/7134)
1243: - Fix FIA pad logic in graph mode after upstream vLLM change. [#7144](https://github.com/vllm-project/vllm-ascend/pull/7144)
1244: - Fix a precision issue caused by wrong KV cache reshape on Qwen3.5. [#7209](https://github.com/vllm-project/vllm-ascend/pull/7209)
1245: - Fix extra processes spawned on rank0 device. [#7107](https://github.com/vllm-project/vllm-ascend/pull/7107)
1246: - Graph capture failures now properly raise exceptions for easier debugging. [#5644](https://github.com/vllm-project/vllm-ascend/pull/5644)
1247: - Fix Qwen3.5 model by replacing torch_npu.npu_recurrent_gated_delta_rule by fused_recurrent_gated_delta_rule. [#7109](https://github.com/vllm-project/vllm-ascend/pull/7109)
1248: - Fix the bug when running Qwen3-Reranker-0.6B with LoRA. [#7156](https://github.com/vllm-project/vllm-ascend/pull/7156)
1249: 
[...]
2308: ### Experimental
2309: 
2310: - Atlas 300I series is experimental supported in this release (Functional test passed with Qwen2.5-7b-instruct/Qwen2.5-0.5b/Qwen3-0.6B/Qwen3-4B/Qwen3-8B). [#1333](https://github.com/vllm-project/vllm-ascend/pull/1333)
2311: - Support EAGLE-3 for speculative decoding. [#1032](https://github.com/vllm-project/vllm-ascend/pull/1032)
2312: 

## vllm-ascend/docs/source/user_guide/support_matrix/supported_models.md
[...]
133:     |-----------------|----------|--------|------|------|------|---------|-------|------|------|--------|-------|--------|--------|-------|-------|--------|----------|---------|----------|-----|
134:     | GLM-5.3-Flash | 🔵 | Experimental | ✅ | 950DT Products | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 200k |  | [GLM-5.3-Flash](../../tutorials/models/GLM5.3-Flash.md) |
135:     |Qwen3.5-397B-A17B|✅        |       |✅    | 950DT Products |✅|✅|✅||✅|✅|✅||✅|✅|✅|✅|✅|1010000|| [Qwen3.5-397B-A17B](../../tutorials/models/Qwen3.5-397B-A17B.md) |
136:     |Qwen3.6-27B      |✅        |       |✅    | 950DT Products |✅|✅|✅||✅|✅|✅||✅|✅|✅|✅|✅|262144|| [Qwen3.5-27B / Qwen3.6-27B](../../tutorials/models/Qwen3.5-27B-Qwen3.6-27B.md) |
137:     |MiniMax-M3       |✅        |MXFP8; text/image/video||950DT Products||✅|✅||✅|✅|✅|✅|✅|✅|✅|🟡|✅|1M|| [MiniMax-M3](../../tutorials/models/MiniMax-M3.md) |
138: 
[...]
147:     | DeepSeek-V4-Flash-Vision-Exp        | 🔵      | W8A8; colocated deployment only | 🟡 | A2/A3 | ✅ | 🟡 | ✅ | 🟡 | ✅ | 🟡 | ✅ | 🟡 | ✅ | ✅ | ❌ | ✅ | ✅ | 130000 | [DeepSeek-V4-Flash-Vision-Exp](../../tutorials/models/DeepSeek-V4-Flash-Vision.md) |
148:     | DeepSeek-V4.1-Flash                 | ✅      | W8A8; 2-node A3 or 4-node A2 colocated deployment | 🟡 | A2/A3 | ✅ | 🟡 | ✅ | ❌ | ✅ | 🟡 | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | 1048576 | [DeepSeek-V4.1-Flash](../../tutorials/models/DeepSeek-V4.1-Flash.md) |
149:     | Qwen3.5-397B-A17B                   | 🔵      |      | ✅  | A2/A3              | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | 1010000 | [Qwen3.5-397B-A17B](../../tutorials/models/Qwen3.5-397B-A17B.md) |
150:     | Qwen3.5-27B / Qwen3.6-27B           | 🔵      |      | ✅  | A2/A3              | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | 262144 | [Qwen3.5-27B / Qwen3.6-27B](../../tutorials/models/Qwen3.5-27B-Qwen3.6-27B.md) |
151:     | Qwen3.6-35B-A3B                     | 🔵      |      | ✅  | A2/A3              | ✅ | ✅ | ✅ |  | 🔵 | ✅ | ✅ |  | ✅ | ✅ | ❌ | ✅ | ✅ | 262144 | [Qwen3.6-35B-A3B](../../tutorials/models/Qwen3.6-35B-A3B.md) |
152:     | Qwen3.8-Flash-Next           | 🔵      |      | ✅  | A3              | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | 262144 | [Qwen3.8-Flash-Next](../../tutorials/models/Qwen3.8-Flash-Next.md) |
153:     | Qwen3-Omni-30B-A3B-Thinking         | 🔵      |      |      | A2/A3              |  |  |  |  |  |  | ✅ |  | ✅ |  |  |  |  |  | [Qwen3-Omni-30B-A3B-Thinking](../../tutorials/models/Qwen3-Omni-30B-A3B-Thinking.md) |
154:     | Kimi-K2.5            | 🔴      |      |      | A2/A3              |  | ✅ | ✅ |  | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | 262144 | [Kimi-K2.5](../../tutorials/models/Kimi-K2.5.md) |
[...]
163:     |-------|---------|------|------|--------------------|------|-----------------|------------------------|------|----------------------|------------------|-----------------|-------------------------------|--------------------|--------------------|---------------|-----|
164:     | Qwen3-VL | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | 🟡 | ✅ | ✅ | ❌ | ✅ | ✅ | 16k | [Qwen-VL-Dense](../../tutorials/models/Qwen-VL-Dense.md) |
165:     | Qwen3.5-Dense | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | 256k | [Qwen3.5-Dense](../../tutorials/models/Qwen3.5-Dense.md) |
166:     | Qwen3.5-35B-A3B | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | 256k | [Qwen3.5-35B-A3B](../../tutorials/models/Qwen3.6-35B-A3B.md) |
167:     | Qwen3.5-27B | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | 256k | [Qwen3.5-27B](../../tutorials/models/Qwen3.5-27B-Qwen3.6-27B.md) |
168:     | Qwen3.6-27B | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | 256k | [Qwen3.6-27B](../../tutorials/models/Qwen3.5-27B-Qwen3.6-27B.md) |
169:     | Qwen3.6-35B-A3B | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | 256k | [Qwen3.6-35B-A3B](../../tutorials/models/Qwen3.6-35B-A3B.md) |
170:     | Qwen3.8-27B | ✅ |  | ❌ | Atlas 300I DUO | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | 256k | [Qwen3.8-27B](../../tutorials/models/Qwen3.8-27B.md) |
171:     | PaddleOCR-VL | ✅ |  | ❌ | Atlas 300I DUO | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | 16k | [PaddleOCR-VL](../../tutorials/models/PaddleOCR-VL.md) |
172:     | Qwen3-ASR | ✅ |  | ❌ | Atlas 300I DUO | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | 🟡 | ❌ | ✅ | ✅ | 4096 | [Qwen3-ASR-1.7B](../../tutorials/models/Qwen3-ASR-1.7B.md) |

## vllm-ascend/tests/e2e/cases/E2E_TEST_CASE_GUIDE.md
[...]
98: test_cases:
99:   - name: Qwen-example
100:     model: Qwen/Qwen3-8B
101:     envs:
102:       SERVER_PORT: DEFAULT_PORT
[...]
188: test_cases:
189:   - name: case-eager
190:     model: Qwen/Qwen3-8B
191:     envs:
192:       <<: *envs
[...]
196: 
197:   - name: case-graph
198:     model: Qwen/Qwen3-8B
199:     envs:
200:       <<: *envs
[...]
211: test_cases:
212:   - name: qwen-epd-example
213:     model: Qwen/Qwen3-8B
214:     service_mode: epd
215:     envs:
[...]
219: 
220:     epd_server_cmds:
221:       - [--port, $ENCODE_PORT, --model, Qwen/Qwen3-8B]
222:       - [--port, $PD_PORT, --model, Qwen/Qwen3-8B]
223: 
224:     epd_proxy_args:

## vllm-ascend/vllm_ascend/ops/triton/docs/fused_gdn_gating.md
[...]
5: - **Location**:
6: `vllm_ascend/ops/triton/fused_gdn_gating.py` — `fused_gdn_gating_kernel`, 1:1 wrapper `fused_gdn_gating_patch`
7: - **Function**: Computes the gating pair of the GDN (Gated DeltaNet) linear attention in one fused kernel: the log-decay gate `g` and the interpolation coefficient `beta_output`. It replaces the host-side torch chain `g = -exp(A_log) * softplus(a + dt_bias); beta = sigmoid(b)` in the recurrent-attention step of `vllm_ascend/ops/gdn.py` (Qwen3-Next / Qwen3.5 hybrid GDN models). Entry: `DeviceOperator.fused_gdn_gating` (A2/950PR&950DT Products) → 1:1 wrapper `fused_gdn_gating_patch` → `fused_gdn_gating_kernel`.
8: - **Formula** (per token `t`, per head `h`, computed in fp32):
9:     - `x = a[t, h] + dt_bias[h]`

## vllm-ascend/vllm_ascend/ops/triton/docs/lora_linear.md
[...]
65: ## Test Cases
66: 
67: The single-operator accuracy test uses TP-local Qwen3.5-27B projection shapes:
68: 
69: - single-slice O projection: hidden size 1536 and output size 5120;
