#!/usr/bin/python3
__author__ = 'claudio'
import sys,getopt
from BaseEngine import TransformEngine


def parseOptions(argv):
    try:
        opts, args = getopt.getopt(argv,"hd:s:f:", ["destination=", "source=", "folder="])
    except getopt.GetoptError:
        print("Main.py -dest <destinationNode> -sour <SourceNode> -fol <filesFolder>")
    optionsDict = {}
    for opt, arg in opts:
        if opt == "-h":
            print("Main.py -d <destinationNode> -s <SourceNode> -f <filesFolder>\n"
                  "Main.py --destination <destinationNode> --source <SourceNode> --folder <filesFolder>")
            sys.exit(2)
        elif opt in ("-d", "--destination"):
            optionsDict["destination"] = arg
        elif opt in ("-s", "--source"):
            optionsDict["source"] = arg
        elif opt in ("-f", "--folder"):
            optionsDict["folder"] = arg

    return optionsDict

def main(args):
    options = parseOptions(args)
    print(options)
    destinationFile = options["destination"]
    sourceFile = options["source"]
    filesFolder = options["folder"]
    engine = TransformEngine(destinationFile, sourceFile, filesFolder)
    engine.run()
    print("Hello,  World!")
    print(args)

if __name__ == '__main__':
    main(sys.argv[1:])
