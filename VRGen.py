from playwright.sync_api import sync_playwright
from time import sleep
import os

javIdListFile = ".\\ids.txt"
email = "EMAIL"
password = "PASSWORD"
urlConfirmAccount = "https://www.dmm.co.jp/monthly/vr/-/detail/=/cid=1nhvr00036/"
outTxtFile = ".\\vrUrls.txt"

if not os.path.exists(outTxtFile):
    with open(outTxtFile, "w") as f:
        print("CREATED OUTFILE")

def getIds():
    with open(javIdListFile, "r", encoding="utf8") as f:
        return [line.rstrip("\n") for line in f.readlines()]

def login(page):
    print("LOGGING IN DMM")
    page.goto("https://www.dmm.co.jp/")
    page.locator('xpath=//*[@id="dm-content"]/main/div/div/div[2]/a').click()
    print("PASSED +18 CHECK")
    page.goto("https://accounts.dmm.co.jp/service/login/password")
    page.locator('xpath=//*[@id="login_id"]').click()
    page.keyboard.type(email, delay=70)
    print("EMAIL INSERTED")
    sleep(3)
    page.locator('xpath=//*[@id="password"]').click()
    page.keyboard.type(password, delay=80)
    print("PASSWORD INSERTED")
    sleep(3)
    page.locator('xpath=//*[@id="__next"]/div[2]/div[1]/div/div/div[1]/div/dl[1]/dd/div/form/div[1]/label').click()
    sleep(0.3)
    page.locator('xpath=//*[@id="__next"]/div[2]/div[1]/div/div/div[1]/div/dl[1]/dd/div/form/div[2]/label').click()
    sleep(0.3)
    page.locator('xpath=//*[@id="loginbutton_script_on"]/label').click()
    sleep(0.3)
    print("CHECKBOX CHECKED")
    page.locator('xpath=//*[@id="loginbutton_script_on"]/span/input').click()
    print("DONE LOGGING IN")
    sleep(3)
    page.goto(urlConfirmAccount)
    page.locator('xpath=//*[@id="main-digital"]/div/div/div/div/dl/dd/form/div[2]/span/input').click()
    print("ACCOUNT CONFIRMED")
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
        page = firefox.new_page()
        login(page)
        vrIds = getIds()
        print(f"Found a total of {len(vrIds)} vr videos in the txt file")
        for id in vrIds:
            vrUrls = []
            url = "https://www.dmm.co.jp/monthly/vr/-/detail/=/cid=" + id + "/"
            print(f"\nNow analyzing the following url: {url} --- id={id}")
            page.goto(url, timeout=0)
            sleep(2)
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
