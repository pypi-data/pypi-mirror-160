__version__: str = '1.5'
__author__: str = 'BlueRed'
__license__: str = 'MIT'
__support__ = 'https://discord.gg/j6n4599RXd'
__note__: str = """
# PyPanel (VERSION %s)
Added: fade_mode argument for Panel.listen() - example: fade_mode = {'banner': pystyle.Col.blue_to_red, 'table': pystyle.Col.red_to_yellow}, command wrapper "Command.command(name)", function "Command.from_file(file)"
Fixed: ...
Message: Hey, its BlueRed! I hope you enjoy my module & thank u, if you want to share it, you can by share the GitHub link and the PyPi project link ! I know that if I stop PyPanel updates, my module will lose downloads, so don't worry, I release at least 1 version per week
""" % __version__
__notes__ = {key: value for key, value in (note.split(': ') for note in __note__.splitlines() if (note.strip() and ': ' in note))}

from ctypes.wintypes import HWND, LPWSTR, UINT
from os import mkdir, name as os_name, remove
from base64 import b64encode, b64decode
from win10toast import ToastNotifier
from threading import Thread
from os.path import exists
import pystyle as _style
from io import BytesIO
from pystyle import *
import tokenize
import ctypes

# must to be edited
prog = ...

# can be edited (suggested)
default_banner = ''
default_banner_second_chars = ['░', '▒', '▓', '█']
title_format = r':name: :version:'
titleEnabled = True

_cache = '__pypanel-cache'
mkdir(_cache) if not exists(_cache) else ...
chars = []
def _prepare_chars():
    _index = 0

    while True:
        try: char = chr(_index)
        except: break
        chars.append(char)
        _index += 1

Thread(target = _prepare_chars).start()

def setTitleFormat(format):
    r"""
    Set the format of the title
    """
    globals()['title_format'] = format

def setDefaultBanner(banner):
    r"""
    Set the default banner used when the banner of a panel is not set
    """
    globals()['default_banner'] = banner

def enable_title():
    r"""
    Enable the title
    """
    globals()['titleEnabled'] = True

def disable_title():
    r"""
    Disable the title
    """
    globals()['titleEnabled'] = False

setSize = System.Size

_events = {
    'onStart': {
        'command': (lambda command, ctx: ...)
    },
    'onLog': (lambda message: ...),
    'onError': (lambda ctx, exception: Colorate.Error(str(exception)))
}

pystyle = _style

logs = BytesIO()

def _log(text):
    logs.write(text.encode('utf-8', 'replace'))
    _events['onLog'](text)

def _preview(func):
    func.__doc__ = f'!!! Preview - This is not working now but in the next versions !!!\n{func.__doc__}'
    func.__preview__ = True
    return func

def _windows_feature(func):
    if type(func) is property: return func
    func.__windows_feature__ = True
    if os_name == 'nt':
        return func
    else:
        def windows_feature_not_supported(*args, **kwargs): pass
        windows_feature_not_supported.__doc__ = f'!!! This feature is not supported on your OS !!!\n{func.__doc__}'
        return windows_feature_not_supported

def event(name = None):
    r"""
    Set a function to be called when the event is triggered
    """
    def decorator(func):
        nonlocal name
        name = name or func.__name__

        if name not in {'on_start_command', 'on_log', 'on_error'}:
            raise Exception(f'The event {name!r} is not supported')

        if name == 'on_start_command':
            _events['onStart']['command'] = func

        if name == 'on_log':
            _events['onLog'] = func

        if name == 'on_error':
            _events['onError'] = func

        return func
    return decorator

class DataSaver():
    r"""
    A class to save data in a file and get it back later
    """

    import base64
    import binascii
    import pickle
    import zlib

    class _Memory():
        def __init__(self, content: tuple) -> None:
            self.content = content

    def __init__(self, file: str) -> None:
        open(file, 'a+').close()
        self.file = file

    def encrypt(self, content: bytes) -> bytes:
        r"""
        Encrypt the content
        """
        content = b64encode(content)
        content = DataSaver.binascii.hexlify(content)
        content = DataSaver.base64.b32encode(content)
        content = DataSaver.zlib.compress(content)
        return content

    def decrypt(self, content: bytes) -> str:
        r"""
        Decrypt the content
        """
        content = DataSaver.zlib.decompress(content)
        content = DataSaver.base64.b32decode(content)
        content = DataSaver.binascii.unhexlify(content)
        content = b64decode(content)
        return content

    def save(self, **data) -> None:
        r"""
        Save a data
        """
        file = open(self.file, 'wb')
        objects = []
        for key, value in data.items():
            objects.append(DataSaver._Memory((key, value)))
        file.write(self.encrypt(DataSaver.pickle.dumps(objects)))

    def load(self) -> None:
        r"""
        Get all the data saved
        """
        if len(open(self.file, 'rb').read()) == 0: return {}
        objects = DataSaver.pickle.loads(self.decrypt(open(self.file, 'rb').read()))
        data = {obj.content[0]: obj.content[1] for obj in objects}
        return data

    def get(self, key: str):
        r"""
        Get a data from the file
        """
        return self.load()[key]

global_saver = DataSaver(f'{_cache}/__cache.pypanel')

class Context():
    r"""
    The context class, used to pass informations to the commands as a class and not as multiple arguments
    """

    def __init__(self, panel, func) -> None:
        self.panel = panel
        self.function = func

        _log(f'Added context for {self.panel}/{self.function}')

    def __str__(self) -> str:
        return f'c~{id(self)}'
    
    def __repr__(self) -> str:
        return f'<context from {self.panel} for {self.function}>'

class Command():
    r"""
    The command class
    """

    def __init__(self, func) -> None:
        self.command = func
        self.name = ' '.join(word.capitalize() for word in func.__name__.split('_'))
        self.results = []

        _log(f'Added command for {self.command}')

    def __str__(self) -> str:
        return f'command {self.name}'

    def __repr__(self) -> str:
        return f'<command {self.name}>'

    def __call__(self, ctx: Context, *args, **kwargs):
        onStart = _events['onStart']['command'](self, ctx)
        prog.update(ctx.panel, self)
        result = self.command(ctx, *args, **kwargs)
        self.results.append((onStart, result))
        _log(f'{self.name} returned {result}')
        return result

    @staticmethod
    def from_file(file: str, command_name: str) -> 'Command':
        r"""
        Create a command from a file (.py, .pyw)
        the file must have a "ctx" variable and must be assigned like this: "ctx = ..."
        you can use "return" to return a value
        """
        io_file = open(file, 'rb')
        tokens = tokenize.tokenize(io_file.readline)
        io_file.close()
        tokens = [
            token if not (token.type == tokenize.NAME and token.string == 'ctx') else tokenize.TokenInfo(
                token.type, '__PyPanel_ctx__', token.start, token.end, token.line
            ) for token in tokens
        ]
        code = tokenize.untokenize(tokens)
        def _func_from_code(ctx: Context):
            exec(code, {'__PyPanel_ctx__': ctx})
        _func_from_code.__name__ = command_name
        return Command(_func_from_code)
    
    @staticmethod
    def command(name: str):
        r"""
        Create a command from a function

        example:

        ```
        @Command.command('My Command')
        def my_command(ctx: Context):
            print('Hello World')
        ```
        """
        def decorator(func) -> 'Command':
            new_command = Command(func)
            new_command.name = name
        return decorator

class Panel():
    r"""
    The panel class
    """
    spaces = 5
    chars = {
        'up': '═',
        'down': '═',
        'left': '║',
        'right': '║',
        'top_left': '╔',
        'top_right': '╗',
        'bottom_left': '╚',
        'bottom_right': '╝',
    }

    def __init__(self, name: str, colors: list[str], instructions: list[tuple], banner: str = default_banner, banner_second_chars: list[str] = default_banner_second_chars, **options) -> None:
        self.name = name
        self.colors = [colors, colors] if type(colors) != list else colors
        self.instructions = instructions
        self.banner_second_chars = banner_second_chars
        self.banner = banner
        self.input = options.get('input', 'Choose a command >>> ')
        self.command404 = options.get('cmd404', 'Command not found :cmd:')

        self.text = {
            'top': '',
            'middle': '',
            'bottom': '',
            'left': '',
            'right': '',
            'bottom_left': '',
            'bottom_right': '',
        }

        self.render()

        panelInfos = {'name': self.name, 'input': self.input, 'command 404 error': self.command404, 'instructions': self.instructions}
        _log(f'Added panel {panelInfos}')

    def render(self) -> None:
        r"""
        Render the final panel string display
        """
        cases = []
        obj = [instr[0] for instr in self.instructions]

        while len(obj) != 0:
            newObj = obj[6:]
            cases.append(obj[:6])
            obj = newObj

        count = 0

        def getIndex():
            nonlocal count
            count += 1
            return count - 1

        if len(cases) > 1:
            table = Add.Add(*['\n'.join(f'[ {getIndex()} ] ' + instr  + (' ' * Panel.spaces) for instr in instrs) for instrs in cases])
        else:
            table = '\n'.join(f'[ {getIndex()} ] ' + instr  + (' ' * Panel.spaces) for instr in cases[0])
        table = '[/] ' + '?' + '\n' + table

        width = 60
        up = Panel.chars['top_left'] + (Panel.chars['up'] * width) + Panel.chars['top_right']
        down = Panel.chars['bottom_left'] + (Panel.chars['down'] * width) + Panel.chars['bottom_right']

        final = '\n'.join((
            up,
            '\n'.join(Panel.chars['left'] + ' ' + line + (
                (' ' * (
                    (width - len(Panel.chars['left'] + ' ' + line) + 1)
                )) + Panel.chars['right']
            ) for line in table.splitlines()),
            down
        ))

        self.table = final

        _log(f'Rendered panel {self.name}')

    def listen(self, *args, left_panel = exit, fade_mode: dict = {'banner': Colorate.Vertical, 'table': Colorate.Horizontal}) -> None:
        r"""
        Listen to the user input and execute the command
        """
        _log(f'Listening to {self.name}')
        while True:
            prog.update(self)
            info = f'{left_panel.name} => {self.name}'
            table = self.table.replace(
                self.table.splitlines()[1],
                self.table.splitlines()[1].replace(
                    '?' + self.table.splitlines()[1].split('?')[1].split(Panel.chars['right'])[0].strip(),
                    info
                )
            )
            lines_parts = table.splitlines()[1].split(Panel.chars['right'])
            table = table.replace(
                table.splitlines()[1].split(
                    Panel.chars['right']
                )[1],
                lines_parts[1][:-(len(info) - 1)]
            )

            if self.text['bottom_left']:
                table = Add.Add(self.text['bottom_left'], table, center = True)

            if self.text['bottom_right']:
                table = Add.Add(table, self.text['bottom_right'], center = True)

            banner = self.banner

            if self.text['left']:
                banner = Add.Add(self.text['left'], banner, center = True)

            if self.text['right']:
                banner = Add.Add(banner, self.text['right'], center = True)

            colored_table = fade_mode['table'](self.colors, Center.XCenter(table))

            print('\033[H\033[J', end = '')
            print(
                '\n'.join([
                    self.text['top'],
                    '',
                    Colorate.Format(Center.XCenter(banner), self.banner_second_chars, fade_mode['banner'], self.colors, Col.white),
                    '',
                    self.text['middle'],
                    '',
                    colored_table,
                    '',
                    self.text['bottom']
                ])
            )
            cmd = Write.Input(self.input, self.colors, 0.005).strip()
            if cmd == '/': left_panel.listen() if type(left_panel) == Panel else left_panel()
            if cmd not in [str(num) for num in range(len(self.instructions))]:
                _log(f'Command {cmd} not found')
                Colorate.Error(self.command404.replace(':cmd:', cmd))
                continue
            command = self.instructions[int(cmd)][1]
            context = Context(self, command)

            class UnknownException(Exception):
                def __init__(self, *args, **kw) -> None:
                    super().__init__(*args, **kw)

            __UnknownException = ...

            try: raise UnknownException() from None
            except UnknownException as _UnknownException: globals()['__UnknownException'] = _UnknownException

            if type(command) == Panel:
                command.listen(context, left_panel = self)
            else:
                prog.update(self, command)
                try: command(context)
                except (Exception, BaseException) as error: _events['onError'](context, error)
                except: _events['onError'](context, __UnknownException)
                _log(f'Command {command} executed')
            input()

    def MakeOutText(self, top: str = None, middle: str = None, bottom: str = None, left: str = None, right: str = None, bottom_left: str = None, bottom_right: str = None) -> None:
        r"""
        Make the text for the panel

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
        """
        if top: self.text['top'] = Center.XCenter(top)
        if middle: self.text['middle'] = Center.XCenter(middle)
        if bottom: self.text['bottom'] = Center.XCenter(bottom)
        self.text['left'] = left
        self.text['right'] = right
        self.text['bottom_left'] = bottom_left
        self.text['bottom_right'] = bottom_right
        self.render()
        _log(f'Made out text for {self.name}')


    def __str__(self):
        r"""
        Return the panel name
        """
        return self.name

    def __repr__(self):
        r"""
        Return the short string representation of the panel
        """
        return f'<panel {self.name}>'

    def __add__(self, other):
        r"""
        Return a custom panel that take the second one to merge the instructions in the first one
        """
        if type(other) == Panel:
            newPanel = self
            newPanel.instructions.extend(other.instructions)
            newPanel.render()
            return newPanel
        else:
            return NotImplemented

    @_preview
    def to_bytes(self) -> bytes:
        r"""
        Convert the panel to bytes
        """
        return b''

    @staticmethod
    @_preview
    def from_bytes(bytes: bytes) -> 'Panel':
        r"""
        Return a panel from a bytes object
        """
        ...

class Program():
    r"""
    The program class
    """

    def __init__(self, name: str, version: str, authors: tuple[str, ...], description: str, license: tuple, **options) -> None:
        self.name = name
        self.version = tuple(int(num) for num in version.split('.'))
        self.authors = authors
        self.description = description
        self.license = license
        self.panel = ...
        self.options = options
        self.last_command = None

        progInfos = {'name': self.name, 'version': self.version, 'authors': self.authors, 'description': self.description, 'license': self.license}
        _log(f'Added program {progInfos}')

    def update(self, panel: Panel = None, command: Command = None) -> None:
        r"""
        Update the current panel
        """
        self.panel = panel
        if command:
            self.last_command = command
        if titleEnabled:
            title = title_format.replace(
                r':name:', self.name
            ).replace(
                r':version:', '.'.join(str(num) for num in self.version)
            ).replace(
                r':authors:', ', '.join(self.authors)
            ).replace(
                r':description:', self.description
            ).replace(
                r':license:', self.license
            ).replace(
                r':panel:', panel.name
            ).replace(
                r':cmd:', command.name if command else ''
            )
            for key, value in self.options.items():
                title = title.replace(fr':{key}:', str(value))
            System.Title(title)
            _log(f'Set title to {title}')


class _windows():
    msgbox_type_info = 64
    msgbox_type_warning = 48
    msgbox_type_alert = 16

    msgbox_buttons_ok = 0
    msgbox_buttons_ok_cancel = 1
    msgbox_buttons_yes_no_cancel = 2
    msgbox_buttons_yes_no = 3

    msgbox_response_default = 0
    msgbox_response_ok = 1
    msgbox_response_cancel = 2
    msgbox_response_abort = 3
    msgbox_response_yes = 6
    msgbox_response_no = 7

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    psapi = ctypes.windll.psapi
    shell32 = ctypes.windll.shell32

    def __init__(self, *args, **kw) -> None:
        for key, value in vars(_windows).items():
            try: setattr(self, key, value)
            except: pass

    @_windows_feature
    def show_box(type: str, title: str, text: str, buttons: int) -> int:
        r"""
        Show a message box
        """
        msgbox = ctypes.windll.user32.MessageBoxW # ctypes.windll.user32.MessageBoxW
        msgbox.restype = UINT
        msgbox.argtypes = (HWND, LPWSTR, LPWSTR, UINT)
        result = msgbox(None, text, title, type | buttons)
        if not result:
            result = Windows.msgbox_response_default
        return result

    @_windows_feature
    def show_error(title: str, text: str) -> None:
        r"""
        Show an error message box
        """
        Windows.show_box(Windows.msgbox_type_alert, title, text, Windows.msgbox_buttons_ok)

    @_windows_feature
    def show_warning(title: str, text: str) -> None:
        r"""
        Show a warning message box
        """
        Windows.show_box(Windows.msgbox_type_warning, title, text, Windows.msgbox_buttons_ok)

    @_windows_feature
    def show_info(title: str, text: str) -> None:
        r"""
        Show an info message box
        """
        Windows.show_box(Windows.msgbox_type_info, title, text, Windows.msgbox_buttons_ok)

    @_windows_feature
    @property
    def console_title(self) -> str:
        r"""
        Get the current window title
        """
        max = 255
        buffer = ctypes.create_unicode_buffer(max)
        ctypes.windll.kernel32.GetConsoleTitleW(buffer, max)
        return buffer.value

    @_windows_feature
    def show_notification(title: str, message: str, icon: bytes = None, wait_end: bool = False) -> None:
        if icon:
            open(f'{_cache}/__icon.pypanel', 'a+').close()
            with open(f'{_cache}/__icon.pypanel', 'rb') as icon_file: icon_file.write(b64decode(icon))
        toast = ToastNotifier()
        toast.show_toast(title, message, f'{_cache}/__icon.pypanel' if icon else None, duration = 5, threaded = not wait_end)
        if icon: remove(f'{_cache}/__icon.pypanel')

Windows = _windows()

prog: Program

__all__ = [obj for obj in globals() if (str(obj)[0] != '_' or str(obj)[-1] != '__')]