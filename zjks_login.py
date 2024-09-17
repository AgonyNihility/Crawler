from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import ddddocr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from timeit import timeit
web = webdriver.Chrome()
mima = "qmw618222"
sfzh = "331181200604203376"
url = 'https://pgzy.zjzs.net:4431/login.htm'
web.get(url)
web.find_element(By.XPATH, '//*[@id="mima"]').send_keys(mima)
web.find_element(By.XPATH, '//*[@id="shenfenzheng"]').send_keys(sfzh)
web.maximize_window()
time.sleep(1)

def verify():
    global Veriftimg
    web.save_screenshot('screen.png')
    img = web.find_element(By.XPATH, '//*[@id="imgVerify"]')
    loc = img.location
    size = img.size
    rangle = (int(loc['x']), int(loc['y']), int(loc['x'] + size['width']),
              int(loc['y'] + size['height']))
    i = Image.open('screen.png')
    frame = i.crop(rangle).convert("RGB")
    frame.save('VerifyCode.png')
    time.sleep(0.1)
    Veriftimg = Image.open('VerifyCode.png').convert("L")
    pixdata = Veriftimg.load()
    w, h = Veriftimg.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < 200:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    Veriftimg.save('Ver.png')
    ocr = ddddocr.DdddOcr()
    with open('Ver.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res

def login():
    while True:
        res= verify()  # 获取新的验证码
        yzm = web.find_element(By.XPATH, '//*[@id="yzm"]')
        yzm.clear()  # 清除输入框内容
        yzm.send_keys(res)
        # Veriftimg.show()
        print("out:", res)
        time.sleep(2)
        web.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
        try:
            WebDriverWait(web, 5).until(EC.alert_is_present())
            alert = web.switch_to.alert
            alert.accept()  # 接受现有警告框，相当于确认
        except:
            break  # 如果没有警告，跳出循环，表示登录成功
        time.sleep(0.5)

def extract():
    login()
    return input("Press Enter to close the browser...")
    web.switch_to.frame("pageurl")
    table_cells = web.find_elements(By.XPATH, '//td[@class="tdright"]')
    for cell in table_cells:
        print(cell.text)

print(timeit(extract(),'from __main__ import extract'))
time.sleep(0.5)
