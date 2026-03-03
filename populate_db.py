
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')  # Verify the settings module name
django.setup()

from quizzes.models import Category, SubCategory, Question, Choice

def populate_data():
    categories_data = {
        'technical': {
            'name': 'Technical',
            'topics': {
                'Programming': [
                    ("What does HTML stand for?", ["Hyper Text Markup Language", "High Tech Multi Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"], 0),
                    ("Which language is used for web apps?", ["PHP", "Python", "JavaScript", "All of the above"], 3),
                    ("What is the extension of Python files?", [".py", ".python", ".p", ".pt"], 0),
                    ("Which is not a programming language?", ["HTML", "Python", "Java", "C++"], 0),
                    ("Who created Python?", ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], 0),
                ],
                'Data Structures': [
                    ("Which data structure uses LIFO?", ["Stack", "Queue", "Array", "Tree"], 0),
                    ("Which data structure uses FIFO?", ["Queue", "Stack", "Graph", "Heap"], 0),
                    ("What is a linked list?", ["A linear collection of data elements", "A non-linear collection", "A type of array", "A database"], 0),
                    ("Time complexity of binary search?", ["O(log n)", "O(n)", "O(n^2)", "O(1)"], 0),
                    ("Which is a non-linear data structure?", ["Tree", "Array", "Stack", "Queue"], 0),
                ],
                'DBMS': [
                    ("What does SQL stand for?", ["Structured Query Language", "Strong Question Language", "Structured Question List", "Simple Query Language"], 0),
                    ("Which is a valid SQL command?", ["SELECT", "GET", "OPEN", "FETCH"], 0),
                    ("What is a primary key?", ["A unique identifier", "Any column", "A foreign key", "A null value"], 0),
                    ("What is normalization?", ["Organizing data to minimize redundancy", "Formatting text", "Backup process", "Database design"], 0),
                    ("Which is a NoSQL database?", ["MongoDB", "MySQL", "PostgreSQL", "Oracle"], 0),
                ],
                'Networking': [
                    ("What does IP stand for?", ["Internet Protocol", "Internal Protocol", "Internet Provider", "Intranet Protocol"], 0),
                    ("Which layer is responsible for routing?", ["Network Layer", "Transport Layer", "Data Link Layer", "Physical Layer"], 0),
                    ("What is HTTP?", ["HyperText Transfer Protocol", "HyperText Transfer Program", "HyperText Transmission Protocol", "HyperText Time Protocol"], 0),
                    ("Which device connects networks?", ["Router", "Switch", "Hub", "Modem"], 0),
                    ("What is a firewall used for?", ["Security", "Speed", "Storage", "Connectivity"], 0),
                ],
                'Cyber Security': [
                    ("What is Phishing?", ["A fraudulent attempt to obtain sensitive information", "Fishing for compliments", "Network scanning", "Password cracking"], 0),
                    ("What does SSL stand for?", ["Secure Sockets Layer", "Secure System Layer", "System Sockets Layer", "Secure Sockets Level"], 0),
                    ("What is a strong password?", ["A mix of chars, numbers, symbols", "Your name", "123456", "password"], 0),
                    ("What is malware?", ["Malicious software", "System software", "Application software", "Utility software"], 0),
                    ("What is encryption?", ["Encoding data", "Deleting data", "Managing data", "Copying data"], 0),
                ]
            }
        },
        'non-technical': {
            'name': 'Non-Technical',
            'topics': {
                'Aptitude': [
                    ("If 5x = 25, then x = ?", ["5", "25", "0.2", "125"], 0),
                    ("What is 15% of 200?", ["30", "15", "20", "40"], 0),
                    ("Next number in series: 2, 4, 8, 16, ?", ["32", "24", "64", "20"], 0),
                    ("A train 200m long passes a pole in 10s. Speed = ?", ["20 m/s", "10 m/s", "30 m/s", "40 m/s"], 0),
                    ("The cost is $100. Discount 10%. Final price?", ["$90", "$10", "$110", "$80"], 0),
                ],
                'Reasoning': [
                    ("Look at this series: 7, 10, 8, 11, 9, 12, ... What number next?", ["10", "12", "13", "14"], 0),
                    ("SCD, TEF, UGH, ____, WKL", ["VIJ", "VJI", "IJV", "JIV"], 0),
                    ("Pen is to poet as needle is to ?", ["Tailor", "Thread", "Button", "Sewing"], 0),
                    ("Which word does not belong?", ["Inch", "Ounce", "Centimeter", "Yard"], 1),
                    ("Safe is to Secure as Guard is to ?", ["Protect", "Lock", "Sure", "Conserve"], 0),
                ],
                'General Knowledge': [
                    ("Capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0),
                    ("Largest ocean?", ["Pacific", "Atlantic", "Indian", "Arctic"], 0),
                    ("Who wrote 'Hamlet'?", ["Shakespeare", "Dickens", "Hemingway", "Austen"], 0),
                    ("Chemical symbol for Gold?", ["Au", "Ag", "Fe", "Pb"], 0),
                    ("Longest river in the world?", ["Nile", "Amazon", "Yangtze", "Mississippi"], 0),
                ],
                'Current Affairs': [
                    ("Who is the UN Secretary General (2024)?", ["António Guterres", "Ban Ki-moon", "Kofi Annan", "Boutros-Ghali"], 0),
                    ("Host of 2024 Olympics?", ["Paris", "Tokyo", "Los Angeles", "Beijing"], 0),
                    ("Currency of Japan?", ["Yen", "Won", "Dollar", "Euro"], 0),
                    ("Largest tech company by market cap (2024)?", ["Microsoft", "Apple", "Google", "Amazon"], 0),
                    ("Current Prime Minister of UK (2024)?", ["Rishi Sunak", "Boris Johnson", "Theresa May", "David Cameron"], 0), 
                ]
            }
        },
        'academic': {
            'name': 'Academic',
            'topics': {
                'Physics': [
                    ("Unit of Force?", ["Newton", "Joule", "Watt", "Pascal"], 0),
                    ("Speed of light?", ["3x10^8 m/s", "3x10^6 m/s", "300 m/s", "3000 km/s"], 0),
                    ("Formula for kinetic energy?", ["1/2 mv^2", "ma", "mgh", "mc^2"], 0),
                    ("Who proposed relativity?", ["Einstein", "Newton", "Bohr", "Tesla"], 0),
                    ("What is gravity?", ["A force of attraction", "A type of energy", "A wave", "A particle"], 0),
                ],
                'Chemistry': [
                    ("Symbol for Water?", ["H2O", "HO2", "H2O2", "OH"], 0),
                    ("Atomic number of Carbon?", ["6", "12", "14", "8"], 0),
                    ("What is pH?", ["Measure of acidity", "Measure of heat", "Measure of mass", "Measure of volume"], 0),
                    ("Element with symbol Na?", ["Sodium", "Nitrogen", "Neon", "Nickel"], 0),
                    ("Simplest element?", ["Hydrogen", "Helium", "Lithium", "Beryllium"], 0),
                ],
                'Mathematics': [
                    ("Value of Pi?", ["3.14159", "3.14", "22/7", "All of the above"], 3),
                    ("Square root of 144?", ["12", "14", "16", "10"], 0),
                    ("Triangle angles sum?", ["180", "360", "90", "270"], 0),
                    ("Derivative of x^2?", ["2x", "x", "2", "x^2"], 0),
                    ("What is a prime number?", ["Divisible only by 1 and itself", "Odd number", "Even number", "Divisible by 2"], 0),
                ]
            }
        },
        'entertainment': {
            'name': 'Entertainment',
            'topics': {
                'Sports': [
                    ("National sport of India?", ["Hockey", "Cricket", "Football", "Kabaddi"], 0),
                    ("Who is known as CR7?", ["Cristiano Ronaldo", "Messi", "Neymar", "Mbappe"], 0),
                    ("How many players in a cricket team?", ["11", "10", "12", "9"], 0),
                    ("Where were the first modern Olympics held?", ["Athens", "Paris", "London", "Rome"], 0),
                    ("Which is a Grand Slam tournament?", ["Wimbledon", "IPL", "Super Bowl", "FIFA World Cup"], 0),
                ],
                'Movies': [
                    ("Who directed 'Titanic'?", ["James Cameron", "Spielberg", "Nolan", "Tarantino"], 0),
                    ("Highest grossing movie (2024 list)?", ["Avatar", "Avengers: Endgame", "Titanic", "Star Wars"], 0),
                    ("Oscar for Best Picture 2024?", ["Oppenheimer", "Barbie", "Killers of the Flower Moon", "Poor Things"], 0),
                    ("Character 'Iron Man' played by?", ["Robert Downey Jr.", "Chris Evans", "Chris Hemsworth", "Mark Ruffalo"], 0),
                    ("Which is an animated movie?", ["Toy Story", "Inception", "The Matrix", "Gladiator"], 0),
                ],
                'Music': [
                    ("King of Pop?", ["Michael Jackson", "Elvis Presley", "Prince", "Madonna"], 0),
                    ("Example of a string instrument?", ["Guitar", "Drum", "Flute", "Trumpet"], 0),
                    ("Who sings 'Shape of You'?", ["Ed Sheeran", "Justin Bieber", "Taylor Swift", "Adele"], 0),
                    ("Which is a classical composer?", ["Beethoven", "Beatles", "Beyonce", "Bono"], 0),
                    ("Number of keys on a piano?", ["88", "66", "44", "22"], 0),
                ]
            }
        }
    }

    print("Starting population...")

    for cat_type, data in categories_data.items():
        # First, try to find existing category by type
        cat_obj = Category.objects.filter(category_type=cat_type).first()
        if cat_obj:
            # Update existing category
            cat_obj.name_en = data['name']
            cat_obj.name_ta = data['name']
            cat_obj.description = f"Test your knowledge in {data['name']} topics."
            cat_obj.save()
            created = False
        else:
            # Create new category
            cat_obj = Category.objects.create(
                category_type=cat_type,
                name_en=data['name'], 
                name_ta=data['name'],
                description=f"Test your knowledge in {data['name']} topics."
            )
            created = True

        print(f"Propagating {cat_obj.name_en}...")

        for topic_name, questions in data['topics'].items():
            sub_obj, created = SubCategory.objects.get_or_create(
                category=cat_obj,
                name_en=topic_name,
                defaults={'name_ta': topic_name, 'description': f"Questions about {topic_name}"}
            )
            print(f"  - Topic: {sub_obj.name_en}")

            # Clear existing questions to avoid duplicates or mixed content if re-running
            # Or check if questions exist
            if Question.objects.filter(subcategory=sub_obj).count() < len(questions):
                for q_text, choices, correct_idx in questions:
                    q, q_created = Question.objects.get_or_create(
                        subcategory=sub_obj,
                        text_en=q_text,
                        defaults={
                            'text_ta': q_text,
                            'difficulty': 'medium'
                        }
                    )
                    
                    if q_created:
                        for idx, choice_text in enumerate(choices):
                            Choice.objects.create(
                                question=q,
                                text_en=choice_text,
                                text_ta=choice_text,
                                is_correct=(idx == correct_idx)
                            )
                print(f"    Added {len(questions)} questions.")
            else:
                 print(f"    Questions already exist.")

    print("Population complete.")

if __name__ == '__main__':
    populate_data()
