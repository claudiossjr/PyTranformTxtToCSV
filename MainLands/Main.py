#!/usr/bin/python3
__author__ = 'claudio'
import sys, getopt
from BaseEngine import TransformEngine


def parse_options(args):
    try:
        opts, argv = getopt.getopt(args, "hd:s:f:", ["destination=", "source=", "folder="])
    except getopt.GetoptError:
        print("Main.py -dest <destinationNode> -sour <SourceNode> -fol <filesFolder>")
    options_dict = {}
    for opt, arg in opts:
        if opt == "-h":
            print("Main.py -d <destinationNode> -s <SourceNode> -f <filesFolder>\n"
                  "Main.py --destination <destinationNode> --source <SourceNode> --folder <filesFolder>")
            sys.exit(2)
        elif opt in ("-d", "--destination"):
            options_dict["destination"] = arg
        elif opt in ("-s", "--source"):
            options_dict["source"] = arg
        elif opt in ("-f", "--folder"):
            options_dict["folder"] = arg

    return options_dict


def main(args):
    options = parse_options(args)
    print(options)
    destination_file = options["destination"]
    source_file = options["source"]
    files_folder = options["folder"]
    engine = TransformEngine(destination_file, source_file, files_folder)
    engine.run()

    print(args)


if __name__ == '__main__':
    main(sys.argv[1:])
