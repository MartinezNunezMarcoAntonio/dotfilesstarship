
from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.layout.floating import Floating
from libqtile.lazy import lazy
from libqtile import hook
from datetime import datetime as dt
from datetime import timezone
import os
import subprocess
from libqtile.log_utils import logger


def get_monitors():
    xr = subprocess.check_output('xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


monitors = get_monitors()

# Run autorandr --change and restart Qtile on screen change
@hook.subscribe.screen_change
def set_screens(event):
    subprocess.run(["autorandr", "--change"])
    qtile.restart()

# When application launched automatically focus it's group
@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) ) #+ suffix(t.day))


def custom_date():
    return custom_strftime('{S} %B %Y - %H:%M', dt.now())


mod = "mod4"

terminal = 'kitty'
home = os.path.expanduser('~')

MYCOLORS = [
    '#073642',
    '#dc322f',
    '#00ff2a',
    '#b58900',
    '#268bd2',
    '#d33682',
    '#2aa198',
    '#eee8d5'
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]

keys = [

    Key([mod], "g",
        lazy.screen.next_group(skip_empty=True),
        desc="Move to next active group"
        ),
    Key([mod, "shift"], "g",
        lazy.screen.prev_group(skip_empty=True),
        desc="Move to previous active group"
        ),
    # Basic movements
    Key([mod], "k",
        lazy.layout.up(),
        desc="Move focus down in stack pane"
        ),
    Key([mod], "j",
        lazy.layout.down(),
        desc="Move focus up in stack pane"
        ),
    Key([mod], "h",
        lazy.layout.left(),
        desc="Move focus left in stack pane"
        #lazy.layout.shuffle_left(),
        #desc='Shuffle left'
        ),
    Key([mod], "l",
        lazy.layout.right(),
        desc="Move focus right in stack pane"
        #lazy.layout.shuffle_right(),
        #desc='Shuffle right'
        ),

    #Managment Size monadtall 
    Key([mod, "mod1"], "Up",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    Key([mod, "mod1"], "Down",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),


    #Shift Movements increase size
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc='Shuffle right'
        ),
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc='Shuffle left'
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc='Shuffle down'
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc='Shuffle up'
        ),
    #Movimientos para BSP
    Key([mod, "mod1"], "j",
        lazy.layout.flip_down(),
        desc='Flip down'
        ),
    Key([mod, "mod1"], "k",
        lazy.layout.flip_up(),
        desc='Flip up'
        ),
    Key([mod, "mod1"], "h",
        lazy.layout.flip_left(),
        desc='Flip left'
        ),
    Key([mod, "mod1"], "l",
        lazy.layout.flip_right(),
        desc='Flip right'
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        desc='Grow down'
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        desc='Grow up'
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        desc='Grow left'
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        desc='Grow right'
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
        ),
    #Para Monadtall
    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
        ),

    # Toggle floating
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),
        desc="Toggle floating"
        ),

    # Toggle Fullscreen
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        lazy.hide_show_bar(position='all'),
        desc='Toggle fullscreen and the bars'
        ),

    #STACK
    # Switch window focus to other pane(s) of stack by CHANGE STACK
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"
        ),

    # Swap panes of split stack
    Key([mod, "shift"], "space",
        lazy.spawn("/home/XMX1946/.config/scriptchangelayoutlenguage.sh"),
        ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
        ),
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"
        ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
        ),
    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"
        ),

    # Toggle bars
    Key([mod], "b",
        lazy.spawn("microsoft-edge-stable"),
        #lazy.hide_show_bar(position='all'),
        desc="navegador"
        ),

    # Qtile system keys
    Key([mod, "shift", "control"], "l",
        lazy.spawn("betterlockscreen -l"),
        desc="Lock screen"
        ),
    Key([mod, "control"], "r",
        lazy.restart(),
        desc="Restart qtile"
        ),
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown qtile"
        ),
    Key([mod], "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"
        ),
    Key([mod, "control"], "p",
        lazy.spawn("" + home + "/.local/bin/powermenu"),
        desc="Launch Power menu"
        ),

    # Rofi
    Key([mod], "p",
        lazy.spawn("rofi -show drun"),
        desc="Launch Rofi menu"
        ),

    # Cycle through windows in the floating layout
    Key([mod, "shift"], "i",
        lazy.window.toggle_minimize(),
        lazy.group.next_window(),
        lazy.window.bring_to_front()
        ),

    # ------------ Hardware Configs ------------
    # Volume
    Key([mod], "minus", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([mod], "equal", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),

    # Screenshots
    Key([], "Print",
        lazy.spawn("escrotum " + home + "/Pictures/Screenshots/%Y%m%d_%H%M%S.png"),
        lazy.spawn("notify-send 'Screenshot'"),
        desc='Save screen to screenshots folder'
        ),
    # Capture region of screen to clipboard
    Key([mod], "s",
        lazy.spawn("escrotum -Cs"),
        desc='Capture region of screen to clipboard'
        ),
]

# Groups with matches

workspaces = [
    {"name": "1", "spawn":[], "label":" ₁","key": "1", "matches": [], "layout": "monadtall"},
    {"name": "2", "spawn":[], "label":" ₂","key": "2", "matches": [Match(wm_class='ranger')], "layout": "monadtall"},
    {"name": "3", "spawn":[], "label":" ₃","key": "3", "matches": [Match(wm_class='vim')], "layout": "monadtall"},
    {"name": "4", "spawn":[], "label":" ₄","key": "4", "matches": [Match(wm_class='telegram-desktop')], "layout": "monadtall"},
    {"name": "5", "spawn":[], "label":" ₅","key": "5", "matches": [Match(wm_class='gimp-2.10')], "layout": "monadtall"},
    {"name": "6", "spawn":"pavucontrol", "label":" ₆","key": "6", "matches": [Match(wm_class='pavucontrol')], "layout": "monadtall"},
    {"name": "7", "spawn":[], "label":" ₇","key": "7", "matches": [Match(wm_class='libreoffice')], "layout": "monadtall"},
    {"name": "8", "spawn":[], "label":" ₈","key": "8", "matches": [Match(wm_class='newsboat')], "layout": "monadtall"},
    {"name": "9", "spawn":[], "label":" ₉","key": "9", "matches": [Match(wm_class='neomutt')], "layout": "monadtall"},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    layouts = workspace["layout"] if "layout" in workspace else None
    spawns = workspace["spawn"] if "spawn" in workspace else None
    label = workspace["label"] if "label" in workspace else None
    groups.append(Group(name=workspace["name"],spawn=spawns,label=label, matches=matches, layout=layouts ))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"])))

# Move window to screen with Mod, Alt and number


for i in range(monitors):
    keys.extend([Key([mod, "mod1"], str(i), lazy.window.toscreen(i))])

# DEFAULT THEME SETTINGS FOR LAYOUTS #
layout_theme = {"border_width": 3,
                "margin": 16,
                "border_focus": BLUE,
                "border_normal": BLACK
                }

layouts = [
    layout.MonadTall(**layout_theme, single_border_width=0),
    layout.Stack(num_stacks=2, **layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Bsp(**layout_theme),
    #layout.Columns(**layout_theme),
    #layout.Floating(**layout_theme),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='RobotoMono Roboto FiraCode Nerd Font Regular',
    fontsize='14',
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = []



for monitor in range(monitors):
    if monitor == 0:
        screens.append(
            Screen(
                top=bar.Bar(
                    [
                        widget.Spacer(length=10),
                        widget.GroupBox(borderwidth=2, inactive='969696', this_current_screen_border=GREEN, this_screen_border='eee8d5', font='RoboMono FiraCode Nerd Font', fontsize=19, highlight_method='line', highlight_color=['000000', '000000']),
                        widget.CurrentLayoutIcon(scale=0.6),
                        widget.CurrentLayout(**widget_defaults),
                        widget.Prompt(**widget_defaults),
                        widget.Spacer(),
                        widget.GenPollText(func=custom_date, update_interval=1, **widget_defaults, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh show"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh edit"), shell=True)}),
                        widget.Spacer(),
                        widget.Net(interface='enp39s0', format='{down} ↓↑ {up}', prefix='M'),
                        widget.Spacer(length=5),
                        widget.Mpris2(
                            name='spotify',
                            objname="org.mpris.MediaPlayer2.spotify",
                            display_metadata=['xesam:title', 'xesam:artist'],
                            scroll_chars=None,
                            stop_pause_text='',
                            **widget_defaults
                        ),
                    ],
                    28, background="#000000AA", margin=[10, 16, 0, 16]  # N E S W
                ),
            )
        )
else:
    screens.append(
        Screen(
            top=bar.Bar(
                [
                    widget.Spacer(),
                    widget.GenPollText(func=custom_date, update_interval=1, **widget_defaults, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh show"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh edit"), shell=True)}),
                    widget.Spacer(),
                ],
                28, background="000000AA", margin=[10, 16, 0, 16]  # N E S W
            ),
        )
    )


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # *layout.Floating.default_float_rules,
    Match(title='Quit and close tabs?'),
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='Conky'),
    Match(wm_class='Firefox'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "Qtile"
