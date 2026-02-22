import tkinter as tk
import os
import json

CONFIG_FILE = "config.json"


def load_config():
    """Loads the Mindestlohn from the config file, or returns the default."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as file:
                data = json.load(file)
                return data.get("Mindestlohn", "13,90")
        except (json.JSONDecodeError, IOError):
            pass
    return "13,90"


def safe_to_float(val_str):
    """Helper function to clean strings and convert to float safely."""
    val_str = val_str.strip().replace(",", ".")
    if not val_str:
        return 0.0 # Return 0 if the field is empty
    try:
        return float(val_str)
    except ValueError:
        print(f"Warning: '{val_str}' is not a valid number. Defaulting to 0.0.")
        return 0.0


def process_inputs():
    """Retrieves and prints the values from all dynamically created input fields."""

    # Extract values using the .get() method on the stored StringVars
    raw_minlohn = input_variables["Mindestlohn"].get()
    with open(CONFIG_FILE, "w") as file:
        json.dump({"Mindestlohn": raw_minlohn}, file)
    minlohn = safe_to_float(raw_minlohn)
    auszahlung = safe_to_float(input_variables["Auszahlungsbetrag"].get())

    # List comprehensions to extract strings from every StringVar in our area lists
    stunden1_vals = [var.get() for var in input_variables["Stunden1"]]
    stunden2_vals = [var.get() for var in input_variables["Stunden2"]]
    stunden1_floats = []
    stunden2_floats = []
    for val in stunden1_vals:
        if val.strip():  # Only process if not empty
            stunden1_floats.append(safe_to_float(val))

        # Clean and convert Area 2
    for val in stunden2_vals:
        if val.strip():  # Only process if not empty
            stunden2_floats.append(safe_to_float(val))
    sum_stunden1_val = sum(stunden1_floats) * minlohn
    sum_stunden2_val = sum(stunden2_floats) * minlohn
    realbetrag = sum_stunden1_val + sum_stunden2_val
    diff = (auszahlung - realbetrag) / 3 + sum_stunden1_val / 2


def add_input_row(fieldname, default_value, area):
    new_var = tk.StringVar(value=default_value if default_value is not None else "")
    if "Stunden" in fieldname:
        if area == 1:
            input_variables["Stunden1"].append(new_var)
        else:
            input_variables["Stunden2"].append(new_var)
    else:
        clean_name = fieldname.replace(":", "").strip()
        input_variables[clean_name] = new_var

    target_frame = area1_frame if area == 1 else area2_frame
    row_frame = tk.Frame(target_frame)
    row_frame.pack(fill="x", pady=2)
    tk.Label(row_frame, text=fieldname, width=15, anchor="e").pack(side="left", padx=5)
    tk.Entry(row_frame, textvariable=new_var).pack(side="left", fill="x", expand=True, padx=5)


root = tk.Tk()
root.title("Dynamic Input List")
root.geometry("400x500")

input_variables = {
    "Stunden1": [],
    "Stunden2": []
}

main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True, padx=10, pady=10)

area1_frame = tk.Frame(main_container)
area1_frame.pack(side="top", fill="both", expand=True)

separator = tk.Frame(main_container, bg="gray", height=2)
separator.pack(side="top", fill="x", pady=15)

area2_frame = tk.Frame(main_container)
area2_frame.pack(side="top", fill="both", expand=True)

saved_minlohn = load_config()
add_input_row("Mindestlohn:", saved_minlohn, 1)
add_input_row("Auszahlungsbetrag:", "", 1)
add_input_row("Stunden:", "", 1)
add_input_row("Stunden:", "", 2)

button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=10)

add_btn1 = tk.Button(
    button_frame,
    text="Add Row to Area 1",
    command=lambda: add_input_row("Stunden:", "", 1)
)
add_btn1.pack(side="left", padx=10)
add_btn2 = tk.Button(
    button_frame,
    text="Add Row to Area 2",
    command=lambda: add_input_row("Stunden:", "", 2)
)
add_btn2.pack(side="left", padx=10)

submit_btn = tk.Button(button_frame, text="Calculate", command=process_inputs)
submit_btn.pack(side="right", padx=10)

root.mainloop()