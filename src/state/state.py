from typing_extensions import TypedDict,Literal
from pydantic import BaseModel, Field
from typing import List

class UserStory(BaseModel):
    user_story: str  = Field(
        description="user story title",
    )
    business_context:str  = Field(
        description="business context",
    )
    acceptance_critera : str = Field(
        description="acceptance criteria",
    )

class TestScenario(BaseModel):
    test_scenario: str  = Field(
        description="test scenario",
    )
class TestScenarios(BaseModel):
    test_scenarios: List[TestScenario]  = Field(
        description="list of test scenarios",
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
    test_step: str  = Field(
        description="test steps",
    )
    step_action: str  = Field(
        description="action",
    )
    step_expected: str  = Field(
        description="expected step",
    )
class TestCase(BaseModel):
    test_case_id: str  = Field(
        description="test case id",
    )
    work_item_type: str  = Field(
        description="work item type",
    )
    state: str  = Field(
        description="state",
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
    test_scenarios: TestScenarios
    scenario_review: Feedback
    test_step_review: Literal["Accepted", "Rejected"] = "Rejected"
    test_case: TestCases