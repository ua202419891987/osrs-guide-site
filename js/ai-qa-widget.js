/**
 * OSRS Guru AI Question & Answer Widget
 * 右下角悬浮窗 - AI 问答系统
 * v2.3 - 多游戏感知 + 本地文章匹配
 *   - OSRS 页面：保持原有 Wiki → DeepSeek 逻辑
 *   - Crimson Desert 页面：先本地匹配12篇CD文章 → DeepSeek fallback
 *   - Windrose 页面：先本地匹配12篇Windrose文章 → DeepSeek fallback
 */

(function () {
  'use strict';

  // ========== 游戏上下文检测 ==========
  const GAME = detectGame();

  function detectGame() {
    var path = window.location.pathname.toLowerCase();
    if (path.indexOf('/crimson-desert/') !== -1 || path.indexOf('crimson-desert') !== -1) return 'crimson-desert';
    if (path.indexOf('/windrose/') !== -1 || path.indexOf('windrose') !== -1) return 'windrose';
    return 'osrs';
  }

  // ========== 配置 ==========
  var CONFIG = {
    apiBase: window.location.hostname === 'localhost' 
      ? 'http://localhost:8000' 
      : 'https://osrs-rag-api.vercel.app',
    widgetId: 'osrs-qa-widget',
    widgetButtonId: 'osrs-qa-toggle-btn',
    maxMessages: 10,
    game: GAME,
    // 根据游戏动态文本
    gameName: GAME === 'crimson-desert' ? 'Crimson Desert' : (GAME === 'windrose' ? 'Windrose' : 'OSRS'),
    gameIcon: GAME === 'crimson-desert' ? '\u2694\uFE0F' : (GAME === 'windrose' ? '\u26F5' : '\u2694\uFE0F'),
    assistantTitle: GAME === 'crimson-desert' ? 'Crimson Desert AI Assistant' : (GAME === 'windrose' ? 'Windrose AI Assistant' : 'OSRS AI Assistant'),
    inputPlaceholder: GAME === 'crimson-desert' ? 'Ask about Crimson Desert...' : (GAME === 'windrose' ? 'Ask about Windrose...' : 'Ask about OSRS guides...'),
    sourceGuruLabel: GAME === 'crimson-desert' ? 'Crimson Desert Guru' : (GAME === 'windrose' ? 'Windrose Guru' : 'OSRS Guru'),
  };

  // ========== CD/Windrose 本地文章索引（关键词 + URL） ==========
  var CD_ARTICLES = [
    { title: 'Crimson Desert New Player Guide 2026', url: 'guides/crimson-desert/crimson-desert-new-player-guide-2026.html', keywords: 'new player beginner start starting intro introduction how to play basics first steps getting started tutorial controls interface character creation guide walkthrough overview' },
    { title: 'Crimson Desert Combat Guide 2026', url: 'guides/crimson-desert/crimson-desert-combat-guide-2026.html', keywords: 'combat fight fighting parry dodge block combos stamina spirit surge grapple counter attack deal damage sword spear axe melee ranged magic battle duel' },
    { title: 'Crimson Desert Weapons & Gear Guide 2026', url: 'guides/crimson-desert/crimson-desert-weapons-gear-guide-2026.html', keywords: 'weapons weapon gear equipment armor best strongest tier list ranking upgrade enhance blacksmith crafting sword greatsword bow shield offhand accessories stats' },
    { title: 'Crimson Desert Quest Walkthrough 2026', url: 'guides/crimson-desert/crimson-desert-quest-walkthrough-2026.html', keywords: 'quest quests story main quest walkthrough mission chapter act faction choice dialogue decision hidden secret ending side quest' },
    { title: 'Crimson Desert Boss Guide 2026', url: 'guides/crimson-desert/crimson-desert-boss-guide-2026.html', keywords: 'boss bosses boss fight enemy pattern attack parry window weak point weak spot strategy how to beat kill defeat all bosses ranked difficulty tier' },
    { title: 'Crimson Desert Skills & Builds Guide 2026', url: 'guides/crimson-desert/crimson-desert-skills-builds-guide-2026.html', keywords: 'skill skills build builds keen senses tree stat stats allocation spirit arts respec reset best build talent class warrior mage assassin archer hybrid' },
  ];

  var WINDROSE_ARTICLES = [
    { title: 'Windrose Beginner Guide 2026', url: 'guides/windrose/windrose-beginner-guide-2026.html', keywords: 'beginner new player start guide how to play first steps survival day 1 starting island raft first ship early game basics tutorial' },
    { title: 'Windrose Combat & Ship Guide 2026', url: 'guides/windrose/windrose-combat-ship-guide-2026.html', keywords: 'combat fight fighting ship naval cannon sailing parry dodge boarding weapons melee land battle sea pirate ammunition ammo cannonball ship types' },
    { title: 'Windrose Crafting & Gear Guide 2026', url: 'guides/windrose/windrose-crafting-gear-guide-2026.html', keywords: 'crafting craft gear equipment weapon tier list best weapons armor ship upgrades rare resource resources consumables station bench materials' },
    { title: 'Windrose Quest & Exploration Guide 2026', url: 'guides/windrose/windrose-quest-exploration-guide-2026.html', keywords: 'quest quests exploration explore treasure map lore fragment hidden secret island route main story chapter' },
    { title: 'Windrose Boss Guide 2026', url: 'guides/windrose/windrose-boss-guide-2026.html', keywords: 'boss bosses boss fight tier 1 tier 2 tier 3 final boss attack pattern farming route strategy how to beat kill defeat enemy monster' },
    { title: 'Windrose Base Building Tips 2026', url: 'guides/windrose/windrose-base-building-tips-2026.html', keywords: 'base building tips layout defense walls traps fleet management trade routes endgame goal settle settlement home island fortification' },
  ];

  // ========== 本地文章匹配（仅 CD/Windrose 使用） ==========
  function matchLocalArticles(question, game) {
    var articles = game === 'crimson-desert' ? CD_ARTICLES : WINDROSE_ARTICLES;
    var lowerQ = question.toLowerCase();
    var matches = [];

    // 常见拼写纠错映射
    var typos = {
      'palyer': 'player', 'playr': 'player', 'plaer': 'player',
      'beginer': 'beginner', 'begineer': 'beginner',
      'wepon': 'weapon', 'weapn': 'weapon', 'wpn': 'weapon',
      'bosse': 'boss', 'bss': 'boss',
      'comba': 'combat', 'cmbat': 'combat',
      'questt': 'quest', 'qust': 'quest',
      'guilde': 'guide', 'guid': 'guide',
      'startt': 'start', 'stat': 'start', 'strt': 'start',
      'howto': 'how to', 'howdoi': 'how do i', 'du': 'do', 'waht': 'what', 'whats': "what's",
      'crimson': 'crimson desert', 'desert': 'crimson desert',
      'windros': 'windrose', 'windose': 'windrose', 'windroses': 'windrose',
    };

    // 预处理问题文本：替换常见拼写错误
    var cleanedQ = lowerQ;
    for (var typo in typos) {
      if (cleanedQ.indexOf(typo) !== -1) {
        cleanedQ = cleanedQ.replace(new RegExp(typo, 'g'), typos[typo]);
      }
    }
    // 合并原始+纠正后的文本用于匹配
    var searchQ = lowerQ + ' ' + cleanedQ;

    for (var i = 0; i < articles.length; i++) {
      var score = 0;
      var keywords = articles[i].keywords.split(' ');
      var titleLower = articles[i].title.toLowerCase();

      // 关键词匹配（在合并后的搜索文本中查找）
      for (var k = 0; k < keywords.length; k++) {
        if (searchQ.indexOf(keywords[k]) !== -1) {
          score += (keywords[k].length > 4 ? 3 : 1);
        }
      }

      // 标题词匹配
      var titleWords = titleLower.replace(/crimson desert |windrose |2026|guide /g, '').split(' ');
      for (var w = 0; w < titleWords.length; w++) {
        if (titleWords[w].length > 2 && searchQ.indexOf(titleWords[w]) !== -1) {
          score += 2;
        }
      }

      if (score > 0) {
        matches.push({ article: articles[i], score: score });
      }
    }

    // 按匹配分数降序排列，取 top 3
    matches.sort(function(a, b) { return b.score - a.score; });
    return matches.slice(0, 3);
  }

  // ========== CSS 注入 ==========
  function injectStyles() {
    var style = document.createElement('style');
    style.textContent = '\n/* AI \u95ee\u7b54\u6d6e\u7a97 - \u6838\u5fc3\u6837\u5f0f */\n#osrs-qa-widget {\n  position: fixed;\n  bottom: 20px;\n  right: 20px;\n  width: 420px;\n  max-height: 600px;\n  background: linear-gradient(135deg, rgba(39, 33, 26, 0.98), rgba(59, 38, 21, 0.95));\n  border: 2px solid rgba(212, 175, 55, 0.4);\n  border-radius: 12px;\n  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), \n              0 0 20px rgba(212, 175, 55, 0.15);\n  display: none;\n  flex-direction: column;\n  z-index: 10000;\n  font-family: \'Segoe UI\', Tahoma, Geneva, sans-serif;\n  overflow: hidden;\n}\n\n#osrs-qa-widget.open {\n  display: flex;\n  animation: slideUp 0.3s ease-out;\n}\n\n@keyframes slideUp {\n  from {\n    opacity: 0;\n    transform: translateY(20px);\n  }\n  to {\n    opacity: 1;\n    transform: translateY(0);\n  }\n}\n\n/* \u5934\u90e8 */\n#osrs-qa-widget .qa-header {\n  background: linear-gradient(90deg, rgba(212, 175, 55, 0.15), rgba(212, 175, 55, 0.08));\n  border-bottom: 1px solid rgba(212, 175, 55, 0.25);\n  padding: 16px 18px;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex-shrink: 0;\n}\n\n#osrs-qa-widget .qa-header-title {\n  display: flex;\n  align-items: center;\n  gap: 8px;\n  font-size: 15px;\n  font-weight: 600;\n  color: #d4af37;\n  font-family: \'Cinzel\', serif;\n}\n\n#osrs-qa-widget .qa-header-title .qa-icon {\n  font-size: 18px;\n}\n\n#osrs-qa-widget .qa-close-btn {\n  background: none;\n  border: none;\n  color: rgba(212, 175, 55, 0.6);\n  font-size: 20px;\n  cursor: pointer;\n  padding: 4px;\n  transition: color 0.2s;\n}\n\n#osrs-qa-widget .qa-close-btn:hover {\n  color: #d4af37;\n}\n\n/* \u6d88\u606f\u533a\u57df */\n#osrs-qa-widget .qa-messages {\n  flex: 1;\n  overflow-y: auto;\n  padding: 16px;\n  display: flex;\n  flex-direction: column;\n  gap: 12px;\n}\n\n#osrs-qa-widget .qa-message {\n  display: flex;\n  gap: 8px;\n  animation: fadeIn 0.3s ease-out;\n}\n\n@keyframes fadeIn {\n  from {\n    opacity: 0;\n    transform: translateY(8px);\n  }\n  to {\n    opacity: 1;\n    transform: translateY(0);\n  }\n}\n\n#osrs-qa-widget .qa-message.user {\n  justify-content: flex-end;\n}\n\n#osrs-qa-widget .qa-message.assistant {\n  justify-content: flex-start;\n}\n\n#osrs-qa-widget .qa-message-bubble {\n  max-width: 85%;\n  padding: 10px 14px;\n  border-radius: 8px;\n  font-size: 13px;\n  line-height: 1.5;\n  word-wrap: break-word;\n}\n\n#osrs-qa-widget .qa-message.user .qa-message-bubble {\n  background: rgba(212, 175, 55, 0.25);\n  border: 1px solid rgba(212, 175, 55, 0.35);\n  color: #e8d5b5;\n}\n\n#osrs-qa-widget .qa-message.assistant .qa-message-bubble {\n  background: rgba(100, 80, 60, 0.4);\n  border: 1px solid rgba(212, 175, 55, 0.2);\n  color: #d4af37;\n}\n\n#osrs-qa-widget .qa-message.assistant .qa-message-bubble.loading {\n  display: flex;\n  align-items: center;\n  gap: 6px;\n  min-height: 24px;\n}\n\n#osrs-qa-widget .qa-message.assistant .qa-message-bubble.loading::after {\n  content: \'\';\n  display: inline-block;\n  width: 4px;\n  height: 4px;\n  background: #d4af37;\n  border-radius: 50%;\n  animation: blink 1s infinite;\n}\n\n@keyframes blink {\n  0%, 100% { opacity: 0.3; }\n  50% { opacity: 1; }\n}\n\n/* \u4fe1\u606f\u6e90\u6807\u7b7e */\n#osrs-qa-widget .qa-source {\n  font-size: 11px;\n  color: rgba(212, 175, 55, 0.6);\n  margin-top: 4px;\n  font-style: italic;\n}\n\n/* \u5f15\u7528\u6587\u7ae0\u94fe\u63a5 */\n#osrs-qa-widget .qa-article-link {\n  display: block;\n  margin-top: 8px;\n  padding: 8px 10px;\n  background: rgba(212, 175, 55, 0.1);\n  border: 1px solid rgba(212, 175, 55, 0.25);\n  border-radius: 6px;\n  font-size: 12px;\n  color: #d4af37;\n  text-decoration: none;\n  transition: all 0.2s;\n  font-weight: 500;\n  cursor: pointer;\n}\n\n#osrs-qa-widget .qa-article-link:hover {\n  background: rgba(212, 175, 55, 0.2);\n  border-color: rgba(212, 175, 55, 0.5);\n  color: #f0d060;\n}\n\n#osrs-qa-widget .qa-article-link .qa-link-icon {\n  margin-right: 5px;\n  font-size: 13px;\n}\n\n/* 多文章匹配列表 */\n#osrs-qa-widget .qa-match-list {\n  margin-top: 6px;\n}\n\n#osrs-qa-widget .qa-match-intro {\n  font-size: 12px;\n  color: rgba(232, 213, 181, 0.7);\n  margin-bottom: 4px;\n}\n\n/* \u8f93\u5165\u533a\u57df */\n#osrs-qa-widget .qa-input-group {\n  border-top: 1px solid rgba(212, 175, 55, 0.2);\n  padding: 12px;\n  background: rgba(0, 0, 0, 0.2);\n  display: flex;\n  gap: 8px;\n  flex-shrink: 0;\n}\n\n#osrs-qa-widget .qa-input-group input {\n  flex: 1;\n  background: rgba(59, 38, 21, 0.6);\n  border: 1px solid rgba(212, 175, 55, 0.25);\n  border-radius: 6px;\n  padding: 8px 12px;\n  color: #d4af37;\n  font-size: 13px;\n  font-family: inherit;\n  transition: border-color 0.2s;\n}\n\n#osrs-qa-widget .qa-input-group input::placeholder {\n  color: rgba(212, 175, 55, 0.4);\n}\n\n#osrs-qa-widget .qa-input-group input:focus {\n  outline: none;\n  border-color: rgba(212, 175, 55, 0.5);\n  background: rgba(59, 38, 21, 0.8);\n}\n\n#osrs-qa-widget .qa-send-btn {\n  background: linear-gradient(135deg, rgba(212, 175, 55, 0.35), rgba(212, 175, 55, 0.2));\n  border: 1px solid rgba(212, 175, 55, 0.4);\n  border-radius: 6px;\n  color: #d4af37;\n  font-size: 15px;\n  cursor: pointer;\n  padding: 6px 12px;\n  transition: all 0.2s;\n  font-weight: 600;\n}\n\n#osrs-qa-widget .qa-send-btn:hover:not(:disabled) {\n  background: linear-gradient(135deg, rgba(212, 175, 55, 0.5), rgba(212, 175, 55, 0.35));\n  border-color: rgba(212, 175, 55, 0.6);\n  transform: scale(1.02);\n}\n\n#osrs-qa-widget .qa-send-btn:disabled {\n  opacity: 0.5;\n  cursor: not-allowed;\n}\n\n/* \u6d6e\u7a97\u6253\u5f00\u6309\u94ae - \u84dd\u8272\u6c34\u871c\u6843\u578b\u5361\u901aAI */\n#osrs-qa-toggle-btn {\n  position: fixed;\n  bottom: 20px;\n  right: 20px;\n  width: 100px;\n  height: 108px;\n  background: #4A90D9;\n  border: none;\n  border-radius: 42% 42% 50% 50% / 44% 44% 58% 58%;\n  cursor: pointer;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n  z-index: 9999;\n  transition: all 0.3s ease;\n  box-shadow: 0 4px 20px rgba(74,144,217,0.45);\n  gap: 0;\n  outline: none;\n  padding: 0;\n  color: #fff;\n}\n\n/* \u5361\u901a\u8138 */\n#osrs-qa-toggle-btn .peach-face {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  gap: 5px;\n}\n\n#osrs-qa-toggle-btn .peach-eyes {\n  display: flex;\n  gap: 14px;\n}\n\n#osrs-qa-toggle-btn .peach-eyes span {\n  display: block;\n  width: 10px;\n  height: 11px;\n  background: #1a3a5c;\n  border-radius: 50%;\n}\n\n#osrs-qa-toggle-btn .peach-mouth {\n  width: 22px;\n  height: 10px;\n  border-bottom: 2.5px solid #1a3a5c;\n  border-radius: 0 0 14px 14px;\n}\n\n/* AI \u6587\u5b57\u6807\u7b7e */\n#osrs-qa-toggle-btn .ai-label {\n  font-size: 15px;\n  font-weight: 700;\n  color: #fff;\n  letter-spacing: 1px;\n  font-family: \'Segoe UI\', \'Cinzel\', sans-serif;\n  line-height: 1;\n  margin-top: 4px;\n}\n\n#osrs-qa-toggle-btn:hover {\n  transform: scale(1.07);\n  box-shadow: 0 6px 28px rgba(74,144,217,0.6);\n  background: #5A9DE5;\n}\n\n#osrs-qa-toggle-btn.hide {\n  display: none;\n}\n\n/* \u54cd\u5e94\u5f0f\u8bbe\u8ba1 */\n@media (max-width: 600px) {\n  #osrs-qa-widget {\n    width: 100%;\n    height: 100%;\n    max-height: 100%;\n    bottom: 0;\n    right: 0;\n    border-radius: 0;\n    max-height: 80vh;\n  }\n  \n  #osrs-qa-toggle-btn {\n    bottom: 20px;\n    right: 20px;\n  }\n}\n\n/* \u6d88\u606f\u6eda\u52a8\u6761\u6837\u5f0f */\n#osrs-qa-widget .qa-messages::-webkit-scrollbar {\n  width: 6px;\n}\n\n#osrs-qa-widget .qa-messages::-webkit-scrollbar-track {\n  background: rgba(0, 0, 0, 0.1);\n  border-radius: 3px;\n}\n\n#osrs-qa-widget .qa-messages::-webkit-scrollbar-thumb {\n  background: rgba(212, 175, 55, 0.25);\n  border-radius: 3px;\n}\n\n#osrs-qa-widget .qa-messages::-webkit-scrollbar-thumb:hover {\n  background: rgba(212, 175, 55, 0.4);\n}\n    ';
    document.head.appendChild(style);
  }

  // ========== HTML 结构创建 ==========
  function createWidget() {
    // 浮窗主体 - 动态标题和占位文字
    var widget = document.createElement('div');
    widget.id = CONFIG.widgetId;
    widget.innerHTML = 
      '<div class="qa-header">' +
        '<div class="qa-header-title">' +
          '<span class="qa-icon">' + CONFIG.gameIcon + '</span>' +
          '<span>' + CONFIG.assistantTitle + '</span>' +
        '</div>' +
        '<button class="qa-close-btn" aria-label="Close AI widget">\u2715</button>' +
      '</div>' +
      '<div class="qa-messages"></div>' +
      '<div class="qa-input-group">' +
        '<input type="text" class="qa-input" placeholder="' + CONFIG.inputPlaceholder + '" aria-label="Ask a question" />' +
        '<button class="qa-send-btn" aria-label="Send message">Send</button>' +
      '</div>';

    // 打开按钮
    var toggleBtn = document.createElement('button');
    toggleBtn.id = CONFIG.widgetButtonId;
    toggleBtn.innerHTML = '<div class="peach-face"><div class="peach-eyes"><span></span><span></span></div><div class="peach-mouth"></div></div><span class="ai-label">AI</span>';
    toggleBtn.title = 'Open ' + CONFIG.assistantTitle;

    // 添加到页面
    document.body.appendChild(widget);
    document.body.appendChild(toggleBtn);

    return { widget: widget, toggleBtn: toggleBtn };
  }

  // ========== 交互逻辑 ==========
  function setupEventHandlers(widget, toggleBtn) {
    var closeBtn = widget.querySelector('.qa-close-btn');
    var sendBtn = widget.querySelector('.qa-send-btn');
    var input = widget.querySelector('.qa-input');
    var messagesContainer = widget.querySelector('.qa-messages');

    // 打开/关闭浮窗
    toggleBtn.addEventListener('click', function() {
      widget.classList.toggle('open');
      if (widget.classList.contains('open')) {
        input.focus();
      }
    });

    closeBtn.addEventListener('click', function() {
      widget.classList.remove('open');
    });

    // 发送消息
    var sendMessage = function() {
      var message = input.value.trim();
      if (!message) return;

      // 显示用户消息
      addMessage(messagesContainer, message, 'user');
      input.value = '';
      sendBtn.disabled = true;

      // 显示加载状态
      addMessage(messagesContainer, 'Searching...', 'assistant', true);

      // === CD/Windrose 页面：先本地匹配 ===
      if (GAME === 'crimson-desert' || GAME === 'windrose') {
        var matches = matchLocalArticles(message, GAME);

        // 移除加载消息
        var loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }

        if (matches.length > 0) {
          // 本地匹配成功 → 直接返回文章链接
          var answerText = 'Here are the most relevant guides for your question:\n\n' +
            matches.map(function(m, idx) {
              return (idx + 1) + '. ' + m.article.title;
            }).join('\n');

          addMessage(messagesContainer, answerText, 'assistant', false, 'osrsguru', '', '');

          // 添加文章链接
          for (var i = 0; i < matches.length; i++) {
            addArticleLink(messagesContainer, matches[i].article.title, matches[i].article.url);
          }
          sendBtn.disabled = false;
          return; // 不调用后端 API
        }

        // 本地未匹配 → 调用后端 API (DeepSeek V3 fallback，带游戏上下文)
        callBackendAPI(message, messagesContainer, sendBtn, GAME);
        return;
      }

      // === OSRS 页面：保持原有逻辑 ===
      callBackendAPI(message, messagesContainer, sendBtn);
    };

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') sendMessage();
    });
  }

  // ========== 调用后端 API ==========
  function callBackendAPI(message, messagesContainer, sendBtn, gameContext) {
    var apiUrl = CONFIG.apiBase + '/rag-api/search?q=' + encodeURIComponent(message);
    // CD/Windrose 页面：传递游戏上下文给后端
    if (gameContext && gameContext !== 'osrs') {
      apiUrl += '&game=' + encodeURIComponent(gameContext);
    }

    fetch(apiUrl)
      .then(function(response) {
        if (!response.ok) throw new Error('API error: ' + response.status);
        return response.json();
      })
      .then(function(data) {
        // 移除加载消息
        var loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }

        // 显示 AI 回复
        var answer = data.answer || 'No answer available';
        var source = data.source || 'unknown';
        var title = data.title || '';
        var url = data.url || '';
        addMessage(messagesContainer, answer, 'assistant', false, source, title, url);
      })
      .catch(function(error) {
        console.error('RAG API error:', error);

        // 移除加载消息
        var loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }

        // 根据当前游戏显示不同的友好提示
        var offlineMsg;
        if (gameContext === 'crimson-desert') {
          offlineMsg = "I couldn't find a specific match for your question.\n\n" +
            'Here are our Crimson Desert guides that might help:\n\n' +
            '  \u27a1\ufe0f New Player Guide — Getting started in Pywel\n' +
            '  \u27a1\ufe0f Combat Mastery — Parry, dodge & combos\n' +
            '  \u27a1\ufe0f Weapons & Gear — Best loadouts ranked\n' +
            '  \u27a1\ufe0f Quest Walkthrough — Main story guide\n' +
            '  \u27a1\ufe0f Boss Guide — All bosses & strategies\n' +
            '  \u27a1\ufe0f Skills & Builds — Best builds for every playstyle\n\n' +
            'You can also browse all guides at osrsguru.com/guides/crimson-de sert/';
        } else if (gameContext === 'windrose') {
          offlineMsg = "I couldn't find a specific match for your question.\n\n" +
            'Here are our Windrose guides that might help:\n\n' +
            '  \u27a1\ufe0f Beginner Guide — Day 1 survival basics\n' +
            '  \u27a1\ufe0f Combat & Ship — Land + naval combat\n' +
            '  \u27a1\ufe0f Crafting & Gear — Best weapons & upgrades\n' +
            '  \u27a1\ufe0f Quest & Exploration — Treasure maps & secrets\n' +
            '  \u27a1\ufe0f Boss Guide — All bosses & farming routes\n' +
            '  \u27a1\ufe0f Base Building — Defenses & layout tips\n\n' +
            'You can also browse all guides at osrsguru.com/guides/windrose/';
        } else {
          // OSRS 默认
          offlineMsg = 'AI Assistant is being upgraded!\n\n' +
            'We are building a smarter knowledge base with 115+ guides,\n' +
            'real-time GE prices, and boss strategies.\n\n' +
            'In the meantime:\n' +
            '  Browse osrsguru.com for all guides\n' +
            '  Check the OSRS section for game-specific help\n\n' +
            'Expected back online soon!';
        }
        addMessage(messagesContainer, offlineMsg, 'assistant', false, CONFIG.sourceGuruLabel);
      })
      .then(function() {
        sendBtn.disabled = false;
      });
  }

  // ========== 辅助函数 ==========
  function addMessage(container, text, role, isLoading, source, title, url) {
    if (isLoading === undefined) isLoading = false;
    if (source === undefined) source = null;
    if (title === undefined) title = '';
    if (url === undefined) url = '';

    var messageDiv = document.createElement('div');
    messageDiv.className = 'qa-message ' + role;

    var bubble = document.createElement('div');
    bubble.className = 'qa-message-bubble' + (isLoading ? ' loading' : '');
    bubble.textContent = text;

    messageDiv.appendChild(bubble);

    // 添加来源标签
    if (!isLoading && source) {
      var sourceTag = document.createElement('div');
      sourceTag.className = 'qa-source';
      var sourceLabel = '';
      if (source === 'osrsguru') sourceLabel = '\uD83D\uDCDA ' + CONFIG.sourceGuruLabel;
      else if (source === 'osrs_wiki+deepseek') sourceLabel = '\uD83D\uDCDA+\uD83E\uDD16 Wiki + DeepSeek';
      else if (source === 'osrs_wiki') sourceLabel = '\uD83D\uDCD6 OSRS Wiki';
      else if (source === 'deepseek') sourceLabel = '\uD83E\uDD16 DeepSeek V3';
      else sourceLabel = '\uD83D\uDCDA ' + CONFIG.sourceGuruLabel;
      sourceTag.textContent = 'Source: ' + sourceLabel;
      messageDiv.appendChild(sourceTag);

      // 如果来自自己文章，添加可点击跳转链接
      if (source === 'osrsguru' && title && url) {
        addArticleLinkToDiv(messageDiv, title, url);
      }
    }

    container.appendChild(messageDiv);

    // 保持只显示最新 N 条消息
    while (container.children.length > CONFIG.maxMessages) {
      container.firstChild.remove();
    }

    // 自动滚动到最新消息
    container.scrollTop = container.scrollHeight;
  }

  // 直接在容器中添加文章链接（用于本地匹配结果）
  function addArticleLink(container, title, url) {
    var link = document.createElement('a');
    link.className = 'qa-article-link';
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener';
    link.innerHTML = '<span class="qa-link-icon">\uD83D\uDCD6</span>Read full guide: ' + title;

    var messageDiv = document.createElement('div');
    messageDiv.className = 'qa-message assistant';
    messageDiv.appendChild(link);
    container.appendChild(messageDiv);

    // 保持消息数量限制
    while (container.children.length > CONFIG.maxMessages) {
      container.firstChild.remove();
    }
    container.scrollTop = container.scrollHeight;
  }

  // 在已有消息div中添加文章链接
  function addArticleLinkToDiv(messageDiv, title, url) {
    var link = document.createElement('a');
    link.className = 'qa-article-link';
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener';
    link.innerHTML = '<span class="qa-link-icon">\uD83D\uDCD6</span>Read full guide: ' + title;
    messageDiv.appendChild(link);
  }

  // ========== 初始化 ==========
  function init() {
    // 注入样式
    injectStyles();

    // 创建浮窗
    var elements = createWidget();
    var widget = elements.widget;
    var toggleBtn = elements.toggleBtn;

    // 设置交互
    setupEventHandlers(widget, toggleBtn);

    console.log('\u2705 ' + CONFIG.assistantTitle + ' initialized');
  }

  // 等待 DOM 加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
