# UDA-Q Agent (Universal AI Data Quality Evaluator)
A multi-agent AI system that evaluates, detects, fixes, and validates data-quality issues automatically using LLM-powered agents and ADK-Python orchestration.
<img width="1024" height="338" alt="image" src="https://github.com/user-attachments/assets/3e12c4d2-c64b-4069-8246-cff0d0dc27b7" />

# Overview
The UDA-Q Agent (Universal AI Data Quality Evaluator & Auto-Fixer) is a multi-agent AI system designed to automatically inspect, detect, fix, validate, and improve data quality using the Agent Development Kit (ADK) and Google Gemini.
This project solves one of the biggest real-world challenges in data work: poor-quality data that reduces the accuracy, reliability, and performance of analytics, machine learning models, and AI systems.

In today’s world, companies use large amounts of structured and unstructured data, but most of it contains issues like missing values, wrong formats, duplicates, inconsistent labels, outliers, and human entry mistakes. Fixing these manually takes a lot of time, and even a small mistake can corrupt an entire dataset.
The UDA-Q Agent automates this entire process in an intelligent, scalable, and explainable way.

# 1. Problem Statement

Organizations face multiple data quality issues:

Missing values

Outliers and noise

Wrong data types

Inconsistent formatting

Spelling mistakes

Duplicates

Schema mismatches

Unstandardized categories

Outdated or conflicting records

These errors cost businesses time, money, and accuracy.
Traditional data cleaning tools are rule-based and require expert knowledge. They also don’t scale well and cannot adapt to different datasets.

To solve this, I built the UDA-Q Agent, an AI-driven system that automatically evaluates and fixes data quality issues using multi-agent collaboration and LLM reasoning. It is fully automated, adaptive, and built for enterprise-grade workflows.
# 2. Why Agents?

Agents are the perfect solution for this problem because they can:

✓ Break down complex workflows into specialized tasks

Each agent handles one part of the pipeline: inspection, planning, fixing, and validation.

✓ Run independently and collaborate through A2A Protocol

They communicate structured outputs with no confusion.

✓ Use long-running operations for large datasets

If a dataset is big, agents can pause/resume without losing context.

✓ Use memory to track decisions, logs, and corrections

Makes debugging and auditing easier.

✓ Tools integration

Agents can use:

Code Execution

MCP tools

Custom cleaning tools

Built-in Google Search

External APIs (OpenAPI tool support)

This multi-agent approach is scalable, modular, and works for any dataset type.

# Architecture

The UDA-Q Agent follows a multi-agent architecture coordinated by an orchestration layer:

1. Inspector Agent

Scans the dataset

Detects problems like missing values, duplicates, type mismatches, invalid categories, outliers, inconsistencies

Creates a structured error report

Computes initial data-quality metrics

2. Planner Agent

Reads the Inspector’s report

Designs a full repair plan

Chooses the best techniques for each issue (imputation, normalization, deduplication, regex correction, formatting rules, etc.)

Prioritizes steps in a logical order

Generates a reproducible plan for the Fixer

3. Fixer Agent

Executes the repair plan step-by-step

Applies transformations using LLM reasoning + code execution

Automatically resolves errors such as:

Missing values (ML-based or rule-based imputation)

Incorrect formats (date, numbers, strings)

Noisy text corrections

Outlier handling

Duplicate removal

Schema corrections

Produces a cleaned dataset

4. Validator Agent

Re-evaluates the cleaned dataset

Calculates post-cleaning metrics

Confirms improvement over baseline

Generates a final Data Quality Score

Outputs a readable summary and audit log

Orchestration Layer

The system is coordinated using:

ADK-Python framework

A2A (Agent-to-Agent) protocol

This enables:

Sequential and parallel agent execution

Tool calling (code interpreter, custom functions, external APIs)

Consistent context sharing

Reproducible workflows

Built-in memory and session control

This layer ensures communication between agents happens in a structured and trustworthy manner.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/d092be6f-80f7-4fd4-8c13-7057abd2c16d" />
# Key Features
✔ Fully Automated Data Cleaning

No manual steps required—upload a dataset and the entire pipeline runs autonomously.

✔ Modular Multi-Agent Design

Each agent is specialized, improving accuracy and transparency.

✔ Domain-Agnostic

Works with datasets from:

Finance

Healthcare

Retail

Social media

Education

E-commerce

Research

IoT

✔ Intelligent Fix Generation

Uses LLM reasoning to choose the best cleaning method dynamically.

✔ Validated & Audited Output

System generates:

Before/after metrics

Final quality score

Repair logs

Human-readable summaries

✔ Supports Multiple Data Formats

CSV, Excel, JSON, SQL tables, etc.

Example Workflow

User uploads a dataset
<img width="1915" height="969" alt="Screenshot 2025-11-22 145813 - Copy" src="https://github.com/user-attachments/assets/73d276d5-b8ce-4558-84c6-20d4c8a60c95" />

Inspector Agent scans dataset and finds issues
Planner Agent creates a detailed repair strategy
Fixer Agent applies all transformations automatically
Validator Agent checks results and produces a final score
System returns cleaned dataset + quality report
<img width="1917" height="996" alt="Screenshot 2025-11-22 151135" src="https://github.com/user-attachments/assets/2bd0774d-b21a-419f-8e46-652c0a5019df" />
<img width="1899" height="837" alt="Screenshot 2025-11-22 151123 - Copy(1)" src="https://github.com/user-attachments/assets/35e07b85-15cf-4962-a649-5c4170ead3d8" />

# 📦 Tech Stack

Python 3.10+
Django
React.js
ADK-Python (Agent Development Kit)
A2A Protocol (Agent-to-Agent communication)
Pandas / NumPy

LLM reasoning + tool execution
## Prerequisites
- Python 3.8+
- Node.js 16+

## Setup Instructions

### Backend (Django)
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/`.

### Frontend (React)
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

# Why This Project Matters

Data is the backbone of digital transformation and AI systems. Poor-quality data directly impacts:

Decision-making
Operational efficiency
ML model accuracy
Revenue predictions
Compliance & reporting

UDA-Q empowers organizations with a powerful AI-driven system that ensures their data is clean, accurate, and ready for downstream tasks—instantly and reliably.

# Conclusion

The UDA-Q Agent is a next-generation, intelligent, automated data-quality system built using multi-agent orchestration and LLM-powered reasoning. It transforms noisy, inconsistent datasets into high-quality, analysis-ready data—without manual effort. Its ability to universally detect, fix, validate, and score data-quality issues makes it a powerful tool for any business or individual working with data.
