SPLIT_PATH="/media/ziyuexu/Data/FL_Dataset/XGB_dataset/epsilon"

echo "Split training/validation data"
OUTPUT_PATH="${SPLIT_PATH}/base_xgb_data"
python3 utils/prepare_data_base.py \
--data_type 2 \
--data_path "${DATASET_PATH}" \
--out_path "${OUTPUT_PATH}"

echo "Split training data horizontally for flare"
OUTPUT_PATH="${SPLIT_PATH}/horizontal_xgb_data_flare"
python3 utils/prepare_data_horizontal.py \
--target_app 0 \
--data_path "${SPLIT_PATH}/base_xgb_data/train.csv" \
--site_num 3 \
--out_path "${OUTPUT_PATH}" \
--out_filename "train.csv"

echo "Validation data pass-through for horizontal case for flare"
OUTPUT_PATH="${SPLIT_PATH}/horizontal_xgb_data_flare"
python3 utils/prepare_data_horizontal.py \
--target_app 0 \
--data_path "${SPLIT_PATH}/base_xgb_data/valid.csv" \
--site_num 1 \
--out_path "${OUTPUT_PATH}" \
--out_filename "valid.csv"

echo "Move the validation file one level above since it is the same for all clients"
mv ${OUTPUT_PATH}/site-1/valid.csv ${OUTPUT_PATH}/valid.csv

echo "Split training data horizontally for fate"
OUTPUT_PATH="${SPLIT_PATH}/horizontal_xgb_data_fate"
python3 utils/prepare_data_horizontal.py \
--target_app 1 \
--data_path "${SPLIT_PATH}/base_xgb_data/train.csv" \
--site_num 3 \
--out_path "${OUTPUT_PATH}" \
--out_filename "train.csv"

echo "Validation data pass-through for horizontal case for fate"
OUTPUT_PATH="${SPLIT_PATH}/horizontal_xgb_data_fate"
python3 utils/prepare_data_horizontal.py \
--target_app 1 \
--data_path "${SPLIT_PATH}/base_xgb_data/valid.csv" \
--site_num 1 \
--out_path "${OUTPUT_PATH}" \
--out_filename "valid.csv"

echo "Move the validation file one level above since it is the same for all clients"
mv ${OUTPUT_PATH}/site-1/valid.csv ${OUTPUT_PATH}/valid.csv

echo "Split training data vertically for flare"
OUTPUT_PATH="${SPLIT_PATH}/vertical_xgb_data_flare"
python3 utils/prepare_data_vertical.py \
--target_app 0 \
--data_path "${SPLIT_PATH}/base_xgb_data/train.csv" \
--site_num 2 \
--out_path "${OUTPUT_PATH}" \
--out_filename "train.csv"

echo "Split validation data vertically for flare"
OUTPUT_PATH="${SPLIT_PATH}/vertical_xgb_data_flare"
python3 utils/prepare_data_vertical.py \
--target_app 0 \
--data_path "${SPLIT_PATH}/base_xgb_data/valid.csv" \
--site_num 2 \
--out_path "${OUTPUT_PATH}" \
--out_filename "valid.csv"

echo "Split training data vertically for fate"
OUTPUT_PATH="${SPLIT_PATH}/vertical_xgb_data_fate"
python3 utils/prepare_data_vertical.py \
--target_app 1 \
--data_path "${SPLIT_PATH}/base_xgb_data/train.csv" \
--site_num 2 \
--out_path "${OUTPUT_PATH}" \
--out_filename "train.csv"

echo "Split validation data vertically for fate"
OUTPUT_PATH="${SPLIT_PATH}/vertical_xgb_data_fate"
python3 utils/prepare_data_vertical.py \
--target_app 1 \
--data_path "${SPLIT_PATH}/base_xgb_data/valid.csv" \
--site_num 2 \
--out_path "${OUTPUT_PATH}" \
--out_filename "valid.csv"
