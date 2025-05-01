# 从黑市mp4文件中解析数据
# 输入格式：.mp4
# 第一轮输出格式：time, item0, item1, item2, item3, item4
# 第二轮输出格式：time, s0, s1, s2, s3, s4
# 第三轮输出格式：excel
import os

from moviepy import VideoFileClip

rect = [818, 168, 1085, 222]

import cv2
import re
import easyocr

reader = easyocr.Reader(['ch_sim'], gpu=True)


def extract_chinese_text(image, ss, fps):
    """
    从图像中提取中文文本
    :param image: 输入的图像
    :return: 提取到的中文文本
    """
    # 创建一个 easyocr 读取器，指定语言为中文
    # 进行 OCR 识别
    current_second = int(ss / fps)
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    result = reader.readtext(image)
    # 提取识别结果中的文本
    # print(result)
    text = ''.join([item[1] for item in result])
    # 使用正则表达式仅保留中文字符
    chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)
    return ''.join(chinese_text)


def process_video(video_path, use_cv2 = False):
    print("Handle", video_path)
    """
    处理视频，对每一秒指定区域进行 OCR 识别
    :param video_path: 视频文件路径
    :param region: 指定区域 [x1, y1, x2, y2]
    """
    if use_cv2:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("无法打开视频文件")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)

    else:
        cap = VideoFileClip(video_path)
        fps = cap.fps
        duration = cap.duration

    region = [818, 168, 1085, 222]
    frame_count = 0
    while True:
        if use_cv2:
            # 设置视频读取位置到指定帧
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
            real_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            if real_frame < frame_count:
                break
            ret, frame = cap.read()
            if not ret:
                break
        else:
            if frame_count >= int(duration * fps):
                break
            frame = cap.get_frame(frame_count / fps)

        current_second = int(frame_count / fps)
        # 提取指定区域
        x1, y1, x2, y2 = region
        roi = frame[y1:y2, x1:x2]
        # 进行 OCR 识别并提取中文文本
        chinese_text = extract_chinese_text(roi, frame_count, fps)
        if chinese_text and chinese_text.startswith("获得"):
            print(f"第 {current_second} 秒: {chinese_text}")
            # print(f"第 {frame_count} 帧: {chinese_text}")
        # 跳转到下一个需要处理的帧
        frame_count += 15
    if use_cv2:
        # 释放视频捕获对象
        cap.release()
    else:
        cap.close()


if __name__ == "__main__":
    pass
    # for x in os.listdir(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_3个二阶2个一阶'):
    #     process_video(os.path.join(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_3个二阶2个一阶', x))
    # for x in os.listdir(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_全部空'):
    #     process_video(os.path.join(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_全部空', x))
    # for x in os.listdir(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_全光1阶'):
    #     process_video(os.path.join(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_全光1阶', x))
    # for x in os.listdir(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\OCR最后'):
    #     process_video(os.path.join(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\OCR最后', x))
    # for x in os.listdir(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_寒冰史莱姆'):
    #     process_video(os.path.join(r'D:\PycharmProjects\law_of_cangyi\mp4\黑市房\黑市_寒冰史莱姆', x))
