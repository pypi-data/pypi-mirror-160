# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caj2pdf', 'caj2pdf.dep']

package_data = \
{'': ['*'], 'caj2pdf.dep': ['bin/*']}

install_requires = \
['pypdf2>=1.26.0,<2.0.0']

entry_points = \
{'console_scripts': ['caj2pdf = caj2pdf.cli:main']}

setup_kwargs = {
    'name': 'caj2pdf-restructured',
    'version': '0.1.0a3',
    'description': 'caj2pdf 重新组织，方便打包与安装',
    'long_description': "# caj2pdf\n\n本项目由 [caj2pdf/caj2pdf](https://github.com/caj2pdf/caj2pdf) 重构而来，仅仅修改了 Python 包的组织方式，以便使用包管理工具进行简便地安装和调用。\n\n1. 可以使用 build.py 脚本编译二进制依赖\n2. 可以在任何工作目录下使用 caj2pdf 命令，而无需移动到同一目录\n3. 如果存在任何关于 CAJ 文件格式而导致的问题，请到 [caj2pdf/caj2pdf](https://github.com/caj2pdf/caj2pdf/issues) 提交反馈。如果存在本项目无法安装、调用出错或者版本过于落后等问题，可到 [issues](issues/) 提交反馈。\n\n## Why\n\n[中国知网](http://cnki.net/)的某些文献（多为学位论文）仅提供其专有的 CAJ 格式下载，仅能使用知网提供的软件（如 [CAJViewer](http://cajviewer.cnki.net/) 等）打开，给文献的阅读和管理带来了不便（尤其是在非 Windows 系统上）。\n\n若要将 CAJ 文件转换为 PDF 文件，可以使用 CAJViewer 的打印功能。但这样得到的 PDF 文件的内容为图片，无法进行文字的选择，且原文献的大纲列表也会丢失。本项目希望可以解决上述两问题。\n\n## How to use\n\n### 环境和依赖\n\n- Python 3.10+ （使用了 `importlib.resources` 模块，以提供在任意目录下工作的能力）\n- [PyPDF2](https://github.com/mstamy2/PyPDF2)\n- [mutool](https://mupdf.com/index.html)\n\n除了Microsoft Windows：我们提供Microsoft Windows 32-bit/64-bit DLLs，HN 格式需要\n\n- C/C++编译器\n- libpoppler开发包，或libjbig2dec开发包\n\n### 安装\n\n#### ArchLinux\n\n```sh\n# poppler 库\nsudo pacman -S base-devel poppler mupdf-tools\npip install caj2pdf-restructured\n\n# jbig2dec 库\nsudo pacman -S base-devel jbig2dec mupdf-tools\nLIBJBIG2DEC=1 pip install caj2pdf-restructured\n```\n\n或使用 [pipx](https://github.com/pipxproject/pipx)\n\n```sh\n# poppler 库\nsudo pacman -S base-devel poppler mupdf-tools\npipx install caj2pdf-restructured\n\n# jbig2dec 库\nsudo pacman -S base-devel jbig2dec mupdf-tools\nLIBJBIG2DEC=1 pipx install caj2pdf-restructured\n```\n\n#### Debian, Ubuntu 等 Linux\n\n```sh\n# poppler 库\nsudo apt install build-essential libpoppler-dev mupdf-tools\npip install caj2pdf-restructured\n```\n\n或使用 [pipx](https://github.com/pipxproject/pipx)\n\n```sh\n# poppler 库\nsudo apt install build-essential libpoppler-dev mupdf-tools\npipx install caj2pdf-restructured\n```\n\n**注意**：\n\n1. jbig2dec 库在 Ubuntu/Debian 上的安装存在依赖问题，因此建议只使用 poppler 库。\n2. Ubuntu 16.04 的 poppler 库版本过于落后，建议在较新的系统上安装。\n\n#### Windows\n\n可以直接通过 pip 或 pipx 安装：\n\n```sh\npip install caj2pdf-restructured\n\npipx install caj2pdf-restructured\n```\n\n然后，从 [mutool](https://mupdf.com/index.html) 下载 mupdf-1.18.0-windows.zip 并解压，将其中的 mutool.exe 添加到 `PATH` 变量中的路径下，以便从任意位置调用。\n\n如果你使用 [choco](https://chocolatey.org) 或 [scoop](https://scoop.sh/) 作为 Windows 下的包管理工具，则可一键式安装：\n\n```sh\nchoco install mupdf\n```\n\n或者\n\n```sh\nscoop install mupdf\n```\n\n### 用法\n\n```\n# 打印文件基本信息（文件类型、页面数、大纲项目数）\ncaj2pdf show [input_file]\n\n# 转换文件\ncaj2pdf convert [input_file] -o/--output [output_file]\n\n# 从 CAJ 文件中提取大纲信息并添加至 PDF 文件\n## 遇到不支持的文件类型或 Bug 时，可用 CAJViewer 打印 PDF 文件，并用这条命令为其添加大纲\ncaj2pdf outlines [input_file] -o/--output [pdf_file]\n```\n\n### 例\n\n```\ncaj2pdf show test.caj\ncaj2pdf convert test.caj -o output.pdf\ncaj2pdf outlines test.caj -o printed.pdf\n```\n\n### 异常输出（IMPORTANT!!!）\n\n尽管这个项目目前有不少同学关注到了，但它**仍然只支持部分 caj 文件的转换**，必须承认这完全不是一个对普通用户足够友好的成熟项目。具体支持哪些不支持哪些，在前文也已经说了，但似乎很多同学并没有注意到。所以**如果你遇到以下两种输出，本项目目前无法帮助到你**。与此相关的 issue 不再回复。\n\n- `Unknown file type.`：未知文件类型；\n\n## How far we've come\n\n知网下载到的后缀为 `caj` 的文件内部结构其实分为两类：CAJ 格式和 HN 格式（受考察样本所限可能还有更多）。目前本项目支持 CAJ 格式文件的转换，HN 格式的转换未完善，并且需要建立两个新的共享库（除了Microsoft Windows：我们提供Microsoft Windows 32-bit/64-bit DLLs），详情如下：\n\n```\ncc -Wall -fPIC --shared -o libjbigdec.so jbigdec.cc JBigDecode.cc\ncc -Wall `pkg-config --cflags poppler` -fPIC -shared -o libjbig2codec.so decode_jbig2data.cc `pkg-config --libs poppler`\n```\n\n抑或和libpoppler 相比，还是取决于您是否更喜欢libjbig2dec一点，可以替换libpoppler：\n\n```\ncc -Wall -fPIC --shared -o libjbigdec.so jbigdec.cc JBigDecode.cc\ncc -Wall `pkg-config --cflags jbig2dec` -fPIC -shared -o libjbig2codec.so decode_jbig2data_x.cc `pkg-config --libs jbig2dec`\n```\n\n**NOTE（zombie110year,2021/04/20）**：现在可以使用 `python build.py` 指令来编译链接库了。并且源代码和输出文件的路径移动到了 `caj2pdf/dep` 之中，和上面的命令不同。\n\n1. 默认使用 libpoppler 作为依赖编译：\n\n```sh\npython build.py\n```\n\n2. 或者，使用 jbig2dec 作为依赖编译：\n\n```sh\nLIBJBIG2DEC=1 python build.py\n```\n\n**关于两种格式文件结构的分析进展和本项目的实现细节，请查阅[项目 Wiki](https://github.com/JeziL/caj2pdf/wiki)。**\n\n## How to contribute\n\n受测试样本数量所限，即使转换 CAJ 格式的文件也可能（或者说几乎一定）存在 Bug。如遇到这种情况，欢迎在 [Issue](https://github.com/JeziL/caj2pdf/issues) 中提出，**并提供可重现 Bug 的 caj 文件**——可以将样本文件上传到网盘等处<del>，也可直接提供知网链接</del>（作者已滚出校园网，提 issue 请提供可下载的 caj 文件）。\n\n如果你对二进制文件分析、图像/文字压缩算法、逆向工程等领域中的一个或几个有所了解，欢迎帮助完善此项目。你可以从阅读[项目 Wiki](https://github.com/JeziL/caj2pdf/wiki) 开始，看看是否有可以发挥你特长的地方。**Pull requests are always welcome**.\n\n## License\n\n本项目基于 [GLWTPL](https://github.com/me-shaon/GLWTPL)  (Good Luck With That Public License) 许可证开源。\n",
    'author': 'Hin-Tak Leung',
    'author_email': 'htl10@users.sourceforge.net',
    'maintainer': 'zombie110year',
    'maintainer_email': 'zombie110year@outlook.com',
    'url': 'https://github.com/zombie110year/caj2pdf-restructured/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
