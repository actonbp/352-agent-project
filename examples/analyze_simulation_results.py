"""
Analyze Team Simulation Results

This script demonstrates how to analyze the results from a CrewAI team simulation.
It includes:
1. Loading simulation results
2. Basic text analysis of agent interactions
3. Visualization of team dynamics
4. Comparing multiple simulation runs
"""

import os
import json
import glob
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def load_simulation_results(filepath):
    """Load simulation results from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_interactions(text):
    """Extract interactions from the simulation text."""
    # This is a simple example - you can make this more sophisticated
    interactions = []
    
    # Extract mentions of other team members
    lines = text.split('\n')
    for line in lines:
        if ':' in line and len(line.split(':')) > 1:
            speaker = line.split(':')[0].strip()
            content = ':'.join(line.split(':')[1:]).strip()
            
            interactions.append({
                'speaker': speaker,
                'content': content,
                'timestamp': datetime.now().isoformat()
            })
    
    return interactions

def analyze_sentiment(text):
    """A very simple sentiment analysis function.
    In a real implementation, use a proper NLP library or API."""
    positive_words = ['agree', 'good', 'great', 'excellent', 'yes', 'like', 'support', 'interesting']
    negative_words = ['disagree', 'bad', 'poor', 'no', 'don\'t', 'cannot', 'issue', 'problem']
    
    text = text.lower()
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

def count_contributions(interactions):
    """Count contributions by each team member."""
    return Counter([interaction['speaker'] for interaction in interactions])

def identify_agreement_patterns(interactions):
    """Identify patterns of agreement/disagreement."""
    agreement_patterns = []
    
    for i, interaction in enumerate(interactions[:-1]):
        next_interaction = interactions[i+1]
        
        # Simple heuristic for agreement detection
        if 'agree' in next_interaction['content'].lower():
            agreement_patterns.append({
                'agreeing_member': next_interaction['speaker'],
                'with_member': interaction['speaker'],
                'content': next_interaction['content']
            })
            
    return agreement_patterns

def visualize_contribution_distribution(contributions, title="Contribution Distribution"):
    """Visualize the distribution of contributions."""
    plt.figure(figsize=(10, 6))
    
    # Sort by number of contributions
    sorted_contributions = dict(sorted(contributions.items(), key=lambda x: x[1], reverse=True))
    
    bars = plt.bar(sorted_contributions.keys(), sorted_contributions.values())
    
    # Add count labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height}', ha='center', va='bottom')
    
    plt.title(title)
    plt.xlabel('Team Member')
    plt.ylabel('Number of Contributions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('contribution_distribution.png')
    plt.close()

def compare_simulations(sim_results_list, names=None):
    """Compare multiple simulation runs."""
    if names is None:
        names = [f'Simulation {i+1}' for i in range(len(sim_results_list))]
    
    # Create comparison metrics
    metrics = []
    
    for i, results in enumerate(sim_results_list):
        metrics.append({
            'name': names[i],
            'duration': results.get('duration_seconds', 0),
            'agent_count': results.get('number_of_agents', 0),
            'task_count': results.get('number_of_tasks', 0),
            # Add more metrics as needed
        })
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(metrics)
    
    # Visualize comparison
    plt.figure(figsize=(12, 6))
    
    # Plot duration
    plt.subplot(1, 2, 1)
    sns.barplot(x='name', y='duration', data=df)
    plt.title('Duration Comparison')
    plt.ylabel('Seconds')
    plt.xticks(rotation=45)
    
    # Plot agent & task counts
    plt.subplot(1, 2, 2)
    df_melted = pd.melt(df, id_vars=['name'], value_vars=['agent_count', 'task_count'],
                        var_name='Metric', value_name='Count')
    sns.barplot(x='name', y='Count', hue='Metric', data=df_melted)
    plt.title('Agent & Task Comparison')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('simulation_comparison.png')
    plt.close()
    
    return df

def analyze_simulation_run(results_path):
    """Analyze a single simulation run."""
    # Load results
    results = load_simulation_results(results_path)
    
    print(f"Analyzing simulation: {results.get('simulation_name', 'Unknown')}")
    print(f"Duration: {results.get('duration_seconds', 0):.2f} seconds")
    print(f"Agents: {results.get('number_of_agents', 0)}")
    print(f"Tasks: {results.get('number_of_tasks', 0)}")
    
    # In a real implementation, you would extract interactions from the text
    # This is a placeholder for demonstration purposes
    sample_interactions = [
        {'speaker': 'Morgan', 'content': 'I think we should focus on the mobile interface first.', 'timestamp': '2023-01-01T12:00:00'},
        {'speaker': 'Taylor', 'content': 'I agree, the mobile experience is critical.', 'timestamp': '2023-01-01T12:01:00'},
        {'speaker': 'Jordan', 'content': 'The UI should be minimalist and focus on usability.', 'timestamp': '2023-01-01T12:02:00'},
        {'speaker': 'Alex', 'content': 'I disagree. Should we reconsider if a mobile app is the right approach?', 'timestamp': '2023-01-01T12:03:00'},
        {'speaker': 'Casey', 'content': 'The data shows students prefer mobile apps for tracking.', 'timestamp': '2023-01-01T12:04:00'},
        {'speaker': 'Morgan', 'content': 'Good point, Alex. Let\'s consider alternatives too.', 'timestamp': '2023-01-01T12:05:00'},
        {'speaker': 'Taylor', 'content': 'We could do both mobile and web for maximum reach.', 'timestamp': '2023-01-01T12:06:00'},
        {'speaker': 'Jordan', 'content': 'I can design interfaces for both platforms.', 'timestamp': '2023-01-01T12:07:00'},
        {'speaker': 'Casey', 'content': 'The data supports Taylor\'s suggestion.', 'timestamp': '2023-01-01T12:08:00'},
        {'speaker': 'Morgan', 'content': 'Let\'s proceed with a multi-platform approach then.', 'timestamp': '2023-01-01T12:09:00'}
    ]
    
    # Analyze contributions
    contributions = count_contributions(sample_interactions)
    print("\nContribution Count:")
    for member, count in contributions.items():
        print(f"- {member}: {count}")
    
    # Visualize
    visualize_contribution_distribution(contributions, 
                                       f"Contribution Distribution - {results.get('simulation_name', 'Unknown')}")
    
    # Identify agreement patterns
    agreements = identify_agreement_patterns(sample_interactions)
    print("\nAgreement Patterns:")
    for agreement in agreements:
        print(f"- {agreement['agreeing_member']} agreed with {agreement['with_member']}")
    
    return results

def main():
    """Main function to demonstrate analysis of simulation results."""
    print("Team Simulation Analysis Demonstration")
    print("======================================")
    
    # Example: Load and analyze simulation results
    # In a real implementation, we would use actual result files
    
    # Create sample results directory if needed
    os.makedirs("../data", exist_ok=True)
    
    # For demonstration, we'll create a sample result file if none exists
    sample_file = "../data/sample_results.json"
    if not os.path.exists(sample_file):
        sample_data = {
            "simulation_name": "project_planning_team",
            "duration_seconds": 120.5,
            "number_of_agents": 5,
            "number_of_tasks": 5,
            "agent_composition": [
                {"name": "Morgan", "role": "Team Leader", "personality": {"openness": 0.7}},
                {"name": "Taylor", "role": "Technical Expert", "personality": {"openness": 0.8}},
                {"name": "Jordan", "role": "Creative Designer", "personality": {"openness": 0.9}},
                {"name": "Casey", "role": "Data Analyst", "personality": {"openness": 0.6}},
                {"name": "Alex", "role": "Deviant Strategic Thinker", "personality": {"conformity": 0.2}}
            ],
            "results": "Sample simulation results would go here.",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f, indent=2, default=str)
    
    # Analyze a single simulation
    results = analyze_simulation_run(sample_file)
    
    # Create a second sample file for comparison
    sample_file2 = "../data/sample_results2.json"
    if not os.path.exists(sample_file2):
        sample_data = {
            "simulation_name": "project_planning_team_no_deviant",
            "duration_seconds": 95.2,
            "number_of_agents": 4,  # No deviant member
            "number_of_tasks": 4,
            "agent_composition": [
                {"name": "Morgan", "role": "Team Leader", "personality": {"openness": 0.7}},
                {"name": "Taylor", "role": "Technical Expert", "personality": {"openness": 0.8}},
                {"name": "Jordan", "role": "Creative Designer", "personality": {"openness": 0.9}},
                {"name": "Casey", "role": "Data Analyst", "personality": {"openness": 0.6}}
            ],
            "results": "Sample simulation results without deviant member would go here.",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(sample_file2, 'w') as f:
            json.dump(sample_data, f, indent=2, default=str)
    
    # Compare multiple simulations
    print("\nComparing Multiple Simulations:")
    results2 = load_simulation_results(sample_file2)
    
    comparison_df = compare_simulations(
        [results, results2],
        names=["With Deviant", "Without Deviant"]
    )
    
    print("\nComparison Summary:")
    print(comparison_df)
    
    print("\nAnalysis complete. Visualization files have been saved.")

if __name__ == "__main__":
    main() 