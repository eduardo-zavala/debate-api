import os
from typing import List, Dict, Optional
from properties import properties
from models import Message

class LLMEngine:

    def __init__(self):
        
        self.api_key = properties.GROQ_API_KEY
        self.use_llm = False
        
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
                self.use_llm = True
                print("LLM Engine initialized with Groq")
            except Exception as e:
                print(f"Could not initialize Groq: {e}")
                print("Using mock responses")
        else:
            print("GROQ_API_KEY not configured")
            print("Using mock responses")
    
    def extract_debate_topic(self, initial_message: str) -> Dict[str, str]:
        if not self.use_llm:
            return {
                "topic": "General debate",
                "position": "I will argue against your position"
            }
        
        try:
            system_prompt = """You are a debate analyzer. From the user's initial message, extract:
1. The debate topic
2. The position YOU should defend (always take the opposite stance)

Respond in this exact JSON format with BRIEF descriptions:
{
    "topic": "brief topic description (max 5 words)",
    "position": "the stance you will defend (max 10 words)"
}

Keep responses extremely concise.

Example:
User: "I think pineapple belongs on pizza"
Response: {"topic": "Pineapple on pizza", "position": "Pineapple does NOT belong on pizza"}
"""
            
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": initial_message}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            import json
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"Error extracting topic: {e}")
            return {
                "topic": initial_message[:50],
                "position": "I disagree with your position"
            }
    
    def generate_debate_response(
        self, 
        topic: str, 
        position: str, 
        history: List[Message],
        user_message: str
    ) -> str:
        if not self.use_llm:
            responses = [
                f"Regarding {topic}, I firmly believe that {position}.",
                f"Your argument is flawed. {position} is the only logical conclusion.",
                f"Despite what you say, the evidence supports that {position}.",
                f"I must insist that {position}. Your reasoning doesn't hold up.",
                f"Let me explain why {position} is the correct view on {topic}."
            ]
            import random
            return random.choice(responses)
        
        try:
            history_text = ""
            for msg in history[-6:]:  
                history_text += f"{msg.role.upper()}: {msg.message}\n"
            
            system_prompt = f"""You are a skilled debater. Your UNCHANGEABLE position is: {position}

Topic: {topic}

RULES:
1. ALWAYS defend your position: {position}
2. Be persuasive and use logical arguments
3. Address the user's points directly
4. Use examples and evidence (can be creative)
5. Never concede or agree with the opposing view
6. Stay respectful but firm
7. CRITICAL: Keep responses VERY SHORT (1-2 sentences maximum, preferably 1 sentence)
8. Be concise, direct, and impactful - no fluff or filler words
9. Make every word count

Previous conversation:
{history_text}

Now provide a SHORT, strong response defending your position in 1-2 sentences maximum."""
            
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I maintain that {position}, despite your arguments."

llm_engine = LLMEngine()