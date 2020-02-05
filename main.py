"""
Objective: Convert an image into an array of text

Author: Jormungandr
Version: 2.0
"""
from PIL import Image, ImageFont, ImageDraw
import csv
import os


def load_image(image_name):
    global image_types
    for image_type in image_types:
        try:
            image = Image.open(r"Photos\to_ascii-tize\{}{}".format(image_name, image_type))
            image = image.convert("L")
            return image
        except FileNotFoundError or AttributeError:
            pass


def get_chars(char_file):
    f = open(char_file, "r")
    in_text = f.read()
    lines = in_text.split("\n")
    for line in lines:
        values = line.split("\t")
        char_intensities[values[0]] = float(values[1])


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
            new_number = 255 - ((lightest_pixel - old_number) * ((255-darkest_char)/(lightest_pixel-darkest_pixel)))
            lowest = 0
            next_char = "@"
            for char in char_intensities:
                if new_number >= char_intensities[char] >= lowest:
                    lowest = char_intensities[char]
                    next_char = char
            line_text += next_char
        line_text += "\n"
        text += line_text


def save_text(filename):
    global text
    global path
    with open("TSV\\{}.tsv".format(filename.split(".")[0]), 'wt') as output:
        tsv_writer = csv.writer(output, delimiter='\t', lineterminator='\n')
        for line in canvas:
            tsv_writer.writerow(line)
    output.close()

    x1, y1 = len(canvas[0]), len(canvas)
    try:
        f = open("Ascii\\{0}\\{0}_{1}x{2}.txt".format(filename.split(".")[0], x1, y1), "wt")
    except FileNotFoundError:
        os.mkdir(path + filename.split(".")[0])
        f = open("Ascii\\{0}\\{0}_{1}x{2}.txt".format(filename.split(".")[0], x1, y1), "wt")
    f.write(text)
    f.close()


def save_png(filename):
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
        image.save(".\\Photos\\outfiles\\{0}\\{0}_{1}x{2}_{3}.png".format(filename, x1, y1, font_name))
    except FileNotFoundError:
        os.mkdir(".\\Photos\\outfiles\\{}".format(filename))
        image.save(".\\Photos\\outfiles\\{0}\\{0}_{1}x{2}_{3}.png".format(filename, x1, y1, font_name))


path = "./Ascii/"
canvas = []
text = ""
darkest_pixel = 255
lightest_pixel = 0

# char intensities for consolas
char_intensities = {}

# Image Types
image_types = [".jpg", ".png"]


if __name__ == '__main__':
    filename = input("Name of Photo to ASCII-tize ==> ")
    n = int(input("How Many Pixels for Width of Character ==> "))
    font_name = input("Choose Font ==> ")
    get_chars(".\\fonts\\{}.tsv".format(font_name))
    c_im = load_image(filename)
    pix_val_avg = process_image(c_im, n)
    convert_to_text()
    save_text(filename)
    save_png(filename)
    print(pix_val_avg)
    print(darkest_pixel)
    print(lightest_pixel)
