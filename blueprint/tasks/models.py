from ..models import BaseModel


class Task(BaseModel):
    __tablename__ = 'tasks'




class Suggestion(BaseModel):
    __tablename__ = 'suggestions'
