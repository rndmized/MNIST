##References
#
#https://stackoverflow.com/questions/2872381/how-to-read-a-file-byte-by-byte-in-python-and-how-to-print-a-bytelist-as-a-binar
#
##
import gzip
import numpy as np
import PIL.Image as pil 
#TRAINING SET LABEL FILE (train-labels-idx1-ubyte):
#[offset] [type]          [value]          [description] 
#0000     32 bit integer  0x00000801(2049) magic number (MSB first) 
#0004     32 bit integer  60000            number of items 
#0008     unsigned byte   ??               label 
#0009     unsigned byte   ??               label 
#........ 
#xxxx     unsigned byte   ??               label
#The labels values are 0 to 9.

#Given the an Image array 
#Print values over 128 as # and those that are lower as .
def print_image(image):
    for i in range(28):
        img_representation = ""
        for j in range(28):
            if image[i][j] <= 128: 
                img_representation += "."
            else:
                img_representation += "#"
        print(img_representation)


def read_labels_from_file(filename):
    with gzip.open(filename,'rb ') as f:
        magic = int.from_bytes(f.read(4),byteorder='big')
        size = int.from_bytes(f.read(4),byteorder='big')
        labels = [f.read(1) for i in range(size)]
        labels = [int.from_bytes(label,'big') for label in labels]
    return labels

def read_images_from_file(filename):
    print("Reading images please wait...")
    with gzip.open(filename,'rb') as f:
    #Knowing the bytes and the offset extract necesary data
    #for the image processing
        magic = int.from_bytes(f.read(4),byteorder='big')
        size = int.from_bytes(f.read(4),byteorder='big')
        rows = int.from_bytes(f.read(4),byteorder='big')
        columns = int.from_bytes(f.read(4),byteorder='big')

        #Values for reference
        #print(magic,size, "rows", rows, "columns", columns )
        

        i, j, k = 0, 0, 0
        #Create array to contain the images based on the amount of images and its size(rows and columns)
        images=[[[0 for j in range(rows)] for i in range(columns)] for k in range(size)]
        #Read in the pixels into the array
        for k in range(size):
            for i in range(rows):
                for j in range(columns):
                    images[k][i][j] = int.from_bytes(f.read(1),byteorder='big')
        
    print("File reading finished!")

    return images

def save_images_as_png(image, image_number):
    img = pil.fromarray(np.array(image))
    img = img.convert('RGB')
    image_name = 'img/img-' + str(image_number) +'.png'
    img.save(image_name)
    img.show()
    
    
#data/train-images-idx3-ubyte.gz
#data/t10k-images-idx3-ubyte.gz
images = read_images_from_file('data/t10k-images-idx3-ubyte.gz')

#Provide some sort of interface to select and print the images in memory
while True:
    message = 'Select image number to display (select from 1 - ' + str(len(images)) + ', 0 to exit):'
    n = int(input(message))
    #If number equals 0 or it is higher than the number of images terminate loop
    if n != 0 and n < len(images)+1:
        #Reduce n (array from 0 to size) by one.
        print_image(images[n-1])
        save_images_as_png(images[n-1], n-1)
    else:
        break
