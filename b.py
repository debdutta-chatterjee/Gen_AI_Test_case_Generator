from src.azure.azure import AzureConnection
import os
from src.llm.groq_llm import ChatGroq
from src.graph.graph_builder import GraphBuilder
from src.node.node import Node
from src.state.state import AgentState

api_key = os.environ["API_KEY"]
ado_url = 'https://dev.azure.com/debduttachatterjee09/Agile-US'
pat = 'GEQ76Z0xhwg7ewAkpl2pa7nrsnd74d4VQftOms7OkiwaORogU91WJQQJ99BCACAAAAAAAAAAAAASAZDO2sBr'
ado_us_id = '2' 

#Get US details
ado = AzureConnection()
us_details = ado.get_user_story_details(ado_url,pat,ado_us_id)

#llm
model = ChatGroq(groq_api_key=api_key,model_name="qwen-2.5-32b")

#graph
node = Node(model)
builder = GraphBuilder(node)
graph = builder.build_test_case_graph()
flow = graph.compile()

#invoke graph
initial_state = {
    "user_story": us_details
}

#flow.invoke(initial_state)

state = AgentState(**dict(flow.invoke(initial_state)))
df = state["final_data"]
print(df)