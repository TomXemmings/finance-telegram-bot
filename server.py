from flask import Flask, request, jsonify, send_from_directory
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from database import get_items

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    # Change to your credentials
    "./credentials.json", scope
)
client = gspread.authorize(creds)
# Change to your excel table name
sheet = client.open("EXCEL_TABLE_NAME").sheet1

# Change to your Telegram API token
SECRET_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    accounts = get_items('accounts')
    projects = get_items('projects')
    articles = get_items('articles')
    return jsonify({
        'accounts': accounts,
        'projects': projects,
        'articles': articles
    })

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/submit', methods=['POST'])
def submit():
    token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if token != SECRET_TOKEN:
        return jsonify({'ok': False, 'error': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'ok': False, 'error': 'No data provided'}), 400

    try:
        sheet.append_row([
            data['date'],
            data['amount'],
            data['account'],
            data['username'],
            data['project'],
            data['article'],
            data['comment'],
            data['transactionType']
        ])
        return jsonify({'ok': True})
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return jsonify({'ok': False, 'error': 'Error saving data'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
