import itertools

from strategy import *

# 数据来自 https://github.com/baiyuan1786/StrategyCalculator/tree/e3f24dad0d3e409211b3b34e2917255a1b0ec00f

_strategy_record = [
    飞剑(), 撕裂(), 刃环(), 刀刃风暴(),
    触手(), 影子(), 影刺(), 黑洞(),
    感电(), 闪电链(), 落雷(), 电球(),
    燃烧(), 火弹(), 火环(), 地雷(), 火精灵(),
    寒冷(), 冰锥(), 冰刺(),
    光枪(), 闪光(), 光波(), 光阵(), 圣光标记(),
    中毒(), 史莱姆(), 毒弹(), 毒液(), ]

strategy_list: list[Strategy] = list(itertools.chain(*[x.strategys for x in _strategy_record]))
strategy_dict: dict[str, Strategy] = {s.name: s for s in strategy_list}
