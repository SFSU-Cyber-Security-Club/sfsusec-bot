import asyncio
import pandas as pd
import pytz

from discord.ext import commands
from discord.utils import get
from datetime import datetime, timedelta

time_zone = 'America/Los_Angeles'
time_format = '%m/%d/%Y - %H:%M:%S'
event_IDs = []

async def event_reminder(event, seconds: int, announcements, role):
    '''
    A timer for an event that will end 5 min before the start time
    '''
    await asyncio.sleep(seconds)
    await announcements.send(f'{role} **{event.name}** is starting in **5 minutes** 👏 As a reminder please go to: **{event.location}** 📍 We will see you there 😃')

async def event_check(bot: commands.Bot, server_ID: int, announcements_ID: int):
    '''
    - Bot will check for any scheduled events every midnight, if there is one or more, run the loop
    - Check if the scheduled event already has a timer
    - If not add the event ID to scheduled list and setup a unique timer 5 min before event
    '''
    guild = bot.get_guild(server_ID)
    role = get(guild.roles, name='SFSU student')
    announcements = bot.get_channel(announcements_ID)
    while True:
        now = datetime.now(pytz.timezone(time_zone))
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await asyncio.sleep((midnight-now).total_seconds)
        if len(guild.scheduled_events) > 0:
            for i in range(len(guild.scheduled_events)):
                if guild.scheduled_events[i].id in event_IDs:
                    continue
                event_IDs.append(guild.scheduled_events[i].id)
                # discord event times are all in iso8601 which is UTC
                iso8601 = str(guild.scheduled_events[i].start_time)
                utc = datetime.fromisoformat(iso8601)
                local = utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(time_zone))
                local_formatted = local.strftime(time_format)
                current = datetime.now()
                current_formatted = current.strftime(time_format)
                time = (pd.to_datetime(local_formatted)-pd.to_datetime(current_formatted))
                print(f'The time now is: {current_formatted} | {guild.scheduled_events[i].name} starts at {local_formatted}\n')
                print(f'The time diff is: {time} setting up a timer for 5min before event: {time.total_seconds-300} seconds\n')
                asyncio.create_task(event_reminder(guild.scheduled_events[i], time.total_seconds-300, announcements, role))
