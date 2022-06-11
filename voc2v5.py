# coding=utf-8
"""
@Time: 2020/9/17 9:07
@IDE: PyCharm
@Author: chengzhang
@File: voc2v5.py
"""
import os
import glob
from tqdm import tqdm
import xml.etree.ElementTree as ET
import shutil
import argparse
from random import shuffle
import cv2


def check_x_y_w_h(norm_x, norm_y, norm_w, norm_h):
    norm_x = 0.00001 if norm_x <= 0 else norm_x
    norm_x = 0.99999 if norm_x >= 1 else norm_x
    norm_y = 0.00001 if norm_y <= 0 else norm_y
    norm_y = 0.99999 if norm_y >= 1 else norm_y
    norm_w = 0.00001 if norm_w <= 0 else norm_w
    norm_w = 0.99999 if norm_w >= 1 else norm_w
    norm_h = 0.00001 if norm_h <= 0 else norm_h
    norm_h = 0.99999 if norm_h >= 1 else norm_h
    return norm_x, norm_y, norm_w, norm_h


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x, y, w, h = check_x_y_w_h(x, y, w, h)
    return (x, y, w, h)


def write_txt(train_xml, dataset):
    with open(dataset, "w", encoding="utf-8") as f:
        for xml in tqdm(train_xml):
            print(xml)
            f.write(xml.replace('.xml', '.jpg') + '\n')
            target_label_txt = xml.replace('.xml', '.txt')
            img = cv2.imread(xml.replace('.xml', '.jpg'))
            h, w, c = img.shape
            # 输入文件xml
            in_file = open(xml)
            # 输出label txt
            out_file = open(target_label_txt, 'w')
            tree = ET.parse(in_file)
            root = tree.getroot()
            for obj in root.iter('object'):
                try:
                    cls = obj.find('name').text
                except:
                    continue

                if cls not in classes:
                    continue
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                if cls == 'fall':
                    out_file.write(str(0) + " " + " ".join([str(a) for a in bb]) + '\n')
                elif cls == 'stand':
                    out_file.write(str(1) + " " + " ".join([str(a) for a in bb]) + '\n')


def check_dir(dir):
    try:
        shutil.rmtree(dir)
    except:
        os.makedirs(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)


def parse_annotation(img_dir):
    all_imgs = []
    all_xmls = []
    for tmpdir in img_dir:
        for home, dirs, files in os.walk(tmpdir):
            for filename in files:
                # 文件名列表，包含完整路径
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    filePath = os.path.join(home, filename)
                    all_imgs.append(filePath)
                elif filename.endswith(".xml"):
                    filePath = os.path.join(home, filename)
                    all_xmls.append(filePath)

    return all_xmls


if __name__ == '__main__':
    classes = ['fall','stand']

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_txt", default="./data/train_fall.txt")
    parser.add_argument("--test_txt", default="./data/val_fall.txt")

    flags = parser.parse_args()

    imgPathList = [
        "D:/FallDataset/data/FallDataset1/"

    ]

    dataset = parse_annotation(imgPathList)
    shuffle(dataset)
    num = len(dataset)
    trainNum = int(0.9 * num)

    trainList = dataset[: trainNum]
    testList = dataset[trainNum:]

    write_txt(trainList, flags.train_txt)
    write_txt(testList, flags.test_txt)
