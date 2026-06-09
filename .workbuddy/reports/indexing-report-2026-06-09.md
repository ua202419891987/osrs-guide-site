# Google Indexing API 每日提交报告

**日期**: 2026-06-09 (周二)  
**执行时间**: 23:14 CST  
**自动化 ID**: automation-1780641748498

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| Sitemap URL 总数 | 111 |
| 已提交（历史累计） | 96 |
| 本次待提交 | 15 |
| 本次成功 | **0** |
| 本次失败 | **15** |
| 剩余未提交 | **15** |

## 结果: ❌ 全部失败 — 连续第 4 天 429 QUOTA EXCEEDED

第一个 URL 提交即返回 HTTP 429，Google 今日 200 次/天配额已用完。

## 本次失败的 15 个 URL

1. https://osrsguru.com/guides/osrs-1-99-magic-training-cheap-guide-2026.html
2. https://osrsguru.com/guides/osrs-1-99-farming-guide-beginner-profit-2026.html
3. https://osrsguru.com/guides/osrs-1-99-mining-guide-beginner-2026.html
4. https://osrsguru.com/guides/osrs-f2p-combat-training-guide-2026.html
5. https://osrsguru.com/guides/osrs-mid-game-breakthrough-guide-2026.html
6. https://osrsguru.com/guides/osrs-sailing-ship-crew-guide-2026.html
7. https://osrsguru.com/guides/osrs-sailing-afk-training-guide-2026.html
8. https://osrsguru.com/guides/osrs-toa-solo-beginner-guide-2026.html
9. https://osrsguru.com/guides/osrs-slayer-block-skip-list-2026.html
10. https://osrsguru.com/guides/osrs-corrupted-gauntlet-guide-2026.html
11. https://osrsguru.com/zh/index.html
12. https://osrsguru.com/zh/money-making.html
13. https://osrsguru.com/zh/skill-training.html
14. https://osrsguru.com/zh/quest-guides.html
15. https://osrsguru.com/zh/boss-guides.html

## 趋势分析

| 日期 | 新 URL 数 | 结果 | 备注 |
|------|-----------|------|------|
| 06-06 | 88 | 429 | 第 1 天 |
| 06-07 | 87 | 429 | 第 2 天 |
| 06-08 | 85 | 429 | 第 3 天 |
| 06-09 | 15 | 429 | 第 4 天 |

## ⚠️ 严重警告

**连续 4 天在 9:00 AM CST / 23:00 CST 两个时段执行均返回 429。**

配额重置时间可能不是北京时间 0 点，极可能是**太平洋时间 (PT) 午夜**，对应北京时间下午 3 点。建议：
1. 下次在 **北京时间下午 4 点后** 手动测试一次
2. 或创建新 Automation 尝试在 16:00 CST 执行
3. 确认是否有其他工具/脚本在消耗同一配额

## 技术细节

- 代理: 127.0.0.1:7897 ✅ 正常
- OAuth 认证: ✅ 通过（token 自动刷新）
- 脚本: submit_index_oauth.py v5
- 代理状态: Clash Verge running
