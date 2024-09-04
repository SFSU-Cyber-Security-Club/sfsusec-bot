from datetime import datetime
from discord.ext import commands
import pytz
import pandas as pd
import asyncio

time_zone = "America/Los_Angeles"
time_format = "%m/%d/%Y - %H:%M:%S"
event_check_time = 86400 # 1 day
event_IDs = []

# a timer for a scheduled event
async def event_reminder(event, seconds: int, announcements):
    await asyncio.sleep(seconds)
    await announcements.send(f"@everyone {event.name} is starting in 5 minutes 👏 As a reminder please go to {event.location} 👏 We'll see you there 👏")

# checks every 30 minutes for events and creates timers for them
async def event_check(bot: commands.Bot, server_ID: int, announcements_ID: int):
    '''
    everyday, check for any scheduled events, if there is one or more, run the loop
    first check if the scheduled event already has a timer
    if not add the event ID to scheduled list and setup a unique timer 5 min before event
    '''
    guild = bot.get_guild(server_ID)
    announcements = bot.get_channel(announcements_ID)
    while 1:
        if len(guild.scheduled_events) > 0:
            for i in range(len(guild.scheduled_events)):
                if (guild.scheduled_events[i].id in event_IDs): continue
                event_IDs.append(guild.scheduled_events[i].id)
                # discord event times are all in iso8601 which is UTC
                iso8601 = str(guild.scheduled_events[i].start_time)
                utc = datetime.fromisoformat(iso8601)
                local = utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(time_zone))
                local_formatted = local.strftime(time_format)
                current = datetime.now()
                current_formatted = current.strftime(time_format)
                print(f"The time now is: {current_formatted} | {guild.scheduled_events[i].name} starts at {local_formatted}")
                time = pd.to_datetime(local_formatted) - pd.to_datetime(current_formatted) - 300 # 5 min
                print(f"The time diff is: {time} setting up a timer for {time.seconds} seconds")
                asyncio.create_task(event_reminder(guild.scheduled_events[i], time.seconds, announcements))
                print("------------------------------------------------------------------------------")
        await asyncio.sleep(event_check_time)