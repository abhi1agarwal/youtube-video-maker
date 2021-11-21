#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from shutil import copyfile

from PIL import Image
from google_images_download import google_images_download


class ImageRobot:

    def __init__(self, project_directory):
        self.response = google_images_download.googleimagesdownload()
        self.download_directory = project_directory

    def get_image(self, keywords, master_key):
        keywords = " and ".join(keywords) + " and " + master_key
        arguments = {"keywords": keywords, "limit": 10, "print_urls": True,
                     "no_directory": True, "size": "large", 'aspect_ratio': 'wide',
                     "output_directory": self.download_directory}
        ret = self.response.download(arguments)
        # attempts to ring in a little randomness to avoid duplicates
        choice_num = random.randint(0, min(len(ret[0][keywords]) - 1, 3))
        if len(ret[0][keywords][choice_num]) == 0:
            for i in range(0, len(ret[0][keywords])):
                if len(ret[0][keywords][i]) > 0:
                    choice_num = i
                    break
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

    @staticmethod
    def convert_to_jpg(files):
        for f in files:
            img = Image.open(f)
            rgb_img = img.convert("RGB")
            rgb_img.save(f + ".jpg")
