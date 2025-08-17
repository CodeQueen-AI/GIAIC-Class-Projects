from agents import Agent, Runner, RunContextWrapper
from agents import function_tool, input_guardrail
from pydantic import BaseModel
from typing import Optional
from config import config  

# User Context Model
class UserContext(BaseModel):
    name: str
    member_id: Optional[str] = None  

user = UserContext(name="CodeQueen", member_id="12345")
context = RunContextWrapper(user)

# Guardrail
@input_guardrail
def guard_input(query: str) -> bool:
    keywords = ["book", "availability", "library", "timing"]
    return any(word in query.lower() for word in keywords)

# Tools
@function_tool
def search_book(book_name: str) -> str:
    available_books = ["Python Basics", "Data Science 101", "Machine Learning Guide", "AI Revolution"]
    if book_name in available_books:
        return f"✅ Book '{book_name}' is available in our library."
    return f"❌ Book '{book_name}' not found in the library."

@function_tool
def check_availability(book_name: str, member_id: str = None) -> str:
    if member_id is None:
        return "❌ Only registered members can check availability."
    copies_dict = {
        "Python Basics": 5,
        "Data Science 101": 2,
        "Machine Learning Guide": 0,
        "AI Revolution": 3,
    }
    if book_name not in copies_dict:
        return f"❌ Book '{book_name}' not found."
    copies = copies_dict[book_name]
    return f"📚 '{book_name}' has {copies} copies available." if copies > 0 else f"❌ '{book_name}' is out of stock."

@function_tool
def library_timings() -> str:
    return "⏰ The library is open from 9 AM to 8 PM, Monday to Saturday."

# Library Agent
library_agent = Agent(
    name="Library Assistant",
    instructions="You help users with library-related queries like searching books, checking availability, and library timings.",
    tools=[search_book, check_availability, library_timings]
)

# Interactive Loop
print("📚 Welcome to Library Assistant!")
print("Type your question about books, availability, or library timings.")
print("Type 'exit' to quit.\n")

while True:
    query = input("❓ Your question: ")
    if query.lower() == "exit":
        print("👋 Goodbye!")
        break
    
    result = Runner.run_sync(
        library_agent,
        query,
        run_config=config
    )
    print(f"👉 Answer: {result.final_output}\n")
