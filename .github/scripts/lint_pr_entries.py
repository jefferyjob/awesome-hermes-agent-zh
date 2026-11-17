#!/usr/bin/env python3
"""检查 PR 中对 README.md 的新增条目是否符合收录格式，并核验新增条目指向的仓库。

用法: lint_pr_entries.py <diff文件> <README路径> <变更文件列表（空格分隔）>
输出: Markdown 报告（stdout）
退出码: 0 = 全部通过; 1 = 存在问题
"""
import json
import os
import re
import sys
import time
import urllib.request

TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
ENTRY_RE = re.compile(
    r"^\- \*\*\[(production|beta|experimental)\]\*\*\s*\[[^\]]+\]\(\S+\) by \[[^\]]+\]\(\S+\) - \S.*"
)
URL_RE = re.compile(r"\(https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:/[^)]*)?\)")
ALLOWED_FILES = {"README.md", "assets/"}


def api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-hermes-zh-triage",
            **({"Authorization": "Bearer " + TOKEN} if TOKEN else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None


def added_readme_lines(diff):
    lines, in_readme = [], False
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            in_readme = line.endswith(" b/README.md")
            continue
        if not in_readme or line.startswith(("---", "+++")):
            continue
        if line.startswith("+") and not line.startswith("+++"):
            lines.append(line[1:])
    return lines


def main():
    if len(sys.argv) != 4:
        print("用法: lint_pr_entries.py <diff> <README> <变更文件>", file=sys.stderr)
        return 2
    diff = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    files = sys.argv[3].split()

    problems = []
    unexpected = [f for f in files if f != "README.md" and not f.startswith("assets/")]
    if unexpected:
        problems.append(f"变更了列表范围外的文件：{', '.join(unexpected)}（通常同步 PR 只应改动 README.md 与 assets/）")

    added = added_readme_lines(diff)
    if not added and not unexpected:
        print("未检测到 README.md 的新增行。")
        return 0

    repos = []
    ok_lines = 0
    rows = []
    for line in added:
        if not line.strip():
            continue
        if ENTRY_RE.match(line):
            ok_lines += 1
            urls = [f"{o}/{n}" for o, n in URL_RE.findall(line)]
            rows.append(("✅ 格式", line[:80] + ("…" if len(line) > 80 else ""), "，".join(urls) or "无仓库链接"))
            repos.extend(urls)
        elif line.startswith("- **["):
            rows.append(("❌ 格式", line[:80] + ("…" if len(line) > 80 else ""),
                         "不符合条目格式：`- **[标签]** [名称](URL) by [作者](URL) - 中文描述`，标签须为 production/beta/experimental"))
            problems.append("存在格式不符合的条目行")
        elif line.startswith(("- ", "#", "<", ">", "|", "`", " ", "--")):
            rows.append(("ℹ️ 上下文", line[:80] + ("…" if len(line) > 80 else ""), "非条目行，跳过"))
        else:
            rows.append(("❌ 格式", line[:80] + ("…" if len(line) > 80 else ""),
                         "不符合条目格式：`- **[标签]** [名称](URL) by [作者](URL) - 中文描述`，标签须为 production/beta/experimental"))
            problems.append("存在格式不符合的条目行")

    repo_reports = []
    for full in dict.fromkeys(repos):
        status, data = api(f"/repos/{full}")
        if status == 404:
            repo_reports.append(f"| ❌ | [{full}](https://github.com/{full}) | 仓库不存在或不可见 |")
            problems.append(f"新增条目指向的仓库 {full} 不存在")
            continue
        if status != 200 or data is None:
            repo_reports.append(f"| ⚠️ | [{full}](https://github.com/{full}) | API 异常 (HTTP {status}) |")
            continue
        lic = (data.get("license") or {}).get("spdx_id") or "未声明"
        note = f"{data.get('stargazers_count', 0)}★ · {lic} · 推送 {str(data.get('pushed_at', ''))[:10]}"
        bad = []
        if data.get("archived"):
            bad.append("已归档")
        if data.get("fork"):
            bad.append("是 fork")
        if lic in ("未声明", "NOASSERTION", "OTHER"):
            bad.append("无标准许可证")
        if bad:
            repo_reports.append(f"| ❌ | [{full}](https://github.com/{full}) | {note} · {'、'.join(bad)} |")
            problems.append(f"仓库 {full}：{'、'.join(bad)}")
        else:
            repo_reports.append(f"| ✅ | [{full}](https://github.com/{full}) | {note} |")
        time.sleep(0.3)

    print(f"共检查 {len([r for r in rows])} 行新增内容，其中 {ok_lines} 行符合条目格式。\n")
    if rows:
        print("| 判定 | 行内容（截断） | 说明 |")
        print("|---|---|---|")
        for v, content, note in rows:
            print(f"| {v} | `{content.replace('|', '\\|')}` | {note} |")
    if repo_reports:
        print("\n### 新增条目指向的仓库核验\n")
        print("| 判定 | 仓库 | 信息 |")
        print("|---|---|---|")
        print("\n".join(repo_reports))
    if problems:
        print("\n### 问题清单\n")
        for p in dict.fromkeys(problems):
            print(f"- {p}")
        print("\n**结论：存在需要修正的问题。**")
        return 1
    print("\n**结论：格式与仓库核验通过，等待维护者复核内容。**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
