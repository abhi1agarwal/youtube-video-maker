#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sys
from itertools import chain

from imagerobot import ImageRobot
from searchrobot import SearchRobot
from videorobot import VideoRobot
from uploadrobot import UploadRobot
from urllib.error import HTTPError


def make_project_directory(search_term):
    try:
        search_term = search_term.replace(" ", "_")
        directory_path = os.path.expanduser("~") + "/{}".format(search_term)
        print("directory Path chosen" + directory_path)
        os.mkdir(directory_path)

        return directory_path
    except OSError as ex:
        print("Creation of the project directory failed." + str(ex))
        sys.exit(1)


if __name__ == "__main__":
    search_term = input("Wikipedia search term: ")
    if len(search_term) == 0:
        print("Please enter a search term.")
        sys.exit(1)

    print("Avaiable prefixes:\n1. What is\n2. Who is\n3. The history of\n4. Learn more about")
    prefixes = ["What is", "Who is", "The history of", "Learn more about"]
    prefix = input("Prefix: ")
    if not prefix in "1234":
        print("Please enter a prefix.")
        sys.exit(1)

    project_directory = make_project_directory(search_term)
    prefix = prefixes[int(prefix) - 1]

    print("[*] Starting search robot...")
    search_robot = SearchRobot()
    search_result = search_robot.search(search_term)
    keywords_list = search_robot.get_keywords(search_result)
    for i in range(len(search_result)):
        print("[*] Sentence {0}: {1}".format(i + 1, search_result[i]))
        print("[*] Keywords: {0}\n".format(keywords_list[i]))

    print("[*] Starting image robot...")
    image_robot = ImageRobot(project_directory)
    images_list = []
    keywords_list_cleansed = []
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789')
    for keywords in keywords_list:
        img = image_robot.get_image(keywords, search_term)
        images_list.append(img)
        print("[*] Image saved in: " + str(img))
        for keyword in keywords:
            keywords_list_cleansed.append(''.join(filter(whitelist.__contains__, keyword)))

    print("[*] Renaming images...")
    print("[DIG]" "PRE Image List is " + str(images_list))
    images_list = image_robot.rename_files(images_list)
    print("[DIG]" "POST Image List is " + str(images_list))
    print("[*] Converting images to JPG...")
    image_robot.convert_to_jpg(images_list)

    print("[*] Starting video robot...")
    print("[DIG]" "Project directory " + str(project_directory))
    print("[DIG]" "Search result " + str(search_result))
    print("[DIG] Image list size " + str(len(images_list)) + " search results size " + str(len(search_result)))
    video_robot = VideoRobot(project_directory, len(images_list))
    video_robot.make_video()
    video_robot.add_subtitles(search_result)
    video_robot.add_music()

    print("[*] Starting upload robot...")
    upload_robot = UploadRobot()

    title = prefix + " " + search_term
    description = "\n\n".join(search_result).strip()
    description.replace("<", "")
    description.replace(">", "")
    keywords = ",".join(keywords_list_cleansed[:10]).strip()

    args = argparse.Namespace(
        auth_host_name="localhost",
        auth_host_port=[8080, 8090],
        category="27",
        description=description,
        file="{}/final_video.mp4".format(project_directory),
        keywords=keywords,
        logging_level="ERROR",
        noauth_local_webserver=False,
        privacy_status="public",
        title=title)

    youtube = upload_robot.get_authenticated_service(args)

    print("[*] Uploading video... with args " + str(args))
    try:
        upload_robot.initialize_upload(youtube, args)
    except HTTPError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    print("[*] Backup files saved in: " + project_directory)
