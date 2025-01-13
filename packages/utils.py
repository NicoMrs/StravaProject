# utils.py
import os
import json


def save_json(base_dir, file, data):
    """ Save Json file in directory dir """
    filepath = os.path.join(base_dir, file)

    with open(filepath, 'a+') as outfile:
        json.dump(data, outfile)


def clear_file(base_dir, file):
    """ Remove file from directory"""
    filepath = os.path.join(base_dir, file)
    if os.path.isdir(filepath):
        os.remove(os.path.join(base_dir, file))
