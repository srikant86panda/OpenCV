import os
import cv2
import glob
import argparse
import numpy as np

def sharpen_image(image):
    ## Kernel value from GIMP 
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_shrp = cv2.filter2D(image, -1, kernel)
    # cv2.imshow(f'sharpen image', img_shrp)
    # cv2.waitKey(0)
    return img_shrp

def blur_image(image, kernel_size):
    img_blr = cv2.blur(image, ksize=(kernel_size, kernel_size))
    # cv2.imshow(f'kernel_{kernel_size}', img_blr)
    # cv2.waitKey(0)
    return img_blr

def resize_image(file_name, height, width):
    img = cv2.imread(file_name)
    # cv2.imshow('Original image', img)
    # cv2.waitKey(0)
    # print(img.shape)
    img_height, img_width = img.shape[0:2]
    print(f'image height: {img_height}, width: {img_width}')
    if img_width >= img_height:
        new_img = cv2.resize(img, (width, height))
    else:
        new_img = cv2.resize(img, (height, width))
    return new_img

parser = argparse.ArgumentParser(description='image_batch_processing')
parser.add_argument('-p', '--path',
                    help="path",
                    default=None,
                    type=str, 
                    required = True)

parser.add_argument('-ht', '--height',
                    help="height",
                    default=1000,
                    type=int, 
                    required = True)                

parser.add_argument('-wd', '--width',
                    help="width",
                    default=1100,
                    type=int, 
                    required = True)    

parser.add_argument('-br', '--blur',
                    help="blur",
                    action="store_true",
                    default=False)  

parser.add_argument('-sr', '--sharp',
                    help="sharp",
                    action="store_true",
                    default=False)  

args = parser.parse_args()
path = args.path
height = args.height
width = args.width

try:
    blur = args.blur
except:
    blur = True

try:    
    sharp = args.sharp
except:    
    sharp = True

print(f'path: {path}, height: {height}, width: {width}, blur: {blur}, sharp: {sharp}')

if os.path.exists(path):
    img_file_names = glob.glob(f'{path}/*.jpg')
    if len(img_file_names) < 1:
        print(f'no image file exist at input folder: {path}')
    else:
        new_folder = 'new_images'
        if not os.path.exists(new_folder):
            print(f'folder: {new_folder} does not exist, hence creating')
            os.makedirs(new_folder)

        for i in img_file_names:
            
            file_name = i.split('\\')[-1]
            new_image_file_name = f"{new_folder}/{file_name}"
            print(f'original file: {i}, new file: {new_image_file_name}')
            img = resize_image(i, 1000, 1100)
            if blur:
                img = blur_image(img, 5)
            if sharp:
                img = sharpen_image(img)
            cv2.imwrite(new_image_file_name, img)
else:
    print('input folder does not exist')



