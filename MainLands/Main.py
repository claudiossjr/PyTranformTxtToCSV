#!/usr/bin/python3
__author__ = 'claudio'
import sys, getopt
from BaseEngine import TransformEngine


def parse_options(args):
    try:
        opts, argv = getopt.getopt(args, "hd:s:f:w:o:e:",
                                   ["destination=", "source=", "folder=", "work=", "out=", "end="])
    except getopt.GetoptError:
        print(
                "Main.py -d <destinationNode> -s <SourceNode> -f <filesFolder> "
                "-w <WorkFolder> -o <OutFolder> -e <EndFolder>\n"
                "Main.py --destination <destinationNode> --source <SourceNode> "
                "--folder <filesFolder> --work <WorkFolder> --out <OutFolder> --end <EndFolder>")
        sys.exit(2)

    options_dict = {}
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                "Main.py -d <destinationNode> -s <SourceNode> -f <filesFolder> "
                "-w <WorkFolder> -o <OutFolder> -e <EndFolder>\n"
                "Main.py --destination <destinationNode> --source <SourceNode> "
                "--folder <filesFolder> --work <WorkFolder> --out <OutFolder> --end <EndFolder>")
            sys.exit(2)
        elif opt in ("-d", "--destination"):
            options_dict["destination"] = arg
        elif opt in ("-s", "--source"):
            options_dict["source"] = arg
        elif opt in ("-f", "--folder"):
            options_dict["folder"] = arg
        elif opt in ("-w", "--work"):
            options_dict["work"] = arg
        elif opt in ("-o", "--out"):
            options_dict["out"] = arg
        elif opt in ("-e", "--end"):
            options_dict["end"] = arg

    return options_dict


def main(args):
    options = parse_options(args)
    print(options)
    destination_file = options["destination"]
    source_file = options["source"]
    files_folder = options["folder"]
    work_folder = options["work"]
    out_folder = options["out"]
    end_folder = options["end"]
    engine = TransformEngine(destination_file, source_file, files_folder,work_folder, out_folder, end_folder)
    engine.run()

    print(args)


if __name__ == '__main__':
    main(sys.argv[1:])
