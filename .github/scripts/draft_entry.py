#!/usr/bin/env python3
"""为核验通过的资源推荐 issue 起草中文收录条目 + 判定所属分区。

用法:
  draft_entry.py --repo <owner/name> [--issue-title <标题>] --out <输出JSON路径>

输出 JSON: {"entry": "完整条目行", "section": "分区锚点", "repo": "owner/name"}

环境变量:
  OPENAI_API_KEY    必填
  OPENAI_MODEL      可选，默认 gpt-5.1
  OPENAI_BASE       可选，默认 https://api.openai.com/v1（可指向兼容端点）
  GH_TOKEN          用于读取仓库信息

退出码: 0 = 成功; 非 0 = 失败
"""
import argparse
import base64
import json
import os
import sys
import urllib.request

SECTIONS = {
    "community-skills": "社区技能",
    "agentskillsio-ecosystem": "agentskills.io 生态",
    "plugins": "插件",
    "skill-registries--discovery": "技能注册表与发现",
    "memory-providers": "记忆提供方",
    "tools--utilities": "工具与实用程序",
    "deployment": "部署",
    "integrations--bridges": "集成与桥接",
    "detection--media-forensics": "检测与媒体取证",
    "multi-agent--swarms": "多 Agent 与 Swarm",
    "domain-applications": "领域应用",
    "forks--derivatives": "分叉与衍生项目",
    "guides--documentation": "指南与文档",
}


def http_json(url, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "awesome-hermes-zh-triage"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_model(api_key, base, model, system_prompt, user_prompt):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": int(os.environ.get("OPENAI_MAX_TOKENS", "8192")),
    }
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"API 返回 HTTP {e.code}: {detail}") from e
    choice = data["choices"][0]
    content = (choice.get("message") or {}).get("content") or ""
    if not content.strip():
        raise RuntimeError(f"模型未返回内容: {json.dumps(data)[:500]}")
    return content.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--issue-title", default="")
    p.add_argument("--out", required=True)
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

    section_list = "\n".join(f"- `{k}` = {v}" for k, v in SECTIONS.items())
    system_prompt = (
        "你是 GitHub awesome 列表（中文）的编辑。根据仓库信息起草收录条目并判定分区。"
        "只输出一个 JSON 对象（不要代码围栏、不要解释），字段：\n"
        '{"entry": "完整条目行", "section": "分区锚点"}\n'
        "entry 格式（严格遵守）：`- **[标签]** [显示名称](仓库URL) by [作者](作者URL) - 中文描述`，一行；"
        "标签只能是 production/beta/experimental，保守判定：项目不足3个月或无公开采用记录→experimental；"
        "有发布/测试/完整文档但采用有限→beta；仅当有明显生产使用证据→production。"
        "描述 1~3 句：它是什么 + 对 Hermes agent 用户的价值；涉及 API key/付费/高权限的写明边界；不得编造功能。\n"
        f"section 只能从以下锚点中选一个：\n{section_list}"
    )
    user_prompt = (
        f"仓库: {args.repo}\n"
        f"元数据: {meta}\n"
        f"官方描述: {desc}\n"
        f"issue标题: {args.issue_title}\n"
        f"README节选:\n{readme}\n"
    )

    try:
        out = call_model(api_key, base, model, system_prompt, user_prompt)
    except Exception as e:
        print(f"模型调用失败: {e}", file=sys.stderr)
        return 1

    # 容错：剥掉可能的代码围栏
    out = out.strip()
    if out.startswith("```"):
        out = out.strip("`")
        if out.startswith("json"):
            out = out[4:]
        out = out.strip()
    try:
        obj = json.loads(out)
    except json.JSONDecodeError:
        print(f"模型输出不是有效 JSON: {out[:200]}", file=sys.stderr)
        return 1

    entry = str(obj.get("entry", "")).strip()
    section = str(obj.get("section", "")).strip()
    if not entry.startswith("- **["):
        print(f"条目格式无效: {entry[:100]}", file=sys.stderr)
        return 1
    if section not in SECTIONS:
        print(f"分区无效: {section}", file=sys.stderr)
        return 1

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"entry": entry, "section": section, "repo": args.repo}, f, ensure_ascii=False)
    print(f"起草完成: {section} <- {entry[:60]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
