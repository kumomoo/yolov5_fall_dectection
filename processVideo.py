# coding=utf-8
"""
@Time: 2021/3/9 10:23
@IDE: PyCharm
@Author: chengzhang
@File: processVideo.py
"""
import os
from tqdm import tqdm
import cv2
from xml.dom.minidom import Document

count = 4459


def process(fileDir):
    dataset = [os.path.join(fileDir, i) for i in os.listdir(fileDir)]

    for dir in dataset:
        Annotation = os.path.join(dir, "Annotation_files")
        Annotations = [os.path.join(Annotation, i) for i in os.listdir(Annotation)]
        for ann in tqdm(Annotations):
            txt = open(ann).readlines()
            if len(txt[0].split(',')) < 2:
                videoPath = ann.replace('Annotation_files', 'Videos').replace('.txt', '.avi')
                start, end = int(txt[0].replace('\n', '')), int(txt[1].replace('\n', ''))
                video(videoPath, txt, start, end)


def video(videoPath, txt, start, end):
    global count
    vs = cv2.VideoCapture(videoPath)
    ind = 1

    while True:
        success, frame = vs.read()
        if frame is None:
            break
        if ind >= 6 and ind < start-5 :
            if int(txt[ind].split(',')[1]) ==1:
                Jpg = '{:06d}.jpg'.format(count)
                outPutJpg = os.path.join(save, Jpg)
                outPutXML = outPutJpg.replace('jpg', 'xml')
                cv2.imwrite(outPutJpg, frame)
                count += 1
                imgShape = frame.shape
                info = txt[ind].replace('\n', '').split(',')
                _, _, xmin, ymin, xmax, ymax = info
                bboxsInfo = [[int(xmin), int(ymin), int(xmax), int(ymax)]]
                bbox2xml(bboxsInfo, imgShape, Jpg, outPutXML)
        ind += 1

def bbox2xml(bboxsInfo, imgShape, outPutJpg, outPutXML):
    # for boxInfo in bboxsInfo:
    xmlBuilder = Document()
    annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
    xmlBuilder.appendChild(annotation)
    Pheight, Pwidth, Pdepth = imgShape

    folder = xmlBuilder.createElement("folder")  # folder标签
    folderContent = xmlBuilder.createTextNode("VOC2007")
    folder.appendChild(folderContent)
    annotation.appendChild(folder)

    filename = xmlBuilder.createElement("filename")  # filename标签
    filenameContent = xmlBuilder.createTextNode(outPutJpg)
    filename.appendChild(filenameContent)
    annotation.appendChild(filename)

    size = xmlBuilder.createElement("size")  # size标签
    width = xmlBuilder.createElement("width")  # size子标签width
    widthContent = xmlBuilder.createTextNode(str(Pwidth))
    width.appendChild(widthContent)
    size.appendChild(width)
    height = xmlBuilder.createElement("height")  # size子标签height
    heightContent = xmlBuilder.createTextNode(str(Pheight))
    height.appendChild(heightContent)
    size.appendChild(height)
    depth = xmlBuilder.createElement("depth")  # size子标签depth
    depthContent = xmlBuilder.createTextNode(str(Pdepth))
    depth.appendChild(depthContent)
    size.appendChild(depth)
    annotation.appendChild(size)

    for bbox in bboxsInfo:
        label = "stand"
        box_xmin, box_ymin, box_xmax, box_ymax = bbox

        object = xmlBuilder.createElement("object")
        picname = xmlBuilder.createElement("name")
        nameContent = xmlBuilder.createTextNode(label)
        picname.appendChild(nameContent)
        object.appendChild(picname)
        pose = xmlBuilder.createElement("pose")
        poseContent = xmlBuilder.createTextNode("Unspecified")
        pose.appendChild(poseContent)
        object.appendChild(pose)
        truncated = xmlBuilder.createElement("truncated")
        truncatedContent = xmlBuilder.createTextNode("0")
        truncated.appendChild(truncatedContent)
        object.appendChild(truncated)
        difficult = xmlBuilder.createElement("difficult")
        difficultContent = xmlBuilder.createTextNode("0")
        difficult.appendChild(difficultContent)
        object.appendChild(difficult)

        bndbox = xmlBuilder.createElement("bndbox")
        xmin = xmlBuilder.createElement("xmin")
        xminContent = xmlBuilder.createTextNode(str(box_xmin))
        xmin.appendChild(xminContent)
        bndbox.appendChild(xmin)
        ymin = xmlBuilder.createElement("ymin")
        yminContent = xmlBuilder.createTextNode(str(box_ymin))
        ymin.appendChild(yminContent)
        bndbox.appendChild(ymin)
        xmax = xmlBuilder.createElement("xmax")
        xmaxContent = xmlBuilder.createTextNode(str(box_xmax))
        xmax.appendChild(xmaxContent)
        bndbox.appendChild(xmax)
        ymax = xmlBuilder.createElement("ymax")
        ymaxContent = xmlBuilder.createTextNode(str(box_ymax))
        ymax.appendChild(ymaxContent)
        bndbox.appendChild(ymax)
        object.appendChild(bndbox)

        annotation.appendChild(object)
    f = open(outPutXML, 'w')
    xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')

    f.close()


if __name__ == '__main__':
    fileDir = r"D:\FallDataset\dataset"  # 源数据集路径
    save = r"D:\FallDataset\FallDataset2"  # 保存voc格式路径
    process(fileDir)
