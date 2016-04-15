'''
Find words that has n letters
'''

import praw
import time
from bot_class import Bot_Instance
ALPHABET_LIST = 'abcdefghijklmnopqrstuvwxyz'

'''==================================================================//
split word to list, only alpha allowed, change them to lower
//=================================================================='''
def WordToList(raw_word):

    #turn string into list first----------------//
    word = list(raw_word.lower())

    for i in range(len(word)):

        #if is non-alpha, replace with whitespace, easier to split-----------//
        if(word[i].isalpha() == False):
            word[i] = ' '

    #create list of words--------------------------//
    daList = []

    #if not space, keep pushing characters------------------//
    first_encount = True    #first encounter alpha
    for i in range(len(word)):

        #if alpha-----------------------//
        if(word[i] != ' '):

            #if see first time------------//
            if(first_encount):
                daList.append('') #add a string
                first_encount = False

            daList[-1] += word[i]
        else:
            first_encount = True #next time encounter alpha, considered FIRST

    return daList

'''==================================================================//
Get parent ID from comment permalink
//=================================================================='''
def GetSubID_FromPerma(perma):
    start = perma.find('comments/') + 9
    end = perma.find('/', start)
    return perma[start:end]

class NLettersBot(Bot_Instance):

    '''==================================================================//
    Init
    super(D, self).__init__()
    //=================================================================='''
    def __init__(self, threadID, user_agent, handler, numLetters):

        #login--------------------------------------//
        super(NLettersBot, self).__init__(threadID, user_agent, handler)

        #variables------------------------------//
        self.numLetters = numLetters
        self.latestTime = time.time()

        #for comparing last replied time-----//
        self.lastRepliedTime = 0

        self.word_limit = 10 #only find up till 10 words

    '''==================================================================//
    main loop
    //=================================================================='''
    def run(self):

        #Call super----------------------------//
        super(NLettersBot, self).run()

        comment_stream = praw.helpers.comment_stream(self.r, Bot_Instance.subs_string, 0)

        for c in comment_stream:

            #login access-----------------------------------------//
            self.o.refresh()

            #comment function-----------------------------------------//
            if self.Check_Condition(c):
                self.CarryOut_Action(c)

            #exit---------------------------------//
            if(self.end_now == True):
                break


    '''==================================================================//
    Can comment:
    //=================================================================='''
    def Check_Condition(self, comment):

        if(not comment.author): #if deleted
            return False
        if(comment.author == self.r.user): #if own comment
            return False
        if(comment.is_root == False): #not root comment
           return False
        if(comment.created_utc <= self.latestTime):
            return False
        if(comment.likes == True or comment.likes == False): #voted b4
           return False
        return True

    '''==================================================================//
    Carry out action
    //=================================================================='''
    def CarryOut_Action(self, comment):

      #  print("-Checking: %s" %comment.body)

        #check if contain word with 'n' letters
        List_of_words = []
        count = 0

        #split as long as not alphabet
        gg = WordToList(comment.body)
        for word in gg:

            if(count >= self.word_limit):
                break

            if(len(word) == self.numLetters):

                #check if word is repeat--------------//
                is_inside_alr = False

                for hh in List_of_words: #word is repeat :(

                    if(word == hh):
                        is_inside_alr = True
                        break

                if(is_inside_alr == False):
                    List_of_words.append(word)

                count += 1

        #reply back if MORE than 10 minutes since last reply--------------------------------//
        # and time.time() - self.lastRepliedTime >= 600
        if(len(List_of_words) > 0 and time.time() - self.lastRepliedTime >= 1200):

            #check to make sure is not from Serious sub-----------------------//
            sub_id = GetSubID_FromPerma(comment.permalink)
            sub_obj = self.r.get_submission(submission_id = sub_id)

            if("[Serious]" not in sub_obj.title):

                self.lastRepliedTime = time.time()

                #reply-----------------------------------//
                reply_str = ">"

                #list of words---------------------------------//
                for hh in List_of_words:
                    reply_str += hh + " "

                reply_str += "\n\n"

                if(len(List_of_words) > 1):
                    reply_str += "These words have " + str(self.numLetters) + " letters"
                else:
                    reply_str += "This word has " + str(self.numLetters) + " letters"

                comment.reply(reply_str)

                time.sleep(2)

    '''==================================================================//
    Exit
    //=================================================================='''
    def exit(self):

        #Call super----------------------------//
        super(NLettersBot, self).exit()