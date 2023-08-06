import setuptools

setuptools.setup(
    name="RhinoAccum1",  # 模块名称
    version="1.1",  # 当前版本
    author="Rhinozh",  # 作者
    author_email="Rhinozh@163.com",  # 作者邮箱
    description="too simple",  # 模块简介
    long_description="long_description",  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://github.com/wupeiqi/fucker",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'numpy',
    ],
    python_requires='>=3',
)