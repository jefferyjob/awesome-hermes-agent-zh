#!/usr/bin/env python3
"""为核验通过的资源推荐 issue 起草一条中文收录条目（输出单行到 stdout）。

用法: draft_entry.py --repo <owner/name> [--issue-title <issue标题>]

环境变量: OPENAI_API_KEY（必填）、OPENAI_MODEL（默认 gpt-5.1）、OPENAI_BASE、GH_TOKEN
退出码: 0 = 成功; 非 0 = 失败
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.request

OUT_RE = re.compile(r"^\s*`\s*(- \*\*\[(?:production|beta|experimental)\]\*\*.*)`\s*$", re.S)


def http_json(url, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "awesome-hermes-zh-triage"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_model(api_key, base, model, prompt):
    body = {"model": model, "input": prompt, "max_output_tokens": 2000}
    req = urllib.request.Request(
        base.rstrip("/") + "/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    texts = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") in ("output_text", "text"):
                    texts.append(part.get("text", ""))
    return "".join(texts).strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--issue-title", default="")
    args = p.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("未设置 OPENAI_API_KEY", file=sys.stderr)
        return 2
    base = os.environ.get("OPENAI_BASE", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-5.1")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")

    try:
        repo = http_json(f"https://api.github.com/repos/{args.repo}", token)
        desc = repo.get("description") or ""
        meta = f"{repo.get('stargazers_count')} stars, license={(repo.get('license') or {}).get('spdx_id')}, pushed={repo.get('pushed_at')}, created={repo.get('created_at')}"
        readme = ""
        try:
            rd = http_json(f"https://api.github.com/repos/{args.repo}/readme", token)
            readme = base64.b64decode(rd.get("content", "")).decode("utf-8", "replace")[:1500]
        except Exception:
            pass
    except Exception as e:
        print(f"获取仓库信息失败: {e}", file=sys.stderr)
        return 1

    prompt = (
        "你是 GitHub awesome 列表（中文）的编辑。请为以下仓库起草一行收录条目。\n"
        "格式（严格遵守，只输出这一行，不要解释、不要代码围栏）：\n"
        "- **[标签]** [显示名称](仓库URL) by [作者](作者URL) - 中文描述（1~3句）\n\n"
        "要求：\n"
        "1. 标签只能是 production/beta/experimental，保守判定：项目不足3个月或无公开采用记录→experimental；"
        "有发布/测试/完整文档但采用有限→beta；仅当有明显生产使用证据→production。\n"
        "2. 描述说明它是什么 + 对 Hermes agent 用户的实际价值；涉及 API key/付费/高权限的要写明边界；不得编造功能。\n"
        "3. 显示名称用项目名（可保留英文），URL 用仓库地址。\n\n"
        f"仓库: {args.repo}\n"
        f"元数据: {meta}\n"
        f"描述: {desc}\n"
        f"issue标题: {args.issue_title}\n"
        f"README节选:\n{readme}\n"
    )

    try:
        out = call_model(api_key, base, model, prompt)
    except Exception as e:
        print(f"模型调用失败: {e}", file=sys.stderr)
        return 1

    out = out.strip()
    m = OUT_RE.match(out)  # 容错：整个输出被反引号包裹
    if m:
        out = m.group(1)
    out = out.splitlines()[0].strip().strip("`") if out else ""
    if not out.startswith("- **["):
        print(f"模型输出不是有效条目: {out[:100]}", file=sys.stderr)
        return 1
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
