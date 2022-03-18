import os
from MDL import calc_L_H, calc_L_D_H
from plot_functions import *


def get_turnings_by_mdl_corrected(path):
    """
    :param path: vector of estimated locations, format [ [x_0, y_0], [x_1, y_1], ..., [x_n, y_n] ]
    :return: characteristic points, i.e., indices of turning positions, including starting and ending points.
    For example, CP = [0, 5, 50, 100], meaning that len(estimations) = 101, at index 5 and 50, there are turns.
    """
    CP = [0]
    start_index = 0
    length = 1
    len_first_two_steps = np.sqrt((path[1][0] - path[0][0]) ** 2 + (path[1][1] - path[0][1]) ** 2)
    mdl_accept_prev_all = [len_first_two_steps] # Store the results of using previous step as a turn.
    cost_no_turn = []
    cost_turn = []

    # Initially all steps are treated as turns.
    while start_index + length < len(path):
        # A B C
        curr_index = start_index + length
        if curr_index == len(path) - 1:
            break
        curr_est = [path[i] for i in range(start_index, curr_index + 2)]
        L_H = calc_L_H(curr_est)
        L_D_H = calc_L_D_H(curr_est)
        # Reject previous step as a turn and treat current step as a turn
        mdl_accept_current = L_H + L_D_H
        # Accept previous step as a turn
        mdl_accept_prev = mdl_accept_prev_all[-1] + np.log2(np.sqrt((curr_est[-1][0] - curr_est[-2][0]) ** 2 + (curr_est[-1][1] - curr_est[-2][1]) ** 2))
        # Previous step is a local minimum.
        if mdl_accept_current > mdl_accept_prev:
            CP.append(curr_index)
            start_index = curr_index
            length = 1
            mdl_accept_prev_all.append(mdl_accept_prev-mdl_accept_prev_all[-1])
        else:
            length += 1
            mdl_accept_prev_all.append(mdl_accept_current)
        cost_no_turn.append(mdl_accept_current)
        cost_turn.append(mdl_accept_prev)
    CP.append(len(path) - 1)
    return CP, mdl_accept_prev_all, cost_no_turn, cost_turn


def plot_turn(dir_path):

    for path_name in os.listdir(dir_path):
        print(path_name)
        filename = os.path.join(dir_path, path_name)

        path_coors = []
        freq = 500
        scale = 1
        with open(filename, "r") as f_in:
            i = 0
            for line in f_in:
                if i % freq == 0:
                    coord_str = line.strip('\n').split(' ')
                    path_coors.append([float(coord_str[0]) * scale, float(coord_str[1]) * scale])
                i += 1
                if i > 50000:
                    # A pathway may be walked several times. Detected turns may overlap.
                    # For better visualization purpose only.
                    break

        turns_mdl_corrected, mdl_cost, cost_no_turn, cost_turn = get_turnings_by_mdl_corrected(path_coors)
        turn_coors = [path_coors[i] for i in turns_mdl_corrected]

        plot_turning_on_map(path_coors, turn_coors, path_name.split('.')[0], 'greedy', scale=scale, freq=freq)


if __name__ == "__main__":
    # dir_path = '../data/seen_data'
    dir_path = '../data/unseen_data'
    plot_turn(dir_path)