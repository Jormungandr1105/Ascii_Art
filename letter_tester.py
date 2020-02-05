from PIL import Image, ImageFont, ImageDraw


def load_image(filename, image_types):
    global font_name
    for image_type in image_types:
        try:
            image = Image.open(r"{}_{}{}".format(filename, font_name, image_type))
            image = image.convert("L")
            return image
        except FileNotFoundError or AttributeError:
            pass


def set_canvas(char):
    global canvas
    for x in range(10):
        line = []
        for y in range(10):
            line.append(char)
        canvas.append(line)
    filename = path + "number"
    return filename


def process_image(image, spacing=1):
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
            total_pix += pix_total
            line.append(avg_pix_val)
        canvas.append(line)
    return total_pix/(x*y)


def convert_to_text():
    global text
    global canvas
    text = ''
    for line in canvas:
        line_text = ""
        for char in line:
            line_text += str(char)
        line_text += "\n"
        text += line_text


def save_png(filename):
    global font_name
    global text
    global path
    mult = 2
    x1, y1 = len(canvas[0]), len(canvas)
    image = Image.new("RGB", (mult*3 * x1, mult*6 * y1), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("c:/Windows/Fonts/{}.ttf".format(font_name), size=mult*5)
    draw.text((0, 0), text, fill=(0, 0, 0), font=font)
    image.save("{}_{}.png".format(filename, font_name))


path = "./Photos/Test/"
canvas = []
chars = ["!", "@", "#", "$", "%", "^", "&", "*", "_", "+", "1", "2", "3", "4", "5",
         "6", "7", "8", "9", "0", "-", "=", " ", "'", ";", ":", "?", ".", ",", "|",
         "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G",
         "H", "J", "K", "K", "L", "Z", "X", "C", "V", "B", "N", "M", "q", "w", "e",
         "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k",
         "l", "z", "x", "c", "v", "b", "n", "m", "<", ">", "/"]
text = ""
font_name = "baskvill"

# Image Types
image_types = [".jpg", ".png"]


if __name__ == '__main__':
    outfile = ".\\fonts\\{}.tsv".format(font_name)
    f = open(outfile, "w+")
    out_text = ""
    for char in chars:
        text = ""
        canvas = []
        filename = set_canvas(char)
        convert_to_text()
        save_png(filename)
        c_im = load_image(filename, image_types)
        pix_avg_val = process_image(c_im)
        print("{}: {}".format(char, pix_avg_val))
        if chars[-1] == char:
            out_text += "{}\t{}".format(char, pix_avg_val)
        else:
            out_text += "{}\t{}\n".format(char, pix_avg_val)
    f.write(out_text)
