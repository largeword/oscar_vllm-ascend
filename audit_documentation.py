"""Inventory and scan every Markdown document in the four migration sources.

This is a documentation audit, not a claim that a keyword scan is a manual
review. Full-document hashes and selected excerpts make coverage reproducible.
Source repositories are read-only; outputs go beside this script.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PROJECTS = ("OSCAR", "gpt_new_oscar_kimi", "vllm", "vllm-ascend")
SKIP = {".git", ".venv", "node_modules", "__pycache__"}
TOPICS = {
    "model": r"qwen3[._-]?[58]|qwen3\.8|27b",
    "rotation": r"rotation|hadamard|covariance|eigensolv|校准|旋转|协方差",
    "accuracy": r"accuracy|precision|精度|logits|GPQA|quantile|rounding|k_mean",
    "integration": r"prefix cach|MTP|GDN|RoPE|mamba|INT2|OSCAR",
}


def main():
    inventory = []
    excerpts = []
    for project in PROJECTS:
        base = ROOT.parent / project
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() != ".md":
                continue
            if SKIP.intersection(path.relative_to(base).parts):
                continue
            raw = path.read_bytes()
            text = raw.decode("utf-8", errors="replace")
            lines = text.splitlines()
            counts = {topic: len(re.findall(pattern, text, re.I))
                      for topic, pattern in TOPICS.items()}
            inventory.append({
                "project": project, "path": str(path.relative_to(ROOT.parent)),
                "bytes": len(raw), "lines": len(lines),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "coverage": "full-text automated scan", "topic_counts": counts,
                "headings": [line for line in lines if re.match(r"^#{1,4} ", line)],
            })
            # Keep context rather than isolated matches; excerpts are explicitly
            # not a substitute for reading the source of a substantive finding.
            if project == "gpt_new_oscar_kimi" or (
                    project == "OSCAR" and "rotation" in path.parts):
                relevant = re.compile(TOPICS["rotation"] + "|" + TOPICS["accuracy"], re.I)
            else:
                relevant = re.compile(r"qwen3[._-]?[58]|OSCAR|27B|mamba.*cache.*dtype", re.I)
            selected = set()
            for i, line in enumerate(lines):
                if relevant.search(line):
                    selected.update(range(max(0, i - 2), min(len(lines), i + 3)))
            if selected:
                excerpts.append("\n## " + str(path.relative_to(ROOT.parent)) + "\n")
                previous = -2
                for i in sorted(selected):
                    if i > previous + 1:
                        excerpts.append("[...]\n")
                    excerpts.append(f"{i + 1}: {lines[i]}\n")
                    previous = i
    summary = {p: {"files": sum(x["project"] == p for x in inventory),
                   "lines": sum(x["lines"] for x in inventory if x["project"] == p),
                   "bytes": sum(x["bytes"] for x in inventory if x["project"] == p)}
               for p in PROJECTS}
    (ROOT / "documentation_inventory.json").write_text(
        json.dumps({"summary": summary, "files": inventory}, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "documentation_excerpts.md").write_text(
        "# Automated documentation excerpts\n\nCoverage: full-text scan; selected context only.\n" + "".join(excerpts))
    print(json.dumps(summary, indent=2))
    print(f"Excerpt lines: {sum(s.count(chr(10)) for s in excerpts)}")


if __name__ == "__main__":
    main()
