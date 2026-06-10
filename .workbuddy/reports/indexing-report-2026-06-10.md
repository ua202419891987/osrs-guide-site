# Google Indexing API — 每日提交报告

**日期**: 2026-06-10 09:44:42
**状态**: AUTH_BLOCKED (双重封锁)
**执行时间**: 约 30 秒

## 统计摘要

| 指标 | 数值 |
|------|------|
| Sitemap 总 URL 数 | 111 |
| 之前已提交 | 96 |
| 本次新发现 URL | 15 |
| ✅ 成功提交 | 0 |
| ❌ 提交失败 | 15 |
| 🔴 配额超限 (429) | 否 |
| 剩余未提交 | 15 |

## 问题诊断

### ❌ 问题 1: OAuth Token 已过期
- 脚本: `submit_index_oauth.py`
- 错误: `invalid_grant: Token has been expired or revoked`
- 原因: Refresh token 被 Google 吊销（可能超过 50 个 refresh token 限制）
- 修复: 需要**手动运行脚本**重新 OAuth 授权（需要浏览器交互）

### ❌ 问题 2: Service Account 无 Search Console 权限
- 脚本: `daily_indexing_submit.py` (v6, SA + raw requests)
- 服务账号: `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com`
- 错误: `HTTP 403` — 所有 15 个 URL 均返回 403
- 代理: ✅ 127.0.0.1:7897 正常工作
- 修复: 需在 [Google Search Console](https://search.google.com/search-console) 中将 SA 邮箱添加为 osrsguru.com 的**所有者 (Owner)**

## 失败 URL 列表（15 个）

| # | URL | 错误 |
|---|-----|------|
| 1 | guides/osrs-1-99-magic-training-cheap-guide-2026.html | HTTP 403 |
| 2 | guides/osrs-1-99-farming-guide-beginner-profit-2026.html | HTTP 403 |
| 3 | guides/osrs-1-99-mining-guide-beginner-2026.html | HTTP 403 |
| 4 | guides/osrs-f2p-combat-training-guide-2026.html | HTTP 403 |
| 5 | guides/osrs-mid-game-breakthrough-guide-2026.html | HTTP 403 |
| 6 | guides/osrs-sailing-ship-crew-guide-2026.html | HTTP 403 |
| 7 | guides/osrs-sailing-afk-training-guide-2026.html | HTTP 403 |
| 8 | guides/osrs-toa-solo-beginner-guide-2026.html | HTTP 403 |
| 9 | guides/osrs-slayer-block-skip-list-2026.html | HTTP 403 |
| 10 | guides/osrs-corrupted-gauntlet-guide-2026.html | HTTP 403 |
| 11 | zh/index.html | HTTP 403 |
| 12 | zh/money-making.html | HTTP 403 |
| 13 | zh/skill-training.html | HTTP 403 |
| 14 | zh/quest-guides.html | HTTP 403 |
| 15 | zh/boss-guides.html | HTTP 403 |

## 推荐操作（优先级排序）

### 🔴 高优先级：修复 Service Account 权限（一劳永逸）
1. 打开 [Google Search Console](https://search.google.com/search-console)
2. 选择 `osrsguru.com` 属性
3. Settings → Users and permissions → Add user
4. 输入: `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com`
5. 权限选择: **Owner (完全)**
6. 保存后，自动化脚本将永久可用（不再需要 OAuth 交互）

### 🟡 备选：手动重新 OAuth 授权（临时修复）
1. 在本地 CMD 中运行：
   ```
   cd C:\Users\Lenovo\osrs-guide-site\scripts
   python submit_index_oauth.py
   ```
2. 浏览器会弹出授权页面
3. 用 `1530398390@qq.com` 登录并授权

---

*由每日自动化任务 (automation-1780641748498) 于 2026-06-10 生成*
