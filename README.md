Description (in progress)
![ChessPuzzle gif](https://github.com/dmytrokovych/descriptions/blob/main/ChessPuzzle/chess_puzzle.gif)

## General info
ChessPuzzle is a web app that creates personalised chess puzzles based on a user's recent games on [chess.com](https://www.chess.com/). Just enter your chess.com username and receive the puzzles to solve in your browser.

Each puzzle is a position from the user's last games in which the user made a mistake. ChessPuzzles gives an opportunity for the user to fix the mistake and make the correct move. Errors in each game are caught by a chess engine running in the background on a server, after which puzzles (positions and best moves) are saved to a database. The chess engine used for game analysis is open-sourced [Stockfish 14].(https://stockfishchess.org/). 

### Demo
Here is a live demo: [http://34.118.102.169/](http://34.118.102.169/)\
(In case of problems use my username: 'dmytroko' or one of these: 'FabianoCaruana', 'Hikaru')


## Technologies
Project is created with:
- Python 3.9
- Flask
- JavaScript
- HTML/CSS
- SQLite
- Celery
- Redis

## Usage
![ChessPuzzle home](https://github.com/dmytrokovych/descriptions/blob/main/ChessPuzzle/chess_puzzle_1.png)

![ChessPuzzle profile](https://github.com/dmytrokovych/descriptions/blob/main/ChessPuzzle/chess_puzzle_2.png)

![ChessPuzzle puzzle](https://github.com/dmytrokovych/descriptions/blob/main/ChessPuzzle/chess_puzzle_3.png)


### Contribution
To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request
