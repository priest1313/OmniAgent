"""OmniAgent Agent Hands: run commands posted in a vibe-run issue, report results as a comment.

Protocol:
  1. owner opens an issue, each command on its own line prefixed with `$ `
  2. `$` literals inside commands must be escaped as backslash-dollar
  3. owner adds the `vibe-run` label -> this script runs on ubuntu-latest
"""
import os
import re
import subprocess

MAX_HEAD = 40000
MAX_TAIL = 12000
RUN_TIMEOUT = 900

USAGE = (
    "## 🤖 Agent Hands\n\n"
    "هیچ فرمانی پیدا نشد. فرمان‌ها را در بدنه Issue بنویس، هر خط با `$` شروع شود:\n\n"
    "```bash\n"
    "$ echo سلام\n"
    "$ gradle assembleDebug\n"
    "```\n\n"
    "سپس لیبل `vibe-run` را به Issue اضافه کن.\n"
)


def extract_commands(body):
    cmds = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("$"):
            continue
        cmds.append(re.sub(r"^\\?\$", "", stripped, count=1).strip())
    return cmds


def run_commands(cmds):
    log_parts = []
    failures = 0
    for cmd in cmds:
        log_parts.append(f"\n$ {cmd}")
        try:
            proc = subprocess.run(
                ["bash", "-c", cmd],
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT,
            )
            log_parts.append(proc.stdout or "")
            if proc.stderr:
                log_parts.append(proc.stderr)
            log_parts.append(f"[exit: {proc.returncode}]\n")
            if proc.returncode != 0:
                failures += 1
        except subprocess.TimeoutExpired:
            log_parts.append("⏱ بیش از 15 دقیقه طول کشید و قطع شد\n")
            failures += 1
    log = "\n".join(log_parts)
    rc = 0 if failures == 0 else 1
    return rc, log


def truncate(text):
    if len(text) <= MAX_HEAD + MAX_TAIL:
        return text
    return (
        text[:MAX_HEAD]
        + f"\n\n... [خروجی بلند بود؛ {len(text) - MAX_HEAD - MAX_TAIL} کاراکتر حذف شد]\n\n"
        + text[-MAX_TAIL:]
    )


def post_comment(md):
    with open("/tmp/comment.md", "w") as f:
        f.write(md)
    subprocess.run(["gh", "issue", "comment", ISSUE_NUMBER, "--body-file", "/tmp/comment.md"], check=False)


def main():
    cmds = extract_commands(ISSUE_BODY)
    if not cmds:
        post_comment(USAGE)
        return

    rc, log = run_commands(cmds)
    fence = "````" if "```" in log else "```"
    status = "✅ موفق" if rc == 0 else "❌ یک یا چند فرمان شکست خورد"
    log = truncate(log)
    md = (
        "## 🤖 Agent Hands — گزارش اجرا\n\n"
        f"وضعیت: {status}\n\n"
        f"{fence}bash\n{log}\n{fence}\n"
    )
    post_comment(md)


if __name__ == "__main__":
    main()
