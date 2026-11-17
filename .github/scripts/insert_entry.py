#!/usr/bin/env python3
"""把收录条目插入 README 指定分区末尾，并登记到本地条目白名单。

用法:
  insert_entry.py --anchor <分区锚点> --repo <owner/name> --line "<完整条目行>" \
      [--readme README.md] [--local-file .github/local-entries.txt]

退出码: 0 = 成功
"""
import argparse
import re
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--readme", default="README.md")
    p.add_argument("--anchor", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--line", required=True)
    p.add_argument("--local-file", default=".github/local-entries.txt")
    args = p.parse_args()

    if not args.line.startswith("- **["):
        print(f"条目行格式无效: {args.line[:80]}", file=sys.stderr)
        return 1

    with open(args.readme, encoding="utf-8") as f:
        lines = f.read().splitlines()

    anchor_pos = None
    for i, l in enumerate(lines):
        if f'<a id="{args.anchor}"></a>' in l:
            anchor_pos = i
            break
    if anchor_pos is None:
        print(f"锚点不存在: {args.anchor}", file=sys.stderr)
        return 1

    # 分区范围 = 锚点之后（跳过分区自身标题）到下一个标题之前；找最后一个条目行
    last_entry = None
    heading_re = re.compile(r"^#{1,3} ")
    heading_seen = 0
    for i in range(anchor_pos + 1, len(lines)):
        if heading_re.match(lines[i]):
            heading_seen += 1
            if heading_seen > 1:  # 第一个是分区自己的标题，第二个即进入下一分区
                break
            continue
        if lines[i].startswith("- **["):
            last_entry = i
    if last_entry is None:
        print(f"分区 {args.anchor} 中未找到现有条目", file=sys.stderr)
        return 1

    if any(args.repo in l for l in lines):
        print(f"README 中已存在 {args.repo}，跳过插入", file=sys.stderr)
        return 1

    lines.insert(last_entry + 1, args.line)
    with open(args.readme, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # 登记到白名单（同步校验时放行该本地条目）
    existing = set()
    try:
        with open(args.local_file, encoding="utf-8") as f:
            existing = {l.strip() for l in f if l.strip()}
    except FileNotFoundError:
        pass
    if args.repo not in existing:
        with open(args.local_file, "a", encoding="utf-8") as f:
            f.write(args.repo + "\n")

    print(f"已插入 {args.anchor} 分区末尾（第 {last_entry + 2} 行），白名单已登记 {args.repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
