# Skills Extraction Algorithm

## Development Environment
- Ubuntu 20.04
- Conda

## Project Structure
```
├── .dvc
│   ├── .gitignore 
│   └── config
├── .github
│   └── workflows
│       └── ci.yml
├── requirements
│   ├── dev_requirements.txt
│   └── requirements.txt
├── ssg_sea
│   ├── config
│   │   ├── __init__.py
│   │   ├── core.py
│   ├── data
│   │   ├── .gitignore 
│   │   ├── apps_tools_alias.xlsx.dvc
│   │   ├── output_original_code.csv.dvc
│   │   ├── database.sqlite.dvc 
│   │   └── test_course_data.csv.dvc                                  
│   ├── __init__.py
│   ├── dvc.lock
│   ├── dvc.yaml
│   ├── params.yaml
│   ├── model_card.md
│   ├── VERSION
│   ├── utils.py 
│   ├── load_data.py
│   ├── process_data.py
│   └── extract_skills.py
├── tests        
│   ├── __init__.py          
│   ├── test_load_data.py
│   ├── test_process_data.py
│   └── test_extract_data.py
├── .gitignore
├── MANIFEST.in
├── mypy.ini
├── pyproject.toml
├── README.md
├── environment.yml
└── setup.py
```

# Development

## Create Project Environment

Create Conda environment from yaml

`conda env create -f environment.yml`

Activate the project environment

`conda activate skills-extraction`

## Retrieval of Data/Model Artefact

1. Obtain the access right to the dvc remote repository (contact the dvc repo owner)
2. Execute `dvc pull` in the terminal

## Execute the Model Pipeline

Execute `cd ssg_sea` and then `dvc repro` in the terminal

## Test the code

Execute `pytest` in the terminal

# Packaging the Project

## Package the Code

Execute `python3 -m build` in the terminal

## Upload to PyPI Distribution

Execute `python3 -m twine upload dist/*` in the terminal

## Install the Package from PyPI

Execute `pip install ssg-sea` in the terminal
