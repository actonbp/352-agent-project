# Analyzing Simulation Results

This guide will help you analyze and extract insights from your team simulation results, whether you're using the Leadership Style, Diversity and Inclusion, or other simulation modules.

## Accessing Your Simulation Results

After running a simulation, results are saved in the `data/results` directory with your simulation name:

```
data/results/your_simulation_name_YYYY-MM-DD_HH-MM-SS.json
```

You can also access results programmatically if you saved the output:

```python
# Results from your last simulation
results = sim.run_simulation()

# Results from a previously saved file
import json
with open('data/results/your_simulation_name.json', 'r') as f:
    results = json.load(f)
```

## What's In Your Results

Each simulation results file contains:

1. **Simulation metadata**:
   - Simulation name, type, and timestamp
   - Configuration settings (team size, model used, etc.)

2. **Team information**:
   - Team member profiles with roles and traits
   - Leadership style or diversity configuration

3. **Tasks**:
   - Task descriptions and requirements
   - Dependencies between tasks (if applicable)

4. **Interactions**:
   - Full conversation logs between team members
   - Decision-making processes
   - Contributions from each member

5. **Outcomes**:
   - Solutions or decisions produced
   - Quality metrics
   - Completion time

## Basic Analysis Techniques

### Using the Analysis Module

The simplest way to analyze results is using our built-in analysis module:

```python
from src.analysis import analyze_simulation

# Basic analysis of a single simulation
analysis = analyze_simulation("data/results/your_simulation_name.json")
print(analysis.summary())

# For comparing two simulations:
from src.analysis import compare_simulations
comparison = compare_simulations(
    "data/results/simulation1.json",
    "data/results/simulation2.json"
)
comparison.show_differences()
```

### Key Metrics to Consider

When analyzing results, consider these key dimensions:

1. **Participation balance**: 
   - How equally did team members contribute?
   - Were some voices dominant while others were marginalized?

2. **Process efficiency**:
   - How many interactions were required to complete tasks?
   - Were there unnecessary delays or confusion?

3. **Solution quality**:
   - How innovative and comprehensive was the final solution?
   - Did it effectively address all requirements?

4. **Collaboration patterns**:
   - How did information flow between team members?
   - Were there communication bottlenecks?

5. **Conflict and resolution**:
   - What disagreements emerged?
   - How were conflicting viewpoints handled?

## Advanced Analysis Techniques

### Text Analysis of Interactions

For deeper insights, you can analyze the text of team interactions:

```python
from src.analysis import TextAnalyzer

analyzer = TextAnalyzer("data/results/your_simulation_name.json")

# Sentiment analysis of interactions
sentiment_by_member = analyzer.get_sentiment_by_member()

# Topic modeling to see main discussion themes
topics = analyzer.extract_discussion_topics()

# Communication network analysis
network = analyzer.create_communication_network()
network.visualize()
```

### Comparative Analysis

To compare multiple simulations:

```python
from src.analysis import SimulationComparison

# Compare leadership styles
comparison = SimulationComparison([
    "data/results/authoritarian_sim.json",
    "data/results/democratic_sim.json",
    "data/results/laissez_faire_sim.json",
    "data/results/transformational_sim.json"
])

comparison.plot_participation_balance()
comparison.plot_solution_quality()
comparison.generate_comparison_report("leadership_comparison.html")
```

### Data Visualization

Use our visualization tools to create insightful charts:

```python
from src.visualization import SimulationVisualizer

viz = SimulationVisualizer("data/results/your_simulation_name.json")

# Participation distribution
viz.plot_participation_distribution()

# Communication network
viz.plot_communication_network()

# Task completion timeline
viz.plot_task_timeline()

# Team member influence
viz.plot_member_influence()
```

## Tips for Effective Analysis

1. **Start with questions**: Begin with clear research questions to focus your analysis
2. **Look beyond averages**: Examine individual interactions and specific moments
3. **Triangulate data**: Use multiple metrics to validate your findings
4. **Consider context**: Account for the type of task and team composition
5. **Compare configurations**: Analysis is most insightful when comparing different setups
6. **Look for patterns**: Identify recurring behaviors or interaction patterns
7. **Visualize data**: Create charts and network graphs to reveal hidden insights

## Common Analysis Pitfalls

- **Confirmation bias**: Looking only for evidence that supports your hypothesis
- **Over-generalization**: Drawing broad conclusions from limited simulations
- **Mistaking correlation for causation**: Assuming relationships are causal
- **Ignoring confounding factors**: Not accounting for other variables
- **Cherry-picking data**: Selecting only favorable results

## Creating Your Analysis Report

A complete analysis report should include:

1. **Research question/hypothesis**: What were you investigating?
2. **Simulation setup**: Configurations and parameters used
3. **Methods**: How you analyzed the data
4. **Findings**: Key observations and patterns
5. **Discussion**: Interpretation and connections to theory
6. **Limitations**: Constraints and potential biases
7. **Conclusions**: Main takeaways and implications

## Using Excel or Google Sheets

For basic analysis using spreadsheets:

1. Export your data to CSV using:
   ```python
   from src.analysis import export_to_csv
   export_to_csv("data/results/your_simulation_name.json", "my_analysis.csv")
   ```

2. Import the CSV into Excel or Google Sheets
3. Use pivot tables to analyze participation and contributions
4. Create charts to visualize key metrics

## Using Python Libraries

For advanced analysis, consider using these Python libraries:

- **Pandas**: Data manipulation and analysis
- **NLTK or spaCy**: Natural language processing
- **NetworkX**: Network analysis of team interactions
- **Matplotlib or Seaborn**: Data visualization
- **Scikit-learn**: Machine learning for pattern identification

## Need Help?

If you need assistance with your analysis:

1. Check the example notebooks in the `examples/analysis` folder
2. Refer to the API documentation for our analysis modules
3. Use the GitHub discussions forum for questions
4. Attend office hours for personalized guidance 