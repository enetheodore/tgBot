import telebot

BOT_TOKEN = "your bot tocken"
department_group_chats = {
    '8': 'GROUP_CHAT_ID_1',
    '12': 'GROUP_CHAT_ID_2',
    'bsc': 'GROUP_CHAT_ID_3'
}

bot = telebot.TeleBot(BOT_TOKEN)



# Dictionary of departments and jobs
departments = {
    '8': [''],
    '10': [''],
    '12': [''],
    'BSc & MSc': ['']
}

department_files = {}  # Dictionary to store files organized by department
selected_department = None  # Variable to store the selected department
user_data = {}  # Dictionary to store user data (name, sex, work experience, and job name)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for department in departments:
        keyboard.add(telebot.types.KeyboardButton(department))
    bot.reply_to(message, "እንኳን ወደ የኛ Bot በደህና መጡ! እባክዎ ስምዎን ያስገቡ:", reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_sex)

def ask_sex(message):
    user_name = message.text
    user_data[message.chat.id] = {'name': user_name}
    bot.reply_to(message, f"ሰላም, {user_name}! እባክዎ ጾታዎን ያስገቡ (ወንድ/ሴት):")
    bot.register_next_step_handler(message, ask_experience)

def ask_experience(message):
    user_sex = message.text
    user_id = message.chat.id
    user_data[user_id]['sex'] = user_sex
    bot.reply_to(message, "እባክዎን የስራ ልምድዎን ያስገቡ (ለምን ያህል አመታት?):")
    bot.register_next_step_handler(message, select_department)

def select_department(message):
    user_experience = message.text
    user_id = message.chat.id
    user_data[user_id]['experience'] = user_experience

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for department in departments:
        keyboard.add(telebot.types.KeyboardButton(department))
    bot.reply_to(message, "እባክዎን የትምህርት ደረጃዎን ይምረጡ ወይም ያስገቡ:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in departments.keys())
def list_jobs(message):
    global selected_department
    selected_department = message.text
    department = selected_department
    jobs_list = "\n".join(departments[department])
    bot.reply_to(message, f"{department}:\nእባክዎ የመረጡትን የስራ ስም ያስገቡ :")

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
        
       #sending for different groups depending on their departments
       if group_chat_id:
              bot.send_message(group_chat_id, f"File received for {department} - {job_name} job.\nUploaded by: {user_name}\nGender: {user_gender}\nExperience: {user_experience}")
       # bot.send_message(GROUP_CHAT_ID, f"File received for {department} - {job_name} job.\nUploaded by: {user_name}\nGender: {user_sex}\nExperience: {user_experience}")
        bot.send_document(GROUP_CHAT_ID, file_id)  # Send the file to the group chat
        selected_department = None
    else:
        bot.reply_to(message, "እባክዎ መጀመሪያ የትምህርት ደረጃዎን ይምረጡ!!")

bot.infinity_polling()
