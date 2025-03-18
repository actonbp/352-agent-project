# Custom Team Simulation Guide

This guide will help you design and run custom team simulations that match your specific research questions. Unlike the more structured Leadership or Diversity simulations, this module gives you complete flexibility in designing team compositions, personalities, and task types.

## What This Simulation Allows

The custom Team Simulation module enables you to:

- Design teams with completely customized roles and personalities
- Create unique tasks specific to your research question
- Define custom interaction patterns and processes
- Measure specific outcomes and metrics
- Introduce your own variables of interest

## Getting Started

### Step 1: Design Your Team

Start by designing the team composition that matches your research question:

```python
from src.team_simulation import TeamSimulation

# Create a new simulation
sim = TeamSimulation(
    simulation_name="my_custom_simulation",
    team_size=5,  # Number of team members
    model="gpt-4o-mini"  # Model to use for agents
)

# Add team members with custom roles and personalities
sim.add_team_member(
    role="Product Manager",
    traits=["organized", "decisive", "strategic", "diplomatic"],
    background="5 years experience in tech product management",
    communication_style="direct but tactful"
)

sim.add_team_member(
    role="UX Designer",
    traits=["creative", "empathetic", "detail-oriented", "visual thinker"],
    background="Graphic design background with focus on user interfaces",
    communication_style="visual and metaphor-rich"
)

# Add more team members as needed...
```

### Step 2: Create Custom Tasks

Define tasks that align with your research question:

```python
# Add a brainstorming task
sim.add_task(
    task_name="Feature Brainstorming",
    description="Generate 10 innovative features for our new mobile app",
    assigned_to="UX Designer",  # Assign to specific role
    expected_output="List of 10 features with brief descriptions",
    complexity="medium"  # low, medium, high
)

# Add a decision-making task
sim.add_task(
    task_name="Feature Prioritization",
    description="Prioritize the 10 features based on user value and development effort",
    assigned_to="Product Manager",
    expected_output="Prioritized list with rationale for each decision",
    complexity="high",
    dependencies=["Feature Brainstorming"]  # This task depends on the first task
)

# Add a collaborative task
sim.add_task(
    task_name="Integration Planning",
    description="Plan how features will integrate with existing systems",
    assigned_to=["Product Manager", "UX Designer", "Developer"],  # Assign to multiple roles
    expected_output="Integration roadmap document",
    complexity="high",
    requires_consensus=True  # Team must reach consensus on this task
)
```

### Step 3: Define Team Processes

Choose how your team will work together:

```python
# Run the simulation with your chosen process type
results = sim.run_simulation(
    process_type="hierarchical",  # or "sequential" or "collaborative"
    communication_constraints={
        "async_only": False,        # True for asynchronous communication only
        "limited_visibility": False  # True if members can only see certain messages
    },
    conflict_probability=0.2  # Probability of generating conflicting perspectives
)
```

### Step 4: Save and Analyze Results

```python
# Save the results
sim.save_results()

# Analyze specific aspects of the interaction
from src.analysis import SimulationAnalyzer

analyzer = SimulationAnalyzer(results)
contribution_metrics = analyzer.get_contribution_metrics()
process_metrics = analyzer.get_process_metrics()
outcome_quality = analyzer.evaluate_outcome_quality()

print(f"Contribution balance: {contribution_metrics['balance_score']}")
print(f"Process efficiency: {process_metrics['efficiency_score']}")
print(f"Outcome quality: {outcome_quality['quality_score']}")
```

## Available Customization Options

### Team Member Attributes

You can customize these attributes for each team member:

- **Role**: The team member's formal role or title
- **Traits**: Personality characteristics that influence behavior
- **Background**: Educational or professional experience
- **Communication style**: How they typically express themselves
- **Expertise level**: Their level of skill (novice, intermediate, expert)
- **Motivations**: What drives their behavior and decisions
- **Working style**: How they prefer to approach tasks

### Task Properties

Tasks can be customized with these properties:

- **Task name**: A descriptive name
- **Description**: Detailed description of the task objectives
- **Assigned to**: Specific roles or members who should complete it
- **Expected output**: Format and content of the deliverable
- **Complexity**: How challenging the task is (low, medium, high)
- **Dependencies**: Other tasks that must be completed first
- **Deadline**: Time constraint (in simulation time units)
- **Requires consensus**: Whether the team must agree on the outcome
- **Success criteria**: Specific requirements to consider the task successful

### Process Types

Your team can operate in several ways:

- **Sequential**: Tasks are completed one after another in a predefined order
- **Hierarchical**: Tasks have dependencies, creating a structured workflow
- **Collaborative**: All team members work together on tasks simultaneously
- **Adaptive**: The process changes based on task outcomes and team performance

### Communication Constraints

Simulate different communication environments:

- **Async only**: Members can only communicate asynchronously
- **Limited visibility**: Members can only see certain messages
- **Structured updates**: Communication happens only at specific intervals
- **Communication delay**: Messages have a delay before being received
- **Information asymmetry**: Different members have access to different information

## Example Research Questions

This flexible simulation module is ideal for exploring questions such as:

- How does information asymmetry affect team decision quality?
- What communication patterns emerge in remote vs. co-located teams?
- How do teams with diverse expertise levels resolve technical conflicts?
- What effect does time pressure have on team collaboration patterns?
- How do different conflict resolution strategies affect team outcomes?
- What impact does role clarity have on team efficiency and satisfaction?

## Example: Investigating Communication Patterns

Here's an example that investigates different communication patterns:

```python
# Create the simulation
sim = TeamSimulation(
    simulation_name="communication_patterns",
    team_size=6,
    model="gpt-4o"
)

# Add team members with varied communication styles
sim.add_team_member(
    role="Team Lead",
    traits=["structured", "direct", "logical"],
    communication_style="concise and to-the-point"
)

sim.add_team_member(
    role="Creative Director",
    traits=["imaginative", "expressive", "intuitive"],
    communication_style="metaphor-rich and visual"
)

sim.add_team_member(
    role="Technical Expert",
    traits=["analytical", "precise", "detail-oriented"],
    communication_style="technical and detailed"
)

sim.add_team_member(
    role="Account Manager",
    traits=["relationship-focused", "diplomatic", "attentive"],
    communication_style="relationship-oriented and diplomatic"
)

sim.add_team_member(
    role="Project Coordinator",
    traits=["organized", "process-oriented", "thorough"],
    communication_style="structured and process-focused"
)

sim.add_team_member(
    role="New Hire",
    traits=["curious", "eager", "adaptable"],
    communication_style="questioning and seeking clarification"
)

# Define a complex problem-solving task
sim.add_task(
    task_name="Strategic Planning",
    description="Develop a strategic plan for launching a new product in an emerging market",
    assigned_to=["Team Lead", "Creative Director", "Technical Expert", 
                "Account Manager", "Project Coordinator", "New Hire"],
    expected_output="Comprehensive strategic plan document",
    complexity="high",
    requires_consensus=True
)

# Run three different simulations with different communication structures
centralized_results = sim.run_simulation(
    process_type="hierarchical",
    communication_constraints={
        "centralized": True  # All communication goes through the team lead
    }
)
sim.save_results("centralized_communication")

distributed_results = sim.run_simulation(
    process_type="collaborative",
    communication_constraints={
        "centralized": False  # Direct communication between all members
    }
)
sim.save_results("distributed_communication")

# Analyze and compare the results
# ...
```

## Advanced Features

### Introducing External Events

You can introduce events during the simulation:

```python
sim.add_external_event(
    event_name="Budget Cut",
    description="The project budget has been reduced by 30%",
    trigger_after_task="Initial Planning",
    affected_roles=["Team Lead", "Project Coordinator"]
)
```

### Tracking Specific Metrics

Define custom metrics to track:

```python
sim.track_metric(
    metric_name="idea_generation_rate",
    description="Number of unique ideas generated per hour",
    measurement_method="count_unique_concepts_per_time_unit"
)
```

### Custom Agent Behaviors

Create agents with specific behavioral tendencies:

```python
sim.add_team_member(
    role="Devil's Advocate",
    traits=["critical", "analytical", "challenging"],
    behavioral_prompts=[
        "Always question assumptions behind ideas",
        "Regularly point out potential flaws in plans",
        "Ask 'what if' questions to test robustness of proposals"
    ]
)
```

## Tips for Effective Custom Simulations

1. **Start with a clear research question**: Design your team and tasks to specifically address your question
2. **Control your variables**: Change only one variable at a time to isolate effects
3. **Use appropriate team size**: 3-7 members is usually optimal for meaningful interactions
4. **Balance complexity**: Too simple gives shallow results, too complex becomes unmanageable
5. **Run multiple variations**: Compare different configurations for robust findings
6. **Create realistic scenarios**: Base your tasks on real-world situations relevant to your field
7. **Document your configuration**: Keep detailed notes on all customizations for reproducibility

## Need Help?

If you need assistance designing your custom simulation:

1. Review the example notebooks in the `examples/custom_simulations` folder
2. Consult the API documentation for the `TeamSimulation` class
3. Use the GitHub discussions forum for specific questions
4. Attend office hours for personalized guidance 