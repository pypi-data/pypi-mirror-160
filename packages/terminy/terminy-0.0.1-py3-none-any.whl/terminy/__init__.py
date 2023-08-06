import getopt
import sys

def parse_param(sys_argv, params:dict)->dict:
    """
    """
    argv = sys_argv[1:]

    # params = {'table': '', 'incremental': '', 'fields': '', 'where': ''}

    shorts = ''
    full = []
    instruction = str(__file__)

    if params.get('_help', None):
        shorts += params.get('_help').get('short', 'h')

    for k, v in params.items():
        if not k.startswith('_'):
            short = params.get(k).get('short', k[:1])
            shorts += short
            if v.get('has_parameter', True):
                shorts += ':'
            full.append(k + '=')
            if v.get('mandatory', False):
                instruction += ' -{}'.format(short) + ' <{}>'.format(v.get('description', k))

    # print(shorts, full)

    try:
        opts, _ = getopt.getopt(argv, shorts, full)
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if params.get('_help') and opt=='-' + params.get('_help').get('short', 'h'):
            sys.exit()
        else:
            for k, v in params.items():
                if not k.startswith('_'):
                    short = params.get(k).get('short', k[1:])
                    if opt in ("-" + short, "--" + k):
                        params[k]['value'] = arg

    return params

def parse_values(params:dict)->dict:
    """
    """
    param = parse_param(sys.argv, params)
    values = {}
    for k, v in param.items():
        values[k] = v.get('value', None)
    return values