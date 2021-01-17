# Zachary Rossi
# CS 166
# Lab 7

# This program allows a user to make a transaction between wallets and
# have it recorded on the blockchain ledger

# Dependencies
import hashlib
import csv
import json
from miner import mining

# Constnts
MENUCHOICES = ["1","2","3"]
EXITCHOICES = ["y","n"]
WALLETCHOICES = ["wallet1","wallet2","wallet3"]
WALLET1 = "wallet1.csv"
WALLET2 = "wallet2.csv"
WALLET3 = "wallet3.csv"
INITALCOINS = 100

# Sets all the wallets to have a balance of 100 catcoins
def setUp():
    try:
        with open(WALLET1, 'w') as wallet1:
            inital = csv.writer(wallet1)
            inital.writerow([INITALCOINS])
        wallet1.close()
        with open(WALLET2, 'w') as wallet2:
            inital = csv.writer(wallet2)
            inital.writerow([INITALCOINS])
        wallet2.close()
        with open(WALLET3, 'w') as wallet3:
            inital = csv.writer(wallet3)
            inital.writerow([INITALCOINS])
        wallet3.close()
    except:
        print("error creating files")
# Adds the transaction to a the ledger in the ledger.txt
def addToLedeger(wallet1, wallet2, amount):
    try:
        #Opens the orginal ledger
        with open("ledger.txt", "r") as ledger:
            #loads the content as a python dictionary
            blockchain = json.load(ledger)
        #copies the last header
        lastHeader = blockchain['block'+str(len(blockchain)-1)]["header"]
        #Hashes the header using SHA256
        hashedHead = hashlib.sha256(str(lastHeader).encode('utf-8')).hexdigest()
        #Runs the mining puzzle to verify the hash
        nonce, timestamp = mining(hashedHead)
        #Prepares the data in a dictionary format
        data = { "data":{
                "fromWallet": wallet1,
                "toWallet":wallet2,
                "amount": amount
                    }
                 }
        #hashes the data using sha256
        blockData = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        #Creates a new entry in the dictionary of the id of the new block
        blockchain['block'+str(len(blockchain))] = {
        "header": {
                "lastHash": hashedHead,
                "timestamp": str(timestamp),
                "nonce":nonce,
                "hash": blockData 
                },
            "data":{
                "fromWallet": wallet1,
                "toWallet":wallet2,
                "amount": amount
                    }
        }
        ledger.close()
        #opens the ledger and dumps the updated dictionary
        with open("ledger.txt", "w") as ledger:
            json.dump(blockchain, ledger)
        ledger.close()
    except:
        print("Error File not found")
        
#transfers funds from one user to another
def transfer(wallet1, wallet2, amount):
    try:
        #opens the from wallet and finds the value of the coins
        with open(wallet1+".csv", 'r') as fromWallet:
            wallet1Reader = csv.reader(fromWallet)
            for row in wallet1Reader:
                coins1 = float(row[0])
        #Checks to makes sure the wallet has enough coins to transfer
        if coins1 < amount:
            fromWallet.close()
            return False
        else:
            #deducts coins from the  from wallet so it has the correct amount
            fromWallet.close()
            with open(wallet1+".csv", 'w') as fromWallet:
                wallet1writer = csv.writer(fromWallet)
                wallet1writer.writerow([coins1-amount])
            fromWallet.close()
        #finds the amount of coins in the to wallet
        with open(wallet2+".csv", 'r') as toWallet:
            wallet2Reader = csv.reader(toWallet)
            for row in wallet2Reader:
                coins2 = float(row[0])
        toWallet.close()
        with open(wallet2+".csv", 'w') as toWallet:
            wallet2writer = csv.writer(toWallet)
            #adds the correct amount of coins to the to wallet
            wallet2writer.writerow([coins2+amount])
        toWallet.close()
        return True
    except:
        print("Wallet does not exist")

#Checks the balance of coins for a wallet
def checkBalance(choice):
    with open(choice+".csv") as wallet:
        walletReader = csv.reader(wallet)
        for row in walletReader:
            #gets the amount of coins in the wallet
            coins = row[0]
        wallet.close()
    return coins

#Checks the input and makes sure it is valid for the choices given
def validateInput(options):
    dataIncorrect = True
    while(dataIncorrect):
        choice = input("\n>>> ")
        try:
            for i in options:
                if i == choice:
                    return choice
            print("Invalid Choice please enter either one of the choices listed above.")
        except:
           print("Invaid options given")

#Checksthe input of a number to make sure it only contains digits/deciaml
def validateNum():
    dataIncorrect = True
    while(dataIncorrect):
        choice = input("\n>>> ")
        try:
            num = float(choice)
            if num > 0:
                dataIncorrect = False
            else:
                print("Invalid Choice please enter a num > 0")
        except:
            print("Invalid Choice please enter a num")
    return num
    
#The main menu for the program with all the options
def menu():
    print("Please select from the following options")
    print("1. Check Wallet balance")
    print("2. Transfer Catcoins")
    print("3. Quit CatCoin")
    choice = validateInput(MENUCHOICES)
    if choice == "1":
        print("Please select from the following wallets")
        print("wallet1")
        print("wallet2")
        print("wallet3")
        wallet = validateInput(WALLETCHOICES)
        coins = checkBalance(wallet)
        print(wallet+" has "+coins+" Catcoin(s)")
        print("\nReturning to main menu")
        menu()
    elif choice == "2":
        print("Please Select the wallet you want to transfer from")
        print("wallet1")
        print("wallet2")
        print("wallet3")
        wallet1 = validateInput(WALLETCHOICES)
        print("Please Select the wallet you want to transfer to")
        print("wallet1")
        print("wallet2")
        print("wallet3")
        wallet2 = validateInput(WALLETCHOICES)
        print("Enter the amount you want to transfer")
        amount = validateNum()
        print("are you sure you want to transfer",amount,"CatCoins to,",wallet2,"? y/n")
        choice = validateInput(EXITCHOICES)
        if(choice == "y"):
            success = transfer(wallet1, wallet2, amount)
            if(success):
                addToLedeger(wallet1, wallet2, str(amount))
                print("Transaction complete") 
                print(amount,"transfered from",wallet1,"to",wallet2)
            else:
                print("Transfer failed insufficent funds")
            print("\nReturning to main menu")
            menu()
        elif choice == "n":
            menu()
    elif choice == "3":
        print("Are you sure you want to exit CatCoin? y/n")
        choice = validateInput(EXITCHOICES)
        if choice == "y":
            print("Bye")
        elif choice == "n":
            menu()

#Main driver for the function sets up the wallets for every run
def main():
    setUp()
    menu()

main()
