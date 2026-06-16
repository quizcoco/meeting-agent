from pydantic import BaseModel


class AskRequest(BaseModel):
    query: str

class MeetingRequest(BaseModel):
    text: str