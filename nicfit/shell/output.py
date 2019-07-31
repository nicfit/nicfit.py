import operator
import textwrap
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.shortcuts import print_tokens


class Styles:
    NAME_VALUE_DICT = {Token.Name: 'bold',
                       Token.Delim: '#0000ee',
                       Token.Value: ''}
    NAME_VALUE = style_from_dict(NAME_VALUE_DICT)

    DEFN_LIST_DICT = {Token.Name: 'italic',
                      Token.Delim: '#0000ee',
                      Token.Definition: ''}
    DEFN_LIST = style_from_dict(DEFN_LIST_DICT)

    TITLE_DICT = {Token.Title: 'bold',
                  Token.Ruler: '#0000ee'}
    TITLE = style_from_dict(TITLE_DICT)


def printNameValues(pairs, delim=" : ", pad_names=True, style=None):
    nmax = max((len(p[0] or "") for p in pairs)) if pad_names else 0
    tokens = []
    for n, v in pairs:
        if n:
            tokens += [(Token.Name, n),
                       (Token, " " * (nmax - len(n)) if pad_names else ""),
                       (Token.Delim, delim),
                       (Token.Value, str(v)),
                       (Token, "\n"),
                       ]

    print_tokens(tokens, style=style or Styles.NAME_VALUE)


def printDefList(pairs, delim="\n", indent=4, width=None, style=None):
    tokens = []
    for n, v in pairs:
        tokens += [(Token.Name, n), (Token.Delim, delim if v else ""),
                   (Token, " " * indent if v else ""),
                   (Token.Definition, textwrap.fill(str(v), width=70,
                                                    initial_indent=indent)
                                           if v else ""),
                   (Token, "\n"),
                  ]

    print_tokens(tokens, style=style or Styles.DEFN_LIST)


def printTitle(t, hr="=", style=None):
    print_tokens([(Token.Title, t),
                  (Token, "\n"),
                  (Token.Ruler, hr * len(t)),
                  (Token, "\n"),
                 ], style=style or Styles.TITLE)


def printRoomList(rooms_list):
    rooms = sorted(rooms_list, key=operator.itemgetter("population"))
    for room in rooms:
        name, slug = room["name"], room["slug"]
        print(f"* [{slug}]  :  {name}")
        if room["dj"]:
            print(f"\tListeners: {room['population']}  |  "
                  f"DJ: {room['dj']}  |  Media: {room['media']}")
