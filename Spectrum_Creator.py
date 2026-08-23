import png
import numpy as np

from BVI_Spectroscopy_UI import CreateUI

stype = ''
targs = []
pixel_color = ()

dec = np.linspace(255, 0, 80, dtype = int)  #we use spacing of 80 because we only have 400 total pixels to work with
inc = np.linspace(0, 255, 80, dtype = int)  #combine this with the fact that there are 5 major color transitions, 400/5 = 80

def CreateESpec():
    global pixel_color
    #for pixels 0-80 (purple -> blue)

    for px in range(80):
        if px in targs:
            pixel_color = pixel_color + (dec[px], 0, 255)
        else:
            pixel_color = pixel_color + (0, 0, 0)


    #for pixels 80-160 (blue -> cyan)

    for px in range(80):
        if (px + 80) in targs:
            pixel_color = pixel_color + (0, inc[px], 255)
        else:
            pixel_color = pixel_color + (0, 0, 0)


    #for pixels 160-240 (cyan -> green)

    for px in range(80):
        if (px + 160) in targs:
            pixel_color = pixel_color + (0, 255, dec[px])
        else:
            pixel_color = pixel_color + (0, 0, 0)


    #for pixels 240-320 (green -> yellow)

    for px in range(80):
        if (px + 240) in targs:
            pixel_color = pixel_color + (inc[px], 255, 0)
        else:
            pixel_color = pixel_color + (0, 0, 0) 


    #for pixels 320-400 (yellow -> red)

    for px in range(80):
        if (px + 320) in targs:
            pixel_color = pixel_color + (255, dec[px], 0)
        else:
            pixel_color = pixel_color + (0, 0, 0)
        

def CreateASpec():
    global pixel_color
    #for pixels 0-80 (purple -> blue)

    for px in range(80):
        if px not in targs:
            pixel_color = pixel_color + (dec[px], 0, 255)
        else:
            pixel_color = pixel_color + (0, 0, 0)


    #for pixels 80-160 (blue -> cyan)

    for px in range(80):
        if (px + 80) not in targs:
            pixel_color = pixel_color + (0, inc[px], 255)
        else:
            pixel_color = pixel_color + (0, 0, 0)


    #for pixels 160-240 (cyan -> green)

    for px in range(80):
        if (px + 160) not in targs:
            pixel_color = pixel_color + (0, 255, dec[px])
        else:
            pixel_color = pixel_color + (0, 0, 0)


    #for pixels 240-320 (green -> yellow)

    for px in range(80):
        if (px + 240) not in targs:
            pixel_color = pixel_color + (inc[px], 255, 0)
        else:
            pixel_color = pixel_color + (0, 0, 0) 


    #for pixels 320-400 (yellow -> red)

    for px in range(80):
        if (px + 320) not in targs:
            pixel_color = pixel_color + (255, dec[px], 0)
        else:
            pixel_color = pixel_color + (0, 0, 0)


def CreateSpec():
    #setting up all of the variables for the spectrum creator
    global targs, stype
    global dec
    global inc
    global pixel_color
    global width

    width = 400 #each pixel is 1 nm in the range 300-700 nm
    height = 100 #this is just to give the spectrum more depth
    img = []
    stype, targs = CreateUI()
    pixel_color = ()
    
    for i in range(len(targs)):
        targs[i] -= 300

    if stype == "Emission":
        CreateESpec()
    if stype == "Absorption":
        CreateASpec()

    #combine all the pixel_color tuples into a list containing 1 huge tuple with all the rgb codes  
    for i in range(height): 
        img.append(pixel_color)

    pngfile = open('Spectrum.png', 'wb')  #creates the gradient png file
    canvas = png.Writer(width, height, greyscale=False)  #creates the dimensions of the png
    canvas.write(pngfile, img)  #writes each pixel into the png

if __name__ == "__main__":
    CreateSpec()