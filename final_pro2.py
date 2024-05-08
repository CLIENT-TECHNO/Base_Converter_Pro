import tkinter as tk
from tkinter import messagebox

def clear1():
    result_entry.delete(0, "end")
    entry.delete(0, "end")

def exit11():
    close = messagebox.askyesno('EXIT', 'Are you sure that you want to exit?')
    if close:
        root.destroy()

def validate_input(value, base):
    if base == 10:
        return value.replace('.', '').replace('-', '').replace('+', '').isdigit()
    elif base == 2:
        return all(digit in '01.-+' for digit in value)
    elif base == 8:
        return all(digit in '01234567.-+' for digit in value)
    elif base == 16:
        return all(digit in '0123456789ABCDEFabcdef.-+' for digit in value)
    else:
        return False

def convert():
    expression = entry.get()
    source_base = int(from_var.get())
    target_base = int(to_var.get())

    try:
        if not validate_input(expression, source_base):
            raise ValueError("Invalid input for the selected base.")

        if '+' in expression or '-' in expression or '*' in expression or '/' in expression:
            operation = next((op for op in ['+', '-', '*', '/'] if op in expression), None)
            if operation is None:
                raise ValueError("Invalid operation")
            expression_parts = [part.strip() for part in expression.split(operation)]
            if len(expression_parts) != 2:
                raise ValueError("Invalid expression format")
            operand1 = expression_parts[0]
            operand2 = expression_parts[1]
            decimal1 = decimal_value_from_base(source_base, operand1)
            decimal2 = decimal_value_from_base(source_base, operand2)
            decimal_result = decimal_operation(decimal1, decimal2, operation)
        else:
            decimal_value = float(expression)
            if source_base == 10:
                decimal_value = float(expression)
            elif source_base == 2:
                decimal_value = binary_to_decimal(expression)
            elif source_base == 8:
                decimal_value = octal_to_decimal(expression)
            elif source_base == 16:
                decimal_value = hexadecimal_to_decimal(expression)
            decimal_result = decimal_value

        # Convert result to target base
        if target_base == 10:
            result = str(decimal_result)
        elif target_base == 2:
            result = decimal_to_binary(decimal_result)
        elif target_base == 8:
            result = decimal_to_octal(decimal_result)
        elif target_base == 16:
            result = decimal_to_hexadecimal(decimal_result)

        result_var.set(f"Result: {result}")

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input or expression: {e}")

def ones_complement():
    expression = entry.get()
    source_base = int(from_var.get())

    try:
        if not validate_input(expression, source_base):
            raise ValueError("Invalid input for the selected base.")
            
        if source_base == 2:
            result = ones_complement_binary(expression)
            result_var.set(f"1\'C: {result}")
        else:
            raise ValueError("One's complement is only applicable to binary numbers.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def twos_complement():
    expression = entry.get()
    source_base = int(from_var.get())

    try:
        if not validate_input(expression, source_base):
            raise ValueError("Invalid input for the selected base.")
            
        if source_base == 2:
            result = twos_complement_binary(expression)
            result_var.set(f"2\'C: {result}")
        else:
            raise ValueError("Two's complement is only applicable to binary numbers.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def binary_to_decimal(binary_number):
    if '.' in binary_number:
        integer_part, fractional_part = binary_number.split('.')
        integer_decimal = sum(int(digit) * (2 ** index) for index, digit in enumerate(integer_part[::-1]))
        fractional_decimal = sum(int(digit) * (2 ** (-index - 1)) for index, digit in enumerate(fractional_part))
        return integer_decimal + fractional_decimal
    else:
        return sum(int(digit) * (2 ** index) for index, digit in enumerate(binary_number[::-1]))

def octal_to_decimal(octal_number):
    if '.' in octal_number:
        integer_part, fractional_part = octal_number.split('.')
        integer_decimal = sum(int(digit) * (8 ** index) for index, digit in enumerate(integer_part[::-1]))
        fractional_decimal = sum(int(digit) * (8 ** (-index - 1)) for index, digit in enumerate(fractional_part))
        return integer_decimal + fractional_decimal
    else:
        return sum(int(digit) * (8 ** index) for index, digit in enumerate(octal_number[::-1]))

def hexadecimal_to_decimal(hexadecimal_number):
    if '.' in hexadecimal_number:
        integer_part, fractional_part = hexadecimal_number.split('.')
        integer_decimal = sum(int(digit, 16) * (16 ** index) for index, digit in enumerate(integer_part[::-1]))
        fractional_decimal = sum(int(digit, 16) * (16 ** (-index - 1)) for index, digit in enumerate(fractional_part))
        return integer_decimal + fractional_decimal
    else:
        return sum(int(digit, 16) * (16 ** index) for index, digit in enumerate(hexadecimal_number[::-1]))

def decimal_to_binary(decimal_number):
    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part if '.' in str(decimal_number) else 0
    integer_binary = bin(integer_part)[2:]
    fractional_binary = ''
    if fractional_part != 0:
        fractional_binary = '.'
        max_precision = 10
        while fractional_part > 0 and max_precision > 0:
            fractional_part *= 2
            if fractional_part >= 1:
                fractional_part -= 1
                fractional_binary += '1'
            else:
                fractional_binary += '0'
            max_precision -= 1
    return integer_binary + fractional_binary

def decimal_to_octal(decimal_number):
    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part if '.' in str(decimal_number) else 0
    integer_octal = oct(integer_part)[2:]
    fractional_octal = ''
    if fractional_part != 0:
        fractional_octal = '.'
        max_precision = 10
        while fractional_part > 0 and max_precision > 0:
            fractional_part *= 8
            digit = int(fractional_part)
            fractional_octal += str(digit)
            fractional_part -= digit
            max_precision -= 1
    return integer_octal + fractional_octal

def decimal_to_hexadecimal(decimal_number):
    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part if '.' in str(decimal_number) else 0
    integer_hexadecimal = hex(integer_part)[2:].upper()
    fractional_hexadecimal = ''
    if fractional_part != 0:
        fractional_hexadecimal = '.'
        max_precision = 10
        while fractional_part > 0 and max_precision > 0:
            fractional_part *= 16
            digit = int(fractional_part)
            fractional_hexadecimal += hex(digit)[2:].upper()
            fractional_part -= digit
            max_precision -= 1
    return integer_hexadecimal + fractional_hexadecimal

def decimal_operation(decimal1, decimal2, operation):
    if operation == '+':
        return decimal1 + decimal2
    elif operation == '-':
        return decimal1 - decimal2
    elif operation == '*':
        return decimal1 * decimal2
    elif operation == '/':
        return decimal1 / decimal2

def decimal_value_from_base(base, number):
    if base == 2:
        return binary_to_decimal(number)
    elif base == 8:
        return octal_to_decimal(number)
    elif base == 16:
        return hexadecimal_to_decimal(number)
    else:
        return float(number)

def ones_complement_binary(binary_number):
    if isinstance(binary_number, str) and all(digit in '01' for digit in binary_number):
        return ''.join(['1' if bit == '0' else '0' for bit in binary_number])
    else:
        raise ValueError("Invalid binary number")

def twos_complement_binary(binary_number):
    if isinstance(binary_number, str) and all(digit in '01' for digit in binary_number):
        ones_comp = ones_complement_binary(binary_number)
        return bin(int(ones_comp, 2) + 1)[2:]
    else:
        raise ValueError("Invalid binary number")

root = tk.Tk()
root.title("Number System Converter")
root.geometry("600x700")
root.configure(bg="#092635", cursor='pirate')
root.resizable(width=False, height=False)

entry = tk.Entry(root, width=25, bg="#9EC8B9", cursor='pirate', fg="#283747", font=("Arial", 30), bd=5)
entry.pack(pady=20)

from_var = tk.IntVar()
to_var = tk.IntVar()

from_frame = tk.Frame(root, bg="#092635")
from_frame.pack()
from_label = tk.Label(from_frame, text="From:", cursor='pirate', font=("Helvetica", 15), bg="#092635", fg="#5C8374")
from_label.pack(side="left")
from_radio_decimal = tk.Radiobutton(from_frame, text="Decimal", cursor='pirate', variable=from_var, value=10,
                                    bg="#092635", fg="#5C8374", font=("Helvetica", 15))
from_radio_decimal.pack(side="left", padx=10)
from_radio_binary = tk.Radiobutton(from_frame, text="Binary", cursor='pirate', variable=from_var, value=2, bg="#092635",
                                   fg="#5C8374", font=("Helvetica", 15))
from_radio_binary.pack(side="left", padx=10)
from_radio_octal = tk.Radiobutton(from_frame, text="Octal", cursor='pirate', variable=from_var, value=8, bg="#092635",
                                  fg="#5C8374", font=("Helvetica", 15))
from_radio_octal.pack(side="left", padx=10)
from_radio_hexadecimal = tk.Radiobutton(from_frame, cursor='pirate', text="Hexadecimal", variable=from_var, value=16,
                                        bg="#092635", fg="#5C8374", font=("Helvetica", 15))
from_radio_hexadecimal.pack(side="left", padx=10)

to_frame = tk.Frame(root, bg="#092635")
to_frame.pack(padx=40)
to_label = tk.Label(to_frame, text="To:", cursor='pirate', font=("Helvetica", 15), bg="#092635", fg="#5C8374")
to_label.pack(side="left")
to_radio_decimal = tk.Radiobutton(to_frame, text="Decimal", cursor='pirate', variable=to_var, value=10, bg="#092635",
                                  fg="#5C8374", font=("Helvetica", 15))
to_radio_decimal.pack(side="left", padx=10)
to_radio_binary = tk.Radiobutton(to_frame, text="Binary", cursor='pirate', variable=to_var, value=2, bg="#092635",
                                 fg="#5C8374", font=("Helvetica", 15))
to_radio_binary.pack(side="left", padx=10)
to_radio_octal = tk.Radiobutton(to_frame, text="Octal", variable=to_var, value=8, bg="#092635", fg="#5C8374",
                                font=("Helvetica", 15))
to_radio_octal.pack(side="left", padx=10)
to_radio_hexadecimal = tk.Radiobutton(to_frame, text="Hexadecimal", cursor='pirate', variable=to_var, value=16,
                                      bg="#092635", fg="#5C8374", font=("Helvetica", 15))
to_radio_hexadecimal.pack(side="left", padx=10)

result_var = tk.StringVar()

result_entry = tk.Entry(root, width=25, text="", cursor='star', font=("Helvetica", 30), bg="#9EC8B9",
                        fg="black", textvariable=result_var)
result_entry.pack(pady=70)

exit_button = tk.Button(root, text='Exit', fg='black', bg='#5C8374',command= exit11, relief="groove", width=39,
                        font=('Arial', 18))
exit_button.pack(side="bottom", pady=8)

clear_button = tk.Button(root, text='clear', fg='black', bg='#5C8374', relief="groove",command=clear1, width=39,
                         font=('Arial', 18))
clear_button.pack(side="bottom", pady=2)

convert_button = tk.Button(root, text="Convert", bg="#5C8374", fg="black", font=('Arial', 18),
                           relief="groove", width=39, command=convert)
convert_button.pack(side="bottom", pady=6)

twos_complement_button = tk.Button(root, text="twos-complement", bg="#5C8374", fg="black", font=('Arial', 18),
                           relief="groove", width=39, command=twos_complement)
twos_complement_button.pack(side="bottom", pady=6)

ones_complement_button = tk.Button(root, text="ones-complement", bg="#5C8374", fg="black", font=('Arial', 18),
                           relief="groove", width=39, command=ones_complement)
ones_complement_button.pack(side="bottom", pady=6)

root.mainloop()
