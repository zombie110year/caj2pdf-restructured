from os import getenv
from pathlib import Path
from platform import system
from pprint import pprint
from subprocess import PIPE, run
from sys import exit
from typing import Any, Dict

basedir = Path(__file__).parent.absolute()
# input
decode_jbig2data_x_cc = str(basedir / "caj2pdf" / "dep" / "decode_jbig2data_x.cc")
decode_jbig2data_cc = str(basedir / "caj2pdf" / "dep" / "decode_jbig2data.cc")
jbigdec_cc = str(basedir / "caj2pdf" / "dep" / "jbigdec.cc")
JBigDecode_cc = str(basedir / "caj2pdf" / "dep" / "JBigDecode.cc")

# output
libjbigdec_so = str(basedir / "caj2pdf" / "dep" / "bin" / "libjbigdec.so")
libjbig2codec_so = str(basedir / "caj2pdf" / "dep" / "bin" / "libjbig2codec.so")
libjbigdec_32dll = str(basedir / "caj2pdf" / "dep" / "bin" / "libjbigdec-w32.dll")
libjbig2codec_32dll = str(basedir / "caj2pdf" / "dep" / "bin" / "libjbig2codec-w32.dll")
libjbigdec_64dll = str(basedir / "caj2pdf" / "dep" / "bin" / "libjbigdec-w64.dll")
libjbig2codec_64dll = str(basedir / "caj2pdf" / "dep" / "bin" / "libjbig2codec-w64.dll")


def build(setup_kwargs: Dict[str, Any]):
    """编译二进制依赖

    读取环境变量 `LIBJBIG2DEC` 选择依赖库：

    1. `LIBJBIG2DEC=0` 或未设置，则使用 poppler 库
    2. `LIBJBIG2DEC=1` 或任何非 `0` 值，使用 libjbig2dec 库
    """

    if system() == "Linux":
        if getenv("LIBJBIG2DEC", "0") == "0":
            build_poppler()
        else:
            build_jbig2dec()
        setup_kwargs["package_data"]["caj2pdf.dep"] = []
    elif system() == "Windows":
        print("BUILD: {}".format(libjbigdec_32dll))
        print("BUILD: {}".format(libjbigdec_64dll))
        print("BUILD: {}".format(libjbig2codec_32dll))
        print("BUILD: {}".format(libjbig2codec_64dll))
        setup_kwargs["package_data"]["caj2pdf.dep"] = ["bin/*.dll"]
    return setup_kwargs

def build_poppler():
    dep_checker = run(["pkg-config", "--libs", "--cflags", "poppler"], stdout=PIPE)
    if dep_checker.returncode != 0:
        print("poppler 未安装，请通过系统包管理器安装")
        exit(-1)

    cmd_jbigdec = ["cc", "-Wall", "-fPIC", "-shared", "-o", libjbigdec_so, jbigdec_cc, JBigDecode_cc]
    run(cmd_jbigdec)
    print("BUILD: {}".format(libjbigdec_so))

    poppler_flags = dep_checker.stdout.decode("utf-8").strip().split(" ")
    cmd_jbig2codec = ["cc", "-Wall", *poppler_flags, "-fPIC", "-shared", "-o", libjbig2codec_so, decode_jbig2data_cc]
    run(cmd_jbig2codec)
    print("BUILD: {}".format(libjbig2codec_so))


def build_jbig2dec():
    dep_checker = run(["pkg-config", "--libs", "--cflags", "jbig2dec"], stdout=PIPE)
    if dep_checker.returncode != 0:
        print("jbig2dec 未安装，请通过系统包管理器安装")
        exit(-1)

    cmd_jbigdec = ["cc", "-Wall", "-fPIC", "-shared", "-o", libjbigdec_so, jbigdec_cc, JBigDecode_cc]
    run(cmd_jbigdec)
    print("BUILD: {}".format(libjbigdec_so))

    jbig2dec_flags = dep_checker.stdout.decode("utf-8").strip().split(" ")
    cmd_jbig2codec = ["cc", "-Wall", *jbig2dec_flags, "-fPIC", "-shared", "-o", libjbig2codec_so, decode_jbig2data_x_cc]
    run(cmd_jbig2codec)
    print("BUILD: {}".format(libjbig2codec_so))


if __name__ == "__main__":
    # 只编译二进制文件，不处理打包程序
    build({})
