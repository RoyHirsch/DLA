import time
import copy
import os
import random
import imageio
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils import *


def get_dla_shape(radius, is_gif, folder_name='images', sample_name='test', save_pic_interval=100):

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    x_seed = radius + 2
    y_seed = radius + 2
    size = radius * 2 + 5

    matrix = np.zeros((size, size))
    time_matrix = np.zeros((size, size))

    for row in range(0, size):
        for col in range(0, size):
            if row == y_seed and col == x_seed:
                matrix[row][col] = 1
                time_matrix[row][col] = 1
            elif np.sqrt((x_seed-col)**2 + (y_seed - row)**2) > radius:
                matrix[row][col] = 2

    cmap_base = colors.ListedColormap(['black', 'white', 'black'])
    cmap_jet = plt.get_cmap('jet')
    cmap_jet.set_under('black')
    zero_one_cmap = colors.ListedColormap(['black', cmap_jet(-1)])

    random_walkers_count = 0
    complete_cluster = False
    counter = 0
    used_interval = []

    while not complete_cluster:
        random_walkers_count += 1
        random.seed()
        location = get_random_sample(radius, x_seed, y_seed)

        # Initialize variables, like Friend tag and near edge identifier
        is_found_friend = False
        is_need_edge = False

        # Set an individual walker out, stop if found a 'friend', give up if it reached the edge of the board
        while not is_found_friend and not is_need_edge:
            new_loc, is_found_friend, is_need_edge, is_exit = check_neighbours(location, size, matrix)

            # Add to the cluster if near a friend
            if is_found_friend:
                matrix[location[1]][location[0]] = 1
                counter += 1
                time_matrix[location[1]][location[0]] = counter + 1

            else:
                location = new_loc

        intervalSavePic = range(2, 400000, save_pic_interval)
        if random_walkers_count in intervalSavePic:
            print("still working, have added ", random_walkers_count, " random walkers.", " Added to cluster: ", counter)
        if is_gif:
            if random_walkers_count in intervalSavePic:
                used_interval.append(random_walkers_count)
                plt.xticks([])
                plt.yticks([])
                if time_matrix.max() != 1:
                    plt.imshow(time_matrix, interpolation='nearest', vmin=1.0 / time_matrix.max(), cmap=cmap_jet)
                else:
                    plt.imshow(time_matrix, interpolation='nearest', cmap=zero_one_cmap)

                plt.savefig("{}/cluster_{}_{}.png".format(folder_name, sample_name, str(random_walkers_count)), dpi=200)
                plt.close()
       
        if random_walkers_count == 400000:
            print("Break the cycle, taking too many iterations")
            complete_cluster = True

        if is_found_friend and is_exit:
            complete_cluster = True

    plt.matshow(matrix, interpolation='nearest', cmap=cmap_base)
    plt.xticks([])
    plt.yticks([])
    plt.savefig("{}/cluster_{}.png".format(folder_name, sample_name), dpi=200)
    plt.close()

    plt.matshow(time_matrix, interpolation='nearest', vmin=1.0 / time_matrix.max(), cmap=cmap_jet)
    plt.xticks([])
    plt.yticks([])
    plt.savefig("{}/time_cluster_{}.png".format(folder_name, sample_name), dpi=200)
    plt.close()

    if is_gif:
        with imageio.get_writer('{}/movie_{}.gif'.format(folder_name, sample_name), mode='I') as writer:
            for i in used_interval:
                filename = "{}/cluster_{}_{}.png".format(folder_name, sample_name, i)
                image = imageio.imread(filename)
                writer.append_data(image)
                os.remove(filename)
            image = imageio.imread("{}/time_cluster_{}.png".format(folder_name, sample_name))
            writer.append_data(image)

    return counter, matrix


def get_dla_shape_hist(radius, is_gif, folder_name='images', sample_name='test', dpi=70, rev=False):
    eps = 1e-31
    inf = 1e+31

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    x_seed = radius + 2
    y_seed = radius + 2
    size = radius * 2 + 5

    gif_frames = []
    matrix = np.zeros((size, size))
    final_matrix = np.zeros((size, size))
    time_matrix = np.zeros((size, size))

    for row in range(0, size):
        for col in range(0, size):
            if row == y_seed and col == x_seed:
                final_matrix[row][col] = 1
                matrix[row][col] = 1
                time_matrix[row][col] = 1
            elif np.sqrt((x_seed - col) ** 2 + (y_seed - row) ** 2) > radius:
                matrix[row][col] = 2

    gif_frames.append(final_matrix)
    custom_cmap = plt.get_cmap('gray')
    custom_cmap.set_under('black')

    random_walkers_count = 0
    complete_cluster = False
    counter = 1
    used_interval = []

    while not complete_cluster:
        random_walkers_count += 1
        random.seed()
        location = get_random_sample(radius, x_seed, y_seed)

        # Initialize variables, like Friend tag and near edge identifier
        is_found_friend = False
        is_need_edge = False
        path_hist = []
        hist_matrix = np.zeros((size, size))

        # Set an individual walker out, stop if found a 'friend', give up if it reached the edge of the board
        while not is_found_friend and not is_need_edge:
            new_loc, is_found_friend, is_need_edge, is_exit = check_neighbours(location, size, matrix)
            path_hist.append(new_loc)

            # Add to the cluster if near a friend
            if is_found_friend:
                for i, step in enumerate(path_hist):
                    hist_matrix[step[1]][step[0]] = i**2 + 2
                    frame = add_mets(final_matrix, copy.deepcopy(hist_matrix))
                    gif_frames.append(frame)

                final_matrix[location[1]][location[0]] = 1
                matrix[location[1]][location[0]] = 1
                counter += 1
                time_matrix[location[1]][location[0]] = counter + 1

            else:
                location = new_loc

        if random_walkers_count == 400000:
            print("Break the cycle, taking too many iterations")
            complete_cluster = True

        if is_found_friend and is_exit:
            complete_cluster = True

    if is_gif:
        if rev:
            mid = len(gif_frames) // 2
            gif_frames = gif_frames[mid:] + gif_frames[:mid]
        filename = "{}/frame.png".format(folder_name)
        with imageio.get_writer('{}/movie_{}.gif'.format(folder_name, sample_name), mode='I') as writer:
            for frame in tqdm(gif_frames):
                plt.imshow(frame, interpolation='nearest', vmin=1.0 / time_matrix.max(), cmap=custom_cmap)
                plt.xticks([])
                plt.yticks([])
                plt.savefig(filename, dpi=dpi)
                plt.close()

                image = imageio.imread(filename)
                time.sleep(0.005)
                os.remove(filename)
                writer.append_data(image)

    return counter, matrix
