"""
Leadership Style Simulation

This simulation explores how different leadership styles affect team dynamics and outcomes.
It allows for comparing authoritarian, democratic, laissez-faire, and transformational leadership.

Research questions this could help explore:
1. How does leadership style affect team creativity and innovation?
2. Which leadership style is most effective for different types of tasks?
3. How do team members with different personality traits respond to different leadership styles?
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables (for API keys)
load_dotenv()

class LeadershipStyleSimulation:
    """Simulation to explore different leadership styles."""
    
    LEADERSHIP_STYLES = {
        "authoritarian": {
            "description": "Directive leader who makes decisions with minimal input from team",
            "traits": {
                "openness": 0.3,  # Less open to others' ideas
                "conscientiousness": 0.9,  # Very organized and structured
                "extraversion": 0.7,  # Assertive communication
                "agreeableness": 0.3,  # More demanding and less cooperative
                "neuroticism": 0.4    # Generally stable emotionally
            },
            "behaviors": """
            You are a directive leader who believes in clear hierarchy and structure.
            You make decisions quickly and expect team members to follow your instructions.
            You provide detailed guidance and closely monitor progress.
            You believe that strong leadership means taking control and being decisive.
            You give feedback directly and focus on efficiency and results.
            """
        },
        "democratic": {
            "description": "Collaborative leader who involves team in decision-making",
            "traits": {
                "openness": 0.8,  # Open to different perspectives
                "conscientiousness": 0.7,  # Organized but flexible
                "extraversion": 0.6,  # Communicative but also listens
                "agreeableness": 0.8,  # Cooperative and supportive
                "neuroticism": 0.3    # Emotionally stable
            },
            "behaviors": """
            You are a collaborative leader who values team input and consensus.
            You facilitate discussions and encourage everyone to contribute ideas.
            You make decisions based on team feedback and shared goals.
            You believe that the best solutions come from collective intelligence.
            You distribute responsibility and trust team members to contribute their expertise.
            """
        },
        "laissez_faire": {
            "description": "Hands-off leader who delegates extensively and provides minimal direction",
            "traits": {
                "openness": 0.7,  # Open to whatever approach team takes
                "conscientiousness": 0.4,  # Less structured approach
                "extraversion": 0.5,  # Moderate involvement in discussions
                "agreeableness": 0.6,  # Generally agreeable but detached
                "neuroticism": 0.2    # Very relaxed about outcomes
            },
            "behaviors": """
            You are a hands-off leader who believes in giving team members complete autonomy.
            You provide resources and support but minimal direct guidance or intervention.
            You trust team members to make their own decisions and solve problems.
            You believe micromanaging inhibits creativity and personal growth.
            You evaluate outcomes rather than controlling the process.
            """
        },
        "transformational": {
            "description": "Inspirational leader who motivates through vision and personal connection",
            "traits": {
                "openness": 0.9,  # Very open to new ideas and change
                "conscientiousness": 0.6,  # Organized but prioritizes inspiration over structure
                "extraversion": 0.8,  # Highly engaging and communicative
                "agreeableness": 0.7,  # Supportive and positive
                "neuroticism": 0.3    # Generally optimistic and stable
            },
            "behaviors": """
            You are an inspirational leader who motivates through vision and personal connection.
            You articulate a compelling future state and connect work to deeper purpose.
            You mentor team members individually and help them develop professionally.
            You believe in leading by example and challenging status quo thinking.
            You focus on both achieving goals and transforming individuals and the team.
            """
        }
    }
    
    def __init__(self, 
                 simulation_name: str, 
                 leadership_style: str,
                 team_size: int = 4,
                 model: str = "gpt-4o-mini"):
        """
        Initialize the leadership simulation.
        
        Args:
            simulation_name: Name of the simulation
            leadership_style: One of "authoritarian", "democratic", "laissez_faire", "transformational"
            team_size: Number of team members (excluding leader)
            model: The LLM model to use
        """
        if leadership_style not in self.LEADERSHIP_STYLES:
            raise ValueError(f"Leadership style must be one of: {', '.join(self.LEADERSHIP_STYLES.keys())}")
            
        self.simulation_name = simulation_name
        self.leadership_style = leadership_style
        self.team_size = team_size
        self.model = model
        self.agents = []
        self.tasks = []
        self.crew = None
        self.results = None
        self.start_time = None
        self.end_time = None
        
        # Team member personalities
        self.team_personalities = [
            {
                "name": "Taylor",
                "role": "Technical Expert",
                "expertise": "software development",
                "traits": {
                    "openness": 0.6,
                    "conscientiousness": 0.8,
                    "extraversion": 0.4,
                    "agreeableness": 0.5,
                    "neuroticism": 0.3
                }
            },
            {
                "name": "Jordan",
                "role": "Creative Designer",
                "expertise": "user experience",
                "traits": {
                    "openness": 0.9,
                    "conscientiousness": 0.5,
                    "extraversion": 0.7,
                    "agreeableness": 0.7,
                    "neuroticism": 0.4
                }
            },
            {
                "name": "Riley",
                "role": "Project Coordinator",
                "expertise": "project management",
                "traits": {
                    "openness": 0.5,
                    "conscientiousness": 0.9,
                    "extraversion": 0.6,
                    "agreeableness": 0.7,
                    "neuroticism": 0.3
                }
            },
            {
                "name": "Casey",
                "role": "Market Researcher",
                "expertise": "market analysis",
                "traits": {
                    "openness": 0.7,
                    "conscientiousness": 0.7,
                    "extraversion": 0.5,
                    "agreeableness": 0.6,
                    "neuroticism": 0.4
                }
            },
            {
                "name": "Morgan",
                "role": "Finance Specialist",
                "expertise": "financial planning",
                "traits": {
                    "openness": 0.4,
                    "conscientiousness": 0.8,
                    "extraversion": 0.3,
                    "agreeableness": 0.5,
                    "neuroticism": 0.4
                }
            }
        ]
    
    def setup_team(self):
        """Set up the team with leader and members."""
        # Create the leader first
        self._create_leader()
        
        # Add team members (up to team_size)
        for i in range(min(self.team_size, len(self.team_personalities))):
            person = self.team_personalities[i]
            self._create_team_member(
                person["name"],
                person["role"],
                person["expertise"],
                person["traits"]
            )
    
    def _create_leader(self):
        """Create a leader agent based on the selected leadership style."""
        style_info = self.LEADERSHIP_STYLES[self.leadership_style]
        
        # Convert traits to text description
        traits_text = self._traits_to_text(style_info["traits"])
        
        leader = Agent(
            role="Team Leader",
            goal=f"Lead the team effectively using a {self.leadership_style} leadership style",
            backstory=f"""You are Alex, an experienced team leader with a {self.leadership_style} leadership style.
            {traits_text}
            {style_info["behaviors"]}
            Your job is to guide the team to successful completion of the project while 
            maintaining your leadership style throughout all interactions.""",
            verbose=True,
            allow_delegation=True,
            llm=self.model
        )
        
        self.agents.append({
            "name": "Alex",
            "role": "Team Leader",
            "leadership_style": self.leadership_style,
            "traits": style_info["traits"],
            "agent": leader
        })
        
        return leader
    
    def _create_team_member(self, name: str, role: str, expertise: str, traits: Dict[str, float]):
        """Create a team member agent with specific traits."""
        traits_text = self._traits_to_text(traits)
        
        # Customize backstory based on leader's style
        adaptation_to_leader = self._get_adaptation_text(traits, self.leadership_style)
        
        member = Agent(
            role=role,
            goal=f"Contribute your expertise in {expertise} to help the team succeed",
            backstory=f"""You are {name}, a team member with expertise in {expertise}.
            {traits_text}
            {adaptation_to_leader}
            You work well with others but also have your own perspective and ideas.
            You want the team to succeed and are willing to share your knowledge.""",
            verbose=True,
            llm=self.model
        )
        
        self.agents.append({
            "name": name,
            "role": role,
            "expertise": expertise,
            "traits": traits,
            "agent": member
        })
        
        return member
    
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
            }
        }
        
        for trait, value in traits.items():
            if trait in trait_descriptions:
                if value > 0.7:
                    descriptions.append(trait_descriptions[trait]["high"])
                elif value < 0.3:
                    descriptions.append(trait_descriptions[trait]["low"])
        
        return " ".join(descriptions)
    
    def _get_adaptation_text(self, traits: Dict[str, float], leadership_style: str) -> str:
        """Generate text about how this team member adapts to the leader's style."""
        
        # Check for potential conflict or alignment
        openness = traits.get("openness", 0.5)
        agreeableness = traits.get("agreeableness", 0.5)
        
        if leadership_style == "authoritarian":
            if agreeableness < 0.4:
                return "You sometimes struggle with directive leadership and may feel your autonomy is limited."
            elif agreeableness > 0.7:
                return "You tend to follow directions well and appreciate clear guidance from leadership."
                
        elif leadership_style == "laissez_faire":
            if traits.get("conscientiousness", 0.5) > 0.8:
                return "You sometimes prefer more structure than a hands-off leadership approach provides."
            elif openness > 0.7:
                return "You thrive with the autonomy provided by a hands-off leadership approach."
                
        elif leadership_style == "democratic":
            if openness < 0.4:
                return "You sometimes find collaborative decision-making processes time-consuming."
            elif openness > 0.7:
                return "You value being included in decisions and having your input considered."
                
        elif leadership_style == "transformational":
            if openness < 0.4:
                return "You sometimes find visionary leadership too abstract and prefer concrete direction."
            elif openness > 0.7:
                return "You are inspired by leaders who connect work to a larger purpose and vision."
        
        # Default response if no specific adaptation is identified
        return "You adapt your work style to different leadership approaches as needed."
    
    def setup_creative_task(self):
        """Set up a creative/innovative task scenario."""
        
        # Task for the leader
        self.add_task(
            description=f"""
            Your team has been tasked with designing an innovative solution to reduce plastic waste
            on your university campus. As the team leader using a {self.leadership_style} leadership style,
            guide your team through this creative challenge.
            
            You need to:
            1. Define the scope of the problem
            2. Facilitate the team's creative process
            3. Evaluate proposed ideas
            4. Select the most promising solution
            5. Create an implementation plan
            
            Remember to maintain your {self.leadership_style} leadership style throughout the process.
            """,
            assigned_to="Team Leader",
            expected_output="A comprehensive plan for reducing plastic waste on campus, including the selected solution and implementation steps.",
            context="This is an open-ended creative task that will test the team's innovation capabilities."
        )
        
        # Tasks for team members
        roles = [agent["role"] for agent in self.agents if agent["role"] != "Team Leader"]
        
        if "Technical Expert" in roles:
            self.add_task(
                description="""
                Research and propose technical solutions for reducing plastic waste on campus.
                Consider aspects like waste monitoring systems, recycling technologies, or digital platforms
                that could help track and reduce plastic usage.
                """,
                assigned_to="Technical Expert",
                expected_output="3-5 technology-based solutions with explanations of how they would work.",
                context="Focus on solutions that are technically feasible given university resources."
            )
            
        if "Creative Designer" in roles:
            self.add_task(
                description="""
                Design creative approaches to engage students in plastic waste reduction.
                Consider behavioral design, visual campaigns, or innovative product designs
                that could replace single-use plastics on campus.
                """,
                assigned_to="Creative Designer",
                expected_output="3-5 creative concepts with visual or behavioral design elements.",
                context="Focus on designs that would appeal to college students and drive behavior change."
            )
            
        if "Project Coordinator" in roles:
            self.add_task(
                description="""
                Develop a project timeline and resource allocation plan for implementing
                plastic waste reduction initiatives on campus. Consider stakeholders,
                required approvals, and potential challenges.
                """,
                assigned_to="Project Coordinator",
                expected_output="A project plan with timeline, resource requirements, and risk assessment.",
                context="Consider university bureaucracy and the academic calendar in your planning."
            )
            
        if "Market Researcher" in roles:
            self.add_task(
                description="""
                Research plastic waste trends on college campuses and successful 
                reduction initiatives implemented elsewhere. Analyze what has worked,
                what hasn't, and why.
                """,
                assigned_to="Market Researcher",
                expected_output="An analysis of successful plastic reduction initiatives with key success factors.",
                context="Focus on examples from similar universities when possible."
            )
            
        if "Finance Specialist" in roles:
            self.add_task(
                description="""
                Analyze the costs and potential savings of different plastic waste reduction
                strategies. Consider implementation costs, ongoing expenses, and potential
                financial benefits.
                """,
                assigned_to="Finance Specialist",
                expected_output="A cost-benefit analysis of different plastic reduction approaches.",
                context="Consider both short-term costs and long-term financial sustainability."
            )
    
    def setup_crisis_task(self):
        """Set up a crisis management task scenario."""
        
        # Task for the leader
        self.add_task(
            description=f"""
            Your team manages the IT systems for a midsize company. A ransomware attack has just
            been detected that threatens to encrypt all company data within 24 hours unless a payment
            is made. As the team leader using a {self.leadership_style} leadership style, you must
            guide your team through this crisis.
            
            You need to:
            1. Assess the situation and potential impact
            2. Develop an immediate response strategy
            3. Coordinate team actions to contain and resolve the threat
            4. Create a communication plan for stakeholders
            5. Develop a plan to prevent future attacks
            
            Remember to maintain your {self.leadership_style} leadership style throughout the process.
            """,
            assigned_to="Team Leader",
            expected_output="A comprehensive crisis response plan with immediate actions and future prevention strategies.",
            context="This is a time-sensitive situation requiring quick, effective decisions."
        )
        
        # Tasks for team members
        roles = [agent["role"] for agent in self.agents if agent["role"] != "Team Leader"]
        
        if "Technical Expert" in roles:
            self.add_task(
                description="""
                Analyze the ransomware attack from a technical perspective. Identify the attack vector,
                affected systems, and potential containment strategies. Recommend technical solutions
                for both immediate response and longer-term security.
                """,
                assigned_to="Technical Expert",
                expected_output="Technical analysis and recommendations for containment and recovery.",
                context="This is a sophisticated attack that bypassed standard security measures."
            )
            
        if "Creative Designer" in roles:
            self.add_task(
                description="""
                Develop alternative approaches to the ransomware situation. Consider creative workarounds
                for affected systems, user experience during the recovery, and innovative ways to
                maintain business operations during the crisis.
                """,
                assigned_to="Creative Designer",
                expected_output="Creative solutions for maintaining operations and managing user experience during the crisis.",
                context="Think beyond conventional cybersecurity approaches to solve this problem."
            )
            
        if "Project Coordinator" in roles:
            self.add_task(
                description="""
                Create a detailed response timeline and coordinate resources needed for the crisis response.
                Track all actions taken, manage team workload, and ensure critical tasks are prioritized.
                """,
                assigned_to="Project Coordinator",
                expected_output="A crisis response timeline with resource allocation and task prioritization.",
                context="The company's operations are severely impacted, and every hour counts."
            )
            
        if "Market Researcher" in roles:
            self.add_task(
                description="""
                Research similar ransomware attacks and how other organizations have responded.
                Analyze which approaches were successful, which weren't, and identify best practices
                for crisis communication with stakeholders.
                """,
                assigned_to="Market Researcher",
                expected_output="Analysis of similar cases with successful response strategies and communication approaches.",
                context="This type of attack has happened to other organizations in our industry."
            )
            
        if "Finance Specialist" in roles:
            self.add_task(
                description="""
                Analyze the financial implications of different response options, including paying the ransom
                versus recovery costs. Evaluate business continuity costs, potential liability, and insurance coverage.
                """,
                assigned_to="Finance Specialist",
                expected_output="Financial analysis of response options with risk assessment.",
                context="The ransom demand is $500,000, and the estimated recovery cost without paying is $750,000-1,200,000."
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
    
    def run_simulation(self, process_type: str = "hierarchical"):
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
        print(f"Leadership style: {self.leadership_style}")
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
            "leadership_style": self.leadership_style,
            "duration_seconds": duration,
            "team_size": len(self.agents) - 1,  # Exclude leader from count
            "task_count": len(self.tasks),
            "process_type": self.crew.process.name,
            "team_composition": [
                {
                    "name": agent["name"],
                    "role": agent["role"],
                    "traits": agent.get("traits", {}),
                    "leadership_style": agent.get("leadership_style", None)
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
            
        filename = f"{directory}/{self.simulation_name}_{self.leadership_style}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"Results saved to {filename}")
        return filename


def run_leadership_comparison(task_type="creative", model="gpt-4o-mini"):
    """
    Run simulations comparing different leadership styles on the same task.
    
    Args:
        task_type: Type of task to simulate ("creative" or "crisis")
        model: LLM model to use
    """
    leadership_styles = ["authoritarian", "democratic", "laissez_faire", "transformational"]
    results = {}
    
    for style in leadership_styles:
        print(f"\n=== RUNNING SIMULATION WITH {style.upper()} LEADERSHIP ===\n")
        
        # Create and set up simulation
        sim = LeadershipStyleSimulation(
            simulation_name=f"{task_type}_task",
            leadership_style=style,
            team_size=4,
            model=model
        )
        
        # Set up team and task
        sim.setup_team()
        if task_type == "creative":
            sim.setup_creative_task()
        else:
            sim.setup_crisis_task()
        
        # Run simulation
        result = sim.run_simulation(process_type="hierarchical")
        results[style] = result
        
        # Save results
        sim.save_results()
    
    print("\n=== LEADERSHIP STYLE COMPARISON COMPLETE ===\n")
    print(f"Compared {len(leadership_styles)} leadership styles on a {task_type} task")
    
    # Basic results comparison
    print("\nDuration Comparison:")
    for style, result in results.items():
        print(f"{style.capitalize()}: {result['duration_seconds']:.2f} seconds")
    
    return results


def main():
    """Run demonstrations of the leadership style simulations."""
    print("Leadership Style Simulation Demonstration")
    print("=========================================")
    print("\nThis will run simulations comparing leadership styles.")
    print("Note: This will make multiple API calls and may take some time.")
    
    # Choose a smaller model for faster completion if desired
    model = "gpt-4o-mini"  # Alternatives: "gpt-4", "gpt-4o", etc.
    
    # Run simulations
    print("\nRunning creative task simulations...")
    run_leadership_comparison(task_type="creative", model=model)
    
    print("\nRunning crisis task simulations...")
    run_leadership_comparison(task_type="crisis", model=model)


if __name__ == "__main__":
    main() 