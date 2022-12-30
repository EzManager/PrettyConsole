import builtins
DEFAULT = ()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
LIME = (0, 255, 0)
GREEN = (0, 80, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
REBECCAPURPLE = (102, 51, 153)
PINK = (255, 90, 255)
BROWN = (120, 50, 0)

OPEN = '\x1b['

BOLD = 1
RGB_FORE = '38;2;'
RGB_BACK = '48;2;'
ITALIC = 3
UNDERSCORE = 4
BLINKING = 5
REVERSE = 7
INVISIBLE = 8
STRIKE = 9

R_BOLD = '22;'
R_RGB = '22;'
R_ITALIC = '23;'
R_UNDERSCORE = '24;'
R_BLINKING = '25;'
R_REVERSE = '27;'
R_INVISIBLE = '28;'
R_STRIKE = '29;'

END = '\x1b[0m'


def combine_options(color=DEFAULT, back=DEFAULT, *opts):
    """

    :param color: (R,G,B)
    :param back: (R,G,B)
    :param opts: BOLD(1) | ITALIC(3) | UNDERSCORE(4) | BLINKING(5) | REVERSE(7) | INVISIBLE(8) | STRIKE(9)
    :return: a combined ANSI color code
    """
    tag = ''
    if opts:
        tag += OPEN
        tag += ';'.join(list(map(str, opts))) + 'm'
    if color:
        tag += OPEN
        tag += RGB_FORE + ';'.join(list(map(str, color))) + 'm'
    if back:
        tag += OPEN
        tag += RGB_BACK + ';'.join(list(map(str, back))) + 'm'
    return tag
def print(msg='', color=DEFAULT, *opts, back=DEFAULT, end='\n'):
    """
    Prints msg with custom color or tags.
    Color option prioritizes against the color tag.
    This will change the color of whole messages in this call.

    :param msg: message to print
    :param color: pretty.COLOR_NAME | (R,G,B) values between 0 to 255
    :param opts: pretty.OPTION_NAME | BOLD(1) | ITALIC(3) | UNDERSCORE(4) | BLINKING(5) | REVERSE(7) | INVISIBLE(8) | STRIKE(9)
    :param back: same as color, but must be at the rightest side of parameters with name specification 'back='
    :param end: same as the builtin print's end parameter

    e.g.) pretty.print("PRETTY!", pretty.PINK, pretty.ITALIC, 1, back=(255, 255, 230))
    """
    builtins.print(combine_options(color, back, *opts) + msg + END, end=end)



def interpret(string):
    """
    Interpret the message by similar method as MarkDown.

    bold : **msg**

    color : |COLOR_NAMEmsg

    italic : *msg*

    underscore : _msg_

    blinking : ;msg;

    reverse : ^msg^

    invisible : `msg`

    strike : -msg-

    :param string: a string using above syntax
    :return: modified string
    """
    return "Unimplemented"