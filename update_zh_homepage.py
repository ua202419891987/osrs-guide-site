import re

with open('zh/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The new 8-week roadmap section in Chinese
new_section = '''      <!-- ========== 新手系列：8周路线图 ========== -->
  <div class="container">
  <div class="section-header" style="background:#fff;padding:20px 24px;border-radius:var(--radius-lg);border:1px solid var(--border-bronze);display:flex;align-items:center;gap:12px;flex-wrap:wrap">
    <div class="section-title" id="stage-0" style="margin:0">🗺️ 阶段 0：8周新手路线图 — 从这里开始！</div>
    <span class="new-week-badge">📝 本周更新</span>
    <a href="../guides/osrs-new-player-guide-2026.html" class="see-all" style="margin-left:auto">📚 查看全部新手攻略 →</a>
  </div>

  <!-- 8周路线图网格 -->
  <div class="week-path-grid" style="margin-top:16px;">

    <!-- 第1周：入门步骤 -->
    <div class="week-card" id="week-1">
      <div class="week-card-header">
        <span class="week-number">第 1 周</span>
        <span class="week-goal">🎯 目标：掌握基础</span>
      </div>
      <h3 class="week-card-title">🎮 入门步骤</h3>
      <p class="week-card-desc">掌握操作、导航和核心游戏机制。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-new-player-guide-2026.html">新手完整指南（总览）</a> <span class="wk-badge wk-badge-starting">🌟 起点</span></li>
        <li><a href="../guides/osrs-interface-controls-beginner-guide-2026.html">游戏界面与操作指南</a></li>
        <li class="hidden"><a href="../guides/osrs-bank-inventory-management-2026.html">银行与背包管理</a></li>
        <li class="hidden"><a href="../guides/osrs-maps-travel-guide-2026.html">地图与快速旅行指南</a></li>
        <li class="hidden"><a href="../guides/osrs-combat-triangle-explained-2026.html">战斗三角详解</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-1', this)">查看全部 5 篇攻略</button>
    </div>

    <!-- 第2周：打造角色 -->
    <div class="week-card" id="week-2">
      <div class="week-card-header">
        <span class="week-number">第 2 周</span>
        <span class="week-goal">🎯 目标：战斗就绪</span>
      </div>
      <h3 class="week-card-title">⚔️ 打造角色</h3>
      <p class="week-card-desc">技能、战斗训练、装备 — 打造坚实基础。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-all-skills-overview-guide-2026.html">全部技能总览指南</a></li>
        <li><a href="../guides/osrs-combat-training-beginner-2026.html">战斗训练指南（1–70+）</a></li>
        <li class="hidden"><a href="../guides/osrs-gear-beginner-guide-2026.html">新手装备指南</a></li>
        <li class="hidden"><a href="../guides/osrs-safe-spots-beginner-2026.html">安全点指南</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-2', this)">查看全部 4 篇攻略</button>
    </div>

    <!-- 第3周：赚取金币 -->
    <div class="week-card" id="week-3">
      <div class="week-card-header">
        <span class="week-number">第 3 周</span>
        <span class="week-goal">🎯 目标：赚取首百万金币</span>
      </div>
      <h3 class="week-card-title">💰 赚取金币</h3>
      <p class="week-card-desc">从零到百万富翁 — 赚钱基础。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-money-making-beginner-2026.html">新手赚钱方法（F2P→会员）</a></li>
        <li><a href="../guides/osrs-grand-exchange-guide-2026.html">大交易所完整指南</a></li>
        <li class="hidden"><a href="../guides/osrs-low-level-skilling-money-makers-2026.html">低等级生活技能赚钱法</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-3', this)">查看全部 3 篇攻略</button>
    </div>

    <!-- 第4周：解锁会员 -->
    <div class="week-card" id="week-4">
      <div class="week-card-header">
        <span class="week-number">第 4 周</span>
        <span class="week-goal">🎯 目标：解锁会员内容</span>
      </div>
      <h3 class="week-card-title">💎 解锁会员</h3>
      <p class="week-card-desc">获取会员、训练祷告、正式开始做任务。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-f2p-to-p2p-membership-guide-2026.html">F2P 转 P2P 会员指南</a></li>
        <li><a href="../guides/osrs-prayer-training-beginner-guide-2026.html">祷告训练指南</a></li>
        <li class="hidden"><a href="../guides/osrs-questing-beginner-guide-2026.html">新手任务攻略</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-4', this)">查看全部 3 篇攻略</button>
    </div>

    <!-- 第5周：加入社区 -->
    <div class="week-card" id="week-5">
      <div class="week-card-header">
        <span class="week-number">第 5 周</span>
        <span class="week-goal">🎯 目标：找到你的部落</span>
      </div>
      <h3 class="week-card-title">🏰 加入社区</h3>
      <p class="week-card-desc">公会、玩家房屋、小游戏 — OSRS 一起玩更有趣。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-clan-social-guide-2026.html">公会与社交指南</a></li>
        <li><a href="../guides/osrs-poh-beginner-guide-2026.html">玩家房屋（POH）指南</a></li>
        <li class="hidden"><a href="../guides/osrs-minigames-beginner-guide-2026.html">小游戏新手指南</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-5', this)">查看全部 3 篇攻略</button>
    </div>

    <!-- 第6周：开始打Boss -->
    <div class="week-card" id="week-6">
      <div class="week-card-header">
        <span class="week-number">第 6 周</span>
        <span class="week-goal">🎯 目标：击杀你的第一个 Boss</span>
      </div>
      <h3 class="week-card-title">🐉 开始打Boss</h3>
      <p class="week-card-desc">PvM 第一步 — Barrows、NMZ 及更多。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-barrows-beginner-guide-2026.html">Barrows 兄弟新手指南</a></li>
        <li><a href="../guides/osrs-nmz-beginner-guide-2026.html">噩梦地带（NMZ）指南</a></li>
        <li class="hidden"><a href="../guides/osrs-pvm-beginner-guide-2026.html">PvM 新手指南</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-6', this)">查看全部 3 篇攻略</button>
    </div>

    <!-- 第7周：养成好习惯 -->
    <div class="week-card" id="week-7">
      <div class="week-card-header">
        <span class="week-number">第 7 周</span>
        <span class="week-goal">🎯 目标：更聪明地游玩</span>
      </div>
      <h3 class="week-card-title">📅 养成好习惯</h3>
      <p class="week-card-desc">日常路线、需要避免的常见错误、成就日记。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-daily-weekly-reset-activities-guide-2026.html">每日/每周重置活动指南</a></li>
        <li><a href="../guides/osrs-common-beginner-mistakes-avoid-2026.html">20个新手常见错误</a></li>
        <li class="hidden"><a href="../guides/osrs-achievement-diary-beginner-guide-2026.html">成就日记指南</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-7', this)">查看全部 3 篇攻略</button>
    </div>

    <!-- 第8周：全面提升 -->
    <div class="week-card" id="week-8">
      <div class="week-card-header">
        <span class="week-number">第 8 周</span>
        <span class="week-goal">🎯 目标：从新手毕业</span>
      </div>
      <h3 class="week-card-title">🚀 全面提升</h3>
      <p class="week-card-desc">手机版、回归玩家、账号类型 — 进阶新手话题。</p>
      <ul class="week-guide-list">
        <li><a href="../guides/osrs-mobile-guide-2026.html">OSRS 手机版指南</a></li>
        <li><a href="../guides/osrs-returning-player-guide-2026.html">回归玩家追赶指南</a></li>
        <li class="hidden"><a href="../guides/osrs-ironman-beginner-guide-2026.html">铁人模式新手指南</a></li>
        <li class="hidden"><a href="../guides/osrs-slayer-beginner-guide-2026.html">Slayer 新手指南</a></li>
      </ul>
      <button class="week-card-expand-btn" onclick="toggleWeekCard('week-8', this)">查看全部 4 篇攻略</button>
    </div>

  </div>
  </div>

      <!-- MONEY MAKING -->'''

# Replace the old section
old_pattern = r'      <!-- STAGE 0.*?<!-- MONEY MAKING -->'
new_content = re.sub(old_pattern, new_section, content, flags=re.DOTALL)

if new_content == content:
    print('ERROR: Replacement failed - pattern did not match')
    # Debug: check if STAGE 0 exists
    if 'STAGE 0' in content:
        print('STAGE 0 found, but pattern did not match')
        # Try to find the exact text around STAGE 0
        idx = content.find('STAGE 0')
        if idx >= 0:
            print('Context around STAGE 0:')
            print(repr(content[idx:idx+200]))
else:
    with open('zh/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('✅ Successfully updated Chinese homepage with 8-week roadmap!')
    print(f'Characters replaced: {len(content) - len(new_content)}')
