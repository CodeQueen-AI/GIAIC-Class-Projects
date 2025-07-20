from agents import Agent, Runner
from main import config

# Step 1: Create your agent
agent = Agent(
    name='Smart Store Agent',
    instructions='You are a helpful medical assistant Suggest a treatment or product based on symptoms Explain clearly',
)

# Step 2: Command Line Loop
print("Type your health issue or 'exit' to quit\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        print("👋 Goodbye! Stay healthy")
        break

    # Step 3: Run agent dynamically with input
    result = Runner.run_sync(agent, user_input, run_config=config)

    print("\n🤖 Gemini Suggestion:\n" + result.final_output.strip() + "\n")