import datetime
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from ttkthemes import ThemedTk

# Sample data structures for two auditoriums with 10 seats each
auditorium_1 = {
    'A1': 'available', 'A2': 'available', 'A3': 'available',
    'B1': 'available', 'B2': 'available', 'B3': 'available',
    'C1': 'available', 'C2': 'available', 'C3': 'available',
    'D1': 'available'
}

auditorium_2 = {
    'A1': 'available', 'A2': 'available', 'A3': 'available',
    'B1': 'available', 'B2': 'available', 'B3': 'available',
    'C1': 'available', 'C2': 'available', 'C3': 'available',
    'D1': 'available'
}

# Dictionary to store booking details
booking_details = {
    'auditorium_1': {},
    'auditorium_2': {}
}

# Locks for concurrency control
lock_1 = threading.Lock()
lock_2 = threading.Lock()

# Function to display auditorium layout as a grid of buttons
def display_auditorium_buttons(auditorium, frame, lock, booking_key):
    for widget in frame.winfo_children():
        widget.destroy()
    
    def on_seat_click(seat):
        with lock:
            if auditorium[seat] == "available":
                result = messagebox.askyesno("Book Seat", f"Do you want to book seat {seat}?")
                if result:
                    name = simpledialog.askstring("Input", "Enter your name:")
                    phone = simpledialog.askstring("Input", "Enter your phone number:")
                    email = simpledialog.askstring("Input", "Enter your email:")
                    auditorium[seat] = "booked"
                    booking_details[booking_key][seat] = {
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "date": datetime.datetime.now().date(),
                        "time": datetime.datetime.now().time()
                    }
                    messagebox.showinfo("Success", f"Booking successful for {name}!")
                    display_auditorium_buttons(auditorium, frame, lock, booking_key)
            else:
                messagebox.showerror("Error", f"Seat {seat} is already booked.")
    
    rows = {}
    for seat in auditorium.keys():
        row = seat[0]
        if row not in rows:
            rows[row] = []
        rows[row].append(seat)
    
    for row, seats in rows.items():
        row_frame = tk.Frame(frame)
        row_frame.pack(pady=5)
        for seat in seats:
            color = "green" if auditorium[seat] == "available" else "red"
            btn = tk.Button(row_frame, text=seat, bg=color, fg="white", width=10, height=2,
                            command=lambda s=seat: on_seat_click(s))
            btn.pack(side="left", padx=5)

# Function to see booking details
def see_booking_details(booking_key):
    if booking_details[booking_key]:
        details_text = ""
        for seat, details in booking_details[booking_key].items():
            details_text += f"Seat {seat}:\n"
            details_text += f"  Name: {details['name']}\n"
            details_text += f"  Phone: {details['phone']}\n"
            details_text += f"  Email: {details['email']}\n"
            details_text += f"  Date: {details['date']}\n"
            details_text += f"  Time: {details['time']}\n\n"
        messagebox.showinfo("Booking Details", details_text)
    else:
        messagebox.showinfo("Booking Details", "No bookings found.")

# Function to select date and time
def select_date_time():
    date_str = simpledialog.askstring("Input", "Enter date (YYYY-MM-DD):")
    time_str = simpledialog.askstring("Input", "Enter time (HH:MM):")
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        time = datetime.datetime.strptime(time_str, "%H:%M").time()
        return date.date(), time
    except ValueError:
        messagebox.showerror("Error", "Invalid date or time format.")
        return None, None

# Function to display booked seats
def display_booked_seats(auditorium):
    booked_seats = [seat for seat, status in auditorium.items() if status == 'booked']
    if booked_seats:
        return "Booked Seats: " + ", ".join(booked_seats)
    else:
        return "No seats are currently booked."

# Main function to run the booking system
def main():
    def on_select_auditorium():
        aud_choice = simpledialog.askstring("Input", "Select Auditorium (1 or 2):")
        if aud_choice == "1":
            display_auditorium_buttons(auditorium_1, auditorium_frame, lock_1, "auditorium_1")
        elif aud_choice == "2":
            display_auditorium_buttons(auditorium_2, auditorium_frame, lock_2, "auditorium_2")
        else:
            messagebox.showerror("Error", "Invalid auditorium choice.")

    def on_select_date_time():
        date, time = select_date_time()
        if date and time:
            messagebox.showinfo("Selected Date and Time", f"Selected Date: {date}, Time: {time}")

    def on_show_booked_seats():
        aud_choice = simpledialog.askstring("Input", "Select Auditorium (1 or 2):")
        if aud_choice == "1":
            messagebox.showinfo("Booked Seats", display_booked_seats(auditorium_1))
        elif aud_choice == "2":
            messagebox.showinfo("Booked Seats", display_booked_seats(auditorium_2))
        else:
            messagebox.showerror("Error", "Invalid auditorium choice.")

    def on_see_booking_details():
        aud_choice = simpledialog.askstring("Input", "Select Auditorium (1 or 2):")
        if aud_choice == "1":
            see_booking_details("auditorium_1")
        elif aud_choice == "2":
            see_booking_details("auditorium_2")
        else:
            messagebox.showerror("Error", "Invalid auditorium choice.")

    root = ThemedTk(theme="arc")
    root.title("Auditorium Booking System")
    
    # Set window size and background color
    root.geometry('800x600')
    root.configure(bg='#f0f0f0')

    global display_text
    display_text = tk.StringVar()

    # Title label with larger font and color
    title_label = tk.Label(root, text="Auditorium Booking System", font=("Helvetica", 24), bg='#f0f0f0', fg='#333')
    title_label.pack(pady=20)

    # Frame for buttons
    button_frame = tk.Frame(root, bg='#f0f0f0')
    button_frame.pack(pady=20)

    # Buttons with styles
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)

    ttk.Button(button_frame, text="Select Auditorium", command=on_select_auditorium).grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(button_frame, text="Select Date and Time", command=on_select_date_time).grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(button_frame, text="Show Booked Seats", command=on_show_booked_seats).grid(row=1, column=0, padx=10, pady=10)
    ttk.Button(button_frame, text="See Booking Details", command=on_see_booking_details).grid(row=1, column=1, padx=10, pady=10)
    ttk.Button(button_frame, text="Exit", command=root.quit).grid(row=2, columnspan=2, padx=10, pady=10)

    # Frame to display auditorium layout as buttons
    global auditorium_frame
    auditorium_frame = tk.Frame(root)
    auditorium_frame.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
