from sqlalchemy import (
    MetaData,
    Table,
    insert,
)
from sqlalchemy.exc import IntegrityError
from utils import run_query, get_engine
from flask import Blueprint, request, render_template
import uuid
import jwt
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

home_bp = Blueprint("home", __name__, url_prefix="/home")

keyword1 = ""
page1 = 1
data = []

@home_bp.route("", methods=["GET","POST"])
def search_product():

    global data

    if request.method == "GET":

        if "sort_by" not in request.args:
            sort = "RANDOM()"
        else:
            sort_by = request.args["sort_by"]

            if sort_by == "highest":
                sort = "price DESC"
            elif sort_by == "lowest":
                sort = "price ASC"
            else: 
                sort = "RANDOM()"

        if "sold_by" not in request.args:
            sold = "RANDOM()"
        else:
            sold_by = request.args["sold_by"]

            if sold_by == "highest":
                sold = "sold DESC"
            elif sold_by == "lowest":
                sold = "sold ASC"
            else: 
                sold = "RANDOM()"

        if "sort_by" in request.args and "sold_by" in request.args:

            data = run_query(f"SELECT * FROM product ORDER BY {sort},{sold};")

        elif "sort_by" in request.args and "sold_by" not in request.args:

            data = run_query(f"SELECT * FROM product ORDER BY {sort};")

        elif "sort_by" not in request.args and "sold_by" in request.args:

            data = run_query(f"SELECT * FROM product ORDER BY {sold};")
        else:

            data = run_query(f"SELECT * FROM product ORDER BY RANDOM();")

        message = "Get Product Success"
        
        if data == []:
            message = "Belum ada Data, silahkan isikan Kata Kunci"

        return render_template(
            'index.html',
            data = data, 
            message = message
        )

    
    if request.method == "POST":

        global keyword1  # Declare keyword1 as a global variable
        global page1  # Declare page1 as a global variable

        if "keyword" not in request.args:

            data = []
            
            return {
                    "message": "Silahkan Masukkan Kata Kunci"
                }, 201
            
        else:
        
            keyword = request.args["keyword"]

            if not keyword.strip():
                return {
                    "message": "Silahkan Masukkan Kata Kunci"
                }, 201

            if "page" not in request.args:
                page = 1
            else:
                page = int(request.args["page"])
                

            if keyword == keyword1 and page == page1:
                return {
                        "message": "Search Product success"
                    }, 201

            else:

                run_query("DELETE FROM product;", commit=True)

            # SCRAPING
                opsi = webdriver.ChromeOptions()
                opsi.add_experimental_option('excludeSwitches', ['enable-logging'])
                opsi.add_argument(r"--user-data-dir=C:\Users\Asus\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
                opsi.add_argument(r'--profile-directory=Profile 19') #e.g. Profile 3

                # opsi.add_argument('--headless')
                # opsi.add_argument('--incognito')

                opsi.add_argument("disable-infobars")
                opsi.add_argument("--disable-extensions")
                opsi.add_argument('--no-sandbox')
                opsi.add_argument('--disable-dev-shm-usage')
                opsi.add_argument('--disable-gpu')
                opsi.add_argument('--start-maximized')
                opsi.add_experimental_option("detach", True)

                servis = Service('chromedriver.exe')
                driver = webdriver.Chrome(service=servis, options=opsi)

                url_shopee = f"https://shopee.co.id/search?keyword={keyword}&page={page-1}"
                url_tokped = f"https://www.tokopedia.com/search?q={keyword}&page={page}"
                url_lazada = f"https://www.lazada.co.id/tag/{keyword}/?q={keyword}&page={page}"
                url_bukalapak = f"https://www.bukalapak.com/products?search%5Bkeywords%5D={keyword}&page={page}"


                i = 1

            # SHOPEE

                base_shopee = "https://shopee.co.id"

                driver.get(url_shopee)
                scrolling = 500
                for scroll in range(1, 11):
                    end = scrolling * scroll
                    perintah = "window.scrollTo(0," + str(end) + ")"
                    driver.execute_script(perintah)
                    time.sleep(1)

                content = driver.page_source
                data = BeautifulSoup(content,'html.parser')

                for area in data.find_all('li',class_="col-xs-2-4 shopee-search-item-result__item"):

                    productName = area.find('div',class_="ie3A+n bM+7UW Cve6sh").get_text()
                    if "'" in productName:
                        productName = productName.replace("'","")

                    img_tag = area.find('img', class_='_7DTxhh tWoeMk')
                    if img_tag:
                        productImage = img_tag.get('src')
                    else:
                        productImage = "n"

                    productPrice = area.find('span',class_="ZEgDH9").get_text()
                    if productPrice == "???":
                        price = 0
                    else:
                        split_price = productPrice.split('.')
                        conv_price = ""
                        for p in split_price:
                            conv_price+=p
                        price = int(conv_price)

                    productLink = base_shopee + area.find('a')['href']
                    
                    productSold = area.find('div',class_="r6HknA uEPGHT")
                    if productSold != None:
                        productSold = productSold.get_text()
                        if "+" in productSold:
                            productSold = productSold.replace("+","")
                        if "RB" in productSold:
                            split_sold = productSold.replace("RB Terjual","")
                            sold = int(split_sold.replace(",","")) * 100
                        else:
                            split_sold = productSold.replace(" Terjual","")
                            sold = int(split_sold)
                    else:
                        sold = 0

                    productLocation = area.find('div',class_="zGGwiV").get_text()
                    
                    run_query(f"INSERT INTO product VALUES({i},'SHOPEE','{productImage}','{productName}',{price},{sold},'{productLocation}','{productLink}')", commit=True)
                    # print(productPrice)
                    i+=1

            # # TOKOPEDIA

            #     driver.get(url_tokped)
            #     scrolling = 500
            #     for scroll in range(1, 14):
            #         end = scrolling * scroll
            #         perintah = "window.scrollTo(0," + str(end) + ")"
            #         driver.execute_script(perintah)
            #         time.sleep(1)

            #     content = driver.page_source
            #     data = BeautifulSoup(content,'html.parser')

            #     for id,area in enumerate(data.find_all('div',class_="css-llwpbs")):
            #         # print(i)
            #         if id >= 5 :
            #             productName = area.find('div',class_="prd_link-product-name css-3um8ox").get_text()
            #             if "'" in productName:
            #                 productName = productName.replace("'","")

            #             productImage = area.find('img')['src']

            #             productPrice = area.find('div',class_="prd_link-product-price css-h66vau").get_text()
            #             productPrice = productPrice.replace("Rp","")
            #             split_price = productPrice.split('.')
            #             conv_price = ""
            #             for p in split_price:
            #                 conv_price+=p
            #             price = int(conv_price)

            #             productLink = area.find('a')['href']
                        
            #             productSold = area.find('span',class_="prd_label-integrity css-1duhs3e")
            #             if productSold != None:
            #                 productSold = productSold.get_text()
            #                 if "rb" in productSold:
            #                     # split_sold = productSold.replace(" terjual","")
            #                     sold = int(productSold.replace(" rb+ terjual","")) * 1000

            #                 elif "rb" not in productSold and "+" in productSold:
            #                     # split_sold = productSold.replace(" terjual","")
            #                     sold = int(productSold.replace("+ terjual",""))
                                
            #                 else:
            #                     # split_sold = productSold.replace(" terjual","")
            #                     sold = int(productSold.replace(" terjual",""))
            #             else:
            #                 sold = 0

            #             productLocation = area.find('span',class_="prd_link-shop-loc css-1kdc32b flip").get_text()
                        
            #             run_query(f"INSERT INTO product VALUES({i},'TOKOPEDIA','{productImage}','{productName}',{price},{sold},'{productLocation}','{productLink}')", commit=True)

            #             i+=1

            # #LAZADA

            #     driver.get(url_lazada)
            #     scrolling = 500
            #     for scroll in range(1, 11):
            #         end = scrolling * scroll
            #         perintah = "window.scrollTo(0," + str(end) + ")"
            #         driver.execute_script(perintah)
            #         time.sleep(1)

            #     content = driver.page_source
            #     data = BeautifulSoup(content,'html.parser')

            #     for area in data.find_all('div',class_="Bm3ON"):
            #         # print(i)

            #         title = data.find_all('a')
            #         for t in title:
            #             if t.has_attr('title'):
            #                 productName = t['title']
            #                 if "'" in productName:
            #                     productName = productName.replace("'","")

            #         productImage = area.find('img')['src']

            #         productPrice = area.find('span',class_="ooOxS").get_text()
            #         productPrice = productPrice.replace("Rp","")
            #         split_price = productPrice.split('.')
            #         conv_price = ""
            #         for p in split_price:
            #             conv_price+=p
            #         price = int(conv_price)

            #         productLink = area.find('a')['href']
                    
            #         productSold = area.find('span',class_="_1cEkb")
            #         if productSold != None:
            #             productSold = productSold.get_text()
            #             if "," in productSold:
            #                 split_sold = productSold.replace(" sold","")
                            
            #                 if "+" in split_sold:
            #                     split_sold = split_sold.replace("+","")
                
            #                 sold = int(split_sold.replace(",",""))
            #             else:
            #                 split_sold = productSold.replace(" sold","")
            #                 sold = int(split_sold)
            #         else:
            #             sold = 0

            #         productLocation = area.find('span',class_="oa6ri")
            #         productLocation = productLocation.get_text()
                    
            #         run_query(f"INSERT INTO product VALUES({i},'LAZADA','{productImage}','{productName}',{price},{sold},'{productLocation}','{productLink}')", commit=True)

            #         i+=1

            # #BUKALAPAK

            #     driver.get(url_bukalapak)
            #     scrolling = 500
            #     for scroll in range(1, 9):
            #         end = scrolling * scroll
            #         perintah = "window.scrollTo(0," + str(end) + ")"
            #         driver.execute_script(perintah)
            #         time.sleep(1)

            #     content = driver.page_source
            #     data = BeautifulSoup(content,'html.parser')

            #     for area in data.find_all('div',class_="bl-flex-item mb-8"):
            #         # print(i)

            #         productName = area.find('a',class_="bl-link").get_text()
            #         if "'" in productName:
            #             productName = productName.replace("'","")

            #         productImage = area.find('img')['src']

            #         # div = data.find('div',{"class":"yvbeD6 KUUypF"})
            #         # productImage = div.find('img').attrs['src']

            #         productPrice = area.find('p',class_="bl-text bl-text--semi-bold bl-text--ellipsis__1 bl-product-card-new__price").get_text()
            #         split_price = productPrice.split('.')
            #         conv_price = ""
            #         for p in split_price:
            #             conv_price+=p
            #         price = int(conv_price)

            #         productLink = area.find('a')['href']
                    
            #         productSold = area.find('p',class_="bl-text bl-text--caption-12 bl-text--secondary bl-product-card-new__sold-count")
            #         if productSold != None:
            #             productSold = productSold.get_text()
            #             split_sold = productSold.replace("Terjual ","")
            #             sold = int(split_sold)
            #         else:
            #             sold = 0

            #         productLocation = area.find('p',class_="bl-text bl-text--caption-12 bl-text--secondary bl-text--ellipsis__1 bl-product-card-new__store-location").get_text()

            #         run_query(f"INSERT INTO product VALUES({i},'BUKALAPAK','{productImage}','{productName}',{price},{sold},'{productLocation}','{productLink}')", commit=True)

            #         i+=1

                keyword1 = keyword
                page1 = page

                driver.quit()

            return {
            "message": "Search Product success"
            }, 201

    return {
                "message": "Search Product success"
            }, 201