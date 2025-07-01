from langchain.tools import tool
from backend.services.calendar_service import CalendarService
from backend.config import settings
from datetime import datetime

calendar_service = CalendarService()

@tool
def get_calendar_availability(date: str, start_time: str = "09:00", end_time: str = "17:00") -> str:
    """Check calendar availability for a specific date and time range in IST timezone."""
    try:
        availability = calendar_service.check_availability(date, start_time, end_time)
        
        if availability['is_free']:
            return f"✅ {date} is completely free from {start_time} to {end_time} IST. Available for booking!"
        
        busy_slots = []
        for event in availability['events']:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            title = event.get('summary', 'Busy')

            if 'T' in start:
                start_utc = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_utc = datetime.fromisoformat(end.replace('Z', '+00:00'))
                start_ist = start_utc.astimezone(settings.IST)
                end_ist = end_utc.astimezone(settings.IST)

                start_time_str = start_ist.strftime('%H:%M')
                end_time_str = end_ist.strftime('%H:%M')
                busy_slots.append(f"{start_time_str}-{end_time_str} ({title})")

        return f"📅 {date} has these busy times (IST): {', '.join(busy_slots)}. I can suggest free slots around these times."

    except Exception as e:
        return f"❌ Error checking calendar: {str(e)}"

@tool
def create_calendar_event(title: str, date: str, start_time: str, end_time: str, description: str = "") -> str:
    """Create a calendar event in IST timezone and return confirmation."""
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        start_datetime = datetime.combine(date_obj.date(), datetime.strptime(start_time, "%H:%M").time())
        end_datetime = datetime.combine(date_obj.date(), datetime.strptime(end_time, "%H:%M").time())

        start_datetime = settings.IST.localize(start_datetime)
        end_datetime = settings.IST.localize(end_datetime)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
        }

        created_event = calendar_service.create_event(event)
        return f"🎉 SUCCESS! Booked '{title}' on {date} from {start_time} to {end_time} IST. Event ID: {created_event.get('id')}"

    except Exception as e:
        return f"❌ Failed to create event: {str(e)}"

@tool
def suggest_time_slots(date: str, duration_minutes: int = 60) -> str:
    """Suggest available time slots for a given date based on calendar availability."""
    try:
        availability_result = get_calendar_availability(date)

        if "completely free" in availability_result:
            suggestions = [
                "09:00-10:00 (Morning slot)",
                "10:00-11:00 (Late morning)",
                "11:00-12:00 (Pre-lunch)",
                "14:00-15:00 (Early afternoon)",
                "15:00-16:00 (Mid afternoon)",
                "16:00-17:00 (Late afternoon)"
            ]
            return f"💡 Here are suggested time slots for {date}:\n• " + "\n• ".join(suggestions)
        else:
            return f"💡 Based on your calendar, here are some free slots for {date}:\n• Before 12:00\n• 13:00 onwards\n\nWould you like me to book a specific time?"

    except Exception as e:
        return f"❌ Error getting suggestions: {str(e)}"
