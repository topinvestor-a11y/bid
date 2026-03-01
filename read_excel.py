
import pandas as pd

try:
    # 엑셀 파일을 읽어옵니다.
    df = pd.read_excel('경매물건목록.xlsx')
    
    # 데이터프레임의 처음 5개 행을 출력합니다.
    print("--- 처음 5개 행 ---")
    print(df.head())
    
    # 데이터프레임의 모든 열 이름을 출력합니다.
    print("\n--- 전체 열 목록 ---")
    print(df.columns.tolist())

except FileNotFoundError:
    print("'경매물건목록.xlsx' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
