from image_proc import  get_binary_centered_mask
from efficient_dla import BaseDLA, DLA_PathHist

if __name__ == '__main__':
    # init = get_centralized_init(20)
    # dla = DLA_PathHist(init, max_particles=22, radius=None, log_level=3, random_walk_policy='edge')
    # dla.grow()
    # dla.save_video(dir='', fname='hist_r10_1', dpi=300, cmap='gray', save_pic_interval=1)
    #
    # _dir = '/Users/royhirsch/Documents/GitHub/DLA/bicycle'


    # for max_particles in [10000, 20000, 30000]:
    #     init = get_binary_centered_mask('/Users/royhirsch/Documents/GitHub/DLA/images/bicycle.jpeg', 400, 600)
    #     dla = DLA(init, max_particles=max_particles, radius=30, log_level=3, random_walk_policy='radius')
    #     .grow()
    #     if not os.path.exists(_dir):
    #         os.makedirs(_dir)
    #     dla.save_image(dir=_dir, name='bicycle_{}p'.format(max_particles), cmap='bw', dpi=1200, is_vector=True)

    init = get_binary_centered_mask('/Users/royhirsch/Documents/GitHub/DLA/images/me.jpeg', 400, 500)
    dla = BaseDLA(init, max_particles=30000, radius=30, log_level=3, random_walk_policy='radius')
    dla.grow()

    dla.save_image(dir='', name='me_30k_bw', cmap='bw', dpi=1200, is_vector=True)
    dla.save_image(dir='', name='me_30k_gray', cmap='gray', dpi=1200, is_vector=True)

    dla.save_image(dir='', name='me_30k_bw', cmap='bw', dpi=1200, is_vector=False)
    dla.save_image(dir='', name='me_30k_gray', cmap='gray', dpi=1200, is_vector=False)
    dla.save_video(dir='', fname='me_movie_30k', dpi=300, cmap='gray', save_pic_interval=100)

    init = get_binary_centered_mask('/Users/royhirsch/Documents/GitHub/DLA/images/bicycle.jpeg', 400, 500)
    dla = BaseDLA(init, max_particles=40000, radius=30, log_level=3, random_walk_policy='radius')
    dla.grow()

    dla.save_image(dir='', name='bicycle_40k_bw', cmap='bw', dpi=1200, is_vector=True)
    dla.save_image(dir='', name='bicycle_40k_gray', cmap='gray', dpi=1200, is_vector=True)

    dla.save_image(dir='', name='bicycle_40k_bw', cmap='bw', dpi=1200, is_vector=False)
    dla.save_image(dir='', name='bicycle_40k_gray', cmap='gray', dpi=1200, is_vector=False)
    dla.save_video(dir='', fname='bicycle_movie_40k', dpi=300, cmap='gray', save_pic_interval=100)
