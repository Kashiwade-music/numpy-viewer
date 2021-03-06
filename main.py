import numpy as np
import argparse
import shutil
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

    shutil.copyfile(f'{args.config}', f'{config.output_dir}/{output_dir_name}/config.yaml')

    for input_file in config.input_files:
        input_npy: np.ndarray = np.load(input_file.path)
        if tuple(input_file.predict_shape) == input_npy.shape:
            print(f'{cmdmarks.INFO}predict shape == actual shape. \n   (predict, actual) = ({tuple(input_file.predict_shape)}, {input_npy.shape}) : {os.path.basename(input_file.path)}')
        else:
            print(f'{cmdmarks.WARNING}predict shape != actual shape. \n   (predict, actual) = ({tuple(input_file.predict_shape)}, {input_npy.shape}) : {os.path.basename(input_file.path)}')

        if config.normalize is not None:
            if input_file.normalize is not None:
                plot_ndarray(x=input_npy, file_basename=os.path.basename(input_file.path), output_dir_path=f'{config.output_dir}/{output_dir_name}',
                             cmap=config.cmap, histogram=input_file.histogram, normalize_vmin=input_file.normalize.vmin, normalize_vmax=input_file.normalize.vmax)
            else:
                plot_ndarray(x=input_npy, file_basename=os.path.basename(input_file.path), output_dir_path=f'{config.output_dir}/{output_dir_name}',
                             cmap=config.cmap, histogram=input_file.histogram, normalize_vmin=config.normalize.vmin, normalize_vmax=config.normalize.vmax)
        else:
            if input_file.normalize is not None:
                plot_ndarray(x=input_npy, file_basename=os.path.basename(input_file.path), output_dir_path=f'{config.output_dir}/{output_dir_name}',
                             cmap=config.cmap, histogram=input_file.histogram, normalize_vmin=input_file.normalize.vmin, normalize_vmax=input_file.normalize.vmax)
            else:
                plot_ndarray(x=input_npy, file_basename=os.path.basename(input_file.path), output_dir_path=f'{config.output_dir}/{output_dir_name}',
                             cmap=config.cmap, histogram=input_file.histogram)


if __name__ == '__main__':
    main()
