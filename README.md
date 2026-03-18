# Airflow Training Resources

This repository contains materials for an Apache Airflow training course, including hands-on labs, code examples, and a presentation (available in Google Slides). 

## Content

- **modules:** This directory contains code examples demonstrating various Airflow concepts and features, organized by module.
- **labs:** This directory contains guided lab exercises that allow you to apply your Airflow knowledge in practical scenarios.
- **infra:** This directory contains Terraform scripts for provisioning the infrastructure needed for the training (e.g., an Airflow instance).

## Getting Started

### Prerequisites

- **Git:** Make sure you have Git installed on your system.
- **Python 3.8 or higher:** Airflow requires Python 3.8 or above.
- **Poetry:** We'll use Poetry for dependency management.

### Setup Instructions

1. **Clone the repository:**
   ```bash
   cd ~
   git clone https://github.com/siudzinskim/airflow-training.git
   cd airflow-training
   ```

2. **Install Poetry (if not already installed):**
   ```bash
   sudo pip install poetry
   ```

3. **Install project dependencies:**
   ```bash
   cd ~/airflow-training
   poetry install
   ```

4. **Add k8s config:
   ```bash
   mkdir ~/.kube/
   microk8s  microk8s config > ~/.kube/config
   microk8s enable hostpath-storage
   ```
   
5. **Open VSCode and a terminal in VSCode window:**
   - You can usually find this under the "Terminal" tab in main menu (Ctrl+Shift+`).

6. **Navigate to the `infra` folder:**
   ```bash
   cd infra
   ```

7. **Run Terraform:**
   ```bash
   terraform init
   terraform plan 
   terraform apply
   ```
   - Review the output of `terraform plan` carefully before applying the changes.

