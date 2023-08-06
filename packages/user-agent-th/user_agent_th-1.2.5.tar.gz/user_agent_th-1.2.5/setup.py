# #!/usr/bin/env python
# # coding: utf-8
# import setuptools
#
# # 由于最终README.md还涉及到格式转换，暂未处理，因此，未将该文件上传
# # with open("README.md", "r", encoding='UTF-8') as fh:
# #     long_description = fh.read()
#
# setuptools.setup(
#     name="user_agent_th",  # 包的分发名称，使用字母、数字、_、-
#     version="1.0.3",  # 版本号, 每次上传到PyPI后，版本后不再运行重复，版本号规范：https://www.python.org/dev/peps/pep-0440/
#     author="xddmmm",  # 作者名字
#     author_email="3163450460@qq.com",  # 作者邮箱
#     description="user_agent",  # 包的简介描述
#     # long_description=long_description,     # 包的详细介绍(一般通过加载README.md)
#     # long_description_content_type="text/markdown", # 和上条命令配合使用，声明加载的是markdown文件
#     url="",  # 项目开源地址
#     packages=['th_random_ua'],
#     # 包含在发布软件包文件中的可被import的python包文件。如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包
#     include_package_data=True,  # 打包包含静态文件标识！！上传静态数据时有用
#     classifiers=[  # 关于包的其他元数据(metadata)
#         "License :: OSI Approved :: MIT License",  # 根据MIT许可证开源
#         "Operating System :: OS Independent",  # 与操作系统无关
#     ],
# )
from setuptools import setup, find_packages

setup(name='user_agent_th',  # 打包后的包文件名
      version='1.2.5',  # 版本号
      description='aaaaaaa',  # 说明
      long_description="爬虫组ua",  # 详细说明
      license="MIT Licence",  # 许可
      url='',
      author='',
      author_email='',
      packages=find_packages(),  # 这个参数是导入目录下的所有__init__.py包
      include_package_data=True,
      platforms="any",
      install_requires=[],  # 引用到的第三方库
      # py_modules=['pip-test.DoRequest', 'pip-test.GetParams', 'pip-test.ServiceRequest',
      #             'pip-test.ts.constants', 'pip-test.ac.Agent2C',
      #             'pip-test.ts.ttypes', 'pip-test.ac.constants',
      #             'pip-test.__init__'],  # 你要打包的文件，这里用下面这个参数代替
      # packages=[''] # 这个参数是导入目录下的所有__init__.py包
      )
