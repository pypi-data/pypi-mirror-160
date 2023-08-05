import matplotlib.pyplot as plt
import matplotlib
import logging

from file_utils import get_grid_positions, prepare_file_name_saving

logging.basicConfig(
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
    filename="chembee_plotting.log",
)


matplotlib.rcParams.update({"font.size": 32})
fig = plt.figure(figsize=(15, 15))


def plot_calibration(
    fig: plt.figure,
    clf_list: list,
    calibration_displays: dict,
    ax_calibration_curve,
    grid_spec,
    grid: tuple,
    colors,
    file_name: str = "calibration",
    prefix: str = "calibration/",
):

    ax_calibration_curve.grid()
    ax_calibration_curve.set_title("Calibration plots")
    # call other method to avoid messing it up

    grid_positions = get_grid_positions(rows=grid[0], cols=grid[1])
    for i in range(len(clf_list)):
        clf = clf_list[i]
        name = clf.name
        row, col = grid_positions[i]
        ax = fig.add_subplot(grid_spec[row, col])

        ax.hist(
            calibration_displays[name].y_prob,
            range=(0, 1),
            bins=100,
            label=name,
            color=colors(i),
        )
        if i == grid[0] - 1:
            ax.set(xlabel="Mean predicted probability", ylabel="Count")
        else:
            ax.set(title="", xlabel="", ylabel="Count")

    file_name = prepare_file_name_saving(prefix, file_name, ending=".png")
    fig.tight_layout()
    plt.savefig(file_name)
    logging.info("Saved calibration plot " + str(file_name))
    plt.cla()
    plt.clf()
