# utils.py
import csv
import os
import sys # For platform check

USER_DB = "users.csv"
def clear_screen():
    # Clears the terminal screen. 'cls' for Windows, 'clear' for macOS/Linux.
    os.system('cls' if os.name == 'nt' else 'clear')
# ANSI escape codes for colors
class AnsiColors:
    HEADER = '\033[95m'    # Purple
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'   # Yellow
    FAIL = '\033[91m'      # Red
    ENDC = '\033[0m'       # Reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m' # A nice orange for farewell or special emphasis

# --- Original get_display_name ---
def get_display_name(username):
    if not os.path.exists(USER_DB):
        return username # Fallback if DB not found
    try:
        with open(USER_DB, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username:
                    return row[2] # Display name is in the 3rd column
    except FileNotFoundError:
        pass # Handled by the initial check, but good practice
    except Exception: # Catch other potential errors during file read
        pass 
    return username # Fallback if user not found or error

# --- Aesthetic Functions ---
_colorama_initialized = False

def init_colors():
    global _colorama_initialized
    if _colorama_initialized:
        return
    try:
        import colorama
        colorama.init(autoreset=True)
        _colorama_initialized = True
    except ImportError:
        # Basic ANSI enabling for Windows if colorama is missing
        if sys.platform == "win32":
            os.system('') 
        print(f"{AnsiColors.WARNING}Warning: Colorama library not found for full cross-platform color support.{AnsiColors.ENDC}")
        print(f"{AnsiColors.WARNING}Please install it with: pip install colorama{AnsiColors.ENDC}")
        # Proceed, ANSI might work on modern Windows terminals, or not.

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title, char="═", width=60):
    print(f"\n{AnsiColors.HEADER}{AnsiColors.BOLD}{char * width}{AnsiColors.ENDC}")
    title_line = f" {title.center(width-2)} "
    print(f"{AnsiColors.HEADER}{AnsiColors.BOLD}{title_line}{AnsiColors.ENDC}")
    print(f"{AnsiColors.HEADER}{AnsiColors.BOLD}{char * width}{AnsiColors.ENDC}\n")

def print_error(message):
    print(f"{AnsiColors.FAIL}❌ Error: {message}{AnsiColors.ENDC}")

def print_success(message):
    print(f"{AnsiColors.GREEN}✅ Success: {message}{AnsiColors.ENDC}")

def print_warning(message):
    print(f"{AnsiColors.WARNING}⚠️ Warning: {message}{AnsiColors.ENDC}")

def print_info(message):
    print(f"{AnsiColors.CYAN}ℹ️ {message}{AnsiColors.ENDC}")

def styled_input(prompt_message):
    return input(f"{AnsiColors.BLUE}➡️  {prompt_message}{AnsiColors.ENDC} ")

def print_option(number, text):
    print(f"  {AnsiColors.CYAN}{number}.{AnsiColors.ENDC} {text}")

def print_farewell(message="Terima kasih telah menggunakan sistem MABSkuy!"):
    print(f"\n{AnsiColors.ORANGE}{AnsiColors.BOLD}{message}{AnsiColors.ENDC}\n")

def print_table_header(columns, widths):
    header_str = ""
    for col, width in zip(columns, widths):
        header_str += f"{col:<{width}} "
    print(f"{AnsiColors.BOLD}{header_str.strip()}{AnsiColors.ENDC}")
    print(f"{AnsiColors.BLUE}{'-' * (sum(widths) + len(widths) -1)}{AnsiColors.ENDC}")

def print_table_row(values, widths, row_color=""):
    row_str = ""
    for val, width in zip(values, widths):
        row_str += f"{str(val):<{width}} "
    print(f"{row_color}{row_str.strip()}{AnsiColors.ENDC if row_color else ''}")