from playwright.sync_api import sync_playwright
from time import sleep
import os

javIdListFile = ".\\ids.txt"
email = ""
password = ""
outTxtFile = ".\\vrUrls.txt"

if not os.path.exists(outTxtFile):
    with open(outTxtFile, "w") as f:
        print("CREATED OUTFILE")

def getIds():
    with open(javIdListFile, "r", encoding="utf8") as f:
        return [line.rstrip("\n") for line in f.readlines()]

def login(page):
    print("LOGGING IN DMM")
    page.goto("https://accounts.dmm.co.jp/service/login/password")
    page.locator('xpath=//*[@id="login_id"]').click()
    page.keyboard.type(email, delay=70)
    print("EMAIL INSERTED")
    sleep(3)
    page.locator('xpath=//*[@id="password"]').click()
    page.keyboard.type(password, delay=80)
    print("PASSWORD INSERTED")
    sleep(3)
    page.locator('css=#use_auto_login').click()
    sleep(0.3)
    print("CHECKBOX CHECKED")
    page.locator('xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div/div/div/div/div/div/div/div[2]/form/button').click()
    print("DONE LOGGING IN")
    sleep(3)

def writeVrUrls(urls):
    with open(outTxtFile, "a", encoding="utf8") as f:
        for url in urls:
            f.write(url)
            f.write("\n")
    print(f"urls written in: {outTxtFile}")

def main():
    with sync_playwright() as playwright:
        firefox = playwright.chromium.launch(headless=True)
        context = firefox.new_context()
        context.add_cookies([{"name": "age_check_done", "value":"1", "url":"https://www.dmm.co.jp"}])
        page = context.new_page()
        login(page)
        vrIds = getIds()
        print(f"Found a total of {len(vrIds)} vr videos in the txt file")
        for id in vrIds:
            vrUrls = []
            url = "https://www.dmm.co.jp/monthly/vr/-/detail/=/cid=" + id + "/"
            print(f"\nNow analyzing the following url: {url} --- id={id}")
            page.goto(url, timeout=0)
            sleep(2)
            bitrateSelector = page.locator('css=#download_bitrate')
            bitrateSelector.click()
            sleep(1)
            optionNum = len(bitrateSelector.locator('css=option').all())
            for i in range(optionNum):
                page.keyboard.press("ArrowDown")
                sleep(0.2)
            page.keyboard.press("Enter")
            for qualityList in page.locator('css=#download_panel ul').all():
                if qualityList.is_visible():
                    for a in qualityList.locator('css=a').all():
                        with page.expect_download() as download_info:
                            sleep(5)
                            a.click()
                            sleep(2)
                            download = download_info.value
                            vrUrls.append(download.url)
                            download.cancel()
            print(f"Found a total of {len(vrUrls)} parts")
            writeVrUrls(vrUrls)

if __name__ == "__main__":
    main()
