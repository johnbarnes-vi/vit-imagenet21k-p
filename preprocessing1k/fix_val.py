import os
import shutil
import scipy.io

# Function to load mappings between synsets, wnids, and words from meta.mat
def load_mappings(mat_path):
    meta_data = scipy.io.loadmat(mat_path)
    synsets = meta_data['synsets']
    # Map synsets to wnids
    synset2wnid = {int(s[0][0][0][0]): str(s[0][1][0]) for s in synsets}
    # Map wnids to words (descriptions)
    wnid2words = {str(s[0][1][0]): str(s[0][2][0]) for s in synsets}
    return synset2wnid, wnid2words

# Function to read ground truth labels from a text file
def read_ground_truth(file_path):
    with open(file_path, 'r') as file:
        labels = [int(line.strip()) for line in file.readlines()]
    return labels

# Function to inspect the first 30 ground truth labels (for debugging)
def inspect_val_data(ground_truth_labels, wnids, wnids2words):
    for idx, label in enumerate(ground_truth_labels, start=1):
        print(idx, label, wnids[label], wnids2words[wnids[label]])
        if idx > 30:
            break

# Function to organize validation data into subdirectories by wnid
def organize_val_data(val_dir, ground_truth_labels, wnids, wnids2words):
    for idx, label in enumerate(ground_truth_labels, start=1):
        wnid = wnids[label]
        subdir = os.path.join(val_dir, wnid)
        os.makedirs(subdir, exist_ok=True) # Create subdir for wnid if it doesn't exist

        # Construct image name based on index, following the naming convention
        image_name = f'ILSVRC2012_val_{idx:08}.JPEG'
        source_image_path = os.path.join(val_dir, image_name)

        # Move the image to the corresponding wnid subdir
        dest_image_path = os.path.join(subdir, image_name)
        shutil.move(source_image_path, dest_image_path)
        print(f"Moved {image_name} to {wnid} ({wnids2words[wnid]})")

# Path to meta.mat and ground truth file
mat_path = '/mnt/imagenet1k_resized/ILSVRC2012_devkit_t12/data/meta.mat'
ground_truth_file_path = '/mnt/imagenet1k_resized/ILSVRC2012_devkit_t12/data/ILSVRC2012_validation_ground_truth.txt'
val_dir = '/mnt/imagenet1k_resized/ILSVRC2012_img_val'

# Load mappings and ground truth labels
wnids, wnids2words = load_mappings(mat_path)
ground_truth_labels = read_ground_truth(ground_truth_file_path)

# Organize validation data into subdirectories by wnid
organize_val_data(val_dir, ground_truth_labels, wnids, wnids2words)
