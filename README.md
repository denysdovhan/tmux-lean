# tmux-lean

A small, terminal-aware tmux theme with process icons for every pane.

## Install

Requires **tmux 3.6+**, a **Nerd Font**, and **macOS `pmset`** for the battery.
Automatic light/dark colors require a terminal that reports its theme to tmux;
otherwise the dark palette is used. ANSI colors follow your terminal palette.

Add to your `tmux.conf` before TPM initialization:

```tmux
set -g @plugin 'denysdovhan/tmux-lean'
```

Then press **prefix + I** to install with [TPM](https://github.com/tmux-plugins/tpm).
Put the theme before `tmux-continuum`, if used, so continuum can add its save hook
to `status-right` after the theme loads. Keep TPM initialization at the bottom:

```tmux
run '~/.config/tmux/plugins/tpm/tpm'
```

That path assumes `~/.config/tmux/tmux.conf`. For `~/.tmux.conf`, TPM normally lives
at `~/.tmux/plugins/tpm/tpm` instead.

## Behavior

- Yellow session block; each window shows its number, all pane icons, then name.
- Active windows use brand-colored icons and an inverted light/dark background.
- Flat vertical dividers meet the colored blocks without background gaps.
- Right side: battery and hostname only, on a black background in light mode
  and a light background in dark mode.
  Battery icon and percentage text are red below 10%,
  orange below 25%, yellow below 50%, and green otherwise. The charging icon
  appears only while charging. Hostname text is light in light mode and dark
  in dark mode; dividers use ANSI gray (`colour8`).

Window names stay editable. Process icons use tmux's foreground command, not
the language of an open file or programs hidden behind another runtime.
Native tmux lookups are generated once per reload; only the battery uses a
status command. Keybindings and terminal settings remain yours.

## Customize

Edit `theme.conf` for colors, UI icons, separators, and status formats. Edit
`processes.conf` for process regexes, Nerd Font glyphs, and brand colors on dark
and light backgrounds; later matching rows win. Unknown commands use the
terminal icon. The active window inverts the terminal's background, so its
brand colors use the opposite background column.

Reload your tmux configuration after edits. With XDG configuration:

```sh
tmux source-file ~/.config/tmux/tmux.conf
```

These files are in TPM's `tmux-lean` directory. Keep a fork for lasting edits;
local edits can conflict with plugin updates.

## Portability and tests

Tested on macOS with tmux 3.6b. The battery script requires `pmset`; there is no
Linux battery backend. Machines with no reported battery show no battery text.
Other systems and terminal/font combinations are unverified.

Tests use Python 3's standard library. The loading check starts and stops its
own isolated tmux server; it does not touch your sessions.

```sh
python3 tests/test_tmux_battery.py
python3 tests/test_tmux_theme.py
```
