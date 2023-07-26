from datetime import datetime, timedelta, date
from styles import *
import glob
import json
import os



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
    

def format_text(text):
    accents = {
        'a': ['à', 'ã', 'á', 'â'],
        'e': ['é', 'è', 'ê', 'ë'],
        'i': ['î', 'ï'],
        'u': ['ù', 'ü', 'û'],
        'o': ['ô', 'ö'],
        '': [' ', '-', '_', '\'', '(', ')', '"']
    }
    text = text.lower()
    for (char, special_chars) in accents.items():
        for special in special_chars:
            text = text.replace(special, char)
    return text


#######################
#     Pixels file     #
#######################

def find_pixel_file():
    pattern = "*.json"
    files = glob.glob(pattern)
    files.sort()  # Trie les fichiers par ordre croissant

    if not files:
        print("No JSON file found in current directory.")
        choice = input("Do you want to create a new JSON file ? (y/n): ")
        if choice.lower() in ["y", "o", "yes", "oui", "1"]:
            pixel_file = "PIXELS-BACKUP-" + datetime_to_string(datetime.now()) + ".json"
            with open(pixel_file, 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
            print(f"\n> JSON file created !\n")
            return pixel_file
        else:
            exit()

    if len(files) == 1:
        return files[0]

    print("Available JSON files:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")

    while True:
        try:
            choice = int(input("Please enter the number of the JSON file you want to choose: "))
            if 1 <= choice <= len(files):
                return files[choice-1]
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a valid number.")



def load_pixels():
    pixel_file = find_pixel_file()
    with open(pixel_file, "r", encoding='utf-8') as f:
        pixels = json.load(f)
    
    return [Pixel(pixel=pixel) for pixel in pixels]


def write_to_json(pixels):

    pixel_file = find_pixel_file()

    with open(pixel_file, 'w', encoding='utf-8') as file:
        json.dump(pixels, file, cls=PixelEncoder, ensure_ascii=False, indent=4)

    print("\n> Pixel added to JSON file !\n")


def merge_pixels_files():
    pattern = "*.json"
    files = glob.glob(pattern)
    if len(files) < 2:
        print("Not enough JSON files to merge.")
        return
    
    # print("Select the first JSON file:")
    # to_merge_1 = find_pixel_file()

    # print("Select the second JSON file:")
    # to_merge_2 = find_pixel_file()
    # while to_merge_2 == to_merge_1:
    #     print("You can't merge a file to itself.")
    #     to_merge_2 = find_pixel_file()

    # # Load the pixels from the 'to_merge_1' file
    # with open(to_merge_1, 'r') as from_file:
    #     pixels_1 = json.load(from_file)

    # # Load the pixels from the 'to_merge_2' file
    # with open(to_merge_2, 'r') as to_file:
    #     pixels_2 = json.load(to_file)

    # # Convert pixel lists to sets for easy comparison
    # dates_in_list1 = {pixel.date for pixel in pixels_1}
    # dates_in_list2 = {pixel.date for pixel in pixels_2}

    # conflicts = []
    # for date1 in dates_in_list1:
    #     if date1 in dates_in_list2:
    #         conflicts.append((search_pixel_by_date(pixels_1, date1), search_pixel_by_date(pixels_2, date1)))

    # if not conflicts:
    #     print(">No conflicts found. Merging files...")
    #     merged_pixels = pixels_1 + pixels_2
    # else:
    #     pixels_dict_1 = {pixel.date: pixel for pixel in pixels_1}
    #     pixels_dict_2 = {pixel.date: pixel for pixel in pixels_2}

    #     print("Conflicts found. Please choose how to handle them:")
    #     print("1. Keep all pixels of the first file.")
    #     print("2. Keep all pixels of the second file.")
    #     print("3. Handle conflicts individually.")

    #     conflict_strategy = input("Your choice: ")
    #     while conflict_strategy not in ["1", "2", "3"]:
    #         conflict_strategy = input("Enter a valid input: ")

    # print(">Merge completed.")


#####################
#      Display      #
#####################


def display_pixels_month(pixels, number_to_display):
    try:
        number_to_display = int(number_to_display)
        if (number_to_display < 1):
            number_to_display = len(pixels)
    except ValueError:
        number_to_display = len(pixels)

    pixels_2_display = pixels.copy()
    pixels_2_display = pixels_2_display[-number_to_display:]

    display_grid = {}

    for pixel in pixels_2_display:
        full_date = pixel.date.split("-")
        year = int(full_date[0])
        month = int(full_date[1])
        day = int(full_date[2])
        dt = date(year, month, day)
        week_number = dt.isocalendar()[1]
        if display_grid.get((year, week_number)) is None:
            display_grid[(year, week_number)] = [0] * 7
        display_grid[(year, week_number)][dt.weekday()] = get_color_of_mood(pixel.score)

    # display the grid
    weeks_sorted = sorted(display_grid.keys())

    for week in weeks_sorted:
        days = display_grid[week]
        for day in days:
            if day == 0:
                print("  ", end='')
            else:
                print(day + PIXEL_CHAR + RESET, end='')
        print()


def display_pixels_year(pixels, number_to_display):
    try:
        number_to_display = int(number_to_display)
        if (number_to_display < 1):
            number_to_display = len(pixels)
    except ValueError:
        number_to_display = len(pixels)

    pixels_2_display = pixels.copy()
    pixels_2_display = pixels_2_display[-number_to_display:]

    display_grid = {}

    for pixel in pixels_2_display:
        date = pixel.date.split("-")
        year = date[0]
        month = date[1]
        day = date[2]
        if display_grid.get((year, month)) is None:
            display_grid[(year, month)] = [0] * 31
        display_grid[(year, month)][int(day)-1] = get_color_of_mood(pixel.score)

    # display the grid
    months_sorted = sorted(display_grid.keys())

    for month in months_sorted:
        days = display_grid[month]
        for day in days:
            if day == 0:
                print("  ", end='')
            else:
                print(day + PIXEL_CHAR + RESET, end='')
        print()



def display_statistics(pixels, number_of_words):
    try:
        number_of_words = int(number_of_words)
        if (number_of_words < 1):
            number_of_words = 5
    except ValueError:
        number_of_words = 5

    pixels_stats = pixels.copy()
    pixels_stats = sorted(pixels_stats, key=lambda pixel: datetime.strptime(pixel.date, "%Y-%m-%d"), reverse=True)


    print(UNDERLINE + "\nGeneral statistics:" + RESET)
    dates = [datetime.strptime(pixel.date, "%Y-%m-%d") for pixel in pixels_stats]
    longest_streak = 1
    last_streak = 1
    for i in range(1, len(dates)):
        if dates[i-1] == dates[i] + timedelta(days=1):
            last_streak += 1
        else:
            last_streak = 0

        if last_streak > longest_streak:
            longest_streak = last_streak

    totals_days = (dates[0] - dates[-1]).days + 1
    days_missed = totals_days - len(pixels_stats)

    print(f"Number of pixels: {len(pixels_stats)}")
    print(f"First pixel: {pixels_stats[-1].date}")
    print(f"Longest streak: {longest_streak}")
    print(f"Current streak: {last_streak}")
    print(f"Number of pixels missed since the first pixel: {days_missed} ({days_missed/totals_days*100:.2f}%)")


    print(UNDERLINE + "\nMood statistics:" + RESET)
    moods_occurence = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    avg_mood = 0
    avg_mood_7 = 0
    avg_mood_30 = 0
    avg_mood_365 = 0

    for i, pixel in enumerate(pixels_stats):
        mood = pixel.score
        moods_occurence[str(mood)] += 1
        if i < 7:
            avg_mood_7 += mood
        if i < 30:
            avg_mood_30 += mood
        if i < 365:
            avg_mood_365 += mood
        avg_mood += mood

    avg_mood = round(avg_mood / len(pixels_stats), 2)
    avg_mood_7 = round(avg_mood_7 / min(len(pixels_stats), 7), 2)
    avg_mood_30 = round(avg_mood_30 / min(len(pixels_stats), 30), 2)
    avg_mood_365 = round(avg_mood_365 / min(len(pixels_stats), 365), 2)

    for mood in range(1, 6):
        MOOD_COLOR = get_color_of_mood(mood)
        print(MOOD_COLOR + f" {mood}: {moods_occurence[str(mood)]}" + RESET)

    print(f"Average mood ({len(pixels_stats)} days): {avg_mood}")
    print(f"Average mood of the last 7 days: {avg_mood_7}")
    print(f"Average mood of the last 30 days: {avg_mood_30}")
    print(f"Average mood of the last 365 days: {avg_mood_365}")
    

    print(UNDERLINE + "\nNotes statistics:" + RESET)
    top_words = {}
    top_words_7 = {}
    top_words_30 = {}
    top_words_365 = {}

    for i, pixel in enumerate(pixels_stats):
        current_words = set()
        note = pixel.notes
        for word in note.split():
            if sum(1 for char in word if char.isalpha()) >= 3:
                cleaned_word = ''.join(char for char in word if char.isalnum())
                current_words.add(cleaned_word)
        for word in current_words:
            for word_key in top_words.keys():
                if word_key.lower() == word.lower():
                    word = word_key
                    break
            top_words[word] = top_words.get(word, 0) + 1
            if i < 7:
                top_words_7[word] = top_words_7.get(word, 0) + 1
            if i < 30:
                top_words_30[word] = top_words_30.get(word, 0) + 1
            if i < 365:
                top_words_365[word] = top_words_365.get(word, 0) + 1
        
    print(f"Top {number_of_words} words:")
    for word, count in sorted(top_words.items(), key=lambda item: item[1], reverse=True)[:number_of_words]:
        print(f" - {word} : {count} ({100 * count / len(pixels_stats):.2f}%)")

    if (len(top_words_7) > 0) and (len(top_words_7) != len(top_words)):
        print(f"Top {number_of_words} words of the last 7 days:")
        for word, count in sorted(top_words_7.items(), key=lambda item: item[1], reverse=True)[:number_of_words]:
            print(f" - {word} : {count} ({100 * count / min(len(pixels_stats), 7):.1f}%)")

    if (len(top_words_30) > 0) and (len(top_words_30) != len(top_words_7)):
        print(f"Top {number_of_words} words of the last 30 days:")
        for word, count in sorted(top_words_30.items(), key=lambda item: item[1], reverse=True)[:number_of_words]:
            print(f" - {word} : {count} ({100 * count / min(len(pixels_stats), 30):.1f}%)")

    if (len(top_words_365) > 0) and (len(top_words_365) != len(top_words_30)):
        print(f"Top {number_of_words} words of the last 365 days:")
        for word, count in sorted(top_words_365.items(), key=lambda item: item[1], reverse=True)[:number_of_words]:
            print(f" - {word} : {count} ({100 * count / min(len(pixels_stats), 365):.1f}%)")


    print(UNDERLINE + "\nTags statistics:" + RESET)
    top_tags = {}
    top_tags_7 = {}
    top_tags_30 = {}
    top_tags_365 = {}

    for i, pixel in enumerate(pixels_stats):
        for tag in pixel.tags:
            for tag_key in top_tags.keys():
                if tag_key.lower() == tag.lower():
                    tag = tag_key
                    break
            top_tags[tag] = top_tags.get(tag, 0) + 1
            if i < 7:
                top_tags_7[tag] = top_tags_7.get(tag, 0) + 1
            if i < 30:
                top_tags_30[tag] = top_tags_30.get(tag, 0) + 1
            if i < 365:
                top_tags_365[tag] = top_tags_365.get(tag, 0) + 1

    number_of_tags = 5
    print(f"Top {number_of_tags} tags:")
    for tag, count in sorted(top_tags.items(), key=lambda item: item[1], reverse=True)[:number_of_tags]:
        print(f" - {tag} : {count} ({100 * count / len(pixels_stats):.1f}%)")

    if (len(top_tags_7) > 0) and (len(top_tags_7) != len(top_tags)):
        print(f"Top {number_of_tags} tags of the last 7 days:")
        for tag, count in sorted(top_tags_7.items(), key=lambda item: item[1], reverse=True)[:number_of_tags]:
            print(f" - {tag} : {count} ({100 * count / min(len(pixels_stats), 7):.1f}%)")

    if (len(top_tags_30) > 0) and (len(top_tags_30) != len(top_tags_7)):
        print(f"Top {number_of_tags} tags of the last 30 days:")
        for tag, count in sorted(top_tags_30.items(), key=lambda item: item[1], reverse=True)[:number_of_tags]:
            print(f" - {tag} : {count} ({100 * count / min(len(pixels_stats), 30):.1f}%)")

    if (len(top_tags_365) > 0) and (len(top_tags_365) != len(top_tags_30)):
        print(f"Top {number_of_tags} tags of the last 365 days:")
        for tag, count in sorted(top_tags_365.items(), key=lambda item: item[1], reverse=True)[:number_of_tags]:
            print(f" - {tag} : {count} ({100 * count / min(len(pixels_stats), 365):.1f}%)")

    print("\n\n")


######################
#       Checks       #
######################

def get_aviability(pixels, date: str) -> str:
    return search_pixel_by_date(pixels, date) == "No pixel found"

def get_color_aviability(pixels, date: str) -> str:
    if search_pixel_by_date(pixels, date) == "No pixel found":
        return GREEN
    else:
        return RED


########################
#   Search functions   #
########################

def search_pixel_by_date(pixels, search_date):
    search_date = datetime_to_string(datetime.strptime(search_date, "%Y-%m-%d"))
    matching_pixels = []
    for pixel in pixels:
        if pixel.date == search_date:
            matching_pixels.append(pixel)
            break

    # Returns the first pixel found instead of printing it because it's used in the get_aviability function    
    return matching_pixels[0] if matching_pixels else "No pixel found" 


def search_pixel_by_mood(pixels, search_mood, number_of_pixels):
    matching_pixels = []
    for pixel in pixels:
        if str(pixel.score) == str(search_mood):
            matching_pixels.append(pixel)
    if len(matching_pixels) > 0:
        print(f"{len(matching_pixels)} pixels found")
        for pixel in matching_pixels[:number_of_pixels]:
            print(pixel)
    else:
        print("No pixel found")


def search_pixel_by_tag(pixels, search_tag, number_of_pixels):
    formated_tag = format_text(search_tag)
    matching_pixels = []
    for pixel in pixels:
        if formated_tag in format_text(pixel.tags):
            matching_pixels.append(pixel)
    if len(matching_pixels) > 0:
        print(f"{len(matching_pixels)} pixels found")
        for pixel in matching_pixels[:number_of_pixels]:
            print(pixel)
    else:
        print("No pixel found")


def search_pixel_by_notes(pixels, search_notes, number_of_pixels):
    formated_notes = format_text(search_notes)
    matching_pixels = []
    for pixel in pixels:
        if formated_notes in format_text(pixel.notes):
            matching_pixels.append(pixel)
    if len(matching_pixels) > 0:
        print(f"{len(matching_pixels)} pixels found")
        for pixel in matching_pixels[:number_of_pixels]:
            print(pixel)
    else:
        print("No pixel found")


########################
#    Create a Pixel    #
########################

def write_pixel(pixels):

    today = datetime_to_string(datetime.now())
    yesterday = datetime_to_string(datetime.now() - timedelta(days=1))
    day_before_yesterday = datetime_to_string(datetime.now() - timedelta(days=2))
    date = today

    ready_to_write = False
    while not ready_to_write:
        print(UNDERLINE + "Choose the date" + RESET)
        print(get_color_aviability(pixels, today) + f"default. today ({today})" + RESET)
        print(get_color_aviability(pixels, yesterday) + "1. yesterday" + RESET)
        print(get_color_aviability(pixels, day_before_yesterday) + "2. day before yesterday" + RESET)
        print("3. manual")
        choice = input("Your choice: ")

        ready_to_write = True
        if choice == "1":
            date = yesterday
        elif choice == "2":
            date = day_before_yesterday
        elif choice == "3":
            date = input("Date (YYYY-MM-DD): ")
            while not(is_date_valid(date)):
                date = input("Enter a valid date (YYYY-MM-DD): ")

        if not get_aviability(pixels, date):
            print(f"\n{UNDERLINE}The Pixel of this date already exists{RESET}")
            print("Would you like to overwrite it ?")
            choice = input("y/n: ")
            if choice.lower() in ["y", "o", "yes", "oui", "1"]:
                print("Pixel will be overwritten")
                # remove the pixel from the list
                pixels = [pixel for pixel in pixels if pixel.date != date]
            else:
                ready_to_write = False


    print()
    score = "0"
    while score not in ["1", "2", "3", "4", "5"]:
        score = input(f"Enter your {UNDERLINE}mood{RESET} [1-5]: ")

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

    new_pixel = Pixel(pixel={"date": date, "type": "Mood", "scores": [score], "notes": notes.strip(), "tags": tags})
    pixels.append(new_pixel)
    print(new_pixel)

    return pixels


class Pixel:

    def __init__(self, pixel: dict = None):
        self.date = pixel["date"]
        self.pixel_type = pixel["type"]
        # self.scores = pixel["scores"] # Not yet implemented
        self.score = pixel["scores"][0]
        self.notes = pixel["notes"]
        self.tags = pixel["tags"][0]["entries"] if pixel["tags"] else []

    def __str__(self):
        MOOD_COLOR = get_color_of_mood(self.score)
        date = f"Pixel Date: {UNDERLINE + self.date + RESET}"
        mood = f"Mood: {MOOD_COLOR}{self.score}{RESET}"
        notes = MOOD_COLOR + f"Notes: {self.notes}" + RESET if self.notes else "no notes"
        tags = f"Tags: {', '.join(self.tags)}" if self.tags else "no tags"
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

    pixels = load_pixels()

    ##########################
    #          MENU          #
    ##########################

    os.system('cls' if os.name == 'nt' else 'clear')
    print(BOLD + " Welcome to YearInPixels PC !" + RESET)

    while True:
        print('='*30)
        print("1. Write a pixel")
        print("2. Search pixel")
        print("3. Display pixels")
        print("4. Statistics")
        # print("5. Merge pixels files") # Not yet implemented
        print("9. About/infos")
        print("other. exit")
        choice_menu = input("Choice: ")
        print()

        if choice_menu == "1":
            pixels = write_pixel(pixels)
            
            write_to_json(pixels)  # Write the updated pixels list to the JSON file

        elif choice_menu == "2":
            print("1. Search by date")
            print("2. Search by notes")
            print("3. Search by mood")
            print("4. Search by tag")
            choice_search = input("Choice: ")
            while choice_search not in ["1", "2", "3", "4"]:
                choice_search = input("Enter a valid input: ")
    
            if choice_search == "1":
                search_prompt = "Date to find (YYYY-MM-DD): "
            elif choice_search == "2":
                search_prompt = "Notes to find: "
                search_func = search_pixel_by_notes
            elif choice_search == "3":
                search_prompt = "Mood to find [1-5]: "
                search_func = search_pixel_by_mood
            elif choice_search == "4":
                search_prompt = "Tag to find: "
                search_func = search_pixel_by_tag

            search_value = input(search_prompt)

            if choice_search == "1":
                while not is_date_valid(search_value):
                    search_value = input("Enter a valid date: ")
                
                print(search_pixel_by_date(pixels, search_value.strip()))

            else:
                try:
                    number_of_pixels = int(input("Number of pixels: "))
                except ValueError:
                    number_of_pixels = 1

                search_func(pixels, search_value.strip(), number_of_pixels)

        elif choice_menu == "3":
            """
            print("1. Grid display")
            # print("2. Calendar display") # Not yet implemented
            choice_display = input("Choice: ")
            """
            number_to_display = input("Number of pixels to display: ")
            display_pixels_year(pixels, number_to_display)

        elif choice_menu == "4":
            number_to_display = input("Number of words to display (notes): ")
            display_statistics(pixels, number_to_display)

        elif choice_menu == "5":
            merge_pixels_files()

        elif choice_menu == "9":
            print("YearInPixels PC")
            print("Version 1.3")
            print("Inspired by an original idea from @nueses_ on Discord.")
            print("Check out the repository for the PC version here: https://github.com/Leogendra/YearInPixels-PC")
            print("Feel free to contribute or report bugs !")

            print("\nUseful informations:")
            print("This program is optimised for fast use, if you don't choose a number in a list, it will take the first value by default.")
            print("You can customize your palette in the styles.py file.")



        else:
            print("Have a nice day !")
            exit()