from twitter import *
from twitter.follow import *
from twitter.cmdline import *
from argparse import ArgumentParser
from time import sleep
from secrets import con_key, con_secret
from random import randint

#my_twitter_creds = os.path.expanduser('~/.twitter_creds')
my_twitter_creds2 = ('/home/ubuntu/Ayda_Twitter/twitterbot/twitter_credsinwage2')
if not os.path.exists(my_twitter_creds2):
    oauth_dance('managemick', con_key, con_secret, my_twitter_creds2)

oauth_token, oauth_secret = read_token_file(my_twitter_creds2)

twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, con_key, con_secret))


openfile = open('/home/ubuntu/Ayda_Twitter/twitterbot/copylist.txt')
content = openfile.read()
openfile.close()

split = content.splitlines()
touse = ''
if len(split) >0:
    openfile = open('/home/ubuntu/Ayda_Twitter/twitterbot/copylist.txt','w+')
    touse = split[0]
    for index, line in enumerate(split):
        if index > 0:
            openfile.writelines(line+'\n')
    openfile.writelines(touse)
    openfile.close()
print 'Account: ' + touse + 'will be followed'


parser = ArgumentParser(
    description="Twitter unfollow and follow API")

parser.add_argument('-m', '--myaccount', help="my account")
parser.add_argument('-c', '--copyaccount', help="account to copy followers")
args = parser.parse_args()
#print twitter.application.rate_limit_status()

myaccount = 'PancakeMick'
copyaccount = touse

#delete all people not following back
if myaccount and copyaccount:
    #print myaccount
    #people following
    followingme = follow(twitter, myaccount, False)
    #print lookup(twitter, userids)
    #followers
    myfollowers = follow(twitter, myaccount, True)
    #print lookup(twitter, followers)
    print 'These people are following me: ' 
    print myfollowers
    tounfollow = []
    for id in followingme:
        if id not in myfollowers:
            tounfollow.append(id)
    print len(tounfollow)
    #print lookup(twitter, tounfollow)
    #uncomment below when u run
    print 'These people will be unfollowed '
    print tounfollow
    for k, v in lookup(twitter, tounfollow).iteritems():
        print v
        sleep(randint(5,25))
        try:
            twitter.friendships.destroy(screen_name=v)
        except Exception as (e):
            print e
sleep(randint(1000,2000))
#copy followers of copyaccount
if myaccount and copyaccount:
    print 'This account will be followed: ' + copyaccount

    #followers
    copyfollowers = follow(twitter, copyaccount, True)

    sleep(randint(500,1200))
    tofollow = []
    for id in copyfollowers:
        if id not in myfollowers and id not in followingme:
            tofollow.append(id)
    print len(tofollow)
    #print lookup(twitter, tofollow)
    #uncomment below when u run
    for count, (k, v) in enumerate(lookup(twitter, tofollow).iteritems()):
        if count < 400:
            sleep(randint(50,250))
            try:
                twitter.friendships.create(screen_name=v)
                print 'Now Following: ' + v
            except Exception as (e):
                print e
                if 'unable to follow more people at this time.' in str(e) or 'cannot perform write actions' in str(e):
                    exit()
