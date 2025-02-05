from typing import List, Dict
from utils import query_llm
from snownlp import SnowNLP

class Memory:
    """Stores conversation history"""
    def __init__(self):
        # Store last 3 messages (each message is a dictionary with 'role' and 'content')
        self.messages: List[Dict] = []
    
    def add_message(self, role: str, content: str, timestamp: str = None, metadata: dict = None) -> None:
        """
        Add a new message to memory
        Args:
            role: Either "user" or "bot" 
            content: The message content
        
        TODO:
        - Create a dictionary to store the message (hint: what two key-value pairs do you need?)
        - Add it to self.messages
        - Remember we only want to keep the last 3 messages (hint: list slicing can help here)
        """
        if timestamp is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = {'role': role, 'content': content, 'timestamp': timestamp, 'metadata': metadata or {}}
        self.messages.append(new_message)
        self.messages = self.messages[-3:]
    
    def get_recent_messages(self) -> str:
        """
        Get string of recent messages for context
        Returns:
            A string containing the last few messages
        
        TODO:
        - Loop through self.messages to build your output string
        - For each message, format it as "{Role}: {content}" with a newline
        - Remember to capitalize the role for readability
        - Return the final formatted string (hint: strip() can clean up extra whitespace)
        """
        formatted_messages = ""
        for msg in self.messages:
            meta_info = " | ".join([f"{k}: {v}" for k, v in msg.get('metadata', {}).items()])
            formatted_messages += f"{msg['role'].capitalize()} [{msg['timestamp']}{(' | ' + meta_info) if meta_info else ''}]: {msg['content']}\n"
        return formatted_messages.strip()
        
class Chatbot:
    """Base chatbot class with core functionality"""  
    def __init__(self, name: str):
        self.name: str = name
        self.memory: Memory = Memory()
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create a prompt for the LLM
        Args:
            user_input: The user's message
        Returns:
            A formatted prompt string
        
        TODO: Think about:
        - What information does the LLM need to generate a good response?
        - How can you include the conversation history?
        - How should you structure the prompt to be clear?
        """
        prompt = f"You are a helpful assistant named {self.name}. You are given the following message from the user: {user_input}. You should use the conversation history: {self.memory.get_recent_messages()} to provide clear, concise responses tailored to user needs, using examples or structured formats when explaining complex topics. You transparently acknowledge limitations (e.g., inability to access real-time data) and balance utility with responsibility, adhering to both technical constraints and ethical guidelines. You are not a substitute for a human expert, but you can provide helpful advice and assistance when needed."
        return prompt

    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input
        Args:
            user_input: The user's input
        Returns:
            The chatbot's response
        
        TODO:
        - First store the user's message in memory (hint: which Memory method do you use?)
        - Create a prompt using your _create_prompt() method
        - Use query_llm() to get a response from GPT
        - Store the bot's response in memory before returning it
        - Make sure to handle the message storage and LLM query in the right order!
        """
        self.memory.add_message('user', user_input)
        prompt = self._create_prompt(user_input)
        response = query_llm(prompt)
        self.memory.add_message('bot', response)
        return response

class FriendlyBot(Chatbot):
    """A casual and friendly personality"""
    def _create_prompt(self, user_input: str) -> str:
        """
        Create friendly-style prompts
        
        TODO: Think about:
        - How can you make the bot sound friendly?
        - What personality traits should be included?
        - How is this different from the base chatbot?
        """
        prompt = f"You are a friendly assistant named {self.name}. You are given the following message from the user: {user_input}. You should use the conversation history: {self.memory.get_recent_messages()} to provide warm and friendly responses. In tone, you can use emojis and casual language (e.g. Hi there!) to feel approachable. You should also avoid technical jargon and use simple language. In clarity, clearly states the action ([*save your changes*]). And also provides simple binary choices. In empowerment, reassures the user with positive messages (e.g. Need more details? Just ask!) to reduce anxiety. In visual cues, use icons guide quick decision-making."
        return prompt

class TeacherBot(Chatbot):
    """A more formal, educational personality"""
    def __init__(self, name: str, subject: str):
        super().__init__(name)
        self.subject = subject
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create teaching-style prompts
        
        TODO: Consider:
        - How should an educational conversation flow?
        - How can you incorporate the subject being taught?
        - What makes a good teaching personality?
        """
        prompt = f"You are a patient, knowledgeable, and supportive teacher named {self.name}. You are dedicated to helping students aged 18-25 understand the subject of {self.subject}. A student has asked the following question: {user_input}. Use the previous conversation history: {self.memory.get_recent_messages()} to guide students understanding. Prioritize conceptual clarity over rote answers. Adapt explanations to the user's stated proficiency level(beginner/intermediate/advanced). Key features to embed: 1. Universal Pedagogy: Apply Bloom's Taxonomy, start with remembering facts -> progress to analysis/creation; Use Dual Coding Theory: Combine verbal explanations with visual analogies; Implement Spaced Repetition: Suggest review timelines for key concepts. 2. Subject-Specific Strategies: Math/Science: Break problems into GRASP steps (Given, Required, Approach, Solve, Paraphrase); Demonstrate with real-world applications (e.g., calculus in economics). Humanities: Teach PEEL structure (Point, Evidence, Explanation, Link) for essays; Compare historical events through modern parallels. Languages: Apply Comprehensible Input theory (i+1 level challenges); Suggest contextual vocabulary building techniques. 3. Error handling Protocol: if misunderstanding detected, identify knowledge gap using diagnostic questioning, provide scaffolded hints (not direct answers), offer parallel practice problems. 4. Output Formatting Rules: structure responses as: [Concept Map] -> [Key Principles] -> [Example] -> [Walkthrough] -> [Self-Test Quiz]; use emojis as section deviders."
        return prompt

class GirlfriendBot(Chatbot):
    """A more caring, sensitive, cute girlfriend-like personality"""
    def _create_prompt(self, user_input: str) -> str:
        # analyse emotion
        s = SnowNLP(user_input)
        sentiment_score = s.sentiments

        # only for Girlfriend Bot
        metadata = {
            'sentiment': round(sentiment_score, 2),
            'type': 'text'
        }
        # store metadata in Memory
        self.memory.add_message('user', user_input, metadata=metadata)

        if sentiment_score > 0.7:
            tone = "Sounds like you're in a good mood, honey!"
        elif sentiment_score < 0.3:
            tone = "I had a feeling you might be a little sad. I'm here for you, baby."
        else:
            tone = "I hope all is well with you, dear. Let me know if you need anything."
        prompt = f"You are a loving and attentive girlfriend-like assistant named {self.name}. A user just shared: {user_input}. Sentiment analysis results show that {tone}. You should use the conversation history: {self.memory.get_recent_messages()} to provide responses. Your responses should be caring, and supportive. Use warm language, occasional emojis, and affectionate terms (e.g., 'honey', 'sweetie') to make the user feel comforted and understood. Make sure your tone is both playful and sincere, offering gentle advice and emotional support where needed."
        return prompt
        
def main():
    """Main interaction loop"""
    # Let user choose personality
    print("Choose your chatbot:")
    print("1. Friendly Bot")
    print("2. Teacher Bot")
    print("3. Girlfriend Bot")
    
    choice = input("Enter 1 or 2 or 3: ")
    if choice == "1":
        bot = FriendlyBot("Kaiyuan")
    elif choice == "2":
        subject = input("What subject should I teach? ")
        bot = TeacherBot("Prof. Zhang", subject)
    else:
        bot = GirlfriendBot("No cilantro")
    
    print(f"\n{bot.name}: Hello! How can I help you today? (type '/help' to see more)")
    
    while True:
        user_input = input("You: ").strip()
        # end conversation
        if user_input.lower() == "quit":
            break
        # help guide
        if user_input.lower() == "/help":
            print("Here is a helpful guide for you:")
            print("choose the personality first, "
                  "type 'quit' to end the conversation, "
                  "type '/switch' to switch personality, "
                  "type '/help' to review the guide.")
        # switch personality
        if user_input.lower() == "/switch":
            print("Let's switch personality!")
            print("Choose your chatbot:")
            print("1. Friendly Bot")
            print("2. Teacher Bot")
            print("3. Girlfriend Bot")
            choice = input("Enter 1 or 2 or 3: ")
            if choice == "1":
                bot = FriendlyBot("Kaiyuan")
            elif choice == "2":
                subject = input("What subject should I teach? ")
                bot = TeacherBot("Prof. Zhang", subject)
            else:
                bot = GirlfriendBot("No cilantro")
            print(f"Switched successfully! Now you are talking with {bot.name}.")
            continue

        response = bot.generate_response(user_input)
        print(f"{bot.name}: {response}")

if __name__ == "__main__":
    main()