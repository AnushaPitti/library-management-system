"""
LIBRARY MANAGEMENT SYSTEM
Think Champ PV LTD - Internship Mini Project
Python 3.x | No External Dependencies Required
"""

import json
import os
from datetime import datetime, timedelta

BOOKS_FILE = "books.json"
STUDENTS_FILE = "students.json"
TRANSACTIONS_FILE = "transactions.json"
USERS_FILE = "users.json"

FINE_PER_DAY = 2
LOAN_PERIOD_DAYS = 14
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_ADMIN = {
    "username": "admin",
    "password": "admin123",
    "full_name": "Administrator",
    "role": "Admin",
    "registered_date": "2026-06-01 00:00:00"
}

CATEGORIES = [
    "Fiction", "Non-Fiction", "Science", "Technology", "Programming",
    "Mathematics", "History", "Biography", "Self-Help", "Literature",
    "Engineering", "Medical", "Law", "Arts", "Comics", "Reference", "Other"
]

class Color:
    ESC     = "\033"
    RESET   = ESC + "[0m"
    BOLD    = ESC + "[1m"
    DIM     = ESC + "[2m"
    RED     = ESC + "[91m"
    GREEN   = ESC + "[92m"
    YELLOW  = ESC + "[93m"
    BLUE    = ESC + "[94m"
    MAGENTA = ESC + "[95m"
    CYAN    = ESC + "[96m"
    WHITE   = ESC + "[97m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title, color=None):
    if color is None:
        color = Color.CYAN
    w = 60
    print(f"\n{color}{Color.BOLD}{'=' * w}")
    print(f"  {title.upper()}")
    print(f"{'=' * w}{Color.RESET}")

def print_success(msg):
    print(f"  {Color.GREEN}[OK] {msg}{Color.RESET}")

def print_error(msg):
    print(f"  {Color.RED}[ERROR] {msg}{Color.RESET}")

def print_warning(msg):
    print(f"  {Color.YELLOW}[WARNING] {msg}{Color.RESET}")

def print_info(msg):
    print(f"  {Color.BLUE}[INFO] {msg}{Color.RESET}")

def get_input(prompt, allow_empty=False):
    while True:
        value = input(f"  {Color.WHITE}{prompt}{Color.RESET}").strip()
        if value or allow_empty:
            return value
        print_error("This field cannot be empty.")

def get_choice(prompt, valid_options):
    while True:
        choice = input(f"  {Color.CYAN}> {prompt}{Color.RESET}").strip()
        if choice in valid_options:
            return choice
        print_error(f"Invalid choice. Enter one of: {', '.join(valid_options)}")

def confirm(prompt):
    response = input(f"  {Color.YELLOW}{prompt} (y/n): {Color.RESET}").strip().lower()
    return response in ('y', 'yes')

def generate_id(prefix, existing_ids):
    max_num = 0
    for eid in existing_ids:
        if eid.startswith(prefix):
            try:
                num = int(eid[len(prefix):])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return f"{prefix}{max_num + 1:04d}"

def format_table_row(columns, widths, color=None):
    if color is None:
        color = Color.WHITE
    row = "  |"
    for col, width in zip(columns, widths):
        row += f" {str(col):<{width}} |"
    return f"{color}{row}{Color.RESET}"

def format_table_separator(widths, char="-"):
    sep = "  +"
    for w in widths:
        sep += f"{char * (w + 2)}+"
    return sep

def format_table_top(widths):
    return format_table_separator(widths, "-")

def format_table_bottom(widths):
    return format_table_separator(widths, "-")

def load_json(filepath, default=None):
    if default is None:
        default = []
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print_warning(f"Could not load {filepath}: {e}")
    return default

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print_error(f"Could not save {filepath}: {e}")

def initialize_users():
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, [DEFAULT_ADMIN])
        return [DEFAULT_ADMIN.copy()]
    users = load_json(USERS_FILE, [])
    if not users:
        save_json(USERS_FILE, [DEFAULT_ADMIN])
        return [DEFAULT_ADMIN.copy()]
    return users

def register_new_user(users):
    print_header("Register New User", Color.GREEN)
    full_name  = get_input("Enter Full Name      : ")
    username   = get_input("Enter Username       : ")
    for u in users:
        if u["username"].lower() == username.lower():
            print_error(f"Username '{username}' already exists! Try a different one.")
            return users, False
    password   = get_input("Enter Password       : ")
    confirm_pw = get_input("Confirm Password     : ")
    if password != confirm_pw:
        print_error("Passwords do not match! Registration failed.")
        return users, False
    if len(password) < 4:
        print_error("Password must be at least 4 characters long!")
        return users, False
    print(f"\n  {Color.CYAN}Select Role:{Color.RESET}")
    print(f"    1. Admin (Full access)")
    print(f"    2. User  (Standard access)")
    role_choice = get_choice("Enter role (1/2): ", ["1", "2"])
    role = "Admin" if role_choice == "1" else "User"
    new_user = {
        "username": username, "password": password, "full_name": full_name,
        "role": role, "registered_date": datetime.now().strftime(DATE_FORMAT)
    }
    users.append(new_user)
    save_json(USERS_FILE, users)
    print()
    print_success(f"Registration Successful!")
    print_info(f"Name     : {full_name}")
    print_info(f"Username : {username}")
    print_info(f"Role     : {role}")
    print()
    print_info("You can now login with your new credentials.")
    return users, True

def login_user(users):
    print_header("Login", Color.YELLOW)
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        username = get_input(f"Username (Attempt {attempt}/{max_attempts}): ")
        password = get_input(f"Password: ")
        for u in users:
            if u["username"] == username and u["password"] == password:
                print_success(f"Login Successful! Welcome, {u['full_name']}!")
                return u
        remaining = max_attempts - attempt
        if remaining > 0:
            print_error(f"Invalid credentials! {remaining} attempt(s) remaining.")
        else:
            print_error("Maximum attempts exceeded. Access Denied!")
            return None
    return None

def pre_login_menu():
    clear_screen()
    print(f"""
{Color.CYAN}{Color.BOLD}
    +==============================================================+
    |                                                              |
    |        LIBRARY MANAGEMENT SYSTEM                             |
    |                                                              |
    |        Welcome!                                              |
    |        Think Champ PV LTD - Internship Project               |
    |                                                              |
    +==============================================================+
{Color.RESET}""")
    users = initialize_users()
    while True:
        print(f"""
{Color.CYAN}{Color.BOLD}  +----------------------------------------------+
  |              WELCOME TO LIBRARY              |
  +----------------------------------------------+{Color.RESET}
  {Color.WHITE}|                                              |
  |    1.  Login (Existing User)                 |
  |    2.  Register New User                     |
  |    3.  Exit                                  |
  |                                              |
  {Color.CYAN}{Color.BOLD}+----------------------------------------------+{Color.RESET}""")
        choice = get_input("\n  Enter Your Choice (1-3): ")
        if choice == "1":
            user = login_user(users)
            if user:
                return user
            input(f"\n  {Color.DIM}Press Enter to try again...{Color.RESET}")
        elif choice == "2":
            users, success = register_new_user(users)
            input(f"\n  {Color.DIM}Press Enter to continue...{Color.RESET}")
        elif choice == "3":
            print(f"\n  {Color.GREEN}Goodbye!{Color.RESET}")
            return None
        else:
            print_error("Invalid choice! Please enter 1, 2, or 3.")

def add_book(books):
    print_header("Add New Book", Color.GREEN)
    book_id = generate_id("BK", [b["id"] for b in books])
    print_info(f"Auto-generated Book ID: {Color.BOLD}{book_id}{Color.RESET}")
    title  = get_input("Enter Book Title       : ")
    author = get_input("Enter Author Name      : ")
    isbn   = get_input("Enter ISBN Number       : ")
    for b in books:
        if b["isbn"].lower() == isbn.lower():
            print_error(f"ISBN '{isbn}' already exists: '{b['title']}'")
            return books
    print(f"\n  {Color.CYAN}Available Categories:{Color.RESET}")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i:2d}. {cat}")
    cat_choice = get_input("Enter Category Number  : ")
    try:
        category = CATEGORIES[int(cat_choice) - 1]
    except (ValueError, IndexError):
        category = "Other"
        print_warning("Invalid category. Defaulting to 'Other'.")
    qty_str = get_input("Enter Quantity         : ")
    try:
        quantity = max(1, int(qty_str))
    except ValueError:
        quantity = 1
        print_warning("Invalid quantity. Defaulting to 1.")
    book = {"id": book_id, "title": title, "author": author, "isbn": isbn,
            "category": category, "quantity": quantity, "available": quantity,
            "added_date": datetime.now().strftime(DATE_FORMAT)}
    books.append(book)
    save_json(BOOKS_FILE, books)
    print()
    print_success(f"Book '{title}' (ID: {book_id}) added successfully!")
    print_info(f"Category: {category} | Quantity: {quantity} | ISBN: {isbn}")
    return books

def view_books(books, transactions):
    print_header("All Books in Library", Color.BLUE)
    if not books:
        print_warning("No books in the library yet.")
        return
    widths = [7, 25, 18, 14, 13, 5, 5, 10]
    headers = ["ID", "Title", "Author", "ISBN", "Category", "Qty", "Avl", "Status"]
    print(format_table_top(widths))
    print(format_table_row(headers, widths, Color.BOLD + Color.CYAN))
    print(format_table_separator(widths, "="))
    for b in books:
        status = f"{Color.GREEN}In Stock" if b["available"] > 0 else f"{Color.RED}All Out"
        row = [b["id"], b["title"][:25], b["author"][:18], b["isbn"][:14],
               b["category"][:13], b["quantity"], b["available"], status + Color.RESET]
        print(format_table_row(row, widths))
    print(format_table_bottom(widths))
    print_info(f"Total: {len(books)} | Copies: {sum(b['quantity'] for b in books)} | Available: {sum(b['available'] for b in books)}")

def search_book(books):
    print_header("Search Book", Color.MAGENTA)
    print(f"  {Color.CYAN}Search by:{Color.RESET}")
    print("    1. Title")
    print("    2. Author")
    print("    3. ISBN Number")
    print("    4. Category")
    print("    5. Book ID")
    choice = get_choice("Enter search type (1-5): ", ["1", "2", "3", "4", "5"])
    keyword = get_input("Enter search keyword    : ").lower()
    field_map = {"1": "title", "2": "author", "3": "isbn", "4": "category", "5": "id"}
    field = field_map[choice]
    results = [b for b in books if keyword in b[field].lower()]
    if results:
        print(f"\n  {Color.GREEN}Found {len(results)} result(s):{Color.RESET}\n")
        widths = [7, 25, 18, 14, 13, 5, 5]
        headers = ["ID", "Title", "Author", "ISBN", "Category", "Qty", "Avl"]
        print(format_table_top(widths))
        print(format_table_row(headers, widths, Color.BOLD + Color.CYAN))
        print(format_table_separator(widths, "="))
        for b in results:
            print(format_table_row([b["id"], b["title"][:25], b["author"][:18],
                   b["isbn"][:14], b["category"][:13], b["quantity"], b["available"]], widths))
        print(format_table_bottom(widths))
    else:
        print_error(f"No books found matching '{keyword}' in {field}.")

def update_book(books):
    print_header("Update Book Details", Color.YELLOW)
    book_id = get_input("Enter Book ID to update: ").upper()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        print_error(f"Book ID '{book_id}' not found.")
        return books
    print_info(f"Current: {book['title']} by {book['author']}")
    print(f"  {Color.DIM}(Press Enter to keep current value){Color.RESET}\n")
    new_title = input(f"  Title    [{book['title']}]  : ").strip()
    new_author = input(f"  Author   [{book['author']}] : ").strip()
    new_isbn = input(f"  ISBN     [{book['isbn']}]   : ").strip()
    new_qty = input(f"  Quantity [{book['quantity']}]      : ").strip()
    if new_title: book["title"] = new_title
    if new_author: book["author"] = new_author
    if new_isbn: book["isbn"] = new_isbn
    if new_qty:
        try:
            diff = int(new_qty) - book["quantity"]
            book["quantity"] = int(new_qty)
            book["available"] = max(0, book["available"] + diff)
        except ValueError:
            print_warning("Invalid quantity.")
    save_json(BOOKS_FILE, books)
    print_success(f"Book '{book['title']}' updated!")
    return books

def delete_book(books, transactions):
    print_header("Delete Book", Color.RED)
    book_id = get_input("Enter Book ID to delete: ").upper()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        print_error(f"Book ID '{book_id}' not found.")
        return books
    issued = book["quantity"] - book["available"]
    if issued > 0:
        print_error(f"Cannot delete! {issued} copies currently issued.")
        return books
    print_warning(f"Book: '{book['title']}' by {book['author']}")
    if confirm("Are you sure you want to delete?"):
        books.remove(book)
        save_json(BOOKS_FILE, books)
        print_success(f"Book '{book['title']}' deleted!")
    else:
        print_info("Cancelled.")
    return books

def add_student(students):
    print_header("Register New Student", Color.GREEN)
    sid = generate_id("ST", [s["id"] for s in students])
    print_info(f"Auto-generated Student ID: {Color.BOLD}{sid}{Color.RESET}")
    name  = get_input("Enter Student Name     : ")
    email = get_input("Enter Email Address    : ")
    phone = get_input("Enter Phone Number     : ")
    course = get_input("Enter Course/Dept      : ")
    for s in students:
        if s["email"].lower() == email.lower():
            print_error(f"Email '{email}' already exists.")
            return students
    student = {"id": sid, "name": name, "email": email, "phone": phone,
               "course": course, "registered_date": datetime.now().strftime(DATE_FORMAT),
               "total_fines_paid": 0}
    students.append(student)
    save_json(STUDENTS_FILE, students)
    print_success(f"Student '{name}' (ID: {sid}) registered!")
    return students

def view_students(students):
    print_header("All Registered Students", Color.BLUE)
    if not students:
        print_warning("No students registered yet.")
        return
    widths = [7, 22, 22, 12, 15]
    headers = ["ID", "Name", "Email", "Phone", "Course"]
    print(format_table_top(widths))
    print(format_table_row(headers, widths, Color.BOLD + Color.CYAN))
    print(format_table_separator(widths, "="))
    for s in students:
        print(format_table_row([s["id"], s["name"][:22], s["email"][:22],
               s["phone"][:12], s["course"][:15]], widths))
    print(format_table_bottom(widths))
    print_info(f"Total Students: {len(students)}")

def issue_book(books, students, transactions):
    print_header("Issue Book", Color.GREEN)
    book_id = get_input("Enter Book ID    : ").upper()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        print_error(f"Book ID '{book_id}' not found.")
        return books, transactions
    if book["available"] <= 0:
        print_error(f"'{book['title']}' not available. All copies issued.")
        return books, transactions
    student_id = get_input("Enter Student ID : ").upper()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        print_error(f"Student ID '{student_id}' not found. Register first.")
        return books, transactions
    for t in transactions:
        if t["book_id"] == book_id and t["student_id"] == student_id and t["status"] == "Issued":
            print_error("Student already has this book.")
            return books, transactions
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=LOAN_PERIOD_DAYS)
    txn = {"txn_id": generate_id("TXN", [t["txn_id"] for t in transactions]),
           "book_id": book_id, "book_title": book["title"],
           "student_id": student_id, "student_name": student["name"],
           "issue_date": issue_date.strftime(DATE_FORMAT),
           "due_date": due_date.strftime(DATE_FORMAT),
           "return_date": None, "fine": 0, "status": "Issued"}
    book["available"] -= 1
    transactions.append(txn)
    save_json(BOOKS_FILE, books)
    save_json(TRANSACTIONS_FILE, transactions)
    print()
    print_success("Book Issued Successfully!")
    print_info(f"Book    : {book['title']} ({book_id})")
    print_info(f"Student : {student['name']} ({student_id})")
    print_info(f"Issue   : {issue_date.strftime('%d-%b-%Y %I:%M %p')}")
    print_info(f"Due     : {due_date.strftime('%d-%b-%Y %I:%M %p')}")
    print_warning(f"Fine of Rs.{FINE_PER_DAY}/day after due date.")
    return books, transactions

def return_book(books, students, transactions):
    print_header("Return Book", Color.YELLOW)
    book_id = get_input("Enter Book ID    : ").upper()
    student_id = get_input("Enter Student ID : ").upper()
    txn = None
    for t in transactions:
        if t["book_id"] == book_id and t["student_id"] == student_id and t["status"] == "Issued":
            txn = t
            break
    if not txn:
        print_error("No active issue record found.")
        return books, transactions
    book = next((b for b in books if b["id"] == book_id), None)
    student = next((s for s in students if s["id"] == student_id), None)
    return_date = datetime.now()
    due_date = datetime.strptime(txn["due_date"], DATE_FORMAT)
    fine = 0
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine = overdue_days * FINE_PER_DAY
        print_warning(f"OVERDUE by {overdue_days} day(s)!")
        print_warning(f"Fine: {overdue_days} x Rs.{FINE_PER_DAY} = Rs.{fine}")
    else:
        print_success("Returned on time. No fine!")
    txn["return_date"] = return_date.strftime(DATE_FORMAT)
    txn["fine"] = fine
    txn["status"] = "Returned"
    if book: book["available"] += 1
    if student and fine > 0: student["total_fines_paid"] += fine
    save_json(BOOKS_FILE, books)
    save_json(STUDENTS_FILE, students)
    save_json(TRANSACTIONS_FILE, transactions)
    print()
    print_success("Book Returned Successfully!")
    print_info(f"Book: {txn['book_title']} | Student: {txn['student_name']}")
    if fine > 0:
        print(f"  {Color.RED}{Color.BOLD}  Fine Amount: Rs.{fine}{Color.RESET}")
    return books, transactions

def view_issued_books(transactions):
    print_header("Currently Issued Books", Color.BLUE)
    issued = [t for t in transactions if t["status"] == "Issued"]
    if not issued:
        print_info("No books currently issued.")
        return
    widths = [9, 20, 18, 12, 12, 8]
    headers = ["TXN ID", "Book", "Student", "Issued", "Due", "Status"]
    print(format_table_top(widths))
    print(format_table_row(headers, widths, Color.BOLD + Color.CYAN))
    print(format_table_separator(widths, "="))
    now = datetime.now()
    for t in issued:
        due = datetime.strptime(t["due_date"], DATE_FORMAT)
        st = f"{Color.RED}OVERDUE" if now > due else f"{Color.GREEN}Active"
        print(format_table_row([t["txn_id"], t["book_title"][:20], t["student_name"][:18],
               t["issue_date"][:10], t["due_date"][:10], st + Color.RESET], widths))
    print(format_table_bottom(widths))

def view_transaction_history(transactions):
    print_header("Transaction History", Color.BLUE)
    if not transactions:
        print_info("No transactions yet.")
        return
    widths = [9, 18, 16, 10, 10, 10, 8, 6]
    headers = ["TXN", "Book", "Student", "Issued", "Due", "Returned", "Status", "Fine"]
    print(format_table_top(widths))
    print(format_table_row(headers, widths, Color.BOLD + Color.CYAN))
    print(format_table_separator(widths, "="))
    for t in transactions:
        ret = t["return_date"][:10] if t["return_date"] else "---"
        c = Color.GREEN if t["status"] == "Returned" else Color.YELLOW
        f_str = f"Rs.{t['fine']}" if t["fine"] > 0 else "---"
        print(format_table_row([t["txn_id"], t["book_title"][:18], t["student_name"][:16],
               t["issue_date"][:10], t["due_date"][:10], ret,
               f"{c}{t['status']}{Color.RESET}", f_str], widths))
    print(format_table_bottom(widths))
    print_info(f"Total: {len(transactions)} | Fines: Rs.{sum(t['fine'] for t in transactions)}")

def overdue_books_alert(transactions):
    print_header("OVERDUE BOOKS ALERT", Color.RED)
    now = datetime.now()
    overdue = []
    for t in transactions:
        if t["status"] == "Issued":
            due = datetime.strptime(t["due_date"], DATE_FORMAT)
            if now > due:
                d = (now - due).days
                overdue.append({**t, "days_overdue": d, "current_fine": d * FINE_PER_DAY})
    if not overdue:
        print_success("No overdue books!")
        return
    widths = [18, 16, 10, 10, 8, 8]
    headers = ["Book", "Student", "Due", "Overdue", "Fine", "ID"]
    print(format_table_top(widths))
    print(format_table_row(headers, widths, Color.BOLD + Color.RED))
    print(format_table_separator(widths, "="))
    for o in overdue:
        print(format_table_row([o["book_title"][:18], o["student_name"][:16],
               o["due_date"][:10], f"{o['days_overdue']}d", f"Rs.{o['current_fine']}",
               o["student_id"]], widths, Color.RED))
    print(format_table_bottom(widths))

def library_statistics(books, students, transactions):
    print_header("Library Statistics Dashboard", Color.CYAN)
    tb = len(books)
    tc = sum(b["quantity"] for b in books) if books else 0
    ta = sum(b["available"] for b in books) if books else 0
    ti = tc - ta
    ts = len(students)
    tt = len(transactions)
    ai = sum(1 for t in transactions if t["status"] == "Issued")
    tr = sum(1 for t in transactions if t["status"] == "Returned")
    tf = sum(t["fine"] for t in transactions)
    now = datetime.now()
    oc = sum(1 for t in transactions if t["status"]=="Issued" and now>datetime.strptime(t["due_date"],DATE_FORMAT))
    print(f"""
  {Color.BOLD}{Color.CYAN}+================================================+
  |          LIBRARY STATISTICS DASHBOARD          |
  +================================================+{Color.RESET}
  {Color.WHITE}|  Total Book Titles     :  {tb:<20}|
  |  Total Copies          :  {tc:<20}|
  |  Available Copies      :  {Color.GREEN}{ta:<20}{Color.WHITE}|
  |  Currently Issued      :  {Color.YELLOW}{ti:<20}{Color.WHITE}|
  |  Overdue Books         :  {Color.RED}{oc:<20}{Color.WHITE}|
  +================================================+
  |  Registered Students   :  {ts:<20}|
  |  Total Transactions    :  {tt:<20}|
  |  Active Issues         :  {ai:<20}|
  |  Total Returns         :  {tr:<20}|
  |  Total Fines Collected :  Rs.{tf:<17}|
  {Color.CYAN}+================================================+{Color.RESET}""")

def category_report(books):
    print_header("Category-wise Report", Color.MAGENTA)
    if not books:
        print_warning("No books.")
        return
    cs = {}
    for b in books:
        c = b["category"]
        if c not in cs: cs[c] = {"count": 0, "total": 0, "avl": 0}
        cs[c]["count"] += 1
        cs[c]["total"] += b["quantity"]
        cs[c]["avl"] += b["available"]
    widths = [18, 8, 10, 10, 10]
    headers = ["Category", "Titles", "Copies", "Avail", "Issued"]
    print(format_table_top(widths))
    print(format_table_row(headers, widths, Color.BOLD + Color.CYAN))
    print(format_table_separator(widths, "="))
    for cat, s in sorted(cs.items()):
        print(format_table_row([cat[:18], s["count"], s["total"], s["avl"], s["total"]-s["avl"]], widths))
    print(format_table_bottom(widths))

def export_report(books, students, transactions):
    print_header("Export Report", Color.GREEN)
    fn = f"library_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    lines = ["=" * 70, "  LIBRARY MANAGEMENT SYSTEM - REPORT",
             f"  Generated: {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}", "=" * 70]
    lines.append("\n[BOOKS]")
    for b in books:
        lines.append(f"  {b['id']} | {b['title']} | {b['author']} | {b['isbn']} | {b['category']} | Qty:{b['quantity']} | Avl:{b['available']}")
    lines.append("\n[STUDENTS]")
    for s in students:
        lines.append(f"  {s['id']} | {s['name']} | {s['email']} | {s['phone']}")
    lines.append("\n[TRANSACTIONS]")
    for t in transactions:
        lines.append(f"  {t['txn_id']} | {t['book_title']} | {t['student_name']} | {t['status']} | Fine:Rs.{t['fine']}")
    lines.append(f"\nTotal Fines: Rs.{sum(t['fine'] for t in transactions)}")
    lines.append("=" * 70)
    with open(fn, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print_success(f"Report exported to: {fn}")

def display_menu(user):
    print(f"""
{Color.CYAN}{Color.BOLD}  +------------------------------------------------------+
  |           LIBRARY MANAGEMENT SYSTEM                  |
  |           Logged in as: {user['full_name']:<28}|
  +------------------------------------------------------+{Color.RESET}
  {Color.WHITE}|                                                      |
  |  {Color.GREEN}[BOOK MANAGEMENT]{Color.WHITE}                                     |
  |    1.  Add Book          4.  Update Book             |
  |    2.  View All Books    5.  Delete Book             |
  |    3.  Search Book                                   |
  |                                                      |
  |  {Color.YELLOW}[ISSUE & RETURN]{Color.WHITE}                                      |
  |    6.  Issue Book        8.  View Issued Books       |
  |    7.  Return Book                                   |
  |                                                      |
  |  {Color.MAGENTA}[STUDENT MANAGEMENT]{Color.WHITE}                                  |
  |    9.  Register Student  10. View All Students       |
  |                                                      |
  |  {Color.BLUE}[REPORTS & ANALYTICS]{Color.WHITE}                                 |
  |   11.  Library Statistics    14. Overdue Alert       |
  |   12.  Category Report       15. Export Report       |
  |   13.  Transaction History                           |
  |                                                      |
  |  {Color.RED} 0.  Exit / Logout{Color.WHITE}                                    |
  |                                                      |
  {Color.CYAN}{Color.BOLD}+------------------------------------------------------+{Color.RESET}""")

def main():
    user = pre_login_menu()
    if not user:
        return
    books = load_json(BOOKS_FILE, [])
    students = load_json(STUDENTS_FILE, [])
    transactions = load_json(TRANSACTIONS_FILE, [])
    while True:
        display_menu(user)
        choice = get_input("\n  Enter Your Choice (0-15): ")
        if   choice == "1":  books = add_book(books)
        elif choice == "2":  view_books(books, transactions)
        elif choice == "3":  search_book(books)
        elif choice == "4":  books = update_book(books)
        elif choice == "5":  books = delete_book(books, transactions)
        elif choice == "6":  books, transactions = issue_book(books, students, transactions)
        elif choice == "7":  books, transactions = return_book(books, students, transactions)
        elif choice == "8":  view_issued_books(transactions)
        elif choice == "9":  students = add_student(students)
        elif choice == "10": view_students(students)
        elif choice == "11": library_statistics(books, students, transactions)
        elif choice == "12": category_report(books)
        elif choice == "13": view_transaction_history(transactions)
        elif choice == "14": overdue_books_alert(transactions)
        elif choice == "15": export_report(books, students, transactions)
        elif choice == "0":
            print(f"""
{Color.GREEN}{Color.BOLD}
    +===========================================================+
    |   Thank you for using Library Management System!          |
    |   Goodbye, {user['full_name'] + '!':<45}|
    +===========================================================+
{Color.RESET}""")
            break
        else:
            print_error("Invalid choice! Enter 0-15.")
        input(f"\n  {Color.DIM}Press Enter to continue...{Color.RESET}")

if __name__ == "__main__":
    main()
