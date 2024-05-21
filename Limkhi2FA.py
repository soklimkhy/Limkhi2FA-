import tkinter as tk
import pyotp
import base64
import time



def generate_totp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()

def on_generate():
    global secret_key  # Declare secret_key as a global variable
    secret_key = entry.get().replace(' ', '').upper()
    base64.b32decode(secret_key)
    update_code()  # Call update_code function

def update_code():
    global code  # Declare code as a global variable
    code = generate_totp(secret_key)
    # Update the clipboard with the new code
    root.clipboard_clear()
    root.clipboard_append(code)
    copy_button.config(state=tk.NORMAL)  # Enable the copy button
    countdown(30 - int(time.time()) % 30)  # Start the countdown

def countdown(time_left):
    if time_left > 0:
        label.config(text=f"Your 6-digit code is: {code}. Expires in {time_left} seconds", 
                     font=('Helvetica', 10), 
                     justify="center", 
                     bg='#02343F',
                     fg="#F0EDCC" )
        root.after(1000, countdown, time_left - 1)  # Call countdown again after 1 second
    else:
        update_code()  # Generate a new code

def on_copy():
    root.clipboard_clear()
    # Get the text from the label and split it
    text = label.cget("text").split(": ")
    # If the text can be split into two parts
    if len(text) == 2:
        # Get the second part (the code) and append it to the clipboard
        root.clipboard_append(text[1].split('.')[0])



# Create the main window
root = tk.Tk()
root.title("Limkhi 2FA")



# Set the window size
root.geometry("460x100")  # Width x Height

# Set the background color
root.configure(bg='#02343F') 

# Create the layout
entry_label = tk.Label(root, 
                       text="Key :", 
                       width=5,
                       fg="#F0EDCC",
                       bg='#02343F')
entry_label.grid(row=0, column=0, sticky='e', pady=10)  # Place on the left

entry = tk.Entry(root, 
                 font=('Helvetica', 10), 
                 width=45,
                 justify="center",
          
                 bg="#F0EDCC", 
                 fg="#02343F", 
                 bd=1, 
                 relief="solid")
entry.grid(row=0, column=1, pady=10)  # Place on the right

generate_button = tk.Button(root, 
                            text="Generate", 
                            command=on_generate, 
                            width=10, 
                            height=1, 
                            bg="#F0EDCC", 
                            fg="#02343F", 
                            activebackground="#10162f", 
                            activeforeground="white")
generate_button.grid(row=0, column=2,padx=10, pady=10)  # Add some vertical padding

label = tk.Label(root, text="...", 
                 font=('Helvetica', 10),
                 fg="#F0EDCC",
                 bg='#02343F')
label.grid(row=2, column=0, columnspan=2)

copy_button = tk.Button(root, 
                        text="Copy Code", 
                        command=on_copy, 
                        state=tk.DISABLED, 
                        width=10, 
                        height=1,
                        bg="#F0EDCC", 
                        fg="#02343F", 
                        activebackground="#10162f", 
                        activeforeground="white")
copy_button.grid(row=2, column=2, pady=10)  # Add some vertical padding

# Run the application
root.mainloop()
