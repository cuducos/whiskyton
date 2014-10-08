# coding: utf-8

import coffeescript
from unipath import Path
from flask.ext.script import Manager
CoffeeCommand = Manager(usage='Compile CoffeeScript file(s)')


@CoffeeCommand.option('-f', '--file', dest='filename', help='CoffeeScript filename')
@CoffeeCommand.command
def compile(filename):
    """
    Compile .coffee files from whiskyton/static/coffeescript/
    into .js files in whiskython/static/js
    """

    # folders
    static = Path('whiskyton', 'static')
    cs_folder = Path(static, 'coffeescript')
    js_folder = Path(static, 'js')

    # check if file exists
    handler = Path(cs_folder, filename)
    if handler.isfile():

        # if file exists
        cs = handler.read_file()
        js = coffeescript.compile(cs)
        output = Path(js_folder, '{}.js' .format(handler.stem))
        output.write_file(js)

        # print results for conference
        print '==> Input: {}\n\n{}\n\n==> Output: {}\n\n{}'.format(handler,
                                                                   cs,
                                                                   output,
                                                                   js)

    else:

        # print error
        print '==> {} is not a valid file'.format(handler)
