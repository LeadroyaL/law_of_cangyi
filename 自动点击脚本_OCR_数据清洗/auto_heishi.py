import os
import logging
import time
from time import sleep

PKG_NAME = "com.actgames.bbee.huawei"
ENTRY_NAME = "TuanjiePlayerAbility"
RETRY_CNT = 10

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')


def restart():
    logging.info("正在重启")
    os.system(f"hdc shell aa force-stop {PKG_NAME}")
    os.system(f"hdc shell aa start -b {PKG_NAME} -a {ENTRY_NAME}")


def wait(second: int):
    logging.debug(f"等待{second}秒")
    time.sleep(second)


def click(msg: str, x: int, y: int, times: int = 1):
    logging.info(f"点击内容 '{msg}'")
    logging.debug(f"点击位置[{x},{y}]")
    os.system(f"hdc shell uitest uiInput click {x} {y}")
    for i in range(times - 1):
        sleep(1)
        logging.debug(f"再次点击位置[{x},{y}]")
        os.system(f"hdc shell uitest uiInput click {x} {y}")


def roll():
    restart()
    wait(30)
    for i in range(RETRY_CNT):
        logging.info(f"正在执行第{i}轮测试")
        click("开始游戏", 1553, 700, 2)
        wait(5)
        click("第二个存档", 1200, 635, 2)
        wait(3)
        click("复制", 330, 1180, 2)
        wait(3)
        click("第一个存档", 500, 600, 2)
        wait(3)
        click("粘贴", 2479, 1166, 2)
        wait(3)
        click("确认", 2040, 922, 2)
        wait(3)
        click("第一个存档", 500, 600, 2)
        wait(3)
        click("启动", 2479, 1166, 2)
        wait(30)
        click("冲刺", 2244, 1040)
        wait(3)
        click("普攻", 2587, 1040)
        wait(3)
        click("获取5策略", 1900, 650, 4)
        wait(15)
        click("右上角", 2700, 75, 2)
        wait(3)
        click("返回主菜单", 2333, 1122, 2)
        wait(3)
        click("确认", 2000, 933, 2)
        wait(10)


while True:
    roll()
