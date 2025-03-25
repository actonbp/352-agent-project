# Running Team Simulations with Local LLMs Tutorial

This tutorial walks you through running team simulations using locally hosted large language models (LLMs) via Ollama, eliminating the need for API keys or usage costs.

## Benefits of Local Models

- **No API costs**: Run as many simulations as you want without paying for API usage
- **Privacy**: All data stays on your computer
- **Control**: Choose from various open-source models with different capabilities
- **Speed**: No network latency (though inference may be slower depending on your hardware)

## Prerequisites

1. **Python environment** with required packages:
   ```
   pip install crewai langchain-community python-dotenv
   ```

2. **Ollama installed** on your computer:
   - Download from [https://ollama.com/](https://ollama.com/)
   - Available for Mac, Windows, and Linux

3. **At least one model downloaded** through Ollama:
   ```
   ollama pull llama3
   ```
   (Other good options: mistral, llama3:8b, phi, etc.)

## Quick Start

1. **Run the tutorial script**:
   ```
   python local_model_team_simulation.py
   ```

2. **Choose local model** when prompted and select which model to use

3. **Watch the simulation run** with a smaller team and simplified tasks

## How It Works

The `local_model_team_simulation.py` script demonstrates:

1. **Local model integration**: Using Ollama with CrewAI via LangChain
2. **Team creation**: Setting up agents with different roles and personalities 
3. **Task definition**: Creating tasks for the team to accomplish
4. **Result processing**: Capturing and saving simulation outputs

## Customizing for Your Project

### Using Different Models

```python
# Try different local models
sim = LocalTeamSimulation(
    simulation_name="custom_simulation",
    model_type="local",
    model_name="mistral",  # or "phi", "llama3:8b", etc.
    temperature=0.7
)

# Or use API models when needed
sim = LocalTeamSimulation(
    simulation_name="custom_simulation",
    model_type="api",
    model_name="gpt-4o-mini",
    temperature=0.7
)
```

### Adjusting Model Parameters

For local models, you can adjust parameters like temperature:

```python
# More creative outputs (higher temperature)
self.llm = Ollama(model=model_name, temperature=0.9)

# More consistent outputs (lower temperature)
self.llm = Ollama(model=model_name, temperature=0.2)
```

### Creating Larger Teams

```python
# Create more diverse teams
leader = sim.create_team_leader("Alex", leadership_style="democratic")
engineer = sim.create_team_member("Jordan", "Developer", "backend")
designer = sim.create_team_member("Taylor", "Designer", "UI/UX")
marketer = sim.create_team_member("Casey", "Marketer", "growth")
# Add as many members as needed
```

## Recommendations for Better Results

1. **Use task-specific prompts**: Be very specific in task descriptions
2. **Keep team size small** when using local models (2-3 agents work well)
3. **Break complex projects into smaller tasks**
4. **Try different models** to find which works best for your simulation
5. **Use sequential process** for simpler coordination between agents
6. **More powerful hardware** will run larger models more efficiently

## Troubleshooting

- **Slow performance**: Try a smaller model like "phi" or "gemma:2b"
- **Out of memory errors**: Reduce model size or close other applications
- **Poor quality outputs**: Improve prompts or try a more capable model

## Next Steps

After getting familiar with the basic simulation:

1. **Create your own scenario**: Define a new team and project
2. **Experiment with leadership styles**: Try different approaches
3. **Compare different models**: See how outputs differ between models
4. **Analyze the simulation results**: Review team dynamics and outputs

Remember, local models may not be as capable as the latest API models, but they provide a free way to experiment with team simulations, making them perfect for educational purposes and prototyping.

## Resources

- [Ollama Models List](https://ollama.com/library)
- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction) 