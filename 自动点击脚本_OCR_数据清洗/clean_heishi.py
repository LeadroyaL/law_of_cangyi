import re
from collections import Counter

import symspellpy.symspellpy as symspell

import database


# 技能*电容易被翻译错误。。。

def uniq_like_linux(input_file, output_file):
    """实现类似 Linux uniq 的去重功能"""
    previous_line = None
    previous_ms = 0
    with open(input_file, 'r', encoding='utf-8') as fin, \
            open(output_file, 'w', encoding='utf-8') as fout:

        for line in fin:
            if line.startswith("Handle"):
                fout.write(line)  # 保留原始格式
                continue
            # 解析每行的列表结构
            current_line = line.strip()

            # 只写入与上一行不同的内容
            ms = int(re.search(r'\d+', line)[0])
            rec = line.strip().split(',')[1]
            current_line = rec
            if current_line != previous_line:
                fout.write(line)  # 保留原始格式
                previous_line = current_line
                previous_ms = ms
            if current_line == previous_line and ms - previous_ms > 10:
                fout.write(line)  # 保留原始格式
                previous_line = current_line
                previous_ms = ms


# 初始化 SymSpell 对象
sym_spell = symspell.SymSpell(1, prefix_length=7)

# 把正确的词添加到字典中
for word in database.strategy_dict:
    sym_spell.create_dictionary_entry(word, 1)


def correct_spellings(misspelled, max_edit_distance=1):
    """
    对给定的待纠正字符串列表进行纠错

    :param misspelled_words: 待纠正的字符串列表
    :param correct_words: 可能的正确字符串列表
    :param max_edit_distance_dictionary: 字典中允许的最大编辑距离
    :param prefix_length: 前缀长度
    :param max_edit_distance: 查找时允许的最大编辑距离
    :return: 包含纠错结果的列表
    """

    suggestions = sym_spell.lookup(misspelled, symspell.Verbosity.CLOSEST, max_edit_distance=max_edit_distance)
    if suggestions:
        best_match = suggestions[0].term
        return (best_match)
    else:
        return (misspelled)


# ----------------- 使用示例 -----------------
if __name__ == "__main__":
    data = []

    with open('run_heishi_.log', encoding='utf8') as file, \
            open('step2.log', 'w', encoding='utf-8') as fout:
        for line in file:
            if "Handle" in line:
                print(line)
                fout.write(line)
                continue
            line = line.strip()
            if '获得' not in line:
                continue
            ms = int(re.search(r'\d+', line)[0])
            rec = line[line.find('获得') + 2:]
            if rec.startswith("传承技火") or rec.startswith("技能毒") or rec.startswith("技能") and rec.endswith("电"):
                pass
            elif rec in database.strategy_dict:
                pass
            elif len(rec) >= 4:
                rec = correct_spellings(rec)
            if rec in database.strategy_dict:
                fout.write(str(ms))
                fout.write(',')
                fout.write(rec)
                fout.write('\n')
            else:
                print(line)

    # 使用示例
    uniq_like_linux('step2.log', 'step3.log')
    with open('step3.log', encoding='utf8') as file:
        cnt = 0
        arr = []
        for line in file:
            line = line.strip()
            if line.startswith('H') or line.startswith("{"):
                print(line)
                print(arr)
                cnt = 0
                arr = []
                continue
            arr.append(line)
            cnt += 1
            if cnt == 5:
                print(','.join([x.split(',')[1] for x in arr]))
                cnt = 0
                arr = []
