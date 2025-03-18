# Diversity and Inclusion Simulation Guide

This guide will help you use the Diversity and Inclusion Simulation module to explore how team composition and inclusive practices affect team dynamics and outcomes.

## What This Simulation Does

The Diversity and Inclusion Simulation allows you to investigate:

- How cognitive diversity affects problem-solving and innovation
- How inclusive practices impact team participation and engagement
- How different combinations of diversity and inclusion affect outcomes
- Which team configurations perform best on different types of tasks

The simulation allows you to compare four different team configurations:
1. High diversity + high inclusion
2. High diversity + low inclusion
3. Low diversity + high inclusion
4. Low diversity + low inclusion

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
3. Create a Python script (e.g., `my_diversity_sim.py`) with the following code:

```python
from src.diversity_inclusion_simulation import DiversityInclusionSimulation, run_diversity_inclusion_comparison

# To run a single configuration:
sim = DiversityInclusionSimulation(
    simulation_name="my_diversity_project",
    team_size=5,
    diversity_level="high",  # Choose from: high, low
    inclusion_level="high",  # Choose from: high, low
    model="gpt-4o-mini"  # Use gpt-4o-mini for faster/cheaper simulations
)
sim.setup_team()
sim.setup_innovation_task()  # or sim.setup_decision_task()
results = sim.run_simulation()
sim.save_results()

# To compare all diversity/inclusion configurations:
# results = run_diversity_inclusion_comparison(task_type="innovation", model="gpt-4o-mini")
```

4. Run the script with `python my_diversity_sim.py`

## Understanding the Simulation

### Diversity Levels

The simulation models diversity across several dimensions:

- **Cognitive diversity**: Different thinking styles, problem-solving approaches, and communication styles
- **Background diversity**: Varied educational backgrounds and expertise areas
- **Experiential diversity**: Different levels of experience and perspective

In **high diversity** teams, members have significantly different thinking styles, backgrounds, and approaches. In **low diversity** teams, members have more homogeneous profiles and similar approaches.

### Inclusion Levels

The simulation also models different levels of inclusion practices:

**High inclusion** teams feature:
- All members explicitly invited to contribute
- Diverse perspectives actively sought out
- Decision-making processes involve everyone
- Communication is transparent and accessible

**Low inclusion** teams feature:
- Interactions dominated by a few voices
- Alternative perspectives rarely sought out
- Decision-making happens informally among select members
- Communication is inconsistent

## Task Types

The simulation supports two types of tasks:

1. **Innovation Task**: A creative challenge to develop a digital solution for university student mental health
   ```python
   sim.setup_innovation_task()
   ```

2. **Decision Task**: A complex decision about international market expansion for a company
   ```python
   sim.setup_decision_task()
   ```

## Customizing the Simulation

### Team Size

You can adjust the team size (default is 5):

```python
sim = DiversityInclusionSimulation(
    simulation_name="my_project",
    team_size=4,  # Change this number
    diversity_level="high",
    inclusion_level="high",
    model="gpt-4o-mini"
)
```

### Process Type

You can change how tasks are processed:

```python
# Sequential: Team members work through tasks in sequence
results = sim.run_simulation(process_type="sequential")

# Hierarchical: Tasks have dependencies and hierarchy
results = sim.run_simulation(process_type="hierarchical")
```

## Example Research Questions

This simulation can help you explore questions such as:

- How does cognitive diversity affect innovation quality?
- Do inclusive practices mitigate potential conflicts in diverse teams?
- Which team configuration performs best on different types of tasks?
- Is there an interaction effect between diversity and inclusion?
- How do various team roles contribute in high vs. low diversity teams?

## Tips for Effective Simulations

1. **Compare multiple configurations**: Always run at least two different configurations to see contrasts
2. **Be systematic**: Change only one variable at a time for clearer comparisons
3. **Run multiple simulations**: Results can vary, so multiple runs provide more reliable insights
4. **Analyze team interactions**: Look beyond outcomes to examine communication patterns
5. **Use faster models**: For initial tests, use `gpt-4o-mini` to save time and API costs

## Analyzing Your Results

See the [Analyzing Simulation Results](analyzing_results_guide.md) guide for detailed instructions on how to extract insights from your simulation data.

## Technical Details

The simulation works by:
- Generating team member profiles with varied thinking styles and backgrounds
- Creating a team facilitator with specific inclusion behaviors
- Assigning role-appropriate tasks to each team member
- Tracking interactions and measuring outcomes
- Saving detailed results for analysis

The code uses a random seed to ensure that "high diversity" teams consistently have more varied characteristics than "low diversity" teams. 