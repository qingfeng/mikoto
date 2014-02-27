#!/usr/bin/env python
# encoding: utf-8

import re
import os
from cgi import escape

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
    ':warning:', ':wheelchair:', ':zap:', ':zzz:', ':see_no_evil:', ':pig:',
    ':hear_no_evil:', ':speak_no_evil:', ':monkey:', ':monkey_face:', ':beers:',
    ':ruby:',
]


# EMOJIS dir: /hub/static/emoji/
EMOJI_GROUPS = {
    ":mergetime:": """
:zap::zap::zap::zap::zap::zap::zap::zap::zap::zap:
:zap::metal: M E R G E T I M E :metal::zap:
:zap::zap::zap::zap::zap::zap::zap::zap::zap::zap:
""",

    ":sparklock:": """
:black_circle::point_down::black_circle:
:point_right::sparkler::point_left:
:black_circle::point_up_2::black_circle:
""",

    ":myballoon:": """
:cloud::partly_sunny::cloud::cloud::cloud::cloud::cloud:
 
        :balloon:
 
                    :runner::dash:
""",

    ":getit:": """
:balloon:
  :raised_hand:
""",

    ":apollo:": """
:octocat:      :star2:             :us:
:sparkles:                :sparkles:   :full_moon:
:star2:     :dizzy:         :rocket:
        :sparkles:     :collision:
:partly_sunny:        :collision:       :sparkles:
:zap:   :collision:
:earth_asia:          :sparkles:         :dizzy:   
""",
}


def parse_emoji_groups(text):
    groups = set(RE_EMOJI_GROUPS.findall(text))
    for group in groups:
        group_text = EMOJI_GROUPS[group]
        group_text = group_text.replace(' ', '&nbsp;')
        group_text = group_text.replace('\n', "<br/>")
        text = text.replace(group, group_text)
    return text


def parse_emoji(text, is_escape=True):
    if not text:
        return ''
    if is_escape:
        text = escape(text)
    text = parse_emoji_groups(text)
    if RE_EMOJI_ONLY.match(text.strip()):
        emoji_img = '<img src="/static/emoji/%s.png" align="absmiddle"/>'
    else:
        emoji_img = '<img src="/static/emoji/%s.png" height="20" width="20" align="absmiddle"/>'
    result = RE_EMOJI.sub(lambda x: emoji_img % x.group().strip(':'), text)
    return result


def all_emojis():
    sub_emoji = 'hub/static/emoji'
    emoji_dir = os.path.join(os.path.curdir, sub_emoji)
    realpath = os.path.dirname(os.path.realpath(__file__))
    curdir = os.path.join(realpath, os.path.pardir, sub_emoji)
    for dir in [emoji_dir, curdir]:
        abs_emoji_dir = os.path.abspath(dir)
        if os.path.isdir(abs_emoji_dir):
            files = os.listdir(abs_emoji_dir)
            if files:
                return [':{}:'.format(fn[:-4]) for fn in files
                        if fn.endswith('.png')]
    return EMOJIS


def url_for_emoji(emoji):
    return '/static/emoji/%s.png' % emoji[1:-1]


RE_EMOJI = re.compile(r'(' + '|'.join([re.escape(x) for x in all_emojis()]) + r')')
RE_EMOJI_ONLY = re.compile(r'^<p>\s*(' + '|'.join([re.escape(x) for x in all_emojis()]) + r')\s*</p>$')
RE_EMOJI_GROUPS = re.compile('|'.join([re.escape(x) for x in EMOJI_GROUPS.keys()]))
