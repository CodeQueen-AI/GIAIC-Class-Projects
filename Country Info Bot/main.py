country_data = {
    "Pakistan": {
        "capital": "Islamabad",
        "language": "Urdu",
        "population": "241 million"
    },
    "France": {
        "capital": "Paris",
        "language": "French",
        "population": "68 million"
    },
    "Japan": {
        "capital": "Tokyo",
        "language": "Japanese",
        "population": "125 million"
    }
}

# Agent 1: Capital Finder
def capital_agent(country):
    return country_data.get(country, {}).get("capital", "Unknown capital")

# Agent 2: Language Finder
def language_agent(country):
    return country_data.get(country, {}).get("language", "Unknown language")

# Agent 3: Population Finder
def population_agent(country):
    return country_data.get(country, {}).get("population", "Unknown population")

# Orchestrator Agent
def orchestrator_agent(country):
    capital = capital_agent(country)
    language = language_agent(country)
    population = population_agent(country)

    return f"📍 Country: {country}\n🏛️ Capital: {capital}\n🗣️ Language: {language}\n👥 Population: {population}"

# Example usage
print(orchestrator_agent("Pakistan"))
print()
print(orchestrator_agent("Japan"))
