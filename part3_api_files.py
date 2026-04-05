 
# -------- PART 3: FILE I/O, APIs & EXCEPTION HANDLING --------

import requests
from datetime import datetime

print("\n========== TASK 1: FILE I/O ==========\n")

# ---- Write to file ----
try:
    with open("python_notes.txt", "w", encoding="utf-8") as f:
        f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
        f.write("Topic 2: Lists are ordered and mutable.\n")
        f.write("Topic 3: Dictionaries store key-value pairs.\n")
        f.write("Topic 4: Loops automate repetitive tasks.\n")
        f.write("Topic 5: Exception handling prevents crashes.\n")
    print("File written successfully.")
except Exception as e:
    print("Error writing file:", e)

# ---- Append ----
try:
    with open("python_notes.txt", "a", encoding="utf-8") as f:
        f.write("Topic 6: Functions help reuse code.\n")
        f.write("Topic 7: APIs allow communication between systems.\n")
    print("Lines appended.")
except Exception as e:
    print("Error appending file:", e)

# ---- Read ----
try:
    with open("python_notes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("\nFile Content:")
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.strip()}")

    print(f"\nTotal lines: {len(lines)}")

    keyword = input("Enter keyword to search: ").lower()
    matches = [line.strip() for line in lines if keyword in line.lower()]

    if matches:
        print("\nMatching Lines:")
        for m in matches:
            print(m)
    else:
        print("No matching lines found.")

except Exception as e:
    print("Error reading file:", e)


# -------- LOGGER FUNCTION --------
def log_error(context, error_type, message):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR in {context}: {error_type} — {message}\n")


print("\n========== TASK 2: API ==========\n")

# ---- Fetch products ----
try:
    url = "https://dummyjson.com/products?limit=20"
    response = requests.get(url, timeout=5)
    data = response.json()

    products = data["products"]

    print("ID | Title | Category | Price | Rating")
    print("-" * 60)

    for p in products:
        print(f"{p['id']} | {p['title'][:20]:<20} | {p['category']:<12} | ${p['price']} | {p['rating']}")

except requests.exceptions.ConnectionError:
    print("Connection failed.")
    log_error("fetch_products", "ConnectionError", "No connection")
except requests.exceptions.Timeout:
    print("Request timed out.")
    log_error("fetch_products", "Timeout", "API timeout")
except Exception as e:
    print("Unexpected error:", e)
    log_error("fetch_products", "Exception", str(e))


# ---- Filter + Sort ----
filtered = [p for p in products if p["rating"] >= 4.5]
filtered.sort(key=lambda x: x["price"], reverse=True)

print("\nFiltered Products (rating >= 4.5):")
for p in filtered:
    print(f"{p['title']} - ${p['price']} - {p['rating']}")


# ---- Category Search ----
try:
    url = "https://dummyjson.com/products/category/laptops"
    response = requests.get(url, timeout=5)
    data = response.json()

    print("\nLaptops:")
    for p in data["products"]:
        print(f"{p['title']} - ${p['price']}")

except Exception as e:
    log_error("category_search", "Exception", str(e))


# ---- POST ----
try:
    url = "https://dummyjson.com/products/add"
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    response = requests.post(url, json=payload, timeout=5)
    print("\nPOST Response:")
    print(response.json())

except Exception as e:
    log_error("post_product", "Exception", str(e))


print("\n========== TASK 3: EXCEPTION HANDLING ==========\n")

# ---- Safe Divide ----
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# ---- Safe File Read ----
def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))


# ---- Input Loop ----
while True:
    user_input = input("\nEnter product ID (1-100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit() or not (1 <= int(user_input) <= 100):
        print("Invalid input.")
        continue

    try:
        url = f"https://dummyjson.com/products/{user_input}"
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", "HTTPError", "404 Not Found")
        else:
            p = response.json()
            print(f"{p['title']} - ${p['price']}")

    except Exception as e:
        log_error("lookup_product", "Exception", str(e))


print("\n========== TASK 4: LOGGING ==========\n")

# ---- Force Connection Error ----
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error("test_connection", "ConnectionError", str(e))

# ---- Force 404 ----
try:
    response = requests.get("https://dummyjson.com/products/999", timeout=5)
    if response.status_code != 200:
        log_error("test_404", "HTTPError", "404 Not Found")
except Exception as e:
    log_error("test_404", "Exception", str(e))


# ---- Print log file ----
print("\nError Log Contents:\n")
try:
    with open("error_log.txt", "r") as f:
        print(f.read())
except Exception as e:
    print("Error reading log:", e)
