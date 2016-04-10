'''
Creates an instance and login with auth
'''
from threading import Event, Thread
from flask import Flask, request
import _thread
import praw

app = Flask(__name__)

REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'
has_authorized = False

'''==================================================================//
Internal functions
//=================================================================='''
@app.route('/')
def homepage():
    link_no_refresh = r.get_authorize_url('UniqueKey', 'identity vote')
    link_refresh = r.get_authorize_url('DifferentUniqueKey', 'identity vote',
                                       refreshable=True)
    link_no_refresh = "<a href=%s>link</a>" % link_no_refresh
    link_refresh = "<a href=%s>link</a>" % link_refresh
    text = "First link. Not refreshable %s</br></br>" % link_no_refresh
    text += "Second link. Refreshable %s</br></br>" % link_refresh
    return text

@app.route('/authorize_callback')
def authorized():

    global has_authorized
    has_authorized = True
    state = request.args.get('state', '')
    code = request.args.get('code', '')
    info = r.get_access_information(code)
    user = r.get_me()
    variables_text = "State=%s, code=%s, info=%s." % (state, code,
                                                      str(info))
    text = 'You are %s and have %u link karma.' % (user.name,
                                                   user.link_karma)
    print("FUCK FUCK FUCK")
    '''
    submission = r.get_submission(submission_id = '4d0ori')
    submission.upvote()
    print("VOTING BABE")'''

    back_link = "<a href='/'>Try again</a>"
    return variables_text + '</br></br>' + text + '</br></br>' + back_link

def fgf():
    while(True):
        print("ASDASD")

'''==================================================================//
Call this function for getting a praw instance logged in
//=================================================================='''
def GetLoggedInPraw(name, useragent, _CLIENT_ID, _CLIENT_SECRET):

    #the global PRAW object--------------------------//
    global r
    r = praw.Reddit(useragent)

    r.set_oauth_app_info(_CLIENT_ID, _CLIENT_SECRET, REDIRECT_URI)


    print("BEFORE")
    _thread.start_new_thread ( app.run(debug=True, port=65010), ())
    print("AFTER")

    global has_authorized
    while(has_authorized == False):
        continue
    global has_authorized
    has_authorized = False

    submission = r.get_submission(submission_id = '4d0ori')
    submission.upvote()
    print("VOTING BABE")

    return r


#testiman77
#lalaboy66
GetLoggedInPraw('testiman77', '/u/testiman77 testing only', 'VUc0r5PL3t1y1w', 'wRH_xO3g0hRWmFTw2Ov9b69EILg')