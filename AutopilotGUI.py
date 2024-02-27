import tkinter as tk

# Create an instance of the Tk class
root = tk.Tk()

# Set the window size to 720p with grey background
root.geometry("1280x720")
root.configure(bg='#5c5d5d')

# Set the window title
root.title("AutoPiLot")


def create_dial_placeholder(canvas, label_text):
    # Create a circle
    canvas.create_oval(10, 10, 210, 210, outline="#000", fill="#FFF")
    # Create a label for the dial
    canvas.create_text(105, 220, text=label_text)


# Speed Dial Placeholder
speed_canvas = tk.Canvas(root, width=220, height=240, bg='#D3D3D3', highlightthickness=0)
create_dial_placeholder(speed_canvas, "Speed")
speed_canvas.grid(row=0, column=0, padx=20, pady=20)

# Target Speed Dial Placeholder
target_speed_canvas = tk.Canvas(root, width=220, height=240, bg='#D3D3D3', highlightthickness=0)
create_dial_placeholder(target_speed_canvas, "Target Speed")
target_speed_canvas.grid(row=0, column=1, padx=20, pady=20)

# Altitude Dial Placeholder
altitude_canvas = tk.Canvas(root, width=220, height=240, bg='#D3D3D3', highlightthickness=0)
create_dial_placeholder(altitude_canvas, "Altitude")
altitude_canvas.grid(row=1, column=0, padx=20, pady=20)

# Target Altitude Dial Placeholder
target_altitude_canvas = tk.Canvas(root, width=220, height=240, bg='#D3D3D3', highlightthickness=0)
create_dial_placeholder(target_altitude_canvas, "Target Altitude")
target_altitude_canvas.grid(row=1, column=1, padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
