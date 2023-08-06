from distutils.core import setup

setup(
    name="hukeSuperMath",     #对外模块名称
    version="1.0",       #版本号
    description="这是对外发布的第一个模块，里面只有数学方法，仅用于测试",       #描述
    author="胡科",         #作者
    author_email="948799942@qq.com",        #作者邮箱
    py_modules=["hukeSuperMath.demo1","hukeSuperMath.demo2"]            #要发布的模块
)