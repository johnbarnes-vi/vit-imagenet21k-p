# --------------------------------------------------------
# ImageNet-21K Pretraining for The Masses
# Copyright 2021 Alibaba MIIL (c)
# Licensed under MIT License [see the LICENSE file for details]
# Written by Tal Ridnik
# --------------------------------------------------------
pwd
mkdir -p /mnt/imagenet21k_new/imagenet21k_train
export ROOT=/mnt/imagenet21k_new/imagenet21k_train # target folder, adjust this path

# untarring the original tar to 21k tar's:
tar -xvf winter21_whole.tar.gz -C $ROOT


find . -type f -print | wc -l # 21841

# extracting all tar's in parallel (!)
cd $ROOT
find . -name "*.tar" | parallel 'echo {};  ext={/}; target_folder=${ext%.*}; mkdir -p $target_folder;  tar  -xf {} -C $target_folder'

# counting the nubmer of classes
find ./ -mindepth 1 -type d | wc -l # 21841

# delete all tar's
cd $ROOT
rm *.tar

# Remove uncommon classes for transfer learning
BACKUP=/mnt/imagenet21k_new/imagenet21k_small_classes
mkdir -p ${BACKUP}
for c in ${ROOT}/n*; do
    count=`ls $c/*.JPEG | wc -l`
    if [ "$count" -gt "500" ]; then
        echo "keep $c, count = $count"
    else
        echo "remove $c, $count"
        mv $c ${BACKUP}/
    fi
done

# counting the number of valid classes
find ./ -mindepth 1 -type d | wc -l  # 11221

# create validation set, 50 images in each folder
VAL_ROOT=/mnt/imagenet21k_new/imagenet21k_val
mkdir -p ${VAL_ROOT}
export ROOT=/mnt/imagenet21k_new/imagenet21k_train
for i in ${ROOT}/n*; do
    c=`basename $i`
    echo $c
    mkdir -p ${VAL_ROOT}/$c
#    for j in `ls $i/*.JPEG | shuf | head -n 50`; do
    for j in `ls $i/*.JPEG | head -n 50`; do # no shuf for reproducibility
        mv $j ${VAL_ROOT}/$c/
    done
done


# resizing, pickling an index, then validating the index
python ../resize.py /mnt/imagenet21k_new/ /mnt/imagenet21k_resized_new/ # change this with real names
python pickle_resized_images.py
python validating_files.py