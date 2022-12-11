# Advent Of Code `aoc-cli`

### from the author of aoc:

Site: [https://adventofcode.com/](https://adventofcode.com/)

> Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as a speed contest, interview prep, company training, university coursework, practice problems, or to challenge each other.

## Why?

This is my attempt on completing AOC 2021. By doing so i created this cli toolkit for ease of managing the codes and sets 
of input for the puzzlesets, written in about 3 days in total. All other attempt before deciding on making this cli program can be accessed in `_old` folder.

note: *this repo only has some of my attempt on AOC2021*, and this tool doesn't do any active request to get all puzzle data from the main site. thus all inputs should be copy-pasted manually.

## Does it work?

Kind of, it's far from perfect. there're still lots of things to be improved.

## How?

tested on python 3.8.5, clone or download this whole repo under the branch `main`

#### examples:

* Run puzzle instance on day 12 with test inputs
  ```sh
  python aoc.py -d 12 --test
  ```

* Create new instance of puzzle (with prefix `day`) within year 2020 container
  ```sh
  python aoc.py --create -y 2020
  ```

* (Help)
  ```sh
  python aoc.py -h
  ```

### Stats

#### 2021 

| Day  | Stars | | Day  | Stars | | Day  | Stars |
| :-:  | :---: |-| :-:  | :---: |-| :-:  | :---: |
|  1   |  **   | |  11  |       | |  21  |  *    |
|  2   |  **   | |  12  |       | |  22  |       |
|  3   |       | |  13  |       | |  23  |       |
|  4   |  **   | |  14  |       | |  24  |       |
|  5   |  **   | |  15  |       | |  25  |       |
|  6   |  *    | |  16  |       | |      |       |
|  7   |  **   | |  17  |       | |      |       |
|  8   |  *    | |  18  |       | |      |       |
|  9   |  **   | |  19  |       | |      |       |
|  10  |  **   | |  20  |       | |      |       |



#### 2022 

| Day  | Stars | | Day  | Stars |
| :-:  | :---: |-| :-:  | :---: |
|  1   |  **   | |  11  |  **   |
|  2   |  **   | |  12  |       |
|  3   |  **   | |  13  |       |
|  4   |  **   | |  14  |       |
|  5   |  **   | |  15  |       |
|  6   |  **   | |  16  |       |
|  7   |  **   | |  17  |       |
|  8   |  **   | |  18  |       |
|  9   |       | |  19  |       |
|  10  |  **   | |  20  |       |

