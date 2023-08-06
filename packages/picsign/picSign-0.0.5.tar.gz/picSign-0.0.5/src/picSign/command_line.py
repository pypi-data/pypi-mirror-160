#!/usr/bin/env python

"""
Sign Picture:
    picSign your image by encoding a text in pixels of the image

Usage:
    picSign (-w | --write) <image> <input> [-f -o OUT]
    picSign (-r | --read) <image>
    picSign (-h | --help)
    picSign --version

Options:
    -w --write              use the program in write mode
    -r --read               use the program in read mode
    -h --help               show this help message and exit
    -f --file               encode a file in the image
    -o OUT --output OUT     output the image to a file [default: out]
Examples:
    pic_sign -w image.png "Hello World"
    pic_sign -r image.png
"""
from docopt import docopt

from main import write_image, read_image


def main():
    args = docopt(__doc__)

    if args['--write']:
        write_image(args['<image>'], args['<input>'], args['--output'], args['--file'])
    elif args['--read']:
        read_image(args['<image>'])
