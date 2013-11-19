import argparse
import asteval

parser = argparse.ArgumentParser(description='Check source code of strategy.')
parser.add_argument('-c', help='source code')

def main():
    args = parser.parse_args()
    aeval = asteval.Interpreter()
    aeval(args.c)

if __name__ == '__main__':
    main()