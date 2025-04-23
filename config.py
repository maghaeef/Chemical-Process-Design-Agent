import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # From .env file
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

# Aspen Plus configuration
ASPEN_PLUS_PATH = os.getenv("ASPEN_PLUS_PATH", r"C:\Program Files\AspenTech\Aspen Plus V12.0\AspenPlus.exe")
SIMULATION_TEMPLATE_PATH = os.getenv("SIMULATION_TEMPLATE_PATH", "./templates/base_simulation.bkp")

# Agent configuration
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))