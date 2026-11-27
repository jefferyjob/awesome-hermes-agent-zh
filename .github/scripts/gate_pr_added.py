#!/usr/bin/env python3
"""PR 自动合并硬门槛：确定性规则，不信任 PR 文本，也不信任 AI 输出。

只允许「在 README.md 追加/修正条目行」的 PR 自动流转：
  - 所有非空新增行必须匹配条目格式（含修正既有条目的行）
  - 新增条目数 <= 上限（防单 PR 批量塞条目）
  - 删除的非空行只允许是条目行（改描述/改链接），且删除条目数 <= 新增条目数（防夹带删条目）
  - 新增条目指向的仓库不得已在 README 中收录（防重复）

用法:
  gate_pr_added.py [--json OUT] <diff文件> <README路径>

退出码: 0 = 通过; 1 = 拒绝（格式/重复问题，应自动关闭）; 2 = 转人工; 3 = 用法错误
stdout: 人读的原因说明；--json 时另写 {entries, repos, removed_entries} 到 OUT
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_pr_entries import ENTRY_RE, URL_RE  # noqa: E402

MAX_ENTRIES = 3


def readme_changes(diff_text):
    """返回 README.md 的（新增行, 删除行）。"""
    added, removed, in_readme = [], [], False
    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            in_readme = line.endswith(" b/README.md")
            continue
        if not in_readme or line.startswith(("---", "+++")):
            continue
        if line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            removed.append(line[1:])
    return added, removed


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", dest="json_out", default="")
    p.add_argument("diff_file")
    p.add_argument("readme_file")
    args = p.parse_args()

    diff_text = open(args.diff_file, encoding="utf-8", errors="replace").read()
    readme_text = open(args.readme_file, encoding="utf-8", errors="replace").read()
    added, removed = readme_changes(diff_text)

    reasons_reject, reasons_human = [], []

    # 1) 非空新增行必须全部是合法条目行（防 HTML/脚本/垃圾文本注入 README）
    bad = [l for l in added if l.strip() and not ENTRY_RE.match(l)]
    for line in bad[:5]:
        reasons_reject.append(
            f"非条目格式的新增行：`{line[:100]}`"
            "（格式须为 `- **[production|beta|experimental]** [名称](URL) by [作者](URL) - 中文描述`）"
        )

    entries = [l for l in added if ENTRY_RE.match(l)]

    # 2) 必须有新增条目（纯删改/清理类不自动流转）
    if not entries and not reasons_reject:
        reasons_human.append("PR 没有新增任何条目行（可能是删改或清理类改动），需人工确认。")

    # 3) 单 PR 条目数量上限
    if len(entries) > MAX_ENTRIES:
        reasons_human.append(
            f"单 PR 新增 {len(entries)} 条条目，超过自动处理上限（{MAX_ENTRIES} 条），需人工复核。"
        )

    # 4) 删除侧限制：非条目删除转人工；删条目数不得超过新增数
    removed_entries = [l for l in removed if ENTRY_RE.match(l)]
    removed_other = [l for l in removed if l.strip() and not ENTRY_RE.match(l)]
    if removed_other:
        reasons_human.append(
            f"PR 删除了 {len(removed_other)} 行非条目内容，需人工确认未误删正文。"
        )
    if len(removed_entries) > len(entries):
        reasons_human.append(
            f"PR 删除 {len(removed_entries)} 条既有条目、仅新增 {len(entries)} 条，"
            "疑似夹带删条目，需人工复核。"
        )

    # 5) 重复收录检查（对照 base 分支的 README；同一仓库「删旧增新」视为修改条目，不算重复）
    removed_repos = {f"{o}/{n}" for l in removed_entries for o, n in URL_RE.findall(l)}
    dups = []
    for owner, name in sorted({u for l in entries for u in URL_RE.findall(l)}):
        full = f"{owner}/{name}"
        if full in removed_repos:
            continue
        if re.search(re.escape("github.com/" + full), readme_text, re.I):
            dups.append(full)
    if dups:
        reasons_reject.append("以下仓库已在 README 中收录，不得重复提交：" + "、".join(dups))

    if reasons_reject:
        for r in reasons_reject:
            print(f"- ❌ {r}")
        code = 1
    elif reasons_human:
        for r in reasons_human:
            print(f"- ⚠️ {r}")
        code = 2
    else:
        print("硬门槛通过")
        code = 0

    if args.json_out:
        repos = [f"{o}/{n}" for l in entries for o, n in URL_RE.findall(l)]
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "entries": entries,
                    "repos": list(dict.fromkeys(repos)),
                    "removed_entries": removed_entries,
                },
                f,
                ensure_ascii=False,
            )
    return code


if __name__ == "__main__":
    sys.exit(main())
