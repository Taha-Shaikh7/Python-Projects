import random
num=random.randint(1,100)
print("Guess the number game between 1 to 100")
print("You have 5 chances to enter the correct number")
for i in range(5):
    guess=input("Enter the number: ")
    if num==guess:
        print("You win")
    elif num!=guess:
        print("you lose")
    else:
        print("Invalid")
print("The number was: ",num)