from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from backend.tools.calendar_tools import get_calendar_availability, create_calendar_event, suggest_time_slots
from backend.config import settings

class ChatAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.1
        )
        
        self.tools = [get_calendar_availability, create_calendar_event, suggest_time_slots]
        self.prompt = self._create_prompt()
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=4
        )
    
    def _create_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", """You are Calendent, an intelligent AI calendar assistant working in IST timezone.

PERSONALITY: Helpful, proactive, and smart about understanding user requests.

CORE ABILITIES:
1. Check calendar availability for any date
2. Book appointments with complete details
3. Suggest optimal time slots when asked
4. Handle natural language date/time requests

SMART BEHAVIOR:
- When user asks "what are free slots" or "suggest times", use suggest_time_slots tool
- When user says "tomorrow", convert to actual date (current_date + 1 day)
- When user asks about "this week" or "Friday", be smart about dates
- Always provide specific, actionable suggestions

BOOKING WORKFLOW:
1. Extract: title, date, start_time, end_time from user request
2. Check availability first
3. If available, book immediately
4. Confirm with success message

CONVERSATION CONTEXT:
{conversation_context}

CURRENT DATE: {current_date} (IST)

IMPORTANT: Be proactive and helpful. If user asks for suggestions, actually suggest specific times."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
    
    def process_message(self, message: str, current_date: str, conversation_context: str) -> str:
        response = self.agent_executor.invoke({
            "input": message,
            "current_date": current_date,
            "conversation_context": conversation_context
        })
        return response["output"]
