from pydantic import BaseModel


class ResumeModel(BaseModel):
    resume_content: str