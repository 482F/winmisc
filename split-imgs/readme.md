### 使用法
python3 split-imgs.py csv_path.csv [start_index]

- csv_path.csv を読み取って一行ごとに画像を処理する
  - start_index を指定すると csv_path.csv の start_index 行目から処理を開始する

### csv の書式

|sharp|filepath|square_side|
|:----|:-------|:----------|
||default_value.jpg|left|

- sharp
  - `#` を入れるとその行は飛ばされる
- filepath
  - 加工元の jpg のパス
- square_side
  - 左右どちらを正方形にするか決める

### その他

- 縦長の画像を入れるとエラーが出る
