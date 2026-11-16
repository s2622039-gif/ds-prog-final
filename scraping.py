
import requests
from bs4 import BeautifulSoup
import time
import sqlite3

# -------------------------
# 1. GitHubからHTMLを取得
# -------------------------

url = "https://github.com/orgs/google/repositories"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20
)

print("ステータスコード:", response.status_code)

time.sleep(1)

soup = BeautifulSoup(response.text, "html.parser")


# -------------------------
# 2. スター数を数値に変換
# -------------------------

def convert_stars(value):
    value = value.strip().lower()

    if value.endswith("k"):
        return int(float(value[:-1]) * 1000)

    return int(value.replace(",", ""))


# -------------------------
# 3. リポジトリ情報を取得
# -------------------------

repo_data = []

repo_links = soup.select('a[href^="/google/"]')

for link in repo_links:
    href = link.get("href", "")
    parts = href.strip("/").split("/")

    if len(parts) == 2 and all(parts):

        repo_item = link.find_parent("li")

        if repo_item is None:
            continue

        repo_name = link.get_text(strip=True)

        language_element = repo_item.select_one(
            ".PrimaryLanguageName__94OAQO"
        )

        language = (
            language_element.get_text(strip=True)
            if language_element else "不明"
        )

        star_link = repo_item.select_one(
            'a[href$="/stargazers"]'
        )

        stars_text = (
            star_link.get_text(strip=True)
            if star_link else "0"
        )

        stars = convert_stars(stars_text)

        repo_data.append({
            "name": repo_name,
            "language": language,
            "stars": stars
        })

        time.sleep(1)


print("取得件数:", len(repo_data))


# -------------------------
# 4. SQLiteデータベースに接続
# -------------------------

conn = sqlite3.connect("github_repos.db")

cursor = conn.cursor()


# -------------------------
# 5. テーブルを作成
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    language TEXT,
    stars INTEGER
)
""")


# -------------------------
# 6. データを登録
# -------------------------

cursor.executemany("""
INSERT OR REPLACE INTO repositories
(name, language, stars)
VALUES (?, ?, ?)
""", [
    (data["name"], data["language"], data["stars"])
    for data in repo_data
])

conn.commit()

print("データベースへの保存が完了しました！")


# -------------------------
# 7. SQLでデータを表示
# -------------------------

cursor.execute("""
SELECT name, language, stars
FROM repositories
ORDER BY stars DESC
""")

results = cursor.fetchall()

print("\nデータベースの保存結果")

for row in results:
    print(row)


# -------------------------
# 8. データベースを閉じる
# -------------------------
# 使用言語ごとのリポジトリ数
cursor.execute("""
SELECT language, COUNT(*)
FROM repositories
GROUP BY language
ORDER BY COUNT(*) DESC
""")

results = cursor.fetchall()

print("\n言語ごとのリポジトリ数")
for row in results:
    print(row)

# 使用言語ごとの平均スター数
cursor.execute("""
SELECT language, AVG(stars)
FROM repositories
GROUP BY language
ORDER BY AVG(stars) DESC
""")

results = cursor.fetchall()

print("\n言語ごとの平均スター数")
for row in results:
    print(row)

cursor.execute("""
SELECT COUNT(*)
FROM repositories
WHERE language = 'Python'
""")

result = cursor.fetchone()

print("\nPythonのリポジトリ数")
print(result[0])


# 言語ごとのリポジトリ数が2件以上のものを表示
cursor.execute("""
SELECT language, COUNT(*)
FROM repositories
GROUP BY language
HAVING COUNT(*) >= 2
ORDER BY COUNT(*) DESC
""")

results = cursor.fetchall()

print("\nリポジトリ数が2件以上ある言語")
for row in results:
    print(row)
conn.close()

print("\n処理が完了しました！")
