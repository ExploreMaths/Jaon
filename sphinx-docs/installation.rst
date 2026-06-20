安装与部署
==========

Helios 支持多种使用方式：从源码安装、通过 pip 安装、使用独立可执行文件，
以及通过 Windows 安装程序关联 ``.helios`` 文件。

从源码安装
----------

.. code-block:: bash

    git clone https://github.com/ExploreMaths/Helios.git
    cd helios
    pip install -e .

安装完成后即可使用 ``python -m helios`` 或 ``helios`` 命令。

安装开发依赖
------------

.. code-block:: bash

    pip install -e .[dev,docs]

这会自动安装 Nuitka（构建独立 exe）和 Sphinx/Furo（构建文档）。

Windows 独立可执行文件
----------------------

如果你不想安装 Python，可以直接使用 ``compiler.exe``：

.. code-block:: bash

    python scripts/build_exe.py

生成的 ``dist/compiler.exe`` 不依赖 Python 环境。

Windows 安装程序（双击运行 .helios）
-------------------------------------

方法一：PowerShell 安装
~~~~~~~~~~~~~~~~~~~~~~~

以管理员身份运行 PowerShell：

.. code-block:: powershell

    cd installer
    powershell -ExecutionPolicy Bypass -File install.ps1

安装后：

- 双击任意 ``.helios`` 文件即可执行
- 右键菜单出现 "Run with Helios"
- ``compiler.exe`` 添加到用户 PATH

方法二：Inno Setup 安装包
~~~~~~~~~~~~~~~~~~~~~~~~~

1. 安装 `Inno Setup <https://jrsoftware.org/isinfo.php>`_。

2. 编译安装包：

   .. code-block:: bash

       iscc installer/setup.iss

3. 运行生成的 ``dist/Helios-Setup.exe``。

卸载
----

PowerShell 安装版：

.. code-block:: powershell

    cd installer
    powershell -ExecutionPolicy Bypass -File uninstall.ps1

Inno Setup 安装版：通过控制面板的 "程序和功能" 卸载。
