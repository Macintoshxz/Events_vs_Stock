"""
This part of code does the same thing as stock_vs_twitter, but written specially for ipad1
since the data format is different as the other product
"""

"""Section 1:"""
iphone_ipad_2009_data = []

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

# a number formatting method        
def num_format(num):
    return '%.4f' % num

# read file
with open('iphone2009.tsv', mode='r', encoding='utf8') as tsv:
    for line in tsv:
        try:
            line = line.split('\t')
            iphone_ipad_2009_data.append([line[1].split('T')[0], line[4]])
        except:
            pass

# print number of raw data and filtered data
print('number of data: ', len(iphone_ipad_2009_data))
print_first_few_element(iphone_ipad_2009_data, 10)
print_output_file(iphone_ipad_2009_data, 'tweets_iphone_ipad_2009')

# calculate the number of tweets per day
iphone_ipad_2009_num_tweets_per_day = {}
for line in iphone_ipad_2009_data:
    key = line[0]
    if key in iphone_ipad_2009_num_tweets_per_day:
        iphone_ipad_2009_num_tweets_per_day[key] += 1
    else:
        iphone_ipad_2009_num_tweets_per_day[key] = 1
        
# print the number of tweets per day to a txt file
outfile = open('us_tweets_iphone_ipad_2009_num_per_day.txt', 'w')
for key, value in iphone_ipad_2009_num_tweets_per_day.items():
    print(key + '\t' + str(value), file = outfile)

"""Section 2:"""

def find_product(product, not_product_list):
    results = []
    for element in iphone_ipad_2009_data:
        if product in element[1]:
            is_not_product = False
            for n in not_product_list:
                if n in element[1]:
                    is_not_product = True
            if not is_not_product:
                results.append(element)
    return results

# define a method that find the data for a product between a start date and end date
def find_product_event_tweets(input_data, start_date, end_date):
    results = []
    for element in input_data:
        dates = element[0].split('-')
        month = int(dates[1])
        date = int(dates[2])
        year = int(dates[0])
        
        if start_date[2] == end_date[2]: # if year is the same, it is always the same acutally  
            if start_date[0] == end_date[0]: # if month is the same, looking for tweets in the same month
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
        else:
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
# - _ ' " are not in the punctuation list since they might be in a real word
#
punctuation_list = ('#', '!', '.', ':', ';', ',', '"', '?', '>', '<', '&', '%', '^', '(', ')', '+', '=', '{', '}', '[', ']', '|')

def remove_punctuation(input_list):
    output_list = []
    for line in input_list:
        tweet_no_punctuation = ''.join(c for c in line[1] if c not in punctuation_list)
        output_list.append([line[0], tweet_no_punctuation])
    return output_list

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

not_ipad = [] # not_ipad contains words that should not in tweets talking about ipad, like 'ipada'
for i in range(26):
    not_ipad.append(chr(ord('a')+i) + 'ipad')
    not_ipad.append('ipad' + chr(ord('a')+i))
not_ipad.remove('ipadd') # 'ipadd' and 'ipads' should not be removed because people always talk about ipad like this
not_ipad.remove('ipads')
not_ipad.remove('ipadi')
not_ipad.remove('eipad')

data_ipad_2009 = find_product('ipad', not_ipad)

# print number of ipad tweets and the first ten example                
print('\nnumber of tweets mentioning ipad:',len(data_ipad_2009))
print('\nThe first ten elements are:')
print_first_few_element(data_ipad_2009, 10)

# find out the different tweets about different versions of ipad
data_ipad1 = find_product_event_tweets(data_ipad_2009, [3, 19, 2010], [4, 15, 2010])
data_ipad1 = remove_url(remove_punctuation(data_ipad1))

ipad1_num_tweets_per_day = {}

for line in data_ipad1:
    key = line[0]
    if key in ipad1_num_tweets_per_day:
        ipad1_num_tweets_per_day[key] += 1
    else:
        ipad1_num_tweets_per_day[key] = 1
  
# print the number of tweets per day to a txt file
outfile = open('us_tweets_ipad1_num_tweets_per_day.txt', 'w')
for key, value in ipad1_num_tweets_per_day.items():
    percentage = num_format(value / iphone_ipad_2009_num_tweets_per_day[key])
    print(key + '\t' + str(value) + '\t' + str(iphone_ipad_2009_num_tweets_per_day[key]) + '\t' + str(percentage), file = outfile)

print_output_file(data_ipad1, 'us_tweets_ipad1.txt')
print('\nnumber of tweets mentioning ipad1:',len(data_ipad1))        
print('\nThe first ten elements are:')
print_first_few_element(data_ipad1, 10)

not_iphone = []
data_iphone_2009 = find_product('iphone', not_iphone)

data_iphone3gs = find_product_event_tweets(data_iphone_2009, [6, 9, 2009], [6, 29, 2009])
data_iphone3gs = remove_url(remove_punctuation(data_iphone3gs))

print_output_file(data_iphone3gs, 'us_tweets_iphone3gs.txt')
print('\nnumber of tweets mentioning ipad1:',len(data_iphone3gs))        
print('\nThe first ten elements are:')
print_first_few_element(data_iphone3gs, 10)

"""Section 3 for this part is done in the 'stock_vs_twitter.py' file"""

"""Section 4:"""

def calculate_daily_sentiment_total_tweet(file_name):
    daily_sentiment_dict = {}
    with open(file_name) as infile:
        for line in infile:
            dates = line.split('\t')[0].split('-')
            month = dates[1]
            day = dates[2]
            year = dates[0]
            pos_score = float((line.split('\t')[1]).split(' ')[0])
            neg_score = float((line.split('\t')[1]).split(' ')[1])
            num_word = float((line.split('\t')[1]).split(' ')[2])
            dates_string = year + ' ' + month + ' ' + day 
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
        key = key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2]
        print(key + '\t' + str(num_format(value[0])) + '\t' + str(num_format(value[1])) + '\t' + str(num_format(value[0] - value[1])) + '\t' + str(value[2]), file = outfile)

# this is a method that calculate total score of positive and negative words in each day
def calculate_daily_sentiment_total_word(file_name):
    daily_sentiment_dict = {}
    with open(file_name) as infile:
        for line in infile:
            dates = line.split('\t')[0].split('-')
            month = dates[1]
            day = dates[2]
            year = dates[0]
            pos_score = float(line.split('\t')[1].split(' ')[0])
            neg_score = float(line.split('\t')[1].split(' ')[1])
            num_word = float(line.split('\t')[1].split(' ')[2])
            dates_string = year + ' ' + month + ' ' + day
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
        key = key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2]
        print(key + '\t' + str(num_format(value[0])) + '\t' + str(num_format(value[1])) + '\t' + str(num_format(value[0] - value[1])) + '\t' + str(value[2]), file = outfile)

# this is a method that calculate total score of numbers positive and negative tweets in each day
threshold_pos_neg = 0
def calculate_daily_pos_neg_tweets(file_name):
    daily_sentiment_dict = {}
    with open(file_name) as infile:
        for line in infile:
            dates = line.split('\t')[0].split('-')
            month = dates[1]
            day = dates[2]
            year = dates[0]
            pos_score = float(line.split('\t')[1].split(' ')[0])
            neg_score = float(line.split('\t')[1].split(' ')[1])
            num_word = float(line.split('\t')[1].split(' ')[2])
            dates_string = year + ' ' + month + ' ' + day
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
        key = key.split(' ')[0] + '\t' + key.split(' ')[1] + '\t' + key.split(' ')[2]
        print(key + '\t' + str(num_format(value[0])) + '\t' + str(num_format(value[1])) + '\t' + str(value[2]), file = outfile)

calculate_daily_sentiment_total_tweet('us_tweets_ipad1_sentiment.txt')
calculate_daily_sentiment_total_word('us_tweets_ipad1_sentiment.txt')
calculate_daily_pos_neg_tweets('us_tweets_ipad1_sentiment.txt')

"""Section 5:"""

def remove_hyphen(file_name):
    output_list = []
    with open(file_name) as infile:
        for line in infile:
            line = line.split('\t')
            day_of_week = ' '
            month = int(line[1])
            date = int(line[2])
            year = int(line[0])
            output_list.append([year, month, date, day_of_week, float(line[3]), float(line[4]), float(line[5]), float(line[6])])
    return output_list

def remove_hyphen_pos_neg(file_name):
    output_list = []
    with open(file_name) as infile:
        for line in infile:
            line = line.split('\t')
            day_of_week = ' '
            month = int(line[1])
            date = int(line[2])
            year = int(line[0])
            output_list.append([year, month, date, day_of_week, float(line[3]), float(line[4]), float(line[5])])
    return output_list

# compare to method to compare two list(dates and tweets) by dates
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

def calculate_percentage(a_list):
    for element in a_list:
        element.append(num_format(element[4] / (element[4] + element[5])))

days_each_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
days_each_month_leap_year = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

# a method to add the missing data of time period 
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

moving_average_range = 5
# a method to calculate the moving average of five days

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

# a method to do all the calculation for different product
def all_calculation_total_tweet(product_name):
    file_name = 'us_tweets_' + product_name + '_daily_sentiment_total_tweet.txt'
    the_list = remove_hyphen(file_name)
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
        
def all_calculation_total_word(product_name):
    file_name = 'us_tweets_' + product_name + '_daily_sentiment_total_word.txt'
    the_list = remove_hyphen(file_name)
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
        
def all_calculation_pos_neg(product_name):
    file_name = 'us_tweets_' + product_name + '_daily_pos_neg.txt'
    the_list = remove_hyphen_pos_neg(file_name)
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

all_calculation_total_tweet('ipad1')
all_calculation_total_word('ipad1')
all_calculation_pos_neg('ipad1')

"""Section 6 is done in the 'stock_vs_tweet' file"""
