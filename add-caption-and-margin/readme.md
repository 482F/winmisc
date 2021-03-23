### 使用法
python3 add-caption-and-margin.py csv_path.csv [start_index]

- csv_path.csv を読み取って一行ごとに画像を処理する
  - start_index を指定すると csv_path.csv の start_index 行目から処理を開始する

### csv の書式

|sharp|filepath|outputname|width|height|anchor_x|anchor_y|margin|comment|
|:-------|:---------|:----|:-----|:-------|:-------|:-----|:------|
||default_value.jpg||long|long|left|top|long*0.01||

- sharp
  - `#` を入れるとその行は飛ばされる
- filepath
  - 加工元の jpg のパス
- outputname
  - 出力名
  - `実行したディレクトリ¥output¥outputname` に出力される
- width, height
  - 加工後の横幅、縦幅
  - 加工前より大きい値ならば余白が追加され、小さい値ならば切り取られる
  - 余白の追加箇所は anchor_x, anchor_y によって指定する
  - 後述の予約語置換と演算機能がある
- anchor_x
  - 画像に余白を追加する、もしくは画像を切り取る際に画像をどこに固定するか
  - left, center, right のいずれかを指定する
- anchor_y
  - 画像に余白を追加する、もしくは画像を切り取る際に画像をどこに固定するか
  - top, center, bottom のいずれかを指定する
- margin
  - 上下左右に追加される余白の幅
  - 0 ならば余白は追加されない
  - 後述の変数置換と演算機能がある
- comment
  - 余白部分に追加されるコメントの本文
  - ここが空白でない場合、一部のパラメータは以下のもの以外指定できなくなる
    - width: long
    - height: long
    - anchor_x: 横長の画像の場合は center、縦長の画像の場合は left
    - anchor_y: 横長の画像の場合は top、縦長の画像の場合は center

#### 備考

- filepath を空欄にし、comment に値を入れることでコメントのみの画像を出力することができる
  - このとき width を指定する必要がある
- width, height, margin には予約語の置換機能と演算機能がある
  - 予約語: 置換先
    - long: filepath の画像の長辺の長さ
    - short: filepath の画像の短辺の長さ
    - width: filepath の画像の横幅
    - height: filepath の画像の縦幅
  - 演算機能
    - `long+30` や、`width*1.3` のように、`+`, `*`, `-` を使った計算ができる
    - 演算子の間に空白を入れるとエラーが出る

### その他

- 画像が縦長か横長かを判別して comment を付ける。縦横同じ幅の場合は横長として扱われる
- 一部のエラーでは原因と、エラーが起こった場所から再開するためのコマンドが表示される
  - ex. `python3 C:¥add-caption-and-margin¥add-caption-and-margin.py C:¥add-caption-and-margin¥csv.csv 15`
