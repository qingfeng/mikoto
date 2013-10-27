#!/usr/bin/env python
# encoding: utf-8

import re
import os
from cgi import escape
# EMOJIS 对应 /hub/static/emoji/ 下的图片
EMOJIS = [
    ':airplane:', ':alien:', ':art:', ':bear:', ':beer:', ':bike:', ':bomb:',
    ':book:', ':bulb:', ':bus:', ':cake:', ':calling:', ':clap:', ':cocktail:',
    ':code:', ':computer:', ':cool:', ':cop:', ':email:', ':feet:', ':fire:',
    ':fish:', ':fist:', ':gift:', ':hammer:', ':heart:', ':iphone:', ':key:',
    ':leaves:', ':lgtm:', ':lipstick:', ':lock:', ':mag:', ':mega:', ':memo:',
    ':moneybag:', ':new:', ':octocat:', ':ok:', ':palm_tree:', ':pencil:',
    ':punch:', ':runner:', ':scissors:', ':ship:', ':shipit:', ':ski:', ':smile:',
    ':smoking:', ':sparkles:', ':star:', ':sunny:', ':taxi:', ':thumbsdown:',
    ':thumbsup:', ':tm:', ':tophat:', ':train:', ':trollface:', ':v:', ':vs:',
    ':warning:', ':wheelchair:', ':zap:', ':zzz:', ':see_no_evil:',':pig:',
    ':hear_no_evil:', ':speak_no_evil:', ':monkey:', ':monkey_face:', ':beers:',
    ':ruby:',
]



def parse_emoji(text, is_escape=True):
    if not text:
        return ''
    if is_escape:
        text = escape(text)
    if RE_EMOJI_ONLY.match(text.strip()):
        emoji_img = '<img src="/static/emoji/%s.png" align="absmiddle"/>'
    else:
        emoji_img = '<img src="/static/emoji/%s.png" height="20" width="20" align="absmiddle"/>'
    result = RE_EMOJI.sub(lambda x: emoji_img % x.group().strip(':'), text)
    return result

def all_emojis():
    curdir = os.path.abspath(os.path.curdir)
    emoji_dir = os.path.join(curdir, 'hub/static/emoji/')
    if os.path.isdir(emoji_dir):
        files = os.listdir(emoji_dir)
    else:
        realpath = os.path.dirname(os.path.realpath(__file__))
        curdir = os.path.join(realpath,os.path.pardir,'hub/static/emoji')
        curdir = os.path.abspath(curdir)
        if os.path.isdir(curdir):
            files = os.listdir(emoji_dir)
        else:
            return EMOJIS
    if files:
        return [':{}:'.format(fn[:-4]) for fn in files if fn.endswith('.png')]
    else:
        return EMOJIS


def url_for_emoji(emoji):
    return '/static/emoji/%s.png' % emoji[1:-1]


RE_EMOJI = re.compile(r'(' + '|'.join([re.escape(x) for x in all_emojis()]) + r')')
RE_EMOJI_ONLY = re.compile(r'^<p>\s*(' + '|'.join([re.escape(x) for x in all_emojis()]) + r')\s*</p>$')