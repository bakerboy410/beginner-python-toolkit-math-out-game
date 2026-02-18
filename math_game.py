import sys
import time
import random
import select
import termios
import tty

# --- Configuration ---
START_TIME = 6.0
MIN_TIME = 1.2  # Slightly faster floor for "instant" mode
BEEP_THRESHOLD = 3.0


def get_question(score):
    """Generates math questions based on the current score."""
    if score < 10:
        a, b = random.randint(1, 9), random.randint(1, 9)
    elif score < 15:
        a = random.randint(5, 20)
        b = random.randint(1, 15)
    else:
        a = random.randint(10, 60)
        b = random.randint(10, 60)

    op = random.choice(["+", "-"])
    if op == "-":
        if a < b:
            a, b = b, a

    question_text = f"{a} {op} {b}"
    answer = eval(question_text)
    return question_text, str(answer)


def play_game():
    score = 0
    current_allowed_time = START_TIME

    print("\n" + "=" * 30)
    print(" READY? 3-SECOND COUNTDOWN!")
    print("=" * 30)
    for i in range(3, 0, -1):
        print(f"       Starting in... {i}", end="\r")
        sys.stdout.flush()
        time.sleep(1)
    print("\n       GO!                     ")

    while True:
        question, correct_answer = get_question(score)
        start_time = time.time()
        user_answer = ""
        last_beep_second = int(current_allowed_time) + 1

        while True:
            elapsed = time.time() - start_time
            remaining = current_allowed_time - elapsed

            if remaining <= 0:
                print(f"\n\n[!] TIME'S UP! The answer was {correct_answer}.")
                return score

            # Tension Beep
            if remaining <= BEEP_THRESHOLD and int(remaining) < last_beep_second:
                sys.stdout.write("\a")
                sys.stdout.flush()
                last_beep_second = int(remaining)

            # Draw the Time Bar
            bar_length = 25
            filled = int(max(0, (remaining / current_allowed_time)) * bar_length)
            bar = "█" * filled + "-" * (bar_length - filled)

            # UI Display
            sys.stdout.write(f"\rQUESTION: {question} = {user_answer}")
            sys.stdout.write(f"    TIME: [{bar}] {remaining:.1f}s  ")
            sys.stdout.flush()

            # Non-blocking Key Capture
            if select.select([sys.stdin], [], [], 0.03)[0]:
                char = sys.stdin.read(1)

                if char in "\n\r":  # Enter key
                    if user_answer == correct_answer:
                        break
                    else:
                        print(
                            f"\n\n[!] WRONG! The correct answer was {correct_answer}."
                        )
                        return score
                elif char in "\x7f":  # Backspace
                    user_answer = user_answer[:-1]
                else:
                    user_answer += char

                # --- INSTANT DETECTION ---
                if user_answer == correct_answer:
                    # Brief flash to show success
                    sys.stdout.write(
                        f"\rQUESTION: {question} = {user_answer}  CORRECT! "
                    )
                    sys.stdout.flush()
                    time.sleep(0.15)
                    break
                elif len(user_answer) >= len(
                    correct_answer
                ) and not correct_answer.startswith(user_answer):
                    # If they typed the wrong digit and reached the length limit
                    print(f"\n\n[!] WRONG! The correct answer was {correct_answer}.")
                    return score

        # Leveling Up
        score += 1
        if score > 15:
            current_allowed_time = max(MIN_TIME, current_allowed_time - 0.2)
        elif score > 5:
            current_allowed_time = max(2.5, current_allowed_time - 0.15)

        # Clear line for next question
        sys.stdout.write("\r" + " " * 70 + "\r")
        sys.stdout.flush()


def main():
    while True:
        print("\n" + "*" * 40)
        print("      MATH-OUT: INSTANT EDITION")
        print("*" * 40)
        choice = input("Would you like to play? (Y/N): ").strip().lower()

        if choice == "y":
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                final_score = play_game()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            print(f"\nGAME OVER! Your total score: {final_score}")
            print("-" * 40)
        else:
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()
