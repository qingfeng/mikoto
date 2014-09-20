# -*- coding: utf-8 -*-

from __future__ import absolute_import
import re

from mikoto.htmlrenderer import RE_USER_MENTION
from mikoto.markdown import render_markdown
from mikoto.checklist import get_checkbox_count
from mikoto.libs.consts import (SOURCE_FILE, NOT_GENERATED,
                                IGNORE_FILE_EXTS, IS_GENERATED)
from mikoto.libs.emoji import parse_emoji


RST_RE = re.compile(r'.*\.re?st(\.txt)?$')
RE_TICKET = re.compile(r'(?:^|\s)#(\d+)')
RE_ISSUE = re.compile(r'(?:^|\s)#issue(\d+)')
RE_COMMIT = re.compile(r'(^|\s)([0-9a-f]{7,40})')
RE_IMAGE_FILENAME = re.compile(
    r'^.+\.(?:jpg|png|gif|jpeg|mobileprovision|svg|ico)$', flags=re.IGNORECASE)

RE_PR_IN_MESSAGE = re.compile(r'(?:^|\s)#(\d+)(?:\s|$)')
RE_ISSUE_IN_MESSAGE = re.compile(r'(?:^|\s)#issue(\d+)(?:\s|$)')

TICKET_LINK_TEXT = r'<a href="/%s/pull/\1/" class="issue-link">#\1</a>'
ISSUE_LINK_TEXT = r'<a href="/%s/issues/\1/" class="issue-link">#\1</a>'
COMMIT_LINK_TEXT = r' <a href="/%s/commit/\2">\2</a>'


def is_binary(fname):
    ext = fname.split('.')
    if ext is None:
        return False
    if len(ext) == 1:
        return ext[0] not in SOURCE_FILE
    ext = '.' + ext[-1]
    if ext in IS_GENERATED:
        return False
    if ext in IGNORE_FILE_EXTS or ext not in (SOURCE_FILE + NOT_GENERATED):
        return True
    return False


def get_mentions_from_text(text):
    try:
        from models.team import Team
    except ImportError:
        from mikoto.libs.mock import Team
    recipients = RE_USER_MENTION.findall(text)
    users = set()
    for _, r in recipients:
        t = Team.get_by_uid(r)
        if t:
            users.update(t.all_members)
        else:
            users.add(r)
    return list(users)


# TODO: move out, not recommended
def render_markdown_with_team(content, team):
    text = render_markdown(content)
    text = re.sub(RE_TICKET, r'<a href="' + team.url +
                  r'issues/\1/" class="issue-link">#\1</a>', text)
    return parse_emoji(text, is_escape=False)


def render_commit_message(message, project):
    text = parse_emoji(message)
    text = re.sub(RE_PR_IN_MESSAGE,
                  r' <a href="/%s/newpull/\1">#\1</a> ' % project.name,
                  text)
    text = re.sub(RE_ISSUE_IN_MESSAGE,
                  r' <a href="/%s/issues/\1">#\1</a> ' % project.name,
                  text)
    text = text.decode('utf8')
    return text


def render_markdown_with_project(content, project_name):
    text = render_markdown(content)
    text = re.sub(RE_TICKET,
                  TICKET_LINK_TEXT % project_name,
                  text)
    text = re.sub(RE_ISSUE,
                  ISSUE_LINK_TEXT % project_name,
                  text)
    text = re.sub(RE_COMMIT,
                  COMMIT_LINK_TEXT % project_name,
                  text)
    text = text.replace("[PROJECT]", "/%s/raw/master/" % project_name)
    return text


def render(content, project_name=None):
    if project_name:
        return render_markdown_with_project(content, project_name)
    return render_markdown(content)
