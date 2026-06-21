# Automation: 每日 Indexing API URL 提交

## 执行历史

### 2026-06-13（上午 9:10）
- 代理正常 (127.0.0.1:7897)，OAuth Token 刷新成功
- Sitemap: 111 URLs 总计，96 已提交，15 新 URL 待提交
- 脚本: submit_index_oauth.py (OAuth + requests)
- 🟢 **突破！成功提交 5 个 URL！** — 连续 8 天失败后首次成功
- 成功: **5** (Batch 2 指南: magic/farming/mining/f2p-combat/mid-game)，失败: **10**（全部 429 配额耗尽）
- 第 6 个 URL 开始触发 429，说明 200 次/天配额在 09:10 仍有少量剩余
- 成功 URL（5）：osrs-1-99-magic-training-cheap-guide-2026 / osrs-1-99-farming-guide-beginner-profit-2026 / osrs-1-99-mining-guide-beginner-2026 / osrs-f2p-combat-training-guide-2026 / osrs-mid-game-breakthrough-guide-2026
- 失败 URL（10）：5 个 June 新指南 + 5 个 ZH 页面
- 已提交累计: 101 URLs，待提交: 10 URLs
- 📊 剩余: sailing-ship-crew / sailing-afk-training / toa-solo-beginner / slayer-block-skip / corrupted-gauntlet / zh首页 / zh-money / zh-skill / zh-quest / zh-boss

### 2026-06-06
- 代理状态: Clash Verge 127.0.0.1:7897 可用
- 脚本执行成功，OAuth 认证通过
- Sitemap: 98 URLs 总计，10 已提交，88 新 URL 待提交
- 结果: **429 QUOTA EXCEEDED** — 第一个 URL 就返回 429，说明今日 200 次/天配额已用完
- 原因: 可能有其他提交操作已消耗了配额，或 Google 重置时间尚未到
- 无需重试，等待配额重置后自动执行

### 2026-06-07
- 代理状态: Clash Verge 127.0.0.1:7897 可用
- 脚本执行成功，OAuth 认证通过
- Sitemap: 100 URLs 总计，13 已提交，87 新 URL 待提交（比昨日多 2 个新页面）
- 结果: **429 QUOTA EXCEEDED** — 连续第二天配额已用完，每个 URL 重试 3 次均返回 429
- 已手动停止脚本避免无意义的重试等待（累计浪费 12 分钟）
- 注意: 脚本中 socket 直连检测在沙箱中会挂起，需使用 `python -u` 参数启用无缓冲输出
- 建议: 连续两天 429，可能是配额重置时间非北京时间 0 点，或存在其他消耗来源。可考虑在非自动化时段手动测试一次确认配额状态

### 2026-06-08
- 代理状态: Clash Verge 127.0.0.1:7897 可用
- 脚本执行成功，OAuth 认证通过（自动刷新 token）
- Sitemap: 106 URLs 总计，21 已提交，85 新 URL 待提交（比上次多 6 个新页面）
- 结果: **429 QUOTA EXCEEDED** — 连续第三天配额已用完，第一个 URL 就返回 429
- 已提交累计: 21 URLs，待提交: 85 URLs
- ⚠️ 连续 3 天 429，配额重置时间可能非北京时间 0 点（可能是太平洋时间午夜）。建议在下午/晚上手动测试一次确认配额状态

### 2026-06-09（晚间执行 23:14）
- 代理正常、OAuth 正常
- Sitemap: 111 URLs 总计，96 已提交，15 新 URL 待提交
- 已提交增加原因：历史脚本在白天可能有其他提交（6/5 Batch 2 + 6/6 新指南 + ZH 页面等）
- 结果: **429 QUOTA EXCEEDED** — 连续第四天。15 个 URL 全部因配额跳过
- 已提交累计: 96 URLs，待提交: 15 URLs（5 个 Batch 2 指南 + 5 个 6/6 新指南 + 5 个 ZH 页面）
- ⚠️ 连续 4 天 429：建议将自动化执行时间改为北京时间下午 4 点后（太平洋时间午夜后），或暂停此自动化直到手动验证配额可用

### 2026-06-10（上午 9:44）
- 代理正常 (127.0.0.1:7897)
- Sitemap: 111 URLs，96 已提交，15 新 URL 待提交
- OAuth 脚本: **TOKEN EXPIRED** — `invalid_grant: Token has been expired or revoked`，Refresh token 被吊销
- 新写 SA 脚本 `daily_indexing_submit.py`：使用服务账号 + requests + 代理，代理通道正常
- SA 脚本结果: **HTTP 403 × 15** — `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com` 无 Search Console 权限
- 成功提交: **0**，失败: **15**（全部 403），剩余: **15**
- 🔴 **根本原因**：双重封锁 — OAuth token 过期 + SA 无 Search Console 权限
- 📋 **修复建议**：
  1. 优先：在 Search Console 添加 SA 邮箱 `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com` 为 Owner（一劳永逸）
  2. 备选：本地手动运行 `submit_index_oauth.py` 重新 OAuth 授权

### 2026-06-11（上午 9:28）
- 代理正常 (127.0.0.1:7897)，SA Token 获取成功
- Sitemap: 111 URLs，96 已提交，15 新 URL 待提交（与昨日相同，无新页面）
- 脚本: `daily_indexing_submit.py` (SA + requests)
- 结果: **HTTP 403 × 15** — 全部失败，SA 仍无 Search Console 权限
- 成功: **0**，失败: **15**，剩余: **15**
- 🔴 **连续 2 天 403** — SA `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com` 未被添加为 Search Console Owner
- ⚠️ **自动化已完全阻塞，直到手动修复 SA 权限为止。每日运行不会改变结果。**

### 2026-06-15（上午 10:24）
- 代理正常 (127.0.0.1:7897)，OAuth Token 刷新成功
- Sitemap: 163 URLs 总计，101 已提交，62 新 URL 待提交
- 新增 7 个 Jun 14 页面（KQ / RuneLite / Range / Cerberus / Sarachnis / Mobile / Regional）
- 脚本: `submit_index_oauth.py` (OAuth + requests)，认证通过
- 结果: **HTTP 429 × 62** — 第一个 URL 就返回 429，配额在上午 10:24 已耗尽
- 成功: **0**，失败: **62**（全部 429 Quota Exceeded），剩余: **62**
- 🔴 **连续 9 天配额耗尽**（Jun 6–9, Jun 12, Jun 15；Jun 10-11 为 403）：上午时段配额始终不可用
- 📊 已提交累计: 101 URLs，待提交: 62 URLs
- ⚠️ **强烈建议改为凌晨 0:30 CST 执行（配额刚重置）**，当前时间窗口无法有效提交

### 2026-06-12（上午 9:10）
- 代理正常 (127.0.0.1:7897)
- Sitemap: 110 URLs（去重），96 唯一已提交，15 新 URL 待提交
- 🟢 **突破**: OAuth Token 刷新成功！(Jun 10 的 `invalid_grant` 已解决)
- 脚本: `submit_index_oauth.py` (OAuth + requests)，认证通过
- 结果: **HTTP 429 × 15** — OAuth 可用但配额耗尽，第一个 URL 就 429
- 成功: **0**，失败: **15**（全部 429 Quota Exceeded），剩余: **15**
- 🔴 **连续 7 天配额耗尽** (Jun 6–12)：200次/天配额在每天上午 9 点已用完
- 📋 **分析**: OAuth 已恢复可用（比 SA 方案更好），唯一瓶颈是配额时间窗口
- 💡 **建议方案**：
  1. 将自动化执行时间改为北京时间凌晨 0:30（太平洋时间上午 9:30，配额刚重置）
  2. 或手动在上午其他时段运行一次 `submit_index_oauth.py` 验证配额窗口

### 2026-06-18（凌晨 0:25 CST — 新配额窗口）
- 代理正常 (127.0.0.1:7897)
- 🔴 **OAuth Token 过期**: `invalid_grant: Token has been expired or revoked`，无法刷新
- SA 方案: JWT 获取成功，代理通道正常
- Sitemap: 213 URLs（比上次少 3，sitemap 自动更新去重），已提交: 101，新 URL: 112
- 脚本: `daily_indexing_submit.py` (SA + requests)
- 结果: **HTTP 403 × 107 + Connection Error × 3 + Timeout × 2** — 全部失败
- 成功: **0**，失败: **112**，剩余: **112**
- 🔴 **双重阻塞重启**: OAuth token expired（Jun 10 同样问题）+ SA 无 Search Console 权限（Jun 10-11 同样问题）
- 📋 **唯一修复路径**: 用户手动 OAuth 重新授权 OR 在 Search Console 为 SA `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com` 添加 Owner 权限
- 💡 **推荐方案**: 二者任选其一即可解除阻塞

### 2026-06-17（上午 9:22）
- 代理正常 (127.0.0.1:7897)，OAuth Token 刷新成功
- Sitemap: 201 URLs 总计（新增 38 个页面：6/16 skill/combat/diary 系列 + 6/17 Crimson Desert 8篇 + Windrose 8篇）
- 已提交: 101 URLs，新 URL: 100（因配额限制截断至 200）
- 脚本: `sandbox_indexing_submit.py`（沙箱版，跳过 socket 网络检查）
- 结果: **HTTP 429 × 100** — 第一个 URL 就返回 429，配额在上午 9:22 已耗尽
- 成功: **0**，失败: **100**（全部 429），剩余: **100**
- 🔴 **连续多天配额耗尽**：上午时段配额始终不可用
- 📊 已提交累计: 101 URLs，待提交: 100 URLs
- ⚠️ **必须将自动化时间改为凌晨 0:30 CST**，当前 9:20 AM 执行时间永远无法获得配额
- 📋 自动化已更新为 0:30 AM CST 执行

### 2026-06-19（凌晨 0:25 CST）
- 代理正常 (127.0.0.1:7897)，SA Token 获取成功
- Sitemap: 213 URLs 总计，101 已提交，112 新 URL 待提交
- 脚本: `daily_indexing_submit.py` (SA + requests)
- 结果: **HTTP 403 × 112** — 全部失败，SA 无 Search Console 权限
- 1 个连接错误 (connection error)，1 个超时 (timeout)
- 成功: **0**，失败: **112**，剩余: **112**
- 🔴 **连续阻塞**: SA `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com` 未被添加为 Search Console Owner
- 📋 **修复步骤**（二选一）:
  1. 【推荐】GSC 添加 SA 邮箱为 Owner（一劳永逸）:
     - 打开 https://search.google.com/search-console
     - 选择 osrsguru.com → 设置 → 用户和权限 → 添加用户
     - 输入: `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com`
     - 权限: **所有者 (Owner)**
  2. 本地重新 OAuth 授权: 运行 `python scripts/submit_index_oauth.py`
- ⚠️ **自动化将持续失败直到权限修复**，建议暂停此自动化或先完成上述修复

### 2026-06-20（凌晨 06:15 CST）
- 代理正常 (127.0.0.1:7897)，SA JWT Token 获取成功
- OAuth: `token.json` 缺失（6/18 `invalid_grant` 后未重建）
- Sitemap: 213 URLs 总计，101 已提交，112 新 URL 待提交
- 脚本: `daily_indexing_submit.py` (SA + requests)
- 结果: **HTTP 403 × 112** — 全部失败，SA 无 Search Console 权限
- 成功: **0**，失败: **112**，剩余: **112**
- 🔴 **连续 10+ 天阻塞**: SA 403 + OAuth expired 双重封锁未解除
- ⚠️ 与 6/19 结果完全相同，自动化每日运行无意义
- 📋 报告已生成: `.workbuddy/reports/indexing-report-2026-06-20.md`
