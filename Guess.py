import random

number = random.randint(1, 100)
guess = 0
attempts = 0

while guess != number:
    attempts += 1
    guess = int(input("Guess a number between 1 and 100: "))

    if guess < number:
        print("Your guess is too low!")
    elif guess > number:
        print("Guess is too high!")
    else:
        print(f"You guessed right after {attempts} attempts")
        break
print("Thanks For Playing")            