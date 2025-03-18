# CrewAI Setup and Usage Guide

This guide explains how to set up and use CrewAI for your team simulations, including information about compatible language models and best practices.

## What is CrewAI?

CrewAI is an open-source framework for orchestrating role-playing, autonomous AI agents. In our team simulations, CrewAI allows us to:

- Create team members with specific roles and personalities
- Assign tasks with dependencies
- Facilitate interactions between team members
- Collect and analyze team outcomes

## Compatible OpenAI Models

CrewAI supports various OpenAI models, with recent updates including:

### GPT-4 Models
- **GPT-4**: Original high-performance model, excellent for complex reasoning
- **GPT-4 Turbo (gpt-4-turbo-2024-04-09)**: Faster and more efficient than GPT-4
- **GPT-4o (gpt-4o-2024-05-13)**: Optimized for general-purpose tasks
- **GPT-4o-mini (gpt-4o-mini-2024-07-18)**: More affordable and faster version of GPT-4o

### O1 Model Family
- **o1-preview**: Most capable OpenAI model for reasoning
- **o1-mini**: More affordable version with strong reasoning capabilities

### Recommended Models for Simulations

For team simulations, we recommend:

| Use Case | Recommended Model | Alternative Model |
|----------|-------------------|-------------------|
| Quick, cheap tests | `gpt-4o-mini` | `gpt-3.5-turbo` |
| Standard simulations | `gpt-4o` | `gpt-4-turbo` |
| High-quality simulations | `o1-mini` | `gpt-4o` |
| Research-grade results | `o1-preview` | `gpt-4` |

## Setting Up Your Environment

### 1. Install Required Packages

```bash
pip install crewai openai
```

### 2. Set Up Your API Key

Create a `.env` file in your project directory:
```
OPENAI_API_KEY=your_api_key_here
```

Load it in your Python code:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. Basic CrewAI Structure

A CrewAI simulation typically follows this structure:

```python
from crewai import Agent, Task, Crew, Process

# Create agents (team members)
team_leader = Agent(
    role="Team Leader",
    goal="Guide the team to achieve project goals efficiently",
    backstory="An experienced leader with 10 years in project management",
    verbose=True,
    allow_delegation=True,
    llm=OpenAI(model="gpt-4o")  # Specify model here
)

# Add more team members...

# Create tasks
task1 = Task(
    description="Develop a project timeline with key milestones",
    expected_output="A detailed project timeline in markdown format",
    agent=team_leader
)

# Add more tasks...

# Create and run the crew (team)
crew = Crew(
    agents=[team_leader, member1, member2, member3],
    tasks=[task1, task2, task3],
    process=Process.sequential  # or Process.hierarchical
)

result = crew.kickoff()
```

## Specifying Different Models for Agents

You can assign different models to different agents:

```python
from crewai import Agent
from langchain_openai import ChatOpenAI

# Team leader uses the most capable model
team_leader = Agent(
    role="Team Leader",
    goal="Guide the team effectively",
    backstory="Experienced leader with strategic vision",
    llm=ChatOpenAI(model="o1-mini")  # Premium model for leader
)

# Regular team member uses standard model
team_member = Agent(
    role="Team Member",
    goal="Support the team with technical work",
    backstory="Junior employee with technical skills",
    llm=ChatOpenAI(model="gpt-4o-mini")  # More affordable model
)
```

## Azure OpenAI Support

If you're using Azure OpenAI, configure it like this:

```python
from langchain_openai import AzureChatOpenAI

azure_llm = AzureChatOpenAI(
    azure_deployment="your-deployment-name",
    openai_api_version="2023-05-15",
)

agent = Agent(
    role="Team Member",
    goal="Complete assigned tasks",
    backstory="...",
    llm=azure_llm
)
```

## Customizing Agent Personalities

For team simulations, you can customize agent personalities:

```python
analytical_member = Agent(
    role="Data Analyst",
    goal="Provide data-driven insights",
    backstory="Detail-oriented professional who relies on facts and logic",
    traits=["analytical", "detail-oriented", "logical", "cautious"],
    llm=ChatOpenAI(model="gpt-4o")
)

creative_member = Agent(
    role="Creative Director",
    goal="Generate innovative ideas",
    backstory="Visionary thinker who pushes boundaries",
    traits=["creative", "risk-taking", "inspirational", "unstructured"],
    llm=ChatOpenAI(model="gpt-4o")
)
```

## Task Dependencies and Process Types

CrewAI supports two types of processes:

1. **Sequential**: Tasks are completed one after another
   ```python
   crew = Crew(
       agents=[agent1, agent2, agent3],
       tasks=[task1, task2, task3],
       process=Process.sequential
   )
   ```

2. **Hierarchical**: Tasks can have dependencies
   ```python
   task2 = Task(
       description="Implement the design",
       expected_output="Working implementation",
       agent=developer,
       dependencies=[task1]  # This task depends on task1
   )
   
   crew = Crew(
       agents=[agent1, agent2, agent3],
       tasks=[task1, task2, task3],
       process=Process.hierarchical
   )
   ```

## Saving and Analyzing Results

To save simulation results:

```python
import json
from datetime import datetime

# Run simulation
result = crew.kickoff()

# Save results
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data/results/simulation_{timestamp}.json"

with open(filename, 'w') as f:
    json.dump({
        'timestamp': timestamp,
        'configuration': {
            'agents': [a.role for a in crew.agents],
            'process': str(crew.process)
        },
        'result': result,
        'interactions': crew.memory.raw_memory  # Get all interactions
    }, f, indent=2)
```

## Tips for Effective Simulations

1. **Start simple**: Begin with fewer agents (2-3) and straightforward tasks
2. **Use specific roles**: Clearly define each team member's role and goals
3. **Be explicit with tasks**: Provide clear instructions and expected outputs
4. **Manage costs**: Use `gpt-4o-mini` for testing, then switch to more capable models
5. **Monitor token usage**: More complex simulations use more tokens
6. **Save interactions**: Always save full interaction logs for later analysis
7. **Run multiple configurations**: Compare different team compositions and processes

## Troubleshooting Common Issues

### API Key Issues
```
Error: OpenAI API key not found
```
Solution: Ensure your `.env` file exists and contains `OPENAI_API_KEY=your_key`.

### Token Limit Exceeded
```
Error: This model's maximum context length is 16385 tokens
```
Solution: Simplify tasks, reduce agent backstories, or use a model with higher context limits.

### Rate Limits
```
Error: Rate limit reached for gpt-4 in organization
```
Solution: Implement exponential backoff or switch to a model with higher rate limits.

## Advanced Usage

### Memory and Context

CrewAI agents maintain memory of past interactions. You can customize this:

```python
from crewai.memory import Memory

custom_memory = Memory()
agent = Agent(
    role="Analyst",
    goal="Analyze data accurately",
    memory=custom_memory
)
```

### Custom Tools

You can equip agents with custom tools:

```python
from crewai import Agent, Tool

calculate_tool = Tool(
    name="Calculator",
    description="Useful for performing numerical calculations",
    func=lambda input_text: eval(input_text)
)

analyst = Agent(
    role="Financial Analyst",
    goal="Provide accurate financial projections",
    tools=[calculate_tool]
)
```

## Coming Soon: New Model Support

CrewAI is regularly updated to support new models as they're released. Check the [CrewAI GitHub repository](https://github.com/joaomdmoura/crewAI) for the latest updates and model compatibility information.

## Need Help?

- Review the examples in the `examples` directory
- Consult the [CrewAI documentation](https://docs.crewai.com/)
- Ask questions on the GitHub Discussions board 