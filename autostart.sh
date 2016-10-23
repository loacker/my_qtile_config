#!/bin/sh

xrdb -merge ${HOME}/.Xresources
xmodmap ${HOME}/.Xmodmap

#${HOME}/bin/runonce "$(which xscreensaver) -no-splash"

/usr/bin/urxvt -e screen -R -D -S local &
/usr/bin/urxvt -e weechat-curses &
/usr/bin/firefox &
/usr/bin/chromium-browser -disable-prompt-on-repost &
#/opt/bin/skype &
/opt/bin/telegram &
/usr/bin/thunderbird &
/usr/bin/redshift-gtk -l 52.38:4.83 -t 5700:3600 -g 0.8 -m randr -v &

