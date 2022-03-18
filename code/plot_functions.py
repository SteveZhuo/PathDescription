import matplotlib.pyplot as plt
import numpy as np


def plot_turning_on_map(estimations, turns, path_name, scheme, scale=1, freq=500):
    scale_org = scale
    # For UST site.
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = -np.inf
    fontsize = 20
    fig, ax = plt.subplots()
    for i, item in enumerate(estimations):
        marker = plt.Circle((item[0], -item[1]), radius=0.1*scale, color='k')
        # marker = plt.Rectangle((item[0], -item[1]), width=10, height=10, linewidth=2, angle=0, color='black')
        plt.gcf().gca().add_artist(marker)
        if item[0] < x_min:
            x_min = item[0]
        if item[0] > x_max:
            x_max = item[0]
        if -item[1] < y_min:
            y_min = -item[1]
        if -item[1] > y_max:
            y_max = -item[1]

    if x_min != np.inf and x_max != -np.inf and y_min != np.inf and y_max != -np.inf:
        if scale > 1:
            scale = 1
        plt.xlim(x_min-10*scale, x_max+10*scale)
        plt.ylim(y_max+10*scale, y_min-10*scale)
    else:
        plt.xlim([-4000, 4000])
        plt.ylim([4000, -4000])
    # plt.plot([item[0] for item in estimations], [item[1] for item in estimations], color='k')
    turn_x = [turns[i][0] for i in range(0, len(turns))]
    turn_y = [-turns[i][1] for i in range(0, len(turns))]
    # plt.axis('equal')
    ax.scatter(turn_x, turn_y, c='r', marker='^', s=30, label='Turn Detected')
    # plt.legend([f"{scheme}: {len(turns)}"])
    plt.legend(borderpad=0.2, markerscale=2, handletextpad=0, loc='upper left', fontsize=fontsize)
    plt.xlabel('X (m)', fontsize=fontsize)
    plt.ylabel('Y (m)', fontsize=fontsize)
    plt.savefig(f"../plots/{path_name}_{scheme}.png", dpi=500)
    plt.close()
    # plt.tight_layout()
    # plt.show()
    print (f"Turning {path_name}_{scheme} plotted.")