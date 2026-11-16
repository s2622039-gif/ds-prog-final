# GitHub Repository Scraping

## 概要
Pythonを使用して、GitHubのGoogle組織が公開しているリポジトリ情報をスクレイピングし、SQLiteデータベースに保存するプログラムです。

## 取得するデータ
- リポジトリ名
- 主要プログラミング言語
- スター数

## 使用技術
- Python
- requests
- BeautifulSoup
- SQLite

## 主な処理
1. GitHubのGoogle組織のリポジトリ一覧ページにアクセスする
2. HTMLからリポジトリ情報を取得する
3. スター数を数値に変換する
4. SQLiteデータベースに保存する
5. SQLを使用してデータを表示・集計する

## 実行方法

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

プログラムを実行します。

```bash
python scraping.py
```

実行すると、取得したリポジトリ情報が `github_repos.db` に保存されます。

## 注意事項
GitHub APIは使用せず、HTMLをスクレイピングしています。アクセス時には `time.sleep(1)` を使用しています。
