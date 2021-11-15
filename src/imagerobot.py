#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from shutil import copyfile
from google_images_download import google_images_download
from PIL import Image
import random


class ImageRobot():

    def __init__(self, project_directory):
        self.response = google_images_download.googleimagesdownload()
        self.download_directory = project_directory

    def get_image(self, keywords, master_key):
        keywords = " and ".join(keywords) + " and " + master_key
        arguments = {"keywords": keywords, "limit": 3, "print_urls": True,
                     "no_directory": True, "size": "large", 'aspect_ratio': 'wide',
                     "output_directory": self.download_directory}

        ret = self.response.download(arguments)
        choice_num = random.randint(0, len(ret[0][keywords]) - 1)
        print("return value " + str(ret) + " choice " + str(choice_num))
        return [ret[0][keywords][choice_num]]

    def rename_files(self, files):
        new_files_list = []
        for i in range(len(files)):
            try:
                new_name = "{0}/img{1}".format(self.download_directory, str(i).zfill(3))
                copyfile(files[i][0], new_name)
                new_files_list.append(new_name)
            except OSError as ex:
                print("Exception while renaming " + str(files[i]) + " : " + str(ex))
                raise ex

        return new_files_list

    def convert_to_jpg(self, files):
        for f in files:
            img = Image.open(f)
            rgb_img = img.convert("RGB")
            rgb_img.save(f + ".jpg")
