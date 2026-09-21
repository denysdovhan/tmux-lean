#!/bin/sh
# macOS battery percentage and text color, emitted together to stay in sync.
pmset -g batt | awk -v icon="$1" -v low="$2" -v medium="$3" -v high="$4" -v full="$5" -v charging="$6" '
  match($0, /[0-9]+%/) {
    level = substr($0, RSTART, RLENGTH) + 0
    colour = full
    if (level < 50) colour = high
    if (level < 25) colour = medium
    if (level < 10) colour = low
    if ($0 ~ /; charging;/) icon = charging
    printf "#[fg=%s] %s %d%%\n", colour, icon, level
    exit
  }
'
