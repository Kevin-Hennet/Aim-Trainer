# Aim Trainer

A reflex and precision game built with Pygame. Click the green targets before time runs out — avoid the red bombs, or it's game over. Each round gets faster and harder, with smaller targets, bigger bombs, and more of both on screen at once.

## Gameplay

- Click **green circles** (targets) to score points and clear the round.
- Avoid clicking **red circles** (bombs) — one hit ends the game.
- Clear all targets before the round timer hits zero to advance to the next round.
- If time runs out while targets remain, the game ends.
- Your score and time remaining are shown in the top-left corner throughout.

## Difficulty Scaling

Every round increases the challenge:

- **Round timer** shrinks (down to a minimum floor).
- **Target radius** shrinks, making targets harder to hit.
- **Bomb radius** grows, making bombs harder to avoid.
- **Number of targets and bombs** on screen increases (up to a cap).

All circles move continuously and bounce off the screen edges, so targets and bombs are always in motion.

## Requirements

- Python 3
- [Pygame](https://www.pygame.org/)

Install Pygame if you don't already have it:

```bash
pip install pygame
```

## How to Run

```bash
python aim_trainer.py
```

(Replace `aim_trainer.py` with whatever you've named the script file.)

## Controls

| Action | Input |
|---|---|
| Hit a target/bomb | Left mouse click |
| Quit | Close the window |

## Project Structure

This is a single-file script containing:

- **Game loop** — handles events, updates positions, draws the screen, and checks round state each frame.
- **`fill_list()`** — generates the starting targets and bombs for a round with randomized position, direction, and size.
- **`move()`** — updates circle positions each frame and bounces them off the screen edges.
- **`draw()`** — renders all circles to the screen.
- **`handle_round()`** — determines whether the current round is won, lost, or still in progress.
- **`difficulty_scaling()`** — calculates the timer, target/bomb size, and target/bomb count for the upcoming round.

## Known Limitations / Future Improvements

- No start screen, pause, or restart-without-relaunching — the game ends by closing/printing to the console.
- Feedback on loss/win is currently printed to the terminal rather than shown in the game window.
- No sound effects or visual polish (e.g., particle effects on hit/miss).
- No persistent high-score tracking.
- No difficulty presets or settings menu.

Possible additions:
- In-window game-over/restart screen
- Sound effects and hit animations
- High-score saving to a local file
- Adjustable starting difficulty
- Combo/streak scoring bonuses
