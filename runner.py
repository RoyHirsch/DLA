import os
import matplotlib
# matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from dla import BaseDLA, DLA_PathHist
from utils import get_centralized_init, get_binary_centered_mask, save_image


if __name__ == '__main__':
    _dir = '/Users/royhirsch/Documents/GitHub/DLA/images_nature'
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    ####################################################################################################################
    # NATURE
    ####################################################################################################################

    init = get_binary_centered_mask(file='/Users/royhirsch/Documents/GitHub/DLA/images/grass.jpeg',
                                    mask_size=450,
                                    out_size=500,
                                    blur_kernel=9,
                                    threshold1=40,
                                    threshold2=80,
                                    min_size_blob=70)
    save_image(init, _dir, 'grass_mask', dpi=300, cmap='gray')
    dla = BaseDLA(init, max_particles=20000, log_level=3, radius=30, random_walk_policy='radius')
    dla.grow()
    dla.save_video(dir=_dir, fname='grass_p20k_movie', cmap='gray', dpi=300, save_pic_interval=10)

    init = get_binary_centered_mask(file='/Users/royhirsch/Documents/GitHub/DLA/images/leaf2.jpeg',
                                    mask_size=450,
                                    out_size=500,
                                    blur_kernel=9,
                                    threshold1=40,
                                    threshold2=80,
                                    min_size_blob=70)
    save_image(init, _dir, 'leaf2_mask', dpi=300, cmap='gray')
    dla = BaseDLA(init, max_particles=20000, log_level=3, radius=30, random_walk_policy='radius')
    dla.grow()
    dla.save_video(dir=_dir, fname='leaf2_p20k_movie', cmap='gray', dpi=300, save_pic_interval=10)

    ####################################################################################################################
    # BASIC TESTS
    ####################################################################################################################
    # init = get_centralized_init(10)
    # dla = BaseDLA(init, max_particles=10, radius=None, log_level=3, random_walk_policy='edge')
    # dla.grow()
    # dla.save_video(dir=_dir, fname='movie', cmap='gray', dpi=20, save_pic_interval=5)

    # dla = DLA_PathHist(init, max_particles=10, radius=None, log_level=3, random_walk_policy='edge')
    # dla.grow()
    # dla.save_video(dir=_dir, fname='movie_hist', cmap='gray', dpi=20, save_pic_interval=5)
