import matplotlib
import os
from tqdm import tqdm
from matplotlib import gridspec
from matplotlib.colors import Normalize
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


def plot_2d_ndarray(x: np.ndarray, file_basename: str, output_dir_path, cmap: str, histogram: bool, normalize_vmin=None, normalize_vmax=None):
    fig: Figure = plt.figure(tight_layout=True)
    fig.suptitle(f'shape = {x.shape} : min = {x.min():.3f} : MAX = {x.max():.3f}')

    gs = gridspec.GridSpec(1, 2, width_ratios=(5, 3))  # *1
    ax1: Axes = fig.add_subplot(gs[0, 0]) if histogram else fig.add_subplot(1, 1, 1)
    ax2: Axes = fig.add_subplot(gs[0, 1]) if histogram else None
    pcm = ax1.pcolormesh(x, cmap=cmap, norm=Normalize(vmin=normalize_vmin, vmax=normalize_vmax)
                         ) if normalize_vmin is not None else ax1.pcolormesh(x, cmap=cmap)
    fig.colorbar(pcm, ax=ax1)

    if histogram:
        ax2.hist(x.flatten())
        fig.set_size_inches(12, 6)

    fig.savefig(f'{output_dir_path}/{os.path.splitext(os.path.basename(file_basename))[0]}')


def plot_ndarray(x: np.ndarray, file_basename: str, output_dir_path, cmap: str, histogram: bool, normalize_vmin=None, normalize_vmax=None):
    if len(x.shape) == 2:
        plot_2d_ndarray(x, file_basename=file_basename, output_dir_path=output_dir_path,
                        cmap=cmap, histogram=histogram, normalize_vmin=normalize_vmin, normalize_vmax=normalize_vmax)
    elif len(x.shape) == 3:
        new_out_dir_path = f'{output_dir_path}/{os.path.splitext(os.path.basename(file_basename))[0]}'
        os.mkdir(new_out_dir_path)
        for idx, input_ndarray in enumerate(tqdm(x)):
            plot_2d_ndarray(input_ndarray, file_basename=f'{idx:03}-{file_basename}', output_dir_path=new_out_dir_path,
                            cmap=cmap, histogram=histogram, normalize_vmin=normalize_vmin, normalize_vmax=normalize_vmax)
    elif len(x.shape) == 4:
        new_out_dir_path = f'{output_dir_path}/{os.path.splitext(os.path.basename(file_basename))[0]}'
        os.mkdir(new_out_dir_path)
        for idx in range(len(x.shape) - 1):
            os.mkdir(f'{new_out_dir_path}/{idx:03}')
        for idx, input_ndarray in enumerate(tqdm(x)):
            for idx_2, input_ndarray_2 in enumerate(tqdm(input_ndarray, leave=False)):
                plot_2d_ndarray(input_ndarray_2, file_basename=f'{idx_2:03}-{file_basename}', output_dir_path=f'{new_out_dir_path}/{idx:03}',
                                cmap=cmap, histogram=histogram, normalize_vmin=normalize_vmin, normalize_vmax=normalize_vmax)
