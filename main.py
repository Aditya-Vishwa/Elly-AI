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
        response = requests.get("https://v2.jokeapi.dev/joke/Any")
        response.raise_for_status()  # Raise an exception if the request was not successful
        joke_data = response.json()
        if joke_data["type"] == "single":
            joke = joke_data["joke"]
        elif joke_data["type"] == "two-part":
            joke = f"{joke_data['setup']} {joke_data['delivery']}"
        else:
            joke = "I couldn't fetch a joke at the moment."
        return joke
    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke from JokeAPI: {e}")
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
        r.pause_threshold = 0.8
        print("Listening...")
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"Recognized: {query}")
            speaker.Speak(f"Vishwa, You Said {query}, So")
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
        if query == "Error":
            say("I'm sorry, an error occurred while processing your request. Please try again.")

        elif query == "UnknownValueError":
            say("I couldn't understand what you said. Can you please repeat it?")

        elif query == "TimeoutError":
            say("I didn't hear any input. Please speak something.")

        sites = [["youtube", "https://www.youtube.com/"], ["google", "https://www.google.com/"],
                 ["portfolio", "https://Aditya-Vishwa.github.io/My-Portfolio"],
                 ["instagram", "https://www.instagram.com/"], ["canva", "https://www.canva.com/"],
                 ["meet", "https://meet.google.com/"], ["classroom", "https://classroom.google.com/"],
                 ["mail", "https://mail.google.com/"], ["twitter", "https://www.twitter.com/"],
                 ["GitHub", "https://www.github.com/"]]

        apps = [["chrome", "chrome.exe"], ["file", "explorer.exe"], ["notepad", "notepad.exe"], ["code", "code"],
                ["discord", "C:/Users/vishw/AppData/Local/Discord/Update.exe --processStart Discord.exe"], []]

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
            response = say("Thanks for telling me your Fancy")
            knowledge_base_file = "knowledge.aiml"
            update_aiml_knowledge_base(user_input, response, knowledge_base_file, user_profile_file)


        if "play neffex" in query:
            musicPath = ("D:/Musics/NEFFEX.mp3")
            speaker.Speak("Let's Go...")
            os.system(f"start wmplayer {musicPath}")

        elif "interesting" in query.lower() or "tell me something" in query.lower():
            response = get_interesting_fact()
            speaker.Rate = 0.5
            say(response)

        elif "play quiz" in query.lower():
            play_quiz()


        elif "tell me a joke" in query.lower() or "jokes" in query.lower():
            joke = get_joke()
            if joke:
                say(joke)
            else:
                say("I'm sorry, I couldn't fetch a joke at the moment. Here's one from my collection instead:")
                say(get_joke())


        elif "hobbies" in query.lower():
            ask_about_hobbies()

        elif "time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Vishwa, it's {strfTime}. Is there anything else you'd like to know?")

        elif "where is" in query:
            location = query
            place = location.split()
            if place:
                last_word = place[-1]
            else:
                last_word = None
            maps(last_word)

        who = ["who are you", "who", "who's there", "what are you"]
        if f"{query}".lower() in who:
            say("Hello Sir! I am Elly a dedicated AI assistant, designed and developed by Vishwa to enhance your daily life. With a blend of intelligence and personality, I am your reliable companion for a wide range of tasks and interactions. Whether you need assistance with organizing your schedule, answering questions, or simply engaging in friendly conversations, I am always at your service. With my intuitive understanding and adaptability, I am here to make your life easier and more enjoyable.")

        bye = ["done", "exit", "end", "break", "you are free", "bye", "bye-bye", "free"]
        if f"{query}".lower() in bye:
            say("Take Care Vishwa")
            break

        print("listening again...")
        speaker.Speak("Listening to you")
