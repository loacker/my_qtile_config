# Copyright (c) 2015 Matteo Piccinini [l0aCk3r]

from libqtile.config import Key, Screen, Group, Drag, Click, hook, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
import os
import subprocess

mod = "mod4"
alt = "mod1"
printkey = "Print"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "h", lazy.layout.previous()),
    Key([mod], "l", lazy.layout.next()),

    # MonadTall layout
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "o", lazy.layout.shrink()),
    Key([mod, "shift"], "space", lazy.layout.flip()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),

    # Move windows from stack to stack
    #Key([mod, "shift"], "l", lazy.layout.client_to_next()),
    #Key([mod, "shift"], "h", lazy.layout.client_to_previous()),

    # Vertical and MonadTall layout
    Key([mod], 'm', lazy.layout.maximize()),
    Key([mod], 'n', lazy.layout.normalize()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle floating
    Key([mod], "t", lazy.window.toggle_floating()),

    # Toggle full screen
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    # This should be usefull when floating windows get buried
    Key([alt], "grave", lazy.window.bring_to_front()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),

    # Kill a window
    Key([mod], "w", lazy.window.kill()),

    # Restart or shutdown qtile
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # Run command
    Key([mod], "r", lazy.spawncmd()),

    # Dual monitor
    Key([mod, alt], "Tab", lazy.window.to_next_screen()),  # Don't work
    Key([mod, alt], "1", lazy.to_screen(0), lazy.group.toscreen(0)),
    Key([mod, alt], "2", lazy.to_screen(1), lazy.group.toscreen(1)),

    # Decrease ratio of current window
    Key([mod, "shift"], "l", lazy.layout.decrease_ratio()),

    # Increase ratio of current window
    Key([mod, "shift"], "h", lazy.layout.increase_ratio()),

    # Spin up applications
    Key([mod], "Return", lazy.spawn("urxvt")),
    Key([alt], "c", lazy.spawn("urxvt -e weechat-curses")),
    Key([alt], "d", lazy.spawn("firefox-bin")),
    Key([alt], "g", lazy.spawn("chromium")),
    Key([alt], "s", lazy.spawn("skype")),
    Key([alt], "m", lazy.spawn("thunderbird-bin")),
    Key([alt], printkey, lazy.spawn("scrot -sb '%d-%m-%Y_%H-%M-%S_$wx$h_scrot_selection.png' -e 'mv $f ~/pictures/screenshots'")),
    Key([mod], printkey, lazy.spawn("scrot -ub '%d-%m-%Y_%H-%M-%S_$wx$h_scrot_window.png' -e 'mv $f ~/pictures/screenshots'")),
]

#groups = [Group(i) for i in "123456890"]

# Use "xprop WM_CLASS" command to retrieve the wm_class attribute of a window
groups = [
    Group("1", matches=[
        Match(wm_class=["URxvt"])]),
    Group("2", matches=[
        Match(wm_class=["Firefox"]),
        Match(wm_class=["chromium-browser-chromium"])]),
    Group("3", matches=[
        Match(wm_class=["Thunderbird"]),
        Match(wm_class=["Skype"])]),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
    Group("0", matches=[
        Match(wm_class=["rdesktop"])]),
]

for i in groups:
    # mod1 + number of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + number of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.VerticalTile(),
    layout.Stack(num_stacks=2),
    layout.MonadTall(),
]

widget_defaults = dict(
    font='Andale',
    fontsize=12,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Sep(),
                widget.TaskList(),
                widget.Sep(),
                widget.Prompt(),
                widget.Systray(),
                widget.Volume(),
                widget.NetGraph(),
                widget.Backlight(backlight_name='intel_backlight'),
                widget.HDDBusyGraph(device='sdb'),
                widget.BatteryIcon(),
                widget.MemoryGraph(graph_color='FF0101'),
                widget.CPUGraph(),
                widget.Sep(),
                widget.Clock(format='%d/%m/%Y %a %I:%M %p'),
            ],
            25,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Sep(),
                widget.TaskList(),
                widget.Sep(),
                widget.Prompt(),
                widget.Systray(),
                widget.Volume(),
                widget.NetGraph(),
                widget.Backlight(backlight_name='intel_backlight'),
                widget.HDDBusyGraph(),
                widget.BatteryIcon(),
                widget.MemoryGraph(graph_color='FF0101'),
                widget.CPUGraph(),
                widget.Sep(),
                widget.Clock(format='%d/%m/%Y %a %I:%M %p'),
            ],
            25,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


@hook.subscribe.client_new
def floating(window):
    floating_types = ['notification', 'toolbar', 'splash', 'dialog']
    transient = window.window.get_wm_transient_for()
    if window.window.get_wm_type() in floating_types or transient:
        window.floating = True


@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
        qtile.cmd_restart()


# Run startup script
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
wmname = "LG3D"


# vim: set ts=8 sw=4 sts=4 tw=79 ff=unix ft=python et ai :
