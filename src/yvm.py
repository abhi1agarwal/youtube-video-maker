#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from urllib.error import HTTPError

from imagerobot import ImageRobot
from searchrobot import SearchRobot
from uploadrobot import UploadRobot
from videorobot import VideoRobot


def make_project_directory(search_term):
    try:
        search_term = search_term.replace(" ", "_")
        directory_path = os.path.expanduser("~") + "/cold_play/{}".format(search_term)
        print("directory Path chosen  : " + directory_path)
        os.makedirs(directory_path, exist_ok=True)

        return directory_path
    except OSError as ex:
        print("Creation of the project directory failed." + str(ex))
        sys.exit(1)


class VideoMaker:
    def __init__(self, stuff, prefix="what is", suffix="", suggested_keywords=""):
        self.stuff = self.search_term = str(stuff)
        self.prefix = prefix
        self.suffix = suffix
        self.suggested_keywords = suggested_keywords
        self.project_directory = make_project_directory(self.stuff)
        self.video_robot = VideoRobot(self.project_directory)  # len(images_list)
        self.image_robot = ImageRobot(self.project_directory)
        self.search_robot = SearchRobot()
        self.search_result = []
        self.keywords_list_cleansed = []
        self.upload_robot = UploadRobot()
        self.title = (self.prefix + " " + self.search_term).strip()
        self.is_video_made = False
        self.is_video_uploaded = False
        self.final_vide_file_name = "{}/final_video.mp4".format(self.project_directory)

    def make_video(self):
        print("[*] Starting search robot...")
        self.search_result = self.search_robot.search(self.search_term + " " + self.suffix)
        keywords_list = self.search_robot.get_keywords(self.search_result)
        for i in range(len(self.search_result)):
            print("[*] Sentence {0}: {1}".format(i + 1, self.search_result[i]))
            print("[*] Keywords: {0}\n".format(keywords_list[i]))

        print("[*] Starting image robot...")
        images_list = []
        self.keywords_list_cleansed = []
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789')
        for keywords in keywords_list:
            img = self.image_robot.get_image(keywords, self.search_term + " " + self.suffix)
            images_list.append(img)
            print("[*] Image saved in: " + str(img))
            for keyword in keywords:
                self.keywords_list_cleansed.append(''.join(filter(whitelist.__contains__, keyword)))

        print("[*] Renaming images...")
        print("[DIG]" "PRE Image List is " + str(images_list))
        images_list = self.image_robot.rename_files(images_list)
        print("[DIG]" "POST Image List is " + str(images_list))
        print("[*] Converting images to JPG...")
        self.image_robot.convert_to_jpg(images_list)

        print("[*] Starting video robot...")
        print("[DIG]" "Project directory " + str(self.project_directory))
        print("[DIG]" "Search result " + str(self.search_result))
        print("[DIG] Image list size " + str(len(images_list)) + " search results size " + str(len(self.search_result)))

        self.video_robot.make_video()
        self.video_robot.add_subtitles(self.search_result, len(images_list))
        self.video_robot.add_music()
        self.is_video_made = os.path.exists(self.final_vide_file_name)

    def upload_video(self):
        print("[*] Starting upload robot...")

        if not self.is_video_made:
            raise Exception("Video is not found in the required place... Please check if it has been created")

        description = ("\n\n".join(self.search_result)).strip()
        description.replace("<", "")
        description.replace(">", "")
        keywords = ",".join(self.keywords_list_cleansed[:10]).strip()
        if len(self.suggested_keywords.strip()) > 0:
            keywords = str(self.suggested_keywords)

        args = argparse.Namespace(
            auth_host_name="localhost",
            auth_host_port=[8080, 8090],
            category="27",
            description=description,
            file=self.final_vide_file_name,
            keywords=keywords,
            logging_level="ERROR",
            noauth_local_webserver=False,
            privacy_status="public",
            title=self.title)

        youtube = self.upload_robot.get_authenticated_service(args)

        print("[*] Uploading video... with args " + str(args))
        try:
            self.upload_robot.initialize_upload(youtube, args)
            self.is_video_uploaded = True
        except HTTPError as e:
            print("An HTTP error occurred:\n%s" % (str(e)))

        print("[*] Backup files for " + self.search_term + " saved in: " + self.project_directory)
        print("[*] self object " + str(self))
        print("[*] Outcome of upload " + str(self.is_video_uploaded))


if __name__ == "__main__":
    class Blah:
        def __init__(self):
            pass

        @staticmethod
        def blast_off():
            search_term = input("Wikipedia search term: ")
            if len(search_term) == 0:
                print("Please enter a search term.")
                sys.exit(1)

            prefixes = ["What is", "Who is", "The history of", "Learn more about"]
            prefix = input("Prefix: ex. " + str(prefixes))
            suffix = input("Any suffixes? ")
            suggested_keywords = input("Any keywords ? ")
            video_maker = VideoMaker(search_term, prefix=prefix, suffix=suffix, suggested_keywords=suggested_keywords)
            video_maker.make_video()
            video_maker.upload_video()
            print("Was video made ? {0} Was it uploaded ? {1} "
                  .format(video_maker.is_video_made, video_maker.is_video_uploaded))


    kickoff = Blah()
    kickoff.blast_off()

#     project_directory = make_project_directory(search_term)
#
#     print("[*] Starting search robot...")
#     search_robot = SearchRobot()
#     search_result = search_robot.search(search_term + " " + suffix)
#     keywords_list = search_robot.get_keywords(search_result)
#     for i in range(len(search_result)):
#         print("[*] Sentence {0}: {1}".format(i + 1, search_result[i]))
#         print("[*] Keywords: {0}\n".format(keywords_list[i]))
#
#     print("[*] Starting image robot...")
#     image_robot = ImageRobot(project_directory)
#     images_list = []
#     keywords_list_cleansed = []
#     whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789')
#     for keywords in keywords_list:
#         img = image_robot.get_image(keywords, search_term + " " + suffix)
#         images_list.append(img)
#         print("[*] Image saved in: " + str(img))
#         for keyword in keywords:
#             keywords_list_cleansed.append(''.join(filter(whitelist.__contains__, keyword)))
#
#     print("[*] Renaming images...")
#     print("[DIG]" "PRE Image List is " + str(images_list))
#     images_list = image_robot.rename_files(images_list)
#     print("[DIG]" "POST Image List is " + str(images_list))
#     print("[*] Converting images to JPG...")
#     image_robot.convert_to_jpg(images_list)
#
#     print("[*] Starting video robot...")
#     print("[DIG]" "Project directory " + str(project_directory))
#     print("[DIG]" "Search result " + str(search_result))
#     print("[DIG] Image list size " + str(len(images_list)) + " search results size " + str(len(search_result)))
#     video_robot = VideoRobot(project_directory, len(images_list))
#     video_robot.make_video()
#     video_robot.add_subtitles(search_result)
#     video_robot.add_music()
#
# print("[*] Starting upload robot...")
# upload_robot = UploadRobot()
#
# title = prefix + " " + search_term
# description = "\n\n".join(search_result).strip()
# description.replace("<", "")
# description.replace(">", "")
# keywords = ",".join(keywords_list_cleansed[:10]).strip()
#
# args = argparse.Namespace(
#     auth_host_name="localhost",
#     auth_host_port=[8080, 8090],
#     category="27",
#     description=description,
#     file="{}/final_video.mp4".format(project_directory),
#     keywords=keywords,
#     logging_level="ERROR",
#     noauth_local_webserver=False,
#     privacy_status="public",
#     title=title)
#
# youtube = upload_robot.get_authenticated_service(args)
#
# print("[*] Uploading video... with args " + str(args))
# try:
#     upload_robot.initialize_upload(youtube, args)
# except HTTPError as e:
#     print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
#
# print("[*] Backup files saved in: " + project_directory)
