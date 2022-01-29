from re import T
import requests
from bs4 import BeautifulSoup
import uuid
import json


def get_product_info(category_item, category_id):

    product_list = []

    # 카테고리 페이지 불러오기
    f = open('C://Users//안운빈//Desktop//nunc_data//nunc_category1.json','a',encoding='utf-8')
    for item in category_item:
        product = {}
        product['id'] = str(uuid.uuid4())
        product['name'] = item.select_one("a.link.goodsDetail").get("data-goodsnm")
        product['price'] = item.select_one("a.link.goodsDetail").get("data-price")
        product['brand'] = item.select_one("a.link.goodsDetail").get("data-brndnm")
        product['image_url'] = category_item[0].select_one("a.link.goodsDetail").get("data-imageurl")
        product['category'] = 1 # 스킨/로션만 1, 카테고리마다 바꿔줘야됨
        product['site'] = 5 # 눙크 5
        product['site_id'] = item.select_one("a.link.goodsDetail").get("data-goodsid")
        site_id = item.select_one("a.link.goodsDetail").get("data-goodsid")

        #link = https://www.mynunc.com/product/goods/view-goods?goodsId={상품번호}&dspCateId=
        link = "https://www.mynunc.com/product/goods/view-goods?goodsId="+site_id+"&dspCateId="
        product['link'] = "https://www.mynunc.com/product/goods/view-goods?goodsId="+site_id+"&dspCateId="

        # 여기부터 상품 상세정보
        item_info = BeautifulSoup(requests.get(link).content, "html.parser", from_encoding="utf-8")
        target = item_info.find("table", {'class':'data-table medium'}).find_all("td")

        product['site_category'] = category_id
        product['volume'] = target[0].getText().rstrip("ml")
        product['expiration_date'] = target[2].getText().replace("\r\n",'')
        product['usage'] = target[3].getText().replace("\r\n",' ')
        product['origin'] = target[5].getText().replace("\r\n",' ')
        product['ingredients'] = target[6].getText().replace("\r\n",' ')
        product['caution'] = target[8].getText().replace("\r\n",' ')

        #json_product = json.dumps(product)

        json.dump(product, f, indent='\n',ensure_ascii=False)

        #with open('C://Users//안운빈//Desktop//nunc_data//nunc_category1.json','r') as f:
            #data = json.load(f)

        product_list.append(product)
        
    f.close()

    print(product_list)
    print(len(product_list))

    
#category_info = requests.get("https://www.mynunc.com/product/goods/main?disCateId=20000126")
# 카테고리 번호 입력
site_category = input()

page_num = 1

while(True):
    category_info = BeautifulSoup(requests.get("https://www.mynunc.com/product/goods/main?disCateId="
    +site_category+"&pageNum=&brandRadio=brndCnt&wordDetailSearch=&page="+str(page_num)).content, "html.parser", from_encoding="utf-8")
    category_item = category_info.select("ul.product-list.row li.item")

    if not category_item:
        print("empty list")
        break

    get_product_info(category_item, site_category)

    page_num+=1
