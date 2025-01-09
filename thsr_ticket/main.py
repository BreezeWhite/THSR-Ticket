import sys
import time
import random
import signal

sys.path.append("./")

from thsr_ticket.controller.booking_flow import BookingFlow

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    global running
    running = False

def main():
    print("Press Ctrl+C to exit the program.")
    
    flow = BookingFlow()
    global running
    running = True

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    while running:
        try:
            status = flow.run()
            if status == 'Finish':
                break
            time.sleep(random.randint(3, 5))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()