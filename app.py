from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import tempfile
from scraper import scrape_auction_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return "URL을 입력해주세요.", 400

    try:
        # 스크래핑 함수 직접 호출
        df = scrape_auction_data(url)
        
        if df is None:
            return "데이터를 찾을 수 없습니다. 올바른 URL인지 확인해주세요.", 404

        # 임시 파일 생성 (클라우드 환경 호환)
        # delete=False로 설정하여 파일 전송 후 삭제하도록 처리하거나
        # OS의 임시 디렉토리에 저장합니다.
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, 'result.xlsx')
        df.to_excel(file_path, index=False)
        
        return redirect(url_for('result'))
        
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}", 500

@app.route('/result')
def result():
    return render_template('result.html', filename='result.xlsx')

@app.route('/download/<filename>')
def download(filename):
    # 임시 디렉토리에서 파일 찾기
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name='경매물건목록.xlsx')
    else:
        return "파일을 찾을 수 없습니다. 다시 스크래핑해주세요.", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
