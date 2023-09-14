import pygame
import speech_recognition as sr
import os
import aiml
import spacy
import nltk
from nltk.tokenize import word_tokenize
import win32com.client
import webbrowser
import datetime
import random
import requests
import json
import pyautogui
import keyboard
import pyperclip
from time import sleep
from bs4 import BeautifulSoup
from bardapi import BardCookies
import threading


def CookieScrapper():
    print("")
    webbrowser.open("https://bard.google.com")
    sleep(2)
    pyautogui.click(x=1736, y=50)
    sleep(1)
    pyautogui.click(x=1505, y=84)
    sleep(1)
    keyboard.press_and_release('ctrl + w')
    keyboard.press_and_release('alt + tab')
    print("*The extraction of essential cookies from GoogleBard has been accomplished successfully.*")

    data = pyperclip.paste()

    try:
        json_data = json.loads(data)
        print(
            "*The process of loading cookies has been executed without any issues, and the cookies are now successfully integrated into the system.*")
        pass

    except json.JSONDecodeError as e:
        print("*Cookies Loaded Unsuccessfully*")
        print("""*The error has been identified as a result of unsuccessful cookie replication from the Chrome extension, 
        which is causing a disruption in the intended functionality.*""")

    SID = "__Secure-1PSID"
    TS = "__Secure-1PSIDTS"
    CC = "__Secure-1PSIDCC"

    try:
        SIDValue = next((item for item in json_data if item["name"] == SID), None)
        TSValue = next((item for item in json_data if item["name"] == TS), None)
        CCValue = next((item for item in json_data if item["name"] == CC), None)
    except Exception as e:
        print(f"Exception Occured {e}")

    if SIDValue is not None:
        SIDValue = SIDValue["value"]
    else:
        print(f"{SIDValue} not found in the JSON data.")

    if TSValue is not None:
        TSValue = TSValue["value"]
    else:
        print(f"{TSValue} not found in the JSON data.")

    if CCValue is not None:
        CCValue = CCValue["value"]
    else:
        print(f"{CCValue} not found in the JSON data.")

    cookie_dict = {
        "__Secure-1PSID": SIDValue,
        "__Secure-1PSIDTS": TSValue,
        "__Secure-1PSIDCC": CCValue,
    }

    return cookie_dict


def update_aiml_knowledge_base(user_input, response, knowledge_base_file, user_profile_file):
    kernel = aiml.Kernel()
    kernel.bootstrap(learnFiles=knowledge_base_file)

    # Create a new AIML category with the provided user input (pattern) and response (template)
    new_category = f"<category><pattern>{user_input}</pattern><template>{response}</template></category>"

    # Append the new category to the AIML file
    with open(knowledge_base_file, "a") as f:
        f.write(new_category)

    # Update the user's profile with hobbies
    user_hobbies = input("User hobbies: ").split(',')
    user_profile = load_user_profile(user_profile_file)
    user_profile["hobbies"] = user_hobbies
    save_user_profile(user_profile, user_profile_file)

    print(f"Updated AIML knowledge base with: User Input='{user_input}', Response='{response}'")


def load_user_profile(user_profile_file):
    try:
        with open(user_profile_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_user_profile(user_profile, user_profile_file):
    with open(user_profile_file, 'w') as file:
        json.dump(user_profile, file, indent=4)


nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Voice = speaker.GetVoices("gender=female")[0]


def process_query(query):
    # Tokenize and analyze the query
    doc = nlp(query)

    # Extract entities, parts of speech, etc., from the parsed query
    entities = [ent.text for ent in doc.ents]
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']

    return entities, nouns


def tokenize(text):
    return word_tokenize(text)


def say(text):
    speaker.Speak(text)


def play_folder_music():
    pygame.mixer.init()
    folder_path = "D:/Musics/"
    try:
        while True:
            # Get a list of all files in the folder
            audio_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

            if not audio_files:
                print("No MP3 files found in the folder.")
                return

            # Select a random audio file from the list
            random_audio_file = random.choice(audio_files)

            # Construct the full path to the selected audio file
            music_path = os.path.join(folder_path, random_audio_file)

            # Load and play the selected audio file
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

            print(f"Now playing: {music_path}")

            # Initialize the command variable
            command = ""

            # Set an event for the end of the music
            pygame.mixer.music.set_endevent(pygame.USEREVENT)

            # Wait for the music to finish playing or for a command
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening for commands...")
                    audio = r.listen(source)

                try:
                    command = r.recognize_google(audio).lower()
                    print(f"Recognized command: {command}")

                    if "stop" in command or "quit" in command:
                        pygame.mixer.music.stop()
                        print("Music stopped.")
                        return

                    # Volume control, maximum volume, and minimum volume (same as before)
                    if "volume up" in command:
                        pygame.mixer.music.set_volume(min(1.0, pygame.mixer.music.get_volume() + 0.1))
                        say("Volume increased.")

                    if "volume down" in command:
                        pygame.mixer.music.set_volume(max(0.0, pygame.mixer.music.get_volume() - 0.1))
                        say("Volume decreased.")

                    if "max volume" in command:
                        pygame.mixer.music.set_volume(1.0)
                        say("Maximum volume set.")

                    if "minimum volume" in command:
                        pygame.mixer.music.set_volume(0.0)
                        say("Minimum volume set.")

                    # Next song
                    if "next song" in command or "next" in command or "next one" in command:
                        pygame.mixer.music.stop()
                        break  # Exit the inner loop to go to the next song

                    # Pause and play (same as before)
                    if "pause" in command:
                        pygame.mixer.music.pause()
                        print("Music paused.")
                    elif "play" in command:
                        pygame.mixer.music.unpause()
                        print("Music resumed.")

                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Could not request results: {e}")

    except Exception as e:
        print(f"Error while playing music: {e}")


def fetch_news_updates():
    news_url = "https://www.bbc.co.uk/news/technology"

    try:
        response = requests.get(news_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_headlines = soup.find_all('h3', class_="gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text")

            if news_headlines:
                # Randomly select a headline
                random_headline = random.choice(news_headlines)

                # Get the text content of the selected headline
                headline_text = random_headline.text
                say(headline_text)
            else:
                print("No headlines found on the page.")

        else:
            print("Failed to fetch news. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Error fetching news:", str(e))


def ask_about_hobbies(user_profile):
    if "hobbies" in user_profile:
        user_hobbies = user_profile["hobbies"]
        say(f"I know you're interested in {', '.join(user_hobbies)}.")
    else:
        say("I'd love to know more about your hobbies. What are some of your favorite hobbies or interests?")
        user_hobbies = input("User hobbies: ").split(',')
        user_profile["hobbies"] = user_hobbies
        save_user_profile(user_profile, user_profile_file)
        say(f"Thanks for sharing! I'm interested in {random.choice(user_hobbies)} too.")


def load_custom_commands(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def maps(location):
    google_maps_url = f"https://www.google.com/maps/search/?q={location}"
    webbrowser.open(google_maps_url)
    say(f"Opening {location} in Google Maps. Is there anything else I can assist you with?")


def greet_user():
    personalities = {
        "friendly": "Hey Vishwa!",
        "cheerful": "I hope you're having a fantastic day!",
        "professional": "So"
    }
    selected_personality = random.choice(list(personalities.keys()))

    try:
        if selected_personality == "friendly":
            speaker.Rate = 1
        elif selected_personality == "cheerful":
            speaker.Rate = 2
        elif selected_personality == "professional":
            speaker.Rate = 0.8

        greeting_text = personalities[selected_personality]
        time = int(datetime.datetime.now().hour)

        if 0 <= time < 11:
            say("Good Morning")
        elif 11 <= time < 12:
            say("Good Noon")
        elif 12 <= time < 15:
            say("Good Afternoon")
        else:
            say("Good Evening")

        speaker.Speak(greeting_text)
    except Exception as e:
        print(f"Error during greeting: {e}")


def get_interesting_fact():
    interesting_facts = [
        {
            "keyword": "fact",
            "content": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible."
        },
        {
            "keyword": "story",
            "content": "Once upon a time in a faraway land, there was a brave knight who embarked on a quest to rescue a captured princess from a fearsome dragon."
        },
        {
            "keyword": "fact",
            "content": "The Great Wall of China is not a single continuous wall but a series of walls and fortifications. It stretches over 13,000 miles and was built over many centuries to protect against invasions."
        },
        {
            "keyword": "story",
            "content": "In a magical forest, there lived a talking tree named Elderwood. Elderwood was the keeper of ancient wisdom and had witnessed the passing of countless seasons and generations of creatures."
        },
        {
            "keyword": "fact",
            "content": "A group of flamingos is called a 'flamboyance.' These vibrant birds are known for their striking pink plumage and are often seen wading in shallow waters."
        },
        {
            "keyword": "story",
            "content": "Long ago, in a hidden valley, there was a secret garden where the flowers sang melodies and the butterflies told tales. It was said that those who discovered the garden would be granted a single wish."
        },
        {
            "keyword": "fact",
            "content": "The oldest known living tree is a Great Basin bristlecone pine called 'Methuselah.' It's estimated to be over 4,800 years old, making it one of the oldest living organisms on Earth."
        },
        {
            "keyword": "story",
            "content": "In the heart of the ocean, there existed a city of merfolk who lived in harmony with the creatures of the deep. One day, a curious human explorer stumbled upon their world and discovered its wonders."
        },
        {
            "keyword": "fact",
            "content": "Octopuses have three hearts. Two pump blood to the gills, while the third pumps oxygenated blood to the rest of the body. This unique circulatory system helps them survive in various aquatic environments."
        },
        {
            "keyword": "story",
            "content": "In a bustling futuristic city, there was a robot named Spark who dreamed of becoming an artist. Despite facing skepticism from other robots, Spark embarked on a journey to prove that robots could create art."
        },
        {
            "keyword": "fact",
            "content": "The Mona Lisa, painted by Leonardo da Vinci, is considered one of the most famous paintings in the world. It's displayed in the Louvre Museum in Paris and attracts millions of visitors annually."
        },
        {
            "keyword": "story",
            "content": "In a far-off galaxy, there was a planet where time flowed backward. The inhabitants aged in reverse, and their memories were of the future. This unique world held many mysteries."
        },
        {
            "keyword": "fact",
            "content": "A day on Venus is longer than its year. Venus rotates very slowly on its axis, taking about 243 Earth days to complete one rotation, while it only takes about 225 Earth days to orbit the Sun."
        },
        {
            "keyword": "story",
            "content": "Deep in the Amazon rainforest, a tribe of indigenous people possessed the knowledge of healing plants that could cure almost any ailment. They guarded this sacred knowledge with great care."
        },
        {
            "keyword": "fact",
            "content": "The world's largest desert is not the Sahara, but Antarctica. Although we often associate deserts with sand dunes, Antarctica is classified as a desert because it receives very little precipitation."
        },
        {
            "keyword": "story",
            "content": "In a quaint little village nestled in the mountains, there lived a wise old sage who was said to possess the power of granting one wish to anyone who could pass his test. Many sought his counsel, but only those with pure hearts succeeded in their quest for a wish."
        },
        {
            "keyword": "fact",
            "content": "Bananas are berries, but strawberries are not! Botanically speaking, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh. Bananas fit this definition, while strawberries, which have their seeds on the outside, do not."
        },
        {
            "keyword": "story",
            "content": "In a bustling metropolis, there was a street musician who played a worn-out violin with unmatched passion. His music had the power to make people stop in their tracks and forget their worries, even if just for a moment. Little did they know, the violin had a magical history that spanned centuries."
        },
        {
            "keyword": "fact",
            "content": "The Eiffel Tower in Paris, France, is made of iron, and it can actually be 15 centimeters taller during the summer months due to the expansion of the iron in the heat."
        },
        {
            "keyword": "story",
            "content": "In a remote village by the sea, there was a lighthouse keeper who had a peculiar habit of collecting seashells. Each shell had a story, and the keeper could hear whispers of the sea within them."
        },
        {
            "keyword": "fact",
            "content": "Polar bears are excellent swimmers and have been known to swim for long distances in search of food. They are well adapted to their cold Arctic environment, with thick fur and layers of blubber to keep them warm."
        },
        {
            "keyword": "story",
            "content": "In a futuristic society where books were banned, a group of rebels known as 'The Literati' secretly preserved and shared the world's literature. Their underground library held the key to preserving knowledge and freedom."
        },
        {
            "keyword": "fact",
            "content": "The Amazon River is the second-longest river in the world, after the Nile. It flows through nine South American countries and is home to an incredibly diverse ecosystem, including thousands of species of fish."
        },
        {
            "keyword": "story",
            "content": "In a land where time was frozen, there was a clockmaker who sought to create a timepiece that could break the spell and restore the flow of time. His journey led him to unexpected places and revelations."
        },
        {
            "keyword": "fact",
            "content": "The hummingbird is the only bird that can fly backward. Their wings move in a figure-eight pattern, allowing them to hover in mid-air and even fly in reverse."
        },
        {
            "keyword": "story",
            "content": "In a hidden valley, there was a village where every resident had a unique superpower. From telekinesis to shape-shifting, their abilities were as diverse as their personalities. They lived in harmony and protected their secret from the outside world."
        },
        {
            "keyword": "fact",
            "content": "The deepest part of the ocean is the Mariana Trench, and its deepest point, known as the Challenger Deep, reaches a depth of approximately 36,070 feet (10,994 meters). It's one of the most mysterious and least explored places on Earth."
        },
        {
            "keyword": "story",
            "content": "In a land of eternal twilight, there was a flower that only bloomed once every hundred years. Its petals emitted a soft, enchanting glow, and those who witnessed its beauty were said to gain extraordinary wisdom."
        },
        {
            "keyword": "fact",
            "content": "The platypus, native to Australia, is one of the few mammals that lay eggs instead of giving birth to live young. It's also known for its unique combination of features, including a duck-like bill and webbed feet."
        },
        {
            "keyword": "story",
            "content": "In a world where dreams were tangible, people could visit a marketplace in their sleep to buy and trade dreams. Some dreams were precious, while others were mundane, but all held the power to shape reality."
        },
        {
            "keyword": "fact",
            "content": "The Sahara Desert wasn't always a desert. Thousands of years ago, it was a lush, green region with rivers and lakes. Climate change gradually transformed it into the arid desert we know today."
        },
        {
            "keyword": "story",
            "content": "In a forgotten corner of the galaxy, there was a planet where the inhabitants communicated through dance instead of words. Their elaborate dance routines conveyed emotions, stories, and even scientific discoveries."
        },
        {
            "keyword": "fact",
            "content": "A single bolt of lightning can heat the air around it to temperatures five times hotter than the sun's surface. Lightning is a powerful natural phenomenon that can have devastating effects."
        },
        {
            "keyword": "story",
            "content": "In a land of floating islands, there was a young inventor who built wings of feathered steel. With these wings, he soared among the islands, exploring hidden realms and uncovering the secrets of the sky."
        },
        {
            "keyword": "fact",
            "content": "The longest hiccuping spree on record lasted for 68 years. Charles Osborne, an American man, hiccuped continuously from 1922 to 1990."
        },
        {
            "keyword": "story",
            "content": "In a futuristic city with no pollution, there was a park where holographic animals roamed freely. Children visited to learn about extinct species and the importance of conservation."
        },
        {
            "keyword": "fact",
            "content": "The world's smallest mammal is the bumblebee bat, which is native to parts of Thailand and Myanmar. It has a wingspan of just a few inches and is about the size of a large bumblebee."
        },
        {
            "keyword": "story",
            "content": "In a time when music had the power to shape reality, there was a musician whose melodies could heal the sick and mend broken hearts. His songs were sought after by kings and paupers alike."
        },
        {
            "keyword": "fact",
            "content": "Cows have best friends, and they often form close bonds with other cows in their herd. When separated from their friends, cows can become stressed and anxious."
        },
        {
            "keyword": "story",
            "content": "In a parallel universe, there existed a planet where gravity worked in reverse. People floated above the ground, and trees grew upside down, with their roots reaching for the sky."
        },
        {
            "keyword": "fact",
            "content": "The world's largest snowflake ever recorded was 15 inches (38 cm) wide and 8 inches (20 cm) thick. It fell in Montana, USA, in 1887."
        },
        {
            "keyword": "story",
            "content": "In a post-apocalyptic world, there was a group of storytellers who roamed the barren landscapes, preserving the tales of the past and bringing hope to those who had lost everything."
        },
        {
            "keyword": "fact",
            "content": "Penguins are excellent swimmers but are not equipped to fly. Instead of wings, they have flippers that allow them to glide gracefully through the water."
        },
        {
            "keyword": "story",
            "content": "In a land where shadows had a life of their own, a shadow puppeteer discovered a way to bring shadow creatures to life. His performances mesmerized audiences, but they also attracted the attention of dark forces."
        },
        {
            "keyword": "fact",
            "content": "The longest recorded flight of a chicken is 13 seconds. Chickens are not built for sustained flight due to their heavy bodies and small wings."
        },
        {
            "keyword": "story",
            "content": "In a city where everyone had the ability to teleport, a young girl discovered a hidden dimension accessible only through her unique teleportation. She became the bridge between two worlds, forging unexpected friendships."
        }
    ]
    random_fact = random.choice(interesting_facts)
    return random_fact["content"]


def get_joke():
    try:
        api_urls = [
            "https://v2.jokeapi.dev/joke/Any",
            "https://official-joke-api.appspot.com/jokes/random",
            "https://icanhazdadjoke.com/",
            "https://jokester-api.herokuapp.com/",
            "https://geek-jokes.sameerkumar.website/api",
        ]

        # Select a random API URL
        joke_api_url = random.choice(api_urls)

        headers = {
            "Accept": "application/json",
            "User-Agent": "Your User Agent (optional)",
        }

        response = requests.get(joke_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was not successful
        joke_data = response.json()

        if "joke" in joke_data:
            return joke_data["joke"]
        elif "setup" in joke_data and "punchline" in joke_data:
            return f"{joke_data['setup']} {joke_data['punchline']}"
        else:
            return "I couldn't fetch a joke at the moment."

    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke: {e}")
        return "I'm sorry, I couldn't fetch a joke at the moment."


def play_quiz():
    quiz_questions = [
        {
            "question": "What is the largest mammal on Earth?",
            "choices": ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Polar Bear"],
            "correct_answer": "B"
        },
        {
            "question": "Which gas do plants absorb from the atmosphere during photosynthesis?",
            "choices": ["A. Oxygen", "B. Carbon Dioxide", "C. Nitrogen", "D. Hydrogen"],
            "correct_answer": "B"
        },
        {
            "question": "Who wrote the play 'Romeo and Juliet'?",
            "choices": ["A. William Shakespeare", "B. Charles Dickens", "C. Jane Austen", "D. Mark Twain"],
            "correct_answer": "A"
        },
        {
            "question": "What is the chemical symbol for gold?",
            "choices": ["A. Go", "B. Ag", "C. Ge", "D. Au"],
            "correct_answer": "D"
        },
        {
            "question": "Which famous scientist formulated the theory of general relativity?",
            "choices": ["A. Isaac Newton", "B. Albert Einstein", "C. Galileo Galilei", "D. Stephen Hawking"],
            "correct_answer": "B"
        },
        {
            "question": "In which year did Christopher Columbus first arrive in the Americas?",
            "choices": ["A. 1492", "B. 1588", "C. 1776", "D. 1607"],
            "correct_answer": "A"
        },
        {
            "question": "What is the chemical symbol for water?",
            "choices": ["A. H2O", "B. CO2", "C. O2", "D. NaCl"],
            "correct_answer": "A"
        },
        {
            "question": "Which country is known as the Land of the Rising Sun?",
            "choices": ["A. China", "B. South Korea", "C. Japan", "D. Thailand"],
            "correct_answer": "C"
        },
        {
            "question": "What is the largest organ in the human body?",
            "choices": ["A. Heart", "B. Brain", "C. Skin", "D. Liver"],
            "correct_answer": "C"
        },
        {
            "question": "Who painted the Mona Lisa?",
            "choices": ["A. Vincent van Gogh", "B. Leonardo da Vinci", "C. Pablo Picasso", "D. Michelangelo"],
            "correct_answer": "B"
        },
        {
            "question": "Which gas makes up the majority of Earth's atmosphere?",
            "choices": ["A. Oxygen", "B. Nitrogen", "C. Carbon Dioxide", "D. Hydrogen"],
            "correct_answer": "B"
        },
        {
            "question": "What is the chemical symbol for iron?",
            "choices": ["A. I", "B. Ir", "C. Fe", "D. In"],
            "correct_answer": "C"
        },
        {
            "question": "Who wrote the novel 'Pride and Prejudice'?",
            "choices": ["A. Charlotte Brontë", "B. Jane Austen", "C. Emily Brontë", "D. F. Scott Fitzgerald"],
            "correct_answer": "B"
        },
        {
            "question": "What is the tallest mountain in the world?",
            "choices": ["A. Mount Kilimanjaro", "B. Mount Everest", "C. Mount Fuji", "D. Mount McKinley"],
            "correct_answer": "B"
        },
        {
            "question": "Which gas do humans exhale when they breathe out?",
            "choices": ["A. Oxygen", "B. Carbon Dioxide", "C. Nitrogen", "D. Hydrogen"],
            "correct_answer": "B"
        },
        {
            "question": "Who is known as the Father of Modern Physics?",
            "choices": ["A. Isaac Newton", "B. Galileo Galilei", "C. Albert Einstein", "D. Stephen Hawking"],
            "correct_answer": "C"
        },
        {
            "question": "Which planet is often called the 'Evening Star' or 'Morning Star'?",
            "choices": ["A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"],
            "correct_answer": "A"
        },
        {
            "question": "What is the chemical symbol for silver?",
            "choices": ["A. Si", "B. S", "C. Ag", "D. Sr"],
            "correct_answer": "C"
        },
        {
            "question": "Who wrote the play 'Hamlet'?",
            "choices": ["A. William Wordsworth", "B. William Shakespeare", "C. William Faulkner", "D. William Blake"],
            "correct_answer": "B"
        },
        {
            "question": "Which gas is responsible for the Earth's ozone layer?",
            "choices": ["A. Oxygen", "B. Hydrogen", "C. Carbon Dioxide", "D. Ozone"],
            "correct_answer": "D"
        },
        # Add more questions and answers as needed
    ]

    random.shuffle(quiz_questions)
    score = 0

    for question_data in quiz_questions:
        question = question_data["question"]
        choices = question_data["choices"]
        correct_answer = question_data["correct_answer"]

        say(question)
        for choice in choices:
            say(choice)

        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        if user_answer == correct_answer:
            say("Correct!")
            score += 1
        else:
            say(f"Sorry, the correct answer is {correct_answer}.")

    say(f"You scored {score} out of {len(quiz_questions)}.")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            return query
        except sr.WaitTimeoutError:
            return "TimeoutError"  # Handle timeout error
        except sr.UnknownValueError:
            return "UnknownValueError"  # Handle unrecognized speech
        except Exception as e:
            print(f"Error: {e}")
            return "Error"


if __name__ == "__main__":
    user_profile_file = "user_profiles.json"
    user_profile = load_user_profile(user_profile_file)
    greet_user()
    print("Listening...")
    speaker.Speak("How can i assist you Today?")
    while True:
        query = takeCommand()

        if "Hey".lower() in query.lower() or "write me".lower() in query.lower() or "Hey".lower() in query.lower():
            cookie_dict = CookieScrapper()
            try:
                bard = BardCookies(cookie_dict=cookie_dict)
            except Exception as e:
                if "SNlM0e value not found" in str(e):
                    # Handle the missing value error here
                    print("SNlM0e value not found in response. Check __Secure-1PSID value.")
                else:
                    # Handle other exceptions if needed
                    print("An error occurred:", str(e))
            reply = bard.get_answer(query)['content']
            response = reply.split('\n')
            query = query.lower()
            words = query.split()
            from_index = words.index("to") if "to".lower() in words else 0
            last_index = words.index("last") if "last".lower() in words else len(words)
            file_name_words = words[from_index + 1:last_index]
            filename = 'To' + ''.join([word.capitalize() for word in file_name_words])
            file_path = filename + '.md'
            with open(file_path, 'w') as file:
                file.write(reply)
            say(response[0])
            say(response[-1])
        elif "Who is".lower() in query.lower():
            reply = bard.get_answer(query)['content']
            response = reply.split('\n')
            query = query.lower()
            words = query.split()
            from_index = words.index("is") if "is".lower() in words else 0
            last_index = words.index("last") if "last".lower() in words else len(words)
            file_name_words = words[from_index + 1:last_index]
            filename = ''.join([word.capitalize() for word in file_name_words])
            file_path = filename + '.md'
            with open(file_path, 'w') as file:
                file.write(reply)
            say(response[0:3])

        elif "Who am I".lower() in query.lower() or "myself".lower() in query.lower():
            say("You are Vishwa, My Developer. Thanks for developing me.")

        sites = [["youtube", "https://www.youtube.com/"], ["google", "https://www.google.com/"],
                 ["portfolio", "https://Aditya-Vishwa.github.io/My-Portfolio"],
                 ["instagram", "https://www.instagram.com/"], ["canva", "https://www.canva.com/"],
                 ["meet", "https://meet.google.com/"], ["classroom", "https://classroom.google.com/"],
                 ["mail", "https://mail.google.com/"], ["twitter", "https://www.twitter.com/"],
                 ["GitHub", "https://www.github.com/"]]

        apps = [["chrome", "chrome.exe"], ["file", "explorer.exe"], ["notepad", "notepad.exe"], ["code", "code"],
                ["discord", "C:/Users/vishw/AppData/Local/Discord/Update.exe --processStart Discord.exe"], []]

        bye = ["quit", "done", "exit", "end", "break", "you are free", "bye", "bye-bye", "free", "close", "no",
               "thankyou","thank","thank-you"]

        try:

            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"I am opening {site[0]}")
                    webbrowser.open(site[1])

            for app in apps:
                # if f"open {app[0]}".lower() in query.lower():
                if len(app) > 0 and f"open {app[0]}".lower() in query.lower():
                    say(f"Opening {app[0]} for you.")
                    os.system(f"start {app[1]}")

            if "My Favourite".lower() in query.lower():
                user_input = query.upper()
                response = "Thanks for telling me your Fancy"
                knowledge_base_file = "knowledge.aiml"
                update_aiml_knowledge_base(user_input, say({response}), knowledge_base_file, user_profile_file)
                break
            elif "play songs" in query.lower():
                play_folder_music()
            elif "interesting" in query.lower() or "tell me something" in query.lower() or "story" in query.lower():
                response = get_interesting_fact()
                speaker.Rate = 0.5
                say(response)
            elif "play quiz" in query.lower():
                play_quiz()
            elif "tell me a joke" in query.lower() or "jokes" in query.lower():
                joke = get_joke()
                if joke:
                    speaker.Rate = 0.5
                    say(joke)
                else:
                    say("I'm sorry, I couldn't fetch a joke at the moment. Here's one from my collection instead:")
                    say(get_joke())
            elif "hobbies" in query.lower():
                ask_about_hobbies()
            elif "time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Vishwa, it's {strfTime}. Is there anything else you'd like to know?")
            elif "news" in query.lower():
                fetch_news_updates()
            elif "where is" in query.lower():
                location = query
                place = location.split()
                if place:
                    last_word = place[-1]
                else:
                    last_word = None
                maps(last_word)
            elif "who are you" in query.lower() or "what are you" in query.lower() or "who" in query.lower() or "hu r u" in query.lower() or "what r u" in query.lower() or "hu" in query.lower():
                say("""
                Hello Sir! I am Elly a dedicated AI assistant, 
                designed and developed by Vishwa to enhance your daily life. 
                With a blend of intelligence and personality, 
                I am your reliable companion for a wide range of tasks and interactions. 
                Whether you need assistance with organizing your schedule, answering questions, or simply engaging in friendly conversations, 
                I am always at your service. With my intuitive understanding and adaptability, 
                I am here to make your life easier and more enjoyable.
                """)
            elif "good morning" in query.lower():
                greet_user()
                takeCommand()
            elif "good afternoon" in query.lower():
                greet_user()
                takeCommand()
            elif "good evening" in query.lower():
                greet_user()
                takeCommand()
            elif "good night" in query.lower():
                say("Good Night, Vishwa")
                break

            elif f"{query}".lower() in bye:
                say("Take Care Vishwa, I am always here to help you.")
                break
            else:
                print(f"{query}")
                say("Feel free to ask anything.")

        except Exception as e:

            print("listening again...")
            print(f"{query}")
            say("Currently, I am in development phase that's why a little limitations, Know.")
