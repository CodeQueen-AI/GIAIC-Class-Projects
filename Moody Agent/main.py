import asyncio
from agents import Agent, Runner
from main import config

# Agent 1: Mood Analyzer
mood_agent = Agent(
    name="Mood Analyzer",
    instructions="Analyze the user's message and return only one word for the mood, such as: happy, sad, excited, angry, or stressed. Only return the mood.",
)

# Agent 2: Activity Recommender
activity_agent = Agent(
    name="Activity Recommender",
    instructions="Suggest a relaxing or uplifting activity for someone who is feeling sad or stressed. Be kind and encouraging in your response.",
)

async def main():
    print("🧠 Mood Analyzer with Handoff (powered by Agents SDK)")
    user_input = input("🗣️ How are you feeling today? ")

    # Step 1: Run Mood Analyzer
    mood_result = await Runner.run(mood_agent, user_input, run_config=config)
    mood = mood_result.final_output.strip().lower()

    print(f"\n🧠 Detected Mood: {mood}")

    # Step 2: Run Activity Recommender if mood is sad/stressed
    if mood in ["sad", "stressed"]:
        activity_result = await Runner.run(activity_agent, f"The user is feeling {mood}.", run_config=config)
        print("\n🎯 Suggested Activity:")
        print(activity_result.final_output.strip())
    else:
        print("\n😊 You're doing great! Keep enjoying your day!")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())