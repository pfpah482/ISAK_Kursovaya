import numpy as np
import cv2

def get_ndvi(nir_img, red_img): 
    nir_img_float = nir_img.astype(float)
    red_img_float = red_img.astype(float)
    sub_mat = np.subtract(nir_img_float, red_img_float)
    sum_mat = np.add(nir_img_float, red_img_float)
    result = np.divide(sub_mat,sum_mat)
    return result;
