from os import getenv
from pathlib import Path
from platform import system
from subprocess import PIPE, run
from sys import exit, stderr


def build(src: str, dst: str):
    """编译二进制依赖

    读取环境变量 `LIBJBIG2DEC` 选择依赖库：

    1. `LIBJBIG2DEC=0` 或未设置，则使用 poppler 库
    2. `LIBJBIG2DEC=1` 或任何非 `0` 值，使用 libjbig2dec 库

    note: 使用 pdm build <https://pdm.fming.dev/latest/pyproject/build/#custom-file-generation>
    """
    root = Path(src)
    dlls = root / "dlls"
    dep = root / "caj2pdf" / "dep"
    # input
    decode_jbig2data_x_cc = (dep / "decode_jbig2data_x.cc").as_posix()
    decode_jbig2data_cc = (dep / "decode_jbig2data.cc").as_posix()
    jbigdec_cc = (dep / "jbigdec.cc").as_posix()
    JBigDecode_cc = (dep / "JBigDecode.cc").as_posix()

    # output
    libjbigdec_so = (dep / "bin" / "libjbigdec.so").as_posix()
    libjbig2codec_so = (dep / "bin" / "libjbig2codec.so").as_posix()

    if system() == "Linux":
        if getenv("LIBJBIG2DEC", "0") == "0":
            build_poppler(
                # output
                libjbigdec_so,
                libjbig2codec_so,
                # input
                jbigdec_cc,
                JBigDecode_cc,
                decode_jbig2data_cc,
            )
        else:
            build_jbig2dec(
                # output
                libjbigdec_so,
                libjbig2codec_so,
                # input
                jbigdec_cc,
                JBigDecode_cc,
                decode_jbig2data_x_cc,
            )
    elif system() == "Windows":
        s_libjbigdec_32dll = dlls / "libjbigdec-w32.dll"
        s_libjbig2codec_32dll = dlls / "libjbig2codec-w32.dll"
        s_libjbigdec_64dll = dlls / "libjbigdec-w64.dll"
        s_libjbig2codec_64dll = dlls / "libjbig2codec-w64.dll"
        t_libjbigdec_32dll = (dep / "bin" / "libjbigdec-w32.dll").as_posix()
        t_libjbig2codec_32dll = (dep / "bin" / "libjbig2codec-w32.dll").as_posix()
        t_libjbigdec_64dll = (dep / "bin" / "libjbigdec-w64.dll").as_posix()
        t_libjbig2codec_64dll = (dep / "bin" / "libjbig2codec-w64.dll").as_posix()
        t_libjbigdec_32dll.hardlink_to(s_libjbigdec_32dll)
        t_libjbig2codec_32dll.hardlink_to(s_libjbig2codec_32dll)
        t_libjbigdec_64dll.hardlink_to(s_libjbigdec_64dll)
        t_libjbig2codec_64dll.hardlink_to(s_libjbig2codec_64dll)
        print("BUILD: {}".format(t_libjbigdec_32dll))
        print("BUILD: {}".format(t_libjbigdec_64dll))
        print("BUILD: {}".format(t_libjbig2codec_32dll))
        print("BUILD: {}".format(t_libjbig2codec_64dll))


def build_poppler(
    # output
    libjbigdec_so,
    libjbig2codec_so,
    # input
    jbigdec_cc,
    JBigDecode_cc,
    decode_jbig2data_cc,
):
    dep_checker = run(["pkg-config", "--libs", "--cflags", "poppler"], stdout=PIPE)
    if dep_checker.returncode != 0:
        print("poppler 未安装，请通过系统包管理器安装", file=stderr)
        exit(-1)

    cmd_jbigdec = [
        "cc",
        "-Wall",
        "-fPIC",
        "-shared",
        "-o",
        libjbigdec_so,
        jbigdec_cc,
        JBigDecode_cc,
    ]
    run(cmd_jbigdec)
    print("BUILD: {}".format(libjbigdec_so))

    poppler_flags = dep_checker.stdout.decode("utf-8").strip().split(" ")
    cmd_jbig2codec = [
        "cc",
        "-Wall",
        *poppler_flags,
        "-fPIC",
        "-shared",
        "-o",
        libjbig2codec_so,
        decode_jbig2data_cc,
    ]
    run(cmd_jbig2codec)
    print("BUILD: {}".format(libjbig2codec_so))


def build_jbig2dec(
    # output
    libjbigdec_so,
    libjbig2codec_so,
    # input
    jbigdec_cc,
    JBigDecode_cc,
    decode_jbig2data_x_cc,
):
    dep_checker = run(["pkg-config", "--libs", "--cflags", "jbig2dec"], stdout=PIPE)
    if dep_checker.returncode != 0:
        print("jbig2dec 未安装，请通过系统包管理器安装", file=stderr)
        exit(-1)

    cmd_jbigdec = [
        "cc",
        "-Wall",
        "-fPIC",
        "-shared",
        "-o",
        libjbigdec_so,
        jbigdec_cc,
        JBigDecode_cc,
    ]
    run(cmd_jbigdec)
    print("BUILD: {}".format(libjbigdec_so))

    jbig2dec_flags = dep_checker.stdout.decode("utf-8").strip().split(" ")
    cmd_jbig2codec = [
        "cc",
        "-Wall",
        *jbig2dec_flags,
        "-fPIC",
        "-shared",
        "-o",
        libjbig2codec_so,
        decode_jbig2data_x_cc,
    ]
    run(cmd_jbig2codec)
    print("BUILD: {}".format(libjbig2codec_so))
