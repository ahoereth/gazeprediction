#!.venv/bin/python

import os
import argparse

import numpy as np
import PIL
import scipy.io

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

def parse_input(coordinates):
    """
    Parses the input arguments for image file names. Only takes file names into account which are
    in the key set of coordinates.
    Returns a list of image names.
    """
    parser = argparse.ArgumentParser(epilog='For setup information, please refer to the README.md')
    parser.add_argument('image', nargs='+', help='image files to load')
    return [image_name for image_name in parser.parse_args().image if image_name in coordinates.keys()]

def load_images(image_names):
    """
    Loads all images given in image_names and stores them in a list alongside
    their names as tuples (name, image).
    """
    return [(image_name, PIL.Image.open(image_name)) for image_name in image_names]

def add_gaze(images, coordinates):
    """
    Takes images and coordinates and draws red pixels at the coordinates for each image, respectively.
    The images are stored in a list as tuples (name, image).
    """
    gazed_images = []
    for image_name, image in images:
        gazed_image = image.copy()
        for c in coordinates[image_name]:
            gazed_image.putpixel(c, (255,0,0))
        gazed_images.append((image_name, gazed_image))
    return gazed_images

def save_images(gazed_images):
    """
    Saves the images from the tuple list into the 'out' directory. Shows the images prior to saving.
    """
    try: # ensure out dir exists
        os.mkdir('out')
    except OSError:
        pass
    for image_name, gazed_image in gazed_images:
        gazed_image.show()
        gazed_image.save(os.path.join('out', image_name[:-4] + '.bmp'))

def plotGaze():
    """
    Reads in the coordinates, parses the input images and loads images for which
    coordinates are available. Plots the coordinates onto the images, shows them, and saves them.
    """
    coordinates = load_coordinates('coordinates.mat')
    image_names = parse_input(coordinates)
    images = load_images(image_names)
    gazed_images = add_gaze(images, coordinates)
    save_images(gazed_images)

if __name__ == '__main__':
    plotGaze()

