from pydantic import BaseModel
from typing import List, Optional
from typing import Dict, TypedDict, Annotated

class TestCase(BaseModel):
    test_case_name: str
    description: str
    expected_result: str
    actual_result: str

class TestSuite(BaseModel):
    test_cases: List[TestCase] 

class AgentState(TypedDict):
    requirement: str
    suite: TestSuite