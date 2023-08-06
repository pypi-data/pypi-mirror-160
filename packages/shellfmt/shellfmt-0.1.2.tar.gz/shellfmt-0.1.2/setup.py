#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'


import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 导入静态文件
file_data = []

setuptools.setup(
    name='shellfmt',
    version='0.1.2',
    description='format .sh file',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='shell file(.sh) formt tool',
    install_requires=[],
    packages=setuptools.find_packages(),
    include_package_data = True,
    author='He xi',
    author_email='xmhexi@qq.com',
    url='https://github.com/xmxoxo/',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 5 - Production/Stable',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: OSI Approved :: MIT License',  # 模块的license

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={  # 项目相关的额外链接
        'Blog': 'https://blog.csdn.net/xmxoxo',
    },
    entry_points={
        'console_scripts': [
            'shellfmt = shellfmt.fmt_shell:main',
            ]
        }
)

