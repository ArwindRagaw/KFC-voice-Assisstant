import streamlit as st
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from langchain_community.llms import Ollama

# Initialize the recognizer and TTS engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize orders and discount flag
orders = []
special_offer_applied = False

# Menu with items and potential discounts
hotel_menu = {
    "hot and crispy combo": {"price": 299, "discount": 10},
    "signature bucket": {"price": 599, "discount": 15},
    "special 11 meal": {"price": 435},
    "hitter savings": {"price": 349},
    "classic zinger combo": {"price": 199},
    "sixer savings": {"price": 499},
    "super savings": {"price": 299},
    "veg lovers meal": {"price": 399},
    "leg piece deal": {"price": 399},
    "new chicken longer": {"price": 179},
    "new single chicken rolls": {"price": 149},
    "new rizo rice bowls": {"price": 199},
    "family deal": {"price": 699},
    "classic zinger": {"price": 199},
    "caribbean spicy zinger": {"price": 199},
    "veg zinger lovers": {"price": 199},
    "tandoori zinger deal": {"price": 399},
    "leg, wings, strips combo": {"price": 399},
    "popcorn rice bowlz deal": {"price": 299},
    "smoky red chicken": {"price": 199},
    "chicken popcorn pack": {"price": 99},
    "veg roll meal": {"price": 199},
    "chicken roll combo": {"price": 199},
    "dessert special": {"price": 99},
    "add-ons": {"price": "Varies"}
}

# Text-to-speech function
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Greeting function
def greet():
    talk('Hello! I am Alexa, your virtual assistant. What would you like to order today?')

# Function to capture voice commands
def take_command():
    try:
        with sr.Microphone() as source:
            st.write('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
            st.write(command)
            return command
    except sr.UnknownValueError:
        talk("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        return ""

# Function to add order items
def add_order(order_item):
    global special_offer_applied
    if order_item in hotel_menu:
        if 'discount' in hotel_menu[order_item] and special_offer_applied:
            discounted_price = hotel_menu[order_item]["price"] * (1 - hotel_menu[order_item]["discount"] / 100)
            orders.append({"item": order_item, "price": discounted_price})
            talk(f'Your order for {order_item} is placed at {discounted_price:.2f} rupees. What would you like to order next?')
        else:
            orders.append({"item": order_item, "price": hotel_menu[order_item]["price"]})
            talk(f'Your order for {order_item} is placed at {hotel_menu[order_item]["price"]:.2f} rupees. What would you like to order next?')
    else:
        talk(f'Sorry, {order_item} is not available on the menu.')

# Function to calculate the total order cost
def calculate_total():
    total = sum(item["price"] for item in orders)
    return total

# Initialize the LLM
llm = Ollama(model="llama3:8b")

# Function to apply special offers
def apply_discount():
    global special_offer_applied
    special_offer_applied = True
    talk("Special offer applied. Discounts will now be applied to your orders.")

# Function to announce specials
def announce_specials():
    specials = [
        "Today's special offer: Get 10% off on the Signature Bucket.",
        "Combo of the day: Buy one Classic Zinger Combo and get a free drink."
    ]
    for special in specials:
        talk(special)

# Function to handle LLM responses
def handle_llama_response(query):
    response = llm.invoke(query)
    return response

# Streamlit interface
st.title("Voice Assistant Ordering System")

if st.button('Start Voice Assistant'):
    greet()  # Greet the user

    while True:
        command = take_command()
        if command:
            if 'play' in command:
                song = command.replace('play', '')
                talk('playing ' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%H:%M')
                talk('The exact time is ' + time)
            elif 'who is' in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 1)
                talk(info)
            elif 'how are you' in command:
                talk('I am fine, how are you?')
            elif 'who are you' in command:
                talk('I am Alexa, a virtual assistant technology.')
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'order' in command:
                food_item = command.replace('order', '').strip()
                add_order(food_item)
            elif 'total' in command:
                total = calculate_total()
                talk(f'Your total amount is {total:.2f} rupees.')
                st.write(f'Orders: {orders}')
                st.write(f'Total amount: {total:.2f} rupees.')
            elif 'special offer' in command:
                announce_specials()
            elif 'discount' in command:
                apply_discount()
            elif 'thank you' in command:
                talk('Thank you for being our valued customer. We are grateful for the pleasure of serving you.')
            else:
                response = handle_llama_response(command)
                talk(response)
