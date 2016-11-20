import cv2
import numpy as np
from sys import argv
from getopt import getopt
from matplotlib import pyplot as plt
from os.path import basename, splitext
from scipy.signal import argrelextrema, convolve2d, order_filter


def _split(img):
    r, g, b = (img[:, :, 0], img[:, :, 1], img[:, :, 2])
    return r, g, b, (r + g + b) / 3.


def _normalize_channel(nom, denom):
    threshold = 0.1 * np.max(denom)
    nom = np.copy(nom)
    yes = np.where(denom > threshold)
    nom[np.where(denom <= threshold)] = 0
    nom[yes] = nom[yes] / denom[yes]
    return nom


def _RGB(r, g, b):
    R = r - (g + b) / 2.
    G = g - (r + b) / 2.
    B = b - (r + g) / 2.
    Y = (r + g) / 2. - np.abs(r - g) / 2. - b
    return R, G, B, Y


def _generate_gabors(shape=(16, 16), sigma=2, lambd=10, gamma=.5, psi=0):
    return [cv2.getGaborKernel(shape, sigma, theta, lambd, gamma, psi)
            for theta in np.arange(0, np.pi, np.pi/4)]


def _apply_gabors(img, gabors):
    return [convolve2d(img, gabor) for gabor in gabors]


def _make_pyramids(img):
    pyramids = [img]
    for i in range(7):
        pyramids.append(cv2.pyrDown(pyramids[-1]))
    return pyramids


def _center_surround_diff(c, s, a, b=None):
    l = a[c] - (b[c] if b is not None else 0)
    r = a[s] if b is None else b[s] - a[s]
    return np.abs(l - cv2.resize(r, l.shape[::-1]))


def _normalize(img):
    M = np.max(img)
    # 4-neighborhood
    # kernel = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    # 8-neighborhood
    kernel = np.ones((3, 3), dtype=np.int)
    filtered = order_filter(img, kernel, np.sum(kernel) - 1)
    m = np.mean(img[np.equal(np.equal(img, filtered), filtered != M)])
    return img * ((M - m) ** 2)


def _addition(imgs, size):
    imgs = [cv2.resize(img, size[::-1]) for img in imgs]
    return np.sum(imgs, 0)


def gabor_saliency(impath):
    img = plt.imread(impath)
    # img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # broken w/ cv2.filter2D
    img_gray = np.dot(img[..., :3], [.299, .587, .114])

    r, g, b, I = _split(img)
    r, g, b = (_normalize_channel(c, I) for c in (r, g, b))
    R, G, B, Y = _RGB(r, g, b)

    gabors = _generate_gabors()
    gabored = _apply_gabors(img_gray, gabors)

    Rp, Gp, Bp, Yp, Ip = (_make_pyramids(m) for m in (R, G, B, Y, I))
    Ops = [_make_pyramids(gabor) for gabor in gabored]

    cs = np.asarray([(2, 5), (2, 6), (3, 6), (3, 7), (4, 7), (4, 8)]) - 1
    Ics = [_center_surround_diff(c, s, Ip) for c, s in cs]
    RGcs = [_center_surround_diff(c, s, Rp, Gp) for c, s in cs]
    BYcs = [_center_surround_diff(c, s, Bp, Yp) for c, s in cs]
    Otcs = [[_center_surround_diff(c, s, Op) for c, s in cs] for Op in Ops]

    Ics = [_normalize(img) for img in Ics]
    RGcs = [_normalize(img) for img in RGcs]
    BYcs = [_normalize(img) for img in BYcs]
    Otcs = [[_normalize(img) for img in Ocs] for Ocs in Otcs]

    shape = Ics[3].shape
    Ibar = _addition(Ics, shape)
    Cbar = _addition([RGcs[i] + BYcs[i] for i in range(len(RGcs))], shape)
    Obar = np.sum([_normalize(_addition(Ocs, shape)) for Ocs in Otcs], 0)

    S = _normalize(Ibar) + _normalize(Cbar) + _normalize(Obar)
    S = cv2.resize(1./3. * S, img.shape[1::-1])

    return S, gabored, gabors, img_gray


def main(impath, *args):
    S, gabored, gabors, gray = gabor_saliency(impath)
    name = splitext(basename(impath))[0]
    
    plt.imsave('{}_gray.png'.format(name), gray, cmap='gray')
    plt.imsave('{}_saliency.png'.format(name), S, cmap='gray')
    for i, (gabor, gabored) in enumerate(zip(gabors, gabored)):
        plt.imsave('{}_gabor_{}.png'.format(name, i), gabor, cmap='gray')
        plt.imsave('{}_gabored_{}.png'.format(name, i), gabored, cmap='gray')


if __name__ == '__main__':
    if len(argv) == 1:
        raise TypeError("gabor_saliency.py requires a target image's filename")
    main(*argv[1:])
