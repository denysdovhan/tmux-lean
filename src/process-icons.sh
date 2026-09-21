#!/bin/sh
# Build tmux's conditional lookups at reload time, not on each status refresh.
# Edit processes.conf for icon/color changes; later matching rows take priority.
set -eu
icon='#{E:@icon-terminal}'
colour='#{E:@window-active-fg}'

while read -r name pattern glyph on_dark on_light; do
  case "$name" in ''|\#*) continue ;; esac
  tmux set -g "@icon-$name" "$glyph"
  tmux set -g "@colour-$name" "#{?#{E:@is-light},$on_dark,$on_light}"
  match="#{m/r:^($pattern)$,#{pane_current_command}}"
  icon="#{?$match,#{E:@icon-$name},$icon}"
  colour="#{?$match,#{E:@colour-$name},$colour}"
done < "$(dirname "$0")/processes.conf"

tmux set -g @pane-icon "$icon"
tmux set -g @pane-colour "$colour"
