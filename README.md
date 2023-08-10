
# ImageNet-21K Preprocessing Project

This repository contains the code and scripts required to preprocess the ImageNet-21K dataset, starting from the original 1.3TB `.tar` file downloaded from image-net.org. The preprocessing steps transform the dataset into a resized, indexed version, stored in the `/mnt/` directory, with a serialized index (pickled object mapping) in the actual project repository. Most of the preprocessing code comes from the paper "ImageNet21k Pretraining for the masses" by Tal Ridnik, Emanuel Ben-Baruch, Asaf Noy, Lihi Zelnik-Manor, with the exception of the `pickle_resized_images.py` script, which was authored as part of this project.

## Overview

The project focuses on a series of preprocessing steps to handle the ImageNet-21K dataset, transforming it from a single `.tar` file to a resized, indexed version with a serialized index.

### Preprocessing

The `preprocessing` directory contains the scripts to handle the stages of extraction, organization, resizing, and indexing.

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

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
