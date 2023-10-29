import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}
symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}


def check_winnings(columns, lines, bet, values):
    """Calculate winnings based on the slot machine spin."""
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        if all(column[line] == symbol for column in columns):
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """Generate a random spin for the slot machine."""
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range(count)]
    columns = [[random.choice(all_symbols) for _ in range(rows)] for _ in range(cols)]
    return columns


def print_slot_machine(columns):
    """Print the slot machine columns."""
    for row in range(len(columns[0])):
        print(" | ".join(column[row] for column in columns))
        

def deposit():
    """Prompt the user to deposit money."""
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        print("Please enter a valid amount.")


def get_number_of_lines():
    """Prompt the user to select the number of lines to bet on."""
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES})? ")
        if lines.isdigit() and 1 <= int(lines) <= MAX_LINES:
            return int(lines)
        print("Please enter a valid number of lines.")


def get_bet():
    """Prompt the user to place a bet."""
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit() and MIN_BET <= int(amount) <= MAX_BET:
            return int(amount)
        print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")


def spin(balance):
    """Perform a spin on the slot machine."""
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet <= balance:
            break
        print(f"You do not have enough to bet that amount, your current balance is: ${balance}")

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


def main():
    """Main function to run the slot machine game."""
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance}")


if __name__ == "__main__":
    main()