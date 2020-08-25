import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

##############################################################  ############
##################### variable related selenium ##########################
##########################################################################
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기


def main():
    global driver, load_wb, review_num

    driver.implicitly_wait(4)  # 렌더링 될때까지 기다린다 4초
    driver.get('https://map.kakao.com/')  # 주소 가져오기

    # 카페 정보 읽어오기
    place_infos = ['강남 맛집용]

    for i, place in enumerate(place_infos):
        if i % 4 == 0 and i != 0:
            sleep(5)
        print("#####", i)
        search(place)

    driver.quit()
    print("finish")


def search(place):
    global driver

    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
    search_area.send_keys(place)  # 검색어 입력
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    sleep(1)

    # 검색된 정보가 있는 경우에만 탐색
    # 1번 페이지 cafe list 읽기
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    cafe_lists = soup.select('.placelist > .PlaceItem') # 검색된 카페 목록

    # 검색된 첫 페이지 카페 목록 크롤링하기
    crawling(place, cafe_lists)
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
            cafe_lists = soup.select('.placelist > .PlaceItem')

            crawling(place, cafe_lists)

    except ElementNotInteractableException:
        print('not found')
    finally:
        search_area.clear()


def crawling(place, cafe_lists):
    """
    페이지 목록을 받아서 크롤링 하는 함수
    :param place: 리뷰 정보 찾을 카페이름
    """

    while_flag = False
    for i, cafe in enumerate(cafe_lists):
        # 광고에 따라서 index 조정해야함
        #if i >= 3:
         #   i += 1

        place_name = cafe.select('.head_item > .tit_name > .link_name')[0].text  # place name
        place_address = cafe.select('.info_item > .addr > p')[0].text  # place address

        detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]'
        driver.find_element_by_xpath(detail_page_xpath).send_keys(Keys.ENTER)
        driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환
        sleep(1)

        print('####', place_name)

        # 첫 페이지
        extract_review(place_name)

        # 2-5 페이지
        idx = 3
        try:
            page_num = len(driver.find_elements_by_class_name('link_page'))
            for i in range(page_num-1):
                driver.find_element_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(idx) +')').send_keys(Keys.ENTER)
                sleep(1)
                extract_review(place_name)
                idx += 1
            driver.find_element_by_link_text('다음').send_keys(Keys.ENTER)
            sleep(1)
            extract_review(place_name)
        except (NoSuchElementException, ElementNotInteractableException):
            print("no review in crawling")

        # 그 이후 페이지
        while True:
            idx = 4
            try:
                page_num = len(driver.find_elements_by_class_name('link_page'))
                for i in range(page_num-1):
                    driver.find_element_by_css_selector('#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(idx) +')').send_keys(Keys.ENTER)
                    sleep(1)
                    extract_review(place_name)
                    idx += 1
                driver.find_element_by_link_text('다음').send_keys(Keys.ENTER)
                sleep(1)
                extract_review(place_name)
            except (NoSuchElementException, ElementNotInteractableException):
                print("no review in crawling")
                break

        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환


def extract_review(place_name):
    global driver

    ret = True

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')

    # 리뷰가 있는 경우
    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            comment = review.select('.txt_comment > span') # 리뷰
            rating = review.select('.grade_star > em') # 별점
            val = ''
            if len(comment) != 0:
                if len(rating) != 0:
                    val = comment[0].text + '/' + rating[0].text.replace('점', '')
                else:
                    val = comment[0].text + '/0'
                print(val)

    else:
        print('no review in extract')
        ret = False

    return ret


if __name__ == "__main__":
    main()