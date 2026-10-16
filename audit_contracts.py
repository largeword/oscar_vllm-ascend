"""Dependency-free, read-only checks supporting the OSCAR migration review.

These inspect configuration and Python signatures without importing torch,
initializing an accelerator, or loading model weights. Numerical examples are
illustrations, not model-accuracy measurements.
"""
import ast
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT.parent
PORT = SOURCES / "gpt_new_oscar_kimi"
ASCEND = SOURCES / "vllm-ascend"


def functions(path):
    tree = ast.parse(path.read_text())
    return {node.name: node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def parameters(node):
    return [arg.arg for arg in (*node.args.posonlyargs, *node.args.args,
                               *node.args.kwonlyargs)]


def main():
    config = json.loads((PORT / "configs/target.json").read_text())
    acceptance = json.loads((PORT / "configs/acceptance.json").read_text())
    source_native = ASCEND / "vllm_ascend/sample/rejection_sampler.py"
    source_adapter = PORT / "oscar_ascend/integration/greedy_sampling.py"
    native = parameters(functions(source_native)["rejection_sample"])
    adapter_tree = ast.parse(source_adapter.read_text())
    adapter = next(node for node in adapter_tree.body
                   if isinstance(node, ast.FunctionDef)
                   and node.name == "rejection_sample_with_guarded_cu")
    call = next(node for node in ast.walk(adapter)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "original")
    adapter_keywords = [kw.arg for kw in call.keywords]
    native_greedy = parameters(functions(
        ASCEND / "vllm_ascend/ops/triton/reject_sample.py"
    )["rejection_greedy_sample_with_triton"])
    adapter_greedy = parameters(functions(source_adapter)["rejection_greedy_sample_with_triton"])

    # Resolve exactly the upstream helper's scalar behavior, without importing
    # its torch/Triton dependencies or executing the rest of the module.
    clip_file = SOURCES / "OSCAR/python/sglang/QuantKernel/oscar_rotation_clip_int2_kv.py"
    clip_ast = functions(clip_file)["_clip_index"]
    namespace = {}
    exec(compile(ast.Module(body=[clip_ast], type_ignores=[]), str(clip_file), "exec"), namespace)
    clip = namespace["_clip_index"]

    result = {
        "scope": "static source/configuration checks and scalar mathematical illustrations; no model or NPU run",
        "commits": {name: subprocess.check_output(
            ["git", "-C", str(SOURCES / name), "rev-parse", "HEAD"], text=True).strip()
            for name in ("OSCAR", "gpt_new_oscar_kimi", "vllm", "vllm-ascend")},
        "port_defaults": {
            "model": config["model"], "served_model_name": config["served_model_name"],
            "rotation_method": config["rotation_method"],
            "k_clip_ratio": config.get("k_clip_ratio", 0.0),
            "v_clip_ratio": config.get("v_clip_ratio", 0.0),
            "rope_override": config["hf_overrides"],
            "speculative_config": config["speculative_config"],
            "prefix_caching": config["enable_prefix_caching"],
            "model_quality_acceptance": acceptance["model_quality"],
        },
        "current_sibling_api_compatibility": {
            "native_rejection_sample_parameters": native,
            "adapter_calls_original_with_keywords": adapter_keywords,
            "unsupported_original_keywords": sorted(set(adapter_keywords) - set(native)),
            "native_greedy_parameters_absent_from_adapter": sorted(set(native_greedy) - set(adapter_greedy)),
            "gdn_fold_method_defined_in_native_builder":
                "_fold_spec_sized_prefill_chunks_into_spec" in functions(
                    ASCEND / "vllm_ascend/ops/gdn_attn_builder.py"),
        },
        "clipping_D256": [
            {"ratio": ratio, "sglang_order_statistic_index": clip(ratio, 256),
             "port_linear_quantile_rank": ratio * 255}
            for ratio in (0.96, 0.92)
        ],
        "TP_geometry_for_reference_24Q_4KV": {
            str(tp): {"local_q_heads": 24 // tp, "local_kv_heads": 4 // tp,
                      "global_kv_heads_by_rank": [list(range(r * (4 // tp), (r + 1) * (4 // tp)))
                                                  for r in range(tp)]}
            for tp in (2, 4)
        },
        "centering_merge_illustration": {
            "description": "Two equal raw logits 0,0; center ONLY history by subtracting q*mu=1. Without LSE correction its probability is wrong, even without quantization.",
            "correct_history_probability": 0.5,
            "uncorrected_history_probability": math.exp(-1) / (1 + math.exp(-1)),
            "required_history_lse_correction": "+ attention_scale * dot(raw_query, key_mean)",
        },
    }
    output = ROOT / "source_audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
