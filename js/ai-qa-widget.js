/**
 * OSRS Guru AI Question & Answer Widget
 * 右下角悬浮窗 - AI 问答系统
 * 集成 RAG API
 */

(function () {
  'use strict';

  // ========== 配置 ==========
  const CONFIG = {
    apiBase: window.location.hostname === 'localhost' 
      ? 'http://localhost:8000' 
      : 'https://osrs-rag-api.vercel.app', // 生产环境 API 地址
    widgetId: 'osrs-qa-widget',
    widgetButtonId: 'osrs-qa-toggle-btn',
    maxMessages: 10,
  };

  // ========== CSS 注入 ==========
  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
/* AI 问答浮窗 - 核心样式 */
#osrs-qa-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 420px;
  max-height: 600px;
  background: linear-gradient(135deg, rgba(39, 33, 26, 0.98), rgba(59, 38, 21, 0.95));
  border: 2px solid rgba(212, 175, 55, 0.4);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 
              0 0 20px rgba(212, 175, 55, 0.15);
  display: none;
  flex-direction: column;
  z-index: 10000;
  font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
  overflow: hidden;
}

#osrs-qa-widget.open {
  display: flex;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 头部 */
#osrs-qa-widget .qa-header {
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.15), rgba(212, 175, 55, 0.08));
  border-bottom: 1px solid rgba(212, 175, 55, 0.25);
  padding: 16px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

#osrs-qa-widget .qa-header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #d4af37;
  font-family: 'Cinzel', serif;
}

#osrs-qa-widget .qa-header-title .qa-icon {
  font-size: 18px;
}

#osrs-qa-widget .qa-close-btn {
  background: none;
  border: none;
  color: rgba(212, 175, 55, 0.6);
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s;
}

#osrs-qa-widget .qa-close-btn:hover {
  color: #d4af37;
}

/* 消息区域 */
#osrs-qa-widget .qa-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

#osrs-qa-widget .qa-message {
  display: flex;
  gap: 8px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

#osrs-qa-widget .qa-message.user {
  justify-content: flex-end;
}

#osrs-qa-widget .qa-message.assistant {
  justify-content: flex-start;
}

#osrs-qa-widget .qa-message-bubble {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.5;
  word-wrap: break-word;
}

#osrs-qa-widget .qa-message.user .qa-message-bubble {
  background: rgba(212, 175, 55, 0.25);
  border: 1px solid rgba(212, 175, 55, 0.35);
  color: #e8d5b5;
}

#osrs-qa-widget .qa-message.assistant .qa-message-bubble {
  background: rgba(100, 80, 60, 0.4);
  border: 1px solid rgba(212, 175, 55, 0.2);
  color: #d4af37;
}

#osrs-qa-widget .qa-message.assistant .qa-message-bubble.loading {
  display: flex;
  align-items: center;
  gap: 6px;
  min-height: 24px;
}

#osrs-qa-widget .qa-message.assistant .qa-message-bubble.loading::after {
  content: '';
  display: inline-block;
  width: 4px;
  height: 4px;
  background: #d4af37;
  border-radius: 50%;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

/* 信息源标签 */
#osrs-qa-widget .qa-source {
  font-size: 11px;
  color: rgba(212, 175, 55, 0.6);
  margin-top: 4px;
  font-style: italic;
}

/* 输入区域 */
#osrs-qa-widget .qa-input-group {
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

#osrs-qa-widget .qa-input-group input {
  flex: 1;
  background: rgba(59, 38, 21, 0.6);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 6px;
  padding: 8px 12px;
  color: #d4af37;
  font-size: 13px;
  font-family: inherit;
  transition: border-color 0.2s;
}

#osrs-qa-widget .qa-input-group input::placeholder {
  color: rgba(212, 175, 55, 0.4);
}

#osrs-qa-widget .qa-input-group input:focus {
  outline: none;
  border-color: rgba(212, 175, 55, 0.5);
  background: rgba(59, 38, 21, 0.8);
}

#osrs-qa-widget .qa-send-btn {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.35), rgba(212, 175, 55, 0.2));
  border: 1px solid rgba(212, 175, 55, 0.4);
  border-radius: 6px;
  color: #d4af37;
  font-size: 15px;
  cursor: pointer;
  padding: 6px 12px;
  transition: all 0.2s;
  font-weight: 600;
}

#osrs-qa-widget .qa-send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.5), rgba(212, 175, 55, 0.35));
  border-color: rgba(212, 175, 55, 0.6);
  transform: scale(1.02);
}

#osrs-qa-widget .qa-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 浮窗打开按钮 */
#osrs-qa-toggle-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.6), rgba(212, 175, 55, 0.4));
  border: 2px solid rgba(212, 175, 55, 0.8);
  border-radius: 50%;
  color: #1a0f08;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

#osrs-qa-toggle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.8), rgba(212, 175, 55, 0.6));
}

#osrs-qa-toggle-btn.hide {
  display: none;
}

/* 响应式设计 */
@media (max-width: 600px) {
  #osrs-qa-widget {
    width: 100%;
    height: 100%;
    max-height: 100%;
    bottom: 0;
    right: 0;
    border-radius: 0;
    max-height: 80vh;
  }
  
  #osrs-qa-toggle-btn {
    bottom: 20px;
    right: 20px;
  }
}

/* 消息滚动条样式 */
#osrs-qa-widget .qa-messages::-webkit-scrollbar {
  width: 6px;
}

#osrs-qa-widget .qa-messages::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

#osrs-qa-widget .qa-messages::-webkit-scrollbar-thumb {
  background: rgba(212, 175, 55, 0.25);
  border-radius: 3px;
}

#osrs-qa-widget .qa-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 175, 55, 0.4);
}
    `;
    document.head.appendChild(style);
  }

  // ========== HTML 结构创建 ==========
  function createWidget() {
    // 浮窗主体
    const widget = document.createElement('div');
    widget.id = CONFIG.widgetId;
    widget.innerHTML = `
      <div class="qa-header">
        <div class="qa-header-title">
          <span class="qa-icon">🤖</span>
          <span>OSRS AI Assistant</span>
        </div>
        <button class="qa-close-btn" aria-label="Close AI widget">✕</button>
      </div>
      <div class="qa-messages"></div>
      <div class="qa-input-group">
        <input 
          type="text" 
          class="qa-input" 
          placeholder="Ask about OSRS guides..." 
          aria-label="Ask a question"
        />
        <button class="qa-send-btn" aria-label="Send message">Send</button>
      </div>
    `;

    // 打开按钮
    const toggleBtn = document.createElement('button');
    toggleBtn.id = CONFIG.widgetButtonId;
    toggleBtn.innerHTML = '💬';
    toggleBtn.title = 'Open OSRS AI Assistant';

    // 添加到页面
    document.body.appendChild(widget);
    document.body.appendChild(toggleBtn);

    return { widget, toggleBtn };
  }

  // ========== 交互逻辑 ==========
  function setupEventHandlers(widget, toggleBtn) {
    const closeBtn = widget.querySelector('.qa-close-btn');
    const sendBtn = widget.querySelector('.qa-send-btn');
    const input = widget.querySelector('.qa-input');
    const messagesContainer = widget.querySelector('.qa-messages');

    // 打开/关闭浮窗
    toggleBtn.addEventListener('click', () => {
      widget.classList.toggle('open');
      if (widget.classList.contains('open')) {
        input.focus();
      }
    });

    closeBtn.addEventListener('click', () => {
      widget.classList.remove('open');
    });

    // 发送消息
    const sendMessage = async () => {
      const message = input.value.trim();
      if (!message) return;

      // 显示用户消息
      addMessage(messagesContainer, message, 'user');
      input.value = '';
      sendBtn.disabled = true;

      // 显示加载状态
      addMessage(messagesContainer, 'Loading...', 'assistant', true);

      try {
        // 调用 RAG API
        const response = await fetch(`${CONFIG.apiBase}/rag-api/search?q=${encodeURIComponent(message)}`);
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        
        // 移除加载消息
        const loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }

        // 显示 AI 回复
        const answer = data.answer || 'No answer available';
        const source = data.source || 'unknown';
        addMessage(messagesContainer, answer, 'assistant', false, source);
      } catch (error) {
        console.error('RAG API error:', error);
        
        // 移除加载消息
        const loadingMsg = messagesContainer.lastElementChild;
        if (loadingMsg && loadingMsg.querySelector('.qa-message-bubble.loading')) {
          loadingMsg.remove();
        }

        // 显示错误消息
        addMessage(
          messagesContainer, 
          'Sorry, I couldn\'t reach the knowledge base. Please try again.',
          'assistant'
        );
      } finally {
        sendBtn.disabled = false;
      }
    };

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendMessage();
    });
  }

  // ========== 辅助函数 ==========
  function addMessage(container, text, role = 'user', isLoading = false, source = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `qa-message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'qa-message-bubble' + (isLoading ? ' loading' : '');
    bubble.textContent = text;

    messageDiv.appendChild(bubble);

    // 添加来源标签
    if (!isLoading && source) {
      const sourceTag = document.createElement('div');
      sourceTag.className = 'qa-source';
      // 三段式 source 标签：数据源 + AI 模型
      let sourceLabel = '';
      if (source === 'osrsguru_rag') sourceLabel = '📚 OSRS Guru';
      else if (source === 'osrsguru_wiki') sourceLabel = '📚+📖 Guides + Wiki';
      else if (source === 'osrs_wiki') sourceLabel = '📖 OSRS Wiki';
      else if (source === 'osrsguru_fallback') sourceLabel = '⚠️ OSRS Guru (offline)';
      else sourceLabel = '📚 OSRS Guru';
      sourceTag.textContent = `Source: ${sourceLabel}`;
      messageDiv.appendChild(sourceTag);
    }

    container.appendChild(messageDiv);

    // 保持只显示最新 N 条消息
    while (container.children.length > CONFIG.maxMessages) {
      container.firstChild.remove();
    }

    // 自动滚动到最新消息
    container.scrollTop = container.scrollHeight;
  }

  // ========== 初始化 ==========
  function init() {
    // 注入样式
    injectStyles();

    // 创建浮窗
    const { widget, toggleBtn } = createWidget();

    // 设置交互
    setupEventHandlers(widget, toggleBtn);

    console.log('✅ OSRS AI QA Widget initialized');
  }

  // 等待 DOM 加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
