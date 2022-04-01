import requests
from selenium import webdriver
import time

# キーワードとダウンロードする画像の数を決め、
# キーワードを検索した結果ページを定義

kw = input('画像のキーワードを入力してください。(英語のみ)\n')
url = f'https://www.pexels.com/ja-jp/search/{kw}/'
indx = 1

# 枚数の入力が間違えている場合や30枚を超えるとプログラムを終了

try:
    max_cnt = int(input('ダウンロードする画像の数を入力してください。\n'))
except ValueError:
    print('数字のみで入力してください\nプログラムを終了致します。')
    time.sleep(1)
    quit()

if max_cnt <= 0:
    try:
        raise ValueError
    except ValueError:
        print('正しい数字を入力してください\nプログラムを終了致します。')
        time.sleep(1)
        quit()

# ブラウザーを開き、画像をリスト化

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)

# スクロールダウンしながら画像を読み込む
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    time.sleep(1)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

photo_items = driver.find_elements_by_class_name('photo-item__img')
image_urls = [i.get_attribute('data-big-src') for i in photo_items]

# リスト化した画像をファイルとしてダウンロード

for image_url in image_urls:
    driver.get(image_url)

    res = requests.get(image_url)
    if res.ok is True:
        file_name = f'{kw}_{indx}.jpeg'
        with open(file_name, 'wb') as f:
            f.write(res.content)
        print(f'ダウンロード中：({indx}) {file_name}')
        indx += 1
    
    if indx > max_cnt:
        print('全てのダウンロードを完了いたしました。')
        break

driver.close()
