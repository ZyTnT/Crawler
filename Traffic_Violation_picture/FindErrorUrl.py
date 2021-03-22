import os

def findErrorUrl():
    file = 'C://交通违规图片/不礼让行人'
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            if f == 'download_video_url.txt':
                filePath = os.path.join(root, f)
                newFilePath = os.path.join(root,'newDownloadList.txt')
                with open(filePath, 'r', encoding='utf-8') as old:
                    lines = old.readlines()
                with open(newFilePath,'w',encoding='utf-8') as new:
                    for line in lines:
                        if 'blob:' in line or line == '\n':
                            continue
                        new.write(line)


if __name__ == '__main__':
    findErrorUrl()
