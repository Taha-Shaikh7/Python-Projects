import random
print("           Rock Paper Scissor Game")
choices=["rock","paper","scissor"]
for i in range(5):
    computer=random.choice(choices)
    game=input("\nEnter the any 1 of them: ")
    
    if game not in choices:
        print("Invalid")
        
    elif (game=="rock" and computer=="paper")or(game=="scissor" and computer=="rock")or (game=="paper" and computer=="scissor"):
        print("Computer: ",computer)
        print("You lose")

    elif (game=="paper" and computer=="rock") or (game=="scissor" and computer=="paper")or (game=="rock" and computer=="scissor"):
        print("Computer: ",computer)
        print("You Win")

    else:
        print("Computer: ",computer)
        print("Its tie")
