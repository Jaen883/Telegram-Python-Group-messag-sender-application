import tkinter as tk
from tkinter import ttk
import time
import telebot

# Initialize your Telegram bot using your bot token
bot = None  # We will initialize it later

# Function to save group ID and bot token
def save_data():
    group_id = group_id_entry.get()
    bot_token = bot_token_entry.get()
    with open("telegram_data.txt", "w") as file:
        file.write(f"Group ID: {group_id}\n")
        file.write(f"Bot Token: {bot_token}")
    initialize_bot(group_id, bot_token)

# Function to initialize the Telegram bot
def initialize_bot(group_id, bot_token):
    global bot
    bot = telebot.TeleBot(bot_token)

# Function to send text data to the Telegram group or bot
def send_text_data():
    if bot is not None:
        chat_id = group_id_entry.get()
        text_data = "\n".join([entry.get() for entry in text_entries])
        bot.send_message(chat_id, text_data)

# Function to send notes to Telegram
def send_notes_to_telegram():
    chat_id = group_id_entry.get()  # Use the entered group ID
    notes_text = "\n".join([entry.get() for entry in text_entries])
    bot.send_message(chat_id, notes_text)

# Function to save notes
def save_notes(event=None):
    with open("notes.txt", "w") as file:
        for i, entry in enumerate(text_entries):
            note = entry.get()
            file.write(f"Note {i+1}: {note}\n")

# Function to load notes
def load_notes():
    try:
        with open("notes.txt", "r") as file:
            lines = file.readlines()
            for i, entry in enumerate(text_entries):
                if i < len(lines):
                    note_parts = lines[i].strip().split(": ")
                    if len(note_parts) == 2:
                        note = note_parts[1]
                        entry.delete(0, tk.END)
                        entry.insert(0, note)
    except FileNotFoundError:
        pass

# Function for auto-saving notes
def auto_save():
    save_notes()
    root.after(1000, auto_save)  # Auto-save every 1 second

# Function to update time
def update_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)  # Update time every second

# Create the main window
root = tk.Tk()
root.title("Telegram Bot App")

# Entry widgets for group ID and bot token
group_id_label = ttk.Label(root, text="Group ID:")
group_id_label.pack(pady=5)
group_id_entry = ttk.Entry(root, width=40)
group_id_entry.pack(pady=5)

bot_token_label = ttk.Label(root, text="Bot Token:")
bot_token_label.pack(pady=5)
bot_token_entry = ttk.Entry(root, width=40)
bot_token_entry.pack(pady=5)

# Button to save group ID and bot token
save_data_button = ttk.Button(root, text="Save Data", command=save_data)
save_data_button.pack(pady=10)

# Label for displaying the current time
time_label = ttk.Label(root, font=("Helvetica", 16))
time_label.pack(pady=10)
update_time()

# Frame to contain the Entry widgets for notes
frame = ttk.Frame(root)
frame.pack(pady=10)

# Entry widgets for notes
text_entries = []
for i in range(10):
    entry = ttk.Entry(frame, style="TEntry", width=40)
    entry.grid(row=i, column=0, pady=5)
    text_entries.append(entry)
    entry.bind("<FocusOut>", save_notes)  # Bind FocusOut event to each entry

# Load existing notes during app startup
load_notes()

# Auto-save notes every 1 second
auto_save()

# Button to send notes to Telegram
send_button = ttk.Button(root, text="Send to Telegram", command=send_notes_to_telegram)
send_button.pack(pady=10)

root.mainloop()
