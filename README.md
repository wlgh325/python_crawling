[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/wlgh325/python_crawling.git)](https://hits.seeyoufarm.com)

<div align=center>

# selenium을 이용한 파이썬 크롤링

</div>

# 사용언어 및 환경
![Python Badge](https://img.shields.io/badge/-Python-9cf?style=flat-square&logo=Python)
Selenium  
Pycharm IDE  
BeautifulSoup

# 참고 사이트
[selenium python exam](https://selenium-python.readthedocs.io/locating-elements.html)

---

# 크롤링 프로젝트
* 모두 chromewebdriver는 따로 설치하셔야 합니다.
기본적인 selenium 사용법은 [이 글](https://hoho325.tistory.com/265)을 참고해주세요!!
1. Selenium을 이용한 카카오맵 리뷰 파이썬 크롤링
```text
카카오맵에서 제공하는 장소들의 리뷰들을 자동으로 크롤링 해주는 코드입니다.  
예를들어 '강남 맛집'으로 검색하게 되면 여러 장소들이 나오게 됩니다.
이 장소들의 '상세보기'탭에 들어가서 리뷰와 별점을 크롤링 할 수 있습니다.

장소들을 찾기 위해서는 xpath를 이용
리뷰 탭을 찾기 위해서는 css selector와 link text를 이용하여 찾아냈습니다.

HTML 코드만 분석이 된다면 이를 얼마든지 응용할 수 있습니다.
```

2. Selenium을 이용한 카카오맵 메뉴 파이썬 크롤링
```text
카카오맵에서 제공하는 장소들의 메뉴들을 자도으로 크롤링 해주는 코드입니다.
예륻들어 '스타벅스 강남R점'의 메뉴들이 궁금해서 검색하다면
검색 후 '상세보기'로 들어가 메뉴 정보를 추출합니다.
메뉴 이름과 가격을 찾아내 수 있습니다.
```
