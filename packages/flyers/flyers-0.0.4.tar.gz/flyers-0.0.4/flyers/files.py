import os
import shutil


class FileSizeUnit(object):
    B = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4
    PB = 5


def read_file(filename: str) -> str:
    with open(filename, encoding='utf-8') as f:
        return f.read()


def read_lines(filename: str) -> list[str]:
    with open(filename, encoding='utf-8') as f:
        return f.readlines()


def read_and_splitlines(path: str) -> list[str]:
    with open(path, encoding='utf-8') as f:
        return f.read().splitlines()


def write_file(filename: str, data: str):
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(data)


def update_file(filename: str, func):
    data = read_file(filename)
    new_data = func(data)
    write_file(filename, new_data)


def get_md5(path) -> str:
    files_md5 = os.popen('md5 %s' % path).read().strip()
    file_md5 = files_md5.replace('MD5 (%s) = ' % path, '')
    return file_md5


def copy_dir(src, dst):
    for files in os.listdir(src):
        name = os.path.join(src, files)
        back_name = os.path.join(dst, files)
        if os.path.isfile(name):
            if os.path.isfile(back_name):
                if get_md5(name) != get_md5(back_name):
                    shutil.copy(name, back_name)
            else:
                shutil.copy(name, back_name)
        else:
            if not os.path.isdir(back_name):
                os.makedirs(back_name)
            copy_dir(name, back_name)


def get_file_size(path: str, unit: int) -> float:
    size_units = FileSizeUnit.__dict__
    if unit not in size_units.values():
        raise TypeError('No supports this unit')

    size = os.path.getsize(path)
    for i in range(unit):
        size = size / float(1024)

    return size
