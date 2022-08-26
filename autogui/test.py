from mytime import get_time

import pyautogui
import pyperclip


def mytest():
    x, y = pyautogui.position()
    print("当前鼠标的X轴的位置为：{}，Y轴的位置为：{}".format(x, y))
    x, y = pyautogui.size()
    print("当前屏幕的分辨率是{}*{}".format(x, y))


def click_first():
    pyautogui.locateAllOnScreen(r'a.png')
    for pos in pyautogui.locateAllOnScreen(r'a.png'):
        # pyautogui.moveTo(x=300, y=300, duration=0.25)
        print(pos)
        pyautogui.leftClick(pos)


# 点击回复
def click_third():
    pyautogui.locateAllOnScreen(r'c.png')
    for pos in pyautogui.locateAllOnScreen(r'c.png'):
        # pyautogui.moveTo(x=300, y=300, duration=0.25)
        print(pos)
        pyautogui.leftClick(pos)
        write_content()
        click_forth()


def click_five():
    # pyautogui.locateAllOnScreen(r'f.png')
    pos = pyautogui.locateOnScreen(r'f.png')
    # pyautogui.moveTo(x=300, y=300, duration=0.25)
    print(pyautogui.center(pos))
    x, y = pyautogui.center(pos)
    pyautogui.moveTo(x + 45, y, 1)
    pyautogui.leftClick()
    print("已点击回复按钮:")


# 提交回复
def click_forth():
    pos = pyautogui.locateOnScreen(r'd.png')
    if pos is not None:
        # pyautogui.moveTo(x=300, y=300, duration=0.25)
        x, y = pyautogui.center(pos)
        pyautogui.moveTo(658, y, 1)
        pyautogui.leftClick()
        print("已提交评论按钮:")
    else:
        print("未找到按钮")


# 写入评论
def write_content():
    content = "%s:测试自动回复100个,测试完就结束...." % format(get_time())
    print(content)
    pyperclip.copy(content)
    pyautogui.hotkey('ctrl', 'v')
    print("已写入内容:")


def click_second():
    # 该坐标的像素点的颜色是：(255, 255, 255)
    pyautogui.locateAllOnScreen(r'b.png')
    for pos in pyautogui.locateAllOnScreen(r'b.png'):
        # pyautogui.moveTo(x=300, y=300, duration=0.25)
        print(pos)
        pyautogui.leftClick(pos)


def myscroll():
    pyautogui.scroll(-400)


if __name__ == '__main__':
    for item in range(100):
        click_five()
        write_content()
        click_forth()
        pyautogui.scroll(-380)
        pyautogui.moveTo(100,100,1)
