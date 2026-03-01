
from flask import Flask, render_template, request, send_file, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return "URL을 입력해주세요.", 400

    # scraper.py를 서브프로세스로 실행
    try:
        subprocess.run(["python", "scraper.py", url], check=True)
        return redirect(url_for('result'))
    except subprocess.CalledProcessError as e:
        return f"스크래핑 중 오류가 발생했습니다: {e}", 500
    except FileNotFoundError:
        return "scraper.py를 찾을 수 없습니다.", 500

@app.route('/result')
def result():
    return render_template('result.html', filename='경매물건목록.xlsx')

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "파일을 찾을 수 없습니다.", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
