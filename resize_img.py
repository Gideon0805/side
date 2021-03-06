# import the necessary packages
from __future__ import print_function
# from imutils.video import VideoStream
import numpy as np
import argparse
from pathlib import Path, PurePath
# import imutils
import time
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="output dir")
ap.add_argument("-i", "--input", required=True,
	help="input dir")
ap.add_argument("--height", type=int, default=None,
	help="resize height")
ap.add_argument("--width", type=int, default=None,
	help="resize width")
args = vars(ap.parse_args())

def ImgResize():
	# initialize the video stream and allow the camera
	# sensor to warmup
	(h, w) = (args["height"], args["width"])
	print("[INFO] reading images...")

	match_type = '*'+'.'+'jpg'

	input_list = []
	output_list = []
	output_dir = Path(args["output"])
	if not output_dir.is_dir():
		Path(args["output"]).mkdir()
		output_dir = Path(args["output"])

	for f in Path(args["input"]).glob('**/*'):
		if PurePath(f).match(match_type):
			file_path = str(f)
			input_list.append(file_path)
			output_file = output_dir.joinpath(file_path.split('/')[-1])
			output_list.append(str(output_file))

	print("[INFO] translating images...")
	for i in range(len(input_list)):
		frame = cv2.imread(input_list[i])
		if frame is None: 
		    raise ValueError('!!! Error opening image !!!')
		frame = cv2.resize(frame, (w, h))
		# frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# resize_frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
		########################### For FA image
		# rotation = True
		# if rotation:
		#     # frame_ = cv2.resize(frame, (crop_H, crop_W)) # width x height = image_H x image_W = x , y
		#     frame_ = cv2.flip(frame, 1)
		#     X = h
		#     Y = w
		#     M = cv2.getRotationMatrix2D((X/2 - 1, Y/2 - 1), 90, 1) # Counterclockwise 90
		#     M[0,2] += (Y - X) / 2 # axis-x shift
		#     M[1,2] += (X - Y) / 2 # axis-y shift
		#     frame_ = cv2.warpAffine(frame_, M, (w, h)) # width x height = image_W x image_H
		#     ## shift and crop
		#     # SH = np.float32([[1, 0, 0],[0, 1, -480]])
		#     # frame = cv2.warpAffine(frame, SH, (1080, 1440))
		#     frame = frame_
		############################
		cv2.imwrite(output_list[i], frame)

	# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	# if args["fps"] is None:
	# 	args["fps"] = int(cap.get(cv2.CAP_PROP_FPS))
	# 	pass

	# cv2.imwrite(output_file, image_live_np)
	# print("[INFO] cleaning up...")
	# cv2.destroyAllWindows()
	# cap.release()
	# writer.release()

def main():

    ImgResize()

    print('Translate finished !')


if __name__ == '__main__':
   main()