#!/usr/bin/env python3

import argparse
import os
import platform

from .cajparser import CAJParser
from .install import install_context_windows
from .utils import add_outlines
from .version import __version__


def main():
    parser = argparse.ArgumentParser(prog="caj2pdf")
    parser.add_argument("--version", action="version", version=f"%(prog)s v{__version__}")
    subparsers = parser.add_subparsers(help="commands", dest="command")

    show_parser = subparsers.add_parser("show", help="Show the information of the CAJ file.")
    show_parser.add_argument("input", help="Path to the CAJ file.")

    convert_parser = subparsers.add_parser("convert", help="Convert the CAJ file to PDF file.")
    convert_parser.add_argument("input", help="Path to the CAJ file.")
    convert_parser.add_argument("-o", "--output", help="Output path to the PDF file.", required=False)

    outlines_parser = subparsers.add_parser("outlines", help="Extract outlines from the CAJ file and add it to PDF file.")
    outlines_parser.add_argument("input", help="Path to the CAJ file.")
    outlines_parser.add_argument("-o", "--output", help="Path to the PDF file.", required=True)

    parse_parser = subparsers.add_parser("parse", help="Parse CAJ file for debugging/development")
    parse_parser.add_argument("input", help="Path to the CAJ file.")

    text_extract_parser = subparsers.add_parser("text-extract", help="Parse CAJ file for debugging/development")
    text_extract_parser.add_argument("input", help="Path to the CAJ file.")

    install_parser = subparsers.add_parser("install", help="install some system features, may need admin permission.")
    install_parser.add_argument("--dry-run", help="not do actually, show the effect.", action="store_true")
    args = parser.parse_args()

    if args.command == "show":
        caj = CAJParser(args.input)
        if caj.format == "PDF" or caj.format == "KDH":
            print("File: {0}\nType: {1}\n".format(args.input, caj.format))
        else:
            print("File: {0}\nType: {1}\nPage count: {2}\nOutlines count: {3}\n".format(
                args.input,
                caj.format,
                caj.page_num,
                caj.toc_num
            ))

    if args.command == "convert":
        caj = CAJParser(args.input)
        if args.output is None:
            if args.input.endswith(".caj"):
                args.output = args.input.replace(".caj", ".pdf")
            elif (len(args.input) > 4 and (args.input[-4] == '.' or args.input[-3] == '.') and not args.input.endswith(".pdf")):
                args.output = os.path.splitext(args.input)[0] + ".pdf"
            else:
                args.output = args.input + ".pdf"
        caj.convert(args.output)

    if args.command == "outlines":
        caj = CAJParser(args.input)
        if caj.format == "PDF" or caj.format == "KDH":
            raise SystemExit("Unsupported file type: {0}.".format(caj.format))
        toc = caj.get_toc()
        add_outlines(toc, args.output, "tmp.pdf")
        os.replace("tmp.pdf", args.output)

    if args.command == "text-extract":
        caj = CAJParser(args.input)
        caj.text_extract()

    if args.command == "parse":
        caj = CAJParser(args.input)
        caj.parse()

    if args.command == "install":
        if platform.system() == "Windows":
            install_context_windows(args.dry_run)
        else:
            raise NotImplementedError("Only support Windows now.")
