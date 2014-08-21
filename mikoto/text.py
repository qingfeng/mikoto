# -*- coding: utf-8 -*-

import chardet


def translate_to_unicode(text, default_encoding='utf-8'):
    if isinstance(text, unicode):
        return text
    elif isinstance(text, str):
        try:
            text.decode(default_encoding)
        except UnicodeDecodeError:
            pass

        encoding = chardet.detect(text).get('encoding')
        if encoding:
            return text.decode(encoding, 'ignore')

        return text.decode(default_encoding, 'ignore')
    else:
        raise ValueError
