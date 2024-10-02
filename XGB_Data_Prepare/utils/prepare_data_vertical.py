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
import shutil

import numpy as np
import pandas as pd


def data_split_args_parser():
    parser = argparse.ArgumentParser(description="Generate data split for dataset")
    parser.add_argument("--data_path", type=str, help="Path to data file")
    parser.add_argument("--site_num", type=int, default=3, help="Total number of sites")
    parser.add_argument("--target_app", type=int, default=0, help="0-Flare, 1-FATE")
    parser.add_argument(
        "--out_path",
        type=str,
        default="./dataset",
        help="Output path for the data split file",
    )
    parser.add_argument("--out_filename", type=str)
    return parser


def split_num_proportion(n, site_num):
    split = []
    ratio_vec = np.ones(site_num)
    total = sum(ratio_vec)
    left = n
    for site in range(site_num - 1):
        x = int(n * ratio_vec[site] / total)
        left = left - x
        split.append(x)
    split.append(left)
    return split


def main():
    parser = data_split_args_parser()
    args = parser.parse_args()

    df = pd.read_csv(args.data_path, header=None)
    rows_total, cols_total = df.shape[0], df.shape[1]
    print(f"site_num: {args.site_num}")
    print(f"rows_total: {rows_total}, cols_total: {cols_total}")

    if args.target_app == 1:
        # FATE, add header and uid
        df["uid"] = df.index.to_series().map(lambda x: "uid_" + str(x))
        # move uid to the first column
        df = pd.concat([df["uid"], df.drop(columns=["uid"])], axis=1)
        df.columns = ["uid"] + ["y"] + [f"x{i}" for i in range(1, df.shape[1] - 1)]


    # split col
    cols_labelowner = int(cols_total * 0.4)
    site_col_size = split_num_proportion(cols_total - cols_labelowner, args.site_num - 1)
    site_col_size.insert(0, cols_labelowner)
    print(f"site_col_size: {site_col_size}")

    for site in range(args.site_num):
        col_start = sum(site_col_size[:site])
        col_end = sum(site_col_size[: site + 1])

        # split data, but keep uid column for FATE
        if args.target_app == 0:
            df_split = df.iloc[:, col_start:col_end]
        else:
            df_split = df.iloc[:, [0] + list(range(col_start+1, col_end+1))]
        print(f"site-{site + 1} split cols [{col_start}:{col_end}]")

        data_path = os.path.join(args.out_path, f"site-{site + 1}")
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)

        # save train and valid data
        if args.target_app == 0:
            df_split.to_csv(path_or_buf=os.path.join(data_path, args.out_filename), index=False, header=False)
        else:
            df_split = df_split.sample(frac=1)
            df_split.to_csv(path_or_buf=os.path.join(data_path, args.out_filename), index=False)


if __name__ == "__main__":
    main()
