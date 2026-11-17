#!/usr/bin/env python3
"""调用 OpenAI API 将上游 README 的变化翻译合入当前中文 README。

用法:
  run_sync_translation.py --upstream <上游README> --current <当前中文README> \
      --agents <AGENTS.md> --out <输出文件>

环境变量:
  OPENAI_API_KEY      必填
  OPENAI_MODEL        可选，默认 gpt-5.1
  OPENAI_BASE         可选，默认 https://api.openai.com/v1（可指向任意 OpenAI 兼容端点，如智谱 https://open.bigmodel.cn/api/paas/v4）
  OPENAI_MAX_TOKENS   可选，默认 32768

退出码: 0 = 成功生成; 非 0 = 失败（错误信息输出到 stderr）
"""
import argparse
import json
import os
import re
import sys
import urllib.request


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def call_model(api_key, base, model, system_prompt, user_prompt, max_tokens):
    """兼容 OpenAI /chat/completions 及其兼容端点（智谱 BigModel 等）。"""
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=1800) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"API 返回 HTTP {e.code}: {detail}") from e
    try:
        choice = data["choices"][0]
    except (KeyError, IndexError):
        raise RuntimeError(f"API 响应缺少 choices: {json.dumps(data)[:500]}")
    if choice.get("finish_reason") == "length":
        raise RuntimeError("模型输出被截断（finish_reason=length），请增大 OPENAI_MAX_TOKENS 或换更大输出上限的模型")
    content = (choice.get("message") or {}).get("content") or ""
    if not content.strip():
        raise RuntimeError(f"模型未返回内容: {json.dumps(data)[:500]}")
    return content


def strip_fences(text):
    """去掉整体被 ```markdown ... ``` 包裹的情况。"""
    m = re.fullmatch(r"\s*```[a-zA-Z]*\n(.*)\n```\s*", text, re.S)
    return m.group(1) if m else text.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--upstream", required=True)
    p.add_argument("--current", required=True)
    p.add_argument("--agents", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--max-output-tokens", type=int, default=None)
    args = p.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("错误: 未设置 OPENAI_API_KEY", file=sys.stderr)
        return 2
    base = os.environ.get("OPENAI_BASE", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-5.1")
    max_tokens = args.max_output_tokens or int(os.environ.get("OPENAI_MAX_TOKENS", "32768"))

    upstream = read(args.upstream)
    current = read(args.current)
    agents = read(args.agents)

    system_prompt = (
        "你是维护一个 GitHub awesome 列表中文翻译镜像的资深技术译者兼工程师。\n"
        "任务：以英文上游 README 为唯一事实来源，把它的全部变化翻译并合入当前中文 README，"
        "输出更新后的完整 README.md 的 Markdown 源码。\n"
        "硬性规则：\n"
        "1. 只输出最终 README 内容本身，不要任何解释、前言、结语或 Markdown 代码围栏。\n"
        "2. 忠实翻译，不增删任何条目或事实；成熟度标签（production/beta/experimental）与条目排序严格跟随上游。\n"
        "3. 条目格式：`- **[标签]** [名称](URL) by [作者](URL) - 中文描述`，一行一条，描述不超过原文信息量。\n"
        "4. 保留本地适配项（详见 AGENTS.md）：顶部翻译声明、Hermes Tweet 条目、参与贡献链接指向本仓库、"
        "每个章节标题前的 `<a id=\"英文锚点\"></a>`、图片使用本仓库 assets/ 相对路径。\n"
        "5. 上游没有而中文版有的内容原样保留；上游删除的内容随之删除。\n"
        "6. 章节结构（标题数量与层级）与上游一一对应。\n"
        "7. URL、代码、专有名词保持原样。\n"
        "8. 若上游引用了 assets/ 下的新图片，保留相对路径引用（文件由流水线负责复制）。\n"
        "输出会被程序自动校验（条目覆盖率、锚点、格式），任何缺漏都会导致整个结果被拒绝。"
    )
    user_prompt = (
        "=== AGENTS.md（规则，必须遵守）===\n"
        f"{agents}\n\n"
        "=== 上游最新 README（英文，事实来源）===\n"
        f"{upstream}\n\n"
        "=== 当前中文 README（基于上游旧版本，需被更新的对象）===\n"
        f"{current}\n\n"
        "现在输出更新后的完整中文 README.md 源码。"
    )

    try:
        text = call_model(api_key, base, model, system_prompt, user_prompt, max_tokens)
    except Exception as e:
        print(f"模型调用失败: {e}", file=sys.stderr)
        return 1

    text = strip_fences(text)
    if "# Awesome Hermes Agent" not in text:
        print("错误: 输出缺少标题，疑似无效输出", file=sys.stderr)
        return 1
    if len(text) < len(current) * 0.5:
        print(f"错误: 输出长度异常（{len(text)} < 当前 {len(current)} 的一半）", file=sys.stderr)
        return 1

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"翻译完成: 输出 {len(text)} 字符，写入 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
