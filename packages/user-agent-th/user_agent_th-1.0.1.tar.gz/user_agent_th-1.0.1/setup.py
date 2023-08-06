#!/usr/bin/env python
# coding: utf-8
import setuptools

# 由于最终README.md还涉及到格式转换，暂未处理，因此，未将该文件上传
# with open("README.md", "r", encoding='UTF-8') as fh:
#     long_description = fh.read()

setuptools.setup(
    name="user_agent_th",  # 包的分发名称，使用字母、数字、_、-
    version="1.0.1",  # 版本号, 每次上传到PyPI后，版本后不再运行重复，版本号规范：https://www.python.org/dev/peps/pep-0440/
    author="xddmmm",  # 作者名字
    author_email="3163450460@qq.com",  # 作者邮箱
    description="user_agent",  # 包的简介描述
    # long_description=long_description,     # 包的详细介绍(一般通过加载README.md)
    # long_description_content_type="text/markdown", # 和上条命令配合使用，声明加载的是markdown文件
    url="",  # 项目开源地址
    packages=setuptools.find_packages(),
    # 包含在发布软件包文件中的可被import的python包文件。如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包
    include_package_data=True,  # 打包包含静态文件标识！！上传静态数据时有用
    classifiers=[  # 关于包的其他元数据(metadata)
        "License :: OSI Approved :: MIT License",  # 根据MIT许可证开源
        "Operating System :: OS Independent",  # 与操作系统无关
    ],
)
