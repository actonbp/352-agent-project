"""
Diversity and Inclusion Team Simulation

This simulation explores how team diversity and inclusion practices affect team dynamics,
decision-making, and outcomes. It allows for comparing teams with varying demographic 
and cognitive diversity factors.

Research questions this could help explore:
1. How does cognitive diversity affect problem-solving capability?
2. How do inclusive practices impact team satisfaction and engagement?
3. How do diverse teams perform on different types of tasks compared to homogeneous teams?
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables (for API keys)
load_dotenv()

class DiversityInclusionSimulation:
    """Simulation to explore diversity and inclusion in teams."""
    
    # Dimensions of diversity that can be varied
    DIVERSITY_DIMENSIONS = {
        "demographic": [
            "gender", "age", "ethnicity", "nationality", 
            "educational_background", "socioeconomic_background"
        ],
        "cognitive": [
            "thinking_style", "problem_solving_approach", 
            "communication_style", "risk_tolerance"
        ],
        "experiential": [
            "industry_experience", "functional_expertise",
            "career_path", "international_experience"
        ]
    }
    
    # Inclusion practices that can be incorporated
    INCLUSION_PRACTICES = {
        "high": {
            "description": "High inclusion team with strong inclusive practices",
            "behaviors": """
            This team has strong inclusion practices:
            - All team members are explicitly invited to contribute
            - Diverse perspectives are actively sought out and valued
            - Decision-making processes involve all team members
            - Team norms support psychological safety
            - Communication is transparent and accessible
            - Team leader actively promotes equity
            """,
            "meeting_structure": """
            When conducting team meetings or discussions:
            - Begin by ensuring all voices are heard
            - Use structured turn-taking to prevent domination by some members
            - Actively solicit input from quieter members
            - Acknowledge and build upon others' ideas
            - Encourage respectful challenging of assumptions
            - Summarize diverse perspectives before making decisions
            """
        },
        "low": {
            "description": "Low inclusion team with minimal inclusive practices",
            "behaviors": """
            This team has minimal inclusion practices:
            - Team interactions tend to be dominated by a few voices
            - Alternative perspectives are rarely sought out
            - Decision-making often happens informally among select members
            - Team culture rewards conformity over diverse thinking
            - Communication is inconsistent and varies by team member
            - Team leader shows unconscious favoritism
            """,
            "meeting_structure": """
            When conducting team meetings or discussions:
            - Move quickly through agenda items focusing on efficiency
            - Allow natural conversation flow (dominant voices tend to lead)
            - Make decisions based on majority or authority perspectives
            - Focus primarily on task completion rather than process
            - Minimize dissent to maintain harmony and speed
            - Rely on conventional approaches and established methods
            """
        }
    }
    
    def __init__(self, 
                 simulation_name: str,
                 team_size: int = 5,
                 inclusion_level: str = "high",
                 diversity_level: str = "high", 
                 model: str = "gpt-4o-mini"):
        """
        Initialize the diversity and inclusion simulation.
        
        Args:
            simulation_name: Name of the simulation
            team_size: Number of team members
            inclusion_level: "high" or "low" level of inclusion practices
            diversity_level: "high" or "low" level of team diversity
            model: The LLM model to use
        """
        if inclusion_level not in self.INCLUSION_PRACTICES:
            raise ValueError(f"Inclusion level must be one of: {', '.join(self.INCLUSION_PRACTICES.keys())}")
            
        self.simulation_name = simulation_name
        self.team_size = team_size
        self.inclusion_level = inclusion_level
        self.diversity_level = diversity_level
        self.model = model
        self.agents = []
        self.tasks = []
        self.crew = None
        self.results = None
        self.start_time = None
        self.end_time = None
        
        # Generate diverse team member profiles
        self.team_profiles = self._generate_team_profiles(team_size, diversity_level)
    
    def _generate_team_profiles(self, size: int, diversity_level: str) -> List[Dict]:
        """
        Generate team member profiles with varying diversity based on diversity_level.
        
        Args:
            size: Number of team members to generate
            diversity_level: "high" or "low" diversity
        
        Returns:
            List of team member profile dictionaries
        """
        # Common names that can work across various demographics
        names = [
            "Alex", "Taylor", "Jordan", "Casey", "Riley", 
            "Morgan", "Jamie", "Drew", "Avery", "Quinn",
            "Cameron", "Reese", "Dakota", "Skyler", "Phoenix"
        ]
        
        # Professional roles
        roles = [
            "Data Analyst", "Project Manager", "UX Designer", 
            "Software Engineer", "Marketing Specialist",
            "Financial Advisor", "HR Consultant", "Product Manager", 
            "Operations Specialist", "Research Scientist"
        ]
        
        # Educational backgrounds
        educations = [
            "Computer Science", "Business Administration", "Psychology",
            "Engineering", "Liberal Arts", "Natural Sciences", 
            "Design", "Mathematics", "Social Sciences", "Humanities"
        ]
        
        # Generate team profiles
        profiles = []
        
        # Always have a facilitator role
        facilitator_profile = {
            "name": random.choice(names),
            "role": "Team Facilitator",
            "background": random.choice(educations),
            "thinking_style": "Integrative",
            "communication_style": "Inclusive",
            "expertise": "Team Dynamics",
            "years_experience": random.randint(5, 15)
        }
        profiles.append(facilitator_profile)
        names.remove(facilitator_profile["name"])
        
        # Generate regular team members
        for i in range(size - 1):  # -1 because we already added the facilitator
            if i < len(names) and i < len(roles):
                name = names[i]
                role = roles[i]
                education = random.choice(educations)
                
                # For high diversity, ensure more variation
                if diversity_level == "high":
                    thinking_styles = ["Analytical", "Creative", "Practical", "Conceptual", "Reflective"]
                    communication_styles = ["Direct", "Collaborative", "Analytical", "Intuitive", "Functional"]
                    expertise_areas = ["Technical", "Process", "People", "Strategy", "Implementation"]
                    
                    profile = {
                        "name": name,
                        "role": role,
                        "background": education,
                        "thinking_style": random.choice(thinking_styles),
                        "communication_style": random.choice(communication_styles),
                        "expertise": random.choice(expertise_areas),
                        "years_experience": random.randint(1, 20)
                    }
                else:
                    # For low diversity, create more homogeneous profiles
                    profile = {
                        "name": name,
                        "role": role,
                        "background": education,
                        "thinking_style": "Analytical" if i % 2 == 0 else "Practical",
                        "communication_style": "Direct" if i % 2 == 0 else "Collaborative",
                        "expertise": "Technical" if i % 2 == 0 else "Process",
                        "years_experience": random.randint(5, 10)
                    }
                
                profiles.append(profile)
        
        return profiles
    
    def setup_team(self):
        """Set up the team with appropriate inclusion practices."""
        # Create team facilitator first
        facilitator_profile = next(p for p in self.team_profiles if p["role"] == "Team Facilitator")
        self._create_facilitator(facilitator_profile, self.inclusion_level)
        
        # Create remaining team members
        member_profiles = [p for p in self.team_profiles if p["role"] != "Team Facilitator"]
        for profile in member_profiles:
            self._create_team_member(profile, self.inclusion_level)
    
    def _create_facilitator(self, profile: Dict, inclusion_level: str):
        """Create a team facilitator agent with specific inclusion practices."""
        inclusion_info = self.INCLUSION_PRACTICES[inclusion_level]
        
        facilitator = Agent(
            role="Team Facilitator",
            goal=f"Lead the team with {inclusion_level} inclusion practices to achieve optimal results",
            backstory=f"""You are {profile['name']}, an experienced team facilitator specializing in team dynamics.
            You have {profile['years_experience']} years of experience and a background in {profile['background']}.
            
            {inclusion_info['behaviors']}
            
            When facilitating team discussions:
            {inclusion_info['meeting_structure']}
            
            Your primary responsibility is to guide the team through the assigned task while implementing
            these inclusion practices consistently.""",
            verbose=True,
            allow_delegation=True,
            llm=self.model
        )
        
        self.agents.append({
            "name": profile["name"],
            "role": profile["role"],
            "background": profile["background"],
            "thinking_style": profile["thinking_style"],
            "communication_style": profile["communication_style"],
            "inclusion_practices": inclusion_level,
            "agent": facilitator
        })
        
        return facilitator
    
    def _create_team_member(self, profile: Dict, inclusion_level: str):
        """Create a team member agent with specific characteristics."""
        # Adjust backstory based on inclusion level
        if inclusion_level == "high":
            participation_guidance = """
            In this team, you're encouraged to actively share your perspective.
            The team values diverse viewpoints and creates space for all voices.
            You should feel comfortable expressing both agreement and disagreement.
            """
        else:
            participation_guidance = """
            In this team, you'll need to find opportunities to contribute.
            Team discussions can move quickly, and sometimes quieter perspectives get overlooked.
            You should try to share your insights when possible without disrupting the flow.
            """
        
        # Create unique perspectives based on thinking style
        if profile["thinking_style"] == "Analytical":
            approach = "You tend to analyze situations logically, looking for patterns and evidence."
        elif profile["thinking_style"] == "Creative":
            approach = "You tend to approach problems from unexpected angles, generating novel ideas."
        elif profile["thinking_style"] == "Practical":
            approach = "You focus on practical, implementable solutions rather than abstract concepts."
        elif profile["thinking_style"] == "Conceptual":
            approach = "You prefer working with big-picture concepts and theoretical frameworks."
        elif profile["thinking_style"] == "Reflective":
            approach = "You carefully consider all angles before offering thoughtful, nuanced perspectives."
        else:
            approach = "You bring your unique perspective to problem-solving and team discussions."
        
        member = Agent(
            role=profile["role"],
            goal=f"Contribute your expertise as a {profile['role']} to help the team succeed",
            backstory=f"""You are {profile['name']}, a {profile['role']} with {profile['years_experience']} years
            of experience and a background in {profile['background']}.
            
            You have a {profile['thinking_style']} thinking style and tend to communicate in a 
            {profile['communication_style']} manner. Your area of expertise is {profile['expertise']}.
            
            {approach}
            
            {participation_guidance}
            
            Your goal is to contribute meaningfully to the team while being authentic to your
            perspective and communication style.""",
            verbose=True,
            llm=self.model
        )
        
        self.agents.append({
            "name": profile["name"],
            "role": profile["role"],
            "background": profile["background"],
            "thinking_style": profile["thinking_style"],
            "communication_style": profile["communication_style"],
            "agent": member
        })
        
        return member
    
    def setup_innovation_task(self):
        """Set up an innovation task that benefits from diverse perspectives."""
        
        # Task for the facilitator
        self.add_task(
            description=f"""
            Your team has been tasked with developing an innovative digital solution 
            to improve mental health support for university students. As the team facilitator
            using {self.inclusion_level} inclusion practices, guide your team through this challenge.
            
            You need to:
            1. Define the scope of the mental health challenges facing students
            2. Facilitate a collaborative ideation process
            3. Evaluate proposed solutions
            4. Develop an implementation plan for the chosen solution
            5. Prepare a summary of your team's process and solution
            
            Remember to maintain the {self.inclusion_level} inclusion practices throughout.
            """,
            assigned_to="Team Facilitator",
            expected_output="A comprehensive proposal for a digital mental health solution, including implementation plan and team process summary.",
            context="Student mental health has become increasingly important, especially with recent changes in education delivery and social conditions."
        )
        
        # Tasks for team members based on their roles
        for agent_data in self.agents:
            if agent_data["role"] == "Team Facilitator":
                continue  # Already assigned task above
                
            role = agent_data["role"]
            name = agent_data["name"]
            thinking_style = agent_data["thinking_style"]
            
            # Customize task based on role
            if "Analyst" in role or "Data" in role:
                self.add_task(
                    description=f"""
                    Research and analyze data related to student mental health challenges and 
                    digital support solutions. Consider user demographics, usage patterns,
                    and effectiveness metrics of existing solutions.
                    
                    Apply your {thinking_style} thinking style to identify insights that might
                    not be immediately obvious to others.
                    """,
                    assigned_to=role,
                    expected_output="Data analysis with key insights about student mental health needs and effective digital interventions.",
                    context="Data can help identify patterns in mental health challenges and solution effectiveness."
                )
            elif "Engineer" in role or "Technical" in role or "Software" in role:
                self.add_task(
                    description=f"""
                    Evaluate technical feasibility of digital mental health support solutions.
                    Consider aspects like platform options, privacy/security requirements,
                    integration needs, and development resources.
                    
                    Apply your {thinking_style} thinking style to identify technical considerations
                    that others might overlook.
                    """,
                    assigned_to=role,
                    expected_output="Technical assessment of solution options with implementation requirements.",
                    context="Technical feasibility and security are crucial for mental health applications."
                )
            elif "Design" in role or "UX" in role:
                self.add_task(
                    description=f"""
                    Design user-centered approaches for digital mental health support.
                    Consider user experience factors, accessibility, engagement strategies,
                    and interface design.
                    
                    Apply your {thinking_style} thinking style to create design solutions
                    that effectively meet student needs.
                    """,
                    assigned_to=role,
                    expected_output="User experience design concepts for the mental health solution.",
                    context="Effective mental health solutions must be engaging and easy to use."
                )
            elif "Marketing" in role or "Market" in role:
                self.add_task(
                    description=f"""
                    Develop strategies for promoting the mental health solution to students.
                    Consider adoption barriers, messaging approaches, and distribution channels.
                    
                    Apply your {thinking_style} thinking style to identify effective ways
                    to reach and engage the student population.
                    """,
                    assigned_to=role,
                    expected_output="Marketing and adoption strategy for the mental health solution.",
                    context="Even the best solution won't help if students don't know about or use it."
                )
            else:
                # Generic task for other roles
                self.add_task(
                    description=f"""
                    Contribute your expertise as a {role} to the team's mental health solution.
                    Consider how your unique perspective and skills can enhance the team's approach.
                    
                    Apply your {thinking_style} thinking style to identify aspects of the challenge
                    that align with your expertise.
                    """,
                    assigned_to=role,
                    expected_output=f"Specialized input related to {role} expertise for the mental health solution.",
                    context=f"Your {role} perspective adds valuable diversity to the team's thinking."
                )
    
    def setup_decision_task(self):
        """Set up a complex decision-making task that benefits from diverse perspectives."""
        
        # Task for the facilitator
        self.add_task(
            description=f"""
            Your team must evaluate and recommend a strategy for a company expanding into 
            international markets. The company is a mid-sized tech firm that has been 
            successful domestically but has no international experience. As the team facilitator
            using {self.inclusion_level} inclusion practices, guide your team through this decision process.
            
            You need to:
            1. Establish decision criteria for evaluating market options
            2. Facilitate collaborative analysis of at least three possible markets
            3. Ensure all perspectives are considered in the evaluation
            4. Lead the team to a final recommendation with implementation steps
            5. Document the decision process and rationale
            
            Remember to maintain the {self.inclusion_level} inclusion practices throughout.
            """,
            assigned_to="Team Facilitator",
            expected_output="A comprehensive market entry recommendation with implementation plan and documentation of the decision process.",
            context="This decision will significantly impact the company's future growth trajectory and resource allocation."
        )
        
        # Tasks for team members based on their roles
        for agent_data in self.agents:
            if agent_data["role"] == "Team Facilitator":
                continue  # Already assigned task above
                
            role = agent_data["role"]
            name = agent_data["name"]
            thinking_style = agent_data["thinking_style"]
            
            # Customize task based on role
            if "Analyst" in role or "Data" in role:
                self.add_task(
                    description=f"""
                    Research and analyze market data for potential international expansion targets.
                    Consider economic indicators, market size, growth projections, competitive landscape,
                    and relevant regulatory factors.
                    
                    Apply your {thinking_style} thinking style to identify insights that might
                    not be immediately obvious to others.
                    """,
                    assigned_to=role,
                    expected_output="Market analysis with comparative data on potential target markets.",
                    context="Quantitative and qualitative data provide essential context for market selection."
                )
            elif "Financial" in role or "Finance" in role:
                self.add_task(
                    description=f"""
                    Develop financial projections and risk assessments for international expansion options.
                    Consider investment requirements, expected returns, currency risks, tax implications,
                    and financial sustainability.
                    
                    Apply your {thinking_style} thinking style to provide financial perspectives
                    that others might not consider.
                    """,
                    assigned_to=role,
                    expected_output="Financial analysis of expansion options with risk assessment.",
                    context="Financial viability is critical for successful international expansion."
                )
            elif "Engineer" in role or "Technical" in role or "Software" in role:
                self.add_task(
                    description=f"""
                    Evaluate technical requirements for serving international markets.
                    Consider infrastructure needs, localization requirements, technical compliance issues,
                    and development resources needed for different markets.
                    
                    Apply your {thinking_style} thinking style to identify technical considerations
                    that could impact market selection.
                    """,
                    assigned_to=role,
                    expected_output="Technical assessment of requirements for different international markets.",
                    context="Technical adaptations are often needed to serve international markets effectively."
                )
            elif "Operations" in role:
                self.add_task(
                    description=f"""
                    Analyze operational implications of international expansion options.
                    Consider supply chain requirements, staffing needs, logistics challenges,
                    and operational risk factors for different markets.
                    
                    Apply your {thinking_style} thinking style to identify operational considerations
                    that could impact market success.
                    """,
                    assigned_to=role,
                    expected_output="Operational analysis of expansion requirements for different markets.",
                    context="Operational execution is a key success factor in international expansion."
                )
            else:
                # Generic task for other roles
                self.add_task(
                    description=f"""
                    Contribute your expertise as a {role} to the international expansion decision.
                    Consider how your perspective and experience relate to the challenges of
                    entering new markets.
                    
                    Apply your {thinking_style} thinking style to identify aspects of market selection
                    that others might overlook.
                    """,
                    assigned_to=role,
                    expected_output=f"Specialized input related to {role} expertise for market selection decision.",
                    context=f"Your {role} perspective adds valuable diversity to the team's decision process."
                )
    
    def add_task(self, description: str, assigned_to: str, expected_output: str, context: str = ""):
        """Add a task to the simulation."""
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
    
    def run_simulation(self, process_type: str = "sequential"):
        """Run the simulation with the specified process type."""
        if not self.agents:
            raise ValueError("No agents have been added to the simulation. Call setup_team() first.")
            
        if not self.tasks:
            raise ValueError("No tasks have been added to the simulation. Set up a task scenario first.")
        
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
        print(f"Team diversity level: {self.diversity_level}")
        print(f"Inclusion practices level: {self.inclusion_level}")
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
        """Process the raw results from the simulation."""
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Create structured metrics
        metrics = {
            "simulation_name": self.simulation_name,
            "diversity_level": self.diversity_level,
            "inclusion_level": self.inclusion_level,
            "duration_seconds": duration,
            "team_size": len(self.agents),
            "task_count": len(self.tasks),
            "process_type": self.crew.process.name,
            "team_composition": [
                {
                    "name": agent["name"],
                    "role": agent["role"],
                    "thinking_style": agent.get("thinking_style", ""),
                    "communication_style": agent.get("communication_style", ""),
                    "background": agent.get("background", "")
                } for agent in self.agents
            ],
            "tasks": [
                {
                    "description": task["description"][:100] + "...",  # Truncate for readability
                    "assigned_to": task["assigned_to"]
                } for task in self.tasks
            ],
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
    
    def save_results(self, directory: str = "../data"):
        """Save the simulation results to a file."""
        if not self.results:
            raise ValueError("No results to save. Run the simulation first.")
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        filename = f"{directory}/{self.simulation_name}_{self.diversity_level}_{self.inclusion_level}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"Results saved to {filename}")
        return filename


def run_diversity_inclusion_comparison(task_type="innovation", model="gpt-4o-mini"):
    """
    Run simulations comparing different diversity and inclusion configurations.
    
    Args:
        task_type: Type of task to simulate ("innovation" or "decision")
        model: LLM model to use
    """
    # Define configurations to test
    configurations = [
        {"diversity": "high", "inclusion": "high"},
        {"diversity": "high", "inclusion": "low"},
        {"diversity": "low", "inclusion": "high"},
        {"diversity": "low", "inclusion": "low"}
    ]
    
    results = {}
    
    for config in configurations:
        diversity = config["diversity"]
        inclusion = config["inclusion"]
        
        print(f"\n=== RUNNING SIMULATION WITH {diversity.upper()} DIVERSITY, {inclusion.upper()} INCLUSION ===\n")
        
        # Create and set up simulation
        sim = DiversityInclusionSimulation(
            simulation_name=f"{task_type}_task",
            team_size=5,
            diversity_level=diversity,
            inclusion_level=inclusion,
            model=model
        )
        
        # Set up team and task
        sim.setup_team()
        if task_type == "innovation":
            sim.setup_innovation_task()
        else:
            sim.setup_decision_task()
        
        # Run simulation
        result = sim.run_simulation(process_type="sequential")
        results[f"{diversity}_{inclusion}"] = result
        
        # Save results
        sim.save_results()
    
    print("\n=== DIVERSITY & INCLUSION COMPARISON COMPLETE ===\n")
    print(f"Compared {len(configurations)} team configurations on a {task_type} task")
    
    # Basic results comparison
    print("\nDuration Comparison:")
    for config_key, result in results.items():
        diversity, inclusion = config_key.split("_")
        print(f"{diversity.capitalize()} diversity, {inclusion.capitalize()} inclusion: {result['duration_seconds']:.2f} seconds")
    
    return results


def main():
    """Run demonstrations of the diversity and inclusion simulations."""
    print("Diversity and Inclusion Simulation Demonstration")
    print("===============================================")
    print("\nThis will run simulations comparing team diversity and inclusion levels.")
    print("Note: This will make multiple API calls and may take some time.")
    
    # Choose a smaller model for faster completion if desired
    model = "gpt-4o-mini"  # Alternatives: "gpt-4", "gpt-4o", etc.
    
    # Run simulations
    print("\nRunning innovation task simulations...")
    run_diversity_inclusion_comparison(task_type="innovation", model=model)
    
    print("\nRunning decision-making task simulations...")
    run_diversity_inclusion_comparison(task_type="decision", model=model)


if __name__ == "__main__":
    main() 