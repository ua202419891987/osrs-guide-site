#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix index.html Weekly Updates card
"""

import re

filepath = r"C:\Users\Lenovo\osrs-guide-site\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace
new_lines = []
for line in lines:
    # Replace preview text line 367-368
    if '🦌 1-99 Hunter Guide' in line:
        line = line.replace('🦌 1-99 Hunter Guide', '🦌 Hunter P1 Upgraded')
    if '🎯 Complete Training Roadmap' in line:
        line = line.replace('🎯 Complete Training Roadmap', '🎯 Ironman Cape Analysis')
    # Replace count line 370
    if '9 New This Week' in line:
        line = line.replace('9 New This Week', '11 New This Week')
    new_lines.append(line)

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done! Index.html Weekly Updates card updated.")
print("Changes:")
print("  1. Preview: 1-99 Hunter Guide -> Hunter P1 Upgraded")
print("  2. Preview: Complete Training Roadmap -> Ironman Cape Analysis")
print("  3. Count: 9 New This Week -> 11 New This Week")
