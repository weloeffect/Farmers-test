import os
import telebot
# from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from datetime import datetime
import requests
load_dotenv()

BOT_TOKEN  = os.environ.get('BOT_TOKEN')
# BASE_URL  = os.environ.get('BASE_URL')
BASE_URL  = "https://farmersbot.onrender.com/"


bot = telebot.TeleBot(BOT_TOKEN)
# bot = AsyncTeleBot(BOT_TOKEN)
print("bot-tokn", BOT_TOKEN)

# @bot.message_handler(commands=['start'])
# def SetDate(message):
   
#     print('message chat id-----', message.chat.id)
   
#     markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
#     text = "Is the date that you have entered data is today or a different date"
#     todayBtn = telebot.types.KeyboardButton('Today')
#     otherBtn = telebot.types.KeyboardButton('Other')
#     markup.add(todayBtn, otherBtn)
#     bot.send_message(message.chat.id, text, reply_markup= markup)
# Register a callback query handler to retrieve the reply markup output

DATASET =  {
    "date": "",
    "time": "",
    "location": "",
    "unit": "",
    "commodity": "",
    "quantity": "",
    "price": "",



}
Location = ["loc1", "loc2", "loc3", "loc4", "loc5",  "loc6"]
UNITS = ["u1", "u2", "u3", "u4", "u5",  "u6"]
COMMODITIES = ["c1", "c2", "c3", "c4", "c5",  "c6"]
messages = []
@bot.message_handler(commands=['start'])
def start_command(message):
    # Create a markup keyboard with two options
    #  -------- main code here

    # markup = telebot.types.InlineKeyboardMarkup()
    # option1 = telebot.types.InlineKeyboardButton('Today', callback_data='Today')
    # option2 = telebot.types.InlineKeyboardButton('Other', callback_data='Other')

    # markup.add(option1, option2)
    # ---- main code here up
    # Send a message with the markup keyboard
    # -- main code here

    # bot.send_message(message.chat.id, 'Please choose an option:', reply_markup=markup)
    
    #  main code here up
    
    USER_ID =  message.from_user.id
    # res = requests.get(BASE_URL + f'message/{USER_ID}')
    # res = requests.post(BASE_URL + f'message/{USER_ID}', {
    #     'message': messages,
    # })
    # print('testing response in telegram bot', res.json())

    # userMessages = res.json()
    
    # bot.send_message(message.chat.id, 'list of retrieved user messages: ')
    # print('user messages', userMessages['userM'][0])
    # ----------
    # arr = userMessages['userM']
    # arr_str = '\n'.join(map(str, arr))
    # bot.send_message(message.chat.id, f'list of retrieved user messages:\n{arr_str}')
    #  -------
    bot.send_message(message.chat.id, 'Hello, welcome to my bot!')
    bot.send_message(message.chat.id, 'start entering messages here and when you are done enter .(period) to stop recording')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.endswith('.'):
        print('messages after period', messages)
        bot.send_message(message.chat.id, 'Stopping message recording.')
        USER_ID =  message.from_user.id
        data = {
            "message": messages
        }
        res = requests.post(BASE_URL + f'message/{USER_ID}', json=data)
        print('res val', res)
        
        # bot.send_message(message.chat.id, f'response sent successfully: {res.json()}')
        bot.send_message(message.chat.id, 'messsage(s) sent sucessfully')
        res2 = requests.get(BASE_URL + f'message/{USER_ID}')
        print('res2 val', res2)
        bot.send_message(message.chat.id, f'backend response is {res2.json()}')
        # print('res from backend', res.json())
    else:
        messages.append(message.text)
    # print('messages', messages)

    
    # keyboard = [[telebot.types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(2)], telebot.types.InlineKeyboardButton('next', callback_data='next')]
    # reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    # bot.send_message(message.chat.id, 'Please choose from the following locations: ', reply_markup=setReplyKeyboard()) --location handler
    # bot.send_message(message.chat.id, 'Please choose from the following units: ', reply_markup=setReplyKeyboardForUnits())  -- unit handler
    # bot.send_message(message.chat.id, 'Please choose from the following commodities: ', reply_markup=setReplyKeyboardForCommodities()) -- comm handler
    # bot.send_message(message.chat.id, 'Please enter a quantity: ') -- quantity handler
    # bot.register_next_step_handler(message, quantity_handler)
    
    # bot.send_message(message.chat.id, sendText())



def quantity_handler(message):
    quantity = message.text
    DATASET['quantity'] = quantity
    bot.send_message(message.chat.id, 'Please enter a price: ')
    bot.register_next_step_handler(message, price_handler)
    # bot.send_message(message.chat.id, f"the data for quantity is {DATASET['quantity']}")


def price_handler(message):
    price = message.text
    DATASET['price'] = price
    # bot.register_next_step_handler(message, sendData_handler)
    # bot.send_message(message.chat.id, f"the data for price is {DATASET['price']}")
    bot.send_message(message.chat.id, f"the data to be saved are the following\n price: {DATASET['price']}\n commodity data: {DATASET['commodity']}\n  date data: {DATASET['date']}\n  location data: {DATASET['location']}\n  quantity data: {DATASET['quantity']}\n time data: {DATASET['time']}\n unit data: {DATASET['unit']}\n")

def sendData_handler(message):
   price = message.text
   print("final data to be sent in dataset", DATASET)


def setReplyKeyboard(): 
    keyboard = []
    # for l in Location:
    #     keyboard.append([telebot.types.InlineKeyboardButton(l, callback_data=l)])

    for i in range(0, len(Location), 2):
        row = []
        for j in range(3):
            if i+j < len(Location):
                row.append(telebot.types.InlineKeyboardButton(Location[i+j], callback_data=Location[i+j]))
        keyboard.append(row)
    
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return reply_markup
    
@bot.callback_query_handler(func=lambda call: call.data in Location)
def location_callback_handler(call):
    print('callstack data ->>', call.message.chat.id)
    selected_location = call.data
    print('selected location', selected_location)
    DATASET['location'] = selected_location
    bot.send_message(call.message.chat.id, 'Please choose from the following commodities: ', reply_markup=setReplyKeyboardForCommodities())
    # Handle selected location here
    pass

def setReplyKeyboardForUnits(): 
    keyboard = []
    # for l in Location:
    #     keyboard.append([telebot.types.InlineKeyboardButton(l, callback_data=l)])

    for i in range(0, len(UNITS), 2):
        row = []
        for j in range(3):
            if i+j < len(UNITS):
                row.append(telebot.types.InlineKeyboardButton(UNITS[i+j], callback_data=UNITS[i+j]))
        keyboard.append(row)
    
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return reply_markup
    
@bot.callback_query_handler(func=lambda call: call.data in UNITS)
def unit_callback_handler(call):
    selected_unit = call.data
    print('selected location', selected_unit)
    DATASET["unit"] = selected_unit
    bot.send_message(call.message.chat.id, 'Please enter a quantity: ')
    bot.register_next_step_handler(call.message, quantity_handler)
    # Handle selected location here
    pass


def setReplyKeyboardForCommodities(): 
    keyboard = []
    # for l in Location:
    #     keyboard.append([telebot.types.InlineKeyboardButton(l, callback_data=l)])

    for i in range(0, len(COMMODITIES), 2):
        row = []
        for j in range(3):
            if i+j < len(COMMODITIES):
                row.append(telebot.types.InlineKeyboardButton(COMMODITIES[i+j], callback_data=COMMODITIES[i+j]))
        keyboard.append(row)
    
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    return reply_markup
    
@bot.callback_query_handler(func=lambda call: call.data in COMMODITIES)
def com_callback_handler(call):
    selected_commodity = call.data
    print('selected location', selected_commodity)
    DATASET["commodity"] = selected_commodity
    bot.send_message(call.message.chat.id, 'Please choose from the following units: ', reply_markup=setReplyKeyboardForUnits())
    # Handle selected location here
    pass



# Handle callback queries from the markup keyboard
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'Today':
        # print('call data----', call.message)
        bot.answer_callback_query(callback_query_id=call.id)
        # bot.send_message(call.from_user.id, "testing reply")
        # bot.register_next_step_handler(call.message, handle_Today)
        
        handle_Today(data=call.message)
        
        
    elif call.data == 'Other':
        # print('call data----', call.message)
        bot.answer_callback_query(callback_query_id=call.id)
        # bot.register_next_step_handler(call.message, handle_Other)
        handle_Other(data=call.message)
        # Do something for option 2

    # elif call.data == 'location':
    #     print('call data----', call)
    #     bot.answer_callback_query(callback_query_id=call.id)
    else:
        pass



    
  
def handle_Today(data):
   today = datetime.now()
   date_simplified = today.strftime("%d/%m/%Y")
   time_simplified = today.strftime("%H:%M:%S")
   DATASET['date'] = date_simplified
   DATASET['time'] = time_simplified
   bot.send_message(data.chat.id, 'Please choose from the following locations: ', reply_markup=setReplyKeyboard())
#    bot.send_message(data.chat.id, f'date sent to backend is {DATASET["date"]} and time sent to backend is {DATASET["time"]}')
    

    # bot.send_message()

def handle_Other(data):
    # Your code here
    sent_msg = bot.send_message(data.chat.id, "enter the date you collected data")
    bot.register_next_step_handler(sent_msg, handle_Date)
    
def handle_Date(data):
    DATASET['date'] = data.text
    sent_msg = bot.send_message(data.chat.id, "enter the time you collected data in HH:MM format")
    bot.register_next_step_handler(sent_msg, handle_Time)

def handle_Time(data):
    DATASET['time'] = data.text
    # bot.send_message(data.chat.id, f'here is the date and time which will be sent to backend Date:{DATASET["date"]} and Time: {DATASET["time"]}')
    # bot.send_message(data.chat.id, "to be continued")
    bot.send_message(data.chat.id, 'Please choose from the following locations: ', reply_markup=setReplyKeyboard())



print('bot is starting to runsssss')
bot.polling()