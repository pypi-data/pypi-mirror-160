from setuptools import find_packages, setup

setup(
    name='RuirenyunLibrary',
    version='1.1.5',
    author='tangyi',
    description="瑞人科技自动化测试框架核心库",
    url="http://team.ruirenyun.tech/",
    license="LGPL",
    packages=find_packages(),
    author_email='314666979@qq.com',
    py_modules=["RuirenyunLibrary.MysqlDB","RuirenyunLibrary.PublicLibrary"],
    install_requires = ["selenium","requests","robotframework","PyYAML","PyMySQL","python-dateutil","robotframework-seleniumlibrary"],
    package_dir  = {'.': 'RuirenyunLibrary'},
    package_data = {'RuirenyunLibrary': ["*.robot"]},
)