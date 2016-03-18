from twitter import *
from twitter.follow import *
from twitter.cmdline import *
from argparse import ArgumentParser
from time import sleep
from secrets import con_key, con_secret

#my_twitter_creds = os.path.expanduser('~/.twitter_creds')
my_twitter_creds2 = ('/home/Ayda_Twitter/twitter_credsinwage2')
if not os.path.exists(my_twitter_creds2):
    oauth_dance('managemick', con_key, con_secret, my_twitter_creds2)

oauth_token, oauth_secret = read_token_file(my_twitter_creds2)

twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, con_key, con_secret))


openfile = open('/home/Ayda_Twitter/copylist.txt')
content = openfile.read()
openfile.close()

split = content.splitlines()
touse = ''
if len(split) >0:
    openfile = open('/home/Ayda_Twitter/copylist.txt','w+')
    touse = split[0]
    for index, line in enumerate(split):
        if index > 0:
            openfile.writelines(line+'\n')
    openfile.writelines(touse)
    openfile.close()
print touse


parser = ArgumentParser(
    description="Twitter unfollow and follow API")

parser.add_argument('-m', '--myaccount', help="my account")
parser.add_argument('-c', '--copyaccount', help="account to copy followers")
args = parser.parse_args()
#print twitter.application.rate_limit_status()

myaccount = 'bitwage'
copyaccount = touse

#delete all people not following back
if myaccount and copyaccount:
    print myaccount
    #people following
    followingme = follow(twitter, myaccount, False)
    #print lookup(twitter, userids)
    #followers
    myfollowers = follow(twitter, myaccount, True)
    #print lookup(twitter, followers)

    tounfollow = []
    for id in followingme:
        if id not in myfollowers:
            tounfollow.append(id)
    print len(tounfollow)
    #print lookup(twitter, tounfollow)
    #uncomment below when u run
    for k, v in lookup(twitter, tounfollow).iteritems():
        print v
        sleep(20)
        try:
            twitter.friendships.destroy(screen_name=v)
        except Exception as (e):
            print e
sleep(10000)
#copy followers of copyaccount
if myaccount and copyaccount:
    print copyaccount

    #followers
    copyfollowers = follow(twitter, copyaccount, True)

    tofollow = []
    for id in copyfollowers:
        if id not in myfollowers and id not in followingme:
            tofollow.append(id)
    print len(tofollow)
    #print lookup(twitter, tofollow)
    #uncomment below when u run
    for count, (k, v) in enumerate(lookup(twitter, tofollow).iteritems()):
        if count < 400:
            print v
            sleep(100)
            try:
                twitter.friendships.create(screen_name=v)
            except Exception as (e):
                print e
                if 'unable to follow more people at this time.' in str(e) or 'cannot perform write actions' in str(e):
                    exit()
