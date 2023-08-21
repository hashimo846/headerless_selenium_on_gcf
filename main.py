import os
import shutil
import stat
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import sys, io

global driver

# 実行権限の付与
def add_execute_permission(path: Path, target: str = "u") -> None:
    """Add `x` (`execute`) permission to specified targets."""
    mode_map = {
        "u": stat.S_IXUSR,
        "g": stat.S_IXGRP,
        "o": stat.S_IXOTH,
        "a": stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
    }
    mode = path.stat().st_mode
    for t in target:
        mode |= mode_map[t]
    path.chmod(mode)

# ドライバーを設定
def settingDriver() -> None:
    global driver
    # ドライバーとヘッドレスブラウザのパス
    print("driver setting")
    driverPath = "/tmp" + "/chromedriver"
    headlessPath = "/tmp" + "/headless-chromium"
    # 実行可能なディレクトリにコピーして権限を付与
    print("copy headless-chromium")
    shutil.copyfile(os.getcwd() + "/headless-chromium", headlessPath)
    add_execute_permission(Path(headlessPath), "ug")
    print("copy chromedriver")
    shutil.copyfile(os.getcwd() + "/chromedriver", driverPath)
    add_execute_permission(Path(driverPath), "ug")
    # ブラウザの設定
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--v=99")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = headlessPath
    # ドライバーを取得
    print("get driver")
    driver = webdriver.Chrome(executable_path=driverPath, chrome_options=chrome_options)

# メイン処理
def seleniumSample(request):
    global driver
    request_json = request.get_json()
    url = request_json["url"]
    settingDriver()
    try:
        print("URL get")
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for s in soup(['script', 'style']):
            s.decompose()
        text = ' '.join(soup.stripped_strings)
        print(text)
    finally:
        print("driver quit")
        driver.quit()
    return text
