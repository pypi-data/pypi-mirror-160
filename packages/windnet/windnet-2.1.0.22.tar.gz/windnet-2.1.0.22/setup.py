# /*
#  * @Author: Guofeng He 
#  * @Date: 2022-05-27 19:56:22 
#  * @Last Modified by:   Guofeng He 
#  * @Last Modified time: 2022-05-27 19:56:22 
#  */

import platform
from sys import argv
from setuptools import setup, find_packages


buildno = 1
try:
    with open("./buildno","r") as fp:
        buildno = int(fp.readline())
except:
    pass
if argv[1]=="sdist":
    try:
        with open("./buildno","w") as fp:
            buildno += 1
            fp.write(str(buildno))
    except:
        pass
    
with open('./README.md', encoding='utf-8') as fp:
    long_description = fp.read()

with open('./requirements.txt', encoding='utf-8') as fp:
    install_requires = fp.readlines() 

if "Windows" in platform.system():
    install_requires.append('pywin32')


setup(
    name="windnet",
    version="2.1.0."+str(buildno),
    author="heguofeng",
    author_email="heguofeng@189.cn",
    description="windnet",
    long_description= long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    python_requires='>3',
    keywords='windnet',
    # 项目主页
    url="http://www.bing.com", 

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包,
    # packages=find_packages(),
    packages=find_packages(include=['windnet']),
    # 数据文件都写在了MANIFEST.in文件中
    include_package_data=True,
     # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    data_files=[
        # ('destdir', ['srcdirfile']),
        ('', ['README.md','requirements.txt',"buildno"]),
               ],

    # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    # 项目的依赖库，读取的requirements.txt内容

    install_requires= install_requires,
    # setup.py 本身要依赖的包，这通常是为一些setuptools的插件准备的配置
    # 这里列出的包，不会自动安装。
    # setup_requires=['pyyaml'],
    # requires=[],

    # 仅在测试时需要使用的依赖，在正常发布的代码中是没有用的。
    # 在执行python setup.py test时，可以自动安装这三个库，确保测试的正常运行。
    tests_require=[
        'pytest>=3.3.1',
        'pytest-cov>=2.5.1',
    ],
    # install_requires 在安装模块时会自动安装依赖包
    # 而 extras_require 不会，这里仅表示该模块会依赖这些包
    # 但是这些包通常不会使用到，只有当你深度使用模块时，才会用到，这里需要你手动安装
    extras_require={
    },
    
     # 用于安装setup_requires或tests_require里的软件包
    # 这些信息会写入egg的 metadata 信息中
    dependency_links=[
        
    ],
    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 foo/main.py 的main 函数
    entry_points={
        'console_scripts': [
            'iproute = windnet.iproute:main',

        ]
    },

    # 将 bin/foo.sh 和 bar.py 脚本，生成到系统 PATH中
    # 执行 python setup.py install 后
    # 会生成 如 /usr/bin/foo.sh 和 如 /usr/bin/bar.py
    # scripts=['client.py']
)



