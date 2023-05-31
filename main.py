#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#set the subtexts
subtext = "Elisabeth & Ralf"
date = "99.99.2023"

#die höhe und breite der bilder in px
canvas_width = 1000 
canvas_height = 1000

#textgrößen
text_size = 100
subtext_size = 75
date_subtext_size = 75

correction_y = -35
line_spacing = 20

#truefont pfade
font_path = 'hello-honey.otf'
subfont_path = 'hello-honey.otf'
datefont_path = 'hello-honey.otf'
date_subfont_path = 'hello-honey.otf'

#Liste der Namen
input_path = 'liste.txt'

#pfad zu dem hintergrundbild
# kann durch pfade z.B. zu PNGs, oder EMFs geändert werden. SVGs funktionieren nicht.
background_path = 'background.png'

#set the path of the output folder
output_path = 'output'

#collage settings
#Wie viele untersetzer passen in einer horizontalen reihe neben einander in den Laser?
collage_nr_horizontal = 6 
collage_horizontal_padding=200
collage_vertical_padding=200


#the space added at the top left corner of the final collage
# default is 0
null_x_ofset = 200
null_y_ofset = 200



#############################################################
################ Ab hier nur für Experten ###################
#############################################################
"""
Created on Thu May  25 11:45:00 2023
@title: main.py
@description: This script is used to generate a list of pictures with text on it.
@input: a list of text and background picture
@output: a list of pictures with text on it and a collage of all pictures
@usage: python3 main.py
@requirement: Python3, PIL
@note:
    #ToDo
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math

#create output folder if it does not exist
cwd = os.getcwd()
real_output_path = os.path.join(cwd,output_path)
if not os.path.exists(real_output_path):
    os.makedirs(real_output_path)



print("#Stage 1:")

# itlerate through the list
with open(input_path, 'r', encoding="UTF-8") as f:
    i=1
    for line in f:
        print("    Processing: " + line.strip())
        #set the text
        text = line.strip()
        #i
        number = str(f'{i:03}')
        #set the output path
        output_file = os.path.join(output_path, number + "-" + text + '.png')
        # skip if the file already exists
        if os.path.isfile(output_file):
            print("File already exists: " + output_file)
            i+=1
            continue
        #set the background
        background = Image.open(background_path).convert('RGBA')
        background = ImageOps.pad(background,(canvas_width,canvas_height), color=None, centering=(0.5, 0.5))
        #set the canvas
        canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255))
        canvas.paste(background, (0, 0), background)        
        #set the font
        font = ImageFont.truetype(font_path, text_size)
        #set the text
        text_width, text_height = font.getsize(text)
        #set the text position
        text_x = (canvas_width - text_width) / 2
        text_y = (canvas_height - text_height) / 2 + correction_y
        #set the text color
        text_color = (0, 0, 0, 255)
        #set the text
        draw = ImageDraw.Draw(canvas)
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        #set the background

        #create anoter layer for the subtext

        subfont = ImageFont.truetype(subfont_path, subtext_size)
        subtext_width, subtext_height = subfont.getsize(subtext)

        subtext_x = (canvas_width - subtext_width) / 2
        subtext_y = (canvas_height - subtext_height) / 2 + text_height + correction_y
        draw.text((subtext_x, subtext_y), subtext, fill=text_color, font=subfont)
        
        #add a horizontal decor line with a length of x% of the canvas width
        decor_line_width = int(canvas_width*0.55)
        decor_line_height = 5
        decor_line_x = (canvas_width - decor_line_width) / 2
        decor_line_y = (canvas_height - decor_line_height) / 2 - decor_line_height - canvas_height*0.05 + correction_y
        draw.rectangle(((decor_line_x, decor_line_y), (decor_line_x+decor_line_width, decor_line_y+decor_line_height)), fill=text_color)

        #add another line belllow the text
        decor_line_x = (canvas_width - decor_line_width) / 2
        decor_line_y = (canvas_height - decor_line_height ) / 2 + correction_y +text_height + canvas_height*0.05
        draw.rectangle(((decor_line_x, decor_line_y), (decor_line_x+decor_line_width, decor_line_y+decor_line_height)), fill=text_color)

        # add a date below the text

        date = "99.99.2023"
        datesubfont = ImageFont.truetype(date_subfont_path, date_subtext_size)
        date_width, date_height = datesubfont.getsize(date) 
        date_x = (canvas_width - date_width) / 2
        date_y = (canvas_height - date_height) / 2 + text_height + canvas_height*0.05 + decor_line_height + canvas_height*0.05
        draw.text((date_x, date_y + correction_y), date, fill=text_color, font=datesubfont)

        #save the picture

        
        

        canvas.save(output_file)
        i+=1

print("#Stage 2:")

#delete previous collage if it exists
path_to_collage = os.path.join(cwd,"output","000-collage.png")
path_to_template = os.path.join(cwd,"output","000-template.png")
if os.path.isfile(path_to_collage):
    os.remove(path_to_collage)


#number of png in the output folder
png_nr = len([name for name in os.listdir(real_output_path) if os.path.isfile(os.path.join(real_output_path, name))])
collage_nr_vertical = int(np.ceil(png_nr/collage_nr_horizontal))
print("    "+str(png_nr)+" png files found in  the output foulder, that means with "+str(collage_nr_horizontal)+" horizontal colums/images. That results in "+str(collage_nr_vertical)+" vertical rows")

collage_width =  collage_nr_horizontal*canvas_width
collage_heigth = collage_nr_vertical*canvas_height

#add padding

collage_width_with_padding = collage_width + ((collage_nr_horizontal-1)*collage_horizontal_padding) + null_x_ofset
collage_heigth_with_padding = collage_heigth + ((collage_nr_vertical)*collage_vertical_padding) + null_y_ofset

collage = Image.new('RGBA', (collage_width_with_padding, collage_heigth_with_padding), (255, 255, 255))
#for png file in output folder:

#iterate through the output folder
x=null_x_ofset
y=null_y_ofset
j=0
couter = 0
for filename in os.listdir(real_output_path):
    if filename.endswith(".png"):
        couter+=1
        j+=1
        #set the path of the picture
        picture_path = os.path.join(real_output_path, filename)
        #open the picture
        picture = Image.open(picture_path).convert('RGBA')
        #paste the picture into the collage
        collage.paste(picture, (x, y), picture)
        #delete the picture
        #os.remove(picture_path)
        
        #set the x and y position for the next picture
        x+=canvas_width+collage_horizontal_padding
        if j == collage_nr_horizontal:
            x=null_x_ofset
            y+=canvas_height+collage_vertical_padding
            j=0
        continue
    else:
        continue



    
collage.save(path_to_collage)    

print("#Stage 3:")

#add a template for the outlies of the pictures

# Create a new image with a white background
image = Image.new("RGB", (canvas_width, canvas_height), "white")
draw = ImageDraw.Draw(image)

# Calculate the center coordinates of the hexagon
center_x = image.width // 2
center_y = image.height // 2

# Calculate the length of each side of the hexagon
side_length = 500

# Calculate the coordinates of the hexagon vertices
vertices = []
for i in range(6):
    angle_deg = 60 * i
    angle_rad = math.radians(angle_deg)
    x = center_x + side_length * math.cos(angle_rad)
    y = center_y + side_length * math.sin(angle_rad)
    vertices.append((x, y))

# Draw the hexagon outline
draw.polygon(vertices, outline="black", fill="blue")

# Save the image
path_to_hexagon=os.path.join(cwd,"output","000-hexagon.png")
image.save(path_to_hexagon)

print("#Stage 4:")
#add a template for the outlies of the pictures
template = Image.new('RGBA', (collage_width_with_padding, collage_heigth_with_padding), (255, 255, 255,255))

#set the path of the picture

#open the picture
hexagon = Image.open(path_to_hexagon).convert('RGBA')
x=null_x_ofset
y=null_y_ofset
j=0
for l in range(couter):
        j+=1
        #set the path of the picture
        
        #open the picture
        hexagon = Image.open(path_to_hexagon).convert('RGBA')
        #paste the picture into the collage
        template.paste(hexagon, (x, y), hexagon)
        #delete the picture
        #os.remove(picture_path)
        
        #set the x and y position for the next picture
        x+=canvas_width+collage_horizontal_padding
        if j == collage_nr_horizontal:
            x=null_x_ofset
            y+=canvas_height+collage_vertical_padding
            j=0
        continue


template.save(path_to_template)



#todo fix bug with alpha channel in windows photo viewer


print("path: "+real_output_path)
print("path to collage: "+path_to_collage+" ")
print("done")