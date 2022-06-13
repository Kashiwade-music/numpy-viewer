import matplotlib
import os
from matplotlib import gridspec
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import yaml
import matplotlib.pyplot as plt
import numpy as np
from easydict import EasyDict


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class cmdmarks:
    SUCCESS = f"{bcolors.OKGREEN}[SUCCESS] {bcolors.ENDC}"
    PROCESSING = f"{bcolors.OKCYAN}[PROCESSING] {bcolors.ENDC}"
    ERROR = f"{bcolors.FAIL}[ERROR] {bcolors.ENDC}"
    INFO = f"{bcolors.HEADER}[INFO] {bcolors.ENDC}"
    WARNING = f"{bcolors.WARNING}[WARNING] {bcolors.ENDC}"


def load_yaml(file):
    with open(file, 'r') as f:
        ed = EasyDict(yaml.safe_load(f))
    return ed


def plot_2d_ndarray(x: np.ndarray, file_basename: str, output_dir_path, normalize_type: str, cmap: str, histogram: bool):
    fig: Figure = plt.figure(tight_layout=True)
    fig.suptitle(f'shape = {x.shape} : min = {x.min():.3f} : MAX = {x.max():.3f}')

    gs = gridspec.GridSpec(1, 2, width_ratios=(5, 3))  # *1
    ax1: Axes = fig.add_subplot(gs[0, 0]) if histogram else fig.add_subplot(1, 1, 1)
    ax2: Axes = fig.add_subplot(gs[0, 1]) if histogram else None
    pcm = ax1.pcolormesh(x, cmap=cmap)
    fig.colorbar(pcm, ax=ax1)

    if histogram:
        ax2.hist(x.flatten())
        fig.set_size_inches(12, 6)

    fig.savefig(f'{output_dir_path}/{os.path.splitext(os.path.basename(file_basename))[0]}')


def plot_ndarray(x: np.ndarray, file_basename: str, output_dir_path, normalize_type: str, cmap: str, histogram: bool):
    if len(x.shape) == 2:
        plot_2d_ndarray(x, file_basename=file_basename, output_dir_path=output_dir_path,
                        normalize_type=normalize_type, cmap=cmap, histogram=histogram)
    elif len(x.shape) == 3:
        new_out_dir_path = f'{output_dir_path}/{os.path.splitext(os.path.basename(file_basename))[0]}'
        os.mkdir(new_out_dir_path)
        for idx, input_ndarray in enumerate(x):
            plot_2d_ndarray(input_ndarray, file_basename=f'{idx:03}-{file_basename}', output_dir_path=new_out_dir_path,
                            normalize_type=normalize_type, cmap=cmap, histogram=histogram)
