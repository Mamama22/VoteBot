'''
Replies to all root comments of a SUBMISSION
'''

import praw
import time
from bot_class import Bot_Instance

class IT_HelpdeskBot(Bot_Instance):

    '''==================================================================//
    Init
    super(D, self).__init__()
    //=================================================================='''
    def __init__(self, threadID, user_agent, handler, subID):

        #login--------------------------------------//
        super(IT_HelpdeskBot, self).__init__(threadID, user_agent, handler)

        #variables------------------------------//
        self.latestTime = time.time()
        self.subID = subID

        #for comparing last replied time-----//
        self.lastRepliedTime = 0

    '''==================================================================//
    main loop
    //=================================================================='''
    def run(self):

        #Call super----------------------------//
        super(IT_HelpdeskBot, self).run()

        start_index = 0

        #keep looping my friend.............
        while(True):

            submission = self.r.get_submission(submission_id = self.sub_id)

            submission.replace_more_comments()
            root_comments = submission.comments
            #flat_comments = praw.helpers.flatten_tree(submission.comments) ONLY need root comments

            i = start_index
            while(i < len(root_comments)):

                #login access-----------------------------------------//
                self.o.refresh()

                #comment function-----------------------------------------//
                if self.Check_Condition(root_comments[i]):
                    self.CarryOut_Action(root_comments[i])

                #counter-----------------//
                i += 1

            #set last index------------------------------//
            start_index = i

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

        comment.reply("HI, FUCK U\n\n^^I am a fucking bot")
        time.sleep(2)

    '''==================================================================//
    Exit
    //=================================================================='''
    def exit(self):

        #Call super----------------------------//
        super(IT_HelpdeskBot, self).exit()