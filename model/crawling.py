# 필요한 패키지 설치
from datetime import datetime 
import time
import subprocess
import sys
import os

import urllib.request
from urllib.request import urlretrieve
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



def install_packages():
    """
    설치해야 할 패키지 목록을 정의하고, 각각 설치를 시도
    """
    packages = [
        "selenium",
        "chromedriver-autoinstaller",
        "webdriver-manager"
    ]

    apt_packages = [
        "chromium-chromedriver"
    ]

    # pip 패키지 설치
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"Error installing {package}: {e}")

    # apt 패키지 설치 (Ubuntu)
    try:
        print("Running apt-get update...")
        subprocess.check_call(["apt-get", "update"])
        for apt_package in apt_packages:
            print(f"Installing {apt_package}...")
            subprocess.check_call(["apt-get", "install", "-y", apt_package])
    except Exception as e:
        print(f"Error installing apt packages: {e}")






def setup_Chromedriver():



    try:
        # Install ChromeDriver matching the installed Google Chrome version
        chromedriver_path = chromedriver_autoinstaller.install()
        print(f"ChromeDriver installed at: {chromedriver_path}")

        # Configure WebDriver options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Headless mode for no GUI
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('lang=ko_KR')  # 한국어 설정


        # Start ChromeDriver with Selenium
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    # ChromeDriver 설정
        return driver


    except Exception as e:
        print(f"An error occurred: {e}")

# section의 숫자가 나타내는 의미
# 100:정치
# 101: 경제
# 102: 사회
# 103: 생활/문화
# 104: 세계
# 105: IT/과학

def crawl_based_section():
    #from datetime import datetime

    # 현재 날짜 가져오기
    date = datetime.now().date()
    date = date.strftime("%Y%m%d")

    driver = setup_Chromedriver()
    #크롤링할 base url
    base_url = "https://news.naver.com/section/"

    #news_list의 속성 = (날짜, 섹션, url, 기사 제목, 기사 내용, 이미지, 감정)
    news_list = []

    # 섹션 리스트 (예: 정치, 경제, 사회 등)
    #sections = ["100", "101", "102","103","104","105"]

    sections = [ "100" ]

    # 각 섹션에서 뉴스 크롤링
    for section in sections:

        section_url = f"{base_url}{section}"  # 섹션 URL 생성
        driver.get(section_url)
        time.sleep(2)  # 페이지 로드 대기

        # 기사 제목과 URL 크롤링
        articles = driver.find_elements(By.XPATH, '//a[contains(@class, "sa_text_title")]')
        for article in articles:
            url = article.get_attribute('href')  # href 속성 (기사 URL)
            title_element = article.find_element(By.XPATH, './strong')  # strong 태그 안의 제목
            title = title_element.text.strip()  # 제목 텍스트


            if section == "100":
                section_name = "정치"
            elif section == "101":
                section_name = "경제"
            elif section == "102":
                section_name = "사회"
            elif section == "103":
                section_name = "생활/문화"
            elif section == "104":
                section_name = "세계"
            elif section == "105":
                section_name = "IT/과학"
            else: section_name = "none"

            # 뉴스 데이터 저장
            news_list.append({
                "date": date,
                "section": section_name,
                "url": url,
                "title": title
            })

            print(f"[{section}] {title}: {url}")  # 크롤링 결과 출력


    # WebDriver 종료
    driver.quit()
    return news_list



def crawl_based_url(news_list):

#   !pkill -f chromedriver

  driver = setup_Chromedriver()
  
  news_content_list=[]
  url_list = [news['url'] for news in news_list]




  for url in url_list:
      driver.get(url)
      time.sleep(2)  # 페이지 로드 대기


  # 기사 내용 추출
      try:
        article_element = driver.find_element(By.ID, "dic_area")  # ID가 dic_area인 부분
        paragraphs = article_element.text.split("\n")  # '\n' 또는 <br>로 구분된 텍스트 처리
        cleaned_paragraphs = [p.strip() for p in paragraphs if p.strip()]  # 공백 제거
        news_content = " ".join(cleaned_paragraphs)  # 한 줄로 합치기

        if not news_content.strip():
          print("기사 내용 추출 실패")
        else:
          print("내용 추출 성공")
          news_list.append({"content": news_content})
          news_content_list.append(news_content)


      except Exception as e:
        print(f"기사 내용을 찾지 못했습니다: {e}")

  #기사 이미지 추출
      try:

        img_tag = driver.find_element(By.ID, "img1")
        news_img = img_tag.get_attribute('src')

        if news_img is None:
          print("이미지 추출 실패")
        else:
          print("이미지 추출 성공")
          news_list.append({"img": news_img})

      except Exception as e:
        print(f"이미지를 추출하지 못했습닌다. : {e}")

#기사 리뷰 추출
      try:

        labels = driver.find_elements(By.CLASS_NAME, "u_likeit_list_name")
        counts = driver.find_elements(By.CLASS_NAME, "u_likeit_list_count")

        if not labels or not counts:
          print("리뷰 추출 실패")
        else:
          print("리뷰 추출 성공")

          results = {}

          for label, count in zip(labels, counts):
            label_text = label.text.strip()
            count_text = count.text.strip()

            results[label_text] = count_text

          news_list.append({"review": results})

      except Exception as e:
        print("기사 내용을 찾을 수 없습니다:", e)


# WebDriver 종료
  driver.quit()
  return news_content_list



def fullCrawl():


    content=[]

    news_list = crawl_based_section()
    content = crawl_based_url(news_list)

    print("content:", news_list)

    return content[0]

if __name__=="__main__":
  install_packages()
  content=fullCrawl()  

