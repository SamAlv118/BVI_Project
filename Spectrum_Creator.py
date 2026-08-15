import png
import numpy as np

exclusions = [486, 656, 434, 410]
for i in range(len(exclusions)):
    exclusions[i] -= 300

width = 400 #each pixel is 1 nm in the range 300-700 nm
height = 1 #this is just to give the spectrum more depth
img = []

dec = np.linspace(255, 0, 80, dtype = int)  #we use spacing of 80 because we only have 400 total pixels to work with
inc = np.linspace(0, 255, 80, dtype = int)  #combine this with the fact that there are 5 major color transitions, 400/5 = 80

pixel_color = ()

#for pixels 0-80 (purple -> blue)

for px in range(80):
    if px not in exclusions:
        pixel_color = pixel_color + (dec[px], 0, 255)
    else:
        pixel_color = pixel_color + (0, 0, 0)


#for pixels 80-160 (blue -> cyan)

for px in range(80):
    if (px + 80) not in exclusions:
        pixel_color = pixel_color + (0, inc[px], 255)
    else:
        pixel_color = pixel_color + (0, 0, 0)


#for pixels 160-240 (cyan -> green)

for px in range(80):
    if (px + 160) not in exclusions:
        pixel_color = pixel_color + (0, 255, dec[px])
    else:
        pixel_color = pixel_color + (0, 0, 0)


#for pixels 240-320 (green -> yellow)

for px in range(80):
    if (px + 240) not in exclusions:
        pixel_color = pixel_color + (inc[px], 255, 0)
    else:
        pixel_color = pixel_color + (0, 0, 0) 


#for pixels 320-400 (yellow -> red)

for px in range(80):
    if (px + 320) not in exclusions:
        pixel_color = pixel_color + (255, dec[px], 0)
    else:
        pixel_color = pixel_color + (0, 0, 0)


#combine all the pixel_color tuples into a list containing 1 huge tuple with all the rgb codes   
img.append(pixel_color)

pngfile = open('gradient.png', 'wb')  #creates the gradient png file
canvas = png.Writer(width, height, greyscale=False)  #creates the dimensions of the png
canvas.write(pngfile, img)  #writes each pixel into the png

