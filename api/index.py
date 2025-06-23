from flask import Flask,json
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
import os
import dotenv
app = Flask(__name__)
dotenv.load_dotenv()
PUSHBULLET_TOKEN = os.getenv("PUSHBULLET_TOKEN")

# Mess Menu Structured from your menu.json
menu = {
    "monday": {
        "breakfast": "Puri, Aloo Rassawala Sabji, Pickle, Masala Boiled Egg, Steam Sprouts, Brown Bread +Butter+Jam, Milk+Mint chai+Coffee, Cornflakes, Chocolate Powder, Watermelon",
        "lunch": "Beetroot Cucumcer Salad, Dal Palak, Moong Masala, Lauki Chana, Plain Rice, Plain Curd, Chapati, Mirchi + Lemon + Pickle, Fryums",
        "snacks": "Veg Makhani Burger, Ketchup, Cold Coffee, Adrak-Elaichi Chai",
        "dinner": "Onion Cucumber Salad, Dal Tadka, Achari Paneer, Steam Rice, Chapati, Lemon+ chutney, Kaju Draskh Ice Cream, Fish Curry"
    },
    "tuesday": {
        "breakfast": "Aloo Pyaaz Paratha, Curd, Pickle, Egg Bhurjee, Brown Bread Butter + Jam, Milk + Elaichi chai+ Coffee, Chocos, Chocolate Powder, Papaya",
        "lunch": "Tomato Onion Salad, Dal Tadka, Punjabi kadi Pakoda, Gilki Masala, Jeera Rice, Masala Buttermilk, Chapati, Mirchi + Lemon + Pickle, Ramakada",
        "snacks": "Chinese Bhel/ Bombay Bhel, Ketchup / Imli Chutney + Green Chutney, Mint Lemon Water, Adrak-Elaichi Chai \n  + Coffee +Milk",
        "dinner": "Beetroot Cucumber Salad / Onion Tomato Salad, Sambar+Coconut Chutney/Rajasthani Dal, Medu Vada/Fried Curd, Lemon Rice/Jeera Rice, Masala Dosa / Fried Bati, Lemon + Pickle / Lehsoon chutney+Lemon + Pickle + green chilli +Ghee, Gulab Jamun/Churma, Chicken Noodles"
    },
    "wednesday": {
        "breakfast": "Vermicelli, Green Chutney, Omelette, Boiled Chana, White Bread +Butter+Jam, Milk + Elaichi Chai+ Coffee, Cornflakes, Bournvita, Banana",
        "lunch": "Mix Salad, Dal Fry, White Chauli Masala, Kadai Paneer, Jeera Rice, Mint Buttermilk, Chapati, Mirchi + Lemon + Pickle, Rice Papad",
        "snacks": "Dahi Papdi Chaat/ Dahi Vada, Imli Chutney + Green Chutney+ Sev + Chopped Onion, Lemonade, Adrak-Elaichi Chai \n  + Coffee +Milk",
        "dinner": "Kachumbar Salad, Dal Fry, Ravaiya Masala, Steam Rice, Chapati, Lemon+Fried Mirchi + Pickle, Dry Fruit Rice Kheer, Butter Chicken"
    },
    "thursday": {
        "breakfast": "Palak Paratha, Curd, Pickle, Egg Bhurji, White Bread Butter + Jam, Milk+Masala Chai+Coffee, Chocos, Boost, Mango",
        "lunch": "Green Salad, Panchratna Dal, Mix Kathod, Bhindi do Pyaza, Jeera Rice, Plain Curd, Chapati, Mirchi + Lemon + Pickle, Roasted Papad",
        "snacks": "Tadka Maggie, Ketchup, Lemon Ice Tea, Adrak-Elaichi Chai+ Coffee +Milk",
        "dinner": "Sambhara Salad, Rajasthani Kadhi, Aloo Tamatar Rassavala, Masala Khichadi, Poori, Lemon + Pickle, Aamras, Chicken Biryani"
    },
    "friday": {
        "breakfast": "Idli, Sambhar, Coconut Peanut Chutney, Masala Boiled Egg, White Bread Butter + Jam, Milk+Masala Chai+Coffee, Cornflakes, Bournvita, Watermelon",
        "lunch": "Mix Salad, Moong Dal Tadka, Rajma Masala, Pumpkin Masala, Jeera Rice, Cucumber Raita, Chapati, Mirchi + Lemon + Pickle, Ramakada",
        "snacks": "Samosa Chaat, Imli Chutney + Green Chutney + Sev + Onion, Lemonade, Adrak-Elaichi Chai \n  + Coffee +Milk",
        "dinner": "Mix Salad, Dal Tadka, Paneer Butter Masala/Egg Curry, Jeera Rice, Chapati, Lemon + Pickle, Vanilla IceCream"
    },
    "saturday": {
        "breakfast": "Tari Poha, Onion, Lemon, Omlette, Moong Sprouts, White Bread Butter + Jam, Milk+Masala Chai+Coffee, Chocos, Boost, Papaya",
        "lunch": "Onion Salad, Urad Dal, Delhi style Chhole, Jeera Pyaaz Aloo, Plain Rice, Rose Lassi, Bhature, Lemon + Pickle + Mint Chutney, Rice Papad",
        "snacks": "Coleslaw Sandwich, Ketchup, Aam Panna, Adrak-Elaichi Chai \n  + Coffee +Milk",
        "dinner": "Beetroot Cucumber Salad, Dal Makhani, Lauki Kofta, Jeera Rice, Chapati, Lemon + pickle, Fruit Custard, Chicken Tikka Masala"
    },
    "sunday": {
        "breakfast": "Onion Dosa/Mysore Masala Dosa, Sambhar, Coconut Peanut Chutney, Boiled Egg, Brown Bread +Butter+Jam, Milk+Adrak-Elaichi Chai+Coffee, Cornflakes, Bournvita, Banana",
        "lunch": "Onion Tomato Salad, Dal Fry, Kala Chana Masala, Bhatta Masala, Plain Rice, Boondi Raita, Chapati, Mirchi + Lemon + Pickle, Ramakada",
        "snacks": "Pani Puri, Aloo Chana Masala+ Chat Masala + Sev + Onion, Lemonade, Adrak-Elaichi Chai \n  + Coffee +Milk",
        "dinner": "Cucumber Onion Salad, Veg. Raita, Mix Veg Dry, Veg Biryani, Chapati, Lemon + Pickle, Coconut Laddoo, Chicken Biryani"
    }
}


def send_push(title, body):
    res = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={
            "Access-Token": PUSHBULLET_TOKEN,
            "Content-Type": "application/json"
        },
        json={
            "type": "note",
            "title": title,
            "body": body
        }
    )
    print(f"[{title}] Sent: {res.status_code}")

def format_meal(day, meal):
    if day not in menu or meal not in menu[day]:
        return f"No menu available for {meal} on {day}"
    meal_items = menu[day][meal]
   
    return meal_items

def notify_meal(meal):
    today = datetime.datetime.now().strftime("%A")
    title = f"🍽️ {meal} Reminder - {today}"
    body = format_meal(today.lower(), meal.lower())
    send_push(title, body)

# Scheduler for 4 daily meal notifications
scheduler = BackgroundScheduler()

# ⏰ Customize these times as per your actual mess schedule:
scheduler.add_job(lambda: notify_meal("Breakfast"), 'cron', day_of_week='mon-fri', hour=7, minute=15)
scheduler.add_job(lambda: notify_meal("Breakfast"), 'cron', day_of_week='sat,sun', hour=7, minute=45)
scheduler.add_job(lambda: notify_meal("Lunch"),     'cron', day_of_week='mon-sun', hour=12, minute=10)
scheduler.add_job(lambda: notify_meal("Snacks"),    'cron', day_of_week='mon-sun', hour=16, minute=00)
scheduler.add_job(lambda: notify_meal("Dinner"),    'cron', day_of_week='mon-sun', hour=19, minute=41)

scheduler.start()

@app.route('/')
def home():
    return "Server is running"
if __name__ == '__main__':
    app.run()
