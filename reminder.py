from datetime import datetime
import pytz
import pandas as pd
import asyncio

time_zone = "America/Los_Angeles"
time_format = "%m/%d/%Y - %H:%M:%S"
event_check_time = 1800 # 30 minutes
event_IDs = []

# a timer for a scheduled event
async def event_reminder(bot, event, seconds, announcements):
    await asyncio.sleep(seconds)
    await announcements.send(f"@everyone {event.name} has started 👏 Please go to {event.location} 👏 We'll see you there 👏")

# checks every 30 minutes for events and creates timers for them
async def event_check(bot, guild, announcements):
    while 1:
        if len(guild.scheduled_events) > 0:
            for i in range(len(guild.scheduled_events)):
                if (guild.scheduled_events[i].id in event_IDs): continue
                event_IDs.append(guild.scheduled_events[i].id)
                # Discord event times are all in iso8601 which is UTC
                iso8601 = str(guild.scheduled_events[i].start_time)
                utc = datetime.fromisoformat(iso8601)
                local = utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(time_zone))
                local_formatted = local.strftime(time_format)
                current = datetime.now()
                current_formatted = current.strftime(time_format)
                print(f"The time now is: {current_formatted} | {guild.scheduled_events[i].name} starts at {local_formatted}")
                time = pd.to_datetime(local_formatted) - pd.to_datetime(current_formatted)
                print(f"The time diff is: {time} setting up a timer for {time.seconds} seconds")
                asyncio.create_task(event_reminder(bot, guild.scheduled_events[i], time.seconds, announcements))
                print("------------------------------------------------------------------------------")
        await asyncio.sleep(event_check_time)