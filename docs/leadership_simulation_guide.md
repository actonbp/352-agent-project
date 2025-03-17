# Leadership Style Simulation Guide

This guide will help you use the Leadership Style Simulation module to explore how different leadership approaches affect team dynamics and outcomes.

## What This Simulation Does

The Leadership Style Simulation allows you to compare how teams perform under different leadership styles:

- **Authoritarian**: Directive approach with clear hierarchy and centralized decision-making
- **Democratic**: Collaborative approach that involves team members in decisions
- **Laissez-faire**: Hands-off approach that gives team members high autonomy
- **Transformational**: Inspirational approach focused on vision and team development

Each leadership style has different traits and behaviors that influence how the team interacts and performs on tasks.

## How to Use This Simulation

### Option 1: Run the simulation online (Recommended for beginners)

If you don't want to set up Python on your computer, you can use Google Colab to run the simulation online:

1. Visit [this Google Colab notebook](https://colab.research.google.com/drive/example-link) (link will be provided by your instructor)
2. Add your OpenAI API key when prompted
3. Run the cells to execute the simulation

### Option 2: Run the simulation on your computer

If you prefer to run the simulation locally:

1. Make sure you have installed Python and the required packages (see [Setup Guide](setup_python.md))
2. Create a file called `.env` with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Create a Python script (e.g., `my_simulation.py`) with the following code:

```python
from src.leadership_style_simulation import LeadershipStyleSimulation, run_leadership_comparison

# To run a single leadership style:
sim = LeadershipStyleSimulation(
    simulation_name="my_project",
    leadership_style="democratic",  # Choose from: authoritarian, democratic, laissez_faire, transformational
    team_size=4,
    model="gpt-4o-mini"  # Use gpt-4o-mini for faster/cheaper simulations
)
sim.setup_team()
sim.setup_creative_task()  # or sim.setup_crisis_task()
results = sim.run_simulation()
sim.save_results()

# To compare all leadership styles:
# results = run_leadership_comparison(task_type="creative", model="gpt-4o-mini")
```

4. Run the script with `python my_simulation.py`

## Understanding the Results

The simulation will generate detailed output showing:

1. The team's interactions and discussions
2. The solutions they developed
3. Performance metrics and contributions from each team member

Results are saved as JSON files in the `data/` directory, named according to the simulation parameters and timestamp.

## Customizing the Simulation

### Changing Team Size

You can adjust the team size by changing the `team_size` parameter when creating the simulation:

```python
sim = LeadershipStyleSimulation(
    simulation_name="my_project",
    leadership_style="democratic",
    team_size=3,  # Change this number
    model="gpt-4o-mini"
)
```

### Choosing Task Types

The simulation supports two types of tasks:

1. **Creative Task**: Focuses on innovation and idea generation
   ```python
   sim.setup_creative_task()
   ```

2. **Crisis Task**: Simulates handling an emergency situation
   ```python
   sim.setup_crisis_task()
   ```

### Modifying Team Member Personalities

You can customize team member personalities by editing the `team_personalities` list in the code. Advanced users can modify the source code to add additional personality types.

## Example Research Questions

This simulation can help you explore questions such as:

- Which leadership style leads to the most creative solutions?
- How does leadership style affect team member participation levels?
- Which leadership style is most effective in crisis situations?
- How do different personality types respond to various leadership styles?
- Does team size influence the effectiveness of certain leadership styles?

## Tips for Effective Simulations

1. **Run Multiple Simulations**: Leadership effects can vary, so run multiple simulations for more reliable results
2. **Compare Conditions**: Always run multiple leadership styles for comparison
3. **Save Your Results**: Keep all result files for analysis
4. **Start Simple**: Begin with smaller teams (3-4 members) and then try larger ones
5. **Use Faster Models**: Start with `gpt-4o-mini` for testing, then use `gpt-4` for final runs

## Analyzing Your Results

See the [Analyzing Simulation Results](analyzing_results_guide.md) guide for detailed instructions on how to extract insights from your simulation data.

## Technical Details

The simulation works by creating AI agents with specific:
- Personality traits (openness, conscientiousness, extraversion, agreeableness, neuroticism)
- Behaviors that align with different leadership styles
- Communication patterns
- Role-specific knowledge

These agents interact using the CrewAI framework to solve the assigned task while maintaining their defined characteristics. 