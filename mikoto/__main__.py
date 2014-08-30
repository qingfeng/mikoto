# -*- coding: utf-8 -*-
import sys
from argparse import ArgumentParser
from libs.text import render

__all__ = ['main']


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Source text file")
    argv = sys.argv[1:] or ['--help']
    args = parser.parse_args(argv)
    if args.file:
        with open(args.file) as f:
            text = f.read().decode("utf8")
            print render(text).encode("utf8")


if __name__ == '__main__':
    main()
