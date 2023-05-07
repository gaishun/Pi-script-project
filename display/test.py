import datetime
import os
import fnmatch
import numpy as np
import cv2
import fitz  # fitz就是pip install PyMuPDF
import PyPDF2


def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        print('matmatmatmatmatmatmatmatmatmatmatmatmatmatmatmatmatmatmatmatmat')
        print(mat)
        print('pixpixpixpixpixpixpixpixpixpixpixpixpixpixpixpixpixpixpixpix')
        print(pix)
        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.save(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

        return 

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)




def ReadSaveAddr(rootDir,dir,Strb):

    # imgPath = rootDir+dir  #原始图片位置
    imgPath = rootDir  #原始图片位置
    imgStorePath = imgPath + '_BMP/'  # 存储路径

    a_list = fnmatch.filter(os.listdir(imgPath),Strb)

    if (not os.path.exists(imgStorePath)):
        os.makedirs(imgStorePath) #创建目录

        for i in range(len(a_list)):
            path = imgPath+'/'+a_list[i]
            # 开始读取
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
			# 直接调用.tofile(_path),我这里显示权限拒绝，所用系统自带的文件写入
            img_encode = cv2.imencode('.bmp',img)[1]

            t = a_list[i]
            t = t[:-4] #拿到图片名

            with open(imgStorePath + t + '.bmp', 'wb') as f: #写入
                f.write(img_encode)
            
            return



def split(page, tup):
    page.mediabox.lower_left=(tup[0],tup[1])
    page.mediabox.lower_right=(tup[2],tup[1])
    page.mediabox.upper_left = (tup[0], tup[3])
    page.mediabox.upper_right = (tup[2], tup[3])


def cut_pdf():
    input_file_path ='.\\test\\test.pdf'
    output_file_path = '.\\test\\test-sp.pdf'

    input_file_list = []
    for i in range(4):
        input_file_list.append(PyPDF2.PdfReader(open(input_file_path, 'rb')))
    output_file = PyPDF2.PdfWriter()

    page_info = input_file_list[0].pages[0]
    doc_w = float(page_info.mediabox.width)
    doc_h = float(page_info.mediabox.height)
    page_count = len(input_file_list[0].pages)

    to_split_XYs = [(0,0,400,500), (0,doc_h/2,doc_w/2,doc_h), (doc_w/2,0,doc_w,doc_h/2), (doc_w/2,doc_h/2,doc_w,doc_h)]  # 要分隔的xy坐标
    
    for page_num in range(page_count):
        for i in range(4):
            this_page = input_file_list[i].pages[page_num]
            split(this_page,to_split_XYs[i])
            output_file.add_page(this_page)

    output_file.write(open(output_file_path, 'wb'))



if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = './test/test.pdf'
    # 2、需要储存图片的目录
    imagePath = './test/'
    pyMuPDF_fitz(pdfPath, imagePath)
    rootDir = './test/'
    # 读取该目录下所有的文件夹(png图片)
    dirlist = os.listdir(rootDir)
    for dir in dirlist:
        ReadSaveAddr(rootDir, dir,"*.png")#传入根目录，以及根目录下某文件夹名


