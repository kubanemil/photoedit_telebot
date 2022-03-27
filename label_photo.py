from PIL import Image, ImageDraw,   ImageFont
import textwrap
import config
from citaty import quotes
from random import randint

def add_label(photo_src):
    im = Image.open(photo_src)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size
    font = ImageFont.truetype(font='font.ttf', size=int(image_height//10))

    text = quotes[randint(0, (len(quotes)-1))].upper() 
    char_width, char_height = font.getsize('A')
    char_per_line = image_width // char_width
    the_line = textwrap.wrap(text, width=char_per_line)

    ln_height = font.getsize(the_line[0])[1]
    ln_num = len(the_line)

    y = image_height - (int(ln_height * ln_num))
    for line in the_line:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width)/2
        draw.text((x,y), line, fill='white', font=font)
        y += line_height
    path_parts = photo_src.split('/')
    final_path = './%s/%s' % (config.path_to_edited_folder, path_parts[-1])
    im.save(final_path)
    return final_path
