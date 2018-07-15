import os
import shutil


def Test1(rootDir):
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for f in files:
            shutil.move(os.path.join(root, f), "./corpora_raw/" + f)


Test1("./corpora_raw")
