'''
Micro-Python ESP32

把当前文件夹下面所有.py文件移动到另外一个子文件夹下面
'''
import os



def is_folder(fname):
    '''
    根据有没有后缀, 判断是不是文件
    '''
    if len(fname.split('.')) > 1:
        return False
    return True


def mvdir(folder_name):
    file_list = os.listdir(folder_name)
    print
    for fname in file_list:
        if is_folder(fname):
            # 如果是文件夹就跳过
            continue
        try:
            # 重命名
            os.remove(fname, folder_name+'/'+fname)
        except:
            pass

def rmdir(folder_name):
    file_list = os.listdir(folder_name)
    print
    for fname in file_list:
        if is_folder(fname):
            # 如果是文件夹就跳过
            continue
        try:
            # 重命名
            os.remove(folder_name+'/'+fname)
        except:
            pass
    
# 目标文件夹位置
# folder_name = './.Trash-1000/files'

rmdir('./.Trash-1000/files')
rmdir('./.Trash-1000/info')