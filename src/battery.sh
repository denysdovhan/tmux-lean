#!/bin/sh
# macOS battery percentage and background color, emitted together to stay in sync.
pmset -g batt 2>/dev/null | awk -v icon="$1" -v low="$2" -v medium="$3" -v high="$4" -v full="$5" -v charging="$6" -v separator="$7" '
  match($0, /[0-9]+%/) {
    level = substr($0, RSTART, RLENGTH) + 0
    colour = full
    if (level < 50) colour = high
    if (level < 25) colour = medium
    if (level < 10) colour = low
    if ($0 ~ /; charging;/) icon = charging
    printf "#[bg=%s] %s %d%%%s\n", colour, icon, level, separator
    exit
  }
'
