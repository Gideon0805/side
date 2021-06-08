import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--img1', type=str, required=True,
                    default=None, help='Image1 path')
parser.add_argument('--img2', type=str, required=True,
                    default=None, help='Image2 path')
args = parser.parse_args()

def calculate_psnr(img1, img2, max_value=255):
    """"Calculating peak signal-to-noise ratio (PSNR) between two images."""
    mse = np.mean((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32)) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(max_value / (np.sqrt(mse)))

def main(img_path1, img_path2):
    image1 = np.loadtxt(img_path1)
    image2 = np.loadtxt(img_path2)
    print('{} Image1 Shape: {} {}'.format('-'*5, image1.shape, '-'*5))
    print('{} Image2 Shape: {} {}'.format('-'*5, image2.shape, '-'*5))

    psnr = calculate_psnr(image1, image2)

    print('{} PSNR = {} {}'.format('='*10, psnr, '='*10))


if __name__ == '__main__':
    main(args.img1, args.img2)