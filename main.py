import numpy as np
import argparse
import os
import datetime
from utils import cmdmarks, load_yaml, plot_ndarray

parser = argparse.ArgumentParser(
    description='Numpyの情報を4次元まで展開してプロットするユーティリティツールです')

parser.add_argument('config', type=str,
                    help="config.yaml. please see config_base.yaml")
args = parser.parse_args()
config = load_yaml(args.config)


def main():
    for input_file in config.input_files:
        if not os.path.isfile(input_file.path):
            print(f'{cmdmarks.ERROR}Wav File given in wavlist is not exist\n\t{input_file.path}')
            return
    print(f'{cmdmarks.SUCCESS}Checked path. Found {len(config.input_files)} npy files.')

    dt = datetime.datetime.today()
    output_dir_name = f'{dt.strftime("%Y%m%d%H%M%S")}'
    os.mkdir(f'{config.output_dir}/{output_dir_name}')
    print(f'{cmdmarks.INFO}output dir name is {config.output_dir}/{output_dir_name}')

    for input_file in config.input_files:
        input_npy: np.ndarray = np.load(input_file.path)
        if tuple(input_file.predict_shape) == input_npy.shape:
            print(f'{cmdmarks.INFO}predict shape == actual shape. \n   (predict, actual) = ({tuple(input_file.predict_shape)}, {input_npy.shape}) : {os.path.basename(input_file.path)}')
        else:
            print(f'{cmdmarks.WARNING}predict shape != actual shape. \n   (predict, actual) = ({tuple(input_file.predict_shape)}, {input_npy.shape}) : {os.path.basename(input_file.path)}')
        plot_ndarray(input_npy, f'{config.output_dir}/{output_dir_name}/{os.path.basename(input_file.path)}.png', "hoge", config.cmap)


if __name__ == '__main__':
    main()
