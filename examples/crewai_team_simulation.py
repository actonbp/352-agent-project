"""
CrewAI Team Simulation Example

This example demonstrates how to use CrewAI to simulate a team working on a project.
It shows:
1. How to create agents with different roles, backgrounds, and personalities
2. How to define tasks for the team to accomplish
3. How to orchestrate team interactions and processes
4. How to analyze team performance and dynamics

Prerequisites:
- OpenAI API key (set as OPENAI_API_KEY environment variable)
"""

import os
from datetime import datetime
import json
from typing import List, Dict
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables (for API keys)
load_dotenv()

class TeamSimulationCrewAI:
    """Team simulation using CrewAI framework."""
    
    def __init__(self, simulation_name: str):
        self.simulation_name = simulation_name
        self.start_time = None
        self.end_time = None
        self.agents = []
        self.tasks = []
        self.crew = None
        self.results = {}
        self.interaction_log = []
        
    def create_team_leader(self, name: str, personality_traits: Dict[str, float] = None):
        """Create a team leader agent."""
        personality_desc = self._personality_to_text(personality_traits)
        
        leader = Agent(
            role="Team Leader",
            goal=f"Lead the team effectively to accomplish goals while maintaining team cohesion",
            backstory=f"""You are {name}, an experienced team leader with strong organizational skills.
            {personality_desc}
            You value both results and team harmony. You are responsible for delegating tasks,
            monitoring progress, and ensuring the project stays on track.""",
            verbose=True,
            allow_delegation=True
        )
        
        self.agents.append({"role": "Team Leader", "name": name, "agent": leader, "personality": personality_traits})
        return leader
    
    def create_team_member(self, name: str, role: str, expertise: str, personality_traits: Dict[str, float] = None):
        """Create a team member agent with specific expertise."""
        personality_desc = self._personality_to_text(personality_traits)
        
        member = Agent(
            role=role,
            goal=f"Contribute your expertise in {expertise} to help the team succeed",
            backstory=f"""You are {name}, a team member with expertise in {expertise}.
            {personality_desc}
            You work well with others but also have your own perspective and ideas.
            You want the team to succeed and are willing to share your knowledge.""",
            verbose=True
        )
        
        self.agents.append({"role": role, "name": name, "agent": member, "personality": personality_traits})
        return member
    
    def create_deviant_member(self, name: str, role: str, expertise: str):
        """Create a 'deviant' team member who challenges group thinking."""
        deviant = Agent(
            role=role,
            goal=f"Contribute your expertise while challenging conventional thinking",
            backstory=f"""You are {name}, a team member with expertise in {expertise}.
            You are known for challenging the status quo and questioning assumptions.
            You're not trying to be difficult, but you believe that the best ideas emerge
            from constructive conflict and diverse perspectives. You often play devil's
            advocate even when you might agree with the team.""",
            verbose=True
        )
        
        self.agents.append({"role": "Deviant " + role, "name": name, "agent": deviant, 
                           "personality": {"conformity": 0.2, "openness": 0.9, "agreeableness": 0.5}})
        return deviant
    
    def add_task(self, description: str, agent, context: str = None):
        """Add a task to the simulation."""
        task = Task(
            description=description,
            agent=agent,
            context=context if context else "",
            expected_output="A detailed report of your contributions, thought process, and interactions with the team."
        )
        
        self.tasks.append(task)
        return task
    
    def _personality_to_text(self, traits: Dict[str, float] = None) -> str:
        """Convert personality traits to descriptive text."""
        if not traits:
            return "You have a balanced personality with no extreme tendencies."
        
        descriptions = []
        if "openness" in traits:
            if traits["openness"] > 0.7:
                descriptions.append("You are very open to new ideas and experiences.")
            elif traits["openness"] < 0.3:
                descriptions.append("You prefer traditional, familiar approaches.")
                
        if "conscientiousness" in traits:
            if traits["conscientiousness"] > 0.7:
                descriptions.append("You are highly organized and detail-oriented.")
            elif traits["conscientiousness"] < 0.3:
                descriptions.append("You tend to be flexible and spontaneous rather than organized.")
                
        if "extraversion" in traits:
            if traits["extraversion"] > 0.7:
                descriptions.append("You are outgoing and energized by social interaction.")
            elif traits["extraversion"] < 0.3:
                descriptions.append("You are more reserved and prefer thinking before speaking.")
                
        if "agreeableness" in traits:
            if traits["agreeableness"] > 0.7:
                descriptions.append("You prioritize team harmony and are cooperative.")
            elif traits["agreeableness"] < 0.3:
                descriptions.append("You're not afraid of disagreement and can be competitive.")
                
        if "neuroticism" in traits:
            if traits["neuroticism"] > 0.7:
                descriptions.append("You tend to worry about things going wrong.")
            elif traits["neuroticism"] < 0.3:
                descriptions.append("You are emotionally stable and rarely get stressed.")
                
        return " ".join(descriptions)
    
    def run_simulation(self, process_type: str = "sequential"):
        """Run the team simulation."""
        self.start_time = datetime.now()
        
        # Choose the process type for the crew
        if process_type.lower() == "sequential":
            process = Process.sequential
        else:
            process = Process.hierarchical
            
        # Create the crew with the agents and tasks
        self.crew = Crew(
            agents=list(agent_data["agent"] for agent_data in self.agents),
            tasks=self.tasks,
            verbose=2,  # Detailed output
            process=process
        )
        
        # Run the crew simulation
        results = self.crew.kickoff()
        
        self.end_time = datetime.now()
        self.results = results
        
        # Process and structure the results
        return self._process_results(results)
    
    def _process_results(self, results):
        """Process the raw results from the simulation."""
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Structure the metrics
        metrics = {
            "simulation_name": self.simulation_name,
            "duration_seconds": duration,
            "number_of_agents": len(self.agents),
            "number_of_tasks": len(self.tasks),
            "agent_composition": [
                {
                    "name": agent_data["name"],
                    "role": agent_data["role"],
                    "personality": agent_data["personality"]
                } for agent_data in self.agents
            ],
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def save_results(self, directory: str = "../data"):
        """Save the simulation results to a file."""
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        filename = f"{directory}/{self.simulation_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        return filename


def main():
    """Run a demo team simulation using CrewAI."""
    
    # Create the simulation
    sim = TeamSimulationCrewAI("project_planning_team")
    
    # Create team members with different personalities and roles
    leader = sim.create_team_leader("Morgan", {
        "openness": 0.7,
        "conscientiousness": 0.8,
        "extraversion": 0.7,
        "agreeableness": 0.6,
        "neuroticism": 0.3
    })
    
    tech_expert = sim.create_team_member("Taylor", "Technical Expert", "software development", {
        "openness": 0.8,
        "conscientiousness": 0.7,
        "extraversion": 0.4,
        "agreeableness": 0.5,
        "neuroticism": 0.4
    })
    
    creative = sim.create_team_member("Jordan", "Creative Designer", "user experience design", {
        "openness": 0.9,
        "conscientiousness": 0.5,
        "extraversion": 0.6,
        "agreeableness": 0.7,
        "neuroticism": 0.5
    })
    
    analyzer = sim.create_team_member("Casey", "Data Analyst", "data analysis and research", {
        "openness": 0.6,
        "conscientiousness": 0.9,
        "extraversion": 0.3,
        "agreeableness": 0.6,
        "neuroticism": 0.4
    })
    
    # Add a "deviant" team member to challenge conventional thinking
    deviant = sim.create_deviant_member("Alex", "Strategic Thinker", "business strategy")
    
    # Create tasks for the team
    sim.add_task(
        "Develop a project plan for creating a new mobile app that helps college students track their study habits.",
        leader,
        "You need to coordinate with all team members to create a comprehensive project plan."
    )
    
    sim.add_task(
        "Propose the technical architecture for the study habit tracking app.",
        tech_expert,
        "Consider key features like tracking study time, setting goals, and providing analytics."
    )
    
    sim.add_task(
        "Design the user interface and experience for the app.",
        creative,
        "The app should be engaging and intuitive for college students."
    )
    
    sim.add_task(
        "Research similar apps and identify market opportunities.",
        analyzer,
        "Analyze competitor apps and identify gaps or opportunities for our app."
    )
    
    sim.add_task(
        "Challenge the team's assumptions about the project direction.",
        deviant,
        "Question key assumptions the team is making and offer alternative perspectives."
    )
    
    # Run the simulation
    print(f"Starting team simulation: {sim.simulation_name}")
    results = sim.run_simulation(process_type="hierarchical")
    
    # Save the results
    filepath = sim.save_results()
    print(f"Simulation results saved to: {filepath}")
    
    # Print summary
    print("\nSimulation Summary:")
    print(f"Duration: {results['duration_seconds']:.2f} seconds")
    print(f"Number of agents: {results['number_of_agents']}")
    print(f"Number of tasks: {results['number_of_tasks']}")

if __name__ == "__main__":
    main() 