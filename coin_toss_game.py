import random
print("         Heads and Tails Game")
choices=["heads","tails"]
for i in range(5):
    computer=random.choice(choices)
    user=input("\nEnter the anyone of them: ")

    if user not in choices:
        print("Invalid")
        
    elif computer==user:
        print("you Win")
    
    else:
        print("Computer:",computer)
        print("You Lose")
