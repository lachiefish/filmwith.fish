import glob
from iptcinfo3 import IPTCInfo
from datetime import datetime
import os

globalTags = ['archive']
imageFolderPath = './assets/archive/'
imageFilePaths = glob.glob(imageFolderPath + '*.jpg')

def getDate(info):
    return datetime.strptime(info['date created'].decode('utf-8'), "%Y%m%d").strftime('%Y-%m-%d')

def getCamera(info): # Or film type
    return " ".join(info['object name'].decode('utf-8').split('_')[1:len(info['object name'].decode('utf-8').split('_'))-1])

def getTags(info):
    strlist = [x.decode('utf-8') for x in info['keywords']]
    strlist.extend(globalTags)
    for tag in strlist: # Remove weird tags that were left from lightroom
        if tag[0].isupper():
            strlist.remove(tag)
    return strlist

def chooseFolder(tags):
    if 'people' in tags:
        return 'people/'
    if 'nature' not in tags:
        tags.append('nature')
    return 'nature/'

for imageFilePath in imageFilePaths:
    info = IPTCInfo(imageFilePath)
    date = getDate(info)
    camera = getCamera(info)
    tags = getTags(info)
    isFilm = 'film' in tags
    if not isFilm:
        tags.append('digital')
    mdFolderName = chooseFolder(tags)
    mdFolderPath = './content/work/' + mdFolderName + info['object name'].decode('utf-8') + '.md'
    mdFolderPath.replace('.jpg', '.md')
    
    tagsStr = '\n    - '.join(tags)
    if not os.path.exists(mdFolderPath):
        mdFile = open(mdFolderPath, 'w')
        mdFile.write(f"""---
images:
    - {imageFilePath.replace('./assets','')}
preview: {imageFilePath.replace('./assets','')}
title: {camera}
date: {date}
tags:
    - {tagsStr}
---""")
        mdFile.close()
