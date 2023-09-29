import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

# Define the symbols and their counts and values
symbol_counts = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")
        self.root.geometry("800x600")  # Larger window size
        self.root.configure(bg="black")  # Dark mode background color

        self.balance = 0
        self.lines = 1
        self.bet = MIN_BET

        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance}", font=("Helvetica", 16), fg="white", bg="black")
        self.balance_label.pack(pady=10)

        self.lines_label = tk.Label(root, text=f"Lines: {self.lines}", font=("Helvetica", 16), fg="white", bg="black")
        self.lines_label.pack(pady=10)

        self.bet_label = tk.Label(root, text=f"Bet: ${self.bet}", font=("Helvetica", 16), fg="white", bg="black")
        self.bet_label.pack(pady=10)

        self.deposit_button = ttk.Button(root, text="Deposit", command=self.deposit, style="TButton", width=15)
        self.deposit_button.pack(pady=10)

        self.spin_button = ttk.Button(root, text="Spin", command=self.spin, style="TButton", width=15)
        self.spin_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit_game, style="TButton", width=15)
        self.quit_button.pack(pady=10)

    def deposit(self):
        amount = simpledialog.askinteger("Deposit", "What would you like to deposit? $")
        if amount is not None:
            if amount > 0:
                self.balance += amount
                self.update_balance_label()

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def update_lines_label(self):
        self.lines_label.config(text=f"Lines: {self.lines}")

    def update_bet_label(self):
        self.bet_label.config(text=f"Bet: ${self.bet}")

    def get_number_of_lines(self):
        lines = simpledialog.askinteger("Number of Lines", f"Enter the number of lines to bet on (1-{MAX_LINES}):")
        if lines is not None:
            if 1 <= lines <= MAX_LINES:
                self.lines = lines
                self.update_lines_label()

    def get_bet(self):
        bet = simpledialog.askinteger("Bet Amount", f"What would you like to bet on each line? (${MIN_BET}-{MAX_BET}):")
        if bet is not None:
            if MIN_BET <= bet <= MAX_BET:
                self.bet = bet
                self.update_bet_label()

    def spin(self):
        if self.balance <= 0:
            messagebox.showerror("Error", "You do not have enough balance to spin.")
            return

        self.get_number_of_lines()
        self.get_bet()
        total_bet = self.bet * self.lines

        if total_bet > self.balance:
            messagebox.showerror("Error", "You do not have enough balance to place this bet.")
            return

        self.balance -= total_bet
        self.update_balance_label()

        slots = self.get_slot_machine_spin()
        self.show_slot_machine(slots)
        winnings, winning_lines = self.check_winnings(slots)
        self.balance += winnings
        self.update_balance_label()

        messagebox.showinfo("Result", f"You won ${winnings} on lines: {winning_lines}")

    def get_slot_machine_spin(self):
        all_symbols = []
        for symbol, symbol_count in symbol_counts.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(COLS):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(ROWS):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)
            columns.append(column)

        return columns

    def show_slot_machine(self, columns):
        slot_machine_window = tk.Toplevel(self.root)
        slot_machine_window.title("Slot Machine Spin Result")

        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                label = tk.Label(slot_machine_window, text=column[row], width=5, height=2, font=("Helvetica", 20))
                label.grid(row=row, column=i)

    def check_winnings(self, columns):
        winnings = 0
        winning_lines = []
        for line in range(self.lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += symbol_value[symbol] * self.bet
                winning_lines.append(line + 1)
        return winnings, winning_lines

    def quit_game(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Define a ttk style for buttons
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 14), foreground="black", background="light gray")
    
    app = SlotMachineApp(root)
    root.mainloop()
