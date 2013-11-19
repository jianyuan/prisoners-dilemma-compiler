from subprocess2 import Popen, PIPE
from tempfile import NamedTemporaryFile
import argparse
import asteval

parser = argparse.ArgumentParser(description='Check source code of strategy.')
parser.add_argument('-c', help='source code')

def check_ast_errors(error):
    if len(error) > 0:
        for err in error:
            msg = '%s: %s' % (err.get_error())
            return msg
    return None

def check_source_code(source_code):
    errors = []

    # aeval = asteval.Interpreter()

    # try:
    #     aeval.parse(source_code)
    # except Exception as e:
    #     msg = check_ast_errors(aeval.error)
    #     print 'ast:', msg

    #     errors.append(msg)

    tmp_file = NamedTemporaryFile()
    try:
        tmp_file.write(source_code)
        tmp_file.flush()

        sp = Popen(['pylint', '--errors-only', '--msg-template="{line}: {msg} ({symbol})"', tmp_file.name], stdout=PIPE, stderr=PIPE)
        out, err = sp.communicate()

        # from pylint import epylint as lint
        # cmd = "%s --msg-template='{line:3d},{column:2d}: {msg} ({symbol})'" % (tmp_file.name,)
        # print cmd
        # (stdout, stderr) = lint.py_run(cmd, True)
        # out = stdout.read()
        # err = stderr.read()

        if out:
            # errors.append(out)
            errors.append('\n'.join(out.split('\n')[1:])) # Remove first line of stdout
        if err:
            errors.append(err)
    finally:
        tmp_file.close()

    if not errors:
        aeval = asteval.Interpreter()
        res = aeval(source_code)

        # if 'decide' not in aeval.symtable or not isinstance(aeval.symtable['decide'], asteval.asteval.Procedure):
        #     errors.append('The `decide(context)` function must be implemented\n')
        # elif len(aeval.symtable['decide'].argnames) != 1:
        #     errors.append('The `decide(context)` function must accept a context argument\n')

    output = {
        'success': not bool(errors),
        'errors': ''.join(errors)
    }

    return output

if __name__ == '__main__':
    import json

    args = parser.parse_args()
    output = check_source_code(args.c)
    print json.dumps(output)
