# put tar files from imagenet website into /mnt/imagenet1k/ for code coherence
# you only need the dev-kit for the ground-truth, the training set, and the val set tar files
# be sure to activate virtual environment for dependencies before running

# Define directory paths
RESIZED_DIR="/mnt/imagenet1k_resized"
DEVKIT_DIR=$RESIZED_DIR
TRAIN_DIR="/mnt/imagenet1k/ILSVRC2012_img_train"
VAL_DIR="/mnt/imagenet1k/ILSVRC2012_img_val"

# Create directories for unpacking
mkdir -p $RESIZED_DIR
mkdir -p $DEVKIT_DIR
mkdir -p $TRAIN_DIR
mkdir -p $VAL_DIR

# Unpack dev-kit into its new directory
tar -xzvf /mnt/imagenet1k/ILSVRC2012_devkit_t12.tar.gz -C $DEVKIT_DIR &

# Unpack training set into its directory
tar -xvf /mnt/imagenet1k/ILSVRC2012_img_train.tar -C $TRAIN_DIR &

# Unpack validation set into its directory
tar -xvf /mnt/imagenet1k/ILSVRC2012_img_val.tar -C $VAL_DIR &

# Wait for all background jobs to complete
wait

# Unpack sub-tarballs in training set directory
for f in $TRAIN_DIR/*.tar; do
    base=$(basename $f)  # Extract the base name of the file
    d="${TRAIN_DIR}/${base%.tar}"  # Create directory path
    mkdir -p $d
    tar -xvf $f -C $d &
done

# Wait for all background jobs to complete
wait

# Remove all tar files in the training directory
find $TRAIN_DIR -name "*.tar" -exec rm {} +

# ADD REMOVAL OF /mnt/imagenet1k/ILSVRC2012_img_val & /mnt/imagenet1k/ILSVRC2012_img_train

# Optional: remove tar files if you wish (uncomment the following lines)
#rm $DEVKIT_DIR.tar.gz
#rm $TRAIN_DIR.tar
#rm $VAL_DIR.tar

# Resize images to standard resolution without losing aspect ratio
python3 ../resize.py /mnt/imagenet1k/ILSVRC2012_img_train /mnt/imagenet1k_resized/ILSVRC2012_img_train
python3 ../resize.py /mnt/imagenet1k/ILSVRC2012_img_val /mnt/imagenet1k_resized/ILSVRC2012_img_val

# Organize resulting directory's structure
python3 fix_val.py
