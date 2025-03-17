"""
Basic Team Simulation Example

This example demonstrates a simple team simulation with two agents working on a problem-solving task.
It shows how to:
1. Set up agent personalities
2. Create interaction patterns
3. Collect basic metrics
"""

import json
from typing import List, Dict
import datetime

class TeamMember:
    def __init__(self, name: str, personality: Dict[str, float]):
        self.name = name
        self.personality = personality
        self.contributions = []
        
    def __str__(self):
        return f"{self.name} ({', '.join(f'{k}: {v}' for k, v in self.personality.items())})"

class TeamSimulation:
    def __init__(self, members: List[TeamMember]):
        self.members = members
        self.conversation_history = []
        self.decisions = []
        self.start_time = None
        self.end_time = None
        
    def start_simulation(self):
        """Initialize and start the simulation."""
        self.start_time = datetime.datetime.now()
        print(f"Starting simulation with team members:")
        for member in self.members:
            print(f"- {member}")
            
    def end_simulation(self):
        """End the simulation and collect metrics."""
        self.end_time = datetime.datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        metrics = {
            "duration_seconds": duration,
            "total_contributions": len(self.conversation_history),
            "contributions_per_member": {
                member.name: len([c for c in self.conversation_history if c["member"] == member.name])
                for member in self.members
            },
            "decisions_made": len(self.decisions)
        }
        
        return metrics

def main():
    # Create team members with different personalities
    team_members = [
        TeamMember("Alice", {
            "openness": 0.8,
            "conscientiousness": 0.7,
            "extraversion": 0.6
        }),
        TeamMember("Bob", {
            "openness": 0.6,
            "conscientiousness": 0.8,
            "extraversion": 0.4
        })
    ]
    
    # Initialize simulation
    sim = TeamSimulation(team_members)
    
    # Run simulation
    sim.start_simulation()
    
    # Simulate some interactions (in a real implementation, this would use LLM calls)
    sim.conversation_history.append({
        "member": "Alice",
        "message": "I think we should approach this by breaking down the problem first.",
        "timestamp": datetime.datetime.now()
    })
    
    sim.conversation_history.append({
        "member": "Bob",
        "message": "Good idea. Let's list out the main components we need to consider.",
        "timestamp": datetime.datetime.now()
    })
    
    sim.decisions.append({
        "decision": "Adopt structured problem-solving approach",
        "timestamp": datetime.datetime.now(),
        "supporters": ["Alice", "Bob"]
    })
    
    # End simulation and get metrics
    metrics = sim.end_simulation()
    
    # Print results
    print("\nSimulation Results:")
    print(json.dumps(metrics, indent=2, default=str))

if __name__ == "__main__":
    main() 