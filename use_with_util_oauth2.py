# -*- coding: utf-8 -*-

"""
An empty bot to be able to start a new bot fast.
Written by /u/SmBe19
"""

import praw
import time
import OAuth2Util

r = praw.Reddit('/u/testiman77 testing only')
o = OAuth2Util.OAuth2Util(r)
o.refresh()

print("START")

submission = r.get_submission(submission_id = '4d0ori')
submission.upvote()
print("VOTING BABE")

submission.replace_more_comments()
flat_comments = praw.helpers.flatten_tree(submission.comments)

i = 0
for i in range(len(flat_comments)):

    if(not flat_comments[i].author):
        continue

    if(flat_comments[i].likes == False):
        continue

    print("DV: %s" %flat_comments[i].body)
    flat_comments[i].upvote()
    time.sleep(2)

print("EXIT")