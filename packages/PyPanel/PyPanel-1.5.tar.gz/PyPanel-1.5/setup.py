version = '1.5'

import setuptools

long_description = r"""
# PyPanel

PyPanel is a module used to create beautiful tools

### Stats

- Pypi Link: [pypi.org/project/PyPanel](https://pypi.org/project/PyPanel)
- Stats Link: [pepy.tech/project/pypanel](https://pepy.tech/project/PyPanel)

[![Downloads](https://static.pepy.tech/personalized-badge/pypanel?period=total&units=international_system&left_color=red&right_color=red&left_text=Downloads)](https://pepy.tech/project/pypanel) [![Downloads](https://static.pepy.tech/personalized-badge/pypanel?period=month&units=international_system&left_color=red&right_color=red&left_text=Downloads%20per%20month)](https://pepy.tech/project/pypanel) [![Downloads](https://static.pepy.tech/personalized-badge/pypanel?period=week&units=international_system&left_color=red&right_color=red&left_text=Downloads%20per%20week)](https://pepy.tech/project/pypanel)

## Setup your program

To setup your program, you have to create a `Program` object and set an attribute to the `prog` var in the module

```python
Program(name, version, authors, description, license, **options)
```

```python
# (!) This is just a example

import PyPanel
from PyPanel import *

prog = Program(
    'Socket Tools', # the name
    '1.0', # the version
    ('BlueRed',), # the authors
    'A simple socket toolkit for many http protocols', # the description
    'MIT' # the license
)

# set the program in the module
setattr(PyPanel, 'prog', prog)
```

`Program` class functions:

- `.update(panel)`: Change the title of the console if the title is actived

## Set a title format

By default, the title change automatically to `:name: :version:` (ex: `Socket Tools 1.0`), but you can change it or disable it

```python
# (!) This is just a example

from PyPanel import *

# change title format
setTitleFormat(r':name: version :version: / made by :authors:') # the title will be 

# disable title
disable_title()

# enable title
enable_title()
```

The title format has many arguments:

- `:name:`: the name of the program
- `:version:`: the version of the program
- `:authors:`: the author(s) of the program
- `:description:`: the description of the program
- `:license:`: the license of the program
- `:panel:`: the current panel
- `:cmd:`: the current cmd (if not command, set to `''`)

if you have added options in your Program class, you can add this value to your title with `:`, your option and `:` (ex: `:option:`), the title will take the string value of the object

## The Context class

The Context class is used to pass informations to the commands as a class and not as multiple arguments

```python
Context(panel, func)
```

when the Context arg is passed, it has for arguments:

- `ctx.panel`: the current panel that is used
- `ctx.function`: the command that is currently called

## Set events

There are many events like:

- `on_start_command`: when a command is executed
- `on_log`: when the module log something
- `on_error`: when a command raise an error

```python
# (!) This is just a example

from PyPanel import *

# create a function that will be called when a command is used
@event('on_start_command')
def on_start_command(command: Command, ctx: Context) -> None:
    print(f'You called {command.name!r} from the panel {ctx.panel}!')

# create a function that will be called when a command raise an error
@event('on_error')
def on_error(ctx: Context, exception) -> None:

    # show an Windows Msgbox error           - if the user is not on windows the function will be equivalent of show_error(*args, **w): pass
    #                  ----------- the title -----------   -------------- the content --------------
    Windows.show_error(f'Error in command {ctx.function}', str(error) + f'\ncause: {error.__cause__}')
    input(f'An error has occurred in the command {ctx.function}: {exception}')
```

## Create commands

To create commands, first: create just a normal function witch contain an argument for the Context when it be called at the first place, and use the decorator `@Command`

```python
# (!) This is just a example

from PyPanel import *
import requests as http

# create the POST request command
@Command
def http_post(ctx: Context) -> None:
    url = input('url: ')
    response = http.post(url)
    print(f'The response code is {response.status_code}')

# create the GET request command
@Command
def http_get(ctx: Context) -> None:
    url = input('url: ')
    response = http.get(url)
    print(f'The response code is {response.status_code}')

# create the PUT request command
@Command
def http_put(ctx: Context) -> None:
    url = input('url: ')
    response = http.put(url)
    print(f'The response code is {response.status_code}')
```

## Create a panel

To create a panel, you have to use the Panel class with the name of the panel, it instructions (commands) and other arguments

```python
Panel(name, colors, instructions, banner, banner_second_chars, **options)
```

```python
# (!) This is just a example

from PyPanel import *

banner = r'''
                            __                  __     ________                   __ 
                           |  \                |  \   |        \                 |  \
  _______  ______   _______| ▓▓   __  ______  _| ▓▓_   \▓▓▓▓▓▓▓▓ ______   ______ | ▓▓
 /       \/      \ /       \ ▓▓  /  \/      \|   ▓▓ \    | ▓▓   /      \ /      \| ▓▓
|  ▓▓▓▓▓▓▓  ▓▓▓▓▓▓\  ▓▓▓▓▓▓▓ ▓▓_/  ▓▓  ▓▓▓▓▓▓\\▓▓▓▓▓▓    | ▓▓  |  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓
 \▓▓    \| ▓▓  | ▓▓ ▓▓     | ▓▓   ▓▓| ▓▓    ▓▓ | ▓▓ __   | ▓▓  | ▓▓  | ▓▓ ▓▓  | ▓▓ ▓▓
 _\▓▓▓▓▓▓\ ▓▓__/ ▓▓ ▓▓_____| ▓▓▓▓▓▓\| ▓▓▓▓▓▓▓▓ | ▓▓|  \  | ▓▓  | ▓▓__/ ▓▓ ▓▓__/ ▓▓ ▓▓
|       ▓▓\▓▓    ▓▓\▓▓     \ ▓▓  \▓▓\\▓▓     \  \▓▓  ▓▓  | ▓▓   \▓▓    ▓▓\▓▓    ▓▓ ▓▓
 \▓▓▓▓▓▓▓  \▓▓▓▓▓▓  \▓▓▓▓▓▓▓\▓▓   \▓▓ \▓▓▓▓▓▓▓   \▓▓▓▓    \▓▓    \▓▓▓▓▓▓  \▓▓▓▓▓▓ \▓▓
'''[1:-1]

main = Panel('Main', (Colors.rainbow), [
    ('POST request', http_post),
    ('GET request', http_get),
    ('PUT request', http_put)
], banner)
```

`Panel` class functions:

- `.render()`: Render the final panel string display
- `.listen(*args)`: Listen to the user input and execute the command

## Add text on your panel

To add text on your panel, you have to call the function `Panel.MakeOutText`.

```python
Panel.MakeOutText(top, middle, bottom, left, right, bottom_left, bottom_right)
```

```
                                     top

                BBBB      AA     NNNN  NN NNNN  NN EEEEEEEE RRRRRR
                B   B    AAAA    NNNNN NN NNNNN NN EE       RR  RRR
        left    BBBB    AA  AA   NN  NNNN NN  NNNN EEEEEE   RRRRRRR     right
                B   B  AAAAAAAA  NN   NNN NN   NNN EE       RR   RR
                BBBB  AA      AA NN    NN NN    NN EEEEEEEE RR    RR

                                    middle

                    o--------------------------------------o
                    |    1. choice           5. choice     |
        bottom_left |    2. choice           6. choice     | bottom_right
                    |    3. choice           7. choice     |
                    |    4. choice           8. choice     |
                    o--------------------------------------o

                                    bottom
```

```python
# (!) This is just a example

from PyPanel import *

border = '\n'.join((' ' * 2) + line + (' ' * 2) for line in [
    'Support: github.com/CSM-BlueRed',
    'Made with PyPanel',
])

main.MakeOutText(
    middle = f'{prog.name} by {", ".join(prog.authors)}!\nMake sure to install PyPanel!',
    bottom = 'discord.gg/plague',
    bottom_left = border,
    bottom_right = border
)
```

## Start your program

To start your program, select your main panel, and use the `listen` function

```python
# (!) This is just a example

main.listen()
```
"""[1:-1]

setuptools.setup(
    name = 'PyPanel',
    version = version,
    author = 'BlueRed',
    description = 'PyPanel is a module used to create beautiful tools',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/CSM-BlueRed/PyPanel',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    packages = setuptools.find_packages(),
    python_requires = '>=3.6',
    install_requires = ['pystyle', 'base64', 'win10toast'],
    keywords = ['python', 'panel', 'tool', 'terminal', 'tui']
)