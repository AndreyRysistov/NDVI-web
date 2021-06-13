import numpy as np


def angles_to_pixel(shape, point, angles_dict):
    delta_x = abs(angles_dict['CORNER_UL_LON_PRODUCT'] - angles_dict['CORNER_UR_LON_PRODUCT'])
    delta_y = abs(angles_dict['CORNER_UL_LAT_PRODUCT'] - angles_dict['CORNER_LL_LAT_PRODUCT'])
    mu_x = delta_x / shape[1]
    mu_y = delta_y / shape[0]
    x = abs(point[1] - angles_dict['CORNER_UL_LON_PRODUCT']) // mu_x
    y = abs(point[0] - angles_dict['CORNER_UL_LAT_PRODUCT']) // mu_y
    return int(x), int(y)



