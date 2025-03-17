# Leadership 352: Team Simulation Project

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.28.1-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

An advanced team dynamics simulation framework using CrewAI to model leadership styles, team diversity, and organizational behavior. This project allows students to explore team dynamics through AI-powered simulations.

## Project Overview

This project provides a framework for creating AI agent-based simulations of team dynamics, leadership styles, and organizational behavior. Students can use these simulations to test hypotheses about team performance and collect rich data on team interactions.

### Key Features

- **Leadership Style Simulations**: Compare authoritarian, democratic, laissez-faire, and transformational leadership approaches
- **Diversity & Inclusion Models**: Explore how team diversity and inclusion practices affect outcomes
- **Customizable Tasks**: Create scenarios for creative problem-solving, decision-making, and crisis management
- **Results Analysis**: Tools for analyzing team interactions, communication patterns, and performance metrics
- **Reproducible Research**: Framework for collecting and comparing data across simulation runs

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for CrewAI examples)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/actonbp/352-agent-project.git
   cd 352-agent-project
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. For CrewAI examples, create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Simulation Modules

### Leadership Style Simulation

The `src/leadership_style_simulation.py` module allows you to compare how different leadership styles affect team performance and dynamics. It supports:

- Authoritarian leadership
- Democratic leadership
- Laissez-faire leadership
- Transformational leadership

### Diversity and Inclusion Simulation

Located in `src/diversity_inclusion_simulation.py`, this module explores how team diversity and inclusion practices impact team dynamics and outcomes on various tasks.

### Example Usage

```python
from src.leadership_style_simulation import run_leadership_comparison

# Compare all leadership styles on a creative task
results = run_leadership_comparison(task_type="creative", model="gpt-4o-mini")
```

## Documentation

Detailed documentation is available in the project files:

- `src/team_simulation_guide.md`: Comprehensive guide to using the simulation modules
- `examples/crewai_setup_guide.md`: Guide for setting up CrewAI
- `check_in_1_worksheet.docx`: Template for designing your team simulation
- `check_in_1_summary_template.docx`: Template for summarizing your simulation design

## Example Research Questions

These simulations can help explore questions such as:

- How do different leadership styles affect team creativity and innovation?
- Which leadership approach is most effective during crisis situations?
- How does team diversity impact problem-solving capability?
- What are the effects of inclusive practices on team satisfaction and engagement?
- How do team structures influence communication patterns and decision quality?

## Project Structure

```
project/
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── src/                            # Source code for simulations
│   ├── simulation_template.py      # Base template for creating simulations
│   ├── leadership_style_simulation.py # Leadership style comparison simulation
│   ├── diversity_inclusion_simulation.py # Diversity and inclusion simulation
│   └── team_simulation_guide.md    # Comprehensive guide to using simulations
├── examples/                       # Example simulations and guides
│   ├── basic_simulation.py         # Simple team simulation example
│   ├── crewai_team_simulation.py   # CrewAI-based team simulation
│   ├── analyze_simulation_results.py # Tools for analyzing simulation data
│   ├── crewai_setup_guide.md       # Guide for setting up CrewAI
│   └── .env.example                # Example environment variables file
└── data/                           # Directory for storing simulation results
```

## License

This project is provided for educational purposes for students in Leadership 352 at Binghamton University.

## Acknowledgments

This project uses the CrewAI framework for orchestrating role-playing autonomous AI agents, built on top of LangChain and other open-source libraries.

## Contributing

While this is an educational project, we welcome suggestions and contributions to improve the simulation framework. Please feel free to open issues or submit pull requests. 