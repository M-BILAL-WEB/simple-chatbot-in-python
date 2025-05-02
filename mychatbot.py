import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai

# Replace this with your real API key from Google AI Studio
API_KEY = ""
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Function to handle chat
def send_message():
    user_message = user_input.get()
    if user_message.strip() == "" or user_message == placeholder_text:
        return
    
    chat_window.insert(tk.END, f"You: {user_message}\n")
    user_input.delete(0, tk.END)

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text.strip()
        chat_window.insert(tk.END, f"Chatbot: {bot_reply}\n\n")
    except Exception as e:
        chat_window.insert(tk.END, f"Error: {str(e)}\n\n")

# Placeholder handling
def on_entry_click(event):
    if user_input.get() == placeholder_text:
        user_input.delete(0, tk.END)
        user_input.config(fg="black")

def on_focusout(event):
    if user_input.get() == "":
        user_input.insert(0, placeholder_text)
        user_input.config(fg="gray")

def send_message():
    user_message = user_input.get()
    if user_message.strip() == "" or user_message == placeholder_text:
        return

    chat_window.insert(tk.END, f"You: {user_message}\n")
    chat_window.insert(tk.END, "Chatbot: Typing...\n")
    chat_window.update()
    user_input.delete(0, tk.END)

    try:
        response = model.generate_content(user_message)
        chat_window.delete("end-3l", "end-2l")  # Remove "Typing..."
        bot_reply = response.text.strip()
        chat_window.insert(tk.END, f"Chatbot: {bot_reply}\n\n")
    except Exception as e:
        chat_window.insert(tk.END, f"Error: {str(e)}\n\n")


# Creates the main window
window = tk.Tk()
window.title("MyChatbot")
window.geometry("500x600")

# Chat display
chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.config(state=tk.NORMAL)

# Insert welcome message
chat_window.insert(tk.END, "Chatbot: How can I help you today?\n\n")

# User input field with placeholder
placeholder_text = "Type here..."
user_input = tk.Entry(window, font=("Arial", 14), fg="gray")
user_input.insert(0, placeholder_text)
user_input.bind("<FocusIn>", on_entry_click)
user_input.bind("<FocusOut>", on_focusout)
user_input.bind("<Return>", lambda event: send_message())
user_input.pack(padx=10, pady=(0,10), fill=tk.X)

send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(padx=10, pady=(0,10))

# Run the GUI loop
window.mainloop()
