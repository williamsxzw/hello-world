###############################################################################
from split import Spliddit

if __name__ == "__main__":
    # create a instance of Spliddit and show the menu
    score_machine = Spliddit()    
    score_machine.show_menu()
    
    # keep user in program using while loop, break only when Q is selected
    # each option will bring user to the corresponding function
    # of an instance of Spliddit program
    
    while 1:
        option = input('\n\tPlease choose an option and press <Enter>:')
        if score_machine.check_option(option):
            if option == "A":
                score_machine.option_a()
            elif option == "C":
                score_machine.option_c()
            elif option == "V":
                score_machine.option_v()         
            elif option == "S":
                score_machine.option_s()
            elif option == "Q":
                score_machine.option_q()
                break
            else:
                print('\noption not valid, please choose from {}'\
                  .format(score_machine.valid_options))
        else:
            print('\noption not valid, please choose from {}'\
                  .format(score_machine.valid_options))