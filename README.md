# Powder keg — dwm rice for the X61s

Bar layout: **tag digits left · date/clock centre · cpu / mem / battery right.**
No window title, no layout symbol.

| file | what it is |
|---|---|
| `jinxbar-dwm.diff` | dwm patch: 3-zone bar, per-tag colours (`tagcols[]`), colour/rect escapes in the status (no status2d needed) |
| `font/Doodlebomb.ttf` | scrawled digits 1–9 at U+100000–100008 (tags), doodles at U+100010–100018 (status, prompt) |
| `font/build_font.py` | regenerates the font (`pip install shapely fonttools`) |
| `config.jinx.h` | fonts, colours, tags, dmenu — paste over the matching blocks in `config.h` |
| `jinxbar` | status script: clock (centre) + CPU/RAM meters and battery cell (right) |
| `starship.toml` | prompt in the same style — copy to `~/.config/starship.toml` |
| `Xresources.jinx` | 16-colour terminal palette (st / xterm) |
| `jinx.nix` | NixOS module wiring it all together |
| `wallpapers/` | both wallpapers fitted to 1024×768 |

## Setup (NixOS)

1. Copy your current dwm `config.h` next to `jinx.nix` and paste in `config.jinx.h`.
2. Put `Doodlebomb.ttf`, `jinxbar` and `jinxbar-dwm.diff` in the same folder.
3. Add `./jinx.nix` to `imports`, then `sudo nixos-rebuild switch`.
4. Start things from `~/.xinitrc` (or `services.xserver.displayManager.sessionCommands`):

   ```sh
   xrdb -merge ~/.Xresources
   feh --no-fehbg --bg-fill ~/wallpapers/wall-night-1024x768.png
   jinxbar &
   exec dwm
   ```

## How the status works

`jinxbar` sets the root window name to `centre<0x1f>right`. The patched dwm
centres the part before the `0x1f` byte and right-aligns the rest. Without the
separator the whole status goes right, so other status scripts still work.

Escapes understood in either part:

| escape | effect |
|---|---|
| `^c#rrggbb^` / `^b#rrggbb^` | text (and rect) colour / background colour |
| `^d^` | reset colours |
| `^f12^` | move right 12 px |
| `^r0,4,24,10^` | filled rectangle at x,y (relative to the cursor / bar top), w,h |

## Notes

- **Tag colours** come from `tagcols[]` in `config.h` (one entry per tag; the build fails if the counts differ).
  Unselected tags draw the digit in its colour, the selected tag becomes a block of that colour.

- Tested by building dwm 6.4 with the patch and running it on a 1024×768 virtual display.
  If the patch doesn't apply to a newer dwm, the change is self-contained:
  copy `drawstatus()` and `drawbar()` from the diff and edit the two-line click
  check in `buttonpress()` by hand.
- **Bar height** is read from dwm automatically; force it with `JINXBAR_BH=<px>`.
- **Battery path** defaults to `BAT0`; override with `JINXBAR_BAT=/sys/class/power_supply/BAT1`.
- **Low battery**: ≤15 % turns the cell red with a skull; charging shows a bolt.
- `ClkLtSymbol` / `ClkWinTitle` mouse bindings now fire on the empty middle of the bar.
