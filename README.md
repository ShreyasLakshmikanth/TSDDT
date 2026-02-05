# Thruster Selection Database and Decision Tool (Mini Demo)

## Overview
This tool is a Python-based analytical system designed to automate the selection phase of the right Thrusters. By combining physical mission requirements with a curated database of thrusters, the tool calculates the **Total System Mass** (Satellite + Thruster + Propellant) to identify the most mass-efficient solution for a specific mission profile.

## Core Features
* **Automated Physics Engine:** Implements the **Tsiolkovsky Rocket Equation** to calculate required propellant mass based on mission Delta-V and thruster Specific Impulse.
* **System-Level Analysis & Constraint Filtering:** Evaluates and automatically excludes thrusters that exceed the satellite’s available power budget.
* **Viewed Analytics:** Provides a step-by-step mathematical breakdown of how the final mass for each candidate was derived.

---

## Technical Implementation

### Data Format: JSON
***<i>I selected JSON as the data exchange format because it is the industry standard for aerospace APIs, ensuring the catalog is natively readable by almost all programming languages (Python, C++, MATLAB). It offers the flexibility to store non-uniform thruster specifications in hierarchical structures without the rigidity of a flat spreadsheet, while remaining text-based for easy version control via Git.</i>***

### Framework: Argparse (CLI)
***<i>The tool utilises the Argparse library to provide a professional Command Line Interface. This framework was chosen for its efficiency, allowing mission designers to iterate rapidly through scenarios without modifying source code, and its robust input validation that ensures mission parameters are mathematically sound before calculations begin.</i>***

---

## How it Works: The "Invisible" Calculation
The tool doesn't just "match" inputs; it performs an architectural trade-off. 
1. **The Power Gate:** It checks if the thruster's **Operating Power (W)** fits within the satellite's power plant capacity.
2. **The Fuel Penalty:** It calculates the "hidden" mass of the propellant. While a thruster may be light, its low efficiency results in a heavy fuel tank.
3. **The Ranking:** Thrusters are ranked by the **Total Launch Mass**, which is the most critical cost-driver in satellite deployment.

---

## Future Scaling & Evolution
***<i>To scale this to a much larger catalog and richer criteria, I would migrate to a PostgreSQL backend using JSONB features to handle thousands of entries with high-performance filtering. I would also expand selection criteria to include Volume Analysis (CubeSat U-size), TRL filtering for risk management, and Thermal Note analysis to ensure the satellite can dissipate waste heat.</i>***

1. **Database Migration (PostgreSQL):**
    * Migrate to a relational database to manage complex relationships between thrusters, compatible propellants, and Power.
    * Utilize **PostgreSQL's JSONB** features to maintain the flexibility of JSON while gaining the search performance and data integrity of a SQL backend.
2. **Expanded Selection Criteria:**
    * **Volume Analysis:** Integrate physical dimensions to check if the system fits within standard CubeSat volumes.
    * **TRL Filtering:** Add "Technology Readiness Level" constraints to filter by "flight-proven" vs. "experimental" hardware.
    * **Thermal Note:** Analyse waste heat to ensure the satellite's thermal control can dissipate the load.
3. **User Experience & Analysis:**
    * **Frontend UI:** Build a decent, web-based UI for the near future to make the tool accessible to non-programming mission architects.
    * **Multi-Objective Optimization:** Implement Pareto-front visualisations to balance the trade-off between certain constraints.

---

## Usage
Run the script via terminal using the following flags:
```bash
python3 main.py --dv [delta-v in m/s] --power [max watts] --mass [sat dry mass in kg]
```

**Example:**
```bash
python3 main.py --dv 500 --power 1500 --mass 100
```
