'''
This bot UPVOTES to comments that fits critia

DO NOT CALL SAVE DATA as might cause threads to conflict
'''

import praw
import time
from bot_class import Bot_Instance
from bot_class import Perma_to_subreddit
latest_visit_time_txt_comment = "last_comment_time.txt"

class ReplyBot(Bot_Instance):

    '''==================================================================//
    Init
    super(D, self).__init__()
    //=================================================================='''
    def __init__(self, threadID, user_agent, handler):

        #login--------------------------------------//
        super(ReplyBot, self).__init__(threadID, user_agent, handler)

        #variables------------------------------//
        self.latest_comment_visit_time = 0
        self.latest_comment_id = 0

        #last visit time---------------------------//
        fo = open(latest_visit_time_txt_comment, "r")
        full = fo.read(100).split('\n')

        #if not first time, get the last latest time-------------------------//
        self.latest_comment_visit_time = float(full[0])
        self.latest_comment_id = full[1]
        fo.close()

    '''==================================================================//
    main loop
    //=================================================================='''
    def run(self):

        #Call super----------------------------//
        super(ReplyBot, self).run()

        comment_stream = praw.helpers.comment_stream(self.r, Bot_Instance.subs_string, 10)

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
    Can comment
    //=================================================================='''
    def Check_Condition(self, comment):

        if(not comment.author): #if deleted
            return False

        if(comment.author == self.r.user): #if own comment
            return False

        if(comment.created_utc <= self.latest_comment_visit_time): #if upvote b4
            return False

        if(comment.id == self.latest_comment_id): #if upvote b4
            return False

        if(comment.likes == True or comment.likes == False): #voted b4
           return False

        return True

    '''==================================================================//
    Carry out action
    //=================================================================='''
    def CarryOut_Action(self, comment):

        subname = Perma_to_subreddit(comment.permalink)
        comment.upvote()
        Bot_Instance.comment_uv_count[subname] += 1

        self.latest_comment_visit_time = comment.created_utc
        self.latest_comment_id = comment.id

        #save the latest time----------------//
        fo = open(latest_visit_time_txt_comment, "w")  #write the updated index to txt file
        fo.write(str(self.latest_comment_visit_time) + '\n')
        fo.write(str(self.latest_comment_id))
        fo.close()

        #save the latest data---------------------------//
        Bot_Instance.CheckData()

        time.sleep(2)

    '''==================================================================//
    Exit
    //=================================================================='''
    def exit(self):

        #Call super----------------------------//
        super(ReplyBot, self).exit()