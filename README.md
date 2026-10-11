# PingPong

A local two-player Pong-style game built with Python and Pygame. Players control opposing paddles, with scoring, sound effects, background music, and a restart screen. The first player to reach 10 points wins.

## Run locally

Requires Python 3, Pygame, and a desktop environment with graphics and audio support.

```bash
git clone https://github.com/YumTaha/PingPong.git
cd PingPong
python -m pip install pygame
python Pong.py
```

Run from the repository root so the bundled assets load correctly.

## Controls

| Input | Action |
| --- | --- |
| W / S | Move the green paddle up / down |
| Up / Down arrow | Move the red paddle up / down |
| Escape | Quit |
| Mouse: Yes / No after the match | Restart / quit |

## Files

`Pong.py` contains the game. `audio/`, `background/`, `fonts/`, and `items/` contain its bundled assets.
