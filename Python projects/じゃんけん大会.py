import random

alice_wins = 0
bob_wins = 0
options = ["pedra", "papel", "tesoura"]

while True:
    alice_input = input("Escreva pedra/papel/tesoura ou q para sair: ").lower()
    
    if alice_input == "q":
        break

    if alice_input not in options:
        continue

    random_number = random.randint(0, 2)
    bob_pick = options[random_number]
    
    print("Bob escolheu", bob_pick + ".")

    if alice_input == bob_pick:
        print("Empate")

    elif bob_pick == "pedra" and alice_input == "papel":
        print("Alice ganhou")
        alice_wins += 1

    elif bob_pick == "tesoura" and alice_input == "pedra":
        print("Alice ganhou")
        alice_wins += 1

    elif bob_pick == "papel" and alice_input == "tesoura":
        print("Alice ganhou")
        alice_wins += 1

    else:
        print("Perdeu")
        bob_wins += 1

print(f"Bob ganhou {bob_wins} vezes.")
print(f"Alice ganhou {alice_wins} vezes.")
print("Ate logo")