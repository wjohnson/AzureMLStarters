# imports
import argparse

import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    # We expect the command to provide a set of input parameters
    # including the hyperparameter values
    # This is different than running a normal sklearn hyperparameter tuning since the
    # below script effectively runs just one iteration of the hyperparameters
    parser = argparse.ArgumentParser()
    # These are the boilerplate ones that every Azure ML job should have
    parser.add_argument("--data", type=str)
    parser.add_argument("--split_column", type=str, help="The name of the column to split the file by")
    parser.add_argument("--split_files_folder", type=str, help="Folder name for the output data")

    # args = parser.parse_args(['--data', '.\\datasets\\retail\\online_retail_II.xlsx', '--split_column', 'Country', '--split_files_folder', '.\\downloads\\'])
    args = parser.parse_args()
    # In this case, we are using a specific excel file but this could be generalized
    # by adding parameters.
    df = pd.read_excel(args.data, sheet_name="Year 2009-2010")
    input_path = Path(args.data)


    distinct_values = df[args.split_column].unique()
    for group in distinct_values:
        group_row_filter = df[args.split_column] == group
        sub_df = df[group_row_filter]

        group_path = (Path(args.split_files_folder) / (input_path.stem + f"__{group}")).with_suffix(".csv")
        print(group, group_path, sep=":")
        sub_df.to_csv(group_path)
