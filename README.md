# caj2pdf

本项目由 [caj2pdf/caj2pdf](https://github.com/caj2pdf/caj2pdf) 重构而来，仅仅修改了 Python 包的组织方式，以便使用包管理工具进行简便地安装和调用。

1. 可以使用 build.py 脚本编译二进制依赖
2. 可以在任何工作目录下使用 caj2pdf 命令，而无需移动到同一目录
3. 如果存在任何关于 CAJ 文件格式而导致的问题，请到 [caj2pdf/caj2pdf](https://github.com/caj2pdf/caj2pdf/issues) 提交反馈。如果存在本项目无法安装、调用出错或者版本过于落后等问题，可到 [issues](issues/) 提交反馈。

## Why

[中国知网](http://cnki.net/)的某些文献（多为学位论文）仅提供其专有的 CAJ 格式下载，仅能使用知网提供的软件（如 [CAJViewer](http://cajviewer.cnki.net/) 等）打开，给文献的阅读和管理带来了不便（尤其是在非 Windows 系统上）。

若要将 CAJ 文件转换为 PDF 文件，可以使用 CAJViewer 的打印功能。但这样得到的 PDF 文件的内容为图片，无法进行文字的选择，且原文献的大纲列表也会丢失。本项目希望可以解决上述两问题。

## How to use

### 环境和依赖

- Python 3.10+ （使用了 `importlib.resources` 模块，以提供在任意目录下工作的能力）
- [PyPDF2](https://github.com/mstamy2/PyPDF2)
- [mutool](https://mupdf.com/index.html)

除了Microsoft Windows：我们提供Microsoft Windows 32-bit/64-bit DLLs，HN 格式需要

- C/C++编译器
- libpoppler开发包，或libjbig2dec开发包

### 安装

#### ArchLinux

```sh
# poppler 库
sudo pacman -S base-devel poppler mupdf-tools
pip install caj2pdf-restructured

# jbig2dec 库
sudo pacman -S base-devel jbig2dec mupdf-tools
LIBJBIG2DEC=1 pip install caj2pdf-restructured
```

或使用 [pipx](https://github.com/pipxproject/pipx)

```sh
# poppler 库
sudo pacman -S base-devel poppler mupdf-tools
pipx install caj2pdf-restructured

# jbig2dec 库
sudo pacman -S base-devel jbig2dec mupdf-tools
LIBJBIG2DEC=1 pipx install caj2pdf-restructured
```

#### Debian, Ubuntu 等 Linux

```sh
# poppler 库
sudo apt install build-essential libpoppler-dev mupdf-tools
pip install caj2pdf-restructured
```

或使用 [pipx](https://github.com/pipxproject/pipx)

```sh
# poppler 库
sudo apt install build-essential libpoppler-dev mupdf-tools
pipx install caj2pdf-restructured
```

**注意**：

1. jbig2dec 库在 Ubuntu/Debian 上的安装存在依赖问题，因此建议只使用 poppler 库。
2. Ubuntu 16.04 的 poppler 库版本过于落后，建议在较新的系统上安装。

#### Windows

可以直接通过 pip 或 pipx 安装：

```sh
pip install caj2pdf-restructured

pipx install caj2pdf-restructured
```

然后，从 [mutool](https://mupdf.com/index.html) 下载 mupdf-1.18.0-windows.zip 并解压，将其中的 mutool.exe 添加到 `PATH` 变量中的路径下，以便从任意位置调用。

如果你使用 [choco](https://chocolatey.org) 或 [scoop](https://scoop.sh/) 作为 Windows 下的包管理工具，则可一键式安装：

```sh
choco install mupdf
```

或者

```sh
scoop install mupdf
```

### 用法

```
# 打印文件基本信息（文件类型、页面数、大纲项目数）
caj2pdf show [input_file]

# 转换文件
caj2pdf convert [input_file] -o/--output [output_file]

# 从 CAJ 文件中提取大纲信息并添加至 PDF 文件
## 遇到不支持的文件类型或 Bug 时，可用 CAJViewer 打印 PDF 文件，并用这条命令为其添加大纲
caj2pdf outlines [input_file] -o/--output [pdf_file]
```
### 例

```
caj2pdf show test.caj
caj2pdf convert test.caj -o output.pdf
caj2pdf outlines test.caj -o printed.pdf
```

#### 右键菜单

0.1.0a4 版本后，可以在 Windows 系统上使用右键菜单转换 CAJ 文件了。

![](screenshot1.png)

需要在命令行中调用命令 `caj2pdf install` 安装注册表，然后才能使用此功能。
如果卸载程序，注册表 **不会被清理**，待研究 pip，看看能不能在 uninstall 之前加 HOOK。

TODO: 清理注册表的功能。

### 异常输出（IMPORTANT!!!）

尽管这个项目目前有不少同学关注到了，但它**仍然只支持部分 caj 文件的转换**，必须承认这完全不是一个对普通用户足够友好的成熟项目。具体支持哪些不支持哪些，在前文也已经说了，但似乎很多同学并没有注意到。所以**如果你遇到以下两种输出，本项目目前无法帮助到你**。与此相关的 issue 不再回复。

- `Unknown file type.`：未知文件类型；

## How far we've come

知网下载到的后缀为 `caj` 的文件内部结构其实分为两类：CAJ 格式和 HN 格式（受考察样本所限可能还有更多）。目前本项目支持 CAJ 格式文件的转换，HN 格式的转换未完善，并且需要建立两个新的共享库（除了Microsoft Windows：我们提供Microsoft Windows 32-bit/64-bit DLLs），详情如下：

```
cc -Wall -fPIC --shared -o libjbigdec.so jbigdec.cc JBigDecode.cc
cc -Wall `pkg-config --cflags poppler` -fPIC -shared -o libjbig2codec.so decode_jbig2data.cc `pkg-config --libs poppler`
```

抑或和libpoppler 相比，还是取决于您是否更喜欢libjbig2dec一点，可以替换libpoppler：

```
cc -Wall -fPIC --shared -o libjbigdec.so jbigdec.cc JBigDecode.cc
cc -Wall `pkg-config --cflags jbig2dec` -fPIC -shared -o libjbig2codec.so decode_jbig2data_x.cc `pkg-config --libs jbig2dec`
```

**NOTE（zombie110year,2021/04/20）**：现在可以使用 `python build.py` 指令来编译链接库了。并且源代码和输出文件的路径移动到了 `caj2pdf/dep` 之中，和上面的命令不同。

1. 默认使用 libpoppler 作为依赖编译：

```sh
python build.py
```

2. 或者，使用 jbig2dec 作为依赖编译：

```sh
LIBJBIG2DEC=1 python build.py
```

**关于两种格式文件结构的分析进展和本项目的实现细节，请查阅[项目 Wiki](https://github.com/JeziL/caj2pdf/wiki)。**

## How to contribute

受测试样本数量所限，即使转换 CAJ 格式的文件也可能（或者说几乎一定）存在 Bug。如遇到这种情况，欢迎在 [Issue](https://github.com/JeziL/caj2pdf/issues) 中提出，**并提供可重现 Bug 的 caj 文件**——可以将样本文件上传到网盘等处<del>，也可直接提供知网链接</del>（作者已滚出校园网，提 issue 请提供可下载的 caj 文件）。

如果你对二进制文件分析、图像/文字压缩算法、逆向工程等领域中的一个或几个有所了解，欢迎帮助完善此项目。你可以从阅读[项目 Wiki](https://github.com/JeziL/caj2pdf/wiki) 开始，看看是否有可以发挥你特长的地方。**Pull requests are always welcome**.

## License

本项目基于 [GLWTPL](https://github.com/me-shaon/GLWTPL)  (Good Luck With That Public License) 许可证开源。
