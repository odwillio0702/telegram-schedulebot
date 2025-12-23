from PIL import Image
import numpy as np

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image_path, width=80):
    image = Image.open(image_path).convert("L")  # grayscale

    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio * 0.55)
    image = image.resize((width, height))

    pixels = np.array(image)
    ascii_image = ""

    for row in pixels:
        for pixel in row:
            ascii_image += ASCII_CHARS[pixel // 25]
        ascii_image += "\n"

    return ascii_image