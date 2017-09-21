##References
#
#https://stackoverflow.com/questions/2872381/how-to-read-a-file-byte-by-byte-in-python-and-how-to-print-a-bytelist-as-a-binar
#
##
import gzip
#TRAINING SET LABEL FILE (train-labels-idx1-ubyte):
#[offset] [type]          [value]          [description] 
#0000     32 bit integer  0x00000801(2049) magic number (MSB first) 
#0004     32 bit integer  60000            number of items 
#0008     unsigned byte   ??               label 
#0009     unsigned byte   ??               label 
#........ 
#xxxx     unsigned byte   ??               label
#The labels values are 0 to 9.

#Given the following arguments: Image array, width and height
#Print values over 128 as # and those that are lower as .
def print_image(height,width,image):
    for i in range(width):
        img_representation = ""
        for j in range(height):
            if image[i][j] <= 128: 
                img_representation += "."
            else:
                img_representation += "#"
        print(img_representation)

#Open file in read mode
f = gzip.open('data/t10k-images-idx3-ubyte.gz','rb')

#Knowing the bytes and the offset extract necesary data
#for the image processing
magic = int.from_bytes(f.read(4),byteorder='big')
size = int.from_bytes(f.read(4),byteorder='big')
rows = int.from_bytes(f.read(4),byteorder='big')
columns = int.from_bytes(f.read(4),byteorder='big')

#Values for reference
#print(magic,size, "rows", rows, "columns", columns )
print("Reading images please wait...")


i, j, k = 0, 0, 0

#Create array to contain the images based on the amount of images and its size(rows and columns)
myArray=[[[0 for j in range(rows)] for i in range(columns)] for k in range(size)]

#Read in the pixels into the array
for k in range(size):
    for i in range(rows):
        for j in range(columns):
            myArray[k][i][j] = int.from_bytes(f.read(1),byteorder='big')

#Close stream
f.close()

#Provide some sort of interface to select and print the images in memory
print("File reading finished!")
while True:
    message = 'Select image number to display (select from 1 -',size,', 0 to exit):'
    n = int(input(message))
    #If number equals 0 or it is higher than the number of images terminate loop
    if n != 0 and n < size+1:
        #Reduce n (array from 0 to size) by one.
        print_image(rows,columns,myArray[n-1])
    else:
        break
