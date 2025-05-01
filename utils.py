import re
from collections import Counter
import itertools
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import database
from strategy import Strategy

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def draw_status(title, text_contents, font_size=8, dpi=300):
    # 加载图片
    img = mpimg.imread("img/策略底图.jpg")

    # 创建一个图形和坐标轴，设置 dpi 以提高分辨率
    fig, ax = plt.subplots(dpi=dpi)

    # 显示图片
    ax.imshow(img)

    # 关闭坐标轴
    ax.axis('off')

    text_positions = [
        [(880, 180), (1155, 180), (1430, 180), (1700, 180), ],
        [(880, 415), (1155, 415), (1430, 415), (1700, 415), ],
        [(880, 645), (1155, 645), (1430, 645), (1700, 645), ],
        [(880, 880), (1155, 880), (1430, 880), (1700, 880), ],
        [(880, 1105), (1155, 1105), (1430, 1105), (1700, 1105), ],
    ]

    text_colors = [
        ['red', 'red', 'red', 'red', ],
        ['red', 'red', 'red', 'red', ],
        ['red', 'red', 'red', 'red', ],
        ['red', 'red', 'red', 'red', ],
        ['red', 'red', 'red', 'red', ],
    ]

    ax.text(1050, 50, title,
            horizontalalignment='center', verticalalignment='center',
            color='white', fontsize=font_size, fontweight='bold')

    text_positions = itertools.chain(*text_positions)
    text_colors = itertools.chain(*text_colors)
    text_contents = itertools.chain(*text_contents)
    # 在指定位置插入文本
    for pos, content, color in zip(text_positions, text_contents, text_colors):
        ax.text(pos[0], pos[1], content,
                horizontalalignment='center', verticalalignment='center',
                color='yellow' if '空' in content else 'red', fontsize=font_size)

    # 显示图形
    plt.show()


def parse_file(file_path) -> (list[list[str]], list[list[Strategy]]):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 提取前五行
        first_five = []
        for line in lines[:5]:
            # 使用正则表达式匹配方括号内的内容
            parts = re.findall(r'\[(.*?)]', line)
            first_five.append(parts)

        # 提取后面的行
        remaining = []
        for line in lines[5:]:
            # 去除换行符，按逗号分割
            parts = line.strip().split(',')
            remaining.append(parts)
        # 后N行: 转为object
        remaining = [[database.strategy_dict[i] for i in sub_arr] for sub_arr in remaining]
        return first_five, remaining
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}。")
    except Exception as e:
        print(f"发生未知错误：{e}")


def plot_element_count(data: list[str]):
    # 统计每个元素的出现次数
    counter = Counter(data)

    labels = list(counter.keys())
    values = list(counter.values())

    # 计算平均值
    average = sum(values) / len(values)

    # 创建一个包含两个子图的画布
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # 绘制柱状图
    ax1.bar(labels, values)
    # 添加平均值线
    ax1.axhline(y=average, color='r', linestyle='--', label='平均值')
    # 添加标题和标签
    ax1.set_title('策略出现次数柱状图')
    ax1.set_ylabel('出现次数')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()

    # 绘制饼状图
    ax2.pie(values, labels=labels, autopct='%1.1f%%')
    ax2.set_title('策略出现次数饼状图')

    plt.tight_layout()
    plt.show()


import numpy as np
from scipy.stats import chisquare
from collections import Counter
import matplotlib.pyplot as plt


def test_uniform_distribution(data) -> (float, float):
    """
    此函数用于检验给定的频次数据是否符合均匀分布。
    :param data: 待检验的频次数据列表
    :return: 卡方检验的统计量和 p 值
    """
    # 计算总频次
    total_freq = sum(data)
    # 计算每个类别在均匀分布下的理论频次
    num_categories = len(data)
    expected = total_freq / num_categories * np.ones(num_categories)
    # 进行卡方检验
    chi2_stat, p_value = chisquare(data, expected)
    print(f"卡方统计量: {chi2_stat}, p 值: {p_value}")
    if p_value > 0.05:
        print("数据可能来自均匀分布。")
    else:
        print("数据不太可能来自均匀分布。")
    return chi2_stat, p_value


def test_uniform_distribution(data, probs=None) -> (float, float):
    """
    此函数用于检验给定的频次数据是否符合均匀分布。
    :param data: 待检验的频次数据列表
    :param probs: 每个类别对应的概率列表
    :return: 卡方检验的统计量和 p 值
    """
    # 计算总频次
    total_freq = sum(data)
    # 计算每个类别在均匀分布下的理论频次
    num_categories = len(data)
    if probs is not None:
        if len(probs) != num_categories:
            raise ValueError("probs的长度必须与data的长度相同。")
        if not np.isclose(sum(probs), 1):
            raise ValueError("probs的元素之和必须近似为1。")
        expected = total_freq * np.array(probs)
    else:
        expected = total_freq / num_categories * np.ones(num_categories)
    # 进行卡方检验
    chi2_stat, p_value = chisquare(data, expected)
    print(f"卡方统计量: {chi2_stat}, p 值: {p_value}")
    if p_value > 0.05:
        print("数据可能来自均匀分布或离散型概率分布")
    else:
        print("数据不太可能来自均匀分布或离散型概率分布。")
    return chi2_stat, p_value


def to_groups(strategies: list[Strategy], group_names: list[str]):
    group_cnt = [0] * len(group_names)
    for s in strategies:
        for i, g in enumerate(group_names):
            if s.name in g:
                group_cnt[i] = group_cnt[i] + 1
    return group_cnt


def to_level(strategies: list[Strategy]):
    group_cnt = [0] * 4
    for s in strategies:
        group_cnt[s.level] += 1
    return group_cnt


def analyze_normal(strategies: list[list[Strategy]]):
    # 普通的是没有状态的，直接视为全部随机
    # 输入是：list^2[Strategy]，转list[Strategy]
    strategies = itertools.chain(*strategies)
    names = [x.name for x in strategies]
    # 带有平均数的柱状图
    # 按照LeveL进行统计的饼状图
    # 按照Position进行统计的饼状图
    # 科学计数的卡方、置信度
    pass


def print_probs(group_names, round_num, probs):
    print(f"第{round_num}轮理论概率分布：")
    for name, prob in zip(group_names, probs):
        print(f"Group[{name}]：{prob:.6f}")
    print()
