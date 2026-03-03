import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')
django.setup()

from quizzes.models import Category, SubCategory, Question, Choice

def clear_and_populate():
    """Clear existing categories, subcategories, questions and populate with new structure"""
    
    print("Clearing old data...")
    Choice.objects.all().delete()
    Question.objects.all().delete()
    SubCategory.objects.all().delete()
    Category.objects.all().delete()
    
    print("Starting fresh population with new 3-category structure...")
    
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
                'Cyber Security': [
                    ("What does 'HTTPS' stand for?", ["Hypertext Transfer Protocol Secure", "High Tech Transport System", "Hyperlink Text Privacy System", "Hidden Trade Security"], 0),
                    ("What is 'Phishing'?", ["Deceptive attempts to get sensitive info", "A type of physical attack", "Optimizing server speed", "Fishing for data cables"], 0),
                    ("Which of these is a common symmetric encryption algorithm?", ["AES", "RSA", "Diffie-Hellman", "DSA"], 0),
                    ("What is a 'Firewall'?", ["Network security system monitoring traffic", "A physical wall to prevent fire", "Software for burning CDs", "A tool for deleting spam"], 0),
                    ("What does 'MFA' stand for in security?", ["Multi-Factor Authentication", "Main File Access", "Memory Flash Array", "Multiple Forensic Analysis"], 0),
                    ("Which type of malware self-replicates across networks?", ["Worm", "Trojan", "Spyware", "Adware"], 0),
                    ("What is 'Social Engineering'?", ["Manipulating people into giving secrets", "Building a social network", "Engineering for social causes", "Upgrading server RAM"], 0),
                    ("What is a 'Zero-day' exploit?", ["Attack on an unknown vulnerability", "Attack that lasts zero days", "Attack from zero distance", "Attack with zero success"], 0),
                    ("What does 'DDoS' stand for?", ["Distributed Denial of Service", "Digital Data Outsource System", "Direct Device Operating Suite", "Disk Data Overwrite Service"], 0),
                    ("What is the purpose of a 'VPN'?", ["Encrypting internet traffic and hiding IP", "Speeding up video games", "Virtual Personal Note", "Validating Public Networks"], 0),
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
                'Logical Reasoning': [
                    ("If 'A' is 1 and 'B' is 2, what is the sum of letters in 'CAT'?", ["24", "20", "25", "22"], 0),
                    ("Which number comes next in the sequence: 1, 3, 6, 10, ?", ["15", "12", "14", "16"], 0),
                    ("If a clock shows 3:00, what is the angle between hands?", ["90 degrees", "180 degrees", "45 degrees", "0 degrees"], 0),
                    ("Point : Line :: Line : ?", ["Plane", "Dot", "Angle", "Curve"], 0),
                    ("If North-East becomes South, what will South become?", ["North-West", "North", "East", "West"], 0),
                    ("All men are mortal. Socrates is a man. Therefore?", ["Socrates is mortal", "Socrates is Greek", "All men are Socrates", "Mortal is Socrates"], 0),
                    ("Find the odd one out: Apple, Orange, Banana, Potato", ["Potato", "Apple", "Orange", "Banana"], 0),
                    ("If REASON is coded as 5, BELIEVED as 7, what is GOVERNMENT?", ["9", "10", "8", "6"], 0),
                    ("A is the father of B but B is not the son of A. What is B?", ["Daughter", "Nephew", "Cousin", "Step-son"], 0),
                    ("How many months have 28 days?", ["All of them", "1", "2", "6"], 0),
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
                    ("Who is the current Secretary-General of the UN?", ["António Guterres", "Ban Ki-moon", "Kofi Annan", "Javier Pérez"], 0),
                    ("Which city hosted the latest Summer Olympics?", ["Paris", "Tokyo", "Beijing", "London"], 0),
                    ("What is the currency of Japan?", ["Yen", "Yuan", "Won", "Dollar"], 0),
                    ("Which country has the largest population?", ["India", "China", "USA", "Indonesia"], 0),
                    ("What is the capital of Ukraine?", ["Kyiv", "Moscow", "Warsaw", "Berlin"], 0),
                    ("Which tech company recently became the most valuable?", ["NVIDIA", "Apple", "Microsoft", "Google"], 0),
                    ("What is 'COP' in the context of climate change?", ["Conference of Parties", "Carbon Offsetting Plan", "Climate Official Protocol", "Carbon Output Plan"], 0),
                    ("Which space agency launched the James Webb Telescope?", ["NASA", "ESA", "Roscosmos", "ISRO"], 0),
                    ("What is the main purpose of the G20 summit?", ["Economic cooperation", "World Peace", "Climate Control", "Space Exploration"], 0),
                    ("Which country recently joined NATO?", ["Sweden", "Ukraine", "Finland", "Georgia"], 0),
                ],
            }
        },
        'entertainment': {
            'name': 'Entertainment',
            'topics': {
                'Movies': [
                    ("Who directed 'Inception'?", ["Christopher Nolan", "Steven Spielberg", "James Cameron", "Quentin Tarantino"], 0),
                    ("Which movie won the Best Picture Oscar in 2024?", ["Oppenheimer", "Barbie", "Poor Things", "Past Lives"], 0),
                    ("Who played Iron Man in the MCU?", ["Robert Downey Jr.", "Chris Evans", "Chris Hemsworth", "Mark Ruffalo"], 0),
                    ("What is the highest-grossing film of all time?", ["Avatar", "Avengers: Endgame", "Titanic", "Star Wars"], 0),
                    ("Which movie features a character named 'Jack Sparrow'?", ["Pirates of the Caribbean", "Indiana Jones", "Harry Potter", "Star Wars"], 0),
                    ("Who directed the movie 'Titanic'?", ["James Cameron", "Steven Spielberg", "Christopher Nolan", "Martin Scorsese"], 0),
                    ("Which actor played the Joker in 'The Dark Knight'?", ["Heath Ledger", "Joaquin Phoenix", "Jack Nicholson", "Jared Leto"], 0),
                    ("What is the first ever animated feature film?", ["Snow White", "Toy Story", "Lion King", "Bambi"], 0),
                    ("In which movie was the quote 'I'll be back' first used?", ["The Terminator", "Predator", "Commando", "Total Recall"], 0),
                    ("Which movie series features 'Wookiees'?", ["Star Wars", "Star Trek", "Guardians of the Galaxy", "Dune"], 0),
                ],
                'Sports': [
                    ("Which country won the 2022 FIFA World Cup?", ["Argentina", "France", "Brazil", "Germany"], 0),
                    ("How many players are in a standard cricket team?", ["11", "10", "12", "9"], 0),
                    ("Who has won the most Ballon d'Or awards?", ["Lionel Messi", "Cristiano Ronaldo", "Pele", "Maradona"], 0),
                    ("Which sport is known as the 'Gentleman's Game'?", ["Cricket", "Football", "Tennis", "Golf"], 0),
                    ("In which city were the first modern Olympics held?", ["Athens", "Paris", "London", "Rome"], 0),
                    ("Which tennis player has the most Grand Slam titles?", ["Novak Djokovic", "Rafael Nadal", "Roger Federer", "Serena Williams"], 0),
                    ("What is the length of a marathon?", ["42.195 km", "40 km", "45 km", "38.5 km"], 0),
                    ("Which country dominated the latest Cricket World Cup?", ["Australia", "India", "England", "South Africa"], 0),
                    ("Who is known as 'The Flying Sikh' of India?", ["Milkha Singh", "P.T. Usha", "Neeraj Chopra", "Abhinav Bindra"], 0),
                    ("Which sport is represented by the 'Davis Cup'?", ["Tennis", "Badminton", "Golf", "Table Tennis"], 0),
                ],
                'Music': [
                    ("Who is known as the 'King of Pop'?", ["Michael Jackson", "Elvis Presley", "Prince", "Madonna"], 0),
                    ("Which band released 'Bohemian Rhapsody'?", ["Queen", "The Beatles", "Led Zeppelin", "Pink Floyd"], 0),
                    ("Who is the most streamed artist on Spotify?", ["Taylor Swift", "Bad Bunny", "Drake", "Ed Sheeran"], 0),
                    ("What instrument has 88 keys?", ["Piano", "Harp", "Accordion", "Xylophone"], 0),
                    ("Which singer is known as 'Queen Bey'?", ["Beyoncé", "Rihanna", "Adele", "Ariana Grande"], 0),
                    ("How many strings does a standard violin have?", ["4", "6", "5", "3"], 0),
                    ("Which genre did Bob Marley specialize in?", ["Reggae", "Jazz", "Blues", "Country"], 0),
                    ("Who composed 'The Four Seasons'?", ["Antonio Vivaldi", "J.S. Bach", "Beethoven", "Mozart"], 0),
                    ("What is the name of BTS's fan base?", ["ARMY", "Blinks", "Exo-L", "VIPS"], 0),
                    ("Which musical period did Mozart belong to?", ["Classical", "Baroque", "Romantic", "Modern"], 0),
                ],
                'Celebrities': [
                    ("What is the real name of the actor 'The Rock'?", ["Dwayne Johnson", "John Cena", "Dave Bautista", "Chris Evans"], 0),
                    ("Who is the world's highest-paid athlete?", ["Cristiano Ronaldo", "Lionel Messi", "LeBron James", "Tiger Woods"], 0),
                    ("Which celebrity is known for the brand 'Fenty Beauty'?", ["Rihanna", "Kylie Jenner", "Selena Gomez", "Ariana Grande"], 0),
                    ("Who is the founder of 'The Gates Foundation'?", ["Bill Gates", "Jeff Bezos", "Elon Musk", "Warren Buffett"], 0),
                    ("Which actress played 'Hermione Granger'?", ["Emma Watson", "Emma Stone", "Anne Hathaway", "Jennifer Lawrence"], 0),
                    ("Who is the author of 'Harry Potter'?", ["J.K. Rowling", "George R.R. Martin", "Stephen King", "J.R.R. Tolkien"], 0),
                    ("Which celebrity has the most followers on Instagram?", ["Cristiano Ronaldo", "Kylie Jenner", "Selena Gomez", "Lionel Messi"], 0),
                    ("Who is the CEO of SpaceX and Tesla?", ["Elon Musk", "Tim Cook", "Jeff Bezos", "Mark Zuckerberg"], 0),
                    ("Which talk show host is known for the 'Big Giveaway'?", ["Oprah Winfrey", "Ellen DeGeneres", "Jimmy Fallon", "James Corden"], 0),
                    ("Who won the Nobel Peace Prize at age 17?", ["Malala Yousafzai", "Greta Thunberg", "Nadia Murad", "Kailash Satyarthi"], 0),
                ],
            }
        }
    }

    print("Creating categories and topics...")
    for cat_type, data in categories_data.items():
        cat_obj, _ = Category.objects.get_or_create(
            category_type=cat_type,
            defaults={
                'name_en': data['name'],
                'name_ta': data['name'],
                'description': f"Dynamic quizzes on {data['name']} topics."
            }
        )

        for topic_name, questions in data['topics'].items():
            sub_obj, _ = SubCategory.objects.get_or_create(
                category=cat_obj,
                name_en=topic_name,
                defaults={'name_ta': topic_name, 'description': f"Become a master in {topic_name}"}
            )

            for q_text, p_choices, correct_idx in questions:
                q = Question.objects.create(
                    subcategory=sub_obj,
                    category=cat_obj,
                    text_en=q_text,
                    text_ta=q_text,
                    difficulty='medium'
                )
                for idx, c_text in enumerate(p_choices):
                    Choice.objects.create(
                        question=q,
                        text_en=c_text,
                        text_ta=c_text,
                        is_correct=(idx == correct_idx)
                    )
            print(f"  ✓ {topic_name}: {len(questions)} questions added")

    print("\nPopulation Complete!")

if __name__ == "__main__":
    clear_and_populate()
