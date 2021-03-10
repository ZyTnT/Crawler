import os.path
#定义一个函数，path为你的路径
def traversalDir_FirstDir(path):
#定义一个列表，用来存储结果
    list = []
#判断路径是否存在
    totalBrand = os.listdir(path)
    for brand in totalBrand:
        brandPath = os.path.join(path, brand)
        totalType = os.listdir(brandPath)
        for type in totalType:
            typePath = os.path.join(brandPath, type)
            if (os.path.exists(typePath)):
            #获取该目录下的所有文件或文件夹目录
                files = os.listdir(typePath)
                for file in files:
                    #得到该文件下所有目录的路径
                    m = os.path.join(typePath,file)
                    #判断该路径下是否是文件夹
                    if (os.path.isdir(m)):
                        h = os.path.split(m)
                        print(h[1])
                        list.append(h[1])
    return list

path = "F://易车评论照片"
TotalBrandList = traversalDir_FirstDir(path)
print(len(TotalBrandList))