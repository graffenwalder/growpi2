import time


class SleepTo():

    def secondOfMinute(second):
        """ Sleep to the next time a second occurs (0 - 59)

        SleepTo.secondOfMinute(5)
        Current time: 00:00:10
        Sleeps until: 00:01:05
        """
        if 0 <= second <= 59:
            currentSecond = int(time.strftime("%S"))
            if second > currentSecond:
                sleeptime = second - currentSecond
            else:
                sleeptime = second - currentSecond + 60
            time.sleep(sleeptime)
        else:
            raise ValueError("Please select a value from 0 to 59")

    def minuteOfHour(minute):
        """ Sleep to the next time a minute occurs (0 - 59)

        SleepTo.minuteOfHour(5)
        Current time: 00:10:00
        Sleeps until: 01:05:00
        """
        if 0 <= minute <= 59:
            currentMinute = int(time.strftime("%M"))
            currentSecond = int(time.strftime("%S"))
            if minute > currentMinute:
                sleeptime = (minute - currentMinute) * 60 - currentSecond
            else:
                sleeptime = (minute - currentMinute + 60) * 60 - currentSecond
            time.sleep(sleeptime)
        else:
            raise ValueError("Please select a value from 0 to 59")

    def hourOfDay(hour):
        """ Sleep to the next time a hour occurs (0 - 23)

        SleepTo.hourOfDay(5)
        Current time: jan 1 10:00:00
        Sleeps until: jan 2 05:00:00
        """
        if 0 <= hour <= 23:
            currentHour = int(time.strftime("%H"))
            currentMinute = int(time.strftime("%M"))
            currentSecond = int(time.strftime("%S"))
            if hour > currentHour:
                sleeptime = (hour - currentHour) * 3600 - \
                    (currentMinute * 60) - currentSecond
            else:
                sleeptime = ((hour - currentHour + 24) * 3600) - \
                    (currentMinute * 60) - currentSecond
            time.sleep(sleeptime)
        else:
            raise ValueError("Please select a value from 0 to 23")

    def nextSecondInterval(second):
        """ Sleep to the next time a second interval occurs(0 - 59)

        SleepTo.nextSecondInterval(13)
        Current time: 00:00:16
        Sleeps until: 00:00:26

        Starts from zero if it goes over the minute

        SleepTo.nextSecondInterval(13)
        Current time: 00:00:54
        Sleeps until: 00:01:13
        """

        if 0 <= second <= 59:
            currentSecond = int(time.strftime("%S"))
            if currentSecond > second:
                nextInterval = second - (currentSecond % second)
                if nextInterval + currentSecond > 60:
                    sleeptime = 60 - currentSecond + second
                else:
                    sleeptime = nextInterval
            else:
                sleeptime = second - currentSecond
            time.sleep(sleeptime)

        else:
            raise ValueError("Please select a value from 0 to 59")

    def nextMinuteInterval(minute):
        """ Sleep to the next time a minute interval occurs(0 - 59)

        SleepTo.nextMinuteInterval(13)
        Current time: 00:16:00
        Sleeps until: 00:26:00

        Starts from zero if it goes over the hour

        SleepTo.nextMinuteInterval(13)
        Current time: 00:54:00
        Sleeps until: 01:13:00
        """
        if 0 <= minute <= 59:
            currentSecond = int(time.strftime("%S"))
            currentMinute = int(time.strftime("%M"))
            if currentMinute > minute:
                nextInterval = minute - (currentMinute % minute)
                if nextInterval + currentMinute > 60:
                    sleeptime = (60 - currentMinute + minute) * \
                        60 - currentSecond
                else:
                    sleeptime = nextInterval * 60 - currentSecond
            else:
                sleeptime = (minute - currentMinute) * 60 - currentSecond
            time.sleep(sleeptime)

        else:
            raise ValueError("Please select a value from 0 to 59")

    def nextHourInterval(hour):
        """ Sleep to the next time a hour interval occurs(0 - 23)

        SleepTo.nextHourInterval(7)
        Current time: 16:00:00
        Sleeps until: 21:00:00

        Starts from zero if it goes over the day

        SleepTo.nextHourInterval(7)
        Current time: jan 1 22:00:00
        Sleeps until: jan 2 07:00:00
        """
        if 0 <= hour <= 23:
            currentHour = int(time.strftime("%H"))
            currentMinute = int(time.strftime("%M"))
            currentSecond = int(time.strftime("%S"))
            if currentHour > hour:
                nextInterval = hour - (currentHour % hour)
                if nextInterval + currentHour > 24:
                    sleeptime = (24 - currentHour + hour) * 3600 - \
                        (currentMinute * 60) - currentSecond
                else:
                    sleeptime = nextInterval * 3600 - \
                        (currentMinute * 60) - currentSecond
            else:
                sleeptime = (hour - currentHour) * 3600 - \
                    (currentMinute * 60) - currentSecond
            time.sleep(sleeptime)

        else:
            raise ValueError("Please select a value from 0 to 23")
