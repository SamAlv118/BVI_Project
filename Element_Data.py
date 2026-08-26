#this is the element dictionary.
#we can modify the lists to include 
#only specific transition lines if so desired
#since larger atoms have more complex spectra,
#it might be worth it to sacrifice resolution 
#in favor of more prominent transition lines.

ELEMENT = {
    "Hydrogen": [410, 434, 486, 656],
    "Helium": [389, 447, 471, 492, 502, 505, 588, 668, 687],
    "Neon": [540, 585, 588, 603, 607, 616, 622, 627, 633, 638, 640, 651, 660, 693],
    "Sodium": [569, 589, 590]
}

#function that retrieves the list 
#of wavelengths for each element in dicitonary
def ls_nm(element_name):
    #using the key (element_name), get the value (list of wavelengths)
    #from the object in the dictionary (ELEMENT) 
    #and return the formatted list. 
    nms = ELEMENT.get(element_name, [])
    return ", ".join(map(str, nms)) #map applies str to each number in nms so that it 
                                    #1. can be stored in the text box in the UI
                                    #2. can be concatenated with the ", " for formatting into the text box
