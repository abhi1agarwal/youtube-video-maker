#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import gtts


class VideoRobot:

    filename_final_without_subs = "final_video_without_subs.mp4"
    filename_final_withsubs_withmusic_withoutspeech = "final_video.mp4"

    def __init__(self, project_directory):
        self.images_directory = project_directory
        self.num = 0
        self.space = 12.5
        self.audio_file_format = "speech{0}.mp3"
        self.filename_final_without_subs = VideoRobot.filename_final_without_subs
        self.filename_final_withsubs_withmusic_withoutspeech = \
            VideoRobot.filename_final_withsubs_withmusic_withoutspeech
        self.subtitles_template = """
{0}
{1}:{2}:{3},{4} --> {5}:{6}:{7},{8}
{{{9}}}
        
"""
        self.template_out = ""

    def make_speech(self, sentences):
        for idx, item in enumerate(sentences):
            tts = gtts.gTTS(text=item)
            filename = self.audio_file_format.format(str(idx).zfill(3))
            tts.save("{0}/{1}".format(self.images_directory, filename))

    def make_videos_with_speech(self, num):
        for idx in range(num):
            fname_num = str(idx).zfill(3)
            command_template = "ffmpeg -y -i \'{0}/img{1}.jpg\' -i \'{0}/speech{1}.mp3\' " \
                               "-vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2,scale=w=1630:h=1080:eval=init:interl=false:" \
                               "in_range=pc:out_range=tv,setsar=1800/1630\" \'{0}/gen{1}.mp4\'"
            command = command_template.format(self.images_directory, fname_num)
            os.system(command)
        with open('{0}/file.txt'.format(self.images_directory), 'w') as file_concat:
            for idx in range(num):
                fname_num = str(idx).zfill(3)
                file_concat.write("file \'gen{0}.mp4\'\n".format(fname_num))
        command_concat = "ffmpeg -f concat -i \'{0}/file.txt\' {0}/{1}".format(
            self.images_directory, self.filename_final_without_subs)
        os.system(command_concat)

    def make_video(self):
        # Take care of codec and aspect ratio as well as dimensions while generating video
        # https://stackoverflow.com/questions/8133242/ffmpeg-resize-down-larger-video-to-fit-desired-size-and-add-padding
        # http://underpop.online.fr/f/ffmpeg/help/setdar_002c-setsar.htm.gz
        command = "cat {0}/img*.jpg | ffmpeg -y -framerate 0.08 -f image2pipe -i - -vf \"pad=ceil(iw/2)*2:ceil(" \
                  "ih/2)*2,scale=w=1630:h=1080:eval=init:interl=false:in_range=pc:out_range=tv,format=yuv420p," \
                  "setsar=1631/1630\" {0}/output_imgs.mp4".format(self.images_directory)
        os.system(command)

    def create_final_template(self, num):
        self.template_out = ""
        for i in range(1, int(num) + 1):
            st = (i - 1) * self.space
            en = i * self.space
            st_hh = int(int(st) / 60 / 60)
            st_mm = int(int(st) / 60) - 60 * st_hh
            st_ss = int(int(st) - (st_hh * 60 * 60 + st_mm * 60))
            st_mili = int((st - int(st)) * 1000)
            en_hh = int(int(en) / 60 / 60)
            en_mm = int(int(en) / 60) - 60 * en_hh
            en_ss = int(int(en) - (en_hh * 60 * 60 + en_mm * 60))
            en_mili = int((en - int(en)) * 1000)
            this_one = self.subtitles_template.format(i, str(st_hh).zfill(2), str(st_mm).zfill(2), str(st_ss).zfill(2),
                                                      str(st_mili).zfill(3), str(en_hh).zfill(2), str(en_mm).zfill(2),
                                                      str(en_ss).zfill(2), str(en_mili).zfill(3), str(i - 1))
            self.template_out = self.template_out + this_one

    def add_subtitles(self, sentences, num):
        self.create_final_template(num)
        self.template_out = self.template_out.format(*sentences)

        with open("{0}/subtitles.srt".format(self.images_directory), "w") as subtitles_file:
            subtitles_file.write(self.template_out)

        os.system("ffmpeg -y -i {0}/output_imgs.mp4 -vf subtitles={0}/subtitles.srt {0}/output_text.mp4".format(
            self.images_directory))

    def add_music(self):
        os.system("ffmpeg -y -i {0}/output_text.mp4 -i bensound-ukulele.mp3 "
                  "-c copy -map 0:v:0 -map 1:a:0 {0}/final_video.mp4".format(self.images_directory))
