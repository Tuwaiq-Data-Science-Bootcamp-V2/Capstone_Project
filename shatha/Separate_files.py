#!/usr/bin/env python
# coding: utf-8

# In[420]:


import pandas as pd


# In[421]:


import os
from os import listdir
import shutil

def file_content(filename):
    folder_dir = "/Users/shatha_95/Desktop/{}".format(filename) # change path
    list1=[]
    for images in os.listdir(folder_dir):
        if images.endswith(".jpg") or images.endswith(".JPG"):
            list1.append(images)
    return list1


def add_images(first_filename,second_filename,directory,list_img_org_name):
    folder_dir = "/Users/shatha_95/Desktop/{}".format(first_filename) # change path
    parent_dir = "/Users/shatha_95/Desktop/{}".format(second_filename) # change path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    parent_dir2="/Users/shatha_95/Desktop/{}/".format(second_filename)+directory # change path
    for j in list_img_org_name:
        shutil.move(folder_dir+'/'+j, parent_dir2)


