"""
This code is written by Python 3.3, so some of the syntax is slightly different,
for example, when printing, Python 3 uses print(), Python 2 uses print 
one may need to remove all the () of printing when running in Python 2

This part of code works for tweets in between 2011 and 2012, 
those in 2009 to 2010, which contains data for ipad1, has different format, 
so some part has to be re-written in another file.
"""

"""
# Section 1: read data from the raw 'all_tweets.tsv' file
# extract time and texts, remove non-us users by time zones 
# save those data in an output file named 'us_tweets.txt' for future use
"""

#us_time_zones is used to extract tweets that are only posted by users whose time zone is in us
us_time_zones = ['Hawaii', 'Alaska', 'Pacific Time (US & Canada)', 'Arizona', 'Mountain Time (US & Canada)', 'Central Time (US & Canada)', 'Eastern Time (US & Canada)', 'Indiana']
data = []
num_raw_data = 0

# a method to print the first few elements in a list
def print_first_few_element(a_list, end):
    for a in a_list[0:end]:
        print(a)

# a method to print all elements in a list to an output file
def print_output_file(a_list, output_file_name):
    outfile = open(output_file_name, 'w')
    for line in a_list:
        try:
            print(line[0] + '\t' + line[1], file = outfile)
        except:
            pass

# read file, the file name is 'ipad.tsv' when we first downloaded from Aron,
# we changed it to 'all_tweets.tsv'
with open('all_tweets.tsv', mode='r', encoding='utf8') as tsv:
    for line in tsv:
        num_raw_data += 1
        
        line = line.strip().split('\t')
        time = line[1].split('=')[1]
        text = line[4][5:].lower()
        
        if len(line[10].split('=')) > 1:
            time_zone = line[10].split('=')[1]
            if time_zone in us_time_zones: # remove tweets that are not in us by time zones
                data.append((time, text))

# print number of raw data and filtered data
print('number of raw data: ', num_raw_data)
print('number of data after removing non-us messages: ', len(data))
# print the first ten elements as example
print('\nThe first ten elements are:')
print_first_few_element(data, 10)
#write all the data in a file for future use
print_output_file(data, 'us_tweets.txt')

# calculate the number of tweets per day
num_tweets_per_day = {}
for line in data:
    time = line[0].split(' ')
    key = time[0] + ' '+ time[1] + ' ' + time[2] + ' ' + time[5]
    if key in num_tweets_per_day:
        num_tweets_per_day[key] += 1
    else:
        num_tweets_per_day[key] = 1
# print the number of tweets per day to a txt file
outfile = open('us_tweets_num_per_day.txt', 'w')
for key, value in num_tweets_per_day.items():
    print(key + '\t' + str(value), file = outfile)

"""
# Section 2: separate data by different products
# save those data in different files
"""

# a method that search for data of a particular product
def find_product(product, not_product_list):
    results = []
    for element in data:
        if product in element[1]:
            is_not_product = False
            for n in not_product_list:
                if n in element[1]:
                    is_not_product = True
            if not is_not_product:
                results.append(element)
    return results

# a method that search for the data of a particular product between a start date and end date
def find_product_event_tweets(input_data, start_date, end_date):
    results = []
    for element in input_data:
        dates = element[0].split(' ')
        month = dates[1]
        date = int(dates[2])
        year = int(dates[5])
        
        if start_date[2] == end_date[2]: # determine if year is the same, it is always the same actually  
            if start_date[0] == end_date[0]: # determine if month is the same, looking for tweets in the same month
                if year == start_date[2]: 
                    if month == start_date[0]:
                        if date >= start_date[1] and date <= end_date[1]:
                            results.append(element)
            else: # month is different
                if month == start_date[0]:
                    if date >= start_date[1]:
                        results.append(element)
                elif month == end_date[0]:
                    if date <= end_date[1]:
                        results.append(element)
        else: # year is different, which never happened in this work
            if year == start_date[2]:
                if month == start_date[0]:
                    if date >= start_date[1]:
                        results.append(element)
            elif year == end_date[2]:
                if month == end_date[0]:
                    if date <= end_date[1]:
                        results.append(element)
    return results

# define a function to remove punctuations in a tweet
# - _ ' " are not in the punctuation list since they might be in a word
punctuation_list = ('#', '!', '.', ':', ';', ',', '"', '?', '>', '<', '&', '%', '^', '(', ')', '+', '=', '{', '}', '[', ']', '|')

# remove punctuation in a tweet
def remove_punctuation(input_list):
    output_list = []
    for line in input_list:
        tweet_no_punctuation = ''.join(c for c in line[1] if c not in punctuation_list)
        output_list.append([line[0], tweet_no_punctuation])
    return output_list

# remove URL in a tweet
def remove_url(input_list):
    output_list = []
    for line in input_list:
        new_tweet = ''
        for word in line[1].split(' '):
            if 'http' in word:
                pass
            else:
                new_tweet += ' ' + word
        output_list.append([line[0], new_tweet.strip()])
    return output_list

"""
# Part1: Apple
"""
# ipad:
not_ipad = [] # not_ipad contains words that should not in tweets talking about ipad, like 'ipada'
for i in range(26):
    not_ipad.append(chr(ord('a')+i) + 'ipad')
    not_ipad.append('ipad' + chr(ord('a')+i))
not_ipad.remove('ipadd') # 'ipadd', 'ipads' should not be removed because people always talk about ipad like this 
not_ipad.remove('ipads')
not_ipad.remove('ipadi') #'ipadi' and 'eipad' should not be removed because people always talk about ipad with iphone like 'iphoneipad' or 'ipadiphone'
not_ipad.remove('eipad')

# find all the ipad tweets
data_ipad = find_product('ipad', not_ipad)

# print number of ipad tweets and the first ten example                
print('\nnumber of tweets mentioning ipad:',len(data_ipad))        
print('\nThe first ten elements are:')
print_first_few_element(data_ipad, 10)

# find out the different tweets about different versions of ipad
data_ipad2 = find_product_event_tweets(data_ipad, ['Feb', 25, 2011], ['Mar', 25, 2011])
data_ipad2 = remove_url(remove_punctuation(data_ipad2))

data_ipad3 = find_product_event_tweets(data_ipad, ['Mar', 2, 2012], ['Mar', 30, 2012])
data_ipad3 = remove_url(remove_punctuation(data_ipad3))

data_ipad4_mini = find_product_event_tweets(data_ipad, ['Oct', 17, 2012], ['Nov', 16, 2012])
data_ipad4_mini = remove_url(remove_punctuation(data_ipad4_mini))

# output these results
print_output_file(data_ipad2, 'us_tweets_ipad2.txt')
print('\nnumber of tweets mentioning ipad2:',len(data_ipad2))        
print('\nThe first ten elements are:')
print_first_few_element(data_ipad2, 10)

print_output_file(data_ipad3, 'us_tweets_ipad3.txt')
print('\nnumber of tweets mentioning ipad3:',len(data_ipad3))        
print('\nThe first ten elements are:')
print_first_few_element(data_ipad3, 10)

print_output_file(data_ipad4_mini, 'us_tweets_ipad4_mini.txt')
print('\nnumber of tweets mentioning ipad4 and ipad mini:',len(data_ipad4_mini))        
print('\nThe first ten elements are:')
print_first_few_element(data_ipad4_mini, 10)

# iphone:
not_iphone = [] # not_iphone contains nothing, since the word 'iphone' does not appear in other cases
data_iphone = find_product('iphone', not_iphone)

data_iphone4s = find_product_event_tweets(data_iphone, ['Sep', 30, 2011], ['Oct', 28, 2011])
data_iphone4s = remove_url(remove_punctuation(data_iphone4s))

data_iphone5 = find_product_event_tweets(data_iphone, ['Sep', 7, 2012], ['Oct', 5, 2012])
data_iphone5 = remove_url(remove_punctuation(data_iphone5))

print_output_file(data_iphone4s, 'us_tweets_iphone4s.txt')
print('\nnumber of tweets mentioning iphone4s:',len(data_iphone4s))        
print('\nThe first ten elements are:')
print_first_few_element(data_iphone4s, 10)

print_output_file(data_iphone5, 'us_tweets_iphone5.txt')
print('\nnumber of tweets mentioning iphone5:',len(data_iphone5))        
print('\nThe first ten elements are:')
print_first_few_element(data_iphone5, 10)

"""
# Part2: Amazon
"""
# kindle fire
not_kindle = []
data_kindle = find_product('kindle', not_kindle)

not_fire = []
data_fire = find_product('fire', [])

# the kindle fire file is searched when there are both 'kindle' and 'fire' in a tweet
data_kindlefire = [a for a in data_kindle if a in data_fire]

data_kindlefire1 = find_product_event_tweets(data_kindlefire, ['Nov', 1, 2011], ['Nov', 30, 2011])
data_kindlefire1 = remove_url(remove_punctuation(data_kindlefire1))

data_kindlefire2 = find_product_event_tweets(data_kindlefire, ['Aug', 30, 2012], ['Sep', 28, 2012])
data_kindlefire2 = remove_url(remove_punctuation(data_kindlefire2))

print_output_file(data_kindlefire1, 'us_tweets_kindlefire1.txt')
print('\nnumber of tweets mentioning kindle fire 1:',len(data_kindlefire1))        
print('\nThe first ten elements are:')
print_first_few_element(data_kindlefire1, 10)

print_output_file(data_kindlefire2, 'us_tweets_kindlefire2.txt')
print('\nnumber of tweets mentioning kindle fire 2:',len(data_kindlefire2))        
print('\nThe first ten elements are:')
print_first_few_element(data_kindlefire2, 10)

"""
# Part 3: Google
"""
# nexus
not_nexus = [] # not_iphone contains nothing, since the word 'nexus' does not appear in other cases
data_nexus = find_product('nexus', not_nexus)
# didn't search for google, since people may use 'nexus' instead of 'google nexus'

data_nexus7 = find_product_event_tweets(data_nexus, ['Jun', 29, 2012], ['Jul', 30, 2012])
data_nexus7 = remove_url(remove_punctuation(data_nexus7))

data_nexus4_10 = find_product_event_tweets(data_nexus, ['Oct', 26, 2012], ['Nov', 28, 2012])
data_data_nexus4_10 = remove_url(remove_punctuation(data_nexus4_10))

print_output_file(data_nexus7, 'us_tweets_nexus7.txt')
print('\nnumber of tweets mentioning nexus 7:',len(data_nexus7))        
print('\nThe first ten elements are:')
print_first_few_element(data_nexus7, 10)

print_output_file(data_nexus4_10, 'us_tweets_nexus4_10.txt')
print('\nnumber of tweets mentioning nexus 4 and 10:',len(data_nexus4_10))        
print('\nThe first ten elements are:')
print_first_few_element(data_nexus4_10, 10)

"""
# Section 3: read the sentimentword.txt file and analyze tweets
# part of speech label is done by standford POS in java and is converted to sentiWordNet label format
# Please refer to the 'Stanford_POS.java' for POS labeling
"""

#read the sentiwordnet file and calculate the avarage of each word#POS
sentiwordnet_dict = {}
with open('SentiWordNet_3.0.0_20130122.txt') as infile:
    line_num = 0
    for line in infile:
        line_num += 1
        if line_num <= 27: # the first 27 lines are not word list
            pass
        else:
            line = line.split('\t')
            words_with_pound = line[4].split(' ')
            
            pos_score = float(line[2]) # positive score for a word
            neg_score = float(line[3]) # negative score for a word
            
            for word_with_pound in words_with_pound:
                word = word_with_pound.split('#') # extract words
                word[0] += "#" + line[0] # label each word with its part of speech
                
                if word[0] in sentiwordnet_dict:
                    score = sentiwordnet_dict[word[0]] # score is a list for each word#pos
                    score[0] += pos_score              # it has positive score, negative score and number of appearance in the SentiWordNet list
                    score[1] += neg_score
                    score[2] += 1
                    sentiwordnet_dict[word[0]] = score
                else:
                    score = [pos_score, neg_score, 1]
                    sentiwordnet_dict[word[0]] = score

# calculate average score for each word#pos and remove those neutral words by threshold
remove_neutral = []
threshold_is_neutral = 0
# if both the positive and negative scores are 0, thye won't contribute to the analysis, so remove this word                                
for key, score in sentiwordnet_dict.items():
    if score[0] == threshold_is_neutral and score[1] == threshold_is_neutral:
        remove_neutral.append(key)
    if score[2] > 1:
        score[0] /= score[2]
        score[1] /= score[2]
                    
print('\norginal length of sentiwordnet dictionary: ', len(sentiwordnet_dict))
print('\nnumbers of neutral words: ', len(remove_neutral))
# remove neutral words
for key in remove_neutral:
    del sentiwordnet_dict[key]
print('\nlength of sentiwordnet dictionary after removing neutral words: ', len(sentiwordnet_dict))
# print some samples
print('\nSample results of SentiWordNet are:')
print('good#a', sentiwordnet_dict['good#a'])
print('good#n', sentiwordnet_dict['good#n'])
print('bad#a', sentiwordnet_dict['bad#a'])


# convert stanford POS to sentiWordNet format
noun_list = ['EX', 'FW', 'NN', 'NNP', 'NNPS', 'NNS', 'POS', 'PRP', 'PRP$', 'RP', 'SYM', 'WP', 'WP$', 'WPB']
adjective_adverb_list = ['CC', 'CD', 'DT', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'PDT', 'RB', 'RBR', 'TO', 'UH', 'WDT']
verb_list = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

# this method converts standford POS label to sentiWordNet label format
# eg, if word label is _NN, I convert it to #n
# sentiWordNet only has three types of labels, so 
# anything that is noun or pronoun is considered as #n
# anything that is verb is considered as #v
# anything left in the stanford label is considered as #a

def file_pos_to_file_sentiwordnet_label(file_name):
    new_tweet_list = []
    with open(file_name) as infile:
        for line in infile:
            old_tweet_words = line.split('\t')[1].split(' ')
            new_tweet = []
            for word in old_tweet_words:
                if '_' in word:
                    word_pos = word.split('_')[1]
                    word = word.split('_')[0]
                    if word_pos in noun_list:
                        new_tweet.append(word + '#n')
                    elif word_pos in adjective_adverb_list:
                        new_tweet.append(word + '#a')
                    elif word_pos in verb_list:
                        new_tweet.append(word + '#v')
            new_tweet_list.append([line.split('\t')[0], new_tweet])
    return new_tweet_list

# this method does the sentiment_analysis by iterating through each tweets
# and find the word also in the sentiWordNet and add up the scores
def sentiment_analysis(listName_sentiment_label):
    sentiment_list = []
    for element in listName_sentiment_label:
        pos_score = 0
        neg_score = 0
        num_word = 0
        for x in element[1]:  
            for key,value in sentiwordnet_dict.items():
                if x == key:
                    pos_score += value[0]
                    neg_score += value[1]
                    num_word += 1
        if num_word > 0:
            sentiment_list.append([element[0], [pos_score, neg_score, num_word]])
    return sentiment_list

# print the output file of sentiment analysis
def print_output_file_sentiment(a_list, output_file_name):
    outfile = open(output_file_name, 'w')
    for line in a_list:
        try:
            print(line[0] + '\t' + str(line[1][0]) + ' ' + str(line[1][1]) + ' ' + str(line[1][2]), file = outfile)
        except:
            pass

# a method that calculate the sentiment score for different products and output the results to files
def create_sentiment_file_print_sample(file_name):
    sentiwordnet_label = file_pos_to_file_sentiwordnet_label(file_name)
    sentiment = sentiment_analysis(sentiwordnet_label)
    output_file_name = file_name.split('POS')[0] + 'sentiment.txt'
    print_output_file_sentiment(sentiment, output_file_name)
    print('\nThe first ten elements are:')
    print_first_few_element(sentiment, 10)

# ipad1 is also calculated here since the format does not matter
create_sentiment_file_print_sample('us_tweets_ipad1_POS.txt')
create_sentiment_file_print_sample('us_tweets_ipad2_POS.txt')
create_sentiment_file_print_sample('us_tweets_ipad3_POS.txt')
create_sentiment_file_print_sample('us_tweets_iphone4s_POS.txt')
create_sentiment_file_print_sample('us_tweets_iphone5_POS.txt')
create_sentiment_file_print_sample('us_tweets_kindlefire1_POS.txt')
create_sentiment_file_print_sample('us_tweets_kindlefire2_POS.txt')
create_sentiment_file_print_sample('us_tweets_nexus7_POS.txt')

"""
# Section 4: calculate daily sentiment values
"""
# format a number to 4 decimal points
def num_format(num):
    return float('%.4f' % num)

# this is a method that calculate total score of positive and negative tweets in each day
def calculate_daily_sentiment_total_tweet(file_name):
    daily_sentiment_dict = {}
    with open(file_name) as infile:
        for line in infile:
            dates = line.split('\t')[0].split(' ')
            days_of_week = dates[0]
            month = dates[1]
            day = dates[2]
            year = dates[5]
            pos_score = float(line.split('\t')[1].split(' ')[0])
            neg_score = float(line.split('\t')[1].split(' ')[1])
            num_word = float(line.split('\t')[1].split(' ')[2])
            dates_string = days_of_week + ' ' + month + ' ' + str(day) + ' ' + str(year)
            # normalize each tweet score to [0, 1] and add up the total
            if dates_string in daily_sentiment_dict:
                daily_sentiment_dict[dates_string][0] += pos_score / num_word
                daily_sentiment_dict[dates_string][1] += neg_score / num_word
                daily_sentiment_dict[dates_string][2] += 1
            else:
                daily_sentiment_dict[dates_string] = [pos_score / num_word, neg_score / num_word, 1]
    output_file_name = file_name.split('_sentiment')[0] + '_daily_sentiment_total_tweet.txt'
    outfile = open(output_file_name, 'w')
    for key, value in daily_sentiment_dict.items():
        key = key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2] + '\t' + key.split(' ')[3]
        print(key + '\t' + str(num_format(value[0])) + '\t' + str(num_format(value[1])) + '\t' + str(num_format(value[0] - value[1])) + '\t' + str(value[2]), file = outfile)

# this is a method that calculate total score of positive and negative words in each day
def calculate_daily_sentiment_total_word(file_name):
    daily_sentiment_dict = {}
    with open(file_name) as infile:
        for line in infile:
            dates = line.split('\t')[0].split(' ')
            days_of_week = dates[0]
            month = dates[1]
            day = dates[2]
            year = dates[5]
            pos_score = float(line.split('\t')[1].split(' ')[0])
            neg_score = float(line.split('\t')[1].split(' ')[1])
            num_word = float(line.split('\t')[1].split(' ')[2])
            dates_string = days_of_week + ' ' + month + ' ' + str(day) + ' ' + str(year)
            # do not normalize each tweet score, add up the positive and negative score directly
            if dates_string in daily_sentiment_dict:
                daily_sentiment_dict[dates_string][0] += pos_score
                daily_sentiment_dict[dates_string][1] += neg_score
                daily_sentiment_dict[dates_string][2] += num_word
            else:
                daily_sentiment_dict[dates_string] = [pos_score / num_word, neg_score / num_word, num_word]
    output_file_name = file_name.split('_sentiment')[0] + '_daily_sentiment_total_word.txt'
    outfile = open(output_file_name, 'w')
    for key, value in daily_sentiment_dict.items():
        key = key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2] + '\t' + key.split(' ')[3]
        print(key + '\t' + str(num_format(value[0])) + '\t' + str(num_format(value[1])) + '\t' + str(num_format(value[0] - value[1])) + '\t' + str(value[2]), file = outfile)

# this is a method that calculate total score of numbers positive and negative tweets in each day
threshold_pos_neg = 0
def calculate_daily_pos_neg_tweets(file_name):
    daily_sentiment_dict = {}
    with open(file_name) as infile:
        for line in infile:
            dates = line.split('\t')[0].split(' ')
            days_of_week = dates[0]
            month = dates[1]
            day = dates[2]
            year = dates[5]
            pos_score = float(line.split('\t')[1].split(' ')[0])
            neg_score = float(line.split('\t')[1].split(' ')[1])
            num_word = float(line.split('\t')[1].split(' ')[2])
            dates_string = days_of_week + ' ' + month + ' ' + str(day) + ' ' + str(year)
            if dates_string in daily_sentiment_dict:
                if (pos_score - neg_score) / num_word >= threshold_pos_neg:
                    daily_sentiment_dict[dates_string][0] += 1
                elif (pos_score - neg_score) / num_word <= -threshold_pos_neg:
                    daily_sentiment_dict[dates_string][1] += 1
                else:
                    daily_sentiment_dict[dates_string][2] += 1
            else:
                pos = 0
                neg = 0 
                neu = 0
                if (pos_score - neg_score) / num_word >= threshold_pos_neg:
                    pos = 1
                elif (pos_score - neg_score) / num_word <= -threshold_pos_neg:
                    neg = 1
                else:
                    neu = 1
                daily_sentiment_dict[dates_string] = [pos, neg, neu]
    output_file_name = file_name.split('_sentiment')[0] + '_daily_pos_neg.txt'
    outfile = open(output_file_name, 'w')
    for key, value in daily_sentiment_dict.items():
        key = key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2] + '\t' + key.split(' ')[3]
        print(key + '\t' + str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]), file = outfile)

#ipad 1 cannot be calculated here, it will be in another file
        
calculate_daily_sentiment_total_tweet('us_tweets_ipad2_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_ipad2_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_ipad2_sentiment.txt')

calculate_daily_sentiment_total_tweet('us_tweets_ipad3_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_ipad3_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_ipad3_sentiment.txt')

calculate_daily_sentiment_total_tweet('us_tweets_iphone4s_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_iphone4s_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_iphone4s_sentiment.txt')

calculate_daily_sentiment_total_tweet('us_tweets_iphone5_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_iphone5_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_iphone5_sentiment.txt')

calculate_daily_sentiment_total_tweet('us_tweets_kindlefire1_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_kindlefire1_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_kindlefire1_sentiment.txt')

calculate_daily_sentiment_total_tweet('us_tweets_kindlefire2_sentiment.txt')           
calculate_daily_sentiment_total_word('us_tweets_kindlefire2_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_kindlefire2_sentiment.txt')

calculate_daily_sentiment_total_tweet('us_tweets_nexus7_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_nexus7_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_nexus7_sentiment.txt')

"""
#Section5: Calculate daily averages and moving averages
"""
dates_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

# this is a method that convert the format of dates form words (like 'Mon Mar 26 00:47:31 CDT 2012') to numbers (2012, 3, 26, Mon)
def convert_date_to_numbers(file_name):
    output_list = []
    with open(file_name) as infile:
        for line in infile:
            line = line.split('\t')
            day_of_week = line[0]
            month = dates_dict[line[1]]
            date = int(line[2])
            year = int(line[3])
            output_list.append([year, month, date, day_of_week, float(line[4]), float(line[5]), float(line[6]), float(line[7])])
    return output_list

# this method does the same thing as the above but it is used for pos_neg files, 
# since the format is slightly different from the total_tweet and total word
def convert_date_to_numbers_pos_neg(file_name):
    output_list = []
    with open(file_name) as infile:
        for line in infile:
            line = line.split('\t')
            day_of_week = line[0]
            month = dates_dict[line[1]]
            date = int(line[2])
            year = int(line[3])
            output_list.append([year, month, date, day_of_week, float(line[4]), float(line[5]), float(line[6])])
    return output_list

# compare to method to compare two list(dates and tweets) by dates, used to sort the dates
def compare_to(list1, list2):
    if list1[0] < list2[0]:
        return -1
    elif list1[0] > list2[0]:
        return 1
    elif list1[1] < list2[1]:
        return -1
    elif list1[1] > list2[1]:
        return 1
    elif list1[2] < list2[2]:
        return -1
    elif list1[2] > list2[2]:
        return 1
    else:
        return 0

# selection sort to sort the list by dates   
def selection_sort(a_list):
    for i in range(len(a_list) - 1):
        min_element = a_list[i]
        min_index = i
        for j in range(i+1, len(a_list)):
            if compare_to(min_element, a_list[j]) > 0:
                min_element = a_list[j]
                min_index = j
        if i != min_index:
            a_list[i], a_list[min_index] = a_list[min_index], a_list[i]

# a method to calculate the average sentiment of all tweets in a day
def calculate_average(a_list):
    for element in a_list:
        element.append(num_format(element[4] / element[7]))
        element.append(num_format(element[5] / element[7]))
        element.append(num_format(element[6] / element[7]))

# used for calculate percentage of the positive tweets in a day for the pos_neg files
def calculate_percentage(a_list):
    for element in a_list:
        element.append(num_format(element[3] / (element[3] + element[4])))

days_each_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
days_each_month_leap_year = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

# a method to add the missing data of a time period, a way to visulize how many missing dates are there
def add_missing_date(a_list):
    start_year = a_list[0][0]
    start_month = a_list[0][1]
    start_date = a_list[0][2]
    end_month = a_list[len(a_list) - 1][1]
    end_date = a_list[len(a_list) - 1][2]
    if start_month == end_month:
        if end_date - start_date + 1 > len(a_list):
            dates_present = [element[2] for element in a_list]
            for i in range(end_date - start_date + 1):
                if i + start_date + 1 not in dates_present:
                    a_list.append([start_year, start_month, i + start_date + 1, ' ', 0, 0, 0, 0, 0, 0, 0])
    else:
        dates_start_month = [element[2] for element in a_list if element[1] == start_month]
        dates_end_month = [element[2] for element in a_list if element[1] == end_month]
        if start_year != 2012:
            for i in range(days_each_month[start_month] - start_date):
                if i + start_date + 1 not in dates_start_month:
                    a_list.append([start_year, start_month, i + start_date + 1, ' ', 0, 0, 0, 0, 0, 0, 0])
        else:
            for i in range(days_each_month_leap_year[start_month] - start_date + 1):
                if i + start_date + 1 not in dates_start_month:
                    a_list.append([start_year, start_month, i + start_date + 1, ' ', 0, 0, 0, 0, 0, 0, 0])
        for i in range(end_date):
            if i + 1 not in dates_end_month:
                a_list.append([start_year, end_month, i + 1, ' ', 0, 0, 0, 0, 0, 0, 0])

# a method that add the missing data of a time period for the pos_neg file
def add_missing_date_pos_neg(a_list):
    start_year = a_list[0][0]
    start_month = a_list[0][1]
    start_date = a_list[0][2]
    end_month = a_list[len(a_list) - 1][1]
    end_date = a_list[len(a_list) - 1][2]
    if start_month == end_month:
        if end_date - start_date + 1 > len(a_list):
            dates_present = [element[2] for element in a_list]
            for i in range(end_date - start_date + 1):
                if i + start_date + 1 not in dates_present:
                    a_list.append([start_year, start_month, i + start_date + 1, ' ', 0, 0, 0, 0])
    else:
        dates_start_month = [element[2] for element in a_list if element[1] == start_month]
        dates_end_month = [element[2] for element in a_list if element[1] == end_month]
        if start_year != 2012:
            for i in range(days_each_month[start_month] - start_date):
                if i + start_date + 1 not in dates_start_month:
                    a_list.append([start_year, start_month, i + start_date + 1, ' ', 0, 0, 0, 0])
        else:
            for i in range(days_each_month_leap_year[start_month] - start_date + 1):
                if i + start_date + 1 not in dates_start_month:
                    a_list.append([start_year, start_month, i + start_date + 1, ' ', 0, 0, 0, 0])
        for i in range(end_date):
            if i + 1 not in dates_end_month:
                a_list.append([start_year, end_month, i + 1, ' ', 0, 0, 0, 0])

# calculate a moving average of 'moving_average_range' days,
# this can be used for different moving average calculation by just change the value of 'moving_average_range'
moving_average_range = 5

def moving_average(a_list):    
    for i in range(len(a_list)):
        average = 0
        if i < moving_average_range:
            for j in range(i + 1):
                average += a_list[j][10]
            average /= i + 1
        else:
            for j in range(i - moving_average_range + 1, i + 1):
                average += a_list[j][10]
            average /= moving_average_range
        a_list[i].append(num_format(average))

# calculate a moving average of 'moving_average_range' days for the pos_neg file 
def moving_average_pos_neg(a_list):
    for i in range(len(a_list)):
        average = 0
        if i < moving_average_range:
            for j in range(i + 1):
                average += a_list[j][7]
            average /= i + 1
        else:
            for j in range(i - moving_average_range + 1, i + 1):
                average += a_list[j][7]
            average /= moving_average_range
        a_list[i].append(num_format(average))

# a method to do all the calculation for total tweet of different products
def all_calculation_total_tweet(product_name):
    file_name = 'us_tweets_' + product_name + '_daily_sentiment_total_tweet.txt'
    the_list = convert_date_to_numbers(file_name)
    selection_sort(the_list)
    calculate_average(the_list)
    add_missing_date(the_list)
    selection_sort(the_list)
    moving_average(the_list)
    print(product_name + ': ')
    for a in the_list:
        print(a)     
    print()
    
    out_file_name = 'us_tweets_' + product_name + '_daily_sentiment_total_tweet_moving_average5.txt'
    outfile = open(out_file_name, 'w')
    for line in the_list:
        try:
            for a in line:
                print(a, end = '\t', file = outfile)
            print(file = outfile)
        except:
            pass
        
# a method to do all the calculation for total word of different products
def all_calculation_total_word(product_name):
    file_name = 'us_tweets_' + product_name + '_daily_sentiment_total_word.txt'
    the_list = convert_date_to_numbers(file_name)
    selection_sort(the_list)
    calculate_average(the_list)
    add_missing_date(the_list)
    selection_sort(the_list)
    moving_average(the_list)
    print(product_name + ': ')
    for a in the_list:
        print(a)     
    print()
    
    out_file_name = 'us_tweets_' + product_name + '_daily_sentiment_total_word_moving_average5.txt'
    outfile = open(out_file_name, 'w')
    for line in the_list:
        try:
            for a in line:
                print(a, end = '\t', file = outfile)
            print(file = outfile)
        except:
            pass

# a method to do all the calculation for positive and negative tweets of different products
def all_calculation_pos_neg(product_name):
    file_name = 'us_tweets_' + product_name + '_daily_pos_neg.txt'
    the_list = convert_date_to_numbers_pos_neg(file_name)
    selection_sort(the_list)
    calculate_percentage(the_list)
    add_missing_date_pos_neg(the_list)
    selection_sort(the_list)
    moving_average_pos_neg(the_list)
    print(product_name + ': ')
    for a in the_list:
        print(a)     
    print()
    
    out_file_name = 'us_tweets_' + product_name + '_daily_sentiment_pos_neg_moving_average5.txt'
    outfile = open(out_file_name, 'w')
    for line in the_list:
        try:
            for a in line:
                print(a, end = '\t', file = outfile)
            print(file = outfile)
        except:
            pass

# the calculation of ipad1 is a little different since the tweet data format is different from these products
all_calculation_total_tweet('ipad2')
all_calculation_total_tweet('ipad3')
all_calculation_total_tweet('iphone4s')
all_calculation_total_tweet('iphone5')
all_calculation_total_tweet('kindlefire1')
all_calculation_total_tweet('kindlefire2')
all_calculation_total_tweet('nexus7')

all_calculation_total_word('ipad2')
all_calculation_total_word('ipad3')
all_calculation_total_word('iphone4s')
all_calculation_total_word('iphone5')
all_calculation_total_word('kindlefire1')
all_calculation_total_word('kindlefire2')
all_calculation_total_word('nexus7')

all_calculation_pos_neg('ipad2')
all_calculation_pos_neg('ipad3')
all_calculation_pos_neg('iphone4s')
all_calculation_pos_neg('iphone5')
all_calculation_pos_neg('kindlefire1')
all_calculation_pos_neg('kindlefire2')
all_calculation_pos_neg('nexus7')

"""
# section 6: Linear regression of the positive score, negative score with the stock daily residual
"""
from sklearn import linear_model
import numpy as np

def linear_regression(product_name, sentiment_type):
    infile_name = 'us_tweets_' + product_name + '_daily_sentiment_' + sentiment_type + '_moving_average5.txt'
    input_list = []
    infile_name_stock = product_name + '_expected_return.txt'
    stock_list = []
    stock_dates = []
    with open(infile_name_stock) as stock:
        for element in stock:
            stock_dates.append(int(element.split('\t')[0]))
            stock_list.append(float(element.split('\t')[1]))

    # open the files and create the X vector
    with open(infile_name) as sentiment:
        for element in sentiment:
            element = element.split('\t')
            input_list.append([int(element[2]), float(element[8]), float(element[9])])
    
    # make sure the tweet data matches the stock price in the same range
    # remove the tweet that are in the weekend
    x_vector = [[element[1], element[2]] for element in input_list if element[0] in stock_dates]
    
    # Create linear regression object
    regr = linear_model.LinearRegression()
    regr.fit(x_vector, stock_list)
    print(product_name + ' ' + sentiment_type + ':')
    print('Coefficients: ', regr.coef_)
    print("Residual sum of squares: %.2f" % np.mean((regr.predict(x_vector) - stock_list) ** 2))
    
    # Variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(x_vector, stock_list))
    print()

linear_regression('ipad1', 'total_tweet')
linear_regression('ipad1', 'total_word')

linear_regression('ipad3', 'total_tweet')
linear_regression('ipad3', 'total_word')
