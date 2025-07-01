from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from typing import Optional, List, Dict
from backend.config import settings


class CalendarService:
    def __init__(self):
        self.service = self._get_calendar_service()

    def _get_calendar_service(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            return build("calendar", "v3", credentials=credentials)
        except Exception as e:
            print(f"Error initializing calendar service: {e}")
            return None

    def get_events(
        self, start_datetime: datetime, end_datetime: datetime
    ) -> List[Dict]:
        if not self.service:
            raise Exception("Calendar service not available")

        events_result = (
            self.service.events()
            .list(
                calendarId=settings.CALENDAR_ID,
                timeMin=start_datetime.isoformat(),
                timeMax=end_datetime.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events_result.get("items", [])

    def create_event(self, event_data: Dict) -> Dict:
        if not self.service:
            raise Exception("Calendar service not available")

        return (
            self.service.events()
            .insert(calendarId=settings.CALENDAR_ID, body=event_data)
            .execute()
        )

    def check_availability(
        self, date: str, start_time: str = "09:00", end_time: str = "17:00"
    ) -> Dict:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            start_datetime = datetime.combine(
                date_obj.date(), datetime.strptime(start_time, "%H:%M").time()
            )
            end_datetime = datetime.combine(
                date_obj.date(), datetime.strptime(end_time, "%H:%M").time()
            )

            start_datetime = settings.IST.localize(start_datetime)
            end_datetime = settings.IST.localize(end_datetime)

            events = self.get_events(start_datetime, end_datetime)

            return {
                "is_free": len(events) == 0,
                "events": events,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
            }
        except Exception as e:
            raise Exception(f"Error checking availability: {str(e)}")
