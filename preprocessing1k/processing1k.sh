# ensure you have unpacked all the imagenet1k files in /mnt/imagenet1k
# at minimum you need the dev-kit for the ground-truth, the training set, and the val set
python resize1k.py
python fix_val.py