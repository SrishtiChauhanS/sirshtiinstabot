import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import termcolor

import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from clarifai.rest import ClarifaiApp

APP_ACCESS_TOKEN = '4388624854.d5a4b3a.327fa44e9db443e598e2d4066d92ff92'
#Token Owner : srishtichauhan1196.main
#list_of_sandbox  : ['princechauhan3133','ananyagupta5623','ysyuvraj079']

BASE_URL = 'https://api.instagram.com/v1/'


# Function declaration to get your own info



def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'



# Function declaration to get the ID of a user by username



def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()



# Function declaration to get the info of a user by username



def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'



# Function declaration to get your recent post



def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



# Function declaration to get the recent post of a user by username



def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# Function declaration to get the ID of the recent post of a user by username


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()




# Function declaration to like the recent post of a user



def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

# Get likes list

def get_like_list(insta_username):
        media_id = get_post_id(insta_username)
        request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)

        print 'GET request url : %s' % (request_url)
        like_list = requests.get(request_url).json()
        print like_list

        if like_list['meta']['code'] == 200:
            if len(like_list['data']):
                for i in range(0, len(like_list['data'])):
                    print 'Username: %s' % (like_list['data'][i]['username'])

            else:
                print 'There is no like for this user media!'
        else:
            print 'Query was unsuccessful!'


# Function declaration to make a comment on the recent post of the user


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


# Function declaration to get the liked by user


def liked_by_user(insta_username):
    media_id = get_post_id(insta_username)
    print "Get request URL:" + ((BASE_URL + "users/self/media/liked?access_token=%s") % (APP_ACCESS_TOKEN))
    liked = requests.get((BASE_URL + "users/self/media/liked?access_token=%s") % (APP_ACCESS_TOKEN)).json()
    print liked["data"][0]["id"]

# Function declaration to get the comments

def get_the_comments(insta_username):
    media_id = get_post_id(insta_username)
    print "Get request URL:" + ((BASE_URL + "media/%s/comments?access_token=%s") % (media_id, APP_ACCESS_TOKEN))
    comments = requests.get((BASE_URL + "media/%s/comments?access_token=%s") % (media_id, APP_ACCESS_TOKEN)).json()
    print comments["data"]

# Function declaration to make delete negative comments from the recent post

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


#define array
#defining dictionary and stored imageurl and words
ar = []
my_dictionary = {
    'imageurl': None,
    'words': ''

}
user_lis = ['princechauhan3133', 'ananyagupta5623']

#function to show the subtrend of a travel and plot through wordcloud
#objective to show subtrend of any activities or event and plot through word cloud
#defining clarifaiApp with generated key
app = ClarifaiApp(api_key='de07e73879da40b4a65dee60367a0626')

# get the general model
model = app.models.get('travel-v1.0')
for user in user_lis:
    def get_users_post(user):
        user_id = get_user_id(user)
        if user_id == None:
            print 'User does not exist!'
            exit()
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_media = requests.get(request_url).json()

        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                image_name = user_media['data'][0]['id'] + '.jpeg'
                image_url = user_media['data'][0]['images']['standard_resolution']['url']
                model = app.models.get('food-items-v1.0')
                response = model.predict_by_url(url=image_url)
                #data fetched through concepts and stored in response
                for x in response['outputs'][0]['data']['concepts']:
                    #print name stored in value
                    print x['name'], x['value']
                    #if value of x greater than .7
                    if x['value'] > .7:
                        #string show the value of x in name
                        strr = x['name']
                        #using temp variable to fetch words stored in dictionary
                        temp = my_dictionary['words']
                        temp = temp + ' ' + str(strr)
                        my_dictionary['words'] = temp
                        #string stored in a dictionary as a words
                String = my_dictionary['words']
                print
                wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1200, height=1000).generate(
                    String)
                plt.imshow(wordcloud)
                plt.axis('off')
                plt.show()
                urllib.urlretrieve(image_url, image_name)
            else:
                print "error"

        else:
            print "error"




def start_bot():
    while True:
        print '\n'
        print termcolor.colored('Hey! Welcome to instaBot!','red')
        print termcolor.colored('Here are your menu options:','blue')
        print termcolor.colored("A.Get your own details\n",'magenta')
        print termcolor.colored("B.Get details of a user by username\n",'magenta')
        print termcolor.colored("C.Get your own recent post\n",'magenta')
        print termcolor.colored("D.Get the recent post of a user by username\n",'magenta')
        print termcolor.colored("E.Get a list of people who have liked the recent post of a user\n",'magenta')
        print termcolor.colored("F.Like the recent post of a user\n",'magenta')
        print termcolor.colored("G.Get a list of comments on the recent post of a user\n",'magenta')
        print termcolor.colored("H.Make a comment on the recent post of a user\n",'magenta')
        print termcolor.colored("I.Delete negative comments from the recent post of a user\n",'magenta')
        print termcolor.colored("J.Get a list of people who have liked the recent post of a user\n",'magenta')
        print termcolor.colored("K.Show Subtrends of travel \n",'magenta')
        print termcolor.colored("L.Exit\n",'cyan')

        choice = raw_input("Enter you choice: ")
        if choice == "A":
            self_info()
        elif choice == "B":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "C":
            get_own_post()
        elif choice == "D":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="E":
           insta_username = raw_input("Enter the username of the user: ")
           liked_by_user(insta_username)
        elif choice=="F":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="G":
           insta_username = raw_input("Enter the username of the user: ")
           get_the_comments(insta_username)
        elif choice=="H":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="I":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "J":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice=="K":
            get_users_post(user)
        elif choice=="L":
            exit()
        else:
            print termcolor.colored("Sorry, wrong choice. Try Again",'red')

start_bot()