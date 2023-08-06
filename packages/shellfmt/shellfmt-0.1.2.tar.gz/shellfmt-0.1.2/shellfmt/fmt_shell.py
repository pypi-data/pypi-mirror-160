#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'


'''
格式化.sh文件，使之可在linux环境下运行；

'''
import argparse
import sys
import os


def getAllFiles_Generator (workpath, fileExt=[]):
    '''
    # 使用生成器遍历目录下指定扩展名的文件
    # get all files in a folder, include subfolders
    # fileExt: ['png','jpg','jpeg']
    # return: 
    #    return a Generator ,include all files , like ['./a/abc.txt','./b/bb.txt']
    '''
    try:
        if os.path.isdir(workpath):
            #if workpath[-1] != '/': workpath+='/'
            for dirname in os.listdir(workpath):
                file_path = os.path.join(workpath, dirname)
                if os.path.isfile( file_path ):
                    if fileExt:
                        ext = os.path.splitext(dirname)[1][1:]
                        if ext in fileExt:
                           yield file_path
                    else:
                        yield file_path
                if os.path.isdir( file_path ):
                    yield from getAllFiles_Generator(file_path, fileExt)
        elif os.path.isfile(workpath):
            yield workpath
    except Exception as e :
        # print(e)
        pass

def format_shell(fname):
    '''
    单个文件格式化处理
    '''
    try:
        with open(fname, 'r', encoding='gbk') as f:  
            txt = f.read()
    except Exception as e:
        return 

    txt = bytes(txt, encoding='gbk')
    txt = txt.replace(b'\r', b'')
    with open(fname, 'wb') as f:
        f.write(txt)

def main():
    parser = argparse.ArgumentParser(description='.SH文件格式化工具')
    parser.add_argument('--fname', default='', required=True, type=str, help="目录或者文件名")
    args = parser.parse_args()
    fname = args.fname
    if os.path.isdir(fname):
        # 目录
        for filename in getAllFiles_Generator(fname, ['sh']):
            print('正在处理:%s'%filename, end='')
            format_shell(filename)
            print('...done!')

    if os.path.isfile(fname):
        # 单个文件处理
        format_shell(fname)
        print('已处理文件：%s'% fname)

    print('all done!')

if __name__ == '__main__':
    main()


'''
usage:
python fmt_shell.py --fname=./test

python fmt_shell.py --fname=test.sh
python fmt_shell.py --fname=start_new_tecclass_nnsvr_dev.sh
python fmt_shell.py --fname=F:\project\成果采集数据技术领域分类模型\publish
'''

