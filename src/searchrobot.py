#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

import wikipedia as wiki
from nltk import tokenize
from rake_nltk import Rake
from watson_developer_cloud import NaturalLanguageUnderstandingV1


class SearchRobot:

    def __init__(self):
        self.keywords_list = []
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version="2018-11-16",
            iam_apikey="YOUR_API_KEY_HERE",
            url="YOUR_URL_HERE")

    @staticmethod
    def search(search_term):
        summary = wiki.summary(search_term, sentences=40)
        summary = re.sub(r"\([^)]*\)", "", summary)

        return tokenize.sent_tokenize(summary)

    def get_keywords(self, sentences):
        for sentence in sentences:
            rake_nltk_var = Rake()
            rake_nltk_var.extract_keywords_from_text(sentence)
            keyword_extracted = rake_nltk_var.get_ranked_phrases()[:3]
            response = keyword_extracted

            temp_list = []
            for keyword in response:
                temp_list.append(keyword)

            self.keywords_list.append(temp_list)

        return self.keywords_list
