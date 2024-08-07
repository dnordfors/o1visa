from fastapi import APIRouter
from app.models.resume_model import ResumeModel
from app.services.immigration import ImmigrationOfficer

router = APIRouter()


@router.post("/evaluate_resume")
async def evaluate_resume(resume: ResumeModel):
    officer = ImmigrationOfficer(resume.resume_content)
    officer.evaluate_applicant()

    return {
        'assessment_report': officer.assessment_report,
        'letter_to_candidate': officer.letter_to_candidate,
        'complete_dialogue_thread': officer.messages
    }