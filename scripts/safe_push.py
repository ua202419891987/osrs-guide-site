#!/usr/bin/env python3
# OSRS Guru - 一键安全推送脚本
# 作用：自动排除红线5篇(Early-Access embargo < 2026-08-23，覆盖 en/zh/pt-br)
#       + 排除 CD/WR 子目录，自动扁平化本地未推 commit，避免反复试验/反复推送。
# 用法：
#   python scripts/safe_push.py <file1> <file2> ... [--from-stash] [--msg "commit message"]
# 例：
#   python scripts/safe_push.py guides/osrs-best-money-making-methods-2026.html guides/osrs-ironman-early-game-guide-2026.html guides/osrs-charged-item-lost-on-death-fix-2026.html --msg "feat: push 3 articles"
#   python scripts/safe_push.py guides/osrs-ironman-early-game-guide-2026.html --from-stash
import sys, subprocess, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 红线5篇（无扩展名，自动覆盖 .html 及 en/zh/pt-br 三种路径）
REDLINE = {
    "osrs-how-to-make-money-with-zulrah",
    "osrs-wilderness-bosses-guide-2026",
    "osrs-gauntlet-meta-changes-2026",
    "osrs-hunter-money-making-guide-2026",
    "osrs-slayer-70-to-95-money-makers-2026",
}
# 明确排除的子目录
EXCLUDE_PREFIX = ("guides/crimson-desert/", "guides/windrose/")


def run(*args, check=True):
    r = subprocess.run(list(args), cwd=REPO, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("❌ 命令失败:", " ".join(args))
        if r.stderr.strip():
            print(r.stderr)
        sys.exit(1)
    return r


def norm(p):
    return p.replace("\\", "/")


def base(p):
    return os.path.splitext(os.path.basename(p))[0]


def blocked(path):
    n = norm(path)
    reasons = []
    if base(n) in REDLINE:
        reasons.append("红线5篇(Early-Access embargo < 2026-08-23)")
    for px in EXCLUDE_PREFIX:
        if px in n:
            reasons.append(f"排除目录 {px}")
    return reasons


def main():
    raw = sys.argv[1:]
    if not raw:
        print("用法: python scripts/safe_push.py <file1> <file2> ... [--from-stash] [--msg \"commit msg\"]")
        sys.exit(2)

    from_stash = "--from-stash" in raw
    raw = [a for a in raw if a != "--from-stash"]

    msg = "chore: safe push"
    if "--msg" in raw:
        i = raw.index("--msg")
        if i + 1 >= len(raw):
            print("❌ --msg 后面需要跟 commit 信息")
            sys.exit(2)
        msg = raw[i + 1]
        raw = raw[:i] + raw[i + 2:]

    files = raw
    if not files:
        print("❌ 未指定任何文件")
        sys.exit(2)

    # 1. 校验目标文件
    for f in files:
        r = blocked(f)
        if r:
            print(f"❌ 拒绝推送 {f}: {', '.join(r)}")
            sys.exit(1)
    print(f"✅ 目标 {len(files)} 个文件均安全（非红线 / 非 CD/WR）")

    # 2. 如需从 stash 取新版
    if from_stash:
        run("git", "checkout", "stash@{0}", "--", *files)
        print("✅ 已从 stash@{0} 取出指定文件到磁盘")

    # 3. 拉取远端最新基线（单人仓库，确保 reset 基线正确）
    run("git", "fetch", "origin", "main")
    print("✅ 已 fetch origin/main")

    # 4. 若有本地未推 commit（可能夹带红线），自动扁平化保留工作树
    ahead = run("git", "rev-list", "--count", "origin/main..HEAD", check=False)
    if ahead.returncode == 0 and ahead.stdout.strip() not in ("", "0"):
        print(f"⚠️ 本地有 {ahead.stdout.strip()} 个未推 commit，自动扁平化（reset --soft origin/main，改动不丢失）")
        run("git", "reset", "--soft", "origin/main")
        run("git", "restore", "--staged", ".")
        print("✅ 已扁平化，所有改动回到工作树（未提交）")

    # 5. 精确 add 指定文件
    run("git", "add", *files)
    print(f"✅ 已暂存 {len(files)} 个文件")

    # 6. 二次校验暂存区（防误加）
    staged = run("git", "diff", "--cached", "--name-only").stdout.splitlines()
    for s in staged:
        r = blocked(s)
        if r:
            print(f"❌ 暂存区含红线/排除文件 {s}: {', '.join(r)}，已撤销暂存")
            run("git", "restore", "--staged", ".")
            sys.exit(1)

    if not staged:
        print("⚠️ 暂存区为空，可能文件已与线上一致，无需推送")
        sys.exit(0)

    # 7. commit + push
    run("git", "commit", "-m", msg)
    print("✅ 已提交")
    run("git", "push", "origin", "main")
    head = run("git", "rev-parse", "origin/main").stdout.strip()
    print(f"🎉 推送成功，远端 HEAD = {head}")


if __name__ == "__main__":
    main()
