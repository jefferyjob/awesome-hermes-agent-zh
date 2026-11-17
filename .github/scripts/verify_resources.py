#!/usr/bin/env python3
"""核验资源推荐 issue 中出现的 GitHub 仓库。

用法: verify_resources.py <issue文本文件> <本仓库README路径>
输出: Markdown 核验报告（stdout）
退出码: 0 = 全部通过（可作为自动收录依据）; 1 = 存在不通过项
"""
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
OWN_REPO = "jefferyjob/awesome-hermes-agent-zh"
REPO_RE = re.compile(r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
STALE_DAYS = 180


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


def extract_repos(text):
    repos = []
    for owner, name in REPO_RE.findall(text):
        name = re.sub(r"\.(git|md|json|yaml|yml)$", "", name)
        full = f"{owner}/{name}"
        if full == OWN_REPO or full not in repos:
            repos.append(full)
    return repos


def main():
    if len(sys.argv) != 3:
        print("用法: verify_resources.py <issue文本> <README路径>", file=sys.stderr)
        return 2
    text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    readme = open(sys.argv[2], encoding="utf-8").read()
    repos = extract_repos(text)

    if not repos:
        print("未在 issue 正文中识别到 GitHub 仓库链接，无法自动核验，请人工判断。")
        return 1

    rows = []
    all_pass = True
    for full in repos:
        status, data = api(f"/repos/{full}")
        problems = []
        if status == 404:
            problems.append("仓库不存在或不可见")
        elif status != 200 or data is None:
            problems.append(f"API 异常 (HTTP {status})")
        else:
            lic = (data.get("license") or {}).get("spdx_id") or "未声明"
            pushed = data.get("pushed_at") or ""
            stars = data.get("stargazers_count", 0)
            if data.get("archived"):
                problems.append("已归档")
            if data.get("fork"):
                problems.append("是 fork")
            if lic in ("未声明", "NOASSERTION", "OTHER"):
                problems.append("无标准许可证")
            if pushed:
                days = (datetime.now(timezone.utc) - datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days
                if days > STALE_DAYS:
                    problems.append(f"{days} 天未推送")
            if stars == 0:
                problems.append("暂无 star")
            s_readme, _ = api(f"/repos/{full}/readme")
            if s_readme == 404:
                problems.append("无 README")

        dup = re.search(re.escape("github.com/" + full), readme, re.I)
        if dup:
            problems.append("已收录")

        if any(p in ("仓库不存在或不可见", "已归档", "是 fork", "无标准许可证", "已收录") for p in problems):
            verdict = "❌"
            all_pass = False
        elif problems:
            verdict = "⚠️"
        else:
            verdict = "✅"

        if status == 200 and data is not None:
            lic = (data.get("license") or {}).get("spdx_id") or "未声明"
            info = f"{data.get('stargazers_count', 0)}★ · {lic} · 推送 {str(data.get('pushed_at', ''))[:10]}"
        else:
            info = "—"
        rows.append((verdict, full, info, "、".join(problems) or "无"))
        time.sleep(0.3)

    print("自动核验了 issue 中提到的仓库（判断依据：CONTRIBUTING 质量标准）\n")
    print("| 判定 | 仓库 | 信息 | 问题 |")
    print("|---|---|---|---|")
    for v, full, info, problems in rows:
        print(f"| {v} | [{full}](https://github.com/{full}) | {info} | {problems} |")
    print("\n判定说明：✅ 通过；⚠️ 通过但需留意（新项目 / 疑似停滞）；❌ 不通过（不存在 / 已归档 / fork / 无标准许可证 / 已收录）。")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
