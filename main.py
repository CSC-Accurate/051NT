import requests
import json
import sys
import os
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, firestore

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Initialize Firebase
try:
    # Yeh line serviceAccountKey.json file ko load karta hai
    cred = credentials.Certificate("serviceAccountKey.json")
    # Aapka project ID yahan use ho raha hai
    firebase_admin.initialize_app(cred, {
        'projectId': 'accurate-d86a6',
    })
    db = firestore.client()
    print(GREEN + "Firebase connected successfully!" + RESET)
except Exception as e:
    print(RED + f"Firebase connection failed: {str(e)}" + RESET)
    print(YELLOW + "Please check:" + RESET)
    print(YELLOW + "1. serviceAccountKey.json file is in the same folder." + RESET)
    print(YELLOW + "2. Project ID 'accurate-d86a6' is correct." + RESET)
    sys.exit(1)

def generate_key():
    """Nayi key banata hai"""
    return str(uuid.uuid4())[:8].upper()

def create_new_key():
    """Firebase mein nayi key banake save karta hai"""
    new_key = generate_key()
    
    # Firebase mein key save karte hain
    key_ref = db.collection('keys').document(new_key)
    key_ref.set({
        'key': new_key,
        'used': False,
        'created_at': datetime.now(),
        'created_by': 'admin'
    })
    
    return new_key

def validate_key(key):
    """Check karta hai ki key valid hai ya nahi"""
    # Admin key check karta hai
    if key == "Ashish-Yadav-001":
        return "admin"
    
    # Firebase se regular key check karta hai
    try:
        key_ref = db.collection('keys').document(key)
        key_doc = key_ref.get()
        
        if key_doc.exists:
            key_data = key_doc.to_dict()
            if not key_data['used']:
                # Key ko used mark kar deta hai
                key_ref.update({
                    'used': True,
                    'used_at': datetime.now()
                })
                return "valid"
    except Exception as e:
        print(RED + f"Error validating key: {str(e)}" + RESET)
    
    return "invalid"

def get_phone_info(mobile):
    """Phone number ki info fetch karta hai"""
    url = f"https://random-remove-batch-tea.trycloudflare.com/search?mobile={mobile}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Response ko Firebase mein save karta hai (optional)
        response_ref = db.collection('phone_responses').document()
        response_ref.set({
            'mobile': mobile,
            'response': data,
            'timestamp': datetime.now()
        })
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def get_vehicle_info(reg_no):
    """Vehicle ki info fetch karta hai"""
    url = f"https://lingering-forest-532d.mrxrobot.workers.dev/vehicle/{reg_no}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Response ko Firebase mein save karta hai (optional)
        response_ref = db.collection('vehicle_responses').document()
        response_ref.set({
            'reg_no': reg_no,
            'response': data,
            'timestamp': datetime.now()
        })
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def get_aadhar_info(aadhar_no):
    """Aadhar ki info fetch karta hai"""
    url = f"https://devxadi.vercel.app/fetch?key=devxadi2104&aadhaar={aadhar_no}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Response ko Firebase mein save karta hai (optional)
        response_ref = db.collection('aadhar_responses').document()
        response_ref.set({
            'aadhar_no': aadhar_no,
            'response': data,
            'timestamp': datetime.now()
        })
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def print_phone_info(data):
    """Phone info ko print karta hai"""
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
    """Vehicle info ko print karta hai"""
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
    """Aadhar info ko print karta hai"""
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
    """User ke command ko process karta hai"""
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
    """Admin panel ke liye function"""
    print("\n" + "="*50)
    print("ADMIN PANEL")
    print("="*50)
    
    while True:
        print("\nAdmin Options:")
        print("1. Create new key")
        print("2. View all keys")
        print("3. View API usage statistics")
        print("4. Exit admin panel")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            new_key = create_new_key()
            print(f"\nNew key created: {new_key}")
            print(BLUE + "You can share this key with anyone to allow access to the tool." + RESET)
        elif choice == "2":
            print("\nAll Keys:")
            print(f"Admin Key: Ashish-Yadav-001")
            
            # Firebase se saare keys fetch karta hai
            keys_ref = db.collection('keys').order_by('created_at', direction=firestore.Query.DESCENDING)
            keys = keys_ref.stream()
            
            print("\nUser Keys:")
            for i, key_doc in enumerate(keys, 1):
                key_data = key_doc.to_dict()
                status = "Used" if key_data['used'] else "Unused"
                created_at = key_data['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                print(f"{i}. Key: {key_data['key']} - Status: {status} - Created: {created_at}")
                if key_data['used']:
                    used_at = key_data['used_at'].strftime("%Y-%m-%d %H:%M:%S")
                    print(f"   Used at: {used_at}")
        elif choice == "3":
            print("\nAPI Usage Statistics:")
            
            # Phone API usage count karta hai
            phone_responses = db.collection('phone_responses').get()
            print(f"Phone API calls: {len(phone_responses)}")
            
            # Vehicle API usage count karta hai
            vehicle_responses = db.collection('vehicle_responses').get()
            print(f"Vehicle API calls: {len(vehicle_responses)}")
            
            # Aadhar API usage count karta hai
            aadhar_responses = db.collection('aadhar_responses').get()
            print(f"Aadhar API calls: {len(aadhar_responses)}")
            
            total_calls = len(phone_responses) + len(vehicle_responses) + len(aadhar_responses)
            print(f"Total API calls: {total_calls}")
        elif choice == "4":
            print("Exiting admin panel.")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main function jo tool start karta hai"""
    # ASCII art print karta hai
    print(RED + "▄▀█ █▀▀ █▀▀ █░█ █▀█ ▄▀█ ▀█▀ █▀▀")
    print("█▀█ █▄▄ █▄▄ █▄█ █▀▄ █▀█ ░█░ ██▄" + RESET)
    
    # Tool name print karta hai
    print(GREEN + "\nInformation Lookup Tool" + RESET)
    
    print("This tool requires a valid access key.")
    print("Enter /adminlogin to access admin panel")
    print("-" * 50)
    
    # Admin login check karta hai
    command = input("\nEnter command or access key: ")
    
    if command.lower() == "/adminlogin":
        admin_key = input("Enter admin key: ")
        if admin_key == "Ashish-Yadav-001":
            admin_panel()
            return
        else:
            print("Invalid admin key. Access denied.")
            return
    
    # Regular key validate karta hai
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
    
    # Command loop chalta hai
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
