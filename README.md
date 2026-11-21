# Space Shooter

A vertical space shooter built with Python and pygame-ce. Shoot the falling enemies, don't let them hit you or slip past, and survive as the levels get harder.

**Play it:**
- Browser (GitHub Pages): https://muhammadatiqsyed-pythonprojects.github.io/space-shooter/
- itch.io: YOUR-ITCH-LINK

## Controls

| Action | Keyboard | Touch / mouse |
|---|---|---|
| Move | Arrow keys or A / D | Hold and drag |
| Shoot | Hold Space | Hold (fires automatically) |
| Pause / resume | P | Tap the pause button, tap to resume |
| Start / retry | P | Tap or click the button |

## Features

- 10 lives, score, levels that get harder as you score, and a best score for the session
- A life is lost when an enemy hits you or gets past you
- Menu, how-to-play, pause and game over screens
- Sprites, sound effects and music
- Playable in the browser, on desktop and on phones

## Run it locally

```bash
git clone https://github.com/muhammadatiqsyed-pythonprojects/space-shooter.git
cd space-shooter
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash); on Mac/Linux use .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Project structure

- `main.py`: game loop and game states
- `settings.py`: all constants (sizes, speeds, colors, paths)
- `player.py`, `bullet.py`, `enemy.py`: game objects
- `button.py`, `ui.py`: menu and text helpers
- `assets/`: images and sounds
- `docs/`: web build served by GitHub Pages
- `build_web.sh`: builds the web version

## Credits

See [CREDITS.md](CREDITS.md).

Built with [pygame-ce](https://pyga.me) and packaged for the web with [pygbag](https://github.com/pygame-web/pygbag).