import time,json,csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options

#driver setup
chrome_options = Options()
chrome_options.page_load_strategy = "eager"
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)   # Launch Chrome browser
driver.implicitly_wait(1)   # Waits up to 8s for elements to appear # Opens LinkedIn
driver.maximize_window()
time.sleep(3)

resource=[]
link=[]
link.append("https://www.acitydiscount.com/Commercial-Kitchen-Equipment.1.25367.2.1.htm")

for s in link:
    driver.get(s)
    imgs = driver.find_elements(By.XPATH, "//div[@class='categories-img']/img")
    titles = driver.find_elements(By.XPATH, "//div[@class='pt-2']")
    anchors = driver.find_elements(By.XPATH,
                                   '//div[@class="col-xl-2dot4 col-lg-2dot4 col-md-2dot4 col-6 my-2 text-center"]/a')
    for img, title, a in zip(imgs, titles, anchors):
        resource.append({
            "img": img.get_attribute("src"),
            "title": title.text,
            "a": a.get_attribute("href")
        })
        link.append(a.get_attribute("href"))
    time.sleep(4)

print(resource)

#skipped link save file
with open("All_Catagory_Main.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["img","title","a"])  # Header
    for link in resource:
        writer.writerow([link["img"],link["title"],link["a"]])