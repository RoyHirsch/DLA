import os
import random
import copy
import imageio
import numpy as np
from tqdm import tqdm

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from utils import imshow


N_WALKS_PRINT_INTERVAL = 1000


class BaseDLA():
    def __init__(self, init_mask, max_particles=None, radius=None, random_walk_policy='edge', log_level=3):
        self._init_mask = init_mask
        self._size = init_mask.shape[0]
        self._center_seed = (self._size // 2, self._size // 2)
        self._white_list = [(i1, i2) for i1, i2 in zip(*np.where(init_mask != 0.0))]
        self._initial_white_list = [(i1, i2) for i1, i2 in zip(*np.where(init_mask != 0.0))]
        self._matrix = copy.deepcopy(init_mask)

        self._max_particles = max_particles if max_particles != None else np.inf
        self._log_level = log_level

        self._random_walk_policy = random_walk_policy
        if self._random_walk_policy == 'edge':
            self._radius = init_mask.shape[0] // 2
        else:
            self._radius = radius if radius != None else init_mask.shape[0] // 2


    def _get_random_seed(self, point):
        theta = 2 * np.pi * random.random()
        x = int(self._radius * np.cos(theta)) + point[0]
        y = int(self._radius * np.sin(theta)) + point[1]
        return (x, y)

    def _get_random_seed_from_radius(self):
        rand_particle = random.choice(self._white_list)
        return self._get_random_seed(rand_particle)

    def _get_random_location(self):
        if self._random_walk_policy == 'edge':
            curr = self._get_random_seed(self._center_seed)
        elif self._random_walk_policy == 'radius':
            curr = self._get_random_seed_from_radius()
        else:
            raise ValueError
        return curr

    def _take_random_step(self, curr):
        decide = random.random()
        if decide < 0.25:
            curr = [curr[0] - 1, curr[1]]
        elif decide < 0.5:
            curr = [curr[0] + 1, curr[1]]
        elif decide < 0.75:
            curr = [curr[0], curr[1] + 1]
        else:
            curr = [curr[0], curr[1] - 1]
        return curr

    def _is_near_edge(self, curr):
        if (curr[1] + 1) > self._size - 1 or \
           (curr[1] - 1) < 1 or \
           (curr[0] + 1) > self._size - 1 or\
           (curr[0] - 1) < 1:
            return True
        elif np.sqrt((self._center_seed[0] - curr[0])**2 + (self._center_seed[1] - curr[1])**2) > self._size // 2:
            return True
        return False

    def _is_intersection(self, curr):
        if self._matrix[curr[0] + 1, curr[1]] != 0 or \
           self._matrix[curr[0] - 1, curr[1]] != 0 or \
           self._matrix[curr[0], curr[1] + 1] != 0 or \
           self._matrix[curr[0], curr[1] - 1] != 0:
            return True
        return False

    def _add_new_particle(self, curr, rank):
        self._white_list.append(curr)
        self._matrix[curr[0], curr[1]] = rank

    def grow(self):
        random.seed()
        n_particles = 2
        n_walks = 0

        while n_particles < self._max_particles:
            curr = self._get_random_location()
            n_walks += 1

            while True:
                curr = self._take_random_step(curr)
                if self._is_near_edge(curr):
                    break
                if self._is_intersection(curr):
                    self._add_new_particle(curr, n_particles)
                    n_particles += 1
                    break

            if self._log_level > 2 and n_walks % N_WALKS_PRINT_INTERVAL == 0:
                print('Logged {} particles (out of {})'.format(n_particles, self._max_particles))

        if self._log_level > 2:
            print('Finish grow')

    def save_video(self, dir='', fname='movie.gif', cmap='gray', dpi=200, save_pic_interval=5):

        added_particles = [p for p in self._white_list if p not in self._initial_white_list]
        m = copy.deepcopy(self._init_mask)
        with imageio.get_writer(os.path.join(dir, fname) + '.gif', mode='I') as writer:
            writer.append_data(self.get_matrix_as_image(m, cmap, dpi))
            plt.close()

            counter = 1
            for ps in tqdm(self.chunker(added_particles, save_pic_interval)):
                counter += 1
                for p in ps:
                    m[p[0], p[1]] = counter

                writer.append_data(self.get_matrix_as_image(m, cmap, dpi))
                plt.close()

    def save_image(self, dir='', name='pic.jpg', cmap='gray', dpi=1200, is_vector=False):
        file_suffix = 'svg' if is_vector else 'jpg'
        full_path = os.path.join(dir, name) + '.' + file_suffix
        imshow(self.matrix, cmap=cmap)
        if is_vector:
            plt.savefig(full_path, format='svg', dpi=dpi)
        else:
            plt.savefig(full_path, dpi=dpi)
        plt.close()

    @property
    def matrix(self):
        return self._matrix

    @property
    def binary_matrix(self):
        m = np.zeros_like(self._matrix)
        m[np.where(self._matrix != 0.0)] = 1.0
        return m

    @staticmethod
    def chunker(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    @staticmethod
    def get_matrix_as_image(m, cmap, dpi):
        fig = plt.figure(dpi=dpi)
        imshow(m, cmap=cmap)
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        return data.reshape(fig.canvas.get_width_height()[::-1] + (3,))


class DLA_PathHist(BaseDLA):
    def __init__(self, init_mask, max_particles=None, radius=None, random_walk_policy='edge', log_level=3):
        super().__init__(init_mask, max_particles, radius, random_walk_policy, log_level)
        self._walks_hist = []

    def _add_new_particle(self, curr, rank, walk_hist):
        self._white_list.append(curr)
        self._walks_hist.append(walk_hist)
        self._matrix[curr[0], curr[1]] = rank

    def grow(self):
        random.seed()
        n_particles = 2
        n_walks = 0

        while n_particles < self._max_particles:
            curr = self._get_random_location()
            walk_hist = [curr]
            n_walks += 1

            while True:
                curr = self._take_random_step(curr)
                walk_hist.append(curr)
                if self._is_near_edge(curr):
                    break
                if self._is_intersection(curr):
                    self._add_new_particle(curr, n_particles, walk_hist)
                    n_particles += 1
                    break

            if self._log_level > 2 and n_walks % N_WALKS_PRINT_INTERVAL == 0:
                print('Logged {} particles (out of {})'.format(n_particles, self._max_particles))

        if self._log_level > 2:
            print('Finish grow')

    def save_video(self, dir='', fname='movie.gif', cmap='gray', dpi=200, save_pic_interval=5):

        def add_mets(org, new):
            max_val = new.max()
            locs = np.where(org != 0.0)
            for loc0, loc1 in zip(locs[0], locs[1]):
                new[loc0][loc1] = max_val
            return new

        m = copy.deepcopy(self._init_mask)
        with imageio.get_writer(os.path.join(dir, fname) + '.gif', mode='I') as writer:
            writer.append_data(self.get_matrix_as_image(m, cmap, dpi))
            plt.close()

            for walk_hist in tqdm(self._walks_hist):
                walk_mat = np.zeros_like(m)
                walk_counter = 1
                for step in walk_hist:
                    walk_mat[step[0], step[1]] = walk_counter ** 3
                    walk_counter += 1
                    writer.append_data(self.get_matrix_as_image(add_mets(m, walk_mat), cmap, dpi))
                    plt.close()

                m[step[0], step[1]] = 1.0
            writer.append_data(self.get_matrix_as_image(m, cmap, dpi))
            plt.close()
