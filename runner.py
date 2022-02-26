import os
from dla import BaseDLA, DLA_PathHist
from utils import get_centralized_init


if __name__ == '__main__':
    _dir = '/Users/royhirsch/Documents/GitHub/DLA/tmp'
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    init = get_centralized_init(10)
    dla = BaseDLA(init, max_particles=10, radius=None, log_level=3, random_walk_policy='edge')
    dla.grow()
    dla.save_video(dir=_dir, fname='movie', cmap='gray', dpi=20, save_pic_interval=5)

    init = get_centralized_init(10)
    dla = DLA_PathHist(init, max_particles=10, radius=None, log_level=3, random_walk_policy='edge')
    dla.grow()
    dla.save_video(dir=_dir, fname='movie_hist', cmap='gray', dpi=20, save_pic_interval=5)
