# imports
import argparse

import pandas as pd
from pathlib import Path
import os
from distutils.dir_util import copy_tree

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--many_models_path", type=str, help="The folder containing the trained models")
    parser.add_argument("--final_model", type=str, help="The path to the final model")

    args = parser.parse_args()

    print(f"many_models_path path is {args.many_models_path}")
    print(f"final_model path is {args.final_model}")
    if not os.path.exists(args.many_models_path):
        print("many_models_path Path does NOT exist")
        exit()
    
    print(f"data path IsFile: {os.path.isfile(args.many_models_path)}")
    print(f"data path IsDirectory: {os.path.isdir(args.many_models_path)}")
    print(f"final_model path IsFile: {os.path.isfile(args.final_model)}")
    print(f"final_model path IsDirectory: {os.path.isdir(args.final_model)}")
    

    if os.path.isdir(args.many_models_path):
        files_in_data = os.listdir(args.many_models_path)

        for dirpath, dirnames, filenames in os.walk(args.many_models_path):
            print(dirpath, dirnames, filenames)
    
        print("Copying content to magical output folder")
        copy_tree(src=Path(args.many_models_path), dst = args.final_model)
        print("Copied content. Walking directory")
        for dirpath, dirnames, filenames in os.walk(args.final_model):
            print(dirpath, dirnames, filenames)