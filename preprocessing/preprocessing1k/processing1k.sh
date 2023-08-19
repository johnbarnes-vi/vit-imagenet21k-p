# ensure you have unpacked all the imagenet1k files in /mnt/imagenet1k
# at minimum you need the dev-kit for the ground-truth, the training set, and the val set

# ADD THE `tar` COMMANDS TO UNPACK EVERYTHING IN PARALLEL HERE, ITS LAST STEP BEFORE FULLY AUTOMATED PREPROCESSING PIPELINE
python ../resize.py /mnt/imagenet1k/ /mnt/imagenet1k_resized/ # fix these paths
python fix_val.py