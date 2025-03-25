"""
Check-in 2: Basic Team Simulation Script

This script provides a simplified implementation of a team simulation using CrewAI.
It creates a small team with different roles and personalities working on a basic task.
You can use this as a starting point for your own team simulation experiments.

Prerequisites:
- OpenAI API key (set as OPENAI_API_KEY environment variable or in .env file)
- Installed the required packages (pip install -r requirements.txt)
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables (for OpenAI API key)
load_dotenv()

class BasicTeamSimulation:
    """
    A simplified team simulation using CrewAI.
    
    This class creates a team of agents with different roles and personalities,
    assigns them tasks, and runs a simulation of their interaction.
    """
    
    def __init__(self, simulation_name, model="gpt-4o-mini"):
        """
        Initialize the simulation.
        
        Args:
            simulation_name: Name of the simulation (used for saving results)
            model: The LLM model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.simulation_name = simulation_name
        self.model = model
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
            llm=self.model
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
        
        # Create the agent
        agent = Agent(
            role=role,
            goal=f"Contribute your expertise in {expertise} to help the team succeed",
            backstory=f"""You are {name}, with expertise in {expertise}.
            {personality_desc}You work well with others while maintaining your unique perspective.
            You want the team to succeed and are eager to share your knowledge.""",
            verbose=True,
            llm=self.model
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


def run_product_team_simulation(model="gpt-4o-mini"):
    """
    Run a simple simulation of a product team working on a new feature.
    
    Args:
        model: The LLM model to use
        
    Returns:
        The simulation results
    """
    # Create the simulation
    sim = BasicTeamSimulation("product_feature_team", model=model)
    
    # Create team members
    leader = sim.create_team_leader("Alex", leadership_style="democratic")
    designer = sim.create_team_member(
        "Taylor", 
        "Product Designer", 
        "UX/UI design",
        personality={"openness": 0.8, "extraversion": 0.7}
    )
    developer = sim.create_team_member(
        "Jordan", 
        "Software Developer", 
        "backend development",
        personality={"conscientiousness": 0.9, "extraversion": 0.4}
    )
    
    # Create tasks
    product_context = """
    Your team works at a software company building a mobile app for task management.
    Users have requested a new feature to categorize and prioritize tasks.
    The feature needs to be intuitive, visually appealing, and technically feasible.
    """
    
    sim.add_task(
        description="Lead the team in designing and implementing a new task categorization feature",
        assigned_to=leader,
        expected_output="A comprehensive plan for the feature implementation with team roles and timeline",
        context=product_context
    )
    
    sim.add_task(
        description="Create a user-friendly design for the task categorization feature",
        assigned_to=designer,
        expected_output="A design proposal including UI mockups and user flow diagrams",
        context=product_context
    )
    
    sim.add_task(
        description="Evaluate technical feasibility and implementation approach",
        assigned_to=developer,
        expected_output="Technical specifications and implementation plan for the feature",
        context=product_context
    )
    
    # Run the simulation
    results = sim.run_simulation(process_type="hierarchical")
    
    # Save and return results
    sim.save_results()
    return results


if __name__ == "__main__":
    print("Starting team simulation...")
    results = run_product_team_simulation()
    print("Simulation complete!") 