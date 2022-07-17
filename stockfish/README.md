1. Download the open source chess engine [Stockfish 14](https://www.dropbox.com/sh/75gzfgu7qo94pvh/AAAZLV-YmwZBDO_NEvaer87pa/Stockfish%2014?dl=0&subfolder_nav_tracking=1) to this directory.

2. Give the path to the executable file in puzzle_generator.py: 

```python
# windows
transport, engine = await chess.engine.popen_uci(r"stockfish\stockfish_win\stockfish_14_x64.exe")
```
```python
# linux
transport, engine = await chess.engine.popen_uci(r"stockfish/stockfish_linux/stockfish_15_x64")
```
