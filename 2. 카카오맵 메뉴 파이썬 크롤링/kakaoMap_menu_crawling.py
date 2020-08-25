import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup

# termianl UTF-8 encoding : chcp 65001

##########################################################################
##################### variable related selenium ##########################
##########################################################################
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기


def main():
    global driver, menu_wb

    driver.implicitly_wait(4)  # 렌더링 될때까지 기다린다 4초
    driver.get('https://map.kakao.com/')  # 주소 가져오기

    search("강남 맛집")

    driver.quit()
    print("finish")


def search(place):
    global driver

    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
    search_area.send_keys(place)  # 검색어 입력
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    sleep(1)

    # 검색된 정보가 있는 경우에만 탐색
    # 1번 페이지 place list 읽기
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    place_lists = soup.select('.placelist > .PlaceItem') # 검색된 장소 목록

    # 검색된 첫 페이지 장소 목록 크롤링하기
    crawling(place_lists)
    search_area.clear()

    # 우선 더보기 클릭해서 2페이지
    try:
        driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
        sleep(1)

        # 2~ 5페이지 읽기
        for i in range(2, 6):
            # 페이지 넘기기
            xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
            driver.find_element_by_xpath(xPath).send_keys(Keys.ENTER)
            sleep(1)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            place_lists = soup.select('.placelist > .PlaceItem') # 장소 목록 list

            crawling(place_lists)

    except ElementNotInteractableException:
        print('not found')
    finally:
        search_area.clear()

def crawling(placeLists):
    for i, place in enumerate(placeLists):
        menuInfos = getMenuInfo(i, driver)
        print(menuInfos)

def getMenuInfo(i, driver):
    # 상세페이지로 가서 메뉴찾기
    detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]'
    driver.find_element_by_xpath(detail_page_xpath).send_keys(Keys.ENTER)
    driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환
    sleep(1)

    menuInfos = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 메뉴의 3가지 타입
    menuonlyType = soup.select('.cont_menu > .list_menu > .menuonly_type')
    nophotoType = soup.select('.cont_menu > .list_menu > .nophoto_type')
    photoType = soup.select('.cont_menu > .list_menu > .photo_type')

    if len(menuonlyType) != 0:
        for menu in menuonlyType:
            menuInfos.append(_getMenuInfo(menu))
    elif len(nophotoType) != 0:
        for menu in nophotoType:
            menuInfos.append(_getMenuInfo(menu))
    else:
        for menu in photoType:
            menuInfos.append(_getMenuInfo(menu))

    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환

    return menuInfos

def _getMenuInfo(menu):
    menuName = menu.select('.info_menu > .loss_word')[0].text
    menuPrices = menu.select('.info_menu > .price_menu')
    menuPrice = ''

    if len(menuPrices) != 0:
        menuPrice =  menuPrices[0].text.split(' ')[1]

    return [menuName, menuPrice]

if __name__ == "__main__":
    main()