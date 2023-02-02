import builtins
import re

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

R_BOLD = 22
R_RGB = 22
R_ITALIC = 23
R_UNDERSCORE = 24
R_BLINKING = 25
R_REVERSE = 27
R_INVISIBLE = 28
R_STRIKE = 29

END = '\x1b[0m'


def combine_options(color=DEFAULT, back=DEFAULT, *opts):
    """

    :param color: (R,G,B) | "RRGGBB"
    :param back: (R,G,B) | "RRGGBB"
    :param opts: BOLD(1) | ITALIC(3) | UNDERSCORE(4) | BLINKING(5) | REVERSE(7) | INVISIBLE(8) | STRIKE(9)
    :return: a combined ANSI color code
    """
    tag = ''
    if opts:
        tag += OPEN
        tag += ';'.join(list(map(str, opts))) + 'm'
    for param, com in ((color, RGB_FORE), (back, RGB_BACK)):
        if param:
            if type(param) == tuple:
                pass
            elif type(param) == str:
                param = hex_to_256(param)
            else:
                raise TypeError("You need to write 2^8 RGB value as (R,G,B) tuple format, or HTML color as string type without #")
            tag += OPEN
            tag += com + ';'.join(list(map(str, param))) + 'm'
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
    if type(msg) is not str:
        msg = str(msg)
    builtins.print(combine_options(color, back, *opts) + msg + END, end=end)



def interpret(string, strict_check=False, end=END):
    """
    Interpret the message by similar method as MarkDown.
    Notice! The syntax will be checked loosely. So, only one asterisk can add ITALIC option.
    Strict mode will be implemented later.

    bold : ~msg~

    fore-color : #FFFFFFmsg# ( [open] #0x0x0xmsg | [close] msg# )

    italic : * msg *

    underscore : _msg_

    blinking : %msg%

    reverse : ^msg^

    invisible : ` msg `

    strike : -msg-

    :param string: a string using above syntax
    :param strict_check: check syntax carefully, but causes exception when the syntax error occur
    :param end: same as print, and basically add reset character at the end of interpreted string
    :return: modified string

    e.g.) I'm _FORESTHOUSE_ and I like #00FF00~^*Forest*^~#.
    """
    match = {'~': [R_BOLD, BOLD],
             '#': [R_RGB, R_RGB],  # Closing only
             '*': [R_ITALIC, ITALIC],
             '_': [R_UNDERSCORE, UNDERSCORE],
             '%': [R_BLINKING, BLINKING],
             '^': [R_REVERSE, REVERSE],
             '`': [R_INVISIBLE, INVISIBLE],
             '-': [R_STRIKE, STRIKE]}
    state = {'~': False,
             '#': False,  # Ignorable
             '*': False,
             '_': False,
             '%': False,
             '^': False,
             '`': False,
             '-': False}
    color_syntax = re.compile(r'#[0-9a-fA-F]{6}')  # Should be preceded about others' syntax checking
    syntax = re.compile(r'[~#*_%^`-]+')

    # fore-color
    color_sections = set(color_syntax.findall(string))
    for section in color_sections:
        color = hex_to_256(section[1:])
        string = string.replace(section, combine_options(color))

    # others
    for section in syntax.findall(string):
        opts = []
        for c in section:
            state[c] = not state[c]
            opts.append(match[c][state[c]])

        string = string.replace(section, combine_options(DEFAULT, DEFAULT, *opts), 1)
    return string + END


def hex_to_256(h: str):
    """
    Change HTML color format to 0-255 RGB tuple value
    :param h: HTML color without # (e.g. 'FFFFFF' means WHITE)
    :return: (R,G,B) value each is between 0 and 255 as tuple
    """
    return tuple((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))