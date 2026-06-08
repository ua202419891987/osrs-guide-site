# RuneLite Plugin Hub 提交指南

## 提交前检查清单

- [ ] 插件使用外部服务（API），已在描述中声明
- [ ] 代码遵循 RuneLite 插件规范
- [ ] JAR 文件在本地测试通过
- [ ] 插件图标已准备（16x16 PNG）

## 提交步骤

### 1. Fork plugin-hub 仓库
```
https://github.com/runelite/plugin-hub
```

### 2. 创建插件配置文件
在 `plugins/` 目录下创建 `osrs-guru-ai` 文件：

```properties
# Plugin Hub metadata
displayName=OSRS Guru AI
author=OSRS Guru
description=AI-powered OSRS guide assistant. Ask questions, get boss tips, and check GE prices without leaving the game. Connects to osrsguru.com RAG API.
tags=ai,guide,wiki,boss,price
plugins=com.osrsguru.plugin.OSRSGuruPlugin
```

### 3. 添加 JAR + Icon
```bash
cp build/libs/osrsguru-runelite-plugin-1.0.0.jar plugin-hub/plugins/osrs-guru-ai/
cp src/main/resources/osrsguru-icon.png plugin-hub/plugins/osrs-guru-ai/
```

### 4. 创建 Pull Request
```
Title: Add OSRS Guru AI plugin

Body:
## OSRS Guru AI — In-game AI Guide Assistant

**What it does:**
- AI-powered Q&A sidebar → calls osrsguru.com RAG API
- Auto-detects player activity → recommends relevant guides
- GE price lookup → real-time OSRS Wiki prices
- Boss overlay hints (future)

**Why it belongs on Plugin Hub:**
- No existing RuneLite plugin does AI-powered guide search
- Backed by 115+ original OSRS guides on osrsguru.com
- Uses real-time OSRS Wiki + GE data as supplement
- Open source, free to use

**API endpoint:** https://osrs-rag-api.vercel.app
**Website:** https://osrsguru.com
```

### 5. 代码审查要点

RuneLite 团队会检查：
- [x] 不发送用户数据到第三方（API 只传搜索文本，不传玩家信息）
- [x] 不修改游戏内存/自动化操作
- [x] 遵守 Jagex 第三方客户端规则
- [x] 代码在 GitHub 公开

### 审查时间

通常 **1-2 周**。通过后在 RuneLite 插件列表搜索 "OSRS Guru AI" 即可安装，覆盖 250K+ 日活用户。

## 快速命令

```bash
# 构建
cd runelite-plugin
gradle clean build

# 本地测试
copy build\libs\*.jar %USERPROFILE%\.runelite\externalmanager\

# Fork + Clone plugin-hub
git clone https://github.com/YOUR_USERNAME/plugin-hub.git
cd plugin-hub

# 添加插件文件
mkdir plugins\osrs-guru-ai
copy ..\build\libs\*.jar plugins\osrs-guru-ai\
copy ..\src\main\resources\osrsguru-icon.png plugins\osrs-guru-ai\

# 提交 PR
git add plugins/osrs-guru-ai
git commit -m "Add OSRS Guru AI plugin"
git push origin master
# → 在 GitHub 创建 Pull Request
```
