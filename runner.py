from dla import get_dla_shape, get_dla_shape_hist

# for i in range(6):
#     mass, matrix = get_dla_shape(radius=60, is_gif=True, folder_name='images_r60', sample_name='r60_{}'.format(i))

mass, matrix = get_dla_shape_hist(radius=5, is_gif=True, folder_name='images_hist', sample_name='r5_pdi300_0', dpi=300, rev=False)
mass, matrix = get_dla_shape_hist(radius=5, is_gif=True, folder_name='images_hist', sample_name='r5_pdi300_1', dpi=300, rev=False)
mass, matrix = get_dla_shape_hist(radius=5, is_gif=True, folder_name='images_hist', sample_name='r5_pdi300_2', dpi=300, rev=False)
