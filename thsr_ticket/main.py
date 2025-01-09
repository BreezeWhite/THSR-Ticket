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
    flow = BookingFlow()
    status = flow.run()
    return status

if __name__ == "__main__":
    print("Press Ctrl+C to exit the program.")
    
    status = False
    running = True

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    while running:
        try:
            if status:
                break
            status = main()
            time.sleep(random.randint(3, 5))
        except Exception as e:
            print(e)