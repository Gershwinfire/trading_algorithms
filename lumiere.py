import kucoin_helpers
import time


#This is going to be Lumiere himself. The man, the bot, the first iteration and legend.
########IMMEDIATELY BEGIN KEEPING rounds of data. 
                    #Leave room for INFO: in database to allow comment made to first and last entry in database for round
                        ##This will allow for easy diefin tin
                    #look forward to using minimax  
                    
starting_account_balance = kucoin_helpers.doge_musk_check_balance()
print(f"BEGINNING BALANCE: {starting_account_balance}")

list_of_winLOSS = []
####Start keeping this data
total_times_to_run = input("How many times should we run this data: ")
total_times_to_run = int(total_times_to_run)
for i in range(total_times_to_run):
    answer = kucoin_helpers.execute_doge_musktrade()
    list_of_winLOSS.append(answer)
    time.sleep(0.5)
failure = 0
success = 0
for outcome in list_of_winLOSS:
    if outcome == "Failure":
        failure += 1
    if outcome == "Success":
        success += 1


ending_account_balance = kucoin_helpers.doge_musk_check_balance()


total_PNL = ending_account_balance - starting_account_balance

print(f"SUCCESS: {success}\nFailure: {failure}")
print(f"BEGINNING BALANCE: {starting_account_balance}")
print(f"ENDING BALANCE: {ending_account_balance}")
print(f"PNL : {total_PNL}")
    
   
