"""
Course:     Programming for Data Science with Python - Intro to Version Control
Date:       2020-09-01
Author:     D.A. Plager
Filename:   bikeshare_2.py
Description:    This script uses specifically formatted comma-separated value
                (.csv) data from bikeshare programs in various cities and outputs
                the user-defined city's unfiltered or filtered (by month and/or day)
                bikeshare data summary statistics.
"""
import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington).
    city_tuple = ('chicago', 'new york city', 'washington')
    flag1 = True

    while flag1:
        city = input("Please enter the name of the CITY whose data you want" +
                     "\nto analyze (chicago, new york city, or washington): ")
        city = city.lower()

        if city == 'exit':
            sys.exit()

        if city not in city_tuple:
            print("\nPlease try again or enter 'exit'.")
        else:
            flag1 = False

    # Get user input for month (all, january, february, ... , june).
    month_tuple = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    flag2 = True

    while flag2:
        month = input("If desired, enter the name of one specific MONTH (january to june only)" +
                     "\nwhose data you want to limit your analysis to; otherwise, enter 'all': ")
        month = month.lower()

        if month == 'exit':
            sys.exit()

        if month not in month_tuple:
            print("\nPlease try again or enter 'exit'.")
        else:
            flag2 = False

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    weekday_tuple = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    flag3 = True

    while flag3:
        day = input("If desired, enter the name of one specific DAY of the week (monday to sunday)" +
                     "\nwhose data you want to limit your analysis to; otherwise, enter 'all': ")
        day = day.lower()

        if day == 'exit':
            sys.exit()

        if day not in weekday_tuple:
            print("\nPlease try again or enter 'exit'.")
        else:
            flag3 = False

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe.
    # NOTE: Could use 'try'-'except' in a 'while' Loop to handle missing .csv file.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month   # 1 to 12 for Jan. to Dec.
    df['day_of_week'] = df['Start Time'].dt.dayofweek   # 0 = Monday, 6 = Sunday
# NOTE: .dt.weekday_name caused an Error in my Spyder work environment.


# QUESTION: Is there a concise Pandas function/method for converting a Pandas
# Dataframe column of numeric day values (i.e., 'day_of_week'; 0 = Monday,
# 6 = Sunday) to their corresponding string day names?  Presumably, I could use
# a 'for' Loop to accomplish this numeric to string day name conversion, but is
# there any Pandas function that is more direct?


    # Filter by month if applicable.
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        months = ('january', 'february', 'march', 'april', 'may', 'june')
        month_num = months.index(month) + 1

        # Boolean indexing to filter by month to create the new dataframe.
        df = df[df['month'] == month_num]

    # Filter by day of week if applicable.
    if day != 'all':
        # Use the index of the weekdays tuple to get the corresponding int.
        weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        weekday_num = weekdays.index(day)

        # Boolean indexing to filter by day of week to create the new dataframe.
        df = df[df['day_of_week'] == weekday_num]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # For converting month_mode number and day_mode number to corresponding string name.
    months = ('january', 'february', 'march', 'april', 'may', 'june')
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    # Display the most common month.
    month_mode = df['month'].mode()[0]
    month_name = months[month_mode - 1]
    most_freq_month_ct = df['month'].value_counts().max()
    print("Month of most frequent usage: {}".format(month_name.title()))
    print("Month usage count: {}".format(most_freq_month_ct))


    # Display the most common day of week.
    day_mode = df['day_of_week'].mode()[0]
    day_name = weekdays[day_mode]
    most_freq_day_ct = df['day_of_week'].value_counts().max()
    print("Day of most frequent usage: {}".format(day_name.title()))
    print("Day usage count: {}".format(most_freq_day_ct))


    # Display the most common start hour.
    start_hr_mode = df['Start Time'].dt.hour.mode()[0]
    most_freq_start_hr = df['Start Time'].dt.hour.value_counts().max()
    print("Most frequent start hour: {}".format(start_hr_mode))
    print("Start hour count: {}".format(most_freq_start_hr))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    most_popular_start = df['Start Station'].mode()[0]
    most_popular_start_ct = df['Start Station'].value_counts().max()
    print("Most popular start station: {}".format(most_popular_start))
    print("Start station count: {}".format(most_popular_start_ct))


    # Display most commonly used end station.
    most_popular_end = df['End Station'].mode()[0]
    most_popular_end_ct = df['End Station'].value_counts().max()
    print("Most popular end station: {}".format(most_popular_end))
    print("End station count: {}".format(most_popular_end_ct))


    # Display most frequent combination of start station and end station trip.

    '''
    # Obtain counts of each Start-End Station combination (1st attempt).
    most_pop_trip_ct_df = df.groupby(['Start Station', 'End Station']).count()
    print(type(most_pop_trip_ct_df))
        # NOTE: Pandas 'DataFrame' returned w/ redundant counts of each Start-End
        # Station combination in all 11 columns.
    print("\nDataFrame form of .count():\n{}".format(most_pop_trip_ct_df))

    # Obtain a Pandas Series of counts of each Start-End Station combination.
    most_pop_trip_ct_series = most_pop_trip_ct_df[0]   # KeyError: 0
    most_pop_trip_ct_series = most_pop_trip_ct_df[[0]]   # KeyError: "None of [Int64Index([0], dtype='int64')] are in the [columns]"
    most_pop_trip_ct_series = most_pop_trip_ct_df['Unnamed']   # KeyError: 'Unnamed'
    most_pop_trip_ct_df = df.groupby(['Start Station', 'End Station'])[0].count()  # KeyError: 'Column not found: 0'
    print("\nUnnamed column 0:\n{}".format(most_pop_trip_ct_series))

# QUESTION: Why am I unable to access the first 'Unnamed' (index 0) column via
# the above attempts??  If possible, please provide code that would return a
# Pandas Series of the first 'Unnamed: 0' column of most_pop_trip_ct_df.

    '''

    # Obtain a Pandas Series of counts of each Start-End Station combination,
    # and identify the combination(s) with the maximum count value.

    # NOTE: I chose 'Trip Duration' (no NaNs) in place of 'Unnamed: 0" column (see just above).
    # Pandas 'Series' of trip counts.
    trip_cts = df.groupby(['Start Station', 'End Station'])['Trip Duration'].count()

    # Maximum trip count int.
    most_pop_trip_max = trip_cts.max()

    # Boolean indexing for trip(s) having the maximum trip count.
    most_pop_trip = trip_cts[trip_cts == most_pop_trip_max]


# QUESTION: Will I run into trouble if more than one Start-End Station trip
# tied with the maximum trip count??
# Perhaps something comparable to the
# best_rated = book_ratings[(book_ratings == 5).any(axis = 1)]['Book Title'].values
# example that returns a NumPy ndarray is more appropriate here??


    '''
    # Checking the data types and values of various objects.
    print(type(trip_cts))   # Pandas 'Series' of counts returned.
    print("'Trip Duration' column of .groupby() counts:\n{}".format(trip_cts))
    print(type(most_pop_trip_max))   # 'int' class
    print("'Trip Duration' column of .groupby() counts max:\n{}".format(most_pop_trip_max))
    print()
    print("Most popular trip:\n{}".format(most_pop_trip.index))
    print("Most popular trip:\n{}".format(most_pop_trip.index[0]))

    '''

    # Tuple Unpacking of the 1st element (index 0) of the "MultiIndex"-type
    # object returned from 'most_pop_trip.index[0]'.
# QUESTION: Again, might the following only output one Start-End trip even if
# there were more than one trip having the maximum trip count?!
    start_station, end_station = most_pop_trip.index[0]
    print("\nMost popular trip:")
    print("    Start station - {}".format(start_station))
    print("      End station - {}".format(end_station))
    print("Most popular trip count:\n{}".format(most_pop_trip_max))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_time = df['Trip Duration'].sum()
    print('Sum of all trip durations: {0:.2f} hours'.format(total_trip_time / 3600))


    # display mean travel time
    mean_trip_time = df['Trip Duration'].mean()
    print('\nAverage trip duration: {0:.2f} minutes'.format(mean_trip_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_type_cts = df['User Type'].value_counts()
    print("User Type counts: \n{}".format(user_type_cts))

    try:
        # Display counts of gender.
        gender_cts = df['Gender'].value_counts()
        print("\nCounts based on User Gender: \n{}".format(gender_cts))


        # Display earliest, most recent, and most common year of birth.
        earliest_yr = df['Birth Year'].min()
        latest_yr = df['Birth Year'].max()
        most_freq_yr = df['Birth Year'].mode()[0]

        print("\nEarliest birth year: {}".format(int(earliest_yr)))
        print("\nLatest birth year: {}".format(int(latest_yr)))
        print("\nMost frequent birth year: {}".format(int(most_freq_yr)))

    except KeyError:
        print("\nNo gender and/or birth year data available.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print("\nThe following data is for:")
        print("\n   {}".format(city.title()))
        print("\n   Month(s) - {}".format(month.title()))
        print("\n   Day(s) of the Week - {}".format(day.title()))

        df = load_data(city, month, day)
        flag4 = True
        while flag4:
            answer = input("Would you like to see several rows and the" +
                       " dimensions of this data ('yes' or 'no')? ")
            if answer == 'yes':
                print("\nUser-defined DataFrame data (first five rows):\n{}".format(df.head()))
                print("\nUser-defined DataFrame full dimensions (rows, columns): {}".format(df.shape))
                input("\nPress <Enter> key to continue.")
                flag4 = False
            else:
                flag4 = False

        time_stats(df)

        station_stats(df)

        trip_duration_stats(df)

        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
