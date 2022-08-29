"""提供给上下文菜单调用

目前仅支持 Windows
"""
import pathlib
import sys

from .cajparser import CAJParser
from .exceptions import Caj2PdfException


def main():
    try:
        app()
    except Exception as e:
        pass


def app():
    try:
        cajfilepath_str = sys.argv[1]
    except IndexError as e:
        raise Caj2PdfException(f"找不到caj文件，输入参数为：{sys.argv!r}")

    cajfilepath = pathlib.Path(cajfilepath_str)
    if not cajfilepath.exists():
        raise Caj2PdfException(f"caj文件不存在：{cajfilepath.as_posix()}")

    inputfile = str(cajfilepath)
    outputfile = f"{inputfile}.pdf"

    caj = CAJParser(inputfile)
    caj.convert(outputfile)
