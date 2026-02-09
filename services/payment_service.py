import razorpay
import os
from dotenv import load_dotenv

load_dotenv()   # 🔥 THIS WAS MISSING

print("KEY:", os.getenv("RAZORPAY_KEY_ID"))
print("SECRET:", os.getenv("RAZORPAY_KEY_SECRET"))


client = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

def create_order(amount):
    # amount in paise
    return client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })
