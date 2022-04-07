import cv2
from pytube import YouTube
from parser import args
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import glob
import os


class YouTubeConverter():

    def __init__(self):

        self.height = args.height
        self.width = args.width
        self.rate = args.frame_rate
        self.MOVIE_PATH = args.movie_path
        self.IMAGE_PATH = args.image_path

    def URLreader(self) -> list:
        """ Parse through .txt file with urls and store them in a list.
        """
        urls = []

        with open('urls.txt') as file:

            # urls = [line.split(',') for line in file]
            for line in file:
                line = line.split(',')

                url = []

                for attr in range(len(line)):

                    if attr == 0:
                        url.append(line[attr])

                    else:
                        url.append(float(line[attr]))

                urls.append(url)

        return urls

    def DownloadMovie(self, url: str) -> None:
        """ Download movie clips from YouTube to MOVIE_PATH.
        :param url: URL to YouTube-clip
        """
        movie = YouTube(url)
        movie = movie.streams.filter(file_extension='mp4').get_highest_resolution()
        movie.download(self.MOVIE_PATH)

    def Movie2Image(self,
                    movie: str,
                    fraction_width: float,
                    fraction_height: float,
                    displacement_top: float,
                    displacement_left: float,
                    start: int = 0,
                    end: int = 0,
                    file_count: int = 0) -> int:
        """ Converts mp4 file to .jpg files representing movie frames.

        :params movie: Path to the actual movie in mp4 format
        :params fraction_width: Width of the cropping window, in percent %.
        :params fraction_height: Heght of the cropping window, in percent %.
        :params displacement_top: Displacement of the cropping window from the top, in percent %.
        :params displacement_left: Displacement of the cropping window from the left, in percent %.
        :params start: Start time, in seconds
        :params end: End time, in seconds
        :params file_count: Filecount, to keep track of generated images

        :return file_count: Filecount after frames extraction
        """

        vidcap = cv2.VideoCapture(movie)
        count = 0
        success = True

        FPS = int(vidcap.get(cv2.CAP_PROP_FPS))
        VIDEO_HEIGHT = vidcap.get(3)
        VIDEO_WIDTH = vidcap.get(4)

        def GenerateImage(image: np.ndarray, file_count: int) -> int:
            """ Crops and saves images to 'data/images/'

            :params image: Image represented in a numpy array, using the cv2 package.
            :params file_count: Current filecount

            :return file_count: Filecount after download
            """

            if args.bw:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Measure window size
            box_size_height = int(VIDEO_HEIGHT * fraction_width)
            box_size_width = int(VIDEO_WIDTH * fraction_height)

            # Measure displacement of window
            start_y = int(VIDEO_HEIGHT * (displacement_top))
            end_y = start_y + box_size_height

            start_x = int(VIDEO_WIDTH * (displacement_left))
            end_x = start_x + box_size_width

            # Crop image
            image = image[start_x: end_x - 1, start_y:end_y - 1]

            # Re-size image
            image = cv2.resize(image, (self.height, self.width))

            # Download image
            cv2.imwrite(self.IMAGE_PATH + 'img%d.jpg' % file_count, image)

            file_count += 1

            return file_count

        while success:

            success, image = vidcap.read()

            if count % (int(FPS * self.rate)) == 0:

                if end > 0:

                    # If current movie frame is within the desired interval
                    if count >= int(FPS * start) and count <= int(FPS * end):

                        file_count = GenerateImage(image, file_count)

                    # If current movie frame is outside the interval
                    elif count > int(FPS * end):

                        return file_count

                else:
                    # Generate images
                    file_count = GenerateImage(image, file_count)

            count += 1

        return file_count

    def start(self):
        """ Start the extraction process.
        """

        print(f'Loading URL-links.')

        urls = self.URLreader()

        filecount = 0

        print(f'Activating extraction process.')
        for url_list in tqdm(urls):
            url = url_list[0]  # URL to YouTube-clip
            fraction_width = url_list[1]  # Width of cropping window, in percent %
            fraction_height = url_list[2]  # Height of cropping window, in percent %
            displacement_top = url_list[3]  # Displacement from top, in percent %
            displacement_left = url_list[4]  # Displacement from left, in percent %

            start = int(url_list[5])  # Start time
            end = int(url_list[6])  # End time

            assert fraction_width + displacement_left <= 1, 'Width and displacement should account for maximum of 100%.'
            assert fraction_height + displacement_top <= 1, 'Height and displacement should account for maximum of 100%.'

            movie = self.DownloadMovie(url)

            print(f'Converting YouTube-clips to .jpg frames to {args.image_path}')

            file = glob.glob(f"{self.MOVIE_PATH}*.mp4")[0]
            filecount = self.Movie2Image(file, fraction_width, fraction_height, displacement_top, displacement_left,
                                         start, end, filecount)
            os.remove(file)

        print(f'Extracted {filecount} images')


if __name__ == '__main__':
    convert_engine = YouTubeConverter()
    convert_engine.start()



