import cv2
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from functools import partial
from shutil import copyfile
import os
from glob import glob
import errno
import argparse
from check_sizes import check_sizes

def resize_image(inputFileName, output_size, input_str, output_str):
    try:
        out_path = inputFileName.replace(input_str, output_str)

        if not os.path.exists(os.path.dirname(out_path)):
            try:
                os.makedirs(os.path.dirname(out_path))
            except OSError as exc:  # Guard against race condition
                print("OSError ", inputFileName)
                if exc.errno != errno.EEXIST:
                    raise

        assert out_path != inputFileName
        im = cv2.imread(inputFileName)
        shape = im.shape
        max_dim = max(shape[0], shape[1])
        scale_factor = output_size / max_dim

        im_resize = cv2.resize(im, (int(shape[1] * scale_factor), int(shape[0] * scale_factor)))
        delta_w = output_size - im_resize.shape[1]
        delta_h = output_size - im_resize.shape[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        im_resize = cv2.copyMakeBorder(im_resize, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        cv2.imwrite(out_path, im_resize)
    except:
        print("general failure ", inputFileName)


def main():
    parser = argparse.ArgumentParser(description="Resize images in a directory.")
    parser.add_argument("input_path", help="Path to the input directory.")
    parser.add_argument("output_path", help="Path to the output directory.")
    parser.add_argument("--output_size", type=int, default=224, help="Target size for the images.")
    args = parser.parse_args()

    num_threads = cpu_count() # Get the number of available CPU cores

    print("scanning files...")
    files = [y for x in os.walk(args.input_path) for y in glob(os.path.join(x[0], '*.*'))]
    print(f"done, start resizing using {num_threads} threads")

    pool = ThreadPool(num_threads) # Use the number of available CPU cores
    resize_image_fun = partial(resize_image, output_size=args.output_size, input_str=args.input_path, output_str=args.output_path)
    pool.map(resize_image_fun, files)
    
    check_sizes(args.input_path)
    check_sizes(args.output_path)

if __name__ == '__main__':
    main()