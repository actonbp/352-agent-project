# Guide for AI Assistants

This document provides guidance specifically for AI assistants working on the LEAD 352 Team Simulation Project. It complements the [DEVELOPMENT.md](DEVELOPMENT.md) guide with AI-specific information.

## 🧠 Project Context

This project is an educational tool for the LEAD 352 course at Berkeley Haas, focusing on teams and interpersonal dynamics. Students use agent-based simulations to explore concepts like:

- Leadership styles and their impacts on team performance
- Diversity and inclusion in team settings
- Communication patterns and team structures
- Conflict resolution and decision-making processes

The target audience is undergraduate students with varying levels of technical expertise.

## 📋 When Working on This Project

### Key Priorities

1. **Educational Value**: Prioritize creating clear, educational content that helps students understand team dynamics concepts
2. **Usability**: Ensure all code and documentation is accessible to students with limited coding experience
3. **Documentation**: Maintain both student-facing and developer documentation with every change

### Repository Navigation

- **Student materials** are in the `docs/` directory and served via GitHub Pages
- **Core simulation code** is in the `src/` directory
- **Example simulations** are in the `examples/` directory
- **Developer guides** are in the repository root (README.md, DEVELOPMENT.md, this file)

### Documentation Separation

Maintain clear separation between:

1. **Student-facing documentation** (in `docs/`):
   - Written in accessible language
   - Focused on using the simulations
   - Contains assignment instructions
   - Avoids implementation details

2. **Developer documentation** (root directory):
   - Technical implementation details
   - Code architecture explanations
   - Future development plans
   - Contribution guidelines

## 💻 Common Tasks and Approaches

### Adding a New Simulation Type

1. Create a new Python module in `src/` (e.g., `src/conflict_resolution_simulation.py`)
2. Create a student-facing guide in `docs/` (e.g., `docs/conflict_resolution_guide.md`)
3. Add example usage in `examples/`
4. Update both README.md and the docs index.md to reference the new simulation
5. Document technical details in DEVELOPMENT.md

### Updating an Existing Simulation

1. Make changes to the module in `src/`
2. Update the corresponding student guide in `docs/`
3. Update any examples in `examples/` to showcase new features
4. If it's a breaking change, document in DEVELOPMENT.md

### Adding Analysis Tools

1. Add the analysis functionality to `src/analysis.py` or create a new module
2. Create or update student documentation in `docs/analyzing_results_guide.md`
3. Add example usage in `examples/analysis/`

## 🛠️ Working with CrewAI

This project uses CrewAI as the underlying framework for simulations. Key concepts:

- **Agents**: Represent team members with specific roles, goals, and personality traits
- **Tasks**: Define work to be done, with descriptions and expected outputs
- **Crew**: Groups agents together and orchestrates their interactions
- **Process**: Defines how tasks are executed (sequential or hierarchical)

When updating CrewAI-related code:

1. Check compatibility with the current CrewAI version
2. Test with multiple OpenAI models (especially gpt-4o-mini for cost-efficiency)
3. Include proper error handling for API limits and token constraints
4. Document model requirements and limitations

## 📊 Current Implementation Status

### Complete and Ready
- Leadership style simulation framework
- Diversity & inclusion simulation framework
- Basic simulation analysis tools
- Student documentation for core features

### In Development
- Google Colab integration
- Enhanced visualization tools
- Advanced text analysis of team interactions
- Azure OpenAI support

### Planned for Future
- Conflict resolution simulation
- Cross-cultural dynamics simulation
- Time pressure effects modeling
- Interactive results dashboard

## 🤝 Collaboration with Human Developers

When a human developer will continue your work:

1. Clearly summarize what you've done and the current state
2. Highlight any pending issues or decisions
3. Suggest next steps with clear rationales
4. Document any assumptions you've made

## 📝 Code Style Guidelines

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add type hints for better code understanding
- Include docstrings for all functions and classes
- Comment complex logic or algorithms
- Keep functions focused and reasonably sized

## 🚀 Future Direction

The project aims to:

1. Expand the range of team dynamics that can be simulated
2. Improve the realism and nuance of agent interactions
3. Enhance analysis tools to extract meaningful insights
4. Make simulations more accessible to students with limited technical backgrounds
5. Create ready-to-use Google Colab notebooks for zero-setup usage

## 📚 Helpful Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [LEAD 352 Course Description](https://haas.berkeley.edu/undergrad/academics/curriculum/course-descriptions/)
- [Team Dynamics Academic Research](https://scholar.google.com/scholar?q=team+dynamics+organizational+behavior) 