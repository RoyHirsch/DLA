import os.path

import cv2
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import colors


def imshow(m, cmap='gray'):
    if cmap == 'jet':
        cmap = plt.get_cmap('jet')
        cmap.set_under('black')
        plt.xticks([])
        plt.yticks([])
        plt.imshow(m, interpolation='nearest', vmin=1.0 / m.max(), cmap=cmap)

    elif cmap == 'bw':
        cmap = colors.ListedColormap(['black'] + ['white'] * 254)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(m, cmap=cmap)

    else:
        plt.xticks([])
        plt.yticks([])
        plt.imshow(m, cmap=cmap)


def read_image(file):
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def save_image(m, dir, name, dpi=300, cmap='gray', format='jpeg'):
    full_path = os.path.join(dir, name + '.jpg')
    plt.figure()
    imshow(m, cmap)
    plt.savefig(full_path, format=format, dpi=dpi)


def resize(img, out_size):
    h = img.shape[0]
    w = img.shape[1]

    if h > w:
        ratio = float(out_size) / h
        w_tag = int(ratio * w)
        dim = (w_tag, out_size)
    else:
        ratio = float(out_size) / w
        h_tag = int(ratio * h)
        dim = (out_size, h_tag)
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def centralize(bkg_size, inp):
    m = np.zeros((bkg_size, bkg_size))
    h, w = inp.shape
    hm = bkg_size // 2

    crop = m[hm - h // 2: hm + h // 2, hm - w // 2: hm + w // 2]
    ch, cw = crop.shape
    h_delta = (h - ch) if ch != h else 0
    w_delta = (w - cw) if cw != w else 0

    m[hm - h // 2: hm + h // 2 + h_delta,
    hm - w // 2: hm + w // 2 + w_delta] = inp
    return m


def remove_small_blobs(img, min_size_blob=150):
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)

    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    img = np.zeros((output.shape))
    for i in range(0, nb_components):
        if sizes[i] >= min_size_blob:
            img[output == i + 1] = 255
    return img


def get_centralized_init(size):
    if size % 2 == 0: size += 1
    visited = np.zeros((size, size))
    visited[size//2, size//2] = 1
    return visited


def get_binary_centered_mask(file, mask_size, out_size, blur_kernel=5, threshold1=30, threshold2=50, min_size_blob=40):
    if mask_size % 2 != 0 or out_size % 2 != 0:
        raise ValueError('mask_size out_size needs to be even numbers')
    if mask_size >= out_size:
        raise ValueError('mask_size should be smaller then out_size')

    gray = read_image(file)

    blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
    edge_img = cv2.Canny(blurred, threshold1, threshold2)
    clean_edge_img = remove_small_blobs(edge_img, min_size_blob)
    resized = resize(clean_edge_img, mask_size)
    return centralize(out_size, resized)
