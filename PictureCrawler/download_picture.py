import os
import requests


def main(file):
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'url.txt':
                filepath = os.path.join(root, f)
                download(filepath,root)


def download(filepath,root):
    data = open(filepath,"r",encoding='utf-8')
    print(data)
    n = 0
    for line in data:
        try:
            line = line.replace('\n','')
            line = line.split(", ")

            rootpath = root + "//" + line[1]
            downloadPath = rootpath + "//" + str(n) + ".png"

            if not os.path.exists(rootpath):
                os.makedirs(rootpath)

            if not os.path.exists(downloadPath):
                img = requests.get(line[0], headers={
                    'User-Agent': 'Mozilla/5`.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'})
                with open(downloadPath, "wb") as f:
                    f.write(img.content)
                    n += 1
                    print(n)
            else: break

        except Exception as err:
            print(err)
            continue



file = "F://易车评论照片"
main(file)
