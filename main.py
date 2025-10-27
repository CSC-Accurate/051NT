import requests
import json
import sys
import os
from datetime import datetime
import uuid

# File to store keys
KEYS_FILE = "keys.json"

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def initialize_keys_file():
    """Initialize the keys file if it doesn't exist"""
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'w') as f:
            json.dump({
                "admin_key": "Ashish-Yadav-001",
                "keys": []
            }, f, indent=2)

def load_keys():
    """Load keys from the file"""
    initialize_keys_file()
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys_data):
    """Save keys to the file"""
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys_data, f, indent=2)

def generate_key():
    """Generate a new unique key"""
    return str(uuid.uuid4())[:8].upper()

def create_new_key():
    """Create a new key and add it to the keys file"""
    keys_data = load_keys()
    new_key = generate_key()
    keys_data["keys"].append({
        "key": new_key,
        "used": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_keys(keys_data)
    return new_key

def validate_key(key):
    """Validate if a key is valid and not used"""
    keys_data = load_keys()
    
    # Check if it's the admin key
    if key == keys_data["admin_key"]:
        return "admin"
    
    # Check regular keys
    for key_data in keys_data["keys"]:
        if key_data["key"] == key and not key_data["used"]:
            # Mark the key as used
            key_data["used"] = True
            key_data["used_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_keys(keys_data)
            return "valid"
    
    return "invalid"

def format_json(data, indent=2):
    """Format JSON data in a readable way"""
    return json.dumps(data, indent=indent, ensure_ascii=False)

def get_phone_info(mobile):
    """Fetch phone number information"""
    url = f"https://random-remove-batch-tea.trycloudflare.com/search?mobile={mobile}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def get_vehicle_info(reg_no):
    """Fetch vehicle information"""
    url = f"https://lingering-forest-532d.mrxrobot.workers.dev/vehicle/{reg_no}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def get_aadhar_info(aadhar_no):
    """Fetch Aadhar information"""
    url = f"https://devxadi.vercel.app/fetch?key=devxadi2104&aadhaar={aadhar_no}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def print_phone_info(data):
    """Print phone information in a formatted way"""
    if "error" in data:
        print(f"Error: {data['error']}")
        return
    
    if "data" not in data or not data["data"]:
        print("No data found for this phone number.")
        return
    
    print("\n" + "="*50)
    print("PHONE NUMBER INFORMATION")
    print("="*50)
    
    for i, item in enumerate(data["data"], 1):
        print(f"\nRecord {i}:")
        print(f"Mobile: {item.get('mobile', 'N/A')}")
        print(f"Name: {item.get('name', 'N/A')}")
        print(f"Father's Name: {item.get('fname', 'N/A')}")
        print(f"Address: {item.get('address', 'N/A')}")
        print(f"Alternate: {item.get('alt', 'N/A')}")
        print(f"Circle: {item.get('circle', 'N/A')}")
        if 'email' in item:
            print(f"Email: {item['email']}")

def print_vehicle_info(data):
    """Print vehicle information in a formatted way"""
    if "error" in data:
        print(f"Error: {data['error']}")
        return
    
    if "data" not in data:
        print("No data found for this vehicle number.")
        return
    
    print("\n" + "="*50)
    print("VEHICLE INFORMATION")
    print("="*50)
    
    item = data["data"]
    print(f"\nRegistration Number: {item.get('regNo', 'N/A')}")
    print(f"Vehicle Class: {item.get('vehicleClass', 'N/A')}")
    print(f"Chassis Number: {item.get('chassis', 'N/A')}")
    print(f"Engine Number: {item.get('engine', 'N/A')}")
    print(f"Manufacturer: {item.get('vehicleManufacturerName', 'N/A')}")
    print(f"Model: {item.get('model', 'N/A')}")
    print(f"Color: {item.get('vehicleColour', 'N/A')}")
    print(f"Fuel Type: {item.get('type', 'N/A')}")
    print(f"Owner: {item.get('owner', 'N/A')}")
    print(f"Registration Date: {item.get('regDate', 'N/A')}")
    print(f"Registration Authority: {item.get('regAuthority', 'N/A')}")
    print(f"Insurance Company: {item.get('vehicleInsuranceCompanyName', 'N/A')}")
    print(f"Insurance Valid Until: {item.get('vehicleInsuranceUpto', 'N/A')}")
    print(f"Status: {item.get('status', 'N/A')}")
    print(f"Present Address: {item.get('presentAddress', 'N/A')}")

def print_aadhar_info(data):
    """Print Aadhar information in a formatted way"""
    if "error" in data:
        print(f"Error: {data['error']}")
        return
    
    print("\n" + "="*50)
    print("AADHAR INFORMATION")
    print("="*50)
    
    print(f"\nAddress: {data.get('address', 'N/A')}")
    print(f"Home District: {data.get('homeDistName', 'N/A')}")
    print(f"Home State: {data.get('homeStateName', 'N/A')}")
    print(f"Scheme: {data.get('schemeName', 'N/A')}")
    
    if "memberDetailsList" in data and data["memberDetailsList"]:
        print("\nFamily Members:")
        for i, member in enumerate(data["memberDetailsList"], 1):
            print(f"\nMember {i}:")
            print(f"Name: {member.get('memberName', 'N/A')}")
            print(f"Relationship: {member.get('releationship_name', 'N/A')}")
            print(f"UID Available: {'Yes' if member.get('uid') == 'Yes' else 'No'}")

def process_command(command):
    """Process the command and call the appropriate function"""
    parts = command.strip().split()
    if len(parts) < 3 or parts[0] != "/Info":
        print("Invalid command. Use format: /Info [type] [value]")
        print("Types: number, aadhar, vehicle")
        return
    
    info_type = parts[1].lower()
    value = parts[2]
    
    if info_type == "number":
        print(f"Fetching information for phone number: {value}")
        data = get_phone_info(value)
        print_phone_info(data)
    elif info_type == "aadhar":
        print(f"Fetching information for Aadhar number: {value}")
        data = get_aadhar_info(value)
        print_aadhar_info(data)
    elif info_type == "vehicle":
        print(f"Fetching information for vehicle number: {value}")
        data = get_vehicle_info(value)
        print_vehicle_info(data)
    else:
        print("Invalid information type. Use: number, aadhar, or vehicle")

def admin_panel():
    """Admin panel for managing keys"""
    print("\n" + "="*50)
    print("ADMIN PANEL")
    print("="*50)
    
    while True:
        print("\nAdmin Options:")
        print("1. Create new key")
        print("2. View all keys")
        print("3. Exit admin panel")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            new_key = create_new_key()
            print(f"\nNew key created: {new_key}")
        elif choice == "2":
            keys_data = load_keys()
            print("\nAll Keys:")
            print(f"Admin Key: {keys_data['admin_key']}")
            print("\nUser Keys:")
            for i, key_data in enumerate(keys_data["keys"], 1):
                status = "Used" if key_data["used"] else "Unused"
                print(f"{i}. Key: {key_data['key']} - Status: {status} - Created: {key_data['created_at']}")
                if key_data["used"]:
                    print(f"   Used at: {key_data.get('used_at', 'N/A')}")
        elif choice == "3":
            print("Exiting admin panel.")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main function to run the CLI tool"""
    # Print ASCII art in red color
    print(RED + "▄▀█ █▀▀ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █▀▀")
    print("█▀█ █▄▄ █▄▄ █▄█ █▀▄ █▀█ ░█░ ██▄" + RESET)
    
    # Print tool name in green color
    print(GREEN + "\nInformation Lookup Tool" + RESET)
    
    
    print("-" * 50)
    
    # Check for admin login
    command = input("\nEnter access key: ")
    
    if command.lower() == "/adminlogin":
        admin_key = input("Enter admin key: ")
        if admin_key == "Ashish-Yadav-001":
            admin_panel()
            return
        else:
            print("Invalid admin key. Access denied.")
            return
    
    # Validate regular key
    key_status = validate_key(command)
    
    if key_status == "invalid":
        print("Invalid or already used key. Access denied.")
        return
    
    if key_status == "admin":
        print("Admin key detected. Redirecting to admin panel...")
        admin_panel()
        return
    
    print("Access granted. Key validated successfully.")
    print("\nAvailable commands:")
    print("  /Info number [phone_number]")
    print("  /Info aadhar [aadhar_number]")
    print("  /Info vehicle [vehicle_number]")
    print("  /exit to quit")
    print("-" * 50)
    
    while True:
        try:
            command = input("\nEnter command: ")
            
            if command.lower() == "/exit":
                print("Exiting the tool. Goodbye!")
                break
            
            process_command(command)
        except KeyboardInterrupt:
            print("\nExiting the tool. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
