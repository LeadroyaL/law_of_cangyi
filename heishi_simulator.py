import random


class Group:
    def __init__(self, strategies: list[str]):
        self.strategies = strategies

    def __len__(self):
        return len(self.strategies)

    def __repr__(self):
        return f'{self.strategies}'

    def __str__(self):
        return f'{self.strategies}'

    def __eq__(self, other):
        return self.strategies == other.strategies


def roll(groups: list[Group], has标记闪光: bool) -> (str, list[Group]):
    total = sum([len(x) for x in groups])
    weights = [len(x) / total for x in groups]
    # 抽1组
    group = random.choices(groups, weights=weights)[0]
    # 移除
    groups.remove(group)
    # 从1组里抽1个
    strategy = random.choice(group.strategies)
    # 如果抽到的是圣光标记，那么3个一阶、1个二阶、0个红
    if strategy == '圣光标记':
        groups.append(Group(['稳定标记', '标记强化', '随机标记']))
        groups.append(Group(['标记共鸣']))
        if Group(["冰刺再生", "无尽冰刺"]) in groups:
            groups.remove(Group(["冰刺再生", "无尽冰刺"]))
        if not has标记闪光:
            groups.append(Group(['标记闪光']))
    # 如果抽到的是其他基础策略，那么加入3个一阶、1个二阶、1个红（红色有出入，平均算1个差不多）
    if strategy in ["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "冲刺毒弹"]:
        groups.append(Group(['冲刺一阶1', '冲刺一阶2', '冲刺一阶3']))
        groups.append(Group(['冲刺二阶']))
        groups.append(Group(['冲刺红']))
    return strategy, groups


def five_roll(groups: list[Group], has标记闪光=True) -> list[str]:
    ret = []
    for i in range(5):
        s, groups = roll(groups, has标记闪光)
        ret.append(s)
    return ret


def case0():
    groups = [
        Group(["连续刃环"]),
        Group(["冰刺再生", "无尽冰刺"]),
        Group(["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "圣光标记", "冲刺毒弹"]),
    ]
    five_s = five_roll(groups, has标记闪光=False)
    if '连续刃环' in five_s:
        if '冰刺再生' in five_s or '无尽冰刺' in five_s:
            if '标记闪光' in five_s:
                return 1
    return 0


def case1():
    groups = [
        Group(["中毒毒弹"]),
        Group(["连续刃环"]),
        Group(["冰刺再生", "无尽冰刺"]),
        Group(["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "圣光标记", "冲刺毒弹"]),
    ]
    five_s = five_roll(groups)
    if "中毒毒弹" in five_s:
        if '连续刃环' in five_s:
            if '冰刺再生' in five_s or '无尽冰刺' in five_s:
                if '冲刺一阶1' not in five_s and '冲刺一阶2' not in five_s and '冲刺一阶3' not in five_s \
                        and '冲刺二阶' not in five_s and '冲刺红' not in five_s:
                    return 1
    return 0


def case2():
    groups = [
        Group(["中毒毒弹"]),
        Group(["连续刃环"]),
        Group(["冰刺再生", "无尽冰刺"]),
        Group(["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "圣光标记", "冲刺毒弹"]),
        Group(["电解化毒"]),
    ]
    five_s = five_roll(groups)
    if "中毒毒弹" in five_s:
        if '连续刃环' in five_s:
            if '冰刺再生' in five_s or '无尽冰刺' in five_s:
                if '冲刺一阶1' not in five_s and '冲刺一阶2' not in five_s and '冲刺一阶3' not in five_s \
                        and '冲刺二阶' not in five_s and '冲刺红' not in five_s:
                    return 1
    return 0


def case3():
    groups = [
        Group(["中毒毒弹"]),
        Group(["连续刃环"]),
        Group(["冰刺再生", "无尽冰刺"]),
        Group(["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "圣光标记", "冲刺毒弹"]),
        Group(["电解化毒"]),
        Group(["多重冰刺"]),
    ]
    five_s = five_roll(groups)
    if "中毒毒弹" in five_s:
        if '连续刃环' in five_s:
            if '冰刺再生' in five_s or '无尽冰刺' in five_s:
                if '冲刺一阶1' not in five_s and '冲刺一阶2' not in five_s and '冲刺一阶3' not in five_s \
                        and '冲刺二阶' not in five_s and '冲刺红' not in five_s:
                    return 1
    return 0


def case4():
    groups = [
        Group(["中毒毒弹"]),
        Group(["连续刃环"]),
        Group(["冰刺再生", "无尽冰刺"]),
        Group(["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "圣光标记", "冲刺毒弹"]),
        Group(["冰刺强化", "冰刺穿透", "精准冰刺"]),
        Group(["多重冰刺"]),
    ]
    five_s = five_roll(groups)
    if "中毒毒弹" in five_s:
        if '连续刃环' in five_s:
            if '冰刺再生' in five_s or '无尽冰刺' in five_s:
                if '冲刺一阶1' not in five_s and '冲刺一阶2' not in five_s and '冲刺一阶3' not in five_s \
                        and '冲刺二阶' not in five_s and '冲刺红' not in five_s:
                    return 1
    return 0


def case5():
    groups = [
        Group(["中毒毒弹"]),
        Group(["连续刃环"]),
        Group(["冰刺再生", "无尽冰刺"]),
        Group(["冲刺飞剑", "冲刺影子", "冲刺落雷", "冲刺燃烧", "冲刺冰锥", "圣光标记", "冲刺毒弹"]),
        Group(["冰刺强化", "冰刺穿透", "精准冰刺"]),
        Group(["电解化毒"]),
        Group(["多重冰刺"]),
    ]
    five_s = five_roll(groups)
    if "中毒毒弹" in five_s:
        if '连续刃环' in five_s:
            if '冰刺再生' in five_s or '无尽冰刺' in five_s:
                if '冲刺一阶1' not in five_s and '冲刺一阶2' not in five_s and '冲刺一阶3' not in five_s \
                        and '冲刺二阶' not in five_s and '冲刺红' not in five_s:
                    return 1
    return 0


if __name__ == '__main__':
    CNT = 1000000
    print(f"基于雷云火弹和中毒毒弹： {sum(case0() for i in range(CNT)) / CNT * 100:.2f}%")
    print(f"基于冲刺三激活 case1： {sum(case1() for i in range(CNT)) / CNT * 100:.2f}%")
    print(f"基于冲刺三激活 case2： {sum(case2() for i in range(CNT)) / CNT * 100:.2f}%")
    print(f"基于冲刺三激活 case3： {sum(case3() for i in range(CNT)) / CNT * 100:.2f}%")
    print(f"基于冲刺三激活 case4： {sum(case4() for i in range(CNT)) / CNT * 100:.2f}%")
    print(f"基于冲刺三激活 case5： {sum(case5() for i in range(CNT)) / CNT * 100:.2f}%")
