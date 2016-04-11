'''
base class for bot instance(is a Thread)

IMPORTANT: THIS BOT CLASS IS MEANT FOR ONE ACCOUNT WITH MANY INSTANCES, NOT MANY ACCOUNTS

static variables welcome here
'''

from __future__ import with_statement # 2.5 only
import OAuth2Util
import praw
import threading
from threading import Lock
import datetime

DATA_TXT = "data.txt"

'''==================================================================//
Find string in list:
Yes: returns pos
No: returns -1
//=================================================================='''
def FindInList_str(theList, findMe):
    for i in range(len(theList)):
        if(findMe in theList[i]):
            return i
    return -1

'''==================================================================//
Get subreddit from perma
//=================================================================='''
def Perma_to_subreddit(perma):
    start = perma.find('r/') + 2
    end = perma.find('/comments')
    subreddit = perma[start:end]
    return subreddit

class Bot_Instance (threading.Thread):

    #STATIC-------------------------------------//
    #sync----------------------//
    lock = Lock()

    #dictionary-------------------//
    comment_uv_count = {}
    link_uv_count = {}

    #subreddit string---------//
    subs_string = "" #combine 1 or more subs
    sub_list = []   #same as above, but in list

    #misc--------------//
    current_day = 77

    #ENUM--------------------------------//
    COMMENT_POS = 0
    LINK_POS = 1
    TOTAL_POS = LINK_POS + 1

    '''==================================================================//
    Init static (CALL ONCE)
    //=================================================================='''
    @staticmethod
    def Init_Static(subs_string):
        print("|-------- INIT STATIC DATA NOW --------|")

        #get subreddit list------------------------//
        Bot_Instance.subs_string = subs_string

        #load common static data---------------------//
        Bot_Instance.load_static_data()


    '''==================================================================//
    Init
    multiple subreddit: "pics+funny+mildlyinteresting"
    //=================================================================='''
    def __init__(self, threadID, user_agent, handler):

        #thread module start-------------------------//
        threading.Thread.__init__(self)

        #login--------------------------------------//
        self.r = praw.Reddit(user_agent, h = handler)
        self.o = OAuth2Util.OAuth2Util(self.r)
        self.o.refresh()
        self.threadID = threadID

        #CORE-------------------------------------//
        self.has_died = False
        self.end_now = False

    '''==================================================================//
    Run function: OVERLOAD and CALL
    //=================================================================='''
    def run(self):
        print("|---STARTING BOT THREAD ID: %d" %self.threadID)


    '''==================================================================//
    Exit function: OVERLOAD AND CALL
    //=================================================================='''
    def exit(self):
        print("|---EXITING BOT THREAD ID: %d" %self.threadID)


    '''==================================================================//
    check day and save data
    //=================================================================='''
    @staticmethod
    def CheckData():

        with Bot_Instance.lock: #multithread
            #check, if not same day, reset------------------------//
            i = datetime.datetime.now()

            #CHECK if its a new day-------------------------//
            if(Bot_Instance.current_day != i.day):
                Bot_Instance.current_day = i.day

                print("|---CHANGE OF DAY!!!")

                #RESET-------------------------//
                for i in Bot_Instance.sub_list:
                    Bot_Instance.comment_uv_count[i] = 0
                    Bot_Instance.link_uv_count[i] = 0

            #resafe everything-------------------//
            Bot_Instance.save_static_data()

    '''==================================================================//
    Load data at init (MUST CALL ONCE)
    //=================================================================='''
    @staticmethod
    def load_static_data():

        #multiple subreddit list-----------------------//
        Bot_Instance.sub_list = Bot_Instance.subs_string.split('+')

        #populate the dict of comment and link-------------//
        for i in Bot_Instance.sub_list:
            Bot_Instance.comment_uv_count[i] = 0
            Bot_Instance.link_uv_count[i] = 0

        #open this text file in read mode only
        fo = open(DATA_TXT, "r")

        #pass contents to a string
        str = fo.read(1000)

        #if no data yet, go out-----------------------//
        if(len(str) < 2):
            fo.close()
            Bot_Instance.CheckData()
            return

        listOfWords = str.split('\n')

        #find if the subreddit is already saved, if not, create new entry------------//
        for sub_name in Bot_Instance.sub_list:
            print("|---Sub: %s" %sub_name)

            #see is previously saved-----------------------------//
            line_pos = FindInList_str(listOfWords, "S: " + sub_name)

            #YES, is saved b4------------------------------------//
            if (line_pos != -1):

                #get link and comment values---------------------//
                line_pos += 1
                Bot_Instance.comment_uv_count[sub_name] = int(listOfWords[line_pos + Bot_Instance.COMMENT_POS])
                Bot_Instance.link_uv_count[sub_name] = int(listOfWords[line_pos + Bot_Instance.LINK_POS])
                print("COMMENT SO FAR: %d" %Bot_Instance.comment_uv_count[sub_name] )
                print("LINK SO FAR: %d" %Bot_Instance.link_uv_count[sub_name] )


        #current day: last index----------------------//
        Bot_Instance.current_day = int( listOfWords[-1][listOfWords[-1].find(':') + 1:len(listOfWords[-1])] )
        print("LAST DAY: %d" %Bot_Instance.current_day)

        #close
        fo.close()

        #resave again just in case-------------------//
        Bot_Instance.CheckData()

    '''==================================================================//
    Save data
    //=================================================================='''
    @staticmethod
    def save_static_data():

        #save the latest time----------------//
        fo = open(DATA_TXT, "w")  #write the updated index to txt file

        #FOLLOW THE FUCKING ORDER FROM ENUM----------------------------------//
        for i in Bot_Instance.sub_list:
            fo.write("S: " + i + '\n')
            fo.write(str(Bot_Instance.comment_uv_count[i]) + '\n')
            fo.write(str(Bot_Instance.link_uv_count[i]) + '\n')

        #last line will be the day of last online--------------------//
        fo.write("Day: " + str(Bot_Instance.current_day))
        fo.close()