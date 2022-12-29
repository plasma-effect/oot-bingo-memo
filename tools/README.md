# tools

ツールが入ってます

**管理者へ：追加、更新したら使い方を書くこと！**

## goal_to_yaml

ootbingoリポジトリのgoal-list.jsの中身をyamlに変換するツール。

### 引数(goal_to_yaml)

- 位置引数
  - 変換したいgoal-list.jsのパス
- `--short`(`-s`)
  - short用タスクリストの出力先
- `--normal`(`-n`)
  - normal用タスクリストの出力先

## check_diff

バージョン間のdiffを取るツール。dataディレクトリ内のファイルを使ってください。

### 引数(check_diff)

- 位置引数
  - 第1引数：前のバージョンのdataのパス
  - 第2引数：次のバージョンのdataのパス
- `--output`(`-o`)
  - 出力先、省略した場合標準出力
