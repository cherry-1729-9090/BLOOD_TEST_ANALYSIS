from medical_crew import MedicalCrew
import json

def simulate_interaction(agent, input_data, expected_output):
    try:
        # Call the appropriate method based on the agent's role
        if agent.role == 'Blood Test Analyst':
            agent_output = agent.analyze_report(input_data)
        elif agent.role == 'Medical Research Specialist':
            agent_output = agent.conduct_research(input_data)
        elif agent.role == 'Holistic Health Advisor':
            agent_output = agent.provide_recommendations(input_data)
        else:
            raise Exception(f"Unknown role: {agent.role}")
        
        # Compare agent output with expected output
        if agent_output != expected_output:
            print(f"Agent '{agent.role}' output did not match expected output.")
        else:
            print(f"Agent '{agent.role}' produced the expected output.")
    
    except AttributeError:
        raise Exception(f"Agent '{agent.role}' does not have the required method to process the input.")

def save_agent_config(agents, filename):
    agent_configs = []
    for agent in agents:
        agent_configs.append({
            'role': agent.role,
            'goal': agent.goal,
            'backstory': agent.backstory,
            # Removed 'expected_output' since it's not an attribute of the agents
        })
    
    with open(filename, 'w') as f:
        json.dump(agent_configs, f)
    
    print(f"Agent configurations saved to {filename}.")

def train_agents(n_iterations, filename):
    crew = MedicalCrew().crew()
    
    try:
        # Simulate training interactions
        for _ in range(n_iterations):
            for agent in crew:
                # Define input data and expected output for training
                input_data = {"dummy_data": "example"}  # Replace with actual input data
                expected_output = "expected_output_example"  # Replace with actual expected output
                
                simulate_interaction(agent, input_data, expected_output)
        
        # Save the agent configurations
        save_agent_config(crew, filename)
        
        print(f"Training completed successfully. Agent configurations saved to {filename}.")
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

if __name__ == "__main__":
    # Specify the number of iterations and output filename
    n_iterations = 5000000  # Adjust as necessary
    filename = "trained_agents_config.json"  # Output file for trained agents configuration
    
    # Start training
    train_agents(n_iterations=n_iterations, filename=filename)
