# Python Mathematics Game

## Overview

This is a simple command-line mathematics game where the player is asked basic addition and subtraction questions. The player has a limited amount of time to answer each question, and the time limit decreases as more questions are answered correctly.

## Objective

The objective of this project is to learn Python as a new programming language while improving skills in AI prompting. Generative AI is used to guide the learning process, problem-solving, and implementation of the game.

## Requirements

* Python 3.6 or higher
* Unix-based Operating System
* Standard Pthon Library, no dependancies needed
* ANSI-Compatible Terminal

##Installation
clone the repository
Naviagate to the ***math_out.py*** file
Run the file in the terminal, no installation of libraries needed

## Usage

When the game starts, the player is asked whether they want to play. If the player agrees, the game begins by presenting simple addition or subtraction questions. The player must answer each question within the given time limit. The game ends when the player enters an incorrect answer or runs out of time, and the final score is displayed.

##Example Output 
''' 
****************************************
      MATH-OUT: INSTANT EDITION
****************************************
Would you like to play? (Y/N): Y

==============================
 READY? 3-SECOND COUNTDOWN!
==============================
       Starting in... 1
       GO!                     
QUESTION: 8 + 9 = 1    TIME: [███----------------------] 0.8s         

[!] WRONG! The correct answer was 17.

GAME OVER! Your total score: 4
----------------------------------------

****************************************
      MATH-OUT: INSTANT EDITION
****************************************
Would you like to play? (Y/N): N
Thanks for playing! Goodbye.
''
'
## Common Issue
1. Terminal "Stuck" in Raw Mode
Issue: If the game is force-closed (e.g., Ctrl+C or a terminal crash), your terminal might stop showing what you type or behave erratically.
Reason: The game puts the terminal in cbreak mode to capture keys instantly. If it doesn't exit cleanly, it doesn't "reset" the terminal settings.
Solution: Type the command reset and press Enter. This will restore standard terminal behavior.

2. Audio Not Playing
Issue: The "Tension Beep" isn't audible.
Reason: Modern Linux distributions often disable the "System Bell" (\a) by default.
Solution: Ensure "System Sounds" and "Terminal Bell" are enabled in your Ubuntu/GNOME settings.

3. OS Compatibility
Issue: Game fails to start on Windows cmd.exe.
Reason: The project uses Unix-specific modules (termios, tty, select).
Solution: Windows users should run the game via WSL (Windows Subsystem for Linux) or a Git Bash terminal.
