# class datetime.datetime
# A combination of a date and a time.
# Attributes: year, month, day, hour, minute, second, microsecond, and tzinfo.
from datetime import datetime, timedelta, time


class ical_helpers:
    def __init__(self, principal, calendar):
        self.dt_today = datetime.today()
        self.today = self.get_time(self.dt_today)
        self.principal = principal
        self.calendar = calendar
        self.alarmmode = None
        self.icalstr = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:{publisher}
BEGIN:VEVENT
UID:123456789@example.com
LOCATION:{location}
SUMMARY:{summary}
DESCRIPTION:{description}
CLASS:{cls}
DTSTART:{start}
DTEND:{end}
DTSTAMP:{stamp}{ALARM}
END:VEVENT
END:VCALENDAR"""

        self.alarmstr = """
BEGIN:VALARM
{trigger}{repeat}
DURATION:PT15M
ACTION:DISPLAY{alarm_description}
END:VALARM"""
        self.info = None
        self.alarm = None

    def create_new_calendar(self, cal_name):
        """Creates new calendar with given name.
        @param principal
        @param cal_name: name of calendar"""
        self.calendar = self.principal.make_calendar(name=cal_name)
        return self.calendar

    def get_time(self, dt):
        """
        Returns iCal time formatted string. "YYYYMMDDTHHMMSSZ"
        @param dt: daytime object
        """
        icaldtstr = "{year:04d}{month:02d}{day:02d}T{hour:02d}{minute:02d}{second:02d}Z".format(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second
        )
        return icaldtstr

    def get_trigger_time(self, mode, value):
        """Returns iCal-formatted string for reminder trigger.
        @param mode: before/after/time
        @param value: <amount>H/M/S if mode is "before" or "after";
         datetime object if mode == "time"
         """
        if mode == "time":
            trigstr = "TRIGGER;VALUE=DATE-TIME:"
            trigstr += get_time(value)
        elif mode == "before":
            trigstr = "TRIGGER:-P" + value
        elif mode == "after":
            trigstr = "TRIGGER;RELATED=END:P" + value
        else:
            trigstr = ""
            print("mode has to be 'before', 'after' or 'time'.")
        return trigstr

    def set_infos(self, info):
        self.info = info
        self.fill_alarmstr(self.info.trigger, self.info.repeat, self.info.alarm_desc)

    def insert_event(self):
        # fill_icalstr(dtstart, dtend, dtstamp, summary, publisher, method="PUBLISH", location=None, description=None, cls="PUBLIC", rule=None)
        insert = self.fill_icalstr()
        print(insert)
# fill_icalstr(self, start, end, stamp, summary, publisher="none", method="PUBLISH", location="", description="", cls="PUBLIC", rule=None):
        self.calendar.save_event(insert)
        print("saved event.")

    def fill_alarmstr(self, trigger, repeat="", alarm_description=""):
        """
        Fills alarmstr with alarm information.
        @param isalarm: bool if there should be a alarm.
        @param trigger: Time of trigger
        @param repeat: repitition of alarm
        @param alarm_description: description of alarm
        """

        if repeat:
            repeat = "\nREPEAT:" + repeat
        else:
            repeat = ""
        if alarm_description:
            alarm_description = "\nDESCRIPTION:" + alarm_description
        if self.info.trigger != "":
            alertstr = self.alarmstr.format(trigger=trigger,
                                            repeat=repeat,
                                            alarm_description=alarm_description
                                            )
        else:
            self.alarm = ""
            return
        self.alarm = alertstr
        return

    def fill_icalstr(self):
        """
        Fills icalstr with event information.
        """
        # if rule is not None:
        #     rrule = "FREQ={}\n".format(self.info.rule)
        # else:
        #     rrule = ""
        # if not description:
        #     description = ""
        # if not location:
        #     location = ""
        finalstr = self.icalstr.format(
            publisher=self.info.publisher,
            location=self.info.location,
            summary=self.info.summary,
            description=self.info.description,
            cls=self.info.cls,
            start=self.get_time(self.info.begin),
            end=self.get_time(self.info.end),
            stamp=self.today,
            ALARM=self.alarm,
            rrule=self.info.rrule)
        return finalstr


# print(today)
#print(datetime(2022, 5, 17, 18, 27).hour)


# eg_publisher = "me"
# eg_method = "PUBLISH"
# eg_location = "Nowhere"
# eg_summary = "Testitest"
# eg_description = "Describe"
# eg_cls = "PRIVATE"
# eg_uid = "20220516T060000Z-123401@example.com"
# eg_dtimestamp = "20220516T060000Z"
# eg_dtstart = "20220517T060000Z"
# eg_dtend = "20220517T230000Z"
# eg_rrule = "FREQ=YEARLY"
