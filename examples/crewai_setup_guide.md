# CrewAI Setup Guide for Team Simulations

This guide will help you set up and use CrewAI for your team simulation project.

## What is CrewAI?

CrewAI is a framework for orchestrating role-playing autonomous AI agents. It allows you to create a "crew" of agents with different roles, goals, and personalities, then assign them tasks to work on together. This is perfect for simulating team dynamics!

## Prerequisites

1. **Python 3.8+**: Make sure you have Python installed
2. **OpenAI API Key**: You'll need this to use the language models
3. **Required Libraries**: Install from requirements.txt

## Setup Steps

### 1. Install Required Packages

```bash
# In your terminal or command prompt
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in your project directory with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

To get an OpenAI API key:
1. Go to [OpenAI's platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API keys and create a new key

### 3. Understanding the Basic Components

CrewAI has three main components:

1. **Agents**: AI agents with specific roles, goals, and backstories
2. **Tasks**: Specific assignments for agents to complete
3. **Crew**: The orchestrator that manages agents and their tasks

## Creating Your Team Simulation

### Step 1: Define Your Research Question

Before coding, clarify what aspect of team dynamics you want to explore, for example:
- How does personality diversity affect problem-solving?
- What impact does a deviant member have on team creativity?
- How do different leadership styles affect team performance?

### Step 2: Design Your Agents

Create agents with different characteristics:

```python
from crewai import Agent

team_leader = Agent(
    role="Team Leader",
    goal="Lead the team effectively to accomplish the project goals",
    backstory="""You are a team leader with 5 years of experience.
    You have a directive leadership style and value efficiency.""",
    verbose=True,
    allow_delegation=True
)

creative_member = Agent(
    role="Creative Designer",
    goal="Contribute innovative ideas to the project",
    backstory="""You are a creative professional with a keen eye for innovation.
    You think outside the box and sometimes challenge conventional approaches.""",
    verbose=True
)
```

### Step 3: Create Tasks

Define what your team needs to accomplish:

```python
from crewai import Task

brainstorming_task = Task(
    description="Brainstorm 5 innovative solutions to the given problem",
    agent=creative_member,
    expected_output="A list of 5 innovative solutions with brief explanations"
)

planning_task = Task(
    description="Create a project plan based on the team's ideas",
    agent=team_leader,
    expected_output="A comprehensive project plan with timelines and responsibilities"
)
```

### Step 4: Form a Crew and Run the Simulation

```python
from crewai import Crew, Process

crew = Crew(
    agents=[team_leader, creative_member, technical_member],
    tasks=[brainstorming_task, planning_task, implementation_task],
    verbose=2,
    process=Process.hierarchical  # or Process.sequential
)

results = crew.kickoff()
```

## Example Scenarios

Check out `crewai_team_simulation.py` for a complete example of:
- A 5-member team with diverse personalities
- One "deviant" member who challenges group thinking
- Multiple tasks to complete together
- Hierarchical process flow
- Results collection and analysis

## Analyzing Results

After running your simulation, you can analyze the output to answer your research question:

1. **Qualitative Analysis**: Review the content of agent outputs
   - What ideas did they generate?
   - How did they interact with each other?
   - How did they resolve conflicts?

2. **Quantitative Analysis**:
   - Count instances of agreement/disagreement
   - Measure task completion time
   - Evaluate solution quality against criteria

## Tips for Success

1. **Be Specific with Agent Backstories**: The more detail you provide about personality traits and work style, the more realistic the simulation will be.

2. **Use Clear Task Descriptions**: Clearly define what each agent needs to do.

3. **Try Different Process Types**:
   - `Process.sequential`: Tasks are completed one after another
   - `Process.hierarchical`: Allows for more complex workflows with delegation

4. **Save and Compare Results**: Run multiple simulations with different team compositions to compare outcomes.

## Troubleshooting

- **API Rate Limits**: If you hit OpenAI rate limits, add a delay between API calls or use a different model
- **Memory Issues**: For complex simulations, consider running on a machine with more RAM
- **Output Quality**: If outputs are too generic, try adjusting the agent backstories to be more specific 