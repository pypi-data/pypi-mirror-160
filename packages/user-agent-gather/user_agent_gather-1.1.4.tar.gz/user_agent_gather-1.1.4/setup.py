import setuptools
from setuptools import setup

# setup(name='th_random_ua',
#       version='1.1.2',
#       description='随机ua',
#       author='xddmmm',
#       license='MIT',
#       packages=setuptools.find_packages())
# from setuptools import setup, find_packages
#
# setup(
#     name="th_random_ua",  # 包的名称
#     version="1.1.1",  # 版本
#     author="xddmmm",  # 作者名
#     # url = "qiyenull.github.io", 	网站，不是必要，此网站需要存在且未被占用
#     description="随机ua",  # 包的信息说明
#     packages=find_packages("random_ua"),  # 打包时，开始的目录
#     package_dir={"": "random_ua"},  # 告诉 setuptools 包都在 qiye 下
#     package_data={
#         ## 包含 data 文件夹下所有的 *.dat 文件
#         "": [".txt", ".info", "*.properties", ".py"],
#         "": ["data/*.*"],
#     },
#     # 取消所有测试包
#     exclude=["*.test", "*.test.*", "test.*", "test"]
#
# )
from setuptools import setup, find_packages

setup(name='user_agent_gather',  # 打包后的包文件名
      version='1.1.4',  # 版本号
      description='随机ua',  # 说明
      long_description="随机ua",  # 详细说明
      license="MIT Licence",  # 许可
      url='',
      author='wzr',
      author_email='3163450460@qq.com',
      packages=find_packages(),  # 这个参数是导入目录下的所有__init__.py包
      include_package_data=True,
      platforms="any",
      py_modules=["th_random_ua.th_random_ua"],
      install_requires=[""],  # 引用到的第三方库
      # py_modules=['pip-test.DoRequest', 'pip-test.GetParams', 'pip-test.ServiceRequest',
      #             'pip-test.ts.constants', 'pip-test.ac.Agent2C',
      #             'pip-test.ts.ttypes', 'pip-test.ac.constants',
      #             'pip-test.__init__'],  # 你要打包的文件，这里用下面这个参数代替
      # packages=[''] # 这个参数是导入目录下的所有__init__.py包
      )
