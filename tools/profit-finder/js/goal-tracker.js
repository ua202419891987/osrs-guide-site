/**
 * goal-tracker.js — OSRS Profit Finder Goal Tracker (付费用户专属)
 *
 * 设定目标（买Bond/攒装备/攒特定GP数），追踪进度，可视化完成度。
 * 数据持久化到 localStorage，集成 engine.js 推荐方法自动填写 GP/hr。
 *
 * Dependencies:
 *   - engine.js (window.engine) — 可选，用于自动建议赚钱方法
 *
 * Exports:
 *   window.goalTracker — 完整 API 对象
 *
 * Custom Events:
 *   goal:set       — 新目标设置时触发
 *   goal:updated   — 进度更新时触发
 *   goal:completed — 目标达成时触发
 */

(function () {
  'use strict';

  // ──────────────────────────── Constants ────────────────────────────

  /** localStorage key */
  var GOAL_KEY = 'osrsguru_profit_finder_goal';

  /** 预设目标列表 */
  var PRESET_GOALS = [
    { name: 'Buy an OSRS Bond', gp: 7400000 },
    { name: 'Dragon Hunter Lance', gp: 85000000 },
    { name: 'Toxic Blowpipe', gp: 2500000 },
    { name: 'Dragonfire Shield', gp: 20000000 },
    { name: 'Dexterous Prayer Scroll', gp: 22000000 },
    { name: 'Twisted Bow', gp: 1500000000 },
    { name: 'Scythe of Vitur', gp: 850000000 },
    { name: 'Custom Goal', gp: 0 }
  ];

  /** 默认目标结构 */
  var defaultGoal = {
    targetName: '',
    targetGP: 0,
    currentGP: 0,
    startGP: 0,
    methodId: '',
    gpPerHour: 0,
    sessionsPerDay: 0,
    hoursPerSession: 0,
    createdAt: null,
    lastUpdated: null,
    completed: false,
    history: []
  };

  // ──────────────────────── Module State ──────────────────────────────

  /** @type {Object|null} 当前目标（内存缓存） */
  var currentGoal = null;

  // ──────────────────── Core CRUD Functions ──────────────────────────

  /**
   * 初始化目标追踪器
   * - 从 localStorage 读取已有目标
   * - 如果有活跃（未完成）目标，自动渲染小部件
   */
  function initGoalTracker() {
    try {
      var saved = loadFromStorage();
      if (saved) {
        currentGoal = saved;
        // 如果有活跃目标，自动显示进度
        if (!currentGoal.completed) {
          renderGoalWidget();
        }
      }
      console.log('[GoalTracker] Initialized. Active goal:', currentGoal && !currentGoal.completed ? currentGoal.targetName : 'none');
    } catch (err) {
      console.error('[GoalTracker] Init error:', err.message);
      currentGoal = null;
    }
  }

  /**
   * 设置新目标
   * @param {Object} goalData - 目标数据对象
   * @param {string} goalData.targetName - 目标名称
   * @param {number} goalData.targetGP - 目标GP数额
   * @param {number} [goalData.startGP=0] - 起始GP
   * @param {string} [goalData.methodId=''] - 使用的赚钱方法ID
   * @param {number} [goalData.gpPerHour=0] - 该方法GP/hr
   * @param {number} [goalData.sessionsPerDay=0] - 每天进行几轮
   * @param {number} [goalData.hoursPerSession=0] - 每轮几小时
   * @returns {Object} 设置后的目标对象
   */
  function setGoal(goalData) {
    try {
      if (!goalData) {
        throw new Error('goalData is required');
      }
      if (!goalData.targetName || !goalData.targetGP || goalData.targetGP <= 0) {
        throw new Error('targetName and targetGP (>0) are required');
      }

      var now = Date.now();
      currentGoal = {
        targetName: goalData.targetName,
        targetGP: goalData.targetGP,
        currentGP: goalData.startGP || 0,
        startGP: goalData.startGP || 0,
        methodId: goalData.methodId || '',
        gpPerHour: goalData.gpPerHour || 0,
        sessionsPerDay: goalData.sessionsPerDay || 0,
        hoursPerSession: goalData.hoursPerSession || 0,
        createdAt: now,
        lastUpdated: now,
        completed: false,
        history: []
      };

      saveToStorage(currentGoal);
      renderGoalWidget();

      // 触发 goal:set 事件
      dispatchGoalEvent('goal:set', currentGoal);

      console.log('[GoalTracker] Goal set:', currentGoal.targetName, '-', formatGp(currentGoal.targetGP));
      return deepClone(currentGoal);
    } catch (err) {
      console.error('[GoalTracker] setGoal error:', err.message);
      return null;
    }
  }

  /**
   * 读取当前目标
   * @returns {Object|null}
   */
  function getGoal() {
    if (currentGoal) return deepClone(currentGoal);
    var saved = loadFromStorage();
    if (saved) {
      currentGoal = saved;
      return deepClone(currentGoal);
    }
    return null;
  }

  /**
   * 更新进度
   * @param {number} gpEarned - 本轮赚取的GP
   * @param {number} hoursPlayed - 本轮游戏时间（小时）
   * @returns {Object|null} 更新后的目标对象
   */
  function updateProgress(gpEarned, hoursPlayed) {
    try {
      var goal = getGoal();
      if (!goal) {
        throw new Error('No active goal found. Set a goal first.');
      }
      if (goal.completed) {
        throw new Error('Goal already completed. Reset to start a new one.');
      }

      gpEarned = Number(gpEarned) || 0;
      hoursPlayed = Number(hoursPlayed) || 0;

      // 追加到 history
      goal.history.push({
        date: new Date().toISOString(),
        gpEarned: gpEarned,
        hoursPlayed: hoursPlayed
      });

      // 更新 currentGP
      goal.currentGP += gpEarned;
      goal.lastUpdated = Date.now();

      // 检查是否达成目标
      if (goal.currentGP >= goal.targetGP) {
        goal.completed = true;
        goal.currentGP = goal.targetGP; // 修正不超过目标值
      }

      // 保存
      currentGoal = goal;
      saveToStorage(goal);
      renderGoalWidget();

      // 触发事件
      dispatchGoalEvent('goal:updated', goal);

      if (goal.completed) {
        dispatchGoalEvent('goal:completed', goal);
        console.log('[GoalTracker] GOAL COMPLETED!', goal.targetName);
      }

      return deepClone(goal);
    } catch (err) {
      console.error('[GoalTracker] updateProgress error:', err.message);
      return null;
    }
  }

  /**
   * 计算进度
   * @returns {Object} { percentage, earnedGP, targetGP, remainingGP, estimatedHours, estimatedDays }
   */
  function getProgress() {
    var goal = getGoal();
    if (!goal) {
      return {
        percentage: 0,
        earnedGP: 0,
        targetGP: 0,
        remainingGP: 0,
        estimatedHours: 0,
        estimatedDays: 0
      };
    }

    var earnedGP = goal.currentGP - goal.startGP;
    var targetGP = goal.targetGP - goal.startGP;
    var percentage = targetGP > 0 ? Math.min(100, Math.round((earnedGP / targetGP) * 100)) : 0;
    var remainingGP = Math.max(0, goal.targetGP - goal.currentGP);

    var estimated = calcEstimatedTime(
      remainingGP,
      goal.gpPerHour,
      goal.sessionsPerDay,
      goal.hoursPerSession
    );

    return {
      percentage: percentage,
      earnedGP: earnedGP,
      targetGP: targetGP,
      remainingGP: remainingGP,
      estimatedHours: estimated.hours,
      estimatedDays: estimated.days
    };
  }

  /**
   * 标记目标为已完成
   * @returns {Object|null}
   */
  function completeGoal() {
    try {
      var goal = getGoal();
      if (!goal) {
        throw new Error('No active goal found.');
      }
      if (goal.completed) {
        console.log('[GoalTracker] Goal already completed:', goal.targetName);
        return deepClone(goal);
      }

      goal.completed = true;
      goal.currentGP = goal.targetGP;
      goal.lastUpdated = Date.now();

      currentGoal = goal;
      saveToStorage(goal);
      renderGoalWidget();

      dispatchGoalEvent('goal:completed', goal);
      dispatchGoalEvent('goal:updated', goal);

      console.log('[GoalTracker] Goal manually completed:', goal.targetName);
      return deepClone(goal);
    } catch (err) {
      console.error('[GoalTracker] completeGoal error:', err.message);
      return null;
    }
  }

  /**
   * 清除目标数据
   */
  function resetGoal() {
    try {
      currentGoal = null;
      localStorage.removeItem(GOAL_KEY);
      // 隐藏进度显示，显示设置界面
      var setupEl = document.getElementById('goal-setup');
      var progressEl = document.getElementById('goal-progress');
      if (setupEl) setupEl.style.display = 'block';
      if (progressEl) progressEl.style.display = 'none';
      console.log('[GoalTracker] Goal reset.');
    } catch (err) {
      console.error('[GoalTracker] resetGoal error:', err.message);
    }
  }

  // ──────────────────── Estimated Time Calculation ───────────────────

  /**
   * 计算预计剩余时间
   * @param {number} remainingGP - 剩余GP
   * @param {number} gpPerHour - 每小时GP
   * @param {number} sessionsPerDay - 每天轮数
   * @param {number} hoursPerSession - 每轮小时数
   * @returns {{ hours: number, days: number }}
   */
  function calcEstimatedTime(remainingGP, gpPerHour, sessionsPerDay, hoursPerSession) {
    if (!gpPerHour || gpPerHour <= 0) {
      return { hours: 0, days: 0 };
    }

    var hours = Math.ceil(remainingGP / gpPerHour);
    var dailyHours = sessionsPerDay * hoursPerSession;
    var days = dailyHours > 0 ? Math.ceil(hours / dailyHours) : 0;

    return { hours: hours, days: days };
  }

  // ──────────────────── Suggestions from Engine ──────────────────────

  /**
   * 从 engine 获取推荐方法列表
   * @returns {Array<Object>} 推荐方法数组 [{ id, name, gpPerHour }]
   */
  function getSuggestedMethods() {
    try {
      // 检查 engine 是否加载且有缓存数据
      if (window.engine && window.engine.findBestMethods) {
        // 尝试读取上次答题结果 — 从 DOM 获取引擎结果卡片数据
        var resultCards = document.querySelectorAll('.result-card');
        if (resultCards && resultCards.length > 0) {
          var methods = [];
          for (var i = 0; i < resultCards.length; i++) {
            var card = resultCards[i];
            var methodId = card.getAttribute('data-method-id');
            var nameEl = card.querySelector('h3');
            var gpEl = card.querySelector('.gp-value');
            if (methodId && nameEl) {
              methods.push({
                id: methodId,
                name: nameEl.textContent.trim(),
                gpPerHour: gpEl ? parseGpValue(gpEl.textContent.trim()) : 0
              });
            }
          }
          if (methods.length > 0) return methods;
        }
      }

      // 无推荐：返回空数组
      return [];
    } catch (err) {
      console.warn('[GoalTracker] getSuggestedMethods error:', err.message);
      return [];
    }
  }

  // ──────────────────── Render ───────────────────────────────────────

  /**
   * 渲染目标追踪小部件
   * 将 UI 注入到 #goal-tracker 容器中
   */
  function renderGoalWidget() {
    try {
      var container = document.getElementById('goal-tracker');
      if (!container) {
        console.warn('[GoalTracker] #goal-tracker container not found in DOM.');
        return;
      }

      var goal = getGoal();

      if (!goal) {
        // 无目标：显示设置界面
        renderSetupView(container);
        return;
      }

      if (goal.completed) {
        // 已完成：显示完成界面
        renderCompletedView(container, goal);
        return;
      }

      // 进行中：显示进度界面
      renderProgressView(container, goal);
    } catch (err) {
      console.error('[GoalTracker] renderGoalWidget error:', err.message);
    }
  }

  /**
   * 渲染目标设置界面
   * @param {HTMLElement} container
   */
  function renderSetupView(container) {
    var setupHtml = buildSetupHTML();
    container.innerHTML = [
      '<div id="goal-setup">',
        setupHtml,
      '</div>',
      '<div id="goal-progress" style="display:none;"></div>'
    ].join('');

    // 绑定设置表单事件
    bindSetupEvents(container);
  }

  /**
   * 渲染进度界面
   * @param {HTMLElement} container
   * @param {Object} goal
   */
  function renderProgressView(container, goal) {
    var progress = getProgress();
    var progressHtml = buildProgressHTML(goal, progress);

    container.innerHTML = [
      '<div id="goal-setup" style="display:none;"></div>',
      '<div id="goal-progress">',
        progressHtml,
      '</div>'
    ].join('');

    // 绑定进度界面事件
    bindProgressEvents(container, goal);
  }

  /**
   * 渲染目标完成界面
   * @param {HTMLElement} container
   * @param {Object} goal
   */
  function renderCompletedView(container, goal) {
    var totalEarned = goal.currentGP - goal.startGP;
    var totalHours = 0;
    for (var i = 0; i < goal.history.length; i++) {
      totalHours += goal.history[i].hoursPlayed || 0;
    }

    var html = [
      '<div id="goal-setup" style="display:none;"></div>',
      '<div id="goal-progress">',
        '<div class="goal-completed-banner" style="text-align:center;padding:32px 20px;',
          'background:linear-gradient(135deg,rgba(34,197,94,0.1),rgba(245,158,11,0.1));',
          'border:2px solid rgba(34,197,94,0.3);border-radius:12px;margin-bottom:20px;">',
          '<div style="font-size:48px;margin-bottom:12px;">🎉</div>',
          '<h3 style="color:#22c55e;font-size:24px;margin:0 0 8px;">目标达成！</h3>',
          '<p style="color:#f1f5f9;font-size:18px;margin:0 0 4px;">',
            escapeHtml(goal.targetName),
          '</p>',
          '<p style="color:#94a3b8;font-size:14px;margin:0;">',
            '累计赚取 ', formatGp(totalEarned), ' GP',
            totalHours > 0 ? ' · 游戏时间 ' + totalHours.toFixed(1) + ' 小时' : '',
          '</p>',
        '</div>',
        '<div class="goal-actions" style="text-align:center;">',
          '<button class="goal-btn goal-btn-primary" data-action="set-new"',
          ' style="padding:10px 24px;background:linear-gradient(135deg,#f59e0b,#d97706);',
          'color:#1a1a2e;border:0;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer;">',
            '设置新目标',
          '</button>',
          ' ',
          '<button class="goal-btn goal-btn-secondary" data-action="reset"',
          ' style="padding:10px 24px;background:transparent;border:1px solid rgba(255,255,255,0.2);',
          'color:#94a3b8;border-radius:8px;font-size:16px;cursor:pointer;">',
            '清除',
          '</button>',
        '</div>',
      '</div>'
    ].join('');

    container.innerHTML = html;

    // 绑定完成界面按钮事件
    var setNewBtn = container.querySelector('[data-action="set-new"]');
    var resetBtn = container.querySelector('[data-action="reset"]');
    if (setNewBtn) {
      setNewBtn.addEventListener('click', function () {
        resetGoal();
      });
    }
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        resetGoal();
      });
    }
  }

  // ──────────────────── HTML Builders ────────────────────────────────

  /**
   * 构建设置界面的 HTML
   * @returns {string}
   */
  function buildSetupHTML() {
    // 预设目标选项
    var presetsHtml = '';
    for (var i = 0; i < PRESET_GOALS.length; i++) {
      var p = PRESET_GOALS[i];
      var gpDisplay = p.gp > 0 ? formatGp(p.gp) : '自定义数额';
      presetsHtml += [
        '<div class="goal-preset-option" data-gp="', p.gp, '" data-name="', escapeHtml(p.name), '"',
        ' style="padding:10px 16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);',
        'border-radius:8px;cursor:pointer;transition:all 0.2s;margin-bottom:8px;',
        'display:flex;justify-content:space-between;align-items:center;"',
        ' onmouseover="this.style.borderColor=\'#f59e0b\';this.style.background=\'rgba(245,158,11,0.08)\'"',
        ' onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\';this.style.background=\'rgba(255,255,255,0.04)\'">',
          '<span style="color:#f1f5f9;font-size:15px;font-weight:500;">', escapeHtml(p.name), '</span>',
          '<span style="color:#f59e0b;font-size:14px;font-weight:600;">', gpDisplay, '</span>',
        '</div>'
      ].join('');
    }

    // 建议方法下拉选项
    var suggestedMethods = getSuggestedMethods();
    var methodOptionsHtml = '<option value="">-- 不选择方法（手动输入GP/hr） --</option>';
    for (var m = 0; m < suggestedMethods.length; m++) {
      methodOptionsHtml += [
        '<option value="', escapeHtml(suggestedMethods[m].id), '"',
        ' data-gp="', suggestedMethods[m].gpPerHour, '"',
        '>',
          escapeHtml(suggestedMethods[m].name), ' (', formatGp(suggestedMethods[m].gpPerHour), '/hr)',
        '</option>'
      ].join('');
    }

    return [
      '<div class="goal-header" style="margin-bottom:20px;">',
        '<h3 style="color:#f59e0b;font-size:20px;margin:0 0 4px;">🎯 目标追踪器</h3>',
        '<p style="color:#94a3b8;font-size:13px;margin:0;">设定一个GP目标，追踪你的赚钱进度</p>',
      '</div>',

      // 预设目标选择
      '<div class="goal-presets" style="margin-bottom:20px;">',
        '<label style="display:block;color:#cbd5e1;font-size:14px;font-weight:500;margin-bottom:8px;">选择目标</label>',
        presetsHtml,
      '</div>',

      // 自定义目标表单
      '<div class="goal-custom-form" id="goal-custom-form" style="display:none;margin-bottom:20px;',
        'padding:16px;background:rgba(255,255,255,0.03);border-radius:8px;border:1px solid rgba(255,255,255,0.06);">',
        '<label style="display:block;color:#cbd5e1;font-size:14px;font-weight:500;margin-bottom:6px;">自定义目标名称</label>',
        '<input type="text" id="goal-custom-name" placeholder="例如: Bandos Chestplate"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
        'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;',
        'margin-bottom:12px;">',
        '<label style="display:block;color:#cbd5e1;font-size:14px;font-weight:500;margin-bottom:6px;">目标GP数额</label>',
        '<input type="number" id="goal-custom-gp" placeholder="例如: 50000000" min="1" step="1000"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
        'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;">',
      '</div>',

      // 赚钱方法选择
      '<div class="goal-method-section" style="margin-bottom:20px;">',
        '<label style="display:block;color:#cbd5e1;font-size:14px;font-weight:500;margin-bottom:8px;">使用的赚钱方法（可选）',
          suggestedMethods.length > 0 ? ' — 检测到推荐方法' : '',
        '</label>',
        '<select id="goal-method-select"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);',
        'border:1px solid rgba(255,255,255,0.1);border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;',
        'box-sizing:border-box;margin-bottom:12px;appearance:auto;">',
          methodOptionsHtml,
        '</select>',

        '<label style="display:block;color:#cbd5e1;font-size:14px;font-weight:500;margin-bottom:6px;">GP / 小时</label>',
        '<input type="number" id="goal-gp-per-hour" placeholder="例如: 500000" min="0" step="1000"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
        'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;">',

        '<div style="display:flex;gap:12px;margin-top:12px;">',
          '<div style="flex:1;">',
            '<label style="display:block;color:#cbd5e1;font-size:13px;font-weight:500;margin-bottom:6px;">每天轮数</label>',
            '<input type="number" id="goal-sessions-day" placeholder="1" min="0"',
            ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
            'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;">',
          '</div>',
          '<div style="flex:1;">',
            '<label style="display:block;color:#cbd5e1;font-size:13px;font-weight:500;margin-bottom:6px;">每轮小时数</label>',
            '<input type="number" id="goal-hours-session" placeholder="1" min="0" step="0.5"',
            ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
            'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;">',
          '</div>',
        '</div>',

        '<label style="display:block;color:#cbd5e1;font-size:14px;font-weight:500;margin-bottom:6px;margin-top:12px;">起始GP（可选）</label>',
        '<input type="number" id="goal-start-gp" placeholder="0" min="0" step="1000"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
        'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;">',
      '</div>',

      // 确认按钮
      '<div class="goal-actions" style="text-align:center;">',
        '<button id="goal-start-btn"',
        ' style="padding:12px 32px;background:linear-gradient(135deg,#f59e0b,#d97706);',
        'color:#1a1a2e;border:0;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer;',
        'transition:opacity 0.2s;width:100%;"',
        ' onmouseover="this.style.opacity=\'0.9\'" onmouseout="this.style.opacity=\'1\'">',
          '🚀 开始追踪！',
        '</button>',
      '</div>'
    ].join('');
  }

  /**
   * 构建进度界面的 HTML
   * @param {Object} goal
   * @param {Object} progress
   * @returns {string}
   */
  function buildProgressHTML(goal, progress) {
    var pct = progress.percentage;
    var barFilled = Math.round(pct / 10); // 每10%一格
    var barEmpty = 10 - barFilled;
    if (barFilled > 10) barFilled = 10;
    if (barEmpty < 0) barEmpty = 0;

    // 进度条：████████░░
    var bar = '';
    for (var f = 0; f < barFilled; f++) bar += '█';
    for (var e = 0; e < barEmpty; e++) bar += '░';

    // 时间估计提示
    var estHtml = '';
    if (progress.estimatedHours > 0) {
      estHtml = '预计还需 ';
      if (progress.estimatedDays > 0) {
        estHtml += progress.estimatedHours + ' 小时 (' + progress.estimatedDays + ' 天)';
      } else {
        estHtml += progress.estimatedHours + ' 小时';
      }
    } else if (goal.gpPerHour > 0) {
      estHtml = '目标已达成（或剩余GP为0）';
    } else {
      estHtml = '请设置GP/hr以查看预计时间';
    }

    // 进度条颜色
    var barColor = '#22c55e';
    if (pct < 30) barColor = '#ef4444';
    else if (pct < 70) barColor = '#f59e0b';

    // 最新历史记录（最近5条）
    var historyHtml = '';
    var history = goal.history || [];
    var recentHistory = history.slice(-5);
    if (recentHistory.length > 0) {
      historyHtml += '<div class="goal-history" style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);">';
      historyHtml += '<h4 style="color:#94a3b8;font-size:13px;font-weight:500;margin:0 0 8px;">最近记录</h4>';
      for (var h = recentHistory.length - 1; h >= 0; h--) {
        var rec = recentHistory[h];
        var dateStr = rec.date ? rec.date.substring(0, 10) : '--';
        historyHtml += [
          '<div style="display:flex;justify-content:space-between;padding:4px 0;font-size:13px;">',
            '<span style="color:#64748b;">', dateStr, '</span>',
            '<span style="color:#22c55e;">+', formatGp(rec.gpEarned), '</span>',
            '<span style="color:#94a3b8;">', rec.hoursPlayed || 0, 'h</span>',
          '</div>'
        ].join('');
      }
      historyHtml += '</div>';
    }

    return [
      '<div class="goal-header" style="margin-bottom:16px;display:flex;justify-content:space-between;align-items:flex-start;">',
        '<div>',
          '<h3 style="color:#f59e0b;font-size:18px;margin:0 0 4px;">🎯 ', escapeHtml(goal.targetName), '</h3>',
          '<p style="color:#94a3b8;font-size:13px;margin:0;">',
            goal.methodId ? '方法: ' + escapeHtml(goal.methodId) : '',
          '</p>',
        '</div>',
        '<button class="goal-btn-goal-reset" data-action="reset"',
        ' style="background:transparent;border:1px solid rgba(255,255,255,0.15);color:#94a3b8;',
        'border-radius:6px;padding:4px 12px;font-size:12px;cursor:pointer;">',
          '重置',
        '</button>',
      '</div>',

      // 进度条
      '<div class="goal-progress-bar-container" style="margin-bottom:12px;">',
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">',
          '<span style="color:#f1f5f9;font-size:13px;">进度</span>',
          '<span style="color:', barColor, ';font-size:15px;font-weight:700;">', pct, '%</span>',
        '</div>',
        '<div style="background:rgba(255,255,255,0.08);border-radius:8px;padding:10px 14px;',
          'font-family:monospace;font-size:18px;letter-spacing:2px;color:', barColor, ';text-align:center;">',
          bar,
        '</div>',
      '</div>',

      // GP数据
      '<div class="goal-stats" style="display:flex;justify-content:space-between;margin-bottom:16px;">',
        '<div style="text-align:center;flex:1;">',
          '<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">已赚</div>',
          '<div style="color:#22c55e;font-size:18px;font-weight:700;">', formatGp(progress.earnedGP), '</div>',
        '</div>',
        '<div style="text-align:center;flex:1;">',
          '<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">目标</div>',
          '<div style="color:#f1f5f9;font-size:18px;font-weight:700;">', formatGp(goal.targetGP), '</div>',
        '</div>',
        '<div style="text-align:center;flex:1;">',
          '<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">剩余</div>',
          '<div style="color:#f59e0b;font-size:18px;font-weight:700;">', formatGp(progress.remainingGP), '</div>',
        '</div>',
      '</div>',

      // 预计时间
      '<div class="goal-estimate" style="text-align:center;padding:10px;',
        'background:rgba(245,158,11,0.06);border-radius:8px;margin-bottom:16px;">',
        '<span style="color:#cbd5e1;font-size:14px;">', estHtml, '</span>',
      '</div>',

      // 进度更新表单
      '<div class="goal-update-form" style="padding:16px;background:rgba(255,255,255,0.03);',
        'border:1px solid rgba(255,255,255,0.06);border-radius:8px;margin-bottom:16px;">',
        '<h4 style="color:#cbd5e1;font-size:14px;font-weight:500;margin:0 0 12px;">更新进度</h4>',

        '<label style="display:block;color:#94a3b8;font-size:13px;margin-bottom:4px;">今天赚了多少GP？</label>',
        '<input type="number" id="goal-update-gp" placeholder="例如: 500000" min="0" step="1000"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
        'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;margin-bottom:10px;">',

        '<label style="display:block;color:#94a3b8;font-size:13px;margin-bottom:4px;">今天玩了几小时？</label>',
        '<input type="number" id="goal-update-hours" placeholder="例如: 2" min="0" step="0.5"',
        ' style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);',
        'border-radius:6px;color:#f1f5f9;font-size:14px;outline:none;box-sizing:border-box;margin-bottom:12px;">',

        '<button id="goal-update-btn"',
        ' style="width:100%;padding:10px 0;background:linear-gradient(135deg,#22c55e,#16a34a);',
        'color:#fff;border:0;border-radius:6px;font-size:15px;font-weight:600;cursor:pointer;',
        'transition:opacity 0.2s;"',
        ' onmouseover="this.style.opacity=\'0.9\'" onmouseout="this.style.opacity=\'1\'">',
          '更新进度',
        '</button>',
      '</div>',

      historyHtml,

      // 完成目标按钮
      '<div class="goal-actions" style="text-align:center;margin-top:12px;">',
        '<button id="goal-complete-btn"',
        ' style="padding:10px 24px;background:transparent;border:1px solid rgba(34,197,94,0.3);',
        'color:#22c55e;border-radius:8px;font-size:14px;font-weight:500;cursor:pointer;',
        'transition:all 0.2s;width:100%;"',
        ' onmouseover="this.style.background=\'rgba(34,197,94,0.1)\'"',
        ' onmouseout="this.style.background=\'transparent\'">',
          '✓ 完成目标！',
        '</button>',
      '</div>'
    ].join('');
  }

  // ──────────────────── Event Binding ────────────────────────────────

  /**
   * 绑定设置界面的事件
   * @param {HTMLElement} container
   */
  function bindSetupEvents(container) {
    // 预设目标点击
    var presetOptions = container.querySelectorAll('.goal-preset-option');
    for (var i = 0; i < presetOptions.length; i++) {
      presetOptions[i].addEventListener('click', function () {
        var gp = parseInt(this.getAttribute('data-gp'), 10);
        var name = this.getAttribute('data-name');

        if (gp === 0) {
          // Custom Goal — 显示自定义表单
          var customForm = document.getElementById('goal-custom-form');
          if (customForm) customForm.style.display = 'block';
          // 清除其他预设的高亮
          highlightPreset(this, presetOptions);
          return;
        }

        // 隐藏自定义表单
        var customForm = document.getElementById('goal-custom-form');
        if (customForm) customForm.style.display = 'none';

        // 高亮选中
        highlightPreset(this, presetOptions);

        // 自动填充GP/hr输入框为空
        var gpPerHourInput = document.getElementById('goal-gp-per-hour');
        if (gpPerHourInput && !gpPerHourInput.value) {
          gpPerHourInput.focus();
        }
      });
    }

    // 方法选择变化 — 自动填充GP/hr
    var methodSelect = document.getElementById('goal-method-select');
    if (methodSelect) {
      methodSelect.addEventListener('change', function () {
        var selected = this.options[this.selectedIndex];
        var gp = parseInt(selected.getAttribute('data-gp'), 10);
        var gpInput = document.getElementById('goal-gp-per-hour');
        if (gpInput && gp > 0) {
          gpInput.value = gp;
        }
      });
    }

    // 开始追踪按钮
    var startBtn = document.getElementById('goal-start-btn');
    if (startBtn) {
      startBtn.addEventListener('click', function () {
        handleStartGoal();
      });
    }

    // 回车键支持
    var inputs = container.querySelectorAll('input');
    for (var j = 0; j < inputs.length; j++) {
      inputs[j].addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          handleStartGoal();
        }
      });
    }
  }

  /**
   * 绑定进度界面的事件
   * @param {HTMLElement} container
   * @param {Object} goal
   */
  function bindProgressEvents(container, goal) {
    // 重置按钮
    var resetBtn = container.querySelector('[data-action="reset"]');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        if (confirm('确定要重置目标吗？所有进度数据将丢失。')) {
          resetGoal();
        }
      });
    }

    // 更新进度按钮
    var updateBtn = document.getElementById('goal-update-btn');
    if (updateBtn) {
      updateBtn.addEventListener('click', function () {
        handleUpdateProgress();
      });
    }

    // 回车键支持
    var updateInputs = container.querySelectorAll('#goal-update-gp, #goal-update-hours');
    for (var i = 0; i < updateInputs.length; i++) {
      updateInputs[i].addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          handleUpdateProgress();
        }
      });
    }

    // 完成目标按钮
    var completeBtn = document.getElementById('goal-complete-btn');
    if (completeBtn) {
      completeBtn.addEventListener('click', function () {
        if (confirm('确定要标记"'+ goal.targetName +'"为已完成吗？')) {
          completeGoal();
        }
      });
    }
  }

  /**
   * 处理开始追踪
   */
  function handleStartGoal() {
    try {
      // 获取选中的预设
      var selectedPreset = document.querySelector('.goal-preset-option.selected');
      var targetName = '';
      var targetGP = 0;

      if (selectedPreset) {
        targetName = selectedPreset.getAttribute('data-name');
        targetGP = parseInt(selectedPreset.getAttribute('data-gp'), 10);
      }

      // 如果是 Custom Goal，从自定义表单读取
      if (targetGP === 0 || targetName === 'Custom Goal') {
        var customNameInput = document.getElementById('goal-custom-name');
        var customGPInput = document.getElementById('goal-custom-gp');
        if (customNameInput && customGPInput) {
          targetName = customNameInput.value.trim() || 'Custom Goal';
          targetGP = parseInt(customGPInput.value, 10);
        }
      }

      if (!targetName || !targetGP || targetGP <= 0) {
        alert('请选择一个目标或填写自定义目标和GP数额。');
        return;
      }

      // 读取方法参数
      var methodSelect = document.getElementById('goal-method-select');
      var methodId = methodSelect ? methodSelect.value : '';
      var gpPerHour = parseInt(document.getElementById('goal-gp-per-hour').value, 10) || 0;
      var sessionsPerDay = parseInt(document.getElementById('goal-sessions-day').value, 10) || 0;
      var hoursPerSession = parseFloat(document.getElementById('goal-hours-session').value) || 0;
      var startGP = parseInt(document.getElementById('goal-start-gp').value, 10) || 0;

      setGoal({
        targetName: targetName,
        targetGP: targetGP,
        startGP: startGP,
        methodId: methodId,
        gpPerHour: gpPerHour,
        sessionsPerDay: sessionsPerDay,
        hoursPerSession: hoursPerSession
      });
    } catch (err) {
      console.error('[GoalTracker] handleStartGoal error:', err.message);
      alert('设置目标失败，请重试。');
    }
  }

  /**
   * 处理更新进度
   */
  function handleUpdateProgress() {
    try {
      var gpInput = document.getElementById('goal-update-gp');
      var hoursInput = document.getElementById('goal-update-hours');

      var gpEarned = parseFloat(gpInput ? gpInput.value : 0) || 0;
      var hoursPlayed = parseFloat(hoursInput ? hoursInput.value : 0) || 0;

      if (gpEarned <= 0) {
        alert('请输入赚取的GP数额（大于0）。');
        return;
      }

      var result = updateProgress(gpEarned, hoursPlayed);
      if (result) {
        // 清空输入
        if (gpInput) gpInput.value = '';
        if (hoursInput) hoursInput.value = '';
      }
    } catch (err) {
      console.error('[GoalTracker] handleUpdateProgress error:', err.message);
      alert('更新进度失败，请重试。');
    }
  }

  // ──────────────────── Utility Helpers ──────────────────────────────

  /**
   * 高亮选中的预设目标
   * @param {HTMLElement} selected
   * @param {NodeList} allOptions
   */
  function highlightPreset(selected, allOptions) {
    for (var i = 0; i < allOptions.length; i++) {
      allOptions[i].classList.remove('selected');
      allOptions[i].style.borderColor = 'rgba(255,255,255,0.08)';
      allOptions[i].style.background = 'rgba(255,255,255,0.04)';
    }
    selected.classList.add('selected');
    selected.style.borderColor = '#f59e0b';
    selected.style.background = 'rgba(245,158,11,0.12)';
  }

  /**
   * 格式化GP数值显示
   * @param {number} value
   * @returns {string}
   */
  function formatGp(value) {
    if (value === undefined || value === null || isNaN(value)) return '0';
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    }
    if (value >= 1000) {
      return (value / 1000).toFixed(0) + 'K';
    }
    return Number(value).toLocaleString();
  }

  /**
   * 从格式化后的GP字符串解析数值（反向formatGp）
   * @param {string} str - 例如 "1.5M"、"500K"、"1234"
   * @returns {number}
   */
  function parseGpValue(str) {
    if (typeof str !== 'string') return 0;
    str = str.trim().toUpperCase();
    if (str.indexOf('M') !== -1) {
      return parseFloat(str) * 1000000;
    }
    if (str.indexOf('K') !== -1) {
      return parseFloat(str) * 1000;
    }
    return parseInt(str.replace(/,/g, ''), 10) || 0;
  }

  /**
   * Escape HTML 防止 XSS
   * @param {*} str
   * @returns {string}
   */
  function escapeHtml(str) {
    if (typeof str !== 'string') {
      str = String(str || '');
    }
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * 保存目标到 localStorage
   * @param {Object} goal
   */
  function saveToStorage(goal) {
    try {
      localStorage.setItem(GOAL_KEY, JSON.stringify(goal));
    } catch (err) {
      console.error('[GoalTracker] Failed to save to localStorage:', err.message);
    }
  }

  /**
   * 从 localStorage 读取目标
   * @returns {Object|null}
   */
  function loadFromStorage() {
    try {
      var raw = localStorage.getItem(GOAL_KEY);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      // 基本验证
      if (parsed && parsed.targetName && typeof parsed.targetGP === 'number') {
        return parsed;
      }
      return null;
    } catch (err) {
      console.warn('[GoalTracker] Failed to load from localStorage:', err.message);
      return null;
    }
  }

  /**
   * 深度克隆对象
   * @param {*} obj
   * @returns {*}
   */
  function deepClone(obj) {
    try {
      return JSON.parse(JSON.stringify(obj));
    } catch (err) {
      return obj;
    }
  }

  /**
   * 派发自定义事件
   * @param {string} eventName
   * @param {Object} detail
   */
  function dispatchGoalEvent(eventName, detail) {
    try {
      var event = new CustomEvent(eventName, {
        detail: deepClone(detail || {}),
        bubbles: true
      });
      document.dispatchEvent(event);
    } catch (err) {
      console.warn('[GoalTracker] Failed to dispatch event:', eventName, err.message);
    }
  }

  // ──────────────────── Global Exports ───────────────────────────────

  /** 完整 API */
  window.goalTracker = {
    initGoalTracker: initGoalTracker,
    setGoal: setGoal,
    getGoal: getGoal,
    updateProgress: updateProgress,
    getProgress: getProgress,
    completeGoal: completeGoal,
    resetGoal: resetGoal,
    renderGoalWidget: renderGoalWidget,
    calcEstimatedTime: calcEstimatedTime,
    getSuggestedMethods: getSuggestedMethods,
    PRESET_GOALS: PRESET_GOALS,
    defaultGoal: defaultGoal,
    GOAL_KEY: GOAL_KEY
  };

  // ──────────────────── Auto-Init ─────────────────────────────────────

  // DOM 加载完成后自动初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initGoalTracker();
    });
  } else {
    initGoalTracker();
  }

  // 监听 profit-finder:reset 事件，清除目标关联状态
  document.addEventListener('profit-finder:reset', function () {
    // 不主动清除目标数据，但重新渲染小部件同步状态
    if (document.getElementById('goal-tracker')) {
      renderGoalWidget();
    }
  });

})();
