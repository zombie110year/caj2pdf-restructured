"""提供给上下文菜单调用

目前仅支持 Windows
"""
import pathlib
import sys
import threading

from .cajparser import CAJParser
from .exceptions import Caj2PdfException


def main():
    try:
        app()
    except Exception:
        pass


def app():
    try:
        cajfilepath_str = sys.argv[1]
    except IndexError:
        raise Caj2PdfException(f"找不到caj文件，输入参数为：{sys.argv!r}")

    cajfilepath = pathlib.Path(cajfilepath_str)
    if not cajfilepath.exists():
        raise Caj2PdfException(f"caj文件不存在：{cajfilepath.as_posix()}")

    inputfile = str(cajfilepath)
    outputfile = f"{inputfile}.pdf"
    task = threading.Thread(
        group=None, target=convert_caj, args=(inputfile, outputfile)
    )
    alive = AliveStatus()
    task.start()
    alive.start()
    task.join()
    alive.finish()
    alive.join()


def convert_caj(inputfile, outputfile):
    caj = CAJParser(inputfile)
    caj.convert(outputfile)


class AliveStatus(threading.Thread):
    def __init__(self):
        super().__init__(group=None)
        self.finished = False

    def run(self):
        from time import sleep

        status = ("正在转换 <<<<<<", "正在转换 >>>>>>")
        i = 0b0
        while not self.finished:
            print(status[i & 0b1], end="\r", file=sys.stderr)
            i ^= 0b1
            sleep(0.2)

    def finish(self):
        self.finished = True
