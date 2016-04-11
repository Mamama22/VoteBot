'''
This bot upvotes LINK SUBMISSION ONLY (replies too)
'''

import praw
import time
from bot_class import Bot_Instance
from bot_class import Perma_to_subreddit

class SubVoteBot(Bot_Instance):

    '''==================================================================//
    Init
    super(D, self).__init__()
    //=================================================================='''
    def __init__(self, threadID, user_agent, handler, latest_visit_time_txt):

        #login--------------------------------------//
        super(SubVoteBot, self).__init__(threadID, user_agent, handler)

        #Variables---------------------//
        self.latest_sub_visit_time = 0 #the last submission created time in previous visit
        self.latest_sub_ID = 0  #D of latest visited post (So we do not go to it again)

        #LATEST SUB VISIT TIME: load from save file----------------------//
        fo = open(latest_visit_time_txt, "r")
        full = fo.read(100).split('\n')


        #if not first time, get the last latest time-------------------------//
        self.latest_sub_visit_time = float(full[0])
        self.latest_sub_ID = full[1]
        fo.close()

        #Get the latest time form previous visit---------------------------------------//
        self.latest_visit_time_txt = latest_visit_time_txt

    '''==================================================================//
    Check sub time if is skippable
    //=================================================================='''
    def Check_sub_time(self, sub):

        #if comment is too early, do not DV--------------------------------------------//
        if(sub.created_utc >= self.latest_sub_visit_time):
            return False
        return True

    '''==================================================================//
    Get reply
    //=================================================================='''
    def Reply(self, subname, comment):

        #the total karma given in string form------------------------------------//
        link_uv_str = str(Bot_Instance.link_uv_count[subname])
        comment_uv_str = str(Bot_Instance.comment_uv_count[subname])

        #overall-------------------------------------------------------------------//
        overall_link = 0
        overall_comment = 0
        for i in Bot_Instance.sub_list:
            overall_link += Bot_Instance.link_uv_count[i]
            overall_comment += Bot_Instance.comment_uv_count[i]

        reply_str = ""

        if(subname == 'fansOfHahahahut3' or subname == 'fansOfHahahahut4'):
            reply_str += "Upvoted link post\n\n"
            reply_str += "##Karma given today:\n\n"
            reply_str += "#####" + subname + ":\n\n"
            reply_str += ">Link:`" + link_uv_str + "`" + " Comment:`" + comment_uv_str + "`\n\n"
            reply_str += "#####Overall:\n\n"
            reply_str += ">Link:`" + str(overall_link) + "`" + " Comment:`" + str(overall_comment) + "`\n\n"
            #reply_str += "***\n\n^An ^upvote ^a ^day ^keeps ^the ^mods ^away"
        else:
            reply_str += "Upvoted you:)"

        comment.add_comment(reply_str)

    '''==================================================================//
    main loop
    //=================================================================='''
    def run(self):

        #Call super----------------------------//
        super(SubVoteBot, self).run()

        sub_stream = praw.helpers.submission_stream(self.r, Bot_Instance.subs_string, 20)

        #loop thru submissions from earliest to latest--------------------------------//
        for c in sub_stream:

            if(not c.author): #if deleted
                continue

            #login access-----------------------------------------//
            self.o.refresh()

            #submission ID check-------------------------------//
            if( self.Check_sub_time(c) == True):
                print("---skipping....")
                continue

            #if like b4... do not go in again------------------------//
            #if(c.likes == True or c.likes == False):
            #    continue
            if(c.id == self.latest_sub_ID): #test ID check
                continue

            #reset data if end of day--------------------------//
            Bot_Instance.CheckData()

            #print title--------------------------------------------//
            if('https://www.reddit.com/r/' not in c.url):

                subname = Perma_to_subreddit(c.permalink)
                print("Sub Text: %s" %c.permalink)

                c.upvote()
                Bot_Instance.link_uv_count[subname] += 1 #upvoted a link

                #reply comment made------------------------------//
                self.Reply(subname, c)

                #save and sleep for 2 secs-----------------------------------//
                self.save_sub_time_and_data(c) #save latest submission time and data
                time.sleep(2)

            else:
                print("IS NOT LINK POST: %s" %c.url)

            #exit---------------------------------//
            if(self.end_now == True):
                break

    '''==================================================================//
    Save data
    //=================================================================='''
    def save_sub_time_and_data(self, submission):

        self.latest_sub_visit_time = submission.created_utc
        self.latest_sub_ID = submission.id

        #save the latest time----------------//
        fo = open(self.latest_visit_time_txt, "w")  #write the updated index to txt file
        fo.write(str(self.latest_sub_visit_time) + '\n')
        fo.write(str(self.latest_sub_ID))
        fo.close()

        #save the latest data---------------------------//
        Bot_Instance.CheckData()

    '''==================================================================//
    Exit
    //=================================================================='''
    def exit(self):

        #Call super----------------------------//
        super(SubVoteBot, self).exit()