import random
import time

print("======================================")
print("      🎮 ROCK - PAPER - SCISSORS 🎮")
print("======================================")
print("Rules: Rock beats Scissors, Scissors beats Paper, Paper beats Rock")
print("Type 'quit' anytime to exit.\n")

choices = ["rock", "paper", "scissors"]

user_score = 0
computer_score = 0

while True:
    user = input("Enter your choice (rock/paper/scissors): ").lower()

    # Exit game
    if user == "quit":
        print("\nGame Ended!")
        print(f"Final Score → You: {user_score} | Computer: {computer_score}")
        print("Thanks for playing! 👋")
        break

    # Checking valid input
    if user not in choices:
        print("❌ Invalid choice! Try again.\n")
        continue

    computer = random.choice(choices)
    print(f"Computer is thinking...", end="")
    time.sleep(0.8)
    print(f"\rComputer chose: {computer}")

    # Game logic
    if user == computer:
        print("🔸 It's a draw!")
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        print("✔ You win this round!")
        user_score += 1
    else:
        print("❗ Computer wins this round!")
        computer_score += 1

    print(f"Score → You: {user_score} | Computer: {computer_score}\n")
    print("--------------------------------------")
