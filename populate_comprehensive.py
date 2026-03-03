import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')
django.setup()

from quizzes.models import Category, SubCategory, Question, Choice

def clear_and_populate():
    """Clear existing questions and populate with comprehensive topic-specific data"""
    
    print("Clearing old questions and choices...")
    Question.objects.all().delete()
    
    print("Starting fresh population with 10 questions per topic...")
    
    # Comprehensive data structure with 10 questions per topic
    categories_data = {
        'technical': {
            'name': 'Technical',
            'topics': {
                'Python': [
                    ("What is the correct file extension for Python files?", [".py", ".python", ".pt", ".pyt"], 0),
                    ("Which keyword is used to define a function in Python?", ["def", "function", "fun", "define"], 0),
                    ("What is the output of: print(type([]))?", ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"], 0),
                    ("How do you insert comments in Python code?", ["# This is a comment", "// This is a comment", "/* This is a comment */", "<!-- This is a comment -->"], 0),
                    ("Which of these is a Python tuple?", ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "1, 2, 3"], 0),
                    ("What does 'pip' stand for in Python?", ["Pip Installs Packages", "Python Install Package", "Package Install Python", "Python Installer Program"], 0),
                    ("Which operator is used for exponentiation in Python?", ["**", "^", "exp", "pow"], 0),
                    ("What is the correct way to create a dictionary in Python?", ["{key: value}", "[key: value]", "(key: value)", "key: value"], 0),
                    ("Which method is used to add an element at the end of a list?", ["append()", "add()", "insert()", "push()"], 0),
                    ("What is the result of: 10 // 3?", ["3", "3.33", "4", "3.0"], 0),
                ],
                'Java': [
                    ("What is the extension of Java source files?", [".java", ".jav", ".class", ".j"], 0),
                    ("Which keyword is used to create a class in Java?", ["class", "Class", "create", "new"], 0),
                    ("What is the default value of a boolean variable in Java?", ["false", "true", "0", "null"], 0),
                    ("Which method is the entry point for a Java application?", ["public static void main(String[] args)", "public void main()", "static void main()", "void main()"], 0),
                    ("What is the size of int in Java?", ["32 bits", "16 bits", "64 bits", "8 bits"], 0),
                    ("Which keyword is used for inheritance in Java?", ["extends", "inherits", "implements", "super"], 0),
                    ("What is the parent class of all classes in Java?", ["Object", "Base", "Parent", "Root"], 0),
                    ("Which access modifier makes a member accessible only within its own class?", ["private", "public", "protected", "default"], 0),
                    ("What is used to handle exceptions in Java?", ["try-catch", "if-else", "switch-case", "for-while"], 0),
                    ("Which collection class allows duplicate elements?", ["ArrayList", "HashSet", "TreeSet", "HashMap"], 0),
                ],
                'Data Structures': [
                    ("Which data structure uses LIFO principle?", ["Stack", "Queue", "Array", "Tree"], 0),
                    ("Which data structure uses FIFO principle?", ["Queue", "Stack", "Linkedlist", "Graph"], 0),
                    ("What is the time complexity of accessing an element in an array?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0),
                    ("Which data structure is used for BFS traversal?", ["Queue", "Stack", "Tree", "Array"], 0),
                    ("Which data structure is used for DFS traversal?", ["Stack", "Queue", "Array", "Heap"], 0),
                    ("What is the worst-case time complexity of binary search?", ["O(log n)", "O(n)", "O(n log n)", "O(1)"], 0),
                    ("In a binary tree, what is the maximum number of nodes at level L?", ["2^L", "L^2", "2*L", "L!"], 0),
                    ("Which data structure is used to implement recursion?", ["Stack", "Queue", "Array", "Tree"], 0),
                    ("What is a circular linked list?", ["Last node points to first node", "First node points to last", "All nodes point to each other", "No pointers"], 0),
                    ("Which sorting algorithm has best case O(n log n)?", ["Merge Sort", "Bubble Sort", "Insertion Sort", "Selection Sort"], 0),
                ],
                'DBMS': [
                    ("What does SQL stand for?", ["Structured Query Language", "System Query Language", "Simple Query Language", "Standard Query Language"], 0),
                    ("Which command is used to retrieve data from a database?", ["SELECT", "GET", "FETCH", "RETRIEVE"], 0),
                    ("What is a primary key?", ["Unique identifier for a record", "Foreign key reference", "Index column", "Any column"], 0),
                    ("Which normal form eliminates transitive dependency?", ["3NF", "1NF", "2NF", "BCNF"], 0),
                   ("What type of JOIN returns all records from both tables?", ["FULL OUTER JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN"], 0),
                    ("Which clause is used to filter records in SQL?", ["WHERE", "FILTER", "HAVING", "SELECT"], 0),
                    ("What is a foreign key?", ["Reference to primary key of another table", "Unique key", "Composite key", "Alternate key"], 0),
                    ("Which command is used to modify existing data?", ["UPDATE", "MODIFY", "CHANGE", "ALTER"], 0),
                    ("What does ACID stand for in databases?", ["Atomicity, Consistency, Isolation, Durability", "Association, Consistency, Integrity, Durability", "Atomicity, Concurrency, Isolation, Data", "All Correct Insertions Daily"], 0),
                    ("Which is an example of NoSQL database?", ["MongoDB", "MySQL", "PostgreSQL", "Oracle"], 0),
                ],
                'Networking': [
                    ("What does IP stand for?", ["Internet Protocol", "Internal Protocol", "Internet Provider", "Internal Provider"], 0),
                    ("Which layer handles routing in OSI model?", ["Network Layer", "Transport Layer", "Data Link Layer", "Application Layer"], 0),
                    ("What is the default port for HTTP?", ["80", "443", "8080", "22"], 0),
                    ("Which protocol is used for secure web browsing?", ["HTTPS", "HTTP", "FTP", "SMTP"], 0),
                    ("What does DNS stand for?", ["Domain Name System", "Domain Network Service", "Data Name System", "Digital Network Service"], 0),
                    ("Which device operates at the Network Layer?", ["Router", "Switch", "Hub", "Repeater"], 0),
                    ("What is the range of well-known ports?", ["0-1023", "1024-49151", "49152-65535", "1-100"], 0),
                    ("Which protocol is connection-oriented?", ["TCP", "UDP", "IP", "ICMP"], 0),
                    ("What is a MAC address?", ["Physical address of network interface", "IP address", "Port number", "Domain name"], 0),
                    ("Which command is used to test network connectivity?", ["ping", "test", "connect", "check"], 0),
                ],
            }
        },
        'non-technical': {
            'name': 'Non-Technical',
            'topics': {
                'Aptitude': [
                    ("If 5x = 25, what is x?", ["5", "25", "20", "10"], 0),
                    ("What is 25% of 200?", ["50", "25", "75", "100"], 0),
                    ("Next in series: 2, 4, 8, 16, ?", ["32", "24", "64", "20"], 0),
                    ("A train 100m long passes a pole in 5 seconds. What is its speed in m/s?", ["20", "10", "25", "15"], 0),
                    ("If a product costs $120 after a 20% discount, what was the original price?", ["$150", "$140", "$100", "$160"], 0),
                    ("What is the average of 10, 20, 30?", ["20", "15", "25", "30"], 0),
                    ("If A:B = 2:3 and B:C = 4:5, what is A:C?", ["8:15", "2:5", "4:5", "3:5"], 0),
                    ("72% of 50 is what number?", ["36", "38", "40", "42"], 0),
                    ("A man gains 10% by selling an article for $110. What is the cost price?", ["$100", "$99", "$105", "$95"], 0),
                    ("Simple interest on $1000 for 2 years at 5% per annum is?", ["$100", "$50", "$150", "$200"], 0),
                ],
                'Reasoning': [
                    ("Complete the series: 7, 10, 8, 11, 9, ?", ["12", "10", "13", "14"], 0),
                    ("SCD, TEF, UGH, ?, WKL", ["VIJ", "VJI", "IJV", "JIV"], 0),
                    ("If DANCE is coded as GDBDF, how is MUSIC coded?", ["NVTJD", "NVTID", "MVSJD", "NVSJC"], 0),
                    ("Pen : Poet :: Needle : ?", ["Tailor", "Thread", "Cloth", "Sewing"], 0),
                    ("Which word does NOT belong: Dog, Cat, Rat, Table?", ["Table", "Rat", "Cat", "Dog"], 0),
                    ("If all roses are flowers and some flowers are red, then?", ["Some roses may be red", "All roses are red", "No roses are red", "All flowers are red"], 0),
                    ("Monday is to Tuesday as Friday is to?", ["Saturday", "Thursday", "Sunday", "Wednesday"], 0),
                    ("Find the odd one: 3, 9, 15, 27, 33", ["27", "3", "15", "33"], 0),
                    ("If BAT is 23, what is CAT?", ["24", "23", "25", "22"], 0),
                    ("North : South :: East : ?", ["West", "North", "South", "North-East"], 0),
                ],
                'General Knowledge': [
                    ("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0),
                    ("Who wrote 'Romeo and Juliet'?", ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"], 0),
                    ("What is the largest ocean on Earth?", ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], 0),
                    ("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Saturn"], 0),
                    ("What is the chemical symbol for gold?", ["Au", "Ag", "Fe", "Cu"], 0),
                    ("Who painted the Mona Lisa?", ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"], 0),
                    ("What is the smallest continent?", ["Australia", "Europe", "Antarctica", "South America"], 0),
                    ("Which gas do plants absorb from the atmosphere?", ["Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen"], 0),
                    ("How many continents are there?", ["7", "5", "6", "8"], 0),
                    ("What is the hardest natural substance?", ["Diamond", "Gold", "Iron", "Platinum"], 0),
                ],
                'Current Affairs': [
                    ("Who is the Secretary-General of the UN (as of 2024)?", ["António Guterres", "Ban Ki-moon", "Kofi Annan", "Javier Pérez"], 0),
                    ("Which city hosted the 2024 Summer Olympics?", ["Paris", "Tokyo", "Beijing", "London"], 0),
                    ("What is the currency of Japan?", ["Yen", "Yuan", "Won", "Dollar"], 0),
                    ("Which country has the largest population?", ["India", "China", "USA", "Indonesia"], 0),
                    ("What is the capital of Australia?", ["Canberra", "Sydney", "Melbourne", "Brisbane"], 0),
                    ("Which organization awards the Nobel Peace Prize?", ["Norwegian Nobel Committee", "Swedish Academy", "UN", "EU"], 0),
                    ("What is COP in climate conferences?", ["Conference of Parties", "Climate Official Protocol", "Carbon Output Plan", "Committee of Paris"], 0),
                    ("Which country launched the James Webb Space Telescope?", ["USA", "Russia", "China", "Europe"], 0),
                    ("What does WHO stand for?", ["World Health Organization", "World Help Organization", "Worldwide Health Office", "World Humanitarian Org"], 0),
                    ("Which is the smallest country by area?", ["Vatican City", "Monaco", "Nauru", "Tuvalu"], 0),
                ],
            }
        },
        'academic': {
            'name': 'Academic',
            'topics': {
                'Physics': [
                    ("What is the SI unit of force?", ["Newton", "Joule", "Watt", "Pascal"], 0),
                    ("What is the speed of light in vacuum?", ["3×10^8 m/s", "3×10^6 m/s", "3×10^10 m/s", "3×10^4 m/s"], 0),
                    ("What is the formula for kinetic energy?", ["1/2 mv²", "mgh", "mc²", "mv"], 0),
                    ("Who proposed the theory of relativity?", ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Nikola Tesla"], 0),
                    ("What is the SI unit of electric current?", ["Ampere", "Volt", "Ohm", "Watt"], 0),
                    ("What type of lens is used to correct myopia?", ["Concave","Convex", "Bifocal", "Cylindrical"], 0),
                    ("What is Newton's second law of motion?", ["F = ma", "F = mv", "F = m/a", "F = a/m"], 0),
                    ("What is the acceleration due to gravity on Earth?", ["9.8 m/s²", "10 m/s²", "8.9 m/s²", "11 m/s²"], 0),
                    ("Which color has the longest wavelength?", ["Red", "Violet", "Blue", "Green"], 0),
                    ("What is the SI unit of energy?", ["Joule", "Watt", "Newton", "Calorie"], 0),
                ],
                'Chemistry': [
                    ("What is the chemical formula of water?", ["H₂O", "HO₂", "H₂O₂", "OH"], 0),
                    ("What is the atomic number of carbon?", ["6", "12", "8", "14"], 0),
                    ("What is pH a measure of?", ["Acidity or alkalinity", "Temperature", "Pressure", "Volume"], 0),
                    ("Which gas is most abundant in Earth's atmosphere?", ["Nitrogen", "Oxygen", "Carbon Dioxide", "Argon"], 0),
                    ("What is the symbol for sodium?", ["Na", "S", "N", "So"], 0),
                    ("Which is the lightest element?", ["Hydrogen", "Helium", "Lithium", "Carbon"], 0),
                    ("What type of bond involves sharing electrons?", ["Covalent", "Ionic", "Metallic", "Hydrogen"], 0),
                    ("What is the pH of pure water?", ["7", "0", "14", "1"], 0),
                    ("Which gas is known as laughing gas?", ["Nitrous Oxide", "Nitrogen", "Oxygen", "Helium"], 0),
                    ("What is the chemical symbol for iron?", ["Fe", "Ir", "I", "Fr"], 0),
                ],
                'Mathematics': [
                    ("What is the value of π (pi)?", ["3.14159...", "2.71828...", "1.61803...", "2.30258..."], 0),
                    ("What is the square root of 144?", ["12", "14", "11", "13"], 0),
                    ("What is the sum of angles in a triangle?", ["180°", "360°", "90°", "270°"], 0),
                    ("What is the derivative of x²?", ["2x", "x", "x²", "2"], 0),
                    ("What is a prime number?", ["Number divisible only by 1 and itself", "Even number", "Odd number", "Multiple of 2"], 0),
                    ("What is 5! (5 factorial)?", ["120", "60", "24", "720"], 0),
                    ("What is the Pythagorean theorem?", ["a² + b² = c²", "a + b = c", "a² - b² = c²", "a × b = c"], 0),
                    ("What is the area of a circle with radius r?", ["πr²", "2πr", "πr", "4πr²"], 0),
                    ("What is log₁₀(100)?", ["2", "10", "100", "1"], 0),
                    ("What is the value of sin(90°)?", ["1", "0", "√3/2", "1/2"], 0),
                ],
            }
        },
        'entertainment': {
            'name': 'Entertainment',
            'topics': {
                'Sports': [
                    ("Which country won the FIFA World Cup 2018?", ["France", "Brazil", "Germany", "Argentina"], 0),
                    ("How many players are there in a cricket team?", ["11", "10", "12", "9"], 0),
                    ("What is the national sport of India?", ["Hockey", "Cricket", "Football", "Kabaddi"], 0),
                    ("Who is known as the 'God of Cricket'?", ["Sachin Tendulkar", "Virat Kohli", "MS Dhoni", "Ricky Ponting"], 0),
                    ("How many Grand Slam tournaments are there in tennis?", ["4", "3", "5", "6"], 0),
                    ("In which sport is the term 'birdie' used?", ["Badminton", "Tennis", "Golf", "Cricket"], 0),
                    ("How many rings are there in the Olympic symbol?", ["5", "4", "6", "7"], 0),
                    ("Which country has won the most Olympic gold medals?", ["USA", "China", "Russia", "Germany"], 0),
                    ("What is the length of an Olympic swimming pool?", ["50 meters", "25 meters", "100 meters", "75 meters"], 0),
                    ("Who has won the most Ballon d'Or awards?", ["Lionel Messi", "Cristiano Ronaldo", "Pele", "Maradona"], 0),
                ],
                'Movies': [
                    ("Who directed 'Titanic'?", ["James Cameron", "Steven Spielberg", "Christopher Nolan", "Martin Scorsese"], 0),
                    ("Which movie won the Best Picture Oscar in 2024?", ["Oppenheimer", "Barbie", "Poor Things", "Killers of the Flower Moon"], 0),
                    ("Who played Iron Man in the Marvel movies?", ["Robert Downey Jr.", "Chris Evans", "Chris Hemsworth", "Mark Ruffalo"], 0),
                    ("Which is the highest-grossing movie of all time?", ["Avatar", "Avengers: Endgame", "Titanic", "Star Wars"], 0),
                    ("Who directed 'Inception'?", ["Christopher Nolan", "Quentin Tarantino", "James Cameron", "Steven Spielberg"], 0),
                    ("Which actor played Jack in 'Titanic'?", ["Leonardo DiCaprio", "Brad Pitt", "Tom Cruise", "Matt Damon"], 0),
                    ("What year was the first 'Star Wars' movie released?", ["1977", "1980", "1975", "1983"], 0),
                    ("Who won the Oscar for Best Actor in 2023?", ["Brendan Fraser", "Austin Butler", "Colin Farrell", "Bill Nighy"], 0),
                    ("Which movie series features Hogwarts School?", ["Harry Potter", "Lord of the Rings", "Narnia", "Percy Jackson"], 0),
                    ("Who directed 'The Godfather'?", ["Francis Ford Coppola", "Martin Scorsese", "Clint Eastwood", "Woody Allen"], 0),
                ],
                'Music': [
                    ("Who is known as the 'King of Pop'?", ["Michael Jackson", "Elvis Presley", "Prince", "Madonna"], 0),
                    ("Which instrument has 88 keys?", ["Piano", "Organ", "Harpsichord", "Synthesizer"], 0),
                    ("Who sings 'Shape of You'?", ["Ed Sheeran", "Justin Bieber", "Bruno Mars", "Shawn Mendes"], 0),
                    ("What is the highest female singing voice?", ["Soprano", "Alto", "Tenor", "Bass"], 0),
                    ("Which band sang 'Bohemian Rhapsody'?", ["Queen", "The Beatles", "Led Zeppelin", "Pink Floyd"], 0),
                    ("How many strings does a standard guitar have?", ["6", "5", "7", "4"], 0),
                    ("Who is known as the 'Queen of Soul'?", ["Aretha Franklin", "Whitney Houston", "Diana Ross", "Tina Turner"], 0),
                    ("Which classical composer became deaf?", ["Beethoven", "Mozart", "Bach", "Chopin"], 0),
                    ("What does BPM stand for in music?", ["Beats Per Minute", "Bass Per Measure", "Bars Per Melody", "Beat Pattern Measure"], 0),
                    ("Which instrument is Yo-Yo Ma famous for playing?", ["Cello", "Violin", "Viola", "Double Bass"], 0),
                ],
            }
        }
    }

    print("Creating categories and topics with questions...")
    
    for cat_type, data in categories_data.items():
        # Get or create category
        cat_obj = Category.objects.filter(category_type=cat_type).first()
        if cat_obj:
            cat_obj.name_en = data['name']
            cat_obj.name_ta = data['name']
            cat_obj.description = f"Test your knowledge in {data['name']} topics."
            cat_obj.save()
        else:
            cat_obj = Category.objects.create(
                category_type=cat_type,
                name_en=data['name'], 
                name_ta=data['name'],
                description=f"Test your knowledge in {data['name']} topics."
            )

        print(f"\n{cat_obj.name_en} Category:")
        
        for topic_name, questions_list in data['topics'].items():
            # Get or create subcategory
            sub_obj, created = SubCategory.objects.get_or_create(
                category=cat_obj,
                name_en=topic_name,
                defaults={'name_ta': topic_name, 'description': f"Test your {topic_name} knowledge"}
            )
            
            # Clear existing questions for this topic
            Question.objects.filter(subcategory=sub_obj).delete()
            
            # Add all questions for this topic
            for q_text, choices, correct_idx in questions_list:
                q = Question.objects.create(
                    subcategory=sub_obj,
                    category=cat_obj,
                    text_en=q_text,
                    text_ta=q_text,
                    difficulty='medium'
                )
                
                for idx, choice_text in enumerate(choices):
                    Choice.objects.create(
                        question=q,
                        text_en=choice_text,
                        text_ta=choice_text,
                        is_correct=(idx == correct_idx)
                    )
            
            print(f"  ✓ {topic_name}: {len(questions_list)} questions added")

    print("\n" + "="*60)
    print("POPULATION COMPLETE!")
    print("="*60)
    total_topics = SubCategory.objects.count()
    total_questions = Question.objects.count()
    print(f"Total Topics: {total_topics}")
    print(f"Total Questions: {total_questions}")
    print(f"Questions per topic: 10")
    print("="*60)

if __name__ == '__main__':
    clear_and_populate()
