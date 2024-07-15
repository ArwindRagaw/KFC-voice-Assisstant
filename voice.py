import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

orders = []
special_offer_applied = False

hotel_menu = {
    "hot and crispy combo": {"price": 299, "discount": 10},  # Example discount of 10%
    "signature bucket": {"price": 599, "discount": 15},    # Example discount of 15%
    "special 11 meal": {"price": 435},
    "hitter savings": {"price": 349},
    "classic zinger combo": {"price": 199},
    "sixer savings": {"price": 499},
    "super savings": {"price": 299},
    "veg lovers meal": {"price": 399},
    "leg piece deal": {"price": 399},
    "new chicken longer": {"price": 179},
    "new single chicken rolls": {"price": 149},
    "new rizo rice bowlz": {"price": 199},
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

def talk(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    talk('Hello! I am Alexa, your virtual assistant. What would you like to order today?')

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
            print(command)
            return command
    except sr.UnknownValueError:
        talk("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        return ""

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

def calculate_total():
    total = sum(item["price"] for item in orders)
    return total

def apply_discount():
    global special_offer_applied
    special_offer_applied = True
    talk("Special offer applied. Discounts will now be applied to your orders.")

def announce_specials():
    specials = [
        "Today's special offer: Get 10% off on the Signature Bucket.",
        "Combo of the day: Buy one Classic Zinger Combo and get a free drink."
    ]
    for special in specials:
        talk(special)

def run_alexa():
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
                print(f'Orders: {orders}')
                print(f'Total amount: {total:.2f} rupees.')
            elif 'special offer' in command:
                announce_specials()
            elif 'discount' in command:
                apply_discount()
            elif 'thank you' in command:
                talk('Thank you for being our valued customer. We are grateful for the pleasure of serving you')

while True:
    run_alexa()
    

