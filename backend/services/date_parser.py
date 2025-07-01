import re
from datetime import datetime
from typing import Dict

class DateParser:
    @staticmethod
    def parse_natural_date(text: str, current_date: str) -> str:
        # Existing implementation remains unchanged
        ...

    @staticmethod
    def extract_time_from_text(text: str) -> Dict[str, str]:
        """
        Extracts start_time and end_time from natural language text using regex patterns.
        Handles various formats:
        - 2 PM, 2:30 PM, 14:00
        - 2-3 PM, 2 to 3:30 PM
        - morning (9-11), afternoon (1-4), evening (5-7)
        - defaults to 09:00-10:00 if no time found
        """
        text_lower = text.lower()
        
        # Regex patterns for time extraction
        time_patterns = [
            # 2 PM to 3:30 PM
            r'(\d{1,2}(?::\d{2})?\s*[ap]m?)\s*(?:to|-|until)\s*(\d{1,2}(?::\d{2})?\s*[ap]m?)',
            # 2-3:30 PM
            r'(\d{1,2}(?::\d{2})?)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m?)',
            # Single time (2 PM) - assume 1 hour duration
            r'(\d{1,2}(?::\d{2})?\s*[ap]m?)\b',
            # 24-hour format (14:00-15:30)
            r'(\d{2}:\d{2})\s*(?:to|-)\s*(\d{2}:\d{2})',
            # Time ranges without meridiem (2-3)
            r'\b(\d{1,2})\s*(?:to|-)\s*(\d{1,2})\b'
        ]

        # Time period mappings
        period_mappings = {
            'morning': ('09:00', '11:00'),
            'afternoon': ('13:00', '16:00'),
            'evening': ('17:00', '19:00'),
            'night': ('20:00', '22:00'),
            'lunch': ('12:00', '13:00')
        }

        # Try to match time patterns
        for pattern in time_patterns:
            match = re.search(pattern, text_lower)
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    start, end = groups
                    return {
                        'start_time': DateParser._normalize_time(start.strip()),
                        'end_time': DateParser._normalize_time(end.strip())
                    }
                elif len(groups) == 1:
                    start = groups[0]
                    return {
                        'start_time': DateParser._normalize_time(start.strip()),
                        'end_time': DateParser._add_hours(start.strip())
                    }

        # Check for time periods (morning/afternoon/evening)
        for period, times in period_mappings.items():
            if period in text_lower:
                return {
                    'start_time': times[0],
                    'end_time': times[1]
                }

        # Default values if no time found
        return {
            'start_time': '09:00',
            'end_time': '10:00'
        }

    @staticmethod
    def _normalize_time(time_str: str) -> str:
        """Convert various time formats to HH:MM format"""
        # Handle 24-hour format
        if re.match(r'\d{2}:\d{2}', time_str):
            return time_str
        
        # Handle 12-hour format
        time_match = re.match(r'(\d{1,2})(?::(\d{2}))?\s*([ap]m?)?', time_str, re.IGNORECASE)
        if not time_match:
            return '09:00'
        
        hour = int(time_match.group(1))
        minute = time_match.group(2) or '00'
        meridiem = time_match.group(3) or ''
        
        # Convert to 24-hour format
        if meridiem.lower().startswith('p') and hour < 12:
            hour += 12
        elif meridiem.lower().startswith('a') and hour == 12:
            hour = 0
        
        return f"{hour:02d}:{minute}"

    @staticmethod
    def _add_hours(time_str: str, hours: int = 1) -> str:
        """Add hours to a time string"""
        normalized = DateParser._normalize_time(time_str)
        time_obj = datetime.strptime(normalized, "%H:%M")
        new_time = time_obj + timedelta(hours=hours)
        return new_time.strftime("%H:%M")
