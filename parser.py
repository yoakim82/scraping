__author__ = 'Majd Jamal'

import numpy as np
#import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Image Classification of fruits and vegetables')

parser.add_argument('--height', type = int, default=256,
	help='Height of generated images. Default: 256')

parser.add_argument('--width', type = int, default=256,
	help='Width of generated images. Default: 256')

parser.add_argument('--bw', action = 'store_true', default=False,
	help='Generate images in grayscale.')

parser.add_argument('--crop', action = 'store_true', default=False,
	help='Cropping images')

parser.add_argument('--box', action = 'store_true', default=False,
	help='Display Cropout box')

parser.add_argument('--convert_only', action = 'store_true', default=False,
	help='Does not download mp4 files, but convert frames to .jpg.')

parser.add_argument('--movie_path', type = str, default='data/movies/',
	help='Path to save mp4 files. Default: data/movies/')

parser.add_argument('--image_path', type = str, default='data/images/',
	help='Path to save jpg files. Default: data/images/')

parser.add_argument('--frame_rate', type = float, default=0.2,
	help='Generate images per FPS * frame_rate. Lower values increases amount of extracted frames. ')


args = parser.parse_args()
