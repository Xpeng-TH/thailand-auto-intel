#!/usr/bin/env python3
"""
生成报告后自动推送到 GitHub Pages
用法：python publish_to_github.py --date 2026-07-24
"""

import subprocess
import sys
import os
import re
from datetime import datetime

REPO_DIR = r"C:\Users\yanruikan\Documents\thailand-auto-intel"
# 注册 GitHub 后，将下面的 YOUR_USERNAME 替换为您的 GitHub 用户名
GITHUB_USERNAME = "Yuri1993-star"
REPO_NAME = "thailand-auto-intel"
GITHUB_PAGES_BASE = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"


def update_index(date_str: str):
    """更新 index.html 中的最新日期"""
    index_path = os.path.join(REPO_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 替换 latest 日期
    updated = re.sub(
        r'const latest = "[0-9-]+";',
        f'const latest = "{date_str}";',
        content
    )
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"index.html 已更新：最新日期 → {date_str}")


def git_push(date_str: str):
    """提交并推送到 GitHub"""
    cmds = [
        ["git", "-C", REPO_DIR, "add", "."],
        ["git", "-C", REPO_DIR, "commit", "-m", f"report: {date_str}"],
        ["git", "-C", REPO_DIR, "push", "origin", "main"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # commit 可能因为"nothing to commit"失败，属于正常
            if "nothing to commit" in result.stdout + result.stderr:
                print("无新变更，跳过 commit")
                continue
            print(f"命令失败：{' '.join(cmd)}")
            print(result.stderr)
            return False
    return True


def publish(date_str: str = None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    update_index(date_str)

    print("推送到 GitHub Pages...")
    if git_push(date_str):
        url = f"{GITHUB_PAGES_BASE}/reports/{date_str}.html"
        print(f"\n✅ 发布成功！报告外链：\n{url}\n")
        return url
    else:
        print("❌ 推送失败，请检查 Git 配置和网络。")
        return None


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    publish(date_arg)
