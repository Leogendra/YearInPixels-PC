from datetime import datetime, timedelta
import glob
import json
import os



# Styles
RESET = "\x1b[0m"  # Reset styles
UNDERLINE = "\x1b[4m"  # Underline text
BOLD = "\x1b[1m"  # Bold text

# Colors
RED = "\x1b[31m"  # Red text
GREEN = "\x1b[32m"  # Green text
YELLOW = "\x1b[33m"  # Yellow text
BLUE = "\x1b[34m"  # Blue text


# Utils
def datetime_to_string(date: datetime) -> str:
    raw_date = date.strftime("%Y-%m-%d")
    # removing the trailing 0's
    if raw_date[8] == "0":
        raw_date = raw_date[:8] + raw_date[9:]
    if raw_date[5] == "0":
        raw_date = raw_date[:5] + raw_date[6:]
    return raw_date


def is_date_valid(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def find_pixel_file() -> str:
    pattern = "*.json"
    files = glob.glob(pattern)
    files.sort()  # Sort the files in ascending order
    if files:
        return files[0]


# Function to load a pixels.json file
def load_pixels() -> list:
    pixel_file = find_pixel_file()
    with open(pixel_file, "r", encoding='utf-8') as f:
        pixels = json.load(f)
    
    return [Pixel(pixel=pixel) for pixel in pixels]
        


def write_to_json(pixels, new_pixel):

    pixel_file = find_pixel_file()
    pixels.append(new_pixel)  # Add the new pixel to the list of pixels

    with open(pixel_file, 'w', encoding='utf-8') as file:
        json.dump(pixels, file, cls=PixelEncoder, ensure_ascii=False, indent=4)

    print("\n> Pixel added to JSON file !\n")



# Color functions
def get_color_of_mood(mood: str) -> str:
    # You can customize your palette here
    if mood == '1':
        return RED
    elif mood == '2':
        return RED
    if mood == '3':
        return YELLOW
    elif mood == '4':
        return GREEN
    elif mood == '5':
        return GREEN
    else:
        return BLUE


def get_aviability(pixels, date: str) -> str:
    return search_pixel_by_date(pixels, date) == "No pixel found"

def get_color_aviability(pixels, date: str) -> str:
    if search_pixel_by_date(pixels, date) == "No pixel found":
        return GREEN
    else:
        return RED



# Search functions
def search_pixel_by_date(pixels, search_date):
    matching_pixels = []
    for pixel in pixels:
        if pixel.date == search_date:
            matching_pixels.append(pixel)
            break
    return matching_pixels[0] if matching_pixels else "No pixel found" # Return the first pixel found instead of printing it because it's used in the get_aviability function


def search_pixel_by_mood(pixels, search_mood):
    matching_pixels = []
    for pixel in pixels:
        if str(pixel.score) == str(search_mood):
            matching_pixels.append(pixel)
    for pixel in (matching_pixels[:number_of_pixels] if matching_pixels else ["No pixel found"]):
        print(pixel)


def search_pixel_by_tag(pixels, search_tag):
    matching_pixels = []
    for pixel in pixels:
        if search_tag in pixel.tags:
            matching_pixels.append(pixel)
    for pixel in (matching_pixels[:number_of_pixels] if matching_pixels else ["No pixel found"]):
        print(pixel)


def search_pixel_by_notes(pixels, search_notes):
    matching_pixels = []
    for pixel in pixels:
        if search_notes in pixel.notes:
            matching_pixels.append(pixel)
    for pixel in (matching_pixels[:number_of_pixels] if matching_pixels else ["No pixel found"]):
        print(pixel)


# Create a pixel
def write_pixel(pixels):

    today = datetime_to_string(datetime.now())
    yesterday = datetime_to_string(datetime.now() - timedelta(days=1))
    day_before_yesterday = datetime_to_string(datetime.now() - timedelta(days=2))
    date = today

    print(UNDERLINE + "Choose the date" + RESET)
    print(get_color_aviability(pixels, today) + f"default. today ({today})" + RESET)
    print(get_color_aviability(pixels, yesterday) + "1. yesterday" + RESET)
    print(get_color_aviability(pixels, day_before_yesterday) + "2. day before yesterday" + RESET)
    print("3. manual")
    choice = input("Your choice: ")

    if choice == "1":
        date = yesterday
    elif choice == "2":
        date = day_before_yesterday
    elif choice == "3":
        date = input("Date (YYYY-MM-DD, without trailing zeros): ")
        while not(is_date_valid(date)):
            date = input("Enter a valid date (YYYY-MM-DD, without trailing zeros): ")

    if not get_aviability(pixels, date):
        print(f"\n{UNDERLINE}The Pixel of this date already exists{RESET}")
        print("Would you like to overwrite it ?")
        choice = input("y/n: ")
        if choice.lower() in ["y", "o", "yes", "oui", "1"]:
            print("Pixel will be overwritten")
        else:
            return


    score = "0"
    while score not in ["1", "2", "3", "4", "5"]:
        score = input(f"\nEnter your {UNDERLINE}mood{RESET} [1-5]: ")

    print()
    notes = ""
    line = "."
    while line != "":
        line = input(f"{UNDERLINE}Notes{RESET} (empty line to stop): ")
        if line != "":
            notes += line + "\n"

    print()
    tags = []
    tag = "."
    while tag != "":
        tag = input(f"{UNDERLINE}Tags{RESET} (empty line to stop): ")
        if tag != "":
            tags.append(tag)

    return Pixel(pixel={"date": date, "type": "Mood", "scores": [score], "notes": notes.strip(), "tags": tags})


class Pixel:

    def __init__(self, pixel: dict = None):
        self.date = pixel["date"]
        self.pixel_type = pixel["type"]
        self.score = pixel["scores"][0]
        self.notes = pixel["notes"]
        self.tags = pixel["tags"]

    def __str__(self):
        MOOD_COLOR = get_color_of_mood(self.score)
        date = f"Pixel Date: {UNDERLINE + self.date + RESET}"
        mood = f"Mood: {MOOD_COLOR}{self.score}{RESET}"
        notes = MOOD_COLOR + f"Notes: {self.notes}" + RESET if self.notes else "no notes"
        tags = f"Tags: {self.tags}" if self.tags else "no tags"
        return f"{date}\n{mood}\n{notes}\n{tags}\n"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, str):
            return False
        return self.__dict__ == other.__dict__

    

    

class PixelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pixel):
            # Create a new dictionary with modified attribute names
            encoded_pixel = {
                "date": obj.date,
                "type": obj.pixel_type,
                "scores": [int(obj.score)],
                "notes": obj.notes,
                "tags": obj.tags
            }
            return encoded_pixel
        return super().default(obj)
    






if __name__ == "__main__":

    try:
        pixels = load_pixels()
    except Exception as exception:
        print("No json file found.\nfull error :", exception)
        exit()

    ##########################
    #          MENU          #
    ##########################

    os.system('cls' if os.name == 'nt' else 'clear')
    print(BOLD + "Welcome to Pixel Writer !" + RESET)

    while True:
        print('='*25)
        print("1. Write a pixel")
        print("2. Search pixel by date")
        print("3. Search pixel by mood")
        print("4. Search pixel by tag")
        print("5. Search pixel by notes")
        print("else. exit")
        choice_menu = input("Choice: ")
        print()

        if choice_menu == "1":
            new_pixel = write_pixel(pixels)
            
            write_to_json(pixels, new_pixel)  # Write the updated pixels list to the JSON file
            
            print(new_pixel)

        elif choice_menu == "2":
            date_to_find = input("Date to find (YYYY-MM-DD): ")
            while not(is_date_valid(date_to_find)):
                date = input("Enter a valid date (YYYY-MM-DD, without trailing zeros): ")
            print(search_pixel_by_date(pixels, date_to_find))

        elif choice_menu == "3":
            mood_to_find = input("Mood to find [1-5]: ")
            number_of_pixels = int(input("Number of pixels: "))
            search_pixel_by_mood(pixels, mood_to_find, number_of_pixels)

        elif choice_menu == "4":
            tag_to_find = input("Tag to find: ")
            number_of_pixels = int(input("Number of pixels: "))
            search_pixel_by_tag(pixels, tag_to_find, number_of_pixels)

        elif choice_menu == "5":
            notes_to_find = input("Notes to find: ")
            number_of_pixels = int(input("Number of pixels: "))
            search_pixel_by_notes(pixels, notes_to_find, number_of_pixels)

        else:
            print("Have a nice day !")
            exit()