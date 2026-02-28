import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_auction_data(url):
    try:
        # 헤더 설정으로 봇 차단 우회
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 실제 사이트 구조에 맞게 CSS 선택자 조정
        auction_items = []
        
        # 테이블 행들을 찾아서 데이터 추출
        for row in soup.select('table.list_table tr'):
            cells = row.select('td')
            if len(cells) >= 10:  # 사이트 구조에 맞춰 최소 컬럼 수 조정
                item_data = {
                    '물건번호': cells[1].get_text(strip=True),
                    '소재지': cells[2].get_text(strip=True),
                    '감정가': cells[5].get_text(strip=True),
                    '최저가': cells[6].get_text(strip=True),
                    '매각기일': cells[9].get_text(strip=True)
                }
                auction_items.append(item_data)
        
        # 엑셀 파일로 저장
        df = pd.DataFrame(auction_items)
        df.to_excel('경매물건목록.xlsx', index=False, encoding='utf-8-sig')
        
        return df
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

# 사용 예시
url = "https://www.befauction.com/auction/list.html?page=1&listnum=100&orderby=&special=&court1=&damdang1=&syear=&sno=&gamMin=0&gamMax=0&eng=12%2C15&uchal_min=&uchal_max=&sday_s=&sday_e=&lowMin=0&lowMax=0&sido1=&gugun1=&dong1=&bunji=&sagunname=&yongdo=&barea_min=&barea_max=&larea_min=&larea_max=&use2%5B%5D=13&special=&addr="
result = scrape_auction_data(url)
if result is not None:
    print("데이터 스크래핑 및 엑셀 파일 저장 완료!")
