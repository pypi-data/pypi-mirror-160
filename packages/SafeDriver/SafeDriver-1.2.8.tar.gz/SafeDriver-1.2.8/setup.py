import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="SafeDriver",    # 包名
    version="1.2.8",  # 版本
    author="测码范晔",   # 作者
    author_email="1538379200@qq.com",    # 邮箱
    description="自动检测并更新driver文件，提高selenium代码的稳定性",
    long_description=long_description,  # 长介绍，为编写的README
    long_description_content_type="text/markdown",  # 使用介绍文本
    url="",     # github等项目地址
    packages=setuptools.find_packages(),    # 自动查找包，手动写也可
    install_requires=['selenium', 'bs4', 'requests', 'lxml'],    # 安装此包所需的依赖，没有为空
    # entry_points={
    #     'console_scripts': [        # 命令行运行代码,如不需要，可以把entry_points这段删除
    #         'pypi-up=pypk.main:run'
    #     ],
    # },
    classifiers=(       # 其他的配置项
        "Programming Language :: Python :: 3",      # 限制pytest编程语言，版本为3
        "License :: OSI Approved :: MIT License",   # 使用MIT的开源协议(手动添加协议后修改此项)
        "Operating System :: OS Independent",   # 系统要求
    ),
)