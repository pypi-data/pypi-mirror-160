#!/usr/bin/env python3

import argparse
import curses
import importlib
import re
import sys
import inspect
from os import walk
import unicodedata

def getFiles(path) :
    for (dirpath, dirnames, filenames) in walk(path) :
        dirpath = dirpath
        dirnames = dirnames
        filenames = filenames
        return filenames

    return []

def getPluginFiles(dirpath):
    return getFiles(dirpath)

def getClassMethods(clazz):
    methods = dict()
    for item in dir(clazz):
        if item.startswith("_"):
            continue

        method = getattr(clazz, item)
        methods[item] = [str(method.__doc__).strip()] 
    
    return methods

def addRun(clazz):

    @classmethod
    def run(clazz, kwargs):
        """
        使用装饰的方法给Plugin进行统一添加该方法，便于统一修改
        """

        print(">>> enter plugin run method")
        # print("cmd line args: " + str(kwargs))
        if len(inspect.signature(getattr(clazz, "__init__")).parameters) == 2: 
            obj = clazz(kwargs)
        else:
            obj = clazz()

        invert_op = getattr(obj, "start", None)
        if callable(invert_op):
            print(">>> enter plugin start method")
            if len(inspect.signature(invert_op).parameters) > 0:
                invert_op(kwargs)
            else:
                invert_op()
            print("<<< end plugin start method")
        print("<<< end plugin run method")

    # print(">>> start add plugin run method")
    setattr(clazz, 'run', run)
    # print(dir(clazz))
    # items = getClassMethods(clazz)
    # for item in items:
    #     if item == "run":
    #         print(item + ": " + items[item][0])
    # print("<<< end add plugin run method")

    return clazz

def _strWidth(chs):
    
    chLength = 0
    for ch in chs:
        if (unicodedata.east_asian_width(ch) in ('F','W','A')):
            chLength += 2
        else:
            chLength += 1
    
    return chLength

def _drawPlugins(mainScreen, plugins, topIndex, index, pluginsMaxLen, maxRows, maxCols, color):
    row  = 1

    # 上下两个边框占用2行
    if (maxRows - 2) > len(plugins):
        for plugin in plugins:
            # 行从1开始绘图，index是从0开始算的
            if ((row - 1) == index):
                mainScreen.addstr(row, maxCols // 2 - pluginsMaxLen // 2, plugin, curses.color_pair(color))
            else:
                mainScreen.addstr(row, maxCols // 2 - pluginsMaxLen // 2, plugin)

            row += 1
    else:
        # 上下两个边框占用2行
        for plugin in plugins[topIndex:topIndex + (maxRows - 2)]:
            # 行从1开始绘图，index是从0开始算的
            if (row - 1) == (index - topIndex):
                mainScreen.addstr(row, maxCols // 2 - pluginsMaxLen // 2, plugin, curses.color_pair(color))
            else:
                mainScreen.addstr(row, maxCols // 2 - pluginsMaxLen // 2, plugin)

            row += 1

    # 刷新界面
    mainScreen.refresh()

def _showPlugins(plugins, helpList):

    # keyboard code
    KEY_BOARD_ENTER = 10
    KEY_BOARD_ESC = 27
    KEY_BOARD_UP = 259
    KEY_BOARD_DOWN = 258
    KEY_BOARD_J = 106
    KEY_BOARD_K = 107
    KEY_BOARD_Q = 113
    KEY_BOARD_H = 104

    # 初始化一个窗口
    mainScreen = curses.initscr()
    # 绘制边框
    mainScreen.border(0)
    # 使用curses通常要关闭屏幕回显，目的是读取字符仅在适当的环境下输出
    curses.noecho()
    # 应用程序一般是立即响应的，即不需要按回车就立即回应的，这种模式叫cbreak模式，相反的常用的模式是缓冲输入模式
    curses.cbreak()
    # 终端经常返回特殊键作为一个多字节的转义序列，比如光标键，或者导航键比如Page UP和Home键。
    # curses可以针对这些序列做一次处理，比如curses.KEY_LEFT返回一个特殊的值。要完成这些工作，必须开启键盘模式。
    mainScreen.keypad(1)
    # 不显示光标
    curses.curs_set(0) 

    # color
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    DEFAULT_COLOR = 1
    FG_GREEN_COLOR = 2
    
    # 获取当前行列信息
    maxRows = curses.LINES
    maxCols = curses.COLS
    MIN_ROWS = 5
    if (maxRows < MIN_ROWS):
        curses.endwin()
        print("terminal rows must more than " + str(MIN_ROWS))
        exit(0)

    pluginsMaxLen = 0
    for plugin in plugins:
        if len(plugin) > pluginsMaxLen:
            pluginsMaxLen = len(plugin)
    

    # 当前选择的目标程序
    index = 0
    # 终端可显示的程序列表第一个程序，因为存在列表显示不全，只能显示部分程序列表的问题
    topIndex = 0
    # 进入Help模式
    inHelpStatus = False

    _drawPlugins(mainScreen, plugins, topIndex, index, pluginsMaxLen, maxRows, maxCols, FG_GREEN_COLOR)

    # Define windows to be used for bar charts
    # curses.newwin(height, width, begin_y, begin_x)
    helpScreen = curses.newwin(
            3,                              # 上下边框 + 内容
            (maxCols - 4),                  # 左右边框 + 左右空列
            (maxRows - 2 - 2 + 1) // 2,     # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
            2                               # 主屏左边框 + 左空列
        )
    
    while True:
        # 等待按键事件
        ch = mainScreen.getch()
    
        if ch == curses.KEY_RESIZE or inHelpStatus:
            mainScreen.clear()
            mainScreen.border(0)
            maxRows, maxCols = mainScreen.getmaxyx()

            helpScreen.resize(
                    3,              # 上下边框 + 内容
                    maxCols - 4     # 左右边框 + 左右空列
                )

            if maxRows < MIN_ROWS:
                curses.endwin()
                print("terminal rows must more than " + str(MIN_ROWS))
                exit(0)
    
            _drawPlugins(mainScreen, plugins, topIndex, index, pluginsMaxLen, maxRows, maxCols, FG_GREEN_COLOR)

            inHelpStatus = False
        # show help
        elif ch == KEY_BOARD_H:
            inHelpStatus = True

            helpScreen.mvwin(
                    (maxRows - 2 - 2 + 1) // 2,     # 主屏上下边框 + 帮助屏上下边框 + 取整补充1
                    2                               # 主屏左边框 + 左空列
                )
            helpScreen.clear()
            # 主屏左右边框 + 左右空列 + 帮助屏左右边框
            helpScreenWidth = maxCols - 4 - 2
            if helpScreenWidth > _strWidth(helpList[index]):
                helpScreen.addstr(1, (helpScreenWidth) // 2 - _strWidth(helpList[index]) // 2, helpList[index])
            else:
                # 可显示字符区域小于字符串实际宽度，只截取一半显示，以后有需求，把这里改成加上三个点表示省略部分
                helpScreen.addstr(1, 1, helpList[index][0:(helpScreenWidth // 2)])
            helpScreen.border(0)
            helpScreen.refresh()
        # 退出按键
        elif ch == KEY_BOARD_ESC or ch == KEY_BOARD_Q:
            index = -1
            break
        elif ch == KEY_BOARD_UP or ch == KEY_BOARD_K:
            index -= 1
            if index <= 0:
                index = 0

            # 处理上边缘
            if topIndex == (index + 1):
                topIndex -= 1

            mainScreen.clear()
            mainScreen.border(0)
            _drawPlugins(mainScreen, plugins, topIndex, index, pluginsMaxLen, maxRows, maxCols, FG_GREEN_COLOR)
        elif ch == KEY_BOARD_DOWN or ch == KEY_BOARD_J:
            index += 1
            if index >= len(plugins):
                index = len(plugins) - 1
            else:
                # 处理下边缘
                # 上下两个边框占用2行
                if (topIndex + (maxRows - 2)) == index :
                    topIndex += 1

            mainScreen.clear()
            mainScreen.border(0)
            _drawPlugins(mainScreen, plugins, topIndex, index, pluginsMaxLen, maxRows, maxCols, FG_GREEN_COLOR)
        elif ch == KEY_BOARD_ENTER:
            break
        else:
            pass
    
    # 退出curses环境
    curses.endwin()

    return index

def PluginsPy(cmd, skipedPlugins=[], pluginsDir="Plugins") :

    parser = argparse.ArgumentParser(prog=cmd)
    subparsers = parser.add_subparsers(help='commands help')

    # tensorflow加载太慢，有需要的情况下通过-s参数判定加载
    argv = sys.argv[1:]
    skipOption = True
    if "-s" in argv and len(argv) >= 1 and argv[0] == "-s":
        if len(argv) == 1:
            argv = []
        elif len(argv) > 1:
            argv = argv[1:]

        skipOption = False

    # 处理插件
    pluginsList = []
    helpList = []
    for file in getPluginFiles(pluginsDir):
        if file == "__init__.py":
            continue

        # skip config: Plugins/__init__.py
        if skipOption and (file.split(".")[0] in skipedPlugins):
            print("skiped pulgin: " + file)
            continue

        """
        1. 使用文件名获取模块名，
        2. 导入模块，
        3. 获取模块同名类，
        4. 获取类方法
        """
        moduleString = file.split(".")[0]
        module = importlib.import_module(pluginsDir + "." + moduleString)
        clazz = getattr(module, moduleString)

        clazzDoc = clazz.__doc__
        # 从类注释中获取类说明，也就是帮助
        helpStr = clazzDoc.split("@")[0].strip().replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
        parser_item = subparsers.add_parser(moduleString, help = helpStr)
        helpList.append(helpStr)

        # 从类注释中获取类参数及参数说明，格式@argument: argument doc
        keyValues = {}
        for arg in clazzDoc.split("\n"):
            keyValue = arg.strip().split(":")
            if len(keyValue) == 2 and keyValue[0].strip().startswith("@"):
                keyValues[keyValue[0].strip().replace("@", "")] = keyValue[1].strip()

        # 转换为命令行参数
        for arg in keyValues:
            matchObj = re.match(r'(\S*)\((\S*)\)', arg)
            if matchObj:
                # print("-----------matchObj-----------")
                # print(matchObj.group(1))
                # print(matchObj.group(2))
                # print("------------------------------")
                parser_item.add_argument('-' + matchObj.group(1), default=matchObj.group(2), help=keyValues[arg])
            else:
                parser_item.add_argument('-' + arg, help=keyValues[arg])

        # 获取当前处理方法并设置为该命令的回调函数
        method = getattr(clazz, "run")
        parser_item.set_defaults(func=method)

        pluginsList.append(moduleString)
    
    if len(argv) == 0:
        index = _showPlugins(pluginsList, helpList)
        if index >= 0:
            print("selected plugin: " + pluginsList[index])
            argv.append(pluginsList[index])
        elif index == -1:
            exit(0)

    #执行函数功能
    args = parser.parse_args(argv)
    if args :
        if len(args.__dict__) > 0:
            print(">>> start call Plugin run or CmdMaps method")
            args.func(args.__dict__)
            print("<<< end call Plugin run or CmdMaps method")
        else:
            parser.parse_args(["-h"])

if __name__ == "__main__" :
    pass
