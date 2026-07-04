#!/usr/bin/env python3
"""
OSRS Gear Recommender — GE 价格自动更新脚本

从 OSRS Wiki API 获取最新 GE 价格，更新 gear-database.json 中的价格数据。

工作流程：
  1. 从 Wiki API 获取最新的价格映射（item name → price）
  2. 加载 gear-database.json
  3. 遍历所有物品，匹配名称，更新 ge_price_estimate 和 ge_price_category
  4. 更新 meta.last_updated 时间戳
  5. 写入更新后的 JSON 文件

用法:
  python scripts/update-prices.py

环境变量:
  OSRS_USER_AGENT: 自定义 User-Agent（可选，默认使用 osrsguru-bot）

依赖:
  requests (pip install requests)

API 文档:
  https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip install requests")
    sys.exit(1)


# =============================================================================
# 配置
# =============================================================================

# 项目根目录（脚本所在目录的上级）
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据库文件路径
DATABASE_PATH = BASE_DIR / "data" / "gear-database.json"

# OSRS Wiki 价格 API
PRICES_API = "https://prices.runescape.wiki/api/v1/osrs/latest"
MAPPING_API = "https://prices.runescape.wiki/api/v1/osrs/mapping"

# API 请求间隔（秒）- 遵守 Wiki 的限流要求
API_DELAY_SECONDS = 3

# User-Agent（Wiki 要求提供）
USER_AGENT = os.environ.get(
    "OSRS_USER_AGENT",
    "osrsguru-gear-tool/1.0 (https://osrsguru.com; contact@osrsguru.com)"
)

# 请求头
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

# 价格区间阈值（与 gear-database.json 中的分类一致）
PRICE_TIERS = [
    ("free", 0, 0),
    ("cheap", 1, 49999),
    ("medium", 50000, 499999),
    ("expensive", 500000, 49999999),
    ("biS", 50000000, float("inf")),
]


# =============================================================================
# 工具函数
# =============================================================================

def log(message: str, level: str = "INFO"):
    """统一日志输出"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def get_price_category(price: float) -> str:
    """
    根据价格确定价格区间分类

    Args:
        price: 物品价格（GP）

    Returns:
        价格区间标签: free | cheap | medium | expensive | biS
    """
    for category, min_price, max_price in PRICE_TIERS:
        if min_price <= price <= max_price:
            return category
    return "biS"


def fetch_json(url: str, retries: int = 3) -> dict | None:
    """
    带重试机制的 JSON API 请求

    Args:
        url: API URL
        retries: 最大重试次数

    Returns:
        JSON 响应字典，失败返回 None
    """
    for attempt in range(1, retries + 1):
        try:
            log(f"Fetching {url} (attempt {attempt}/{retries})")
            response = requests.get(url, headers=HEADERS, timeout=30)

            if response.status_code == 429:
                # 限流了，等待更久
                wait_time = 10 * attempt
                log(f"Rate limited (429), waiting {wait_time}s...", "WARN")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            data = response.json()

            if not data or "data" not in data:
                log(f"Unexpected response format from {url}", "ERROR")
                return None

            return data

        except requests.exceptions.Timeout:
            log(f"Timeout fetching {url}", "WARN")
            time.sleep(5 * attempt)

        except requests.exceptions.RequestException as e:
            log(f"Request failed: {e}", "ERROR")
            if attempt < retries:
                wait = 3 * attempt
                log(f"Retrying in {wait}s...", "INFO")
                time.sleep(wait)

    log(f"All {retries} attempts failed for {url}", "ERROR")
    return None


# =============================================================================
# 核心逻辑
# =============================================================================

def fetch_item_mapping() -> dict:
    """
    从 Wiki API 获取物品名称到 OSRS item ID 的映射

    API 返回:
        {"data": [{"id": 2, "name": "Cannonball", ...}, ...]}

    Returns:
        { "item name (lowercase)": osrs_item_id, ... }
    """
    log("Fetching item name-to-ID mapping...")
    data = fetch_json(MAPPING_API)

    if not data:
        log("Failed to fetch item mapping", "ERROR")
        return {}

    mapping = {}
    for item in data.get("data", []):
        name_lower = item.get("name", "").lower().strip()
        if name_lower:
            mapping[name_lower] = item.get("id")

    log(f"Mapping loaded: {len(mapping)} items")
    return mapping


def fetch_price_data() -> dict:
    """
    从 Wiki API 获取最新 GE 价格

    API 返回:
        {"data": { "2": {"high": 150, "low": 120, ...}, ... }}

    Returns:
        { osrs_item_id: {"high": int, "low": int, "avg": int}, ... }
    """
    log("Fetching latest GE prices...")
    data = fetch_json(PRICES_API)

    if not data:
        log("Failed to fetch price data", "ERROR")
        return {}

    prices = {}
    raw_data = data.get("data", {})

    for osrs_id_str, price_point in raw_data.items():
        high = price_point.get("high") or 0
        low = price_point.get("low") or 0
        avg = round((high + low) / 2) if (high + low) > 0 else 0

        prices[int(osrs_id_str)] = {
            "high": high,
            "low": low,
            "avg": avg,
        }

    log(f"Price data loaded: {len(prices)} items")
    return prices


def load_database() -> dict:
    """
    加载 gear-database.json

    Returns:
        数据库字典
    """
    if not DATABASE_PATH.exists():
        log(f"Database file not found: {DATABASE_PATH}", "ERROR")
        sys.exit(1)

    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        log(f"Database loaded: {DATABASE_PATH.name}")
        return data
    except json.JSONDecodeError as e:
        log(f"Invalid JSON in database: {e}", "ERROR")
        sys.exit(1)
    except Exception as e:
        log(f"Failed to load database: {e}", "ERROR")
        sys.exit(1)


def save_database(data: dict):
    """
    将更新后的数据库写回文件

    Args:
        data: 更新后的数据库字典
    """
    try:
        with open(DATABASE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log(f"Database saved: {DATABASE_PATH.name}")
    except Exception as e:
        log(f"Failed to save database: {e}", "ERROR")
        sys.exit(1)


def update_item_prices(data: dict, prices: dict, mapping: dict) -> dict:
    """
    遍历数据库中的所有物品，更新价格字段

    匹配策略：
      1. 精确匹配物品名称（不区分大小写）
      2. 如果物品名称包含特殊字符（如 "䷀"），尝试去除

    Args:
        data: gear-database.json 字典
        prices: { osrs_id: {high, low, avg} }
        mapping: { name_lower: osrs_id }

    Returns:
        更新统计: { updated: int, not_found: int, errors: int }
    """
    stats = {"updated": 0, "not_found": 0, "errors": 0}
    combat_styles = data.get("combat_styles", {})

    for style_name, style_data in combat_styles.items():
        tiers = style_data.get("tiers", [])

        for tier_idx, tier in enumerate(tiers):
            gear = tier.get("recommended_gear", {})

            for slot_name, item in gear.items():
                try:
                    item_name = item.get("name", "").strip()

                    if not item_name:
                        stats["errors"] += 1
                        continue

                    # 匹配：尝试精确匹配
                    name_lower = item_name.lower()
                    osrs_id = mapping.get(name_lower)

                    # 如果未找到，尝试移除品牌/装饰前缀（如 "Bronze"、"Rune"等）
                    if not osrs_id:
                        # 简单尝试：去掉第一个空格前的部分
                        parts = name_lower.split(" ", 1)
                        if len(parts) > 1 and parts[1]:
                            osrs_id = mapping.get(parts[1])

                    if osrs_id and osrs_id in prices:
                        price_data = prices[osrs_id]
                        new_price = price_data["avg"]

                        # 更新价格
                        old_price = item.get("ge_price_estimate", 0)
                        item["ge_price_estimate"] = new_price
                        item["ge_price_category"] = get_price_category(new_price)

                        if old_price != new_price:
                            stats["updated"] += 1
                        else:
                            # 价格没变也算校验通过
                            stats["updated"] += 1
                    else:
                        stats["not_found"] += 1
                        log(
                            f"No API match for '{item_name}' "
                            f"(style={style_name}, tier={tier.get('level_range', '?')}, slot={slot_name})",
                            "DEBUG"
                        )

                except Exception as e:
                    stats["errors"] += 1
                    log(
                        f"Error processing {slot_name} in {style_name}/{tier.get('level_range', '?')}: {e}",
                        "ERROR"
                    )

    return stats


def update_metadata(data: dict):
    """更新 meta 信息"""
    now = datetime.now(timezone.utc)
    now_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    if "meta" not in data:
        data["meta"] = {}

    data["meta"]["last_updated"] = now_str
    data["meta"]["last_price_update"] = now_str

    # 统计总物品数
    total_items = 0
    for style_name, style_data in data.get("combat_styles", {}).items():
        for tier in style_data.get("tiers", []):
            total_items += len(tier.get("recommended_gear", {}))
    data["meta"]["total_items"] = total_items


def main():
    """主入口"""
    log("=" * 50)
    log("OSRS Gear Price Updater — Starting")
    log("=" * 50)

    # 1. 获取 API 数据
    mapping = fetch_item_mapping()
    if not mapping:
        log("No mapping data available, aborting", "CRITICAL")
        sys.exit(1)

    # API 延迟，避免限流
    time.sleep(API_DELAY_SECONDS)

    prices = fetch_price_data()
    if not prices:
        log("No price data available, aborting", "CRITICAL")
        sys.exit(1)

    # 2. 加载数据库
    database = load_database()

    # 3. 更新价格
    log("Updating item prices...")
    stats = update_item_prices(database, prices, mapping)

    # 4. 更新元数据
    update_metadata(database)

    # 5. 保存数据库
    save_database(database)

    # 6. 输出统计
    log("=" * 50)
    log("Update Summary")
    log("=" * 50)
    log(f"  Items processed (API match): {stats['updated']}")
    log(f"  Items not found in API:     {stats['not_found']}")
    log(f"  Errors:                     {stats['errors']}")
    log(f"  Last updated:               {database['meta']['last_updated']}")
    log("=" * 50)

    # 如果有大量未匹配，输出警告
    if stats["not_found"] > stats["updated"] * 0.5:
        log(
            "WARNING: High number of unmatched items. Check item names in database.",
            "WARN"
        )

    log("Update completed successfully!")


if __name__ == "__main__":
    main()
