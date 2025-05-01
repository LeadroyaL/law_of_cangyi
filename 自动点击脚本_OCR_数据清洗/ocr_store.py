import torch

# 从黑市mp4文件中解析数据
# 输入格式：.mp4
# 第一轮输出格式：time, item0, item1, item2, item3, item4
# 第二轮输出格式：time, s0, s1, s2, s3, s4
# 第三轮输出格式：excel

rect1 = [163, 27, 212, 83]
rect2 = [400, 86, 600, 127]
rect3 = [882, 86, 1040, 127]
rect4 = [1333, 86, 1511, 127]

import cv2
import re
import easyocr

reader = easyocr.Reader(['ch_sim'], gpu=True)


def extract_chinese_text(image):
    """
    从图像中提取中文文本
    :param image: 输入的图像
    :return: 提取到的中文文本
    """
    # 创建一个 easyocr 读取器，指定语言为中文
    # 进行 OCR 识别
    result = reader.readtext(image)
    # 提取识别结果中的文本
    # print(result)
    if any(item[2] < 0.3 for item in result):
        return ''
    text = ''.join([item[1] for item in result])
    # 使用正则表达式仅保留中文字符
    chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)
    return ''.join(chinese_text)


def process_video(video_path):
    print("Handle", video_path)
    """
    处理视频，对每一秒指定区域进行 OCR 识别
    :param video_path: 视频文件路径
    """
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    while True:
        # 设置视频读取位置到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        real_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if real_frame < frame_count:
            break
        ret, frame = cap.read()
        if not ret:
            break
        current_second = int(frame_count / fps)
        # 提取指定区域
        rnd_text = []
        for rect in [rect2, rect3, rect4, ]:
            x1, y1, x2, y2 = rect
            roi = frame[y1:y2, x1:x2]
            # 进行 OCR 识别并提取中文文本
            chinese_text = extract_chinese_text(roi)
            rnd_text.append(chinese_text)
            # 跳转到下一个需要处理的帧
        # 跳过处理失败的情况
        if '' not in rnd_text:
            print(f"第{current_second}秒:[{','.join(rnd_text)}]")
        # print(f"{rnd_text}")
        frame_count += 20
    # 释放视频捕获对象
    cap.release()


if __name__ == "__main__":
    pass
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\火策略1.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\火策略2.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\光策略覆盖1个.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\光策略覆盖2个.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\暗策略无冲突.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\光策略2-3上篇.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\光策略2-3下篇.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\光策略高阶2-3.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\光策略3-2.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\5个一阶强化1.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\5个一阶强化2.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\4个二阶1个红.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\5个二阶强化.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\4个二阶1个红_v2.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\策略房\4个二阶1个红_v3.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\商店房\1个一阶强化4个二阶强化.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\商店房\3个一阶强化2个二阶强化.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\商店房\4个一阶强化1个二阶强化.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\商店房\4个二阶强化1个红.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\商店房\5个一阶强化.mp4")
    # process_video(r"D:\PycharmProjects\law_of_cangyi\mp4\商店房\5个二阶强化.mp4")
