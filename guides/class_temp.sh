#!/bin/bash

total=$(ls *.html 2>/dev/null | wc -l)
echo "TOTAL: $total"

beginner=0
boss=0
money=0
skill=0
quest=0
pvm=0
other=0

for f in $(ls *.html 2>/dev/null | sort); do
    name=$(basename "$f" .html)
    if echo "$name" | grep -qi "beginner"; then
        beginner=$((beginner+1))
    elif echo "$name" | grep -qiE "boss"; then
        boss=$((boss+1))
    elif echo "$name" | grep -qiE "money|flipping|flip|ge-|gp-|profit|bond|runespan|runesmith|green.dragon|revenant"; then
        money=$((money+1))
    elif echo "$name" | grep -qiE "1-99|training|skill|leveling|99-|mining|fishing|hunter|crafting|prayer|agility|thieving|cooking|runecraft|fletching|woodcutting|herblore|construction|smithing|firemaking|slayer"; then
        skill=$((skill+1))
    elif echo "$name" | grep -qiE "quest"; then
        quest=$((quest+1))
    elif echo "$name" | grep -qiE "pvm|raid|theatre|toa|corrupted|nex|nightmare|cerberus|kalphite|sarachnis|grotesque|hydra|muspah|royal.titans"; then
        pvm=$((pvm+1))
    else
        other=$((other+1))
    fi
done

echo "Beginner: $beginner"
echo "Boss: $boss"
echo "Money: $money"
echo "Skill: $skill"
echo "Quest: $quest"
echo "PvM: $pvm"
echo "Other: $other"

echo "---"
echo "Sum: $((beginner+boss+money+skill+quest+pvm+other))"
