import math
import PIL
import extcolors
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib import gridspec
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# from https://kylermintah.medium.com/coding-a-color-palette-generator-in-python-inspired-by-procreate-5x-b10df37834ae

def extract_colors(img):
  tolerance = 32
  limit = 24
  colors, pixel_count = extcolors.extract_from_image(img, tolerance, limit)
  return colors

def get_colour_comparison(colour1, colour2):
  # Red Color
  color1_rgb = sRGBColor.new_from_rgb_hex(colour1);

  # Blue Color
  color2_rgb = sRGBColor.new_from_rgb_hex(colour2);

  # Convert from RGB to Lab Color Space
  color1_lab = convert_color(color1_rgb, LabColor);

  # Convert from RGB to Lab Color Space
  color2_lab = convert_color(color2_rgb, LabColor);

  # Find the color difference
  delta_e = delta_e_cie2000(color1_lab, color2_lab);
  return delta_e


def render_color_platte(colors):
  size = 100
  columns = 6
  width = int(min(len(colors), columns) * size)
  height = int((math.floor(len(colors) / columns) + 1) * size)
  result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
  canvas = ImageDraw.Draw(result)
  for idx, color in enumerate(colors):
      x = int((idx % columns) * size)
      y = int(math.floor(idx / columns) * size)
      canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])
  return result

def fetch_image(image_path):
  urllib.request.urlretrieve(image_path, "image")
  img = PIL.Image.open("image")
  return img

def open_image(image_path):
  img = PIL.Image.open(image_path)
  return img

def overlay_palette(img, color_palette):
  nrow = 2
  ncol = 1
  f = plt.figure(figsize=(20,30), facecolor='None', edgecolor='k', dpi=55, num=None)
  gs = gridspec.GridSpec(nrow, ncol, wspace=0.0, hspace=0.0) 
  f.add_subplot(2, 1, 1)
  plt.imshow(img, interpolation='nearest')
  plt.axis('off')
  f.add_subplot(1, 2, 2)
  plt.imshow(color_palette, interpolation='nearest')
  plt.axis('off')
  plt.subplots_adjust(wspace=0, hspace=0, bottom=0)
  plt.savefig("palette.png")
  # plt.show(block=True)


def get_hex_palette(image_path):
  
  img = open_image(image_path)
  colors = extract_colors(img)
  
  hex_colors = []
  for color in colors:
    hex_colors.append('#%02x%02x%02x' % color[0])
  print(hex_colors)
  return hex_colors
  #uncomment to get a saved image
  # color_palette = render_color_platte(colors)
  # overlay_palette(img, color_palette)


#get_hex_palette("test.jpg")
# print(get_colour_comparison("#FF0000", "#0000FF"))