import os
import requests
import time
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Define the ASCII art text in red
ascii_art = Fore.RED + """
██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗     ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
███████║ ╚████╔╝ ██║  ██║██████╔╝███████║    ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║    ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║    ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

# Smaller text for the creator name
creator_text = "Created by StevePVPs"

# Function to print the options menu in red
def print_options():
    print(Fore.RED + "1. Webhook Info")
    print(Fore.RED + "2. Webhook Spammer")
    print(Fore.RED + "3. Webhook Deleter")

# Clear screen (optional for smoother appearance)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to ask for user input and return the entered option
def ask_for_option():
    print(ascii_art)
    print(Fore.RED + creator_text)  # Print creator's name in smaller text
    print_options()
    option = input(Fore.RED + "Enter option: ")
    return option

# Function to fetch webhook details from Discord API
def get_webhook_details(url):
    try:
        # Make a GET request to Discord API for webhook info
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for non-2xx responses
        data = response.json()

        # Extracting webhook details
        webhook_name = data['name']
        channel_id = data['channel_id']
        guild_id = data['guild_id']

        return webhook_name, channel_id, guild_id
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error retrieving webhook details: {e}")
        return None, None, None

# Function to send message repeatedly to the webhook
def send_message_to_webhook(webhook_url, message, speed=0.1):
    while True:
        try:
            # Send the message to the webhook
            payload = {'content': message}
            response = requests.post(webhook_url, json=payload)

            if response.status_code == 204:
                print(Fore.RED + "Message sent successfully!")
            elif response.status_code == 429:
                print(Fore.RED + "Rate limited! Try again later.")
                time.sleep(5)  # Delay to avoid spamming rate limit
            elif response.status_code == 404:
                print(Fore.RED + "Webhook not found or deleted.")
                break  # Exit the loop if the webhook is deleted
            else:
                print(Fore.RED + f"Error: {response.status_code} - {response.text}")
            
            time.sleep(speed)  # Delay to send message every 0.1 seconds (adjustable)

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error sending message: {e}")
            break  # Exit the loop if an error occurs

# Function to delete the webhook
def delete_webhook(webhook_url):
    try:
        # Send DELETE request to remove the webhook
        response = requests.delete(webhook_url)

        if response.status_code == 204:
            print(Fore.RED + "Webhook successfully nuked by Hydra!")
        elif response.status_code == 404:
            print(Fore.RED + "Webhook not found or already deleted.")
        else:
            print(Fore.RED + f"Error deleting webhook: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error deleting webhook: {e}")

# Function to return to the main menu after each option
def return_to_menu():
    input(Fore.RED + "Press enter to return to menu...")
    clear_console()
    main()

# Main function to run the menu and handle options
def main():
    # Clear screen and print the menu
    clear_console()
    
    # Ask for the option
    option = ask_for_option()

    # Handle Option 1: Webhook Info
    if option == "1":
        clear_console()  # Clear the console

        # Ask for webhook URL
        webhook_url = input(Fore.RED + "Enter webhook URL: ")

        # Get the webhook details from Discord API
        webhook_name, channel_id, guild_id = get_webhook_details(webhook_url)
        
        if webhook_name and channel_id and guild_id:
            # Print the webhook info in red
            print(Fore.RED + f"Webhook Name: {webhook_name}")
            print(Fore.RED + f"Channel ID: {channel_id}")
            print(Fore.RED + f"Guild ID: {guild_id}")
        else:
            print(Fore.RED + "Failed to retrieve webhook info.")
        
        # Return to menu after completion
        return_to_menu()

    # Handle Option 2: Webhook Spammer
    elif option == "2":
        clear_console()  # Clear the console

        # Ask for webhook URL
        webhook_url = input(Fore.RED + "Enter webhook URL: ")

        # Ask for the message to send
        message = input(Fore.RED + "Enter message: ")

        # Start sending the message to the webhook every 0.1 seconds
        send_message_to_webhook(webhook_url, message, speed=0.1)

        # Return to menu after completion
        return_to_menu()

    # Handle Option 3: Webhook Deleter
    elif option == "3":
        clear_console()  # Clear the console

        # Ask for webhook URL
        webhook_url = input(Fore.RED + "Enter webhook URL: ")

        # Delete the webhook
        delete_webhook(webhook_url)

        # Return to menu after completion
        return_to_menu()

    else:
        print(Fore.RED + "Invalid option selected.")
        return_to_menu()

# Run the main function to start the script
if __name__ == "__main__":
    main()
