"""A program that encodes and decodes hidden messages in images through LSB steganography"""
#@__author__ Alana Huitric
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location):
    """Decodes the hidden message in an image.

    Parameters
    ----------
    file_location: str
        The location of the image file to decode. This defaults to the provided
        encoded image in the images folder.
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    # The above could also be written as one of:
    #   red_channel, green_channel, blue_channel = encoded_image.split()
    #   red_channel, _, _ = encoded_image.split()
    #   red_channel, *_ = encoded_image.split()
    # The first has the disadvantage of creating temporary variables that aren't
    # used. The special variable name _ (underscore) is conventionally named
    # an unused variable.

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    # The above could also be written as:
    #   x_size, y_size = encoded_image.size[0]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for x in range(0,x_size):
        for y in range(0, y_size):
            b = bin(red_channel.getpixel((x,y)))
            if b[len(b) - 1] == "1" :
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)

    decoded_image.save("images/decoded_image.png")
    return decoded_image


def write_text(text_to_write, image_size):
    """Write text to an RGB image. Automatically line wraps.

    Parameters
    ----------
    text_to_write: str
        The text to write to the image.
    image_size: (int, int)
        The size of the resulting text image.
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10

    image_text.save("images/imgtext.png")
    return image_text


def encode_image(text_to_encode, template_image):
    """Encode a text message into an image.

    Parameters
    ----------
    text_to_encode: str
        The text to encode into the template image.
    template_image: str
        The image to use for encoding. An image is provided by default.
    """
    text_image = write_text(text_to_encode, template_image.size)

    red_channel = template_image.split()[0]
    green_channel = template_image.split()[1]
    blue_channel = template_image.split()[2]
    r = text_image.split()[0]

    x_size = template_image.size[0]
    y_size = template_image.size[1]

    encoded_image = Image.new("RGB", template_image.size)
    pixels = encoded_image.load()
    text_pixels = text_image.load()

    for x in range(0,x_size):
        for y in range(0, y_size):
            b = bin(red_channel.getpixel((x,y)))
            b_new = ""
            if r.getpixel((x,y)) == 255 and b[len(b) - 1] != "1":
                b_new = b[:-1] + "1"
            elif r.getpixel((x,y)) == 0 and b[len(b) - 1] != "0" :
                b_new = b[:-1] + "0"
            else:
                b_new = b

            br = int(b_new,2)
            pixels[x,y] = (br, green_channel.getpixel((x,y)), blue_channel.getpixel((x,y)))

    encoded_image.save("images/new_encoded_image.png")
    return encoded_image


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image("images/encoded_sample.png")

    image = Image.open("images/art.png")
    print("Encoding the image...")
    encode_image("art: the expression or application of human creative skill and imagination, typically in a visual form such as painting or sculpture, producing works to be appreciated primarily for their beauty or emotional power", image)

    print("Decoding the image...")
    decode_image("images/new_encoded_image.png")
