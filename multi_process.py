'''
Layman: can have multiple instance of same user. Multitask

#Callback link: http://127.0.0.1:65010/authorize_callback

#snow_white_7dwarfs
#lalaboy66

#MarthaKarma
#lalaboy77

#DaMaTaYaDaLa
#lalaboy55

#ThisWordHas8Letters
#lalaboy66

FreeKarma sub no bots allowed
archived post cannot vote/comment

CHANGES MADE:
-now not saving, only load
-now
'''

import sys
from ThisWordHasNLetters import NLettersBot
from bot_comment import ReplyBot
from bot_vote_sub import  SubVoteBot
from praw.handlers import MultiprocessHandler
from bot_class import Bot_Instance

SUB_VISIT_TXT = "sub_visit_time.txt"

#for multiple instances-----------------------------//
handler = MultiprocessHandler('127.0.0.1', 65010)


'''==================================================================//
main function
//=================================================================='''
def Main_Func():

    bot_list = []

    #fansOfHahahahut3
    #FreeKarma
    #create multiple instances-------------//
    ua = '/u/DaMaTaYaDaLa testing only'

    Bot_Instance.Init_Static('AskReddit') #init once static data-------//

    #types of processes to run cocurrently------------------//
    #bot_list.append(ReplyBot(1, ua, handler))
    #bot_list.append(SubVoteBot(2, ua, handler, SUB_VISIT_TXT))
    bot_list.append(NLettersBot(3, ua, handler, 8))

    for i in bot_list:
        try:
            i.start()
        except:
            print("Error: unable to start thread: %d" %i.threadID)

    #multi-thread loop-----------------------//
    while(True):

        #if press end key (NOT GONNA WORK WITH BLOCKING FUNCTIONS)---------------------------//
        if(sys.stdin.read(1) == 'g'):
            print("---END THIS SHIT")
            for h in range(len(bot_list)):
                bot_list[h].end_now = True

            end_counter = 0

            #wait for all threads to end------------------------//
            while(end_counter < len(bot_list)):

                for h in range(len(bot_list)):
                    if(bot_list[h].has_died == False and not bot_list[h].is_alive()):
                        bot_list[h].has_died = True
                        bot_list[h].exit()
                        end_counter += 1

            break

Main_Func()



