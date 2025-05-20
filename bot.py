import schedule
import time
import requests
from kavenegar import KavenegarAPI, APIException, HTTPException

KAVEH_NEGAR_API_KEY = "312F4A38594F4C3253746971536A3773523947624737396659744F784A57734F557A61734F61614A3131343D"
NAVASAN_API_KEY = "freeYom3qIsfNfwbfZp9KO76ZSC8sRlM"

def send_daily_sms():
    gold_price = get_gold_price(NAVASAN_API_KEY)
    try:
        api = KavenegarAPI(KAVEH_NEGAR_API_KEY)
        params = {
            'sender': '2000660110',
            'receptor': '09906611834',
            'message': gold_price,  # SMS still in Persian
        }
        response = api.sms_send(params)
        print("SMS sent successfully.")
    except APIException as e:
        print(f"Kavenegar API Exception: {e}")
    except HTTPException as e:
        print(f"HTTP Exception: {e}")

def get_gold_price(api_key):
    try:
        url = f"http://api.navasan.tech/latest/?api_key={api_key}&item=18ayar"
        response = requests.get(url)
        data = response.json()
        gold = data.get("18ayar", {})
        raw_value = gold.get("value", "N/A")

        try:
            gold_value = f"{int(raw_value):,}"
        except (ValueError, TypeError):
            gold_value = "نامشخص"

        gold_text = f"قیمت گرم طلای ۱۸ عیار:\n💵 {gold_value} تومان"
        return gold_text
    except Exception as e:
        print(f"Error fetching gold price: {e}")
        return "خطا در دریافت قیمت طلا"

# Schedule to run daily at 10:00 AM
# schedule.every().day.at("10:00").do(send_daily_sms)
# For testing purposes (send every 10 seconds):
schedule.every(10).seconds.do(send_daily_sms)

print("Script is running... Waiting for scheduled tasks.")

while True:
    schedule.run_pending()
    #time.sleep(60)
