import csv
import os
from shutil import copyfile
import numpy as np
import subprocess

# defaults
DEFAULT_LABEL_FILE = './data/class_labels_indices.csv'
DEFAULT_CSV_DATASET = './data/unbalanced_train_segments.csv'
DEFAULT_DEST_DIR = './output/'
DEFAULT_FS = 16000

def download(partitionNumber, args):
    # construct path to destination dir
    dst_dir_root = args.destination_dir if args.destination_dir is not None else DEFAULT_DEST_DIR

    if not os.path.isdir(dst_dir_root):
        os.makedirs(dst_dir_root)
        print("dst_dir: " + dst_dir_root)

    partition_csv = f"./output/partition{partitionNumber}.csv"
    with open(partition_csv) as dataset:
        reader = csv.reader(dataset)

        for row in reader:
            # print command for debugging
            print("ffmpeg -ss " + str(row[1]) + " -t 10 -i $(youtube-dl -f 'bestaudio' -g https://www.youtube.com/watch?v=" +
                       str(row[0]) + ") -ar " + str(DEFAULT_FS) + " -- \"" + dst_dir_root + "/" + str(row[0]) + "_" + row[1] + ".wav\"")
            os.system(("ffmpeg -ss " + str(row[1]) + " -t 10 -i $(youtube-dl -f 'bestaudio' -g https://www.youtube.com/watch?v=" +
                       str(row[0]) + ") -ar " + str(DEFAULT_FS) + " -- \"" + dst_dir_root + "/" + str(row[0]) + "_" + row[1] + ".wav\""))


def generatePartitions(num_partitions):
    with open(DEFAULT_CSV_DATASET) as dataset:
        reader = csv.reader(dataset, skipinitialspace=True)
        data = list(reader)
    data.pop(0)
    data.pop(0)
    total = len(data)
    print(f"total lines: {total}")
    slices = np.linspace(0, total, num_partitions+1)
    for i in range(num_partitions):
        to_write = data[int(slices[i]):int(slices[i+1])]
        new_csv_partition = f"./output/partition{i}.csv"
        with open(new_csv_partition, 'w', newline='') as new_csv:
            writer = csv.writer(new_csv)
            writer.writerows(to_write)