import argparse
from subprocess2 import Popen, PIPE
import asteval
import json
from tempfile import NamedTemporaryFile

parser = argparse.ArgumentParser(description='Check source code of strategy.')
parser.add_argument('-c', help='source code')
parser.add_argument('-i', help='STDIN')
parser.add_argument('-t', type=int, default=5, help='timeout in seconds')

def main():
    args = parser.parse_args()
    
    errors = []

    tmp_file = NamedTemporaryFile()
    try:
        tmp_file.write(args.c)
        tmp_file.seek(0)

        sp = Popen(['pylint', '--errors-only', tmp_file.name], stdout=PIPE, stderr=PIPE)
        out, err = sp.communicate()

        if out:
            errors.append('\n'.join(out.split('\n')[1:])) # Remove first line of stdout
        if err:
            errors.append(err)
    finally:
        tmp_file.close()

    if not errors:
        aeval = asteval.Interpreter()
        aeval(args.c)

        if 'decide' not in aeval.symtable or not isinstance(aeval.symtable['decide'], asteval.asteval.Procedure):
            errors.append('The decide(context) function must be implented')
        elif len(aeval.symtable['decide'].argnames) != 1:
            errors.append('The decide(context) function must accept a context argument')

    output = {
        'errors': '\n'.join(errors)
    }

    print json.dumps(output)

if __name__ == '__main__':
    main()