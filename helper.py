from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    num_messages = df.shape[0]
    word = []
    for msg in df['message']:
        word.extend(msg.split())

    num_media = df[df['message'].str.lower() == '<media omitted>'].shape[0]

    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))

    return num_messages, len(word), num_media, len(links)



def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts().head()/df.shape[0])*100,2).reset_index()
    return x,df

def create_word_cloud(selected_user,df):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines()


    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    df = df[df['message'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']

    words = []
    for msg in df['message']:
        for word in msg.lower().split():
            if word not in stopwords:
                words.append(word)
    final_text = " ".join(words)



    # Generate WordCloud

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(final_text)


def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    df = df[df['message'] != 'group_notification']
    df = df[~df['message'].str.lower().str.contains('media omitted', na=False)]

    f = open('stop_hinglish.txt', 'r')
    stopword = f.read()
    words = []
    for msg in df['message']:
        for word in msg.lower().split():
            if word not in stopword:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_df(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([char for char in message if emoji.is_emoji(char)])


    emoji_data = pd.DataFrame(Counter(emojis).most_common(10), columns=['Emoji', 'Count'])
    return  emoji_data


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    timeline= df.groupby(['year', 'month', 'month_name']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month_name'][i] + "-" + str(timeline['year'][i])))
    timeline['time'] = time
    return timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    daily = df.groupby('only_date').count()['message'].reset_index()
    return daily

def weekly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap









#         f = open('stop_hinglish.txt','r')
#         stopword = f.read()
#         temp_df = df[df['message'] != 'group_notification']
#         temp = temp_df[temp_df['user_message'] != '<Media omitted>\n']
#
#         words = []
#         for msg in temp['message']:
#             for word in msg.lower().split():
#                 if word not in stopword:
#                     words.append(msg.split())
#
#        cleaned_text = []
#     for msg in df['messages']:
#         msg = msg.lower()
#         words = [word for word in msg.split() if word not in stopwords]
#         cleaned_text.extend(words)
#
#     final_text = " ".join(cleaned_text)



