/**
 * profit-flow.js — OSRS Profit Finder Question Flow Engine
 *
 * Manages 6-question wizard flow: step navigation, option selection,
 * progress indicators, validation, submission with loading animation,
 * and "Try Again" reset. Reads data from index.html DOM structure.
 */

(function () {
  'use strict';

  // ============================================================
  //  STATE
  // ============================================================

  const answerKeyMap = ['membership', 'combat', 'skill', 'time', 'attention', 'goal'];

  /** Maps HTML data-value → canonical state value */
  function normalizeValue(questionIndex, rawValue) {
    // Q1 membership: "f2p"→"f2p", "p2p"→"p2p" — no change
    if (questionIndex === 0) return rawValue;

    // Q2 combat: "90plus"→"90+", rest unchanged
    if (questionIndex === 1) {
      const map = { '90plus': '90+' };
      return map[rawValue] || rawValue;
    }

    // Q3 skill: same as HTML
    if (questionIndex === 2) return rawValue;

    // Q4 time: "2hplus"→"2h+", rest unchanged
    if (questionIndex === 3) {
      const map = { '2hplus': '2h+' };
      return map[rawValue] || rawValue;
    }

    // Q5 attention: "full-afk"→"fullAfk", "semi-afk"→"semiAfk", "high-risk"→"highRisk"
    if (questionIndex === 4) {
      const map = {
        'full-afk': 'fullAfk',
        'semi-afk': 'semiAfk',
        'high-risk': 'highRisk'
      };
      return map[rawValue] || rawValue;
    }

    // Q6 goal: "first-bond"→"firstBond", "gear-upgrade"→"gearUpgrade",
    // "big-item"→"bigItem", "max-gp"→"maxGp"
    if (questionIndex === 5) {
      const map = {
        'first-bond': 'firstBond',
        'gear-upgrade': 'gearUpgrade',
        'big-item': 'bigItem',
        'max-gp': 'maxGp'
      };
      return map[rawValue] || rawValue;
    }

    return rawValue;
  }

  const state = {
    currentStep: 1,
    totalSteps: 6,
    answers: {
      membership: null,
      combat: null,
      skill: null,
      time: null,
      attention: null,
      goal: null
    }
  };

  // ============================================================
  //  DOM REFS (populated on init)
  // ============================================================

  let dom = {};

  function cacheDom() {
    dom = {
      cards: document.querySelectorAll('.question-card'),
      progressFill: document.getElementById('progressFill'),
      progressLabel: document.getElementById('progressLabel'),
      questionsFlow: document.getElementById('questionsFlow'),
      resultsArea: document.getElementById('resultsArea'),
      resultsList: document.getElementById('resultsList')
    };

    // Create progress step indicators if not present
    if (!document.querySelector('.progress-steps')) {
      createProgressSteps();
    }

    // Inject navigation and submit buttons
    injectNavButtons();
  }

  // ============================================================
  //  DYNAMIC DOM CREATION
  // ============================================================

  function createProgressSteps() {
    const wrapper = document.querySelector('.progress-bar-wrapper');
    if (!wrapper) return;

    const stepsContainer = document.createElement('div');
    stepsContainer.className = 'progress-steps';
    stepsContainer.style.cssText =
      'display:flex;justify-content:space-between;margin-top:8px;';

    for (let i = 1; i <= state.totalSteps; i++) {
      const step = document.createElement('span');
      step.className = 'progress-step' + (i === 1 ? ' active' : '');
      step.dataset.step = i;
      step.textContent = i === 1 ? '\u2713' : i; // first shows check initially
      step.style.cssText =
        'width:28px;height:28px;border-radius:50%;display:flex;align-items:center;' +
        'justify-content:center;font-size:13px;font-weight:700;color:#999;background:#e0e0e0;' +
        'transition:all .3s ease;';

      // first step already active — show pulse
      if (i === 1) {
        applyActiveStepStyle(step);
      }

      stepsContainer.appendChild(step);
    }

    wrapper.appendChild(stepsContainer);
    dom.steps = stepsContainer.querySelectorAll('.progress-step');
  }

  function applyActiveStepStyle(el) {
    el.style.color = '#fff';
    el.style.background = '#f5a623';
    el.style.boxShadow = '0 0 0 4px rgba(245,166,35,0.3)';
    el.style.animation = 'pulse-step 1.5s ease-in-out infinite';
  }

  function applyCompletedStepStyle(el) {
    el.style.color = '#fff';
    el.style.background = '#d4a017';
    el.style.boxShadow = 'none';
    el.style.animation = 'none';
  }

  function applyIncompleteStepStyle(el) {
    el.style.color = '#999';
    el.style.background = '#e0e0e0';
    el.style.boxShadow = 'none';
    el.style.animation = 'none';
  }

  function injectNavButtons() {
    dom.cards.forEach(function (card) {
      var qIdx = parseInt(card.dataset.q, 10);

      // Remove existing injected nav if any (idempotent)
      var existing = card.querySelector('.nav-btn-wrapper');
      if (existing) existing.remove();

      var wrapper = document.createElement('div');
      wrapper.className = 'nav-btn-wrapper';
      wrapper.style.cssText =
        'display:flex;justify-content:space-between;align-items:center;' +
        'margin-top:24px;gap:12px;';

      // Prev button (hidden on step 1)
      if (qIdx > 1) {
        var prevBtn = document.createElement('button');
        prevBtn.className = 'nav-btn prev-btn q-btn';
        prevBtn.type = 'button';
        prevBtn.textContent = '\u2190 Back';
        prevBtn.style.cssText =
          'padding:10px 20px;border:2px solid #ccc;border-radius:8px;' +
          'background:transparent;color:#666;font-size:15px;font-weight:600;' +
          'cursor:pointer;transition:all .2s;';
        prevBtn.addEventListener('mouseenter', function () {
          prevBtn.style.borderColor = '#f5a623';
          prevBtn.style.color = '#f5a623';
        });
        prevBtn.addEventListener('mouseleave', function () {
          prevBtn.style.borderColor = '#ccc';
          prevBtn.style.color = '#666';
        });
        prevBtn.addEventListener('click', goPrev);
        wrapper.appendChild(prevBtn);
      } else {
        // Spacer to keep next btn on the right
        var spacer = document.createElement('div');
        wrapper.appendChild(spacer);
      }

      // Next/Submit button
      if (qIdx < state.totalSteps) {
        var nextBtn = document.createElement('button');
        nextBtn.className = 'nav-btn next-btn q-btn';
        nextBtn.type = 'button';
        nextBtn.textContent = 'Next \u2192';
        nextBtn.style.cssText =
          'padding:10px 24px;border:none;border-radius:8px;' +
          'background:#f5a623;color:#fff;font-size:15px;font-weight:700;' +
          'cursor:pointer;transition:all .2s;margin-left:auto;';
        nextBtn.addEventListener('mouseenter', function () {
          nextBtn.style.background = '#e09515';
        });
        nextBtn.addEventListener('mouseleave', function () {
          nextBtn.style.background = '#f5a623';
        });
        nextBtn.addEventListener('click', goNext);
        wrapper.appendChild(nextBtn);
      } else {
        // Step 6: Submit button
        var submitBtn = document.createElement('button');
        submitBtn.className = 'nav-btn submit-btn q-btn';
        submitBtn.type = 'button';
        submitBtn.textContent = 'Find My Method';
        submitBtn.style.cssText =
          'padding:12px 28px;border:none;border-radius:8px;' +
          'background:linear-gradient(135deg,#f5a623,#d4890f);color:#fff;' +
          'font-size:16px;font-weight:700;cursor:pointer;transition:all .2s;' +
          'margin-left:auto;box-shadow:0 4px 12px rgba(245,166,35,0.4);';
        submitBtn.addEventListener('mouseenter', function () {
          submitBtn.style.background = 'linear-gradient(135deg,#e09515,#c07a0c)';
          submitBtn.style.boxShadow = '0 6px 16px rgba(245,166,35,0.5)';
        });
        submitBtn.addEventListener('mouseleave', function () {
          submitBtn.style.background = 'linear-gradient(135deg,#f5a623,#d4890f)';
          submitBtn.style.boxShadow = '0 4px 12px rgba(245,166,35,0.4)';
        });
        submitBtn.addEventListener('click', handleSubmit);
        wrapper.appendChild(submitBtn);
      }

      card.appendChild(wrapper);
    });
  }

  // ============================================================
  //  PROGRESS BAR & STEPS
  // ============================================================

  function updateProgress() {
    var pct = (state.currentStep / state.totalSteps) * 100;
    if (dom.progressFill) {
      dom.progressFill.style.width = pct + '%';
    }
    if (dom.progressLabel) {
      dom.progressLabel.textContent = 'Step ' + state.currentStep + ' / ' + state.totalSteps;
    }

    // Update step indicators
    if (dom.steps) {
      dom.steps.forEach(function (el) {
        var s = parseInt(el.dataset.step, 10);
        el.classList.remove('active', 'completed');

        if (s < state.currentStep) {
          el.classList.add('completed');
          el.textContent = '\u2713';
          applyCompletedStepStyle(el);
        } else if (s === state.currentStep) {
          el.classList.add('active');
          el.textContent = '\u2713';
          applyActiveStepStyle(el);
        } else {
          el.textContent = s;
          applyIncompleteStepStyle(el);
        }
      });
    }

    // Update question number text
    var activeCard = document.querySelector('.question-card.active');
    if (activeCard) {
      var qNum = activeCard.querySelector('.q-number');
      if (qNum) {
        qNum.textContent = 'Question ' + state.currentStep + ' / ' + state.totalSteps;
      }
    }
  }

  // ============================================================
  //  STEP NAVIGATION
  // ============================================================

  function goToStep(n) {
    try {
      if (n < 1 || n > state.totalSteps) return;
      state.currentStep = n;

      // Show/hide cards
      dom.cards.forEach(function (card) {
        var q = parseInt(card.dataset.q, 10);
        var isActive = q === n;
        card.classList.toggle('active', isActive);
        card.style.display = isActive ? '' : 'none';
      });

      updateProgress();
    } catch (e) {
      console.error('goToStep error:', e);
    }
  }

  function goNext() {
    try {
      var idx = state.currentStep - 1;
      var key = answerKeyMap[idx];
      if (!state.answers[key]) {
        flashError('Please select an option first');
        return;
      }
      if (state.currentStep < state.totalSteps) {
        goToStep(state.currentStep + 1);
      }
    } catch (e) {
      console.error('goNext error:', e);
    }
  }

  function goPrev() {
    try {
      if (state.currentStep > 1) {
        goToStep(state.currentStep - 1);
      }
    } catch (e) {
      console.error('goPrev error:', e);
    }
  }

  // ============================================================
  //  OPTION SELECTION
  // ============================================================

  function handleOptionClick(e) {
    try {
      var btn = e.currentTarget;
      var card = btn.closest('.question-card');
      if (!card) return;

      // Deselect siblings within the same question card
      card.querySelectorAll('.q-btn').forEach(function (sibling) {
        sibling.classList.remove('selected');
        sibling.style.background = '';
        sibling.style.color = '';
        sibling.style.borderColor = '';
        sibling.style.boxShadow = '';
      });

      // Select this button
      btn.classList.add('selected');
      btn.style.background = '#f5a623';
      btn.style.color = '#fff';
      btn.style.borderColor = '#f5a623';
      btn.style.boxShadow = '0 2px 8px rgba(245,166,35,0.4)';

      // Save answer
      var qIdx = parseInt(card.dataset.q, 10) - 1; // 0-based
      var rawValue = btn.dataset.value;
      var key = answerKeyMap[qIdx];
      state.answers[key] = normalizeValue(qIdx, rawValue);
    } catch (e) {
      console.error('handleOptionClick error:', e);
    }
  }

  // ============================================================
  //  ERROR FLASH
  // ============================================================

  function flashError(msg) {
    try {
      var activeCard = document.querySelector('.question-card.active');
      if (!activeCard) return;

      // Remove existing error
      var oldErr = activeCard.querySelector('.flow-error');
      if (oldErr) oldErr.remove();

      var errEl = document.createElement('p');
      errEl.className = 'flow-error';
      errEl.textContent = msg;
      errEl.style.cssText =
        'color:#e74c3c;font-size:14px;font-weight:600;margin:8px 0 0;' +
        'animation:errorFlash 0.5s ease-in-out 3;';

      // Insert after q-text or q-options
      var target = activeCard.querySelector('.q-options');
      if (target) {
        target.parentNode.insertBefore(errEl, target.nextSibling);
      } else {
        activeCard.appendChild(errEl);
      }

      // Auto-remove after 2s
      setTimeout(function () {
        if (errEl.parentNode) errEl.remove();
      }, 2000);
    } catch (e) {
      console.error('flashError error:', e);
    }
  }

  // ============================================================
  //  KEYFRAME INJECTION (for errorFlash & step pulse)
  // ============================================================

  function injectKeyframes() {
    if (document.getElementById('pf-keyframes')) return;

    var style = document.createElement('style');
    style.id = 'pf-keyframes';
    style.textContent =
      '@keyframes errorFlash {' +
      '0%,100%{opacity:1}' +
      '50%{opacity:0.2}' +
      '}' +
      '@keyframes pulse-step {' +
      '0%,100%{box-shadow:0 0 0 4px rgba(245,166,35,0.3)}' +
      '50%{box-shadow:0 0 0 8px rgba(245,166,35,0.15)}' +
      '}';
    document.head.appendChild(style);
  }

  // ============================================================
  //  SUBMIT
  // ============================================================

  function handleSubmit() {
    try {
      // Validate all answers
      var missing = [];
      answerKeyMap.forEach(function (key, idx) {
        if (!state.answers[key]) {
          missing.push('Question ' + (idx + 1));
        }
      });

      if (missing.length > 0) {
        flashError('Please answer all questions before submitting');
        // Navigate to first missing question
        var firstMissingIdx = answerKeyMap.findIndex(function (k) {
          return !state.answers[k];
        });
        goToStep(firstMissingIdx + 1);
        return;
      }

      // Show loading animation
      showLoading(function () {
        // Call engine to find methods
        if (typeof window.findBestMethods === 'function') {
          window.findBestMethods(state.answers);
        } else {
          console.warn('window.findBestMethods not found — engine.js may not be loaded yet');
          showResultsFallback();
        }
      });
    } catch (e) {
      console.error('handleSubmit error:', e);
    }
  }

  // ============================================================
  //  LOADING ANIMATION (1.5s)
  // ============================================================

  function showLoading(callback) {
    try {
      var messages = [
        'Analyzing your profile...',
        'Crunching numbers...',
        'Finding your perfect methods...'
      ];
      var msgIdx = 0;

      // Hide questions flow
      dom.questionsFlow.style.display = 'none';

      // Create loading overlay
      var overlay = document.createElement('div');
      overlay.id = 'pf-loading-overlay';
      overlay.style.cssText =
        'display:flex;flex-direction:column;align-items:center;justify-content:center;' +
        'padding:60px 20px;text-align:center;';

      var spinner = document.createElement('div');
      spinner.style.cssText =
        'width:48px;height:48px;border:4px solid #e0e0e0;border-top-color:#f5a623;' +
        'border-radius:50%;animation:pf-spin 0.8s linear infinite;margin-bottom:20px;';
      overlay.appendChild(spinner);

      var msgEl = document.createElement('p');
      msgEl.id = 'pf-loading-msg';
      msgEl.textContent = messages[0];
      msgEl.style.cssText =
        'font-size:18px;color:#333;font-weight:600;transition:opacity .3s;';
      overlay.appendChild(msgEl);

      // Inject spinner keyframe
      if (!document.getElementById('pf-spin-keyframe')) {
        var spinStyle = document.createElement('style');
        spinStyle.id = 'pf-spin-keyframe';
        spinStyle.textContent =
          '@keyframes pf-spin { to { transform: rotate(360deg); } }';
        document.head.appendChild(spinStyle);
      }

      dom.questionsFlow.parentNode.insertBefore(overlay, dom.questionsFlow.nextSibling);

      // Rotate messages every 500ms
      var msgInterval = setInterval(function () {
        msgIdx = (msgIdx + 1) % messages.length;
        msgEl.textContent = messages[msgIdx];
        msgEl.style.opacity = '0';
        setTimeout(function () {
          msgEl.style.opacity = '1';
        }, 50);
      }, 500);

      // After 1.5s, clean up and callback
      setTimeout(function () {
        clearInterval(msgInterval);
        var ov = document.getElementById('pf-loading-overlay');
        if (ov) ov.remove();
        if (callback) callback();
      }, 1500);
    } catch (e) {
      console.error('showLoading error:', e);
      if (callback) callback();
    }
  }

  // ============================================================
  //  FALLBACK RESULTS DISPLAY (if engine.js not present)
  // ============================================================

  function showResultsFallback() {
    try {
      dom.resultsArea.style.display = 'block';
      dom.resultsList.innerHTML =
        '<div style="text-align:center;padding:30px;color:#999;">' +
        'Engine not ready. Please ensure engine.js is loaded.</div>';
    } catch (e) {
      console.error('showResultsFallback error:', e);
    }
  }

  // ============================================================
  //  TRY AGAIN (reset)
  // ============================================================

  function resetFlow() {
    try {
      // Clear answers
      answerKeyMap.forEach(function (key) {
        state.answers[key] = null;
      });

      // Clear selected styles on all q-btns
      document.querySelectorAll('.q-btn.selected').forEach(function (btn) {
        btn.classList.remove('selected');
        btn.style.background = '';
        btn.style.color = '';
        btn.style.borderColor = '';
        btn.style.boxShadow = '';
      });

      // Remove loading overlay if present
      var ov = document.getElementById('pf-loading-overlay');
      if (ov) ov.remove();

      // Hide results, show questions
      dom.resultsArea.style.display = 'none';
      dom.questionsFlow.style.display = '';

      // Go to step 1
      goToStep(1);
    } catch (e) {
      console.error('resetFlow error:', e);
    }
  }

  // ============================================================
  //  BIND "TRY AGAIN" BUTTON (listens for click on #resultsArea)
  // ============================================================

  function bindTryAgain() {
    // Delegate click to any element with data-action="try-again"
    document.addEventListener('click', function (e) {
      var target = e.target.closest('[data-action="try-again"]');
      if (target) {
        resetFlow();
      }
    });
  }

  // ============================================================
  //  INIT
  // ============================================================

  function init() {
    try {
      injectKeyframes();
      cacheDom();
      bindTryAgain();

      // Start at step 1
      goToStep(1);

      // Bind option button clicks (use event delegation)
      document.addEventListener('click', function (e) {
        var btn = e.target.closest('.question-card .q-btn:not(.nav-btn)');
        if (btn) {
          handleOptionClick({ currentTarget: btn });
        }
      });

      // Expose reset for external use
      window.resetProfitFlow = resetFlow;

      console.log('[ProfitFlow] initialized');
    } catch (e) {
      console.error('[ProfitFlow] init error:', e);
    }
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
