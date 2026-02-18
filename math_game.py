import sys
import time
import random
import select
import termios
import tty

# --- Configuration ---
START_TIME = 6.0
MIN_TIME = 1.5
BEEP_THRESHOLD = 3.0  # Seconds remaining to start beeping


def get_question(score):
    """Generates math questions based on the current score."""
    if score < 10:
        # Level 1: Single digits
        a, b = random.randint(1, 9), random.randint(1, 9)
    elif score < 15:
        # Level 2: Mix of single and double digits
        a = random.randint(5, 20)
        b = random.randint(1, 15)
    else:
        # Level 3: Strictly double digits
        a, b = random.randint(10, 50), random.randint(10, 50)

    op = random.choice(["+", "-"])
    if op == "-":
        if a < b:
            a, b = b, a  # Keep it simple, no negative answers

    question_text = f"{a} {op} {b}"
    answer = eval(question_text)
    return question_text, str(answer)


def flush_input():
    """Clears any stray keystrokes from the terminal buffer."""
    termios.tcflush(sys.stdin, termios.TCIFLUSH)


def play_game():
    score = 0
    current_allowed_time = START_TIME

    print("\n" + "=" * 30)
    print(" READY? 3-SECOND COUNTDOWN!")
    print("=" * 30)
    for i in range(3, 0, -1):
        print(f"       Starting in... {i}", end="\r")
        time.sleep(1)
    print("\n       GO!                     ")

    while True:
        question, correct_answer = get_question(score)
        start_time = time.time()
        user_answer = ""
        last_beep_second = int(current_allowed_time) + 1

        # UI Refresh and Input Loop
        while True:
            elapsed = time.time() - start_time
            remaining = current_allowed_time - elapsed

            if remaining <= 0:
                print(f"\n\n[!] TIME'S UP! The answer was {correct_answer}.")
                return score

            # Tension Beep (ASCII Bell)
            if remaining <= BEEP_THRESHOLD and int(remaining) < last_beep_second:
                sys.stdout.write("\a")  # System beep
                sys.stdout.flush()
                last_beep_second = int(remaining)

            # Draw the Time Bar
            bar_length = 20
            filled = int((remaining / current_allowed_time) * bar_length)
            bar = "█" * filled + "-" * (bar_length - filled)

            # Use ANSI escape to keep the question static and update the bar
            sys.stdout.write(f"\rQUESTION: {question} = {user_answer}")
            sys.stdout.write(f"    TIME: [{bar}] {remaining:.1f}s  ")
            sys.stdout.flush()

            # Check for key presses without pausing the code
            if select.select([sys.stdin], [], [], 0.05)[0]:
                char = sys.stdin.read(1)
                if char in "\n\r":  # User pressed Enter
                    break
                elif char in "\x7f":  # Backspace handling
                    user_answer = user_answer[:-1]
                else:
                    user_answer += char

        # Check Answer
        if user_answer.strip() == correct_answer:
            score += 1
            # Adjust complexity: reduce time every correct answer
            if score > 15:
                current_allowed_time = max(MIN_TIME, current_allowed_time - 0.2)
            elif score > 5:
                current_allowed_time = max(3.0, current_allowed_time - 0.1)

            # Quick visual flash for correct answer
            sys.stdout.write("\r" + " " * 60 + "\r")
            sys.stdout.flush()
        else:
            print(f"\n\n[!] WRONG! The correct answer was {correct_answer}.")
            return score


def main():
    while True:
        print("\n" + "*" * 30)
        print("      MATH-OUT TERMINAL")
        print("*" * 30)
        choice = input("Would you like to play? (Y/N): ").strip().lower()

        if choice == "y":
            # Set terminal to raw mode to capture single keys
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                final_score = play_game()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            print(f"\nGAME OVER! Your score: {final_score}")
        else:
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()
