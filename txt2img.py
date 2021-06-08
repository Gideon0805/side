import numpy as np
from PIL import Image as im
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--txt', type=str, required=True,
                    default=None, help='Txt file path')
parser.add_argument('--img', type=str, required=False,
                    default='./Output.jpg', help='Export image path')
parser.add_argument('--width', type=int, required=True,
                    default=None, help='Image width')
parser.add_argument('--height', type=int, required=True,
                    default=None, help='Image height')
parser.add_argument('--type', type=str, required=False,
                    default='uint8', help='Txt data type')
args = parser.parse_args()

def normalize8(I):
    mn = I.min()
    mx = I.max()

    delta = mx - mn

    I = ((I - mn)/delta) * 255
    return I.astype(np.uint8)

def main(txt_path, img_path, W, H, type):
    if type == 'float':
        float_arr = np.loadtxt(txt_path, dtype=np.float)
        array = normalize8(float_arr)       
        pass
    else:
        array = np.loadtxt(txt_path, dtype=np.uint8)
    print('{} Image WxH : ({}, {}) {}'.format('-'*5, W, H, '-'*5))

    # array = np.reshape(array, (H, W, 3))
    # Rehape
    array = np.reshape(array, (-1, 3), order='F')
    array = np.reshape(array, (H, W, 3))
    print('{} Array shape: {} {}'.format('-'*5, array.shape, '-'*5))
    # creating image object of
    # above array
    data = im.fromarray(array, 'RGB')
     
    # saving the final output 
    # as a PNG file
    data.save(img_path)
    print('{} {} Saved {}'.format('='*10, img_path, '='*10))


if __name__ == '__main__':
    main(args.txt, args.img, args.width, args.height, args.type)