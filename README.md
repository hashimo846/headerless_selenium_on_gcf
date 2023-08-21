# このリポジトリは
Google Cloud Functionsにて、seleniumを使ってヘッドブラウザでスクレイピングを行うためのプログラム
# 使い方
1. `unzip headless-chromium.zip`
2. `zip deploy headless-chromium chromedriver main.py requirements.txt`
3. Cloud FunctionsにZipファイルにて`deploy.zip`をデプロイ