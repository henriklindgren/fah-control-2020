# fah-control-2020
A rehauled Folding@Home controller based on the legacy one at https://github.com/FoldingAtHome/fah-control

## Reason to exist
1. Current folding@home client runs in Python 2 and GTK 2 which are EOL and old respectively.
2. Fun and reasonably scoped project for single maintainer to keep running.

## Key features
In order of priority.

| # | What | Why |
| - | ---- | --- |
| 1 | Cross-platform | Folding@home runs on many types of systems.
| 2 | Python | The previous client was written in it which makes porting network code trivial.
| 3 | tkinter | Fallback to tkinter to make installation and running easier.
| 4 | Cheap to maintain | Choices made to keep maintenance down to a few hours per month.

In addition to this PySimpleGUI was choosen because it can fallback to tkinter (#3), it runs on raspberry's allegedly (#1), it's written and runs in Python (#2) and since it doesn't aim to support complex UIs it is designed to create UIs faster than handcoding it in tkinter (at which point we lose the ability to run it in the other outputs PySimpleGUI allows for).

See https://github.com/PySimpleGUI/PySimpleGUI

## Future milestones
1. Ported old fah-control client without major design changes.

2/3. UX enhancements changing from appearance/structure from old client.

2/3. Mod/plugin system, for example to support in UI for leaderboard with changes in position tracked.

## Current progress
| Date | What |
| ---- | ---- |
| 2020-04-18 | Made repository public. Made README contributor friendly. |

## UI Examples
| Legacy client | Current Progress |
| ------------- | ---------------- |
| ![](https://i.imgur.com/TGUL3Hh.png) | ![](https://i.imgur.com/DauJXR3.png) |


## Contribute

Fork the repository and make pull requests from your fork. Create issues on features and bugs.
