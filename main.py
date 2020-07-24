from PIL import Image, ImageDraw, ImageFont
import os

# name of the file to save
filename = "image.png"
fnt = ImageFont.truetype('arial.ttf', 12)

# create new image
image = Image.new(mode = "RGB", size = (200,70), color = "red")
draw = ImageDraw.Draw(image)
draw.text((10,10), "My Text", font=fnt, fill=(255,255,0))
image.save(filename)

# save the file
image.save(filename)

# open the file
os.system(filename)
