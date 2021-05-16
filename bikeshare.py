import time
import pandas as pnds
import numpy as np
import datetime as dt
import click



CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun')
"""months changed to improve efficiency"""

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')



def choice(prompt, choices=('y', 'n')):
    """Return a valid Yes or No input from the user.
    """
    while True:
        choice = input(prompt).lower().strip()
        if choice == 'end':
            raise SystemExit
        elif ',' not in choice:
            if choice in choices:
                break
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break
        prompt = ("\nOops, something has gone horribly wrong! Please check your"
                  "formatting and enter a valid option:\n>")
    return choice



def get_filters():
    """Input city and filters.
    Returns:
        (str) city -name of the city to analyse
        (str) month -name of the month to filter
        (str) day -name of the day of week to filter
    """
    print("Type end at any time if you would like to exit me.\n")
    while True:
        city = choice("Which city / cities data would you like to analayse? "
                      "New York City, Chicago or Washington? Please use commas "
                      "to list multiple.\n>", CITY_DATA.keys())
        month = choice("\nWhich months would you like to filter data from? "
                       "Once again, please use commas to list multiple.\n>",
                       months)
        day = choice("\nWhich day would you like to filter data from? "
                     "You know the drill by now, please use commas to list "
                     "multiple days.\n>", weekdays)
        confirmation = choice("\nPlease confirm the filters you have chosen. "
                              "\n\n City/Cities: {}\n Month/Months: "
                              "{}\n Day/Days"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nTry again pls!")
    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """Load data
        (str) city - name of the cities
        (str) month - name of the months
        (str) day - name of the days of week
    Returns:
        df - Pandas DataFrame with data
    """
    print("\nLoading Data... Won't be too long!!")
    start_time = time.time()
    if isinstance(city, list):
        df = pnds.concat(map(lambda city: pnds.read_csv(CITY_DATA[city]), city),
                       sort=True)
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pnds.read_csv(CITY_DATA[city])
    df['Start Time'] = pnds.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    if isinstance(month, list):
        df = pnds.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pnds.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]
    print("\nAction has taken {} seconds.".format((time.time() - start_time)))
    print('-'*40)
    return df



def time_stats(df):
    """Display stats on the most frequent travel times."""
    print('\nDisplaying the stats on the most frequent travel times.\n')
    start_time = time.time()
    most_common_month = df['Month'].mode()[0]
    print('The month with the most trips is: ' +
          str(months[most_common_month-1]).title() + '.')
    most_common_day = df['Weekday'].mode()[0]
    print('The most common day of the week is: ' +
          str(most_common_day) + '.')
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' +
          str(most_common_hour) + '.')
    print("\nAction has taken {} seconds.".format((time.time() - start_time)))
    print('-'*40)



def station_stats(df):
    """Display stats on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " +
          most_common_start_station)
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common start end is: " +
          most_common_end_station)
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("The most common start-end combination is: " +
          most_common_start_end_combination)
    print("\nAction has taken {} seconds.".format((time.time() - start_time)))
    print('-'*40)



def trip_duration_stats(df):
    """Display stats on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('The total travel time is : ' +
          total_travel_time + '.')
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("The mean travel time is : " +
          mean_travel_time + ".")
    print("\nAction has taken {} seconds.".format((time.time() - start_time)))
    print('-'*40)



def user_stats(df, city):
    """Display stats on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts().to_string()
    print("User types:")
    print(user_types)
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nGender Distribution:")
        print(gender_distribution)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nThe oldest person to ride a "
              "bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("The youngest person to ride a "
              "bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("The most common birth year amongst "
              "riders is: " + most_common_birth_year)
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))
    print("\nAction has taken {} seconds.".format((time.time() - start_time)))
    print('-'*40)



def raw_data(df, mark_place):
    """Display 5 lines of sorted raw data."""
    print("\nTime to view some raw data!")
    if mark_place > 0:
        last_place = choice("\nWould you like to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0
    if mark_place == 0:
        sort_df = choice("\nHow would you like to sort the way the data is "
                         "displayed in the dataframe? Hit Enter to view "
                         "unsorted.\n \n [st] Start Time\n [et] End Time\n "
                         "[td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>",
                         ('st', 'et', 'td', 'ss', 'es', ''))
        asc_or_desc = choice("\nWould you like it to be sorted ascending or "
                             "descending? \n [a] Ascending\n [d] Descending"
                             "\n\n>",
                             ('a', 'd'))
        if asc_or_desc == 'a':
            asc_or_desc = True
        elif asc_or_desc == 'd':
            asc_or_desc = False
        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_or_desc)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_or_desc)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_or_desc)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_or_desc)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_or_desc)
        elif sort_df == '':
            pass
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5
            if choice("Do you want to keep printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break
    return mark_place



def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        mark_place = 0
        while True:
            select_data = choice("\nPlease select the information you would "
                                 "like.\n\n [ts] Time Stats\n [ss] "
                                 "Station Stats\n [tds] Trip Duration Stats\n "
                                 "[us] User Stats\n [rd] Display Raw Data\n "
                                 "[r] Restart\n\n>",
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                mark_place = raw_data(df, mark_place)
            elif select_data == 'r':
                break
        restart = choice("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break



if __name__ == "__main__":
    main()
