# OSRS Guru AI — RuneLite 插件

游戏内 AI 攻略助手：不切屏、直接问、自动推攻略、实时查价格。

## 功能

| 功能 | 说明 |
|------|------|
| 🔍 AI 搜索 | 侧边栏输入问题，调 osrsguru.com RAG API 返回答案 |
| 📋 自动推荐 | 检测玩家在打什么 Boss → 弹出对应攻略链接 |
| 💰 价格查询 | 输入物品名 → 显示 GE 实时价格 |
| 📍 活动感知 | 识别 Slayer 任务、Boss 区域、自动匹配攻略 |

## 环境要求

- **JDK 11+**（推荐 [Adoptium Temurin 11](https://adoptium.net/)）
- **Gradle 7.x+**（或用项目自带的 gradlew，不需要安装）
- **RuneLite 客户端**（[runelite.net](https://runelite.net/)）

## 一键构建

```bash
# Windows（PowerShell）
cd runelite-plugin

# 1. 生成 Gradle Wrapper（首次）
gradle wrapper --gradle-version 7.6

# 2. 构建插件 JAR
gradlew.bat build

# 3. JAR 在 build/libs/ 下
```

或直接装 Gradle 后：
```bash
gradle build
# → build/libs/osrsguru-runelite-plugin-1.0.0.jar
```

## 安装到 RuneLite

### 方法 1：本地测试
```bash
# 构建后复制到 RuneLite 插件目录
copy build\libs\*.jar %USERPROFILE%\.runelite\externalmanager\
```
重启 RuneLite → 设置 → 插件 → 搜索 "OSRS Guru AI" → 启用

### 方法 2：提交到 Plugin Hub（推荐）
提交到 [RuneLite Plugin Hub](https://github.com/runelite/runelite/wiki/Plugin-Hub) 后，所有 RuneLite 用户都能在插件列表中找到。

见 [SUBMISSION.md](SUBMISSION.md)

## 项目结构

```
runelite-plugin/
├── build.gradle                          # Gradle 构建配置
├── README.md                             # 本文件
├── SUBMISSION.md                         # Plugin Hub 提交指南
├── src/main/java/com/osrsguru/plugin/
│   ├── OSRSGuruPlugin.java              # 插件入口（生命周期 + 事件监听）
│   ├── OSRSGuruPanel.java               # 侧边栏 UI（搜索框 + 答案区 + 价格）
│   ├── OSRSGuruApiClient.java           # HTTP 客户端（调 RAG API）
│   └── ActivityDetector.java            # 玩家活动检测（Boss/Slayer 匹配）
└── src/main/resources/
    └── osrsguru-icon.png                # 插件图标（16x16）
```

## 技术栈

| 层 | 技术 |
|------|------|
| 框架 | RuneLite Plugin API |
| UI | Java Swing（侧边栏面板） |
| HTTP | OkHttp 4.x |
| JSON | Gson |
| 构建 | Gradle 7.x |
| JDK | 11+ |

## API 后端

插件连接到 `osrs-rag-api.vercel.app` 的三层 RAG 架构：

```
用户提问 → 本地 115 篇攻略检索 → OSRS Wiki 实时补充 → DeepSeek/Groq 生成回答
```

API 代码在 `../api/index.py`，部署在 Vercel。
