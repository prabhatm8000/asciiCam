import cv2 as cv
from PIL import Image
import os
import sys
import time
import art

DENSITY_STRING = [' ', ' ', ' ', '.', ',', '-', '=', '+', ':', ';', 'c', 'b', 'a',
                  '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '$', 'W', '#', '@', 'N']
DENSITY_STRING_LEN = len(DENSITY_STRING)

# Define ANSI color escape codes
COLOR_RED = '\033[91m'
LIGHT_RED = "\033[1;31m"
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_PURPLE = '\033[95m'
COLOR_CYAN = '\033[96m'
COLOR_RESET = '\033[0m'


def resizeImage(image: Image, newWidth):
    width, height = image.size
    aspectRatio = width/height
    newHeight = int(newWidth / aspectRatio)
    resizeImage = image.resize((newWidth, newHeight))
    return resizeImage


def printChars(imageFrame: Image, newWidth, rgb=False):
    pixels = resizeImage(imageFrame, newWidth).getdata()
    charactersPrintedInLine = 0
    os.system("cls")
    for px in pixels:
        avg = int(sum(px)/len(px))
        # characters.append(DENSITY_STRING[avg // 25])
        if (charactersPrintedInLine == newWidth - 1):
            sys.stdout.writelines("\n")
            charactersPrintedInLine = 0
        else:
            character = DENSITY_STRING[avg // 25]

            # 0 -> blue, 1 -> green, 2 -> red
            # (!bgr) or (b, g and r > 200) or (b, g, and r < 55) -> white
            if (not rgb) or (px[0] > 200 and px[1] > 200 and px[2] > 200) or (px[0] < 55 and px[1] < 55 and px[2] < 55):
                sys.stdout.write(f"{character} ")

            # yellow
            elif (px[1] > px[0] and px[2] > px[0] and px[0] in range(0, 150)):
                sys.stdout.write(f"{COLOR_YELLOW}{character}{COLOR_RESET} ")

            # blue
            elif (px[0] >= px[1] and px[0] > px[2]):
                sys.stdout.write(f"{COLOR_BLUE}{character}{COLOR_RESET} ")

            # green
            elif (px[1] >= px[0] and px[1] > px[2]):
                sys.stdout.write(f"{COLOR_GREEN}{character}{COLOR_RESET} ")

            # red
            else:
                sys.stdout.write(f"{COLOR_RED}{character}{COLOR_RESET} ")
            charactersPrintedInLine += 1
    sys.stdout.write("press ctrl + c to exit\n")


def videoCapure(captureSrc: str | int, rbg=False):
    try:
        print("loading...")
        cap = cv.VideoCapture(captureSrc)
    except FileNotFoundError:
        sys.stdout.writelines("File not found")

    while True:
        isTrue, frame = cap.read()
        if frame is None:
            sys.stdout.writelines("\nCamera or Video stream ended")
            break

        # for mirror image
        if (type(captureSrc) == int):
            frame = cv.flip(frame, 1)
        imageObj = Image.fromarray(frame)
        printChars(imageObj, 120, rbg)
        # break
        # time.sleep(0.07)

    cap.release()


def ui():
    while True:
        options = ["WebCam", "Video file"]
        os.system("cls")

        print(LIGHT_RED)
        art.tprint("asciiCam")
        print(" " * 35 + "-teleport-1254")

        print(f'{COLOR_YELLOW}Video source: ')
        for index, option in enumerate(options):
            print(f"{index + 1}. {option}")

        try:
            userInput: int = int(input(f"{COLOR_GREEN}Choose: "))
            rgbInput: str = input("rgb? (y/n): ").lower()
            rgb: bool = rgbInput == "y"
            if not rgb: print(COLOR_RESET)
            break
        except ValueError:
            continue

    captureSrc: str | int
    if (userInput == 1):
        captureSrc = 0
    elif (userInput == 2):
        filePath: str = input("Enter file path: ")
        print(COLOR_RESET)
        captureSrc = filePath
    else:
        return

    videoCapure(captureSrc, rgb)


if __name__ == "__main__":
    ui()
