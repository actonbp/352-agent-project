# LEAD 352 Team Simulation Project

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Active-brightgreen)](https://actonbp.github.io/352-agent-project/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.14.0-orange.svg)](https://crewai.io)

This repository contains the code and documentation for the LEAD 352 Team Simulation Project, designed to help students explore team dynamics through agent-based simulations.

## 👩‍🎓 For Students

All student materials are available on our GitHub Pages website:

**[Visit the Project Website](https://actonbp.github.io/352-agent-project/)**

There, you'll find:
- Comprehensive guides for setting up and running simulations
- Instructions for course assignments
- Analysis tools and examples
- FAQs and troubleshooting help

No GitHub knowledge is required to access these materials.

## 👨‍💻 For Developers

If you're a developer or AI assistant working on this project, please refer to these resources:

- [Development Guide](DEVELOPMENT.md) - Overview of project structure and guidelines
- [Contribution Guidelines](DEVELOPMENT.md#contribution-guidelines) - How to contribute to the project
- [Technical Implementation](DEVELOPMENT.md#technical-implementation-notes) - Details on the technical implementation

### Project Structure

```
team_simulation_project/
├── data/                 # Simulation data storage
├── docs/                 # Student-facing documentation (GitHub Pages)
├── examples/             # Example simulations
├── src/                  # Core simulation modules
└── tests/                # Test suite
```

### Quick Start for Development

1. Clone the repository:
   ```bash
   git clone https://github.com/actonbp/352-agent-project.git
   cd 352-agent-project
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

5. Run tests:
   ```bash
   pytest
   ```

## 🤖 For AI Assistants

If you're an AI assistant working on this codebase:

1. Review the [Development Guide](DEVELOPMENT.md) for project structure and guidelines
2. Understand the [student-facing documentation](https://actonbp.github.io/352-agent-project/) to maintain consistency
3. Follow the [Guidelines for AI Assistants](DEVELOPMENT.md#guidelines-for-ai-assistants)
4. Read the specific [AI Assistant Guide](claude.md) for detailed guidance

Key focus areas:
- Maintain clear separation between student-facing content (`docs/`) and development materials
- Ensure code is well-documented and approachable for students with limited programming experience
- Update both developer and student documentation when adding features

## 🚀 Current Development Focus

- Enhancing simulation realism for team dynamics
- Developing better analysis tools for simulation results
- Creating Google Colab notebooks for easier student access
- Adding support for additional language models

## 📝 Upcoming Features

See the [Development Guide](DEVELOPMENT.md#upcoming-features) for information on planned features.

## 📊 Simulation Modules

The project currently includes these simulation modules:

- **Leadership Simulation**: Explore how different leadership styles affect team dynamics
- **Diversity & Inclusion Simulation**: Investigate how team diversity impacts outcomes
- **Custom Team Simulation**: Create custom team compositions and interactions

## 📄 License

This project is licensed for educational use within LEAD 352 at Berkeley Haas. 