##References
#
#https://stackoverflow.com/questions/2872381/how-to-read-a-file-byte-by-byte-in-python-and-how-to-print-a-bytelist-as-a-binar
#
##
import gzip
import numpy as np
import PIL.Image as pil 
import time

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

# Code from lab
def read_labels_from_file(filename):
    print("Reading "+  filename + " please wait...")
    t = time.time()
    with gzip.open(filename,'rb') as f:
        magic = int.from_bytes(f.read(4),byteorder='big')
        size = int.from_bytes(f.read(4),byteorder='big')
        labels = [f.read(1) for i in range(size)]
        labels = [int.from_bytes(label,'big') for label in labels]
    print("Label reading finished!")
    print("Elapsed Time:",(time.time() - t))
    return labels

def read_images_from_file(filename):
    print("Reading "+  filename + " please wait...")
    t = time.time()
    with gzip.open(filename,'rb') as f:
    #Knowing the bytes and the offset extract necesary data
    #for the image processing
        magic = int.from_bytes(f.read(4),byteorder='big')
        size = int.from_bytes(f.read(4),byteorder='big')
        rows = int.from_bytes(f.read(4),byteorder='big')
        columns = int.from_bytes(f.read(4),byteorder='big')

        #Values for reference
        #print(magic,size, "rows", rows, "columns", columns )
        
        # Adapted from
        # https://gist.github.com/akesling/5358964#file-mnist-py-L26
        # And
        # https://github.com/alexpt2000gmit/4Year_ReadTheMNISTDataFiles/blob/master/1_Read%20the%20data%20files.py
        buffer = f.read(rows * columns * size)
        images = np.frombuffer(buffer, dtype=np.uint8).astype(np.float32)
        images = images.reshape(size, rows, columns)

        # Original code for reading images from file commented out
        #Create array to contain the images based on the amount of images and its size(rows and columns)
        #Read in the pixels into the array
        #i, j, k = 0, 0, 0
        #images=[[[0 for j in range(rows)] for i in range(columns)] for k in range(size)]
        #for k in range(size):
        #    for i in range(rows):
        #        for j in range(columns):
        #            images[k][i][j] = int.from_bytes(f.read(1),byteorder='big')
        
    print("Image reading finished!")
    print("Elapsed Time:",(time.time() - t))

    return images

def save_images_as_png(image, image_number, label, image_type):
    img = pil.fromarray(np.array(image))
    img = img.convert('RGB')
    # cast number into string to identify the image
    image_name = 'img/'+ image_type +'-' + str(image_number)+'-' + str(label) +'.png'
    img.save(image_name)
    img.show()
    
    
# Read Images and Labels from Files
train_labels = read_labels_from_file('data/train-labels-idx1-ubyte.gz')
test_labels = read_labels_from_file('data/t10k-labels-idx1-ubyte.gz')
train_images = read_images_from_file('data/train-images-idx3-ubyte.gz')
test_images = read_images_from_file('data/t10k-images-idx3-ubyte.gz')




#Provide some sort of interface to select and print the images in memory
while (True):
    message = 'Select set : [0]Training [1]Testing  '
    n = int(input(message))
    if (n == 0):
        default_images = train_images
        default_labels = train_labels
        image_type = 'train'
    elif(n == 1):
        default_images = test_images
        default_labels = test_labels
        image_type = 'test'
    else:
        break;

    while True:
        message = 'Select image number to display (select from 0 - ' + str(len(default_images)-1) + ', -1 to exit):'
        n = int(input(message))
        #If number equals -1 or it is higher than the number of images terminate loop
        if n != -1 and n < len(default_images):
            print_image(default_images[n])
            save_images_as_png(default_images[n], n,default_labels[n], image_type)
        else:
            break
