
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys

def scrape_auction_data(url):
    """
    주어진 URL에서 경매 데이터를 스크래핑하여 DataFrame으로 반환합니다.
    """
    # 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 웹페이지 요청
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 요청 실패 시 예외 발생

        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 경매 물건 목록을 포함하는 테이블을 찾습니다.
        auction_table = soup.find('table', class_='tbl_act_list_hank')

        scraped_data = []

        if auction_table:
            items = auction_table.find('tbody').find_all('tr')

            for item in items:
                cells = item.find_all('td')
                if len(cells) < 4:
                    continue

                # sbj 셀에서 정보 추출
                sbj_td = cells[2]
                case_type_status_p = sbj_td.find('p', style=lambda v: v and 'font-size:15px' in v)
                case_type = 'N/A'
                status = 'N/A'
                failure_count = '0'
                if case_type_status_p:
                    case_type_status_text = case_type_status_p.get_text(strip=True)
                    if ']' in case_type_status_text:
                        parts = case_type_status_text.split(']')
                        case_type = parts[0] + ']'
                        status = parts[1].strip()
                        if '유찰' in status:
                            try:
                                count_part = status.split('유찰')[1].strip()
                                failure_count = "".join(filter(str.isdigit, count_part))
                                if not failure_count:
                                    failure_count = '0'
                            except (IndexError, ValueError):
                                failure_count = '0'
                    else:
                        status = case_type_status_text

                info_div = sbj_td.find('div', style=lambda v: v and 'display:flex' in v)
                case_number, address, appraised_price, minimum_price, special_conditions = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'

                if info_div:
                    left_div = info_div.find('div', style=lambda v: v and 'width:70%' in v)
                    if left_div:
                        case_number_span = left_div.find('span', style=lambda v: v and 'font-size:17px' in v)
                        if case_number_span: case_number = case_number_span.get_text(strip=True)
                        
                        address_p = left_div.find('p', style=lambda v: v and 'font-size:14px' in v)
                        if address_p: address = address_p.get_text(strip=True)

                        special_p = left_div.find('p', class_='f_red')
                        if special_p: special_conditions = special_p.get_text(strip=True)

                    right_div = info_div.find('div', style=lambda v: v and 'width:30%' in v)
                    if right_div:
                        prices = right_div.find_all('p')
                        if len(prices) > 0 and prices[0].find('span'): appraised_price = prices[0].find('span').get_text(strip=True)
                        if len(prices) > 1 and prices[1].find('span'): minimum_price = prices[1].find('span').get_text(strip=True)

                # 마지막 셀에서 매각기일 및 조회수 추출
                last_td = cells[3]
                views, auction_date = 'N/A', 'N/A'
                
                view_span = last_td.find('span', style=lambda v: v and 'color:black' in v)
                if view_span: views = view_span.get_text(strip=True)

                date_p = last_td.find_all('p')
                if len(date_p) > 2:
                    auction_date = date_p[2].get_text(strip=True, separator=" ").split(" ")[0]

                scraped_data.append([case_number, address, appraised_price, minimum_price, f"{case_type} {status}".strip(), failure_count, auction_date, views, special_conditions])

        if scraped_data:
            df = pd.DataFrame(scraped_data, columns=['사건번호', '소재지', '감정가', '최저가', '상태', '유찰횟수', '매각기일', '조회수', '특수조건'])
            return df
        else:
            return None

    except (requests.exceptions.RequestException, IndexError) as e:
        print(f"오류가 발생했습니다: {e}")
        raise e

if __name__ == "__main__":
    # URL을 명령줄 인자로부터 받습니다.
    if len(sys.argv) < 2:
        print("사용법: python scraper.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    df = scrape_auction_data(url)
    
    if df is not None:
        df.to_excel('경매물건목록.xlsx', index=False)
        print("스크래핑 완료! '경매물건목록.xlsx' 파일에 저장되었습니다.")
    else:
        print("데이터를 스크래핑하지 못했습니다.")
