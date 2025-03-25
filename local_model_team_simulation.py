"""
Local Model Team Simulation Tutorial

This script provides a simplified implementation of a team simulation using CrewAI
with support for both OpenAI API models and local models via Ollama.

Prerequisites:
- For API models: OpenAI API key (set as OPENAI_API_KEY environment variable or in .env file)
- For local models: Ollama installed with models downloaded (https://ollama.com/)
- Required packages: pip install -r requirements.txt

TUTORIAL: This is a step-by-step guide to running team simulations with local LLMs
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Import Ollama integration for local models
from langchain_community.llms import Ollama
# For OpenAI models we'll use CrewAI's built-in support

# Load environment variables (only needed for OpenAI API)
load_dotenv()

class LocalTeamSimulation:
    """
    A team simulation that can use local LLMs via Ollama.
    
    This class creates a team of agents with different roles and personalities,
    assigns them tasks, and runs a simulation of their interaction.
    """
    
    def __init__(self, 
                 simulation_name, 
                 model_type="local",  # "local" or "api"
                 model_name="llama3",  # local model name or API model name
                 temperature=0.7):
        """
        Initialize the simulation with support for local models.
        
        Args:
            simulation_name: Name of the simulation (used for saving results)
            model_type: Either "local" (for Ollama) or "api" (for OpenAI)
            model_name: 
                - If local: model name in Ollama (e.g., "llama3", "mistral")
                - If API: OpenAI model (e.g., "gpt-4o-mini", "gpt-3.5-turbo")
            temperature: Controls randomness of outputs (0.0-1.0)
        """
        self.simulation_name = simulation_name
        self.model_type = model_type
        self.model_name = model_name
        self.temperature = temperature
        
        # Set up the appropriate LLM based on model_type
        if model_type == "local":
            # Use Ollama for local models
            print(f"Using local Ollama model: {model_name}")
            self.llm = Ollama(model=model_name, temperature=temperature)
        else:
            # Use OpenAI API models
            print(f"Using API model: {model_name}")
            self.llm = model_name  # CrewAI handles API models directly
        
        # Initialize other attributes
        self.agents = []
        self.tasks = []
        self.crew = None
        self.results = None
        self.start_time = None
        self.end_time = None
    
    def create_team_leader(self, name, leadership_style="democratic"):
        """
        Create a team leader with a specific leadership style.
        
        Args:
            name: The name of the leader
            leadership_style: The leadership style (democratic, authoritarian, etc.)
        
        Returns:
            The created leader agent
        """
        # Create backstory based on leadership style
        if leadership_style == "democratic":
            backstory = f"""You are {name}, a democratic team leader who values input from all team members.
            You believe in collaborative decision-making and ensuring everyone's voice is heard.
            You provide guidance but allow team members to contribute their expertise.
            When facilitating discussions, you make sure everyone participates and feels valued."""
        elif leadership_style == "authoritarian":
            backstory = f"""You are {name}, an authoritarian team leader who provides clear direction.
            You believe in structured processes and clear chains of command.
            You make decisions efficiently and expect team members to follow your guidance.
            You value results and keeping the team on track above all else."""
        else:  # Default to balanced approach
            backstory = f"""You are {name}, a balanced team leader who adapts their style to the situation.
            You know when to be directive and when to be collaborative.
            You value both results and team cohesion, adjusting your approach as needed."""
        
        leader = Agent(
            role="Team Leader",
            goal="Lead the team effectively to accomplish the project goals",
            backstory=backstory,
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        self.agents.append({
            "name": name,
            "role": "Team Leader",
            "leadership_style": leadership_style,
            "agent": leader
        })
        
        return leader
    
    def create_team_member(self, name, role, expertise, personality=None):
        """
        Create a team member with specific expertise and personality.
        
        Args:
            name: The name of the team member
            role: Their role in the team (e.g., "Designer", "Developer")
            expertise: Their area of expertise
            personality: Optional dict of personality traits
        
        Returns:
            The created team member agent
        """
        # Create a personality description if provided
        personality_desc = ""
        if personality:
            traits = []
            if personality.get("extraversion", 0.5) > 0.7:
                traits.append("outgoing and energetic")
            elif personality.get("extraversion", 0.5) < 0.3:
                traits.append("reserved and thoughtful")
                
            if personality.get("openness", 0.5) > 0.7:
                traits.append("creative and open to new ideas")
            elif personality.get("openness", 0.5) < 0.3:
                traits.append("practical and focused on proven approaches")
                
            if personality.get("conscientiousness", 0.5) > 0.7:
                traits.append("organized and detail-oriented")
            elif personality.get("conscientiousness", 0.5) < 0.3:
                traits.append("flexible and adaptable")
                
            if traits:
                personality_desc = f"You tend to be {', '.join(traits)}. "
        
        # Create the agent with the configured LLM
        agent = Agent(
            role=role,
            goal=f"Contribute your expertise in {expertise} to help the team succeed",
            backstory=f"""You are {name}, with expertise in {expertise}.
            {personality_desc}You work well with others while maintaining your unique perspective.
            You want the team to succeed and are eager to share your knowledge.""",
            verbose=True,
            llm=self.llm
        )
        
        self.agents.append({
            "name": name,
            "role": role,
            "expertise": expertise,
            "personality": personality,
            "agent": agent
        })
        
        return agent
    
    def add_task(self, description, assigned_to, expected_output, context=""):
        """
        Add a task to the simulation.
        
        Args:
            description: Description of the task
            assigned_to: The agent responsible for the task
            expected_output: What should be produced
            context: Additional context for the task
        
        Returns:
            The created task
        """
        task = Task(
            description=description,
            agent=assigned_to,
            expected_output=expected_output,
            context=context
        )
        
        self.tasks.append(task)
        return task
    
    def run_simulation(self, process_type="hierarchical"):
        """
        Run the team simulation with the configured agents and tasks.
        
        Args:
            process_type: How agents work together ("hierarchical" or "sequential")
        
        Returns:
            The processed results of the simulation
        """
        self.start_time = datetime.now()
        
        # Set up the process type
        if process_type.lower() == "sequential":
            process = Process.sequential
        else:
            process = Process.hierarchical
        
        # Create and run the crew
        self.crew = Crew(
            agents=[agent_data["agent"] for agent_data in self.agents],
            tasks=self.tasks,
            verbose=2,  # Detailed output
            process=process
        )
        
        # Run the simulation
        print(f"Starting simulation with {len(self.agents)} agents and {len(self.tasks)} tasks...")
        results = self.crew.kickoff()
        self.results = results
        self.end_time = datetime.now()
        
        # Process and return the results
        return self.process_results(results)
    
    def process_results(self, results):
        """
        Process the raw results from the simulation.
        
        Args:
            results: The raw results from crew.kickoff()
        
        Returns:
            A structured dictionary of simulation results
        """
        # Calculate duration
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Structure the results
        processed_results = {
            "simulation_name": self.simulation_name,
            "model_info": {
                "type": self.model_type,
                "name": self.model_name,
                "temperature": self.temperature
            },
            "duration_seconds": duration,
            "team_composition": [
                {
                    "name": agent_data["name"],
                    "role": agent_data["role"],
                    **({"leadership_style": agent_data["leadership_style"]} if "leadership_style" in agent_data else {}),
                    **({"expertise": agent_data["expertise"]} if "expertise" in agent_data else {}),
                    **({"personality": agent_data["personality"]} if "personality" in agent_data else {})
                } for agent_data in self.agents
            ],
            "tasks": [task.description for task in self.tasks],
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        return processed_results
    
    def save_results(self, directory="data"):
        """
        Save the simulation results to a JSON file.
        
        Args:
            directory: Directory to save the results file
        
        Returns:
            The path to the saved file
        """
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create a filename with timestamp
        filename = f"{directory}/{self.simulation_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Save results as JSON
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"Results saved to {filename}")
        return filename


# ===== TUTORIAL EXAMPLE =====

def tutorial_example():
    """
    Run a simple team simulation that demonstrates local model usage.
    
    This function shows how to set up a basic simulation using
    either local models via Ollama or API models.
    """
    print("=" * 50)
    print("TEAM SIMULATION TUTORIAL")
    print("=" * 50)
    
    # Ask user which model they want to use
    use_local = input("\nUse local model via Ollama? (y/n): ").lower() == 'y'
    
    if use_local:
        # Show available models in Ollama
        import subprocess
        try:
            print("\nChecking available models in Ollama...")
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            print(result.stdout)
            
            model_name = input("Enter model name to use (default: llama3): ") or "llama3"
            
            # Create simulation with local model
            sim = LocalTeamSimulation(
                simulation_name="tutorial_team",
                model_type="local",
                model_name=model_name,
                temperature=0.8  # Higher temperature for more creative outputs
            )
        except:
            print("Error running Ollama. Is it installed? Try: https://ollama.com/")
            print("Falling back to API model...")
            use_local = False
    
    if not use_local:
        # Check if API key is available
        if not os.getenv("OPENAI_API_KEY"):
            print("\nWarning: No OpenAI API key found in environment variables.")
            print("You can set it by creating a .env file with OPENAI_API_KEY=your-key")
        
        model_name = input("\nEnter OpenAI model to use (default: gpt-3.5-turbo): ") or "gpt-3.5-turbo"
        
        # Create simulation with API model
        sim = LocalTeamSimulation(
            simulation_name="tutorial_team",
            model_type="api",
            model_name=model_name,
            temperature=0.7
        )
    
    print("\nCreating team members...")
    
    # Create a simple team (smaller than the previous example to run faster)
    leader = sim.create_team_leader("Alex", leadership_style="democratic")
    
    # Create just one team member for simplicity and faster results
    engineer = sim.create_team_member(
        "Jordan", 
        "Software Developer", 
        "app development",
        personality={"conscientiousness": 0.8, "openness": 0.6}
    )
    
    # Create a simple task context
    print("\nSetting up task context...")
    task_context = """
    You're working on a simple mobile app that helps users track their daily water intake.
    The app needs to be user-friendly and send helpful reminders.
    This is a quick brainstorming session to outline the key features.
    """
    
    # Create a single task for faster execution
    print("\nCreating tasks...")
    sim.add_task(
        description="Brainstorm the core features for a water tracking app",
        assigned_to=leader,
        expected_output="A short list of 3-5 key features for the water tracking app",
        context=task_context
    )
    
    # Add a task for the engineer
    sim.add_task(
        description="Suggest the technical implementation approach for the app",
        assigned_to=engineer,
        expected_output="A brief technical approach with recommended technologies",
        context=task_context
    )
    
    # Run the simulation
    print("\nRunning simulation... (this may take a few minutes)")
    print("Local models may be slower but don't incur API costs.")
    results = sim.run_simulation(process_type="sequential")
    
    # Save and return results
    print("\nSimulation complete!")
    sim.save_results()
    
    # Print a summary
    print("\n" + "=" * 50)
    print("SIMULATION SUMMARY")
    print("=" * 50)
    
    # Simplified results output
    for task_num, result in enumerate(results):
        print(f"\nTask {task_num+1} Output:")
        print("-" * 30)
        print(result)
        print("-" * 30)
    
    print("\nFull results have been saved to the data directory.")
    print("You can modify this script to create more complex simulations!")


if __name__ == "__main__":
    tutorial_example() 