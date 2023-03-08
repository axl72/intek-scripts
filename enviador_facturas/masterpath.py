import os


def get_listdir(path, result=[]):
    list_dir = os.listdir(path)
    list_dir = [os.path.join(path, dir) for dir in list_dir]
    for dir in list_dir:
        if os.path.isdir(dir):
            get_listdir(os.path.join(path, dir), result)
        elif os.path.isfile(dir):
            result.append(os.path.join(path, dir))
    return result
