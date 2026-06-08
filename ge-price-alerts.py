"""
OSRS Guru GE 价格波动提醒系统
==============================
定时监控 OSRS Grand Exchange 热门物品价格，当波动超过阈值时发送通知。

功能:
- 每 5 分钟拉取 OSRS Wiki 实时价格
- 价格波动 >= 5% → 触发提醒
- 支持 Discord Webhook / Telegram Bot / 终端输出
- 可扩展：未来可接入 AI 推荐 "现在适合入手 XX"

用法:
    python ge-price-alerts.py                    # 终端模式，运行一次
    python ge-price-alerts.py --daemon           # 守护进程，每5分钟检查
    python ge-price-alerts.py --discord URL      # Discord 推送
    python ge-price-alerts.py --telegram TOKEN CHAT_ID  # Telegram 推送
"""

import os
import json
import time
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import httpx

# ============================================================
# 配置
# ============================================================
OSRS_PRICES_API = "https://prices.runescape.wiki/api/v1/osrs"
HEADERS = {"User-Agent": "OSRSGuru-PriceBot/1.0 (contact@osrsguru.com)"}
DATA_DIR = Path(__file__).parent / "data"
PRICE_LOG = DATA_DIR / "price_history.json"
ALERT_CONFIG = DATA_DIR / "alert_config.json"

# 默认监控的热门物品（物品名称 → 物品ID，启动时自动从 mapping 获取）
# 如果 mapping 里没有对应 ID，启动时会自动匹配
DEFAULT_WATCH_ITEMS = [
    "Twisted bow",
    "Scythe of vitur",
    "Tumeken's shadow",
    "Osmumten's fang",
    "Dragon claws",
    "Toxic blowpipe",
    "Necklace of anguish",
    "Berserker ring",
    "Bow of faerdhinen",
    "Dexterous prayer scroll",
    "Arcane prayer scroll",
    "Zenyte shard",
    "Enhanced crystal weapon seed",
    "Zulrah's scales",
    "Saradomin brew(4)",
    "Super restore(4)",
    "Prayer potion(4)",
    "Anglerfish",
    "Dragon bones",
    "Superior dragon bones",
    "Amethyst dart",
    "Ruby dragon bolts (e)",
    "Dragon warhammer",
    "Abyssal whip",
    "Bandos chestplate",
    "Armadyl chestplate",
    "Ancestral robe top",
    "Torva platebody",
    "Masori body",
    "Avernic defender hilt",
]

# 价格波动阈值（百分比）
PRICE_CHANGE_THRESHOLD = 5.0  # 5% 波动触发告警
CHECK_INTERVAL = 300           # 5 分钟


# ============================================================
# 数据获取
# ============================================================

def fetch_item_mapping() -> dict[int, str]:
    """获取物品 ID → 名称 映射"""
    resp = httpx.get(f"{OSRS_PRICES_API}/mapping", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return {item["id"]: item["name"] for item in resp.json()}


def fetch_latest_prices() -> dict[int, dict]:
    """获取所有物品最新价格"""
    resp = httpx.get(f"{OSRS_PRICES_API}/latest", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json().get("data", {})


def resolve_watch_items(mapping: dict[int, str]) -> dict[str, int]:
    """将物品名称匹配为 {name: item_id}"""
    resolved = {}
    name_lower_to_ids = {}
    for item_id, name in mapping.items():
        name_lower_to_ids.setdefault(name.lower(), []).append(item_id)

    for watch_name in DEFAULT_WATCH_ITEMS:
        wl = watch_name.lower()
        # 精确匹配
        if wl in name_lower_to_ids:
            resolved[watch_name] = name_lower_to_ids[wl][0]
        else:
            # 模糊匹配
            for name_lower, ids in name_lower_to_ids.items():
                if wl in name_lower:
                    resolved[watch_name] = ids[0]
                    break
    return resolved


# ============================================================
# 价格历史管理
# ============================================================

def load_price_history() -> dict:
    """加载上次价格快照"""
    if PRICE_LOG.exists():
        with open(PRICE_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_price_history(history: dict):
    """保存价格快照"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PRICE_LOG, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def detect_price_changes(
    current: dict[int, dict],
    previous: dict[str, dict],
    watch_items: dict[str, int],
) -> list[dict]:
    """检测价格波动，返回超过阈值的物品列表"""
    alerts = []

    for name, item_id in watch_items.items():
        item_id_str = str(item_id)
        if item_id_str not in current:
            continue

        curr_data = current[item_id_str]
        curr_high = curr_data.get("high", 0)
        curr_low = curr_data.get("low", 0)
        curr_avg = (curr_high + curr_low) / 2 if curr_high and curr_low else 0

        if item_id_str in previous:
            prev = previous[item_id_str]
            prev_avg = prev.get("avg_price", 0)
            if prev_avg > 0 and curr_avg > 0:
                change_pct = ((curr_avg - prev_avg) / prev_avg) * 100
                if abs(change_pct) >= PRICE_CHANGE_THRESHOLD:
                    direction = "up" if change_pct > 0 else "down"
                    alerts.append({
                        "name": name,
                        "item_id": item_id,
                        "high": curr_high,
                        "low": curr_low,
                        "avg": int(curr_avg),
                        "prev_avg": int(prev_avg),
                        "change_pct": round(change_pct, 2),
                        "direction": direction,
                    })

    return alerts


def update_price_history(current: dict[int, dict], watch_items: dict[str, int]) -> dict:
    """更新价格历史快照"""
    history = {}
    for name, item_id in watch_items.items():
        item_id_str = str(item_id)
        if item_id_str in current:
            data = current[item_id_str]
            avg = (data.get("high", 0) + data.get("low", 0)) / 2
            history[item_id_str] = {
                "name": name,
                "high": data.get("high", 0),
                "low": data.get("low", 0),
                "avg_price": int(avg),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
    return history


# ============================================================
# 通知渠道
# ============================================================

def format_alert_message(alerts: list[dict]) -> str:
    """格式化提醒消息（Markdown）"""
    if not alerts:
        return ""

    lines = [
        "## 💰 OSRS GE Price Alerts",
        f"*{datetime.now().strftime('%Y-%m-%d %H:%M')} UTC*",
        "",
    ]
    for a in alerts:
        emoji = "🟢" if a["direction"] == "up" else "🔴"
        lines.append(
            f"{emoji} **{a['name']}**: {a['avg']:,} GP "
            f"({a['direction']}: {a['change_pct']:+.1f}%)  |  "
            f"Buy: {a['low']:,}  /  Sell: {a['high']:,}"
        )

    lines.append("")
    lines.append(f"📊 *{len(alerts)} items with >{PRICE_CHANGE_THRESHOLD}% change*")
    lines.append("[View full guide on osrsguru.com](https://osrsguru.com)")
    return "\n".join(lines)


async def send_discord_webhook(webhook_url: str, message: str):
    """推送到 Discord 频道"""
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(webhook_url, json={"content": message})


async def send_telegram(bot_token: str, chat_id: str, message: str):
    """推送到 Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        })


# ============================================================
# 主循环
# ============================================================

def run_once(
    discord_url: str | None = None,
    telegram_token: str | None = None,
    telegram_chat: str | None = None,
):
    """运行一次价格检查"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking GE prices...")

    if not DATA_DIR.exists():
        print("[ERR] Run rag_indexer.py first to create data/ directory")
        return

    # 获取数据
    mapping = fetch_item_mapping()
    print(f"  Loaded {len(mapping)} item mappings")

    watch_items = resolve_watch_items(mapping)
    print(f"  Watching {len(watch_items)} items")

    prices = fetch_latest_prices()
    print(f"  Fetched {len(prices)} prices")

    # 检测变化
    previous = load_price_history()
    alerts = detect_price_changes(prices, previous, watch_items)

    if alerts:
        msg = format_alert_message(alerts)
        print(f"\n{msg}\n")

        # 推送通知
        if discord_url:
            import asyncio
            asyncio.run(send_discord_webhook(discord_url, msg))
            print("  [OK] Sent to Discord")

        if telegram_token and telegram_chat:
            import asyncio
            asyncio.run(send_telegram(telegram_token, telegram_chat, msg))
            print("  [OK] Sent to Telegram")
    else:
        print(f"  No significant changes (threshold: {PRICE_CHANGE_THRESHOLD}%)")

    # 保存快照
    new_history = update_price_history(prices, watch_items)
    save_price_history(new_history)
    print(f"  [OK] Price snapshot saved")


def run_daemon(
    discord_url: str | None = None,
    telegram_token: str | None = None,
    telegram_chat: str | None = None,
):
    """守护进程模式：每 5 分钟检查一次"""
    print("=" * 50)
    print("OSRS Guru GE Price Alert Daemon")
    print(f"Check interval: {CHECK_INTERVAL}s")
    print(f"Threshold: {PRICE_CHANGE_THRESHOLD}%")
    print("=" * 50)

    while True:
        try:
            run_once(discord_url, telegram_token, telegram_chat)
        except Exception as e:
            print(f"[ERR] {e}")

        print(f"  Next check in {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL)


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OSRS GE Price Alert System")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    parser.add_argument("--discord", type=str, help="Discord webhook URL")
    parser.add_argument("--telegram", type=str, nargs=2, metavar=("TOKEN", "CHAT_ID"),
                        help="Telegram Bot Token + Chat ID")
    parser.add_argument("--threshold", type=float, default=PRICE_CHANGE_THRESHOLD,
                        help=f"Price change threshold %% (default: {PRICE_CHANGE_THRESHOLD})")
    args = parser.parse_args()

    if args.threshold:
        PRICE_CHANGE_THRESHOLD = args.threshold

    tg_token = args.telegram[0] if args.telegram else None
    tg_chat = args.telegram[1] if args.telegram else None

    if args.daemon:
        run_daemon(args.discord, tg_token, tg_chat)
    else:
        run_once(args.discord, tg_token, tg_chat)
