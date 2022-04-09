import driving_mode
import readchar
import os


def get_ch():
    ch = readchar.readchar()
    return ch


if __name__ == '__main__':
    print("Welcome to PiCar")
    key = ""
    while True:
        print("Main Menu:")
        print("Select the driving mode for the PiCar.")
        print("Press '1' for autonomous driving or '2' for manual driving")
        print("To exit the program, press 'x'")
        key = ""
        key = get_ch()
        if key != 'x':
            if key == '1':
                driving_mode.run_autonomous_mode()
            elif key == '2':
                driving_mode.run_manual_mode()
            else:
                print("Invalid input")

            os.system('clear')
        else:
            break
