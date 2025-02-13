import os
import logging
import gspread
from flask import Flask, render_template, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, logging
import pyautogui
# Initialize Flask app
app = Flask(__name__, template_folder='templates')



# Setup logging
logging.basicConfig(filename='bot_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Google Sheets API setup
SHEET_NAME = "Bola 8 - Presupuestos para pedidos"
SHEET_RANGE = "A4:D20"  # Adjust based on column range

# Load credentials from service account JSON file
CREDENTIALS_FILE = "bola8chatbot-e185ecd963e0.json"
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
WHATSAPP_TOKEN = "EAAY1VhEDd4kBOyapwaYOPC9p4t3pv7p1NNBtKRflYojaf9xsfKUqYpiuKB2xpHMKBvi9nCDgLgER9cNJZB0Ha0QMrhJVUaSexQ7yLtbZCZCExuu45pHXyoqN070d7ZA9oqMH2wspHc1SEnmayzbkiBsZAvZChcWtyjABqV7AfpzFKIhXBC9GHvZCZAbZAaKJPXlxnCmST89uQ1og8XJZCh2Ux3IpRACwZDZD"
WHATSAPP_PHONE_ID = "608691765652135"
WHATSAPP_GROUP_ID = "J5HQisIeq4uEcNnyQ1WGHC"
WHATSAPP_RECIPIENTS = ["+5216671040985", "+523328400296", "+5213324940009"]  # Add multiple phone numbers



def send_whatsapp_message(message):
    logging.basicConfig(level=logging.INFO)
    
    for recipient in WHATSAPP_RECIPIENTS:
        try:
            # Open WhatsApp Desktop
            pyautogui.hotkey('win', 's')  # Open Windows Search
            time.sleep(1)
            pyautogui.write('WhatsApp')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)  # Wait for WhatsApp to open
            
            # Search for contact
            pyautogui.hotkey('ctrl', 'f')  # Open search
            time.sleep(1)
            pyautogui.write(recipient)
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(2)
            
            # Type and send message
            pyautogui.write(message)
            time.sleep(1)
            pyautogui.press('enter')
            
            logging.info(f"Message sent successfully to {recipient}")
            print(f"Message sent successfully to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send message to {recipient}: {str(e)}")
            print(f"Failed to send message to {recipient}: {str(e)}")
        
        time.sleep(3)  # Wait before sending the next message



def fetch_orders():
    try:
        sheet = client.open(SHEET_NAME).sheet1
        data = sheet.get(SHEET_RANGE)
        orders = [f"{row[0]}: {row[1]}" for row in data if len(row) >= 2]
        return orders
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return []

@app.route('/')
def index():
    orders = fetch_orders()
    return render_template('index.html', orders=orders)

@app.route('/fetch', methods=['GET'])
def fetch():
    orders = fetch_orders()
    return jsonify(orders)

@app.route('/send', methods=['POST'])
def send():
    orders = fetch_orders()
    if orders:
        message = "\n".join(orders)
        response = send_whatsapp_message(message)
        return jsonify(response)
    return jsonify({"error": "No orders to send"})

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    with open('templates/index.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Order Automation</title>
            <script>
                function sendOrder() {
                    fetch('/send', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => alert('Message sent successfully!'))
                    .catch(error => alert('Error sending message'));
                }
            </script>
        </head>
        <body>
            <h1>Orders</h1>
            <ul>
                {% for order in orders %}
                    <li>{{ order }}</li>
                {% endfor %}
            </ul>
            <button onclick="sendOrder()">Send to WhatsApp</button>
        </body>
        </html>
        """)
    app.run(debug=True)

