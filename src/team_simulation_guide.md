# Team Simulation Guide

This guide will help you use the various team simulation modules to explore and understand team dynamics, leadership, and organizational behavior concepts through AI-powered simulations.

## Introduction

The Team Simulation Project provides a set of tools to model and analyze team interactions, leadership styles, and collaborative dynamics using AI agents. These simulations allow you to:

1. Create controlled experiments to test leadership theories
2. Explore how team diversity affects problem-solving
3. Analyze how different team structures influence outcomes
4. Compare team performance across different scenarios
5. Collect rich qualitative and quantitative data on team behavior

By running these simulations, you can gain insights into team dynamics that would be difficult to observe directly in real-world settings due to time constraints, ethical considerations, or practical limitations.

## Available Simulation Modules

### 1. Leadership Style Simulation

Located in `src/leadership_style_simulation.py`, this module allows you to compare how different leadership styles affect team performance and dynamics.

**Leadership Styles Available:**
- **Authoritarian**: Directive approach with clear hierarchy and centralized decision-making
- **Democratic**: Collaborative approach that involves team members in decisions
- **Laissez-faire**: Hands-off approach that gives team members high autonomy
- **Transformational**: Inspirational approach focused on vision and team development

**Example Usage:**
```python
from leadership_style_simulation import LeadershipStyleSimulation, run_leadership_comparison

# Run a single leadership style simulation
sim = LeadershipStyleSimulation(
    simulation_name="plastic_waste_project",
    leadership_style="democratic",
    team_size=4,
    model="gpt-4o-mini"
)
sim.setup_team()
sim.setup_creative_task()  # or sim.setup_crisis_task()
results = sim.run_simulation()
sim.save_results()

# Or compare all leadership styles on the same task
results = run_leadership_comparison(task_type="creative", model="gpt-4o-mini")
```

**Research Questions to Explore:**
- Which leadership style leads to more creative solutions?
- How does leadership style impact team member satisfaction and engagement?
- Which leadership style is most effective in crisis situations?
- How do different personality types respond to various leadership styles?

### 2. Diversity and Inclusion Simulation

Located in `src/diversity_inclusion_simulation.py`, this module explores how team diversity and inclusion practices affect team outcomes.

**Variables to Manipulate:**
- **Diversity Level**: High vs. low cognitive and demographic diversity
- **Inclusion Practices**: High vs. low levels of inclusive team behaviors
- **Task Types**: Innovation tasks vs. decision-making tasks

**Example Usage:**
```python
from diversity_inclusion_simulation import DiversityInclusionSimulation, run_diversity_inclusion_comparison

# Run a single diversity/inclusion configuration
sim = DiversityInclusionSimulation(
    simulation_name="mental_health_app",
    team_size=5,
    diversity_level="high",
    inclusion_level="high",
    model="gpt-4o-mini"
)
sim.setup_team()
sim.setup_innovation_task()  # or sim.setup_decision_task()
results = sim.run_simulation()
sim.save_results()

# Or compare all diversity/inclusion configurations
results = run_diversity_inclusion_comparison(task_type="innovation", model="gpt-4o-mini")
```

**Research Questions to Explore:**
- How does cognitive diversity impact innovation quality?
- Do inclusive practices mitigate potential conflicts in diverse teams?
- Which team configuration performs best on different types of tasks?
- What are the interaction effects between diversity and inclusion?

## Creating Your Own Simulations

You can extend these simulations or create entirely new ones:

1. **Modify Existing Parameters**: Adjust team size, personality traits, or task descriptions
2. **Create New Task Types**: Define different tasks that test specific team dynamics
3. **Add New Variables**: Introduce new factors like team structure, communication channels, or time pressure
4. **Combine Modules**: Integrate leadership styles with diversity factors

## Running Simulations

All simulations follow a similar pattern:

1. **Initialize**: Create a simulation object with desired parameters
2. **Setup**: Configure the team and task scenario
3. **Run**: Execute the simulation
4. **Analyze**: Process and interpret the results

### Best Practices

- **Start Simple**: Begin with smaller teams (3-5 members) and shorter tasks
- **Use Efficient Models**: For initial testing, use smaller models like `gpt-4o-mini`
- **Compare Conditions**: Always run multiple configurations for comparison
- **Collect Multiple Runs**: Run each configuration multiple times to account for variability
- **Save All Results**: Keep comprehensive records for later analysis

## Analyzing Simulation Results

Each simulation saves results as JSON files that include:
- Team composition and characteristics
- Task descriptions
- Process metrics (time, interactions)
- Output quality and content
- Agent behaviors and contributions

You can use the provided `analyze_simulation_results.py` script to:
- Extract key themes from simulation outputs
- Count contributions from different team members
- Analyze sentiment and agreement patterns
- Visualize team dynamics
- Compare results across different conditions

## Example Research Projects

Here are some example research questions you could explore:

1. **Leadership Effectiveness**: Compare leadership styles across different types of tasks to determine which is most effective in which context.

2. **Diversity and Innovation**: Investigate how team diversity affects innovation quality and the types of solutions generated.

3. **Conflict Management**: Examine how different leadership approaches handle team conflict and which produces the most constructive outcomes.

4. **Decision Quality**: Compare the quality of decisions made by teams with different configurations and processes.

5. **Team Development**: Track how team dynamics evolve over multiple related tasks under consistent leadership.

## Technical Requirements

To run these simulations, you need:

- Python 3.8 or higher
- Required libraries (install via `pip install -r requirements.txt`)
- An OpenAI API key (set in your environment variables or `.env` file)
- Sufficient API credits for your planned simulations

## Best Practices for Reporting Results

When writing up your findings:

1. **Clearly Define Parameters**: Document all simulation settings and configurations
2. **Present Comparative Data**: Always compare across conditions rather than analyzing a single run
3. **Include Qualitative Examples**: Share illustrative excerpts from agent interactions
4. **Acknowledge Limitations**: Discuss the constraints of AI simulations vs. real human teams
5. **Connect to Theory**: Relate your findings to established team and leadership theories

## Additional Resources

- Check the `examples/` directory for sample simulations and analysis scripts
- Refer to `examples/crewai_setup_guide.md` for detailed CrewAI setup instructions
- Review the CrewAI documentation for advanced agent configuration options: https://docs.crewai.com/

## Troubleshooting

Common issues and solutions:

- **API Rate Limits**: If you encounter rate limits, add delay between API calls or use a smaller model
- **Long Runtime**: For faster testing, reduce team size or use simpler tasks
- **Agent Quality**: If agent responses seem generic, try improving their backstories and more specific role descriptions
- **Result Variability**: Run multiple simulations with the same configuration to establish patterns

## Conclusion

Team simulations offer a powerful way to explore leadership and team dynamics concepts. By systematically manipulating variables and comparing outcomes, you can develop insights into how different factors influence team performance.

Remember that while these AI-powered simulations provide valuable data, they represent simplified models of human behavior. Use your findings as starting points for deeper investigation and discussion rather than definitive conclusions about real-world team dynamics. 