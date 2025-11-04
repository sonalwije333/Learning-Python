import math     #imports
import tkinter

button_values = [    #button layout
    ['AC', '⌫', '%', '/'],
    ['7', '8', '9', 'x'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', "√", '=']
]

right_symbols = ['/', 'x', '-', '+', '=']
top_symbols = ['AC', '⌫', '%']

row_count = len(button_values)  # 5
column_count = len(button_values[0])  # 4

color_light_gray = "#D4D4D2"  # Light gray for top buttons
color_dark_gray = "#505050"  # Dark gray for numbers
color_black = "#000000"  # Black for text
color_white = "#FFFFFF"  # White for text on dark buttons
color_orange = "#FF9500"  # Orange for operations

# window setup
window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

# Set initial window size
window.geometry("400x500")

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black, foreground=color_white,
                      anchor="e")

label.grid(row=0, column=0, columnspan=column_count, sticky="nsew")

# A+B, A-B , A*B, A/B
A = None
operator = None
B = None


def clear_all():
    global A, operator, B
    A = None
    operator = None
    B = None


def backspace_function():
    current_text = label["text"]
    if current_text != "0" and len(current_text) > 1:
        label["text"] = current_text[:-1] # Remove last character
    elif current_text != "0" and len(current_text) == 1:
        label["text"] = "0"


def remove_zero_decimal(num):
    if num % 1 == 0:
        return str(int(num))
    else:
        return str(num)


def square_root():
    try:
        current_value = float(label["text"])
        if current_value >= 0:
            result = math.sqrt(current_value)
            label["text"] = remove_zero_decimal(result)
        else:
            label["text"] = "Error"
    except:
        label["text"] = "Error"


def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "+":
                    result = numA + numB
                elif operator == "-":
                    result = numA - numB
                elif operator == "x":
                    result = numA * numB
                elif operator == "/":
                    if numB != 0:
                        result = numA / numB
                    else:
                        label["text"] = "Error"
                        return

                label["text"] = remove_zero_decimal(result)
                A = None
                operator = None
                B = None

        elif value in "+-x/":
            if A is None:
                A = label["text"]
                operator = value
                label["text"] = "0"
            else:
                # If there's already an operation pending, calculate it first
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "+":
                    result = numA + numB
                elif operator == "-":
                    result = numA - numB
                elif operator == "x":
                    result = numA * numB
                elif operator == "/":
                    if numB != 0:
                        result = numA / numB
                    else:
                        label["text"] = "Error"
                        A = None
                        operator = None
                        B = None
                        return

                label["text"] = remove_zero_decimal(result)
                A = remove_zero_decimal(result)
                operator = value
                B = None

    elif value in top_symbols:
        if value == 'AC':
            clear_all()
            label["text"] = "0"
        elif value == '⌫':
            backspace_function()
        elif value == '%':
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except:
                label["text"] = "Error"

    # MOVE SQUARE ROOT HANDLING HERE - OUTSIDE OF top_symbols CONDITION
    elif value == "√":
        square_root()

    else:  # digits or decimal
        if value == ".":
            if "." not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0" or label["text"] == "Error":
                label["text"] = value
            else:
                label["text"] += value


# Create buttons AFTER function definitions  , BUTTON CREATION LOOP
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 20),
                                command=lambda value=value: button_clicked(value))

        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        elif value == "√":  # Add special case for square root button color
            button.config(foreground=color_black, background=color_light_gray)
        else:
            button.config(foreground=color_white, background=color_dark_gray)

        button.grid(row=row + 1, column=column, sticky="nsew")

# Configure row and column weights for proper resizing
for i in range(row_count + 1):
    frame.grid_rowconfigure(i, weight=1)
for j in range(column_count):
    frame.grid_columnconfigure(j, weight=1)

frame.pack(expand=True, fill="both")

# center the window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"+{window_x}+{window_y}")

window.mainloop()