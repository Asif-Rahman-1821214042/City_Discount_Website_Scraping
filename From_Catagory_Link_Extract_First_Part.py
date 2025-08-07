# Selenium setup
import time,json
from selenium import webdriver
from selenium.webdriver.common.by import By


# Launch Chrome browser
driver = webdriver.Chrome()

# Waits up to 8s for elements to appear
driver.implicitly_wait(3)

#Go to That specific link
driver.get("https://www.acitydiscount.com/restaurant_equipment/index.cfm?_faction=1&treenode=57106")  # Opens LinkedIn
driver.maximize_window()
time.sleep(15)


#XPaths
divsX="//div[@class='product-card']"
titleX=".//div[@class='item-title']"
itemBrandX=".//span[@class='item-brand']"
itemModelX=".//span[@class='item-model']"
priceX=".//div[@class='product-extra']"
nextBtnX="//a[@aria-label='Next']"

itemDetails=[]

#collecting all product card

count=1
while True:
    try:
        # time.sleep(2)
        divs = driver.find_elements(By.XPATH, divsX)
        for div in divs:
            #link
            try:
                link = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link=""

            #title
            try:
                title = div.find_element(By.XPATH, titleX).text
            except:
                title = ""

            # Item
            try:
                itemBrand = div.find_element(By.XPATH, itemBrandX).text
            except:
                itemBrand = ""

            # Item
            try:
                itemModel = div.find_element(By.XPATH, itemModelX).text
            except:
                itemModel = ""

            #price
            try:
                price = div.find_element(By.XPATH, priceX).text
            except:
                price = "N/a"

            print("Title: ", title)
            print("item Brand: ", itemBrand)
            print("item Model: ", itemModel)
            print("price: ", price)

            itemDetails.append({
                "Link": link,
                "Title": title,
                "item Brand": itemBrand,
                "item Model": itemModel,
                "price": price
            })
            print("\n")
        nextPage=driver.find_element(By.XPATH, nextBtnX)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        nextPage.click()
        print(30*"=","Page: ",count)
        count=count+1
    except:
        print("\nProblem")
        break

with open("item_data.json", "w", encoding="utf-8") as f:
    json.dump(itemDetails, f, ensure_ascii=False, indent=4)