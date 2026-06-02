# 搜索引擎索引自动提交 — 配置指南

## 目录
1. [Google Indexing API 配置](#1-google-indexing-api-配置)
2. [Bing Webmaster API 配置](#2-bing-webmaster-api-配置)
3. [IndexNow 配置（可选）](#3-indexnow-配置可选)
4. [使用脚本提交](#4-使用脚本提交)

---

## 1. Google Indexing API 配置

### 步骤：获取服务账号密钥

| # | 操作 | 说明 |
|---|------|------|
| 1 | 打开 [Google Cloud Console](https://console.cloud.google.com/) | 登录你的 Google 账号 |
| 2 | 创建项目 → 点击左上角下拉 → **新建项目** | 项目名随便填，如 `osrsguru-indexing` |
| 3 | 进入 **API和服务 → 库** | 搜索 `Indexing API` |
| 4 | 点击 **启用** | 启用 Indexing API |
| 5 | 进入 **API和服务 → 凭据** | 创建凭据 |
| 6 | 点击 **创建凭据 → 服务账号** | |
| 7 | 服务账号名称: `osrsguru-indexing` | 创建后会自动生成邮箱 |
| 8 | 点击刚创建的服务账号 → **密钥 → 添加密钥 → 创建新密钥** | 选择 JSON 格式 |
| 9 | **下载 JSON 密钥文件** | ⚠️ 这是唯一的密钥，妥善保管 |

### 步骤：在 Search Console 中添加服务账号

| # | 操作 | 说明 |
|---|------|------|
| 10 | 打开 [Google Search Console](https://search.google.com/search-console) | |
| 11 | 选择你的站点 `osrsguru.com` | |
| 12 | 左侧菜单 → **设置 → 用户和权限** | |
| 13 | 点击 **添加用户** | 权限选 **拥有者**（必须） |
| 14 | 输入服务账号邮箱 | 格式: `osrsguru-indexing@xxx.iam.gserviceaccount.com` |
| 15 | 保存 | |

### 步骤：配置到脚本

```bash
# 将下载的 JSON 文件放到脚本目录
cp ~/Downloads/osrsguru-indexing-xxxxx.json scripts/
```

---

## 2. Bing Webmaster API 配置

### 步骤：获取 API Key

| # | 操作 | 说明 |
|---|------|------|
| 1 | 打开 [Bing Webmaster Tools](https://www.bing.com/webmasters) | 登录 Microsoft 账号 |
| 2 | 确保 `osrsguru.com` 已添加并验证 | |
| 3 | 右上角齿轮 → **API 访问** | |
| 4 | 点击 **生成 API 密钥** | 复制密钥 |
| 5 | 填写到 `scripts/index_config.json` 的 `bing_api_key` 字段 | |

---

## 3. IndexNow 配置（可选）

IndexNow 是 Bing/Yandex 的新协议，可直接通知搜索引擎，无需 API Key。

在站点根目录创建密钥文件：

```
echo "81f6a2c3d4e5f6a7b8c9d0e1f2a3b4c5" > 81f6a2c3d4e5f6a7b8c9d0e1f2a3b4c5.txt
```

上传到站点根目录（GitHub Pages 项目根目录），确保可通过 `https://osrsguru.com/81f6a2c3d4e5f6a7b8c9d0e1f2a3b4c5.txt` 访问。

---

## 4. 使用脚本提交

### 安装依赖

```bash
pip install google-auth google-api-python-client requests lxml
```

### 命令

```bash
# 查看配置
python scripts/submit_index.py --config

# 预览（不实际提交）
python scripts/submit_index.py --dry-run

# 提交默认 5 个 URL
python scripts/submit_index.py \
  --google-key scripts/your-key.json \
  --bing-key YOUR_BING_API_KEY

# 提交特定 URL
python scripts/submit_index.py \
  --urls "https://osrsguru.com/guides/new-guide.html" \
  --google-key scripts/your-key.json

# 从 sitemap 解析所有 URL 并提交
python scripts/submit_index.py \
  --sitemap \
  --google-key scripts/your-key.json
```

### 提交频率注意

- Google Indexing API: 每天最多 200 次提交（免费）
- Bing URL Submission API: 每天最多 10,000 个 URL
- 建议仅对**新增**或**重大更新**的页面使用，不要批量提交已有页面
