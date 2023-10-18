import time
import sys


def countdown_timer(seconds):
    try:
        for i in range(seconds, -1, -1):
            minutes, secs = divmod(i, 60)
            time_formatted = f"{minutes:02}:{secs:02}"
            sys.stdout.write(f"\rTime remaining: {time_formatted}")
            sys.stdout.flush()

            if i == 0:
                print("\nTime's up!")
                break

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTimer stopped by user.")


if __name__=="__main__":
    countdown_timer(90)