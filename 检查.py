import xml.etree.ElementTree as ET
import os


# 批量修改整个文件夹所有的xml文件
def change_all_xml(xml_path):
    filelist = os.listdir(xml_path)
    #print(filelist)
    # 打开xml文档
    for xmlfile in filelist:
        if xmlfile[-4:]!=".xml":
            continue
        #print(xmlfile[-4:])

        file = os.path.join(xml_path,xmlfile)
        doc = ET.parse(file)
        root = doc.getroot()
        sub1 = root.find('object').find('name')  # 找到filename标签，

        sub1.text = "stand"  # 修改标签内容

        doc.write(file)  # 保存修改


# 修改某个特定的xml文件
def change_one_xml(xml_path):  # 输入的是这个xml文件的全路径
    # 打开xml文档
    doc = ET.parse(xml_path)
    root = doc.getroot()
    sub1 = root.find('filename')  # 找到filename标签，
    sub1.text = '07_205.jpg'  # 修改标签内容
    doc.write(xml_path)  # 保存修改
    print('----------done--------')


# change_all_xml(r'Z:\pycharm_projects\ssd\VOC2007\Annotations')     # xml文件总路径
xml_path = r"D:\FallDataset\data\FallDataset1"
change_all_xml(xml_path)
print("done!")

