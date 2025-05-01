from collections import Counter

import database


def uniq_like_linux(input_file, output_file):
    """实现类似 Linux uniq 的去重功能"""
    previous_line = None
    with open(input_file, 'r', encoding='utf-8') as fin, \
            open(output_file, 'w', encoding='utf-8') as fout:

        for line in fin:
            # 解析每行的列表结构
            current_line = line.strip()

            # 只写入与上一行不同的内容
            if current_line != previous_line:
                fout.write(line)  # 保留原始格式
                previous_line = current_line


# ----------------- 使用示例 -----------------
if __name__ == "__main__":
    data = []

    with open('data/商店夹杂数据1.txt', encoding='utf8') as file, \
        open('data/商店夹杂数据2.txt', 'w', encoding='utf-8') as fout:
        for line in file:
            line = line.strip()
            if '[' in line:
                line = line[line.find('[') + 1: line.find(']')]
            data.append(line.split(','))
            if any(x for x in line.split(',') if x not in database.strategy_dict):
                continue
            fout.write(line)
            fout.write('\n')

    # 使用示例
    uniq_like_linux('data/商店夹杂数据2.txt', 'data/商店房/商店_1个一阶1个二阶.txt')
