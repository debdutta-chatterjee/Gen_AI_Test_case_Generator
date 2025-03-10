from typing_extensions import TypedDict,Literal
from pydantic import BaseModel, Field
from typing import List
from pandas import DataFrame

class UserStory(BaseModel):
    title: str  = Field(
        description="user story title",
    )
    business_context:str  = Field(
        description="business context",
    )
    acceptance_critera : str = Field(
        description="acceptance criteria",
    )

class Feedback(BaseModel):
    feedback_text: str  = Field(
        default='',
        description="feedback in written words",
    )
    feedback_decision:  Literal["Accepted", "Rejected"]  = Field(
        default='Accepted',
        description="feedback in boolean accpeted or rejected",
    )

class TestStep(BaseModel):
    step_number: int  = Field(
        description="step number",
    )
    step_action: str  = Field(
        description="action",
    )
    step_expected: str  = Field(
        description="expected step",
    )
    
class TestCase(BaseModel):
    test_case_id: int  = Field(
        description="step number",
    )
    test_case_title: str  = Field(
        description="test case id",
    )
    test_steps: List[TestStep]  = Field(
        description="list of test cases",
    )

class TestCases(BaseModel):
    test_cases: List[TestCase]  = Field(
        description="list of test cases",
    )

class AgentState(TypedDict):
    user_story : UserStory
    test_cases: TestCases
    final_data :DataFrame