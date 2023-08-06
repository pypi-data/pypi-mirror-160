RED = 0
YELLOW = 0
BLACK = 0
GREEN = 0
MAGENTA = 0
CYAN = 0
WHITE = 0  # 可用颜色


def echo(something, color: int, end: str) -> None:
    """
    建议使用的输出\n
    :param something: 可以为任意类型，如果是字典，列表将输出他们在go中的结构
    :param color: 输出的颜色，可省略，默认为白色
    :param end: 输出的结尾，可省略，默认为换行符
    :return:
    """
    ...


def select(title: str, items: list) -> (int, str):
    """
    生成一个选择菜单，方向键选择，Enter确认 \n
    :param title: 标题
    :param items: 可选择的项目，字符串列表，若为空则不会阻塞
    :return: 返回选项序号与选项文本
    """
    ...


def match(left: str, right: str, text: str) -> list:
    """
    匹配文本中满足条件的全部文本（正则实现）\n
    e.g.
    \t echo(match("a", "c", "abc aqc")) \n
    \t result: ["b","q"] \n
    :param left: 左侧文本
    :param right: 右侧文本
    :param text: 需要匹配的文本
    :return: 返回包含结果的字符串列表
    """
    ...


def walkdir(path: str) -> list:
    """
    遍历文件夹\n
    :param path: 路径
    :return: 所有文件与文件夹
    """
    ...


def unzip(src: str, passwd: str, dest: str) -> None:
    """
    解压zip \n
    :param src: zip文件路径
    :param passwd: 密码，可省略，默认为空字符串
    :param dest: 目标路径，可省略，默认解压在zip同目录下
    :return:
    """


def notice(title: str, msg: str, png_path: str, beep: bool) -> bool:
    """
    弹出通知\n
    :param title: 标题
    :param msg: 消息
    :param png_path: 显示图片，可省略，默认为空字符串
    :param beep: 是否蜂鸣，可省略，默认false
    :return:
    """
    ...
