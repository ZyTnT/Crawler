import os.path
import shutil


def DeleteErrorDir(path):
    totalBrand = os.listdir(path)
    for brand in totalBrand:
        brandPath = os.path.join(path, brand)
        totalType = os.listdir(brandPath)
        for Type in totalType:
            typePath = os.path.join(brandPath, Type)
            files = os.listdir(typePath)
            for file in files:
                m = os.path.join(typePath, file)
                if "æ¬¾" in m:
                    shutil.rmtree(m)
                    print(m)


def FindError(path):
    data = open(path, 'r', encoding='utf-8')
    for line in data:
        if 'æ¬¾' in line:
            print(line.replace('\n', ''))



path = 'C://Users\甄雨桐\Desktop\车款名单.txt'
FindError(path)