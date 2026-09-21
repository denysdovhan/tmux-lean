"""Check plugin loading and formats on a disposable tmux server."""
from pathlib import Path
import shlex
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='tmux-lean-') as directory:
  socket = str(Path(directory) / 'socket')
  # A spaced path checks quoting independently of the checkout location.
  plugin = Path(directory) / 'theme with spaces'
  plugin.symlink_to(root, target_is_directory=True)

  def tmux(*args):
    return subprocess.check_output(
      ['tmux', '-S', socket, *args], text=True).removesuffix('\n')

  def option(name):
    return tmux('show-options', '-gv', name)

  def render(value):
    return tmux('display-message', '-p', value)

  try:
    tmux('-f', '/dev/null', 'new-session', '-d', '-s', 'lean', '-n', 'editor')
    tmux('run-shell', shlex.quote(str(plugin / 'lean.tmux')))
    assert option('@battery-script') == str(plugin / 'battery.sh')
    assert option('@muted-colour') == 'colour8'
    assert render('#{E:@host-style}') == 'fg=colour7,bg=default,nobold'
    assert option('window-status-separator') == ''
    assert option('status-left').endswith('#S#{E:@window-separator}')
    assert option('window-status-current-format').endswith('#{E:@window-separator}')
    assert option('status-right') == (
      '#[fg=#{E:@status-fg},bg=default,nobold]#{E:@battery}'
      '#{E:@info-separator}#[#{E:@host-style}] #{E:@host} ')

    # Substitute command formats to test aliases without launching runtimes.
    for command, glyph in [('node', ''), ('npm', ''), ('python3.13', ''),
                           ('g++', ''), ('nvim', ''), ('unknown', '')]:
      expression = option('@pane-icon').replace('#{pane_current_command}', command)
      assert render(expression) == glyph, command

    for light, background, foreground, brand in [
        ('0', 'colour0', 'colour7', '#356b1f'),
        ('1', 'colour7', 'colour0', '#5faf35')]:
      tmux('set', '-g', '@is-light', light)
      assert render('#{E:@status-bg}') == background
      assert render('#{E:@status-fg}') == foreground
      assert render('#{E:@host-style}') == f'fg={foreground},bg=default,nobold'
      assert render('#{E:@colour-node}') == brand

    tmux('split-window', '-h', '-d')
    tmux('set', '-g', '@pane-icon', 'ICON')
    assert render('#{E:@window-icons}') == 'ICON ICON '
    label = render('#{E:window-status-current-format}')
    assert label.count('ICON') == 2 and label.index('0 ') < label.index('ICON')
    assert label.index('ICON') < label.index('editor')
    tmux('run-shell', shlex.quote(str(plugin / 'lean.tmux')))
    assert option('@is-light') == '#{==:#{client_theme},light}'
    assert '#{pane_current_command}' in option('@pane-icon')
  finally:
    subprocess.run(['tmux', '-S', socket, 'kill-server'], check=False)
print('Plugin load, reload, palettes, aliases, all-pane icons, and layout passed.')
