# Vision Transformers with ImageNet-21K-P

## Overview

This project aims to explore computer vision at scale by utilizing the massive ImageNet-21K dataset. The goal is to leverage this large and diverse dataset to learn about non-trivial applications of computer vision at scale. 

Currently, the repository contains code and scripts for preprocessing the dataset, transforming it from the original 1.3TB file into an organized, resized, and indexed version.

The project's next stage involves training a Vision Transformer (ViT) on the processed ImageNet-21K dataset.

### Preprocessing

The `preprocessing` directory contains the code and scripts required to preprocess the ImageNet-21K dataset, starting from the original 1.3TB `winter21_whole.tar.gz` file downloaded from image-net.org. The preprocessing steps transform the dataset into a resized, indexed version, stored in the `/mnt/` directory, with a serialized index (pickled object mapping) in the actual project repository.

Most of the preprocessing code comes from the paper "ImageNet21k Pretraining for the Masses" by Tal Ridnik et al, with the exception of the `pickle_resized_images.py` script, which was authored as part of this project.

### Resources

The `resources` directory contains serialized indices of the datasets, enabling efficient referencing of images and classes.

## Requirements

Refer to the `requirements.txt` file for the dependencies required to run the project.

## Usage

To run the preprocessing, simply execute the `processing_script.sh` script. This script manages the entire preprocessing workflow, including extraction, organization, resizing, serialization, and validation.

```bash
./processing_script.sh
```

Ensure that the script has execute permissions before running. You may need to run `chmod +x processing_script.sh` if necessary.

## License

This project is licensed under the MIT License.