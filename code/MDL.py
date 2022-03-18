import numpy as np


def calc_L_H(coor):
    length = np.sqrt((coor[-1][0]-coor[0][0]) ** 2 + (coor[-1][1]-coor[0][1]) ** 2)
    dist = np.log2(length)
    return dist


def calc_L_D_H(coor):
    dist = 0
    seg_1_coor = [coor[0], coor[-1]]
    # Delta coors between starting and ending points of segment 1
    se_11 = np.asarray([seg_1_coor[-1][0] - seg_1_coor[0][0],
                        seg_1_coor[-1][1] - seg_1_coor[0][1]])
    for i in range(len(coor)-1):
        seg_2_coor = [coor[i], coor[i+1]]
        # Delta coors between starting points of two segments
        ss_12 = np.asarray([seg_2_coor[0][0] - seg_1_coor[0][0], seg_2_coor[0][1] - seg_1_coor[0][1]])
        # Length square of segment 1
        se_11_square = np.linalg.norm(np.asarray(se_11), 2) ** 2
        # Delta coors between starting and ending points of segment 2
        se_12 = np.asarray([seg_2_coor[-1][0] - seg_1_coor[0][0],
                            seg_2_coor[-1][1] - seg_1_coor[0][1]])
        # Length square of segment 2
        se_22 = np.asarray([seg_2_coor[len(seg_2_coor) - 1][0] - seg_2_coor[0][0],
                            seg_2_coor[len(seg_2_coor) - 1][1] - seg_2_coor[0][1]])

        u_1 = np.dot(ss_12, se_11) / se_11_square
        u_2 = np.dot(se_12, se_11) / se_11_square
        ps = np.asarray(seg_1_coor[0]) + np.dot(u_1, se_11)
        pe = np.asarray(seg_1_coor[0]) + np.dot(u_2, se_11)
        v_dist = calc_v_distance(seg_2_coor, ps, pe)
        a_dist = calc_a_distance(se_11, se_22)
        if v_dist < 0 or a_dist < 0:
            print (f"{v_dist}, {a_dist}")
        if v_dist != 0:
            dist += np.log2(v_dist)
        if a_dist != 0:
            dist += np.log2(a_dist)
    return dist


def calc_v_distance(seg_2_coor, ps, pe):
    dist_v = 0
    l_s = np.linalg.norm(np.asarray(seg_2_coor[0]) - ps, 2)
    l_e = np.linalg.norm(np.asarray(seg_2_coor[-1]) - pe, 2)
    if l_s == 0.0 and l_e == 0.0:
        print ("disc_v is zero.")
        return dist_v
    dist_v = float(l_s ** 2 + l_e ** 2) / (l_s + l_e)
    return dist_v


def calc_a_distance(se_11, se_22):
    cos_theta = np.dot(se_11, se_22) / (np.linalg.norm(se_11, 2) * np.linalg.norm(se_22, 2))
    if cos_theta > 1:      # This case may happen due to the calculation error above
        print (f"se_11: {np.linalg.norm(se_11, 2)}, se_22: {np.linalg.norm(se_22, 2)}")
        print (f"consine: {cos_theta}")
        sin_theta = 0
    else:
        sin_theta = np.sqrt(1 - cos_theta ** 2)
    if cos_theta < 0:
        dist_a = np.linalg.norm(se_22, 2)
    else:
        dist_a = np.linalg.norm(se_22, 2) * sin_theta
    return dist_a