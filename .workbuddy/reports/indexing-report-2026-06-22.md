# Google Indexing API — 每日提交报告

**日期**: 2026-06-22 (周日) 00:25 CST
**脚本**: 自定义 SA + 代理版（通过 ProxiedRequest 类）
**代理**: 127.0.0.1:7897 ✅
**状态**: 🔴 全部失败 — 权限问题未解决

---

## 📊 执行摘要

| 项目 | 数值 |
|------|------|
| Sitemap 总 URL 数 | 264 |
| 已提交（累计） | 108 |
| 本次待提交 | 163 |
| ✅ 成功提交 | **0** |
| ❌ 失败 | **163** |
| 🔴 配额超限 (429) | 否 |
| 🔴 权限错误 (403) | **是 — 100%** |
| 剩余未提交 | **163** |

---

## 🟢 好消息

1. **代理通道正常** — `127.0.0.1:7897` 联通 Google 正常
2. **SA Token 获取成功** — JWT 认证通过（通过 ProxiedRequest 修复了之前 SSL 错误）
3. **配额充足** — 全部 163 个请求都得到 403 响应，没有触发 429 配额限制
4. **Sitemap 增长** — 从 6/20 的 213 增长到今天的 264（新增 51 个 URL）

---

## 🔴 坏消息：连续 11+ 天 403 阻塞

所有 163 个 URL 均返回 **HTTP 403 PERMISSION DENIED**：

```
"Permission denied. Failed to verify the URL ownership"
```

**根本原因**：服务账号 `indexing-ap@osrsgu-indexin.iam.gserviceaccount.com` **仍未在 Google Search Console 中被添加为 Owner**。

这是 6/10-11、6/18-20、6/22 第 5 次出现同样的错误。

---

## 🛠️ 今日技术进展

今天发现并修复了脚本中的一个关键 Bug：
- **原 Bug**: `google.auth.transport.requests.Request` 类的 session 不读 `HTTPS_PROXY` 环境变量，导致 token 刷新时 SSL 握手失败
- **修复方案**: 自定义 `ProxiedRequest` 类，在 session 中显式设置 `proxies`
- **效果**: Token 刷新成功，HTTP 请求本身也能用代理，但 API 返回 403 权限错误

---

## 📋 修复步骤（仍未完成）

### 推荐方案 — 在 Search Console 添加 SA 为 Owner（一劳永逸）

1. 打开 https://search.google.com/search-console
2. 选择资源 `osrsguru.com`（域资源或 URL 前缀资源）
3. 左侧菜单 → **设置** → **用户和权限**
4. 点击 **添加用户**
5. 邮箱地址：`indexing-ap@osrsgu-indexin.iam.gserviceaccount.com`
6. 权限：**所有者 (Owner)**
7. 点击添加

### 备选方案 — 重新 OAuth 授权

本地运行：
```bash
cd C:\Users\Lenovo\osrs-guide-site\scripts
python submit_index_oauth.py
```
然后按提示在浏览器中授权。

---

## 📊 累计统计

- **Sitemap**: 264 URLs
- **已提交**: 108 URLs (41%)
- **未提交**: 156 URLs (59%)
- **403 错误天数**: 5 次（6/10, 6/11, 6/18, 6/19, 6/20, 6/22）
- **429 错误天数**: 8+ 次（6/6-9, 6/12, 6/15, 6/17）

---

*由每日自动化任务 (automation-1780641748498) 生成*
