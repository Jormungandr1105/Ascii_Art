import cv2
import os
from PIL import Image, ImageFont, ImageDraw
import math as m


def get_chars(char_file):
    f = open(char_file, "r")
    in_text = f.read()
    lines = in_text.split("\n")
    for line in lines:
        values = line.split("\t")
        char_intensities[values[0]] = float(values[1])


def video_to_frames(video, path_output_dir):
    # extract frames from a video and save to directory as 'x.png' where
    # x is the frame index
    global count
    vidcap = cv2.VideoCapture(video)
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            if count % 30 == 0:
                cv2.imwrite(os.path.join(path_output_dir, '%d.png') % int(count/30), image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()
    if count == 0:
        print("FAILURE")


def load_image(image_name):
    image = Image.open(r"{}".format(image_name))
    image = image.convert("L")
    return image


def save_png(filename, count):
    global text
    global path
    global font_name
    mult = 2
    x1, y1 = len(canvas[0]), len(canvas)
    image = Image.new("RGB", (mult*3 * x1, mult*6 * y1), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("c:/Windows/Fonts\\{}.ttf".format(font_name), size=mult*5)
    draw.text((0, 0), text, fill=(0, 0, 0), font=font)
    try:
        image.save(".\\Photos\\outfiles\\{}\\{}.png".format(filename, count))
    except FileNotFoundError:
        os.mkdir(".\\Photos\\outfiles\\{}".format(filename))
        image.save(".\\Photos\\outfiles\\{}\\{}.png".format(filename, count))


def convert_to_text():
    global text
    global canvas
    global char_intensities
    global darkest_pixel
    global lightest_pixel
    darkest_char = 255
    for char in char_intensities:
        if char_intensities[char] < darkest_char:
            darkest_char = char_intensities[char]
    for line in canvas:
        line_text = ""
        for number in line:
            old_number = number
            new_number = 255 - (
                        (lightest_pixel - old_number) * ((255 - darkest_char) / (lightest_pixel - darkest_pixel)))
            lowest = 0
            next_char = "@"
            for char in char_intensities:
                if new_number >= char_intensities[char] >= lowest:
                    lowest = char_intensities[char]
                    next_char = char
            line_text += next_char
        line_text += "\n"
        text += line_text


def process_image(image, spacing=1):
    global darkest_pixel
    global lightest_pixel
    y_spacing = spacing * 2
    x, y = image.size
    px = image.load()
    total_pix = 0
    for b in range(0, y, y_spacing):
        line = []
        for a in range(0, x, spacing):
            pix_total = 0
            num_pix = 0
            for d in range(b, min(b + y_spacing, y)):
                for c in range(a, min(a + spacing, x)):
                    pix_total += (px[c, d])
                    num_pix += 1
            avg_pix_val = int(pix_total/num_pix)
            if avg_pix_val < darkest_pixel:
                darkest_pixel = avg_pix_val
            if avg_pix_val > lightest_pixel:
                lightest_pixel = avg_pix_val
            total_pix += pix_total
            line.append(avg_pix_val)
        canvas.append(line)
    return total_pix/(x*y)


count = 0
darkest_pixel = 255
lightest_pixel = 0

# char intensities for consolas
char_intensities = {}

# Image Types
image_types = [".jpg", ".png"]

# Font
font_name = "consola"


if __name__ == '__main__':
    n = 2
    font_name = "consola"
    get_chars(".\\fonts\\{}.tsv".format(font_name))
    video_to_frames('.\\Videos\\Avatar.mp4', '.\\data\\Avatar\\Photos\\')
    for x in range(1, m.floor(count/30)):
        text = ""
        canvas = []
        filename = ".\\data\\Avatar\\Photos\\{}.png".format(x)
        c_im = load_image(filename)
        pix_val_avg = process_image(c_im, spacing=n)
        print("Scanned {}".format(x))
    for x in range(1, m.floor(count/30)):
        text = ""
        canvas = []
        filename = ".\\data\\Avatar\\Photos\\{}.png".format(x)
        c_im = load_image(filename)
        pix_val_avg = process_image(c_im, spacing=n)
        convert_to_text()
        save_png("Avatar", x)
        print("Finished {}".format(x))
