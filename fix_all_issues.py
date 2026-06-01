import os
import re

# 要修正的10篇文件
files = [
    "osrs-ironman-money-making-f2p-2026.html",
    "osrs-low-effort-money-making-for-beginners.html",
    "osrs-how-to-make-gold-with-fishing-2026.html",
    "osrs-f2p-money-making-no-stats-required.html",
    "osrs-passive-money-making-while-offline.html",
    "osrs-cheap-flipping-methods-for-new-players.html",
    "osrs-hunter-money-making-guide-2026.html",
    "osrs-how-to-make-money-with-crafting-low-level.html",
    "osrs-wintertodt-money-making-per-hour.html",
    "osrs-chambers-of-xeric-loot-profit-guide.html"
]

# 真实域名
real_domain = "https://osrsguide.com"

for filename in files:
    filepath = f"/c/Users/Lenovo/osrs-guide-site/guides/{filename}"
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 问题1：修正nav链接路径（如果包含错误的路径）
    # 查找错误的路径（没有/guides/前缀的分类页链接）
    wrong_patterns = [
        ('href="../money-making.html"', 'href="../guides/money-making.html"'),
        ('href="../skill-training.html"', 'href="../guides/skill-training.html"'),
        ('href="../quest-guide.html"', 'href="../guides/quest-guide.html"'),
        ('href="../boss-killing.html"', 'href="../guides/boss-killing.html"')
    ]
    
    for wrong, correct in wrong_patterns:
        content = content.replace(wrong, correct)
    
    # 问题2：修正canonical链接
    content = re.sub(
        r'href="https://yourdomain\.com/guides/',
        f'href="{real_domain}/guides/',
        content
    )
    
    # 问题3：修正拼写错误
    content = content.replace("does't", "doesn't")
    content = content.replace("you're", "you're")  # 检查，如果有错误也修正
    content = content.replace("You're", "You're")
    
    # 问题4：为nav链接添加active类（如果缺失）
    # 根据文件名判断应该高亮哪个分类
    if 'money-making' in filename:
        # 确保money-making链接有active类
        content = re.sub(
            r'<li><a href="\.\./guides/money-making\.html">Money Making</a></li>',
            '<li><a href="../guides/money-making.html" class="active">Money Making</a></li>',
            content
        )
    
    # 保存文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已修正: {filename}")
    else:
        print(f"⚠️  无需修正: {filename}")

print("\n🎉 所有文件修正完成！")
