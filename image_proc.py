import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def read_image(file):
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


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
    m[hm - h // 2: hm + h // 2, hm - w // 2: hm + w // 2] = inp
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

def get_binary_centered_mask(file, mask_size, out_size, blur_kernel=5, threshold1=30, threshold2=50, min_size_blob=40):
    gray = read_image(file)

    blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
    edge_img = cv2.Canny(blurred, threshold1, threshold2)
    clean_edge_img = remove_small_blobs(edge_img, min_size_blob)
    resized = resize(clean_edge_img, mask_size)
    return centralize(out_size, resized)


if __name__ == '__main__':
    o = get_binary_centered_mask(file='/Users/royhirsch/Documents/GitHub/DLA/images/bicycle.jpeg',
                                 mask_size=400,
                                 out_size=1000)
    plt.imshow(o), plt.show()