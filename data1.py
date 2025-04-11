import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
# Define task types
task_types = [
    "3D Model", "3D Render", "Conceptual Design", "Construction Document",
    "Custom Millwork & Joinery Drawing", "Design Development", "Door & Window Schedule",
    "Elevation Drawing", "Finish Schedule", "Floor Plan", "Furniture Layout Plan",
    "General Specification", "Hardscape Plan", "Interior Layout Plan", "Landscape Plan",
    "Lighting & Fixture Plan", "Material Board", "Partition Plan", "Permit Drawing",
    "Reflected Ceiling Plan", "Roof Plan", "Schematic Design", "Section Drawing",
    "Site Plan", "Technical Specification", "Virtual Reality", "Zoning & Building Code Compliance",
    "Others"
]

# Define realistic architectural tasks
task_templates = [
    ("3D Model Development", "Create a detailed 3D model for the client’s new residential project."),
    ("Render Finalization", "Enhance the 3D renders for the commercial building's presentation."),
    ("Conceptual Design Drafting", "Prepare an initial concept sketch for the urban park renovation."),
    ("Construction Documentation", "Compile detailed construction drawings for city permit approval."),
    ("Custom Joinery Design", "Develop detailed joinery drawings for the interior fit-out project."),
    ("Facade Elevation Detailing", "Finalize the detailed elevation drawings for the high-rise building."),
    ("Interior Layout Planning", "Optimize space planning for the luxury apartment interior."),
    ("Lighting Plan Design", "Create a lighting and fixture layout for the retail store."),
    ("Material Selection & Specification", "Curate materials and finishes for the sustainable home project."),
    ("Site Plan Drafting", "Prepare a site plan layout considering zoning and access."),
    ("Structural Coordination", "Coordinate with the structural engineer for beam placements."),
    ("Permit Drawing Submission", "Prepare and submit permit drawings for approval."),
    ("Landscape Design Refinement", "Enhance the planting layout for the residential garden."),
    ("Technical Specifications", "Compile technical specifications for the construction phase."),
    ("Hardscape Design Execution", "Design outdoor paving and seating areas for the commercial plaza."),
     ("Zoning Compliance Review", "Analyze local zoning regulations to ensure the proposed design aligns with building codes."),
    ("Virtual Reality Walkthrough", "Develop an immersive VR experience for client presentation of the office interior."),
    ("Door & Window Schedule Drafting", "Create a detailed schedule for all doors and windows in the hospitality project."),
    ("Partition Plan Finalization", "Define internal partitioning layouts for the healthcare facility."),
    ("Finish Schedule Compilation", "List all interior finishes including floors, walls, and ceilings for the commercial space."),
    ("Furniture Layout Finalization", "Plan and position loose and built-in furniture for the co-working office."),
    ("Reflected Ceiling Plan Drafting", "Draft the reflected ceiling plan including lighting and HVAC elements."),
    ("General Specification Draft", "Prepare general notes and material specifications for tender documents."),
    ("Schematic Design Iteration", "Refine the schematic design for feedback from the stakeholders."),
    ("3D Massing Model", "Create a conceptual massing model to test building envelope limitations."),
    ("Design Coordination Meeting", "Meet with MEP consultants to ensure design integration across disciplines."),
    ("Code Compliance Report", "Prepare a summary document addressing fire, accessibility, and egress codes."),
    ("Construction Site Visit", "Visit the site to verify dimensions before construction begins."),
    ("Roof Plan Drawing", "Detail the slope, drainage, and roofing system layout for the warehouse."),
    ("Sustainability Assessment", "Evaluate building materials and systems for LEED compliance."),
    ("MEP Clash Detection", "Run a clash detection session between MEP and architectural models."),
    ("Custom Fixture Detailing", "Design custom-built washbasin counters for the hotel suites."),
    ("As-Built Drawing Preparation", "Update drawings to reflect actual built conditions post-construction."),
    ("Interior Material Board Creation", "Prepare a presentation board with fabric, finish, and texture samples."),
    ("Client Feedback Revisions", "Implement client-requested changes into the design presentation."),
    ("Bid Package Compilation", "Organize all documents needed for contractor bidding."),
    ("Detail Section Drawing", "Draw enlarged sections through complex junctions in the facade."),
    ("Building Performance Analysis", "Assess daylighting and thermal performance using simulation tools."),
    ("Green Roof Plan Development", "Design the planting and drainage system for the green roof."),
    ("Accessibility Audit", "Review floor plans for compliance with accessibility standards.")
]

priority_levels = ["Low", "Neutral", "High"]


# Function to generate the dataset with match_score ranging from 0.8 to 1.0 across all priority levels
def generate_dataset(num_samples=4200):
    data = []
    for _ in range(num_samples):
        title, description = random.choice(task_templates)
        type_of_task = random.choice(task_types)
        
        # Random priority selection without biasing "High"
        priority_level = random.choice(priority_levels)
        
        due_date = datetime.today() + timedelta(days=random.randint(1, 30))
        workload = random.randint(1, 10)

        # Simulate avg_quality_score to be in the range [0.8, 1.0] with higher chance for high quality
        avg_quality_score = round(np.random.beta(2, 5), 2)  # Higher probability towards 1.0 (from 0.0 to 1.0)
        
        # Adjust match_score generation to favor higher values (closer to 1.0)
        match_score = 0.0

        # Boost match score if task type matches preferred task
        preferred_task = random.choice(task_types)
        if type_of_task == preferred_task:
            match_score += 0.3  # Match between task and preferred task adds some bonus

        # Adjust match score based on priority level (less skewed, but still present)
        if priority_level == "High":
            match_score += 0.3  # High priority gives a slight boost
        elif priority_level == "Neutral":
            match_score += 0.2  # Neutral priority gives a smaller boost
        elif priority_level == "Low":
            match_score += 0.1  # Low priority gives a minimal boost

        # Adjust match score based on average quality score
        match_score += 0.2 * (avg_quality_score)  # Ensure avg_quality_score boosts match score

        # Normalize match score to be between 0 and 1
        match_score = min(match_score, 1.0)

        # Append the generated data
        data.append([ 
            title, description, type_of_task, priority_level, due_date.strftime('%Y-%m-%d'), workload,
            round(avg_quality_score, 2), preferred_task, round(match_score, 2)
        ])

    columns = [
        "title", "description", "type_of_task", "priority_level", "due_date", "workload",
        "avg_quality_score", "preferred_task", "match_score"
    ]
    return pd.DataFrame(data, columns=columns)

# Generate the dataset
df = generate_dataset(4200)

# Save to CSV
th_file_path = "backend/data/low.csv"
df.to_csv(th_file_path, index=False)

th_file_path
