# Chemical Process Design Agent

A sophisticated agent that uses OpenAI's GPT models and Aspen Plus to design chemical processes based on raw materials and product specifications.

## Overview

This project implements an intelligent agent that:

1. Takes raw materials and desired product specifications as input
2. Designs a chemical process to convert the raw materials into the specified products
3. Simulates the process using Aspen Plus via code-based automation
4. Analyzes simulation results to check if specifications are met
5. Iteratively improves the process design until all specifications are satisfied

The agent uses a design-simulation-feedback loop, leveraging OpenAI's GPT models for expert chemical engineering knowledge and Aspen Plus for rigorous process simulation.

## Project Structure

```
chemical_process_agent/
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   └── prompts.py
├── aspen/
│   ├── __init__.py
│   ├── interface.py
│   ├── simulation.py
│   └── parser.py
├── models/
│   ├── __init__.py
│   ├── materials.py
│   └── specifications.py
└── utils/
    ├── __init__.py
    ├── validation.py
    └── helpers.py
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chemical-process-agent.git
cd chemical-process-agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key and Aspen Plus configuration:
```
OPENAI_API_KEY=your_openai_api_key
ASPEN_PLUS_PATH=C:\Program Files\AspenTech\Aspen Plus V12.0\AspenPlus.exe
```

## Usage

1. Prepare your input files:
   - A JSON file describing raw materials
   - A JSON file describing product specifications

2. Run the agent:
```bash
python main.py --raw-materials path/to/raw_materials.json --specifications path/to/specifications.json
```

3. View the results in the `results` directory.

## Example Input Files

### Raw Materials (`raw_materials.json`):
```json
{
  "materials": [
    {
      "name": "Ethylene",
      "chemical_formula": "C2H4",
      "cas_number": "74-85-1",
      "amount": 100,
      "units": "kg/hr",
      "state": "gas",
      "temperature": 298.15,
      "pressure": 101325
    },
    {
      "name": "Water",
      "chemical_formula": "H2O",
      "cas_number": "7732-18-5",
      "amount": 200,
      "units": "kg/hr",
      "state": "liquid",
      "temperature": 298.15,
      "pressure": 101325
    }
  ]
}
```

### Product Specifications (`specifications.json`):
```json
{
  "specifications": [
    {
      "name": "Ethanol",
      "chemical_formula": "C2H5OH",
      "cas_number": "64-17-5",
      "purity": 0.95,
      "yield_requirement": 0.85,
      "state": "liquid",
      "temperature_range": {
        "min": 298.15,
        "max": 353.15
      },
      "pressure_range": {
        "min": 101325,
        "max": 202650
      }
    }
  ]
}
```

## Features

- **Expert Chemical Process Design**: Leverages GPT models for initial process design based on chemical engineering principles
- **Aspen Plus Integration**: Automates process simulation using Aspen Plus through its COM interface
- **Iterative Optimization**: Continuously improves the process design based on simulation results
- **Comprehensive Analysis**: Checks product specifications, mass and energy balances, and simulation errors
- **Detailed Results**: Saves the entire design history and final optimized process

## Requirements

- Python 3.8+
- OpenAI API key
- Aspen Plus (V12.0 or compatible)
- Windows OS (for Aspen Plus COM automation)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- GitHub: [@maghaeef](https://github.com/maghaeef)
- LinkedIn: [mohammad-aghaee](https://www.linkedin.com/in/mohammad-aghaee/)
- Project Link: [https://github.com/maghaeef/Chemical-Process-Design-Agent](https://github.com/maghaeef/Chemical-Process-Design-Agent)