"""
Team Simulation Template

This template provides a starting point for building team simulations.
Students can customize the agent personalities, tasks, and evaluation metrics
to explore their specific research questions.

Usage:
1. Modify the agent creation section to adjust team composition
2. Customize tasks to match your research scenario
3. Add or modify evaluation metrics as needed
4. Run different scenarios and compare results
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables (for API keys)
load_dotenv()

class TeamSimulation:
    """Base class for team simulations."""
    
    def __init__(self, 
                 simulation_name: str, 
                 team_size: int = 5, 
                 include_deviant: bool = False,
                 model: str = "gpt-4o-mini"):
        """
        Initialize the simulation.
        
        Args:
            simulation_name: Name of the simulation for tracking purposes
            team_size: Number of team members (excluding any special roles)
            include_deviant: Whether to include a deviant/devil's advocate member
            model: The LLM model to use (e.g., "gpt-4o-mini", "gpt-4o", "gpt-4")
        """
        self.simulation_name = simulation_name
        self.team_size = team_size
        self.include_deviant = include_deviant
        self.model = model
        self.agents = []
        self.tasks = []
        self.crew = None
        self.results = None
        self.start_time = None
        self.end_time = None
        
        # Default personality traits for team members
        # These can be customized for your specific research question
        self.default_personalities = [
            {
                "name": "Alex",
                "role": "Team Leader",
                "expertise": "project management",
                "traits": {
                    "openness": 0.7,
                    "conscientiousness": 0.8,
                    "extraversion": 0.7,
                    "agreeableness": 0.6,
                    "neuroticism": 0.3
                }
            },
            {
                "name": "Blair",
                "role": "Technical Expert",
                "expertise": "software development",
                "traits": {
                    "openness": 0.8,
                    "conscientiousness": 0.7,
                    "extraversion": 0.4,
                    "agreeableness": 0.5,
                    "neuroticism": 0.4
                }
            },
            {
                "name": "Casey",
                "role": "Creative Lead",
                "expertise": "design thinking",
                "traits": {
                    "openness": 0.9,
                    "conscientiousness": 0.5,
                    "extraversion": 0.7,
                    "agreeableness": 0.7,
                    "neuroticism": 0.4
                }
            },
            {
                "name": "Drew",
                "role": "Analyst",
                "expertise": "data analysis",
                "traits": {
                    "openness": 0.6,
                    "conscientiousness": 0.9,
                    "extraversion": 0.3,
                    "agreeableness": 0.6,
                    "neuroticism": 0.4
                }
            },
            {
                "name": "Ellis",
                "role": "Marketing Specialist",
                "expertise": "market research",
                "traits": {
                    "openness": 0.7,
                    "conscientiousness": 0.6,
                    "extraversion": 0.8,
                    "agreeableness": 0.7,
                    "neuroticism": 0.3
                }
            },
            {
                "name": "Finley",
                "role": "Devil's Advocate",
                "expertise": "critical thinking",
                "traits": {
                    "openness": 0.9,
                    "conscientiousness": 0.6,
                    "extraversion": 0.5,
                    "agreeableness": 0.3,
                    "neuroticism": 0.4,
                    "conformity": 0.2  # Special trait for deviant members
                }
            }
        ]
    
    def setup_team(self, custom_personalities: Optional[List[Dict]] = None):
        """
        Set up the team with the specified personalities.
        
        Args:
            custom_personalities: Optional list of custom personality definitions
        """
        personalities = custom_personalities if custom_personalities else self.default_personalities
        
        # Determine team size based on parameters
        actual_team_size = min(self.team_size, len(personalities) - 1)  # -1 to exclude deviant
        
        # Create regular team members
        for i in range(actual_team_size):
            person = personalities[i]
            name = person["name"]
            role = person["role"]
            expertise = person["expertise"]
            traits = person["traits"]
            
            # Create an agent
            agent = self._create_agent(name, role, expertise, traits)
            self.agents.append(agent)
            
        # Add deviant member if specified
        if self.include_deviant:
            deviant = personalities[-1]  # Last personality is deviant
            agent = self._create_deviant_agent(
                deviant["name"], 
                deviant["role"], 
                deviant["expertise"], 
                deviant["traits"]
            )
            self.agents.append(agent)
    
    def _create_agent(self, name: str, role: str, expertise: str, traits: Dict[str, float]):
        """Create a team member agent with specific traits."""
        traits_text = self._traits_to_text(traits)
        
        agent = Agent(
            role=role,
            goal=f"Contribute your expertise in {expertise} to help the team succeed",
            backstory=f"""You are {name}, with expertise in {expertise}.
            {traits_text}
            You work well with others but also have your own perspective and ideas.
            You want the team to succeed and share your knowledge.""",
            verbose=True,
            allow_delegation=role == "Team Leader",
            llm=self.model
        )
        
        return {
            "name": name,
            "role": role,
            "expertise": expertise,
            "traits": traits,
            "agent": agent
        }
    
    def _create_deviant_agent(self, name: str, role: str, expertise: str, traits: Dict[str, float]):
        """Create a 'deviant' team member who challenges group thinking."""
        traits_text = self._traits_to_text(traits)
        
        agent = Agent(
            role=role,
            goal=f"Contribute your expertise while challenging conventional thinking",
            backstory=f"""You are {name}, with expertise in {expertise}.
            {traits_text}
            You are known for challenging the status quo and questioning assumptions.
            You believe that the best ideas emerge from constructive conflict and diverse perspectives. 
            You often play devil's advocate even when you might agree with the team.""",
            verbose=True,
            llm=self.model
        )
        
        return {
            "name": name,
            "role": role,
            "expertise": expertise,
            "traits": traits,
            "agent": agent
        }
    
    def _traits_to_text(self, traits: Dict[str, float]) -> str:
        """Convert personality traits to descriptive text."""
        descriptions = []
        
        trait_descriptions = {
            "openness": {
                "high": "You are very open to new ideas and experiences.",
                "low": "You prefer traditional, familiar approaches."
            },
            "conscientiousness": {
                "high": "You are highly organized and detail-oriented.",
                "low": "You tend to be flexible and spontaneous rather than organized."
            },
            "extraversion": {
                "high": "You are outgoing and energized by social interaction.",
                "low": "You are more reserved and prefer thinking before speaking."
            },
            "agreeableness": {
                "high": "You prioritize team harmony and are cooperative.",
                "low": "You're not afraid of disagreement and can be competitive."
            },
            "neuroticism": {
                "high": "You tend to worry about things going wrong.",
                "low": "You are emotionally stable and rarely get stressed."
            },
            "conformity": {
                "high": "You tend to go along with group decisions.",
                "low": "You often question group consensus and challenge the team's thinking."
            }
        }
        
        for trait, value in traits.items():
            if trait in trait_descriptions:
                if value > 0.7:
                    descriptions.append(trait_descriptions[trait]["high"])
                elif value < 0.3:
                    descriptions.append(trait_descriptions[trait]["low"])
        
        return " ".join(descriptions)
    
    def add_task(self, description: str, assigned_to: str, expected_output: str, context: str = ""):
        """
        Add a task to the simulation.
        
        Args:
            description: Description of the task
            assigned_to: Role of the agent assigned to the task
            expected_output: Expected format of the output
            context: Additional context for the task
        """
        # Find the agent with the matching role
        agent_data = next((a for a in self.agents if a["role"] == assigned_to), None)
        
        if not agent_data:
            raise ValueError(f"No agent with role '{assigned_to}' found in the team")
        
        task = Task(
            description=description,
            agent=agent_data["agent"],
            expected_output=expected_output,
            context=context
        )
        
        self.tasks.append({
            "description": description,
            "assigned_to": assigned_to,
            "task_object": task
        })
        
        return task
    
    def run_simulation(self, process_type: str = "hierarchical"):
        """
        Run the simulation with the specified process type.
        
        Args:
            process_type: 'sequential' or 'hierarchical'
        """
        if not self.agents:
            raise ValueError("No agents have been added to the simulation. Call setup_team() first.")
            
        if not self.tasks:
            raise ValueError("No tasks have been added to the simulation.")
        
        self.start_time = datetime.now()
        
        # Set up the process type
        process = Process.hierarchical if process_type.lower() == "hierarchical" else Process.sequential
        
        # Create the crew
        self.crew = Crew(
            agents=[a["agent"] for a in self.agents],
            tasks=[t["task_object"] for t in self.tasks],
            verbose=2,
            process=process
        )
        
        # Run the simulation
        print(f"Starting simulation: {self.simulation_name}")
        print(f"Team composition: {len(self.agents)} members")
        print(f"Process type: {process_type}")
        
        # Execute the crew's tasks
        results = self.crew.kickoff()
        
        self.end_time = datetime.now()
        self.results = results
        
        # Process and return the results
        processed_results = self.process_results(results)
        return processed_results
    
    def process_results(self, results):
        """
        Process the raw results from the simulation.
        
        Args:
            results: Raw results from the crew.kickoff() method
        """
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Create structured metrics
        metrics = {
            "simulation_name": self.simulation_name,
            "duration_seconds": duration,
            "team_size": len(self.agents),
            "task_count": len(self.tasks),
            "include_deviant": self.include_deviant,
            "process_type": self.crew.process.name,
            "team_composition": [
                {
                    "name": agent["name"],
                    "role": agent["role"],
                    "expertise": agent["expertise"],
                    "traits": agent["traits"]
                } for agent in self.agents
            ],
            "tasks": [
                {
                    "description": task["description"],
                    "assigned_to": task["assigned_to"]
                } for task in self.tasks
            ],
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def save_results(self, directory: str = "../data"):
        """
        Save the simulation results to a file.
        
        Args:
            directory: Directory to save the results in
        """
        if not self.results:
            raise ValueError("No results to save. Run the simulation first.")
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        filename = f"{directory}/{self.simulation_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"Results saved to {filename}")
        return filename


def create_problem_solving_simulation(include_deviant=True, model="gpt-4o-mini"):
    """
    Create a sample problem-solving simulation.
    
    Args:
        include_deviant: Whether to include a deviant team member
        model: The LLM model to use
    """
    # Create the simulation
    sim = TeamSimulation(
        simulation_name="problem_solving_team",
        team_size=4,  # 4 regular members
        include_deviant=include_deviant,
        model=model
    )
    
    # Set up the team
    sim.setup_team()
    
    # Add tasks
    sim.add_task(
        description="""
        Your team needs to solve the following problem:
        
        A university department is experiencing low student engagement in online courses.
        Attendance in virtual lectures is down 30%, assignment completion rates have dropped,
        and student feedback indicates feelings of disconnection.
        
        As team leader, coordinate with your team to develop a comprehensive solution
        to improve student engagement in online courses.
        """,
        assigned_to="Team Leader",
        expected_output="A comprehensive plan to address the student engagement problem",
        context="This is a complex problem requiring input from multiple perspectives."
    )
    
    sim.add_task(
        description="""
        Based on your technical expertise, propose digital tools and platforms
        that could enhance the online learning experience and increase student engagement.
        """,
        assigned_to="Technical Expert",
        expected_output="A list of recommended digital tools with justification for each",
        context="Consider issues like ease of use, interactivity, and accessibility."
    )
    
    sim.add_task(
        description="""
        Design an engaging online learning experience that incorporates 
        elements of gamification, social interaction, and interactive content.
        """,
        assigned_to="Creative Lead",
        expected_output="A creative design proposal for engaging online courses",
        context="Your design should address the emotional and social aspects of learning."
    )
    
    sim.add_task(
        description="""
        Analyze patterns in student engagement data and identify key factors
        that correlate with higher engagement in online learning environments.
        """,
        assigned_to="Analyst",
        expected_output="A data-backed analysis of engagement factors",
        context="Consider both quantitative and qualitative factors in your analysis."
    )
    
    # If we have a deviant, add their task
    if include_deviant:
        sim.add_task(
            description="""
            Challenge the team's assumptions about online learning and student engagement.
            Consider whether the problem has been correctly framed and if there are
            alternative approaches that haven't been considered.
            """,
            assigned_to="Devil's Advocate",
            expected_output="A critical analysis of the team's approach with alternative perspectives",
            context="Your role is to prevent groupthink and ensure all angles are considered."
        )
    
    return sim


def create_decision_making_simulation(include_deviant=True, model="gpt-4o-mini"):
    """
    Create a sample decision-making simulation.
    
    Args:
        include_deviant: Whether to include a deviant team member
        model: The LLM model to use
    """
    # Create the simulation
    sim = TeamSimulation(
        simulation_name="decision_making_team",
        team_size=4,  # 4 regular members
        include_deviant=include_deviant,
        model=model
    )
    
    # Set up the team
    sim.setup_team()
    
    # Add tasks
    sim.add_task(
        description="""
        Your team needs to decide on a new product to develop for your software company.
        You have the following options:
        
        1. A mobile app for personal finance management
        2. A productivity tool for remote teams
        3. An AI-powered educational platform
        4. A health and wellness tracking system
        
        As team leader, facilitate a decision-making process to select the best option
        and create an implementation plan.
        """,
        assigned_to="Team Leader",
        expected_output="A decision and implementation plan with reasoning",
        context="The company has limited resources, so you can only choose one option."
    )
    
    sim.add_task(
        description="""
        Evaluate the technical feasibility of each product option.
        Consider development time, technical complexity, and required resources.
        """,
        assigned_to="Technical Expert",
        expected_output="A technical feasibility analysis for each option",
        context="The company has a team of 8 developers with various skill levels."
    )
    
    sim.add_task(
        description="""
        Develop creative concepts for each potential product, including
        user experience design, branding considerations, and visual identity.
        """,
        assigned_to="Creative Lead",
        expected_output="Creative concepts and design direction for each option",
        context="The company values intuitive, elegant design that stands out in the market."
    )
    
    sim.add_task(
        description="""
        Analyze market data for each product option, including
        market size, competition, target demographics, and revenue potential.
        """,
        assigned_to="Analyst",
        expected_output="A market analysis with data-backed recommendations",
        context="Consider both short-term revenue and long-term growth potential."
    )
    
    # If we have a deviant, add their task
    if include_deviant:
        sim.add_task(
            description="""
            Challenge the team's thinking about these product options.
            Are there assumptions being made? Are there other options not being considered?
            Is the team approaching this decision correctly?
            """,
            assigned_to="Devil's Advocate",
            expected_output="A critical analysis of the decision-making process and options",
            context="Your role is to ensure the team avoids tunnel vision and considers all angles."
        )
    
    return sim


def main():
    """Run a demonstration of the simulation template."""
    # Example 1: Problem-solving simulation with a deviant
    print("\n=== RUNNING PROBLEM-SOLVING SIMULATION WITH DEVIANT ===\n")
    sim1 = create_problem_solving_simulation(include_deviant=True)
    results1 = sim1.run_simulation(process_type="hierarchical")
    sim1.save_results()
    
    # Example 2: Decision-making simulation without a deviant
    print("\n=== RUNNING DECISION-MAKING SIMULATION WITHOUT DEVIANT ===\n")
    sim2 = create_decision_making_simulation(include_deviant=False)
    results2 = sim2.run_simulation(process_type="sequential")
    sim2.save_results()
    
    print("\n=== SIMULATION DEMONSTRATIONS COMPLETE ===\n")
    print("You can modify the template to create your own simulations!")


if __name__ == "__main__":
    main() 