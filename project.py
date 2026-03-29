import json
import datetime
import random
import os
from typing import List, Dict

class StudySession:
    def __init__(self, subject: str, duration: int, topics: str, notes: str = ""):
        self.subject = subject
        self.duration = duration
        self.topics = topics
        self.notes = notes
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.session_id = hash(f"{subject}{duration}{topics}{self.date}")
    
    def to_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'subject': self.subject,
            'duration': self.duration,
            'topics': self.topics,
            'notes': self.notes,
            'date': self.date
        }
    
    def __str__(self) -> str:
        return f"{self.date} - {self.subject} ({self.duration}min): {self.topics}"

class QuizGenerator:
    def __init__(self):
        self.question_templates = {
            'math': [
                "What is {num1} + {num2}?",
                "Solve: {num1} * {num2}",
                "Calculate {num1} - {num2}"
            ],
            'science': [
                "What is the capital of {country}?",
                "Explain {concept} in one sentence",
                "Who discovered {discovery}?"
            ],
            'history': [
                "When did {event} happen?",
                "Who was the leader during {event}?",
                "What caused {event}?"
            ],
            'programming': [
                "What does {term} stand for?",
                "Explain {concept} in programming",
                "What is the purpose of {function}?"
            ]
        }
        
        self.science_data = {
            'countries': ['France', 'Germany', 'Japan', 'Brazil', 'India'],
            'concepts': ['gravity', 'photosynthesis', 'evolution', 'atoms'],
            'discoveries': ['penicillin', 'electricity', 'DNA structure', 'radioactivity']
        }
        
        self.history_data = {
            'events': ['World War II', 'the Renaissance', 'the Industrial Revolution', 'the French Revolution'],
            'concepts': ['democracy', 'monarchy', 'revolution', 'imperialism']
        }
    
    def generate_question(self, subject: str, topic: str) -> Dict:
        if subject not in self.question_templates:
            subject = 'science'
        
        template = random.choice(self.question_templates[subject])
        
        if subject == 'math':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            question = template.format(num1=num1, num2=num2)
            
            if '+' in template:
                answer = num1 + num2
            elif '*' in template:
                answer = num1 * num2
            else:
                answer = num1 - num2
                
        elif subject == 'science':
            if '{country}' in template:
                country = random.choice(self.science_data['countries'])
                question = template.format(country=country)
                answer = self.get_capital(country)
            elif '{concept}' in template:
                concept = random.choice(self.science_data['concepts'])
                question = template.format(concept=concept)
                answer = self.explain_concept(concept)
            else:
                discovery = random.choice(self.science_data['discoveries'])
                question = template.format(discovery=discovery)
                answer = self.get_discoverer(discovery)
                
        elif subject == 'history':
            if '{event}' in template:
                event = random.choice(self.history_data['events'])
                question = template.format(event=event)
                answer = self.get_event_date(event)
            else:
                concept = random.choice(self.history_data['concepts'])
                question = template.format(concept=concept)
                answer = f"Explanation of {concept}"
                
        else:
            programming_terms = ['API', 'SQL', 'HTML', 'CSS', 'JSON', 'HTTP']
            term = random.choice(programming_terms)
            question = template.format(term=term, concept=topic, function=topic)
            answer = self.explain_programming_term(term)
        
        return {
            'question': question,
            'answer': str(answer),
            'subject': subject,
            'topic': topic
        }
    
    def get_capital(self, country: str) -> str:
        capitals = {
            'France': 'Paris', 'Germany': 'Berlin', 'Japan': 'Tokyo',
            'Brazil': 'Brasília', 'India': 'New Delhi'
        }
        return capitals.get(country, f"Capital of {country}")
    
    def explain_concept(self, concept: str) -> str:
        explanations = {
            'gravity': 'Force that attracts objects with mass toward each other',
            'photosynthesis': 'Process where plants convert light energy to chemical energy',
            'evolution': 'Process of change in species over generations',
            'atoms': 'Basic building blocks of matter made of protons, neutrons, electrons'
        }
        return explanations.get(concept, f"Explanation of {concept}")
    
    def get_discoverer(self, discovery: str) -> str:
        discoverers = {
            'penicillin': 'Alexander Fleming',
            'electricity': 'Benjamin Franklin',
            'DNA structure': 'James Watson and Francis Crick',
            'radioactivity': 'Marie Curie'
        }
        return discoverers.get(discovery, f"Discoverer of {discovery}")
    
    def get_event_date(self, event: str) -> str:
        dates = {
            'World War II': '1939-1945',
            'the Renaissance': '14th-17th century',
            'the Industrial Revolution': '1760-1840',
            'the French Revolution': '1789-1799'
        }
        return dates.get(event, f"Time period of {event}")
    
    def explain_programming_term(self, term: str) -> str:
        explanations = {
            'API': 'Application Programming Interface - allows software applications to communicate',
            'SQL': 'Structured Query Language - used for database management',
            'HTML': 'HyperText Markup Language - structure of web pages',
            'CSS': 'Cascading Style Sheets - styling of web pages',
            'JSON': 'JavaScript Object Notation - data interchange format',
            'HTTP': 'HyperText Transfer Protocol - foundation of web data communication'
        }
        return explanations.get(term, f"Explanation of {term}")

class StudyAnalytics:
    def __init__(self, sessions: List[StudySession]):
        self.sessions = sessions
    
    def get_total_study_time(self) -> int:
        return sum(session.duration for session in self.sessions)
    
    def get_study_time_by_subject(self) -> Dict[str, int]:
        subject_time = {}
        for session in self.sessions:
            subject_time[session.subject] = subject_time.get(session.subject, 0) + session.duration
        return subject_time
    
    def get_study_streak(self) -> int:
        if not self.sessions:
            return 0
        
        dates = sorted(set(session.date.split()[0] for session in self.sessions))
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        streak = 0
        current_date = datetime.datetime.now()
        
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in dates:
                streak += 1
                current_date -= datetime.timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_recommendations(self) -> List[str]:
        recommendations = []
        subject_time = self.get_study_time_by_subject()
        
        if not subject_time:
            return ["Start by logging your first study session!"]
        
        total_time = self.total_study_time_hours()
        
        if total_time < 5:
            recommendations.append("Try to study at least 5 hours per week")
        
        if len(subject_time) == 1:
            subject = list(subject_time.keys())[0]
            recommendations.append(f"Consider studying other subjects besides {subject}")
        
        streak = self.get_study_streak()
        if streak >= 3:
            recommendations.append(f"Great job! You're on a {streak}-day study streak!")
        else:
            recommendations.append("Try to study every day to build a habit")
        
        return recommendations
    
    def total_study_time_hours(self) -> float:
        return self.get_total_study_time() / 60

class StudyStorage:
    def __init__(self, filename: str = "study_sessions.json"):
        self.filename = filename
    
    def save_sessions(self, sessions: List[StudySession]) -> bool:
        try:
            with open(self.filename, 'w') as f:
                json_data = [session.to_dict() for session in sessions]
                json.dump(json_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving sessions: {e}")
            return False
    
    def load_sessions(self) -> List[StudySession]:
        try:
            if not os.path.exists(self.filename):
                return []
            
            with open(self.filename, 'r') as f:
                data = json.load(f)
                sessions = []
                for item in data:
                    session = StudySession(
                        subject=item['subject'],
                        duration=item['duration'],
                        topics=item['topics'],
                        notes=item.get('notes', '')
                    )
                    session.session_id = item['session_id']
                    session.date = item['date']
                    sessions.append(session)
                return sessions
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return []

class AIStudyPartner:
    def __init__(self):
        self.storage = StudyStorage()
        self.sessions = self.storage.load_sessions()
        self.quiz_generator = QuizGenerator()
        self.analytics = StudyAnalytics(self.sessions)
    
    def log_study_session(self):
        print("\n--- Log Study Session ---")
        
        subject = input("Enter subject (math/science/history/programming/other): ").lower()
        duration = int(input("Enter duration in minutes: "))
        topics = input("Enter topics studied: ")
        notes = input("Enter any notes (optional): ")
        
        session = StudySession(subject, duration, topics, notes)
        self.sessions.append(session)
        
        if self.storage.save_sessions(self.sessions):
            print("Study session logged successfully! 📚")
        else:
            print("Failed to save session")
    
    def generate_quiz(self):
        print("\n--- Generate Quiz ---")
        
        if not self.sessions:
            print("No study sessions found. Log some sessions first!")
            return
        
        recent_sessions = sorted(self.sessions, key=lambda x: x.date, reverse=True)[:5]
        
        print("Recent study topics:")
        for i, session in enumerate(recent_sessions, 1):
            print(f"{i}. {session.subject}: {session.topics}")
        
        try:
            choice = int(input("Choose a session to generate quiz for (1-5): ")) - 1
            if 0 <= choice < len(recent_sessions):
                session = recent_sessions[choice]
                
                num_questions = int(input("How many questions? (1-5): "))
                num_questions = max(1, min(5, num_questions))
                
                print(f"\n--- Quiz on {session.subject}: {session.topics} ---")
                correct_answers = 0
                
                for i in range(num_questions):
                    question_data = self.quiz_generator.generate_question(
                        session.subject, session.topics
                    )
                    
                    print(f"\nQ{i+1}: {question_data['question']}")
                    user_answer = input("Your answer: ")
                    
                    print(f"Correct answer: {question_data['answer']}")
                    
                    if user_answer.lower() in question_data['answer'].lower():
                        print("✅ Correct!")
                        correct_answers += 1
                    else:
                        print("❌ Try again next time!")
                
                score = (correct_answers / num_questions) * 100
                print(f"\nQuiz complete! Score: {correct_answers}/{num_questions} ({score:.1f}%)")
                
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter valid numbers")
    
    def view_analytics(self):
        print("\n--- Study Analytics ---")
        
        if not self.sessions:
            print("No study sessions found.")
            return
        
        total_time = self.analytics.get_total_study_time()
        subject_time = self.analytics.get_study_time_by_subject()
        streak = self.analytics.get_study_streak()
        
        print(f"Total study time: {total_time} minutes ({total_time/60:.1f} hours)")
        print(f"Current study streak: {streak} days")
        print(f"Total sessions: {len(self.sessions)}")
        
        print("\nTime by subject:")
        for subject, time in subject_time.items():
            print(f"  {subject}: {time} minutes")
        
        print("\nRecommendations:")
        for recommendation in self.analytics.get_recommendations():
            print(f"  • {recommendation}")
    
    def view_study_sessions(self):
        print("\n--- Study Sessions ---")
        
        if not self.sessions:
            print("No study sessions found.")
            return
        
        for i, session in enumerate(sorted(self.sessions, key=lambda x: x.date, reverse=True), 1):
            print(f"{i}. {session}")
            if session.notes:
                print(f"   Notes: {session.notes}")
    
    def run(self):
        print("🤖 Welcome to AI Study Partner!")
        print("Your personal assistant for effective studying")
        
        while True:
            print("\n" + "="*40)
            print("          AI STUDY PARTNER")
            print("="*40)
            print("1. Log Study Session")
            print("2. Generate Quiz")
            print("3. View Analytics")
            print("4. View Study Sessions")
            print("5. Exit")
            print("="*40)
            
            choice = input("Choose an option (1-5): ")
            
            if choice == "1":
                self.log_study_session()
            elif choice == "2":
                self.generate_quiz()
            elif choice == "3":
                self.view_analytics()
            elif choice == "4":
                self.view_study_sessions()
            elif choice == "5":
                print("Keep studying! Goodbye! 👋")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = AIStudyPartner()
    app.run()
