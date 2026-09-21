"""Run with python3 tests/test_tmux_battery.py; no tmux server required."""
import os
from pathlib import Path
import subprocess
import tempfile

script = Path(__file__).resolve().parents[1] / 'battery.sh'
with tempfile.TemporaryDirectory() as directory:
  mock = Path(directory) / 'pmset'
  mock.write_text('#!/bin/sh\nprintf "%s\\n" "Battery ${LEVEL}%; ${STATE}; present: true"\n')
  mock.chmod(0o755)
  for level, colour in [(0, 'red'), (9, 'red'), (10, 'orange'), (24, 'orange'),
                        (25, 'yellow'), (49, 'yellow'), (50, 'green'), (100, 'green')]:
    for state in ['discharging', 'charging', 'charged', 'AC attached; not charging']:
      env = dict(os.environ, PATH=directory + ':' + os.environ['PATH'],
                 LEVEL=str(level), STATE=state)
      output = subprocess.check_output(
        ['sh', str(script), 'BAT', 'red', 'orange', 'yellow', 'green', 'CHARGING'],
        env=env, text=True)
      icon = 'CHARGING' if state == 'charging' else 'BAT'
      assert output == f'#[fg={colour}] {icon} {level}%\n', output
print('Battery thresholds and charging states passed.')
