from distutils.core import setup

setup(
    name='Demo_test521',  # 对外模块的名字
    version='1.0.0',  # 版本号
    description='测试本地发布模块',  # 描述
    author='dgw',  # 作者
    author_email='535646343@qq.com',
    py_modules=['Demo_test521.add', 'Demo_test521.sub'],  # 要发布的模块
)
