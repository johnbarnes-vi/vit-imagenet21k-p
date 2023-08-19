import os
import argparse
from PIL import Image
from concurrent.futures import ProcessPoolExecutor

def get_image_size(file_path):
    with Image.open(file_path) as img:
        return img.size[0], img.size[1], file_path

def check_sizes(directory):
    largest_image = (0, 0)
    smallest_image = (float('inf'), float('inf'))
    largest_path = smallest_path = None

    def jpeg_file_generator():
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.lower().endswith(('.jpeg', '.jpg')):
                    yield os.path.join(root, file_name)

    jpeg_files = jpeg_file_generator()
    print(f"jpeg_files generator created")

    # Process the images in parallel
    with ProcessPoolExecutor() as executor:
        for width, height, file_path in executor.map(get_image_size, jpeg_files):
            # Check if this image is the largest
            if width * height > largest_image[0] * largest_image[1]:
                largest_image = (width, height)
                largest_path = file_path

            # Check if this image is the smallest
            if width * height < smallest_image[0] * smallest_image[1]:
                smallest_image = (width, height)
                smallest_path = file_path

    print(f"Inside {directory}:")
    print("Largest Image Resolution:", largest_image, "Path:", largest_path)
    print("Smallest Image Resolution:", smallest_image, "Path:", smallest_path)

def main():
    parser = argparse.ArgumentParser(description="Find the largest and smallest JPEG images in a directory.")
    parser.add_argument("directory", help="Path to the directory to scan.")
    args = parser.parse_args()
    
    check_sizes(args.directory)

if __name__ == '__main__':
    main()


