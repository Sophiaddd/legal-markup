#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys

import markup

def build_parser():
    parser=argparse.ArgumentParser(description="Marks up commonly used legal terms in a file.")
    parser.add_argument('source', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=None)
    parser.add_argument('-t', '--type', choices=['html', 'markdown'], default='html') 

    return parser

def main(argv):
    parser=build_parser()
    args=parser.parse_args()#(argv)
    
    if args.output is None:
        output=sys.stdout
    else:
        output=open(args.output, "w")

    if args.type=="html":
        link=markup.html_link
    elif args.type=="markdown":
        link=markup.markdown_link
    else:
        raise Exception("Unknown type {}".format(args.output))

    infile=args.source
    instring=infile.read()
    result=markup.transform(instring, link)
    output.write(result)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
