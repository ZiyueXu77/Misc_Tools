# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os

import pandas as pd


def data_split_args_parser():
    parser = argparse.ArgumentParser(description="Generate data split for dataset")
    parser.add_argument(
        "--data_type",
        type=int,
        default=2,
        help="Type of data: 0 - CreditCard, 1 - Higgs, 2 - Epsilon",
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="/media/ziyuexu/Data/HIGGS/HIGGS.csv",
        help="Path to data file"
    )
    parser.add_argument(
        "--out_path",
        type=str,
        default="/media/ziyuexu/Data/FL_Dataset/higgs/xgb_dataset/",
        help="Output path for the data split file",
    )
    return parser


def main():
    parser = data_split_args_parser()
    args = parser.parse_args()

    if(args.data_type == 0):
        df = pd.read_csv(args.data_path)
        # drop Time and Amount column
        df = df.drop(columns=["Time", "Amount"])
        # move Class column to the first column
        df = pd.concat([df["Class"], df.drop(columns=["Class"])], axis=1)
    elif(args.data_type == 1):
        df = pd.read_csv(args.data_path)
    elif(args.data_type == 2):
        # load Epsilon data
        from catboost.datasets import epsilon
        epsilon_train, _ = epsilon()
        df = pd.DataFrame(epsilon_train)


    rows_total, cols_total = df.shape[0], df.shape[1]

    print(f"rows_total: {rows_total}, cols_total: {cols_total}")

    if not os.path.exists(args.out_path):
        os.makedirs(args.out_path, exist_ok=True)

    # assign first 80% rows to train
    df_train = df.iloc[: int(0.8 * df.shape[0]), :]
    # assign last 20% rows to valid
    df_valid = df.iloc[int(0.8 * df.shape[0]) :, :]
    # save train and valid data
    df_train.to_csv(path_or_buf=os.path.join(args.out_path, "train.csv"), index=False, header=False)
    df_valid.to_csv(path_or_buf=os.path.join(args.out_path, "valid.csv"), index=False, header=False)
    # print the size of train and valid data
    print(f"train size: {df_train.shape[0]}")
    print(f"valid size: {df_valid.shape[0]}")


if __name__ == "__main__":
    main()
