import telebot

BOT_TOKEN = "6087148355:AAGJsd96xkxiFgASHieUgUemow3gYPpCN5Q"
GROUP_CHAT_ID = "358877826"

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary of departments and jobs
departments = {
    '8': [''],
    '10': [''],
    '12': [''], 
    'Dep': [''],
    'BSc': [''], 
    'MSc': [''],
}

department_files = {}  # Dictionary to store files organized by department
selected_department = None  # Variable to store the selected department
user_data = {}  # Dictionary to store user data (name, sex, work experience, and job name)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.text == "/start":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for department in departments:
            keyboard.add(telebot.types.KeyboardButton(department))
        bot.reply_to(message, "እንኳን ወደ የኛ Bot በደህና መጡ! እባክዎ ስምዎን ያስገቡ:", reply_markup=keyboard)
        bot.register_next_step_handler(message, ask_sex)
    else:
        bot.reply_to(message, "Invalid command. Please use the /start command to begin.")

def ask_sex(message):
    user_name = message.text
    user_data[message.chat.id] = {'name': user_name}
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('ወንድ'), telebot.types.KeyboardButton('ሴት'))
    bot.reply_to(message, f"ሰላም, {user_name}! እባክዎ ጾታዎን ያስገቡ (ወንድ/ሴት):", reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_experience)

def ask_experience(message):
    user_sex = message.text
    user_id = message.chat.id
    user_data[user_id]['sex'] = user_sex
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(f'{i}-{i+2}') for i in range(0, 5, 2)])
    keyboard.add(telebot.types.KeyboardButton('5+'))
    bot.reply_to(message, "እባክዎን የስራ ልምድዎን ያስገቡ (ለምን ያህል አመታት?):", reply_markup=keyboard)
    bot.register_next_step_handler(message, select_department)

def select_department(message):
    user_experience = message.text
    user_id = message.chat.id
    user_data[user_id]['experience'] = user_experience

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    department_list = list(departments.keys())
    department_lists = [department_list[i:i + 2] for i in range(0, len(department_list), 2)]
    
    # Add each department list as a row in the keyboard
    for department_row in department_lists:
        keyboard_row = [telebot.types.KeyboardButton(department) for department in department_row]
        keyboard.add(*keyboard_row)
    bot.reply_to(message, "እባክዎን የትምህርት ደረጃዎን ይምረጡ ወይም ያስገቡ:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in departments.keys())
def list_jobs(message):
    global selected_department
    selected_department = message.text
    department = selected_department
    # Create a custom keyboard markup with two columns
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # Split the department options into two lists
    department_list = list(departments.keys())
    department_lists = [department_list[i:i + 2] for i in range(0, len(department_list), 2)]
    
    # Add each department list as a row in the keyboard
    for department_row in department_lists:
        keyboard_row = [telebot.types.KeyboardButton(department) for department in department_row]
        keyboard.add(*keyboard_row)
    bot.reply_to(message, f"{department}:\nእባክዎ የመረጡትን የስራ ስም ያስገቡ :", reply_markup=keyboard)

@bot.message_handler(func=lambda message: selected_department is not None)
def receive_job_name(message):
    job_name = message.text
    user_id = message.chat.id
    user_data[user_id]['job_name'] = job_name
    bot.reply_to(message, "እባክዎ ፋይልዎን ይላኩ !")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global selected_department
    if selected_department is not None:
        department = selected_department
        file_id = message.document.file_id
        caption = message.caption

        if department not in department_files:
            department_files[department] = []

        department_files[department].append((caption, file_id))
        user_id = message.chat.id
        user_name = user_data[user_id]['name']
        user_sex = user_data[user_id]['sex']
        user_experience = user_data[user_id]['experience']
        job_name = user_data[user_id]['job_name']
        bot.reply_to(message, "እናመሰግናለን! የሥራ ማመልከቻውን ተቀብለናል.")
        group_chat_id = department_group_chats.get(department)
        
        # Sending to different groups depending on their departments
        if group_chat_id:
            bot.send_message(group_chat_id, f"File received for {department} - {job_name} job.\nUploaded by: {user_name}\nGender: {user_sex}\nExperience: {user_experience}")
        bot.send_document(group_chat_id, file_id)  # Send the file to the group chat
        selected_department = None
    else:
        bot.reply_to(message, "እባክዎ መጀመሪያ የትምህርት ደረጃዎን ይምረጡ!!")

bot.infinity_polling()
