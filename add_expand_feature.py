#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为index.html中的week-card添加展开列表功能"""

import re

filepath = r"C:\Users\Lenovo\osrs-guide-site\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 正则：匹配每个week-card的内容
# 找到 <div class="week-card" id="week-N"> ... </div>（直到下一个week-card或week-path-grid结束）
# 策略：逐张卡片处理，找到每个card的week-guide-list，然后修改其中的li

# 先找到所有week-card的ID
card_ids = re.findall(r'<div class="week-card" id="(week-\d+)"', content)
print(f"找到 {len(card_ids)} 张卡片: {card_ids}")

for card_id in card_ids:
    # 找到这张卡片的开始位置
    card_start = content.find(f'id="{card_id}"')
    if card_start == -1:
        continue
    
    # 找到这张卡片的结束位置（下一个week-card开始，或者week-path-grid结束）
    next_card_start = -1
    for other_id in card_ids:
        if other_id != card_id:
            pos = content.find(f'id="{other_id}"', card_start + 10)
            if pos != -1 and (next_card_start == -1 or pos < next_card_start):
                next_card_start = pos
    
    # 如果这是最后一张卡片，找到week-path-grid的结束
    if next_card_start == -1:
        end_marker = '</div>\n\n  </div>'
        next_card_start = content.find(end_marker, card_start)
        if next_card_start != -1:
            next_card_start = next_card_start + len(end_marker)
    
    if next_card_start == -1:
        print(f"警告: 找不到 {card_id} 的结束位置")
        continue
    
    card_content = content[card_start:next_card_start]
    
    # 统计这张卡片有多少个li
    li_matches = re.findall(r'<li>(?!<li>)', card_content)
    li_count = len(re.findall(r'<li>', card_content))
    print(f"  {card_id}: 找到 {li_count} 个攻略链接")
    
    # 如果超过2个li，为第3个及以后的li添加hidden类
    if li_count > 2:
        # 找到所有li的位置（在card_content中）
        li_positions = []
        pos = 0
        while True:
            li_pos = card_content.find('<li>', pos)
            if li_pos == -1:
                break
            li_positions.append(li_pos)
            pos = li_pos + 4
        
        # 为第3个及以后的li添加hidden类
        new_card_content = card_content
        offset = 0
        for i, li_pos in enumerate(li_positions):
            actual_pos = li_pos + offset
            if i >= 2:  # 第3个及以后（索引从0开始）
                # 在<li>后面添加class="hidden"
                new_card_content = new_card_content[:actual_pos+4] + ' class="hidden"' + new_card_content[actual_pos+4:]
                offset += len(' class="hidden"')
        
        card_content = new_card_content
    
    # 在</ul>后面添加展开按钮
    # 找到最后一个</ul>的位置（在这张卡片内）
    last_ul_end = card_content.rfind('</ul>')
    if last_ul_end != -1:
        # 在</ul>后面添加按钮
        btn_html = f'\n      <button class="week-card-expand-btn" onclick="toggleWeekCard(\'{card_id}\', this)">View all {li_count} guides</button>\n    '
        card_content = card_content[:last_ul_end+6] + btn_html + card_content[last_ul_end+6:]
    
    # 将修改后的card_content替换回原内容
    content = content[:card_start] + card_content + content[next_card_start:]

# 保存修改后的文件
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n完成！所有卡片已添加展开列表功能。")
