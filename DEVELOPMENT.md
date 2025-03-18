# Development Guide for Team Simulation Project

This document provides an overview of the project structure, development guidelines, and future plans for AI assistants and developers working on the LEAD 352 Team Simulation Project.

## 📂 Repository Structure

The repository is organized as follows:

```
team_simulation_project/
├── data/                 # Data storage for simulations
│   ├── results/          # Simulation results saved here
│   └── samples/          # Sample datasets
├── docs/                 # Student-facing documentation (GitHub Pages)
│   ├── templates/        # Assignment templates
│   └── images/           # Documentation images
├── examples/             # Example simulations for students
│   └── analysis/         # Example analysis scripts
├── src/                  # Core simulation modules
│   ├── leadership_simulation.py     # Leadership styles simulation
│   ├── diversity_inclusion_simulation.py  # Diversity simulation
│   ├── team_simulation.py  # Generic team simulation framework
│   ├── analysis.py       # Analysis tools for simulation results
│   └── visualization.py  # Visualization tools
├── tests/                # Test suite
├── README.md             # Student-oriented project overview
└── DEVELOPMENT.md        # This file - for developers/AI assistants
```

## 🧩 Core Components

### 1. Simulation Modules

The project includes several simulation modules:

- **Leadership Simulation**: Models four leadership styles and their impact on team dynamics
- **Diversity & Inclusion Simulation**: Explores how team diversity and inclusion practices affect outcomes
- **Custom Team Simulation**: A flexible framework for creating custom team compositions and tasks

### 2. Analysis Tools

The `src/analysis.py` module provides tools for:

- Parsing simulation results
- Analyzing interaction patterns
- Measuring team performance
- Visualizing team dynamics

### 3. Documentation System

Student-facing documentation is served via GitHub Pages from the `docs/` directory, while developer documentation is maintained in markdown files at the repository root.

## 🔧 Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code
- Include docstrings for all functions, classes, and modules
- Use type hints where appropriate
- Keep functions focused on single responsibilities

### Adding New Features

When adding new features:

1. Create a new branch with a descriptive name
2. Develop and test the feature
3. Update relevant documentation (both developer and student-facing)
4. Submit a pull request with a detailed description

### Documentation Updates

- Student-facing documentation goes in the `docs/` directory
- Developer-focused documentation should be added to this file or other root-level markdown files
- Ensure code examples work and are up-to-date

## 🚀 Current Development Focus

The project is currently focused on:

1. **Enhancing Simulation Realism**: Improving the cognitive diversity modeling in team interactions
2. **Analysis Tools**: Developing better metrics and visualizations for team dynamics
3. **Google Colab Integration**: Creating ready-to-use notebooks for students without local setup
4. **Azure OpenAI Support**: Adding better support for Azure OpenAI endpoints

## 📝 Upcoming Features

Features planned for future development:

- **Conflict Resolution Simulation**: Model different approaches to team conflict
- **Cross-Cultural Team Simulation**: Explore cultural dynamics in global teams
- **Time Pressure Effects**: Model how deadline pressure affects team performance
- **Visualization Dashboard**: Interactive web dashboard for simulation results

## 💻 Technical Implementation Notes

### Agent Framework

The simulation uses CrewAI as the underlying agent framework:

- Agents are defined with roles, goals, and personality traits
- Tasks are defined with descriptions and expected outputs
- Communication happens via the CrewAI orchestration layer
- Results are captured and saved as JSON for further analysis

### Model Compatibility

We support various OpenAI models (see `docs/crewai_setup_guide.md` for details):
- GPT-4o and GPT-4o-mini are the primary recommended models
- o1-preview and o1-mini provide enhanced reasoning capabilities for complex simulations

## 🤖 Guidelines for AI Assistants

If you're an AI assistant helping with this project:

1. **Understand the Educational Context**: This is for an undergraduate course in organizational behavior and team dynamics.
2. **Favor Clarity Over Complexity**: Code should be readable and approachable for students with limited programming experience.
3. **Document Everything**: Any new feature should be documented both for developers and in student-facing guides.
4. **Maintain Separation of Concerns**: Keep student-facing materials separate from development materials.

## 🔄 Version Control Practices

- Main branch should always be in a working state
- Use descriptive commit messages
- Tag significant releases with version numbers
- Document breaking changes clearly

## 🤝 Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Review existing issues or create a new one describing your proposed change
2. Fork the repository and create a branch for your feature
3. Develop and test your changes
4. Update documentation as needed
5. Submit a pull request with a clear description of the changes

## 📚 Developer Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/) 