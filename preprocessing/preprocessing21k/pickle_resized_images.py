import os
import pickle
import zlib

def process_dataset(path_to_dataset, output_file_path):
    # Collecting information
    keys_relative = [os.path.join(root, file) for root, dirs, files in os.walk(path_to_dataset) for file in files if file.endswith(('.JPEG', '.PNG'))]
    classes = sorted(set(os.path.split(os.path.split(path)[0])[1] for path in keys_relative))
    class_to_idx = {class_name: idx for idx, class_name in enumerate(classes)}

    # Serializing and compressing
    data_to_pickle = (keys_relative, classes, class_to_idx)
    compressed_data = zlib.compress(pickle.dumps(data_to_pickle))

    # Writing to file
    with open(output_file_path, 'wb') as fp:
        fp.write(compressed_data)

    print(f"Pickled {len(keys_relative)} files in {path_to_dataset}")

#fix paths
# Path to the resized training and validation sets
path_to_train_set = '/mnt/imagenet21k_resized_new/imagenet21k_train'
path_to_val_set = '/mnt/imagenet21k_resized_new/imagenet21k_val'

# Output paths
output_train_file_path = '/home/jabarne6/repos/vit-imagenet21k-p/resources/datasets_imagenet21k_resized_train.pkl'
output_val_file_path = '/home/jabarne6/repos/vit-imagenet21k-p/resources/datasets_imagenet21k_resized_val.pkl'

# Process both training and validation sets
process_dataset(path_to_train_set, output_train_file_path)
process_dataset(path_to_val_set, output_val_file_path)


