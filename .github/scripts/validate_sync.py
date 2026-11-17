#!/usr/bin/env python3
"""结构化校验翻译后的 README 是否合格（同步流水线的质量闸门）。

用法:
  validate_sync.py --upstream <上游README> --candidate <新中文README> \
      --current <旧中文README> [--repo-root .]

校验项:
  1. 条目覆盖：上游所有条目链接必须出现在候选文件中（允许白名单本地条目多出）
  2. 章节结构：二级/三级标题数量与上游一致
  3. 条目格式：所有 `- **[...]` 行符合收录格式
  4. 锚点：id 唯一且目录链接都有对应锚点
  5. 本地适配项：翻译声明 / Hermes Tweet / 本仓库贡献链接存在
  6. 图片：候选文件引用的本地图片文件必须存在

退出码: 0 = 通过; 1 = 不通过（报告输出到 stdout）
"""
import argparse
import os
import re
import sys

ENTRY_RE = re.compile(r"^\- \*\*\[(production|beta|experimental)\]\*\*\s*\[[^\]]+\]\(\S+\)(?:\s+by\s+\[[^\]]+\]\(\S+\))?.*\s-\s\S.*")
GITHUB_URL_RE = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")


def load_allowed_extras(path=".github/local-entries.txt"):
    """本地保留条目白名单：.github/local-entries.txt + 固定的 Hermes Tweet。"""
    allowed = {"Xquik-dev/hermes-tweet"}
    try:
        with open(path, encoding="utf-8") as f:
            allowed |= {l.strip() for l in f if l.strip()}
    except FileNotFoundError:
        pass
    return allowed
REQUIRED_STRINGS = ["翻译自", "Hermes Tweet", "jefferyjob/awesome-hermes-agent-zh/issues"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def entries(text):
    """提取条目行中的 owner/repo 集合。"""
    repos = set()
    for line in text.splitlines():
        if line.startswith("- **["):
            for full in GITHUB_URL_RE.findall(line):
                repos.add(full)
    return repos


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--upstream", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--current", required=True)
    p.add_argument("--repo-root", default=".")
    args = p.parse_args()

    upstream = read(args.upstream)
    candidate = read(args.candidate)
    current = read(args.current)
    problems, warnings = [], []

    # 1. 条目覆盖
    up_repos, cand_repos = entries(upstream), entries(candidate)
    missing = sorted(up_repos - cand_repos)
    if missing:
        problems.append(f"上游条目未覆盖（{len(missing)} 条）: " + ", ".join(missing))
    extras = sorted(cand_repos - up_repos)
    allowed = load_allowed_extras()
    unexpected = [r for r in extras if r not in allowed]
    if unexpected:
        problems.append("候选文件多出未知条目（不在上游也不在本地白名单）: " + ", ".join(unexpected))

    # 2. 章节结构
    for level in ("## ", "### "):
        n_up = sum(1 for l in upstream.splitlines() if l.startswith(level))
        n_cand = sum(1 for l in candidate.splitlines() if l.startswith(level))
        if n_up != n_cand:
            problems.append(f"标题结构不一致: '{level}' 上游 {n_up} 个，候选 {n_cand} 个")

    # 3. 条目格式
    bad_lines = [l for l in candidate.splitlines() if l.startswith("- **[") and not ENTRY_RE.match(l)]
    if bad_lines:
        problems.append(f"{len(bad_lines)} 行条目格式不符合规范，例如: " + bad_lines[0][:80])

    # 4. 锚点
    ids = re.findall(r'<a id="([^"]+)"></a>', candidate)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        problems.append("锚点 id 重复: " + ", ".join(sorted(dup)))
    linked = set(re.findall(r"\]\(#([^)]+)\)", candidate))
    orphan = sorted(linked - set(ids))
    if orphan:
        problems.append("目录/内链指向不存在的锚点: " + ", ".join(orphan))

    # 5. 本地适配项
    for s in REQUIRED_STRINGS:
        if s not in candidate:
            problems.append(f"缺少本地适配内容: “{s}”")

    # 6. 图片存在性
    for img in sorted(set(re.findall(r'(?:src="|\()((?:assets/)[^")\s]+)', candidate))):
        if not os.path.exists(os.path.join(args.repo_root, img)):
            problems.append(f"引用的本地图片不存在: {img}")

    # 参考警告：与旧版几乎相同 → 疑似没有真正合入上游变化
    if candidate == current:
        problems.append("候选文件与当前版本完全相同，疑似未执行翻译")

    if problems:
        print("### ❌ 同步校验未通过\n")
        for item in problems:
            print(f"- {item}")
        for w in warnings:
            print(f"- ⚠️ {w}")
        return 1
    print("### ✅ 同步校验通过\n")
    print(f"- 上游条目全覆盖（{len(up_repos)} 条）")
    print(f"- 本地保留条目: {sorted(cand_repos - up_repos)}")
    for w in warnings:
        print(f"- ⚠️ {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
