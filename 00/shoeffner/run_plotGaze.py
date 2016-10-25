#!../../.venv/bin/python

import os
import argparse

import scipy.io
import numpy as np
import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# flag -p/--plot
PLOT = False

def load_coordinates(file_name):
    """
    Loads the coordinates from a Matlab file (v < 7.3).
    Transforms them into a nicer dictionary, such that the image names
    are mapped to coordinates.
    """
    coordinates = {}
    for coord in scipy.io.loadmat(file_name)['coordXYs'][0]:
        coordinates[coord[0][0]] = [c[0] for c in coord[1]]
    return coordinates

def parse_input():
    """
    Parses the input arguments for image file names. Only takes file names into account which are
    in the key set of coordinates.
    Returns the coordinates and a list of image names.
    """
    global PLOT

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', dest='plot', action='store_true', help='if supplied, the plot is shown')
    parser.add_argument('coordinatesfile', help='coordinates file to load')
    parser.add_argument('image', nargs='+', help='image files to load')
    args = parser.parse_args()
    PLOT = args.plot
    coordinates = load_coordinates(args.coordinatesfile)
    return coordinates, [image_name for image_name in args.image if os.path.basename(image_name) in coordinates.keys()]

def load_images(image_names):
    """
    Loads all images given in image_names and stores them in a list alongside
    their names as tuples (name, image).
    """
    return [(image_name, mpimg.imread(image_name)) for image_name in image_names]

def add_gaze(images, coordinates):
    """
    Takes images and coordinates and draws red pixels at the coordinates for each image, respectively.
    If the command line flag -p/--plot is given, the figure is plotted.
    Stores the resulting figure.
    """
    global PLOT

    plt.figure('Gazes', figsize=(12,8))
    for i, (image_name, image) in enumerate(images):
        plt.subplot(3, 3, i + 1)
        plt.imshow(image)
        plt.title("{} ({!s})".format(os.path.basename(image_name), i))
        plt.axis('off')
        plt.scatter(*zip(*coordinates[os.path.basename(image_name)]), color='red', marker='x')
    plt.savefig('Gazes.jpg', bbox_inches='tight')
    if PLOT:
        plt.show()

def plotGaze():
    """
    Reads in the coordinates, parses the input images and loads images for which
    coordinates are available. Plots the coordinates onto the images, shows them, and saves them.
    """
    coordinates, image_names = parse_input()
    images = load_images(image_names)
    add_gaze(images, coordinates)

if __name__ == '__main__':
    plotGaze()

