import utils


def fast_five(file, group_names, weights):
    current_strategies, strategies = utils.parse_file(file)
    utils.draw_status("夹杂着带，进入黑市", current_strategies)
    total = sum(weights)
    # 第1轮概率计算
    round_probs = [w / sum(weights) for w in weights]
    # 第1轮分组化的统计频次
    round1_cnt = utils.to_groups([x[0] for x in strategies], group_names)
    utils.test_uniform_distribution(round1_cnt, round_probs)
    round_probs = [0.0] * len(weights)
    for i in range(len(weights)):
        remaining_after_first = total - weights[i]
        for j in range(len(weights)):
            if i == j:
                continue
            prob = (weights[i] / total) * (weights[j] / remaining_after_first)
            round_probs[j] += prob
    # 第2轮分组化的统计频次
    round_cnt = utils.to_groups([x[1] for x in strategies], group_names)
    utils.test_uniform_distribution(round_cnt, round_probs)
    round_probs = [0.0] * len(weights)
    for i in range(len(weights)):
        remaining_after_first = total - weights[i]
        for j in range(len(weights)):
            if i == j:
                continue
            remaining_after_second = remaining_after_first - weights[j]
            for k in range(len(weights)):
                if k == i or k == j:
                    continue
                prob = (weights[i] / total) * (weights[j] / remaining_after_first) * (
                        weights[k] / remaining_after_second)
                round_probs[k] += prob
    # 第3轮分组化的统计频次
    round_cnt = utils.to_groups([x[2] for x in strategies], group_names)
    utils.test_uniform_distribution(round_cnt, round_probs)
    # 第4轮概率计算
    round_probs = [0.0] * len(weights)
    for i in range(len(weights)):
        remaining_after_first = total - weights[i]
        for j in range(len(weights)):
            if i == j:
                continue
            remaining_after_second = remaining_after_first - weights[j]
            for k in range(len(weights)):
                if k == i or k == j:
                    continue
                remaining_after_third = remaining_after_second - weights[k]
                for l in range(len(weights)):
                    if l == i or l == j or l == k:
                        continue
                    prob = (weights[i] / total) * (weights[j] / remaining_after_first) * (
                            weights[k] / remaining_after_second) * (weights[l] / remaining_after_third)
                    round_probs[l] += prob
    # 第4轮分组化的统计频次
    round_cnt = utils.to_groups([x[3] for x in strategies], group_names)
    utils.test_uniform_distribution(round_cnt, round_probs)
    # 第5轮概率计算
    round_probs = [0.0] * len(weights)
    for i in range(len(weights)):
        remaining_after_first = total - weights[i]
        for j in range(len(weights)):
            if i == j:
                continue
            remaining_after_second = remaining_after_first - weights[j]
            for k in range(len(weights)):
                if k == i or k == j:
                    continue
                remaining_after_third = remaining_after_second - weights[k]
                for l in range(len(weights)):
                    if l == i or l == j or l == k:
                        continue
                    remaining_after_fourth = remaining_after_third - weights[l]
                    for m in range(len(weights)):
                        if m == i or m == j or m == k or m == l:
                            continue
                        prob = (weights[i] / total) * (weights[j] / remaining_after_first) * (
                                weights[k] / remaining_after_second) * (weights[l] / remaining_after_third) * (
                                       weights[m] / remaining_after_fourth)
                        round_probs[m] += prob
    # 第5轮分组化的统计频次
    round_cnt = utils.to_groups([x[4] for x in strategies], group_names)
    utils.test_uniform_distribution(round_cnt, round_probs)
