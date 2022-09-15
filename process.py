import argparse
import os
import core.utils as utils
from multiprocessing import Process, Queue
import time


if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, choices=['partitions', 'download'])
    parser.add_argument('--num_partitions', type=int, nargs='?')
    parser.add_argument('--partition', type=int, nargs='?')

    # parser.add_argument('-b', '--blacklist', nargs='+', type=str,
    #                     help='list of classes which will exclude a clip from being downloaded')
    # parser.add_argument('-d', '--destination_dir', type=str,
    #                     help='directory path to put downloaded (or found) files into')
    # parser.add_argument('--audio_data_dir', type=str,
    #                     help='directory path containing pre-downloaded files from AudioSet')
    # parser.add_argument('-fs', "--sample_rate", type=int,
    #                     help="Sample rate of audio to download. Default 16kHz")
    # parser.add_argument('-s', '--strict',
    #                     help='If used, only match exact string argument passed')
    # parser.add_argument('--label_file', type=str,
    #                     help='Path to CSV file containing AudioSet labels for each class')
    # parser.add_argument('--csv_dataset', type=str,
    #                     help='Path to CSV file containing AudioSet in YouTube-id/timestamp form')

    parser.set_defaults(
        label_file='./data/class_labels_indices.csv',
        csv_dataset='./data/unbalanced_train_segments.csv',
        destination_dir='./output',
        fs=16000,
        num_partitions=1,
        mode = 'partitions'
    )

    args = parser.parse_args()

    if args.destination_dir is not None and not os.path.isdir(args.destination_dir):
        os.makedirs(args.destination_dir)

    if args.mode =="partitions":
        utils.generatePartitions(args.num_partitions)
    elif args.mode == "download":
        utils.download(args.partition, args)

    end = time.time()
    print(f"Total download time {end-start}")