import time,json,csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options

#dataframe
df=pd.read_csv("output_cleaned.csv")

#driver setup
chrome_options = Options()
chrome_options.page_load_strategy = "eager"
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)   # Launch Chrome browser
driver.implicitly_wait(1)   # Waits up to 8s for elements to appear # Opens LinkedIn
driver.maximize_window()
time.sleep(15)

#xpaths
billiBoardX="//div[@class='center']"
definationX="//div[@class='mb-3'][1]/p"
exception_definationX="//div[@class='mb-3']"
featureX="//div[@class='mb-3']//li"
tableX="//table[@class='table mb-3']/tbody/tr"
metaX="//div[@class='media-body']"
hx=".//h4"
pX=".//p"
imgX="//div[@class='product-img']/div[@class='img-inner']//img"
breadCrumpX="//ol[@class='breadcrumb']"
IMGseriesX="//div[@class='row product-thumb icon-images xzoom-thumbs']/button"
PDFseriesX="//div[@class='row product-thumb icon-images xzoom-thumbs']/a"



#main list
itemDetails=[]
Link_Skipped=[]

#count values
count=1
save_interval = 150

#extract data from each link
for iLink in df["Link"]:
    try:
        driver.set_page_load_timeout(20)
        driver.get(iLink)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # genral info extracting
        try:
            billiBoard = driver.find_element(By.XPATH, billiBoardX).text
        except:
            billiBoard = ""
        try:
            try:
                defination = driver.find_element(By.XPATH, definationX).text
            except:
                defination = driver.find_element(By.XPATH, exception_definationX).text
        except:
            defination = ""

        # features extracting
        try:
            features = driver.find_elements(By.XPATH, featureX)
            features_list = []
            for f in features:
                features_list.append(f.text)
        except:
            features_list = []

        try:
            breadCrump=driver.find_element(By.XPATH,"//ol[@class='breadcrumb']").text
        except:
            breadCrump=""

        # meta extracting
        try:
            meta = driver.find_elements(By.XPATH, metaX)
            meta_list = []
            for m in meta:
                h4 = m.find_element(By.XPATH, hx).text
                p = m.find_element(By.XPATH, pX).text
                meta_list.append({
                    "Title": h4,
                    "Meta_Defination": p
                })
        except:
            meta_list = []


        try:
            IMGseries = driver.find_elements(By.XPATH, IMGseriesX)
            IMGseriesList = []
            for i in IMGseries:
                imgSrc = i.find_element(By.TAG_NAME,"img").get_attribute("src")
                IMGseriesList.append(imgSrc)
        except:
            IMGseriesList = []



        try:
            PDFseries = driver.find_elements(By.XPATH, PDFseriesX)
            PDFseriesList = []
            for p in PDFseries:
                pdfSrc = p.get_attribute("href")
                PDFseriesList.append(pdfSrc)
        except:
            PDFseriesList = []

        # table data extracting
        try:
            table = driver.find_elements(By.XPATH, tableX)
            table_info_list = []
            for t in table:
                try:
                    th = t.find_element(By.TAG_NAME, "th").text
                except:
                    th = "title_name"

                try:
                    td = t.find_element(By.TAG_NAME, "td").text
                except:
                    td = ""
                table_info_list.append({
                    th: td
                })
        except:
            table_info_list = []

        # img src extracting
        try:
            img = driver.find_element(By.XPATH, imgX).get_attribute("src")
        except:
            img = ""

        itemDetails.append({
            "Breadcrump_Catagory": breadCrump,
            "billiBoard": billiBoard,
            "defination": defination,
            "features": features_list,
            "meta_list": meta_list,
            "table": table_info_list,
            "image": img,
            "Image_Series": IMGseriesList,
            "PDF_Series": PDFseriesList,
            "Link": iLink
        })
        print({
            "Breadcrump_Catagory": breadCrump,
            "billiBoard": billiBoard,
            "defination": defination,
            "features": features_list,
            "meta_list": meta_list,
            "table": table_info_list,
            "Front_Image": img,
            "Image_Series":IMGseriesList,
            "PDF_Series": PDFseriesList,
            "Link": iLink
        })
        print("\n")
        # parts by parts save
        if len(itemDetails) % save_interval == 0:
            time.sleep(15)
            print(30 * "=>", f" {iLink}")
            with open(f"All_Details_item{count}.json", "w", encoding='utf-8') as f:
                json.dump(itemDetails, f, ensure_ascii=False, indent=4)

    except:
        #Unsuccessful links will be saved here.
        Link_Skipped.append(iLink)
        driver.execute_script("window.stop();")
        time.sleep(10)
        print("skipped")
        continue
    print(f"count: {count}")
    count=count+1



#total save file
with open(f"All_Details_item.json", "w", encoding='utf-8') as f:
    json.dump(itemDetails, f, ensure_ascii=False, indent=4)

#skipped link save file
with open("Link_Skipped.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Skipped_Link"])  # Header
    for link in Link_Skipped:
        writer.writerow([link])