import time
import threading

def get_user_input():
    global skip
    while True:
        user_input = input("Do you want to skip the countdown? (y/n): \n").strip()
        if user_input.lower() == 'y':
            skip = True
            break

def countdown_timer(seconds):
    global skip
    skip = False
    input_thread = threading.Thread(target=get_user_input)
    input_thread.daemon = True
    input_thread.start()
    incorrect_responses = 0

    try:
        for i in range(seconds, -1, -1):
            minutes, secs = divmod(i, 60)
            time_formatted = f"{minutes:02}:{secs:02}"
            print(f"\rTime remaining: {time_formatted} ", end='', flush=True)

            if i == 0 :
                print("\nTime's up!")
                break
            
            if skip:
                print("\nSkipping Countdown...")
                break


           

    except KeyboardInterrupt:
        print("\nTimer stopped by user.")
        print("Skipping countdown...")
        time.sleep(3)

if __name__ == "__main__":
    countdown_timer(15)