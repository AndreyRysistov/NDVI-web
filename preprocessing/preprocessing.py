import numpy as np
import cv2

def apply_gradient(grayscale_mat):
    heatmap = heatmap = cv2.applyColorMap((grayscale_mat * 256.).astype('uint8'), cv2.COLORMAP_SUMMER)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    return heatmap;

def angles_to_pixel(shape, point, angles_dict):
    delta_x = abs(angles_dict['CORNER_UL_LON_PRODUCT'] - angles_dict['CORNER_UR_LON_PRODUCT'])
    delta_y = abs(angles_dict['CORNER_UL_LAT_PRODUCT'] - angles_dict['CORNER_LL_LAT_PRODUCT'])
    mu_x = delta_x / shape[1]
    mu_y = delta_y / shape[0]
    x = abs(point[1] - angles_dict['CORNER_UL_LON_PRODUCT']) // mu_x
    y = abs(point[0] - angles_dict['CORNER_UL_LAT_PRODUCT']) // mu_y
    return int(x), int(y)


def get_rotation_matrix(angle, m, n):
    return np.array([[np.cos(angle), np.sin(angle), 0],
                     [-np.sin(angle), np.cos(angle), 0],
                     [-m * (np.cos(angle) - 1) + n * np.sin(angle), -n * (np.cos(angle) - 1) - m * np.sin(angle), 1]])


def rotate_the_poligon(poligon, angle):
    poligon = np.array(poligon)
    bias = poligon[0]
    offset_polygon = poligon - bias
    m, n = offset_polygon[1][0] / 2, offset_polygon[2][1] / 2
    ones = np.ones(4)
    matrix_point = np.column_stack((offset_polygon, ones))
    rotated_poligon = np.int64(matrix_point @ get_rotation_matrix(angle, m, n)[:, :-1]) + bias
    rotated_poligon = list(map(tuple, rotated_poligon))
    return rotated_poligon


def poligon_to_rectangle(poligon):
    rectangle_lines = [
        [poligon[0], poligon[2]], [poligon[0], poligon[1]],
        [poligon[1], poligon[3]], [poligon[2], poligon[3]]
    ]
    return rectangle_lines
