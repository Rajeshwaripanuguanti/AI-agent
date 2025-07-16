#langchain
#transformers
from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.agents import initialize_agent,Tool
from langchain.agents.agent_types import AgentType
#setup LLM using HuggingFacePipeline
generator=pipeline("text-generation",model="google/flan-t5-small")
llm=HuggingFacePipeline(pipeline=generator)


#define a tool:Task breakdown tool
def breakdown_task_tool(input):
    return f"""here's how to break down this task
           1.understand the topic
           2.Research latest trends in AI and education
           3.create an outline(intro,steps,conclusion)
           4.write each section
           5.polish"""

#create tool
tool=[Tool(name="LearnPlanner",func=breakdown_task_tool,
    description="""use this tool to break large goal to smaller goal""")]

#create agent
agent=initialize_agent(tools=tool,llm=llm,
          agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
          verbose=True)
          
#run agent
goal="Write a blog about the future of AI and education?"
response=agent.run(goal)
print("Task plan\n",response)