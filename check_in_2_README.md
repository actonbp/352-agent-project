# Check-in 2: Basic Team Simulation

This check-in provides a simplified working script for team simulations using CrewAI. The script demonstrates how to create a small team with different roles and personalities working together on a basic task.

## What's Included

- `check_in_2_basic_simulation.py`: A complete, working script that simulates a product team
- Documentation of the key classes and methods
- Sample implementation of a 3-person team working on a product feature

## Getting Started

1. Make sure you have the required packages installed:
   ```
   pip install -r requirements.txt
   ```

2. Set up your OpenAI API key:
   - Create a `.env` file in the project directory
   - Add your API key: `OPENAI_API_KEY=your-api-key-here`

3. Run the example simulation:
   ```
   python check_in_2_basic_simulation.py
   ```

## Understanding the Code

The script is organized into two main parts:

1. **BasicTeamSimulation class**: This is the core simulation engine that:
   - Creates team members with different roles and personalities
   - Assigns tasks to team members
   - Runs the simulation with CrewAI
   - Processes and saves the results

2. **Sample implementation**: The `run_product_team_simulation()` function shows how to:
   - Set up a product team with a leader, designer, and developer
   - Configure their personalities and expertise
   - Create relevant tasks for the team
   - Run the simulation and save results

## Customization Options

You can customize the simulation by:

- **Changing team members**: Add more members with different roles, expertise, and personalities
- **Modifying leadership style**: Try different leadership styles (democratic, authoritarian, etc.)
- **Creating new tasks**: Design tasks specific to your research questions
- **Adjusting the context**: Provide different scenarios for the team to work on

## Example Customization

Here's how you might customize the simulation for your own research:

```python
# Create a custom simulation
sim = BasicTeamSimulation("my_custom_team", model="gpt-4o-mini")

# Create team members with different roles
leader = sim.create_team_leader("Jamie", leadership_style="authoritarian")
researcher = sim.create_team_member(
    "Casey", 
    "Market Researcher", 
    "consumer behavior analysis",
    personality={"openness": 0.6, "conscientiousness": 0.8}
)
engineer = sim.create_team_member(
    "Robin", 
    "Engineering Lead", 
    "product engineering",
    personality={"conscientiousness": 0.9, "extraversion": 0.3}
)
designer = sim.create_team_member(
    "Avery", 
    "Visual Designer", 
    "branding and aesthetics",
    personality={"openness": 0.9, "extraversion": 0.8}
)

# Set a custom context
context = """
Your team is working on rebranding a well-established consumer product
that has been losing market share to newer competitors.
The product needs a fresh look while maintaining brand recognition.
You have 2 months to complete the rebrand before the holiday season.
"""

# Add custom tasks
sim.add_task(
    description="Develop a comprehensive rebranding strategy",
    assigned_to=leader,
    expected_output="A detailed rebranding plan with timeline and resource allocation",
    context=context
)

# Add more tasks and run the simulation
# ...

# Run the simulation
results = sim.run_simulation()
```

## Next Steps

After running the basic simulation, consider:

1. **Analyzing the results**: Look at how different team members contributed and interacted
2. **Comparing different configurations**: Try changing team composition or leadership styles
3. **Expanding the simulation**: Add more team members or more complex tasks
4. **Designing experiments**: Create systematic variations to test specific hypotheses

## Resources

For more information, refer to:

- [Team Simulation Guide](src/team_simulation_guide.md)
- [CrewAI Documentation](https://docs.crewai.com/)
- Example simulations in the `examples/` directory 