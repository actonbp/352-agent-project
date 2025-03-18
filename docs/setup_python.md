# Setting Up Python for Team Simulations

This guide will walk you through setting up Python and installing all the necessary packages to run team simulations on your computer.

## Prerequisites

Before you begin, you'll need:

- A computer running Windows, macOS, or Linux
- Internet connection
- Admin/installation privileges on your computer
- An OpenAI API key (for simulations)

## Step 1: Install Python

### Windows

1. Visit [python.org](https://www.python.org/downloads/windows/)
2. Download the latest Python 3.9+ installer (64-bit recommended)
3. Run the installer
4. **Important**: Check the box "Add Python to PATH" during installation
5. Click "Install Now"

### macOS

1. Visit [python.org](https://www.python.org/downloads/macos/)
2. Download the latest Python 3.9+ installer
3. Run the installer and follow the instructions
4. Verify installation by opening Terminal and typing: `python3 --version`

### Linux

Most Linux distributions come with Python pre-installed. To check your version, open Terminal and type:
```
python3 --version
```

If you need to install Python:
```
sudo apt update
sudo apt install python3 python3-pip
```

## Step 2: Setting Up a Virtual Environment (Recommended)

Virtual environments keep your project dependencies separate from other Python projects.

### Windows

Open Command Prompt and run:
```
python -m venv team_sim_env
team_sim_env\Scripts\activate
```

### macOS/Linux

Open Terminal and run:
```
python3 -m venv team_sim_env
source team_sim_env/bin/activate
```

You'll see `(team_sim_env)` at the beginning of your command line, indicating the environment is active.

## Step 3: Clone the Repository

### Install Git

#### Windows
1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default options

#### macOS
1. Open Terminal and run: `xcode-select --install`
2. Follow the prompts to install Git

#### Linux
```
sudo apt update
sudo apt install git
```

### Clone the Repository

In your command line (with virtual environment activated):
```
git clone https://github.com/actonbp/352-agent-project.git
cd 352-agent-project
```

## Step 4: Install Required Packages

With your virtual environment activated, install the required packages:
```
pip install -r requirements.txt
```

This will install:
- CrewAI: For agent-based simulations
- Pandas: For data handling and analysis
- Matplotlib & Seaborn: For data visualization
- Other dependencies

## Step 5: Set Up Your OpenAI API Key

1. Sign up for an OpenAI account at [platform.openai.com](https://platform.openai.com/signup)
2. Navigate to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
3. Create a new API key and copy it
4. Create a file named `.env` in the root directory of the project
5. Add your API key to the file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

⚠️ **Important**: Never share your API key or commit it to public repositories.

## Step 6: Verify Your Setup

Create a simple test script called `test_setup.py`:
```python
import os
from dotenv import load_dotenv
import crewai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load environment variables
load_dotenv()

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ API key found")
else:
    print("❌ API key not found. Check your .env file")

# Check package imports
print("✅ All packages imported successfully")

print("Setup complete! You're ready to run team simulations.")
```

Run the test script:
```
python test_setup.py
```

If everything is set up correctly, you should see success messages.

## Common Issues and Solutions

### "Module not found" error
```
pip install <missing_module_name>
```

### Permission errors on installation
Try running your command prompt or terminal as administrator/sudo.

### Virtual environment not activating
On Windows, you may need to run:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### API key not being recognized
Make sure:
- Your `.env` file is in the correct location
- You've spelled "OPENAI_API_KEY" correctly
- You're running your script from the project directory
- You're using `load_dotenv()` before accessing the API key

## Running Your First Simulation

Once setup is complete, try running a simple simulation:

1. Navigate to the examples directory:
   ```
   cd examples
   ```

2. Run the leadership simulation example:
   ```
   python leadership_simulation.py
   ```

This will run a quick simulation and generate results in the `data/results` directory.

## Next Steps

Now that your environment is set up, check out these resources:

- [Leadership Simulation Guide](leadership_simulation_guide.md)
- [Diversity Simulation Guide](diversity_simulation_guide.md)
- [Analyzing Results Guide](analyzing_results_guide.md)
- [Research Question Guide](research_question_guide.md)

## Getting Help

If you encounter any issues:

1. Check the [GitHub Discussions](https://github.com/actonbp/352-agent-project/discussions) page for solutions
2. Search for error messages online
3. Ask for help during office hours or on the course forum 