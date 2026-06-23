# Cafe-App-Mini-Project
A lightweight, local data processing application developed as part of the **Generation UK Data Engineering Practitioner** program. This project simulates the foundational elements of data collection, file handling, and structured data manipulation for a local cafe business.

## Project Overview
The objective of this project was to transition a cafe's operational data from raw text files into formatted, manageable data structures using core programming and database principles. This application served as the initial building block for understanding data ingestion, system state management, and localized data processing entirely on a local machine.

### Key Features Developed:
* **Data Ingestion & Persistence:** Developed robust file-handling logic to cleanly load, read, and write product, courier, and order datasets using local text and CSV files.
* **Menu & Order Management:** Built an interactive command-line interface allowing users to dynamically add, view, update, and remove items across related data lists.
* **Structured Coding Foundations:** Applied Object-Oriented Programming (OOP) principles to ensure data models remained modular, scalable, and reusable.
* **Defensive Programming:** Implemented data validation logic and exception handling to prevent application crashes from invalid user inputs.
* **Version Control:** Managed the development lifecycle using Git branching strategies, semantic commits, and repository synchronization via GitHub.

---

## Tech Stack & Foundations
* **Language:** Python
* **Data Storage:** Local Text Files, CSV Data Formats
* **Methodology:** Object-Oriented Programming (OOP), Unit Testing, Agile/Scrum sprint frameworks

---

## Future Improvements & Learning Outcomes
Reflecting on the functional and structural boundaries of this localized application, future iterations of this system will focus on transitioning from a script-based tool to an automated, cloud-hosted architecture:

### 1. Migrating to a Relational Database Tier
* **Current State:** Data is parsed and stored in flat local files, requiring custom search and update logic.
* **Future Change:** Integrate a dedicated relational database management system (such as PostgreSQL). Normalize the data structures up to 3rd Normal Form (3NF) to enforce data integrity and eliminate redundancy.

### 2. Transitioning to Cloud Storage and Warehousing
* **Current State:** Storage is limited to the local host machine's file system.
* **Future Change:** Scale the system by migrating storage to a cloud data lake (such as Amazon S3) for raw file ingestion, and routing processed data into a cloud data warehouse (such as Amazon Redshift) to support large-scale analytical queries.

### 3. Automated Event-Driven Processing
* **Current State:** Data transformations and operations rely on manual user execution via the terminal interface.
* **Future Change:** Redesign the application into an automated ETL/ELT pipeline. Utilize serverless cloud compute (such as AWS Lambda) combined with event triggers to automatically ingest, clean, and load data files the moment they are generated.

### 4. Application Containerization
* **Current State:** The script depends on the specific Python environment configured on the local host machine.
* **Future Change:** Containerize the application using Docker and Docker Compose to isolate dependencies, ensuring the script runs consistently across any development or production environment.
