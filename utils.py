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


def plot_ndarray(x: np.ndarray, file_path: str, normalize_type: str, cmap: str):
    fig = plt.figure()
    if len(x.shape) == 2:
        plt.pcolormesh(x, cmap=cmap)
        plt.colorbar()
        plt.tight_layout()
        fig.savefig(file_path)
