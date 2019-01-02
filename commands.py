# coding: utf-8
import re
import config
import requests

commands = []
command_names = []


def command(func):
    reg = re.compile(r'\.{}(.+)?'.format(func.__name__))

    def callback(api, data):
        match = reg.match(data['body'])
        if match:
            try:
                if getattr(func, 'pass_data', False):
                    res = func(data, (match.group(1) or '').strip())
                else:
                    res = func((match.group(1) or '').strip())
            except Exception as e:
                print e
                res = config.error_message
            if not res:
                return
            elif type(res) in (str, unicode):
                body, file = res, None
            else:
                body, file = res

            body = u'>>{}\n{}'.format(data['count'], body)
            api.post(body, config.bot_name, getattr(func, 'to_convo', data['convo']), config.anna_trip, file)

    command_names.append(func.__name__)
    commands.append(callback)
    return func


@command
def help(arg):
    out_message = 'Commands are: {}'.format(' '.join('.{}'.format(cmd) for cmd in command_names))
    return out_message


@command
def bible(arg):
    res = requests.get('http://labs.bible.org/api/?passage=random').text
    res = res.replace('<', '[').replace('>', ']')
    return res


bible.to_convo = 'bible'


@command
def hi(data, arg):
    return u'Hi, {}'.format(data['name'])


hi.pass_data = True


@command
def echo(arg):
    return arg

