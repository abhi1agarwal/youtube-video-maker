#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class VideoRobot():

    def __init__(self, project_directory, num):
        self.images_directory = project_directory
        self.num = num
        self.space = 12.5
        self.subtitles_template = """
{0}
{1}:{2}:{3},{4} --> {5}:{6}:{7},{8}
{{{9}}}
        
"""
        self.template_out = ""
        for i in range(1, int(num) + 1):
            st = (i-1) * self.space
            en = i*self.space
            st_hh = int(int(st)/60/60)
            st_mm = int(int(st)/60) - 60*st_hh
            st_ss = int(int(st) - (st_hh*60*60 + st_mm*60))
            st_mili = int((st - int(st))*1000)
            en_hh = int(int(en) / 60 / 60)
            en_mm = int(int(en) / 60) - 60 * en_hh
            en_ss = int(int(en) - (en_hh * 60 * 60 + en_mm * 60))
            en_mili = int((en - int(en))*1000)
            thisOne = self.subtitles_template.format(i, str(st_hh).zfill(2), str(st_mm).zfill(2), str(st_ss).zfill(2),
                                                     str(st_mili).zfill(3), str(en_hh).zfill(2), str(en_mm).zfill(2),
                                                     str(en_ss).zfill(2), str(en_mili).zfill(3), str(i-1))
            self.template_out = self.template_out + thisOne

    def make_video(self):
        command = "cat {0}/*.jpg | ffmpeg -y -framerate 0.08 -f image2pipe -i - -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" {0}/output_imgs.mp4".format(self.images_directory)
        os.system(command)

    def add_subtitles(self, sentences):
        self.template_out = self.template_out.format(*sentences)

        with open("{0}/subtitles.srt".format(self.images_directory), "w") as subtitles_file:
            subtitles_file.write(self.template_out)

        os.system("ffmpeg -y -i {0}/output_imgs.mp4 -vf subtitles={0}/subtitles.srt {0}/output_text.mp4".format(
            self.images_directory))

    def add_music(self):
        os.system("ffmpeg -y -i {0}/output_text.mp4 -i bensound-ukulele.mp3 "
                  "-c copy -map 0:v:0 -map 1:a:0 {0}/final_video.mp4".format(self.images_directory))
