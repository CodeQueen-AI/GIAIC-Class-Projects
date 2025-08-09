# from agents import Agent , Runner , RunContextWrapper , function_tool , RunContextWrapper
# from config import config
# from pydantic import BaseModel

# class Account(BaseModel):
#     name : str
#     pin : int

# def check_user(ctx:RunContextWrapper[Account], agent:Agent) -> bool:
#     if ctx.context.name == 'CodeQueen' and ctx.context.pin == '12345':
#         return True
#     else:
#         return False


# @function_tool(is_enabled=check_user)
# def check_balance(account_number : str) -> str:
#     return f"The balance of account is $10000000"

# bank_agent = Agent (
#     name = 'Bank Agent',
#     instructions= 'You are Bank agent answer the queries of the customer related to the bank accounts and there balance information but be sure the user is authenticated.',
#     tools=[check_balance]
# )

# user_context = Account(name='CodeQueen' , pin='12345' )

# result = Runner.run_sync(bank_agent, 
#                          f'I want to know my balance, my account number is 23456',
#                          context=user_context,
#                          run_config=config)


# print(result.final_output)

# Financial Analysis
# Bank se related

# Use the Guardrails in the Bank Agent



from agents import Agent, Runner, RunContextWrapper, function_tool
from config import config
from pydantic import BaseModel

# -------------------------
# Context Data Model
# -------------------------
class Account(BaseModel):
    name: str
    pin: str
    account_number: str

# -------------------------
# Input Guardrails
# -------------------------
def validate_user_input(ctx: RunContextWrapper[Account], agent: Agent) -> bool:
    # Check name
    if not ctx.context.name.isalpha():
        return False
    # Check pin is 5 digits
    if not (ctx.context.pin.isdigit() and len(ctx.context.pin) == 5):
        return False
    # Check account number format
    if not (ctx.context.account_number.isdigit() and len(ctx.context.account_number) == 5):
        return False
    return True

# -------------------------
# Authentication Function
# -------------------------
def check_user(ctx: RunContextWrapper[Account], agent: Agent) -> bool:
    return ctx.context.name == 'CodeQueen' and ctx.context.pin == '12345'

# -------------------------
# Tools (Functions)
# -------------------------
@function_tool(is_enabled=check_user)
def check_balance(account_number: str) -> str:
    if account_number != "23456":
        return "Sorry, account number not found."
    return "The balance of account is $10,000,000."

@function_tool(is_enabled=check_user)
def transfer_funds(account_number: str, amount: float) -> str:
    if account_number != "23456":
        return "Transfer failed: Account not found."
    if amount <= 0:
        return "Invalid transfer amount."
    if amount > 5000:
        return "Transfer limit exceeded. Max $5000 per transaction."
    return f"${amount} has been transferred successfully."

# -------------------------
# Agents
# -------------------------
bank_agent = Agent(
    name="Bank Agent",
    instructions="You are a bank agent. Only give account info if the user is authenticated.",
    tools=[check_balance, transfer_funds]
)

fraud_agent = Agent(
    name="Fraud Detection Agent",
    instructions="You check for suspicious activity and warn the customer if needed."
)

# -------------------------
# Output Guardrails
# -------------------------
def filter_output(output: str) -> str:
    # Prevent revealing sensitive info like PIN
    if "12345" in output:
        return "Sensitive information cannot be displayed."
    return output

# -------------------------
# User Context
# -------------------------
user_context = Account(
    name="CodeQueen",
    pin="12345",
    account_number="23456"
)

# -------------------------
# Run with validation
# -------------------------
if validate_user_input(RunContextWrapper(user_context), bank_agent):
    result = Runner.run_sync(
        bank_agent,
        "I want to know my balance, my account number is 23456",
        context=user_context,
        run_config=config
    )
    print(filter_output(result.final_output))
else:
    print("Invalid input. Please check your details and try again.")
