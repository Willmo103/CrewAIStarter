from coding.coding_agents import CodingAgents as ca
from crewai import task
import from coding_tools import BasicTools, DockerTools


planning_tools = [
    BasicTools.ask_question,
    BasicTools.get_current_date,
    BasicTools.save_output, # TODO: set a cache directory as a default location for saving output
]
# TODO: creat a cache directory in the setup of the project

define_stack_tools = [
    BasicTools.ask_question,
    BasicTools.save_output,
    DockerTools.build_image,
]

setup_environments_tools = [
    DockerTools.write_code,
    DockerTools.run_code,
]

databse_tools = [
    DockerTools.write_code,
    DockerTools.run_code,
]

update_docker_env_tools = [
    DockerTools.build_image,
]

class CodingTasks:
    project_planning = task.Task(
        agent=ca.product_manager,
        tools=[],
        goal="To produce an outline, workflow, and user stories",
        expected_output="""
        A document detailing the project outline, workflow, and user stories

        Example:
        # Project Summary

        ## Outline
        The project will consist of...

        ## Workflow
        - Step 1: ...
        - Step 2: ...

        ## User Stories
        - As a [type of user], I want [an action] so that [benefit].
        """,
    )

    define_stack = task.Task(
        agent="",
        tools=[],
        goal="To decide on the technology stack and successfully create a docker environment",
        expected_output="""
        A YAML document describing the technology stack and environment setup,
        a set of instructions and files for creating the environemt and installing the dependencies.
        a dockerfile to initialize the environment.

        Example:
        ```yaml
        language: Python
        framework: Django
        database: PostgreSQL
        ci_cd: Jenkins
        ```
        """,
    )

    create_database_schema = task.Task(
        agent=ca.database_designer,
        tools=[],
        goal="To design and create the database schema, and test its efficiency",
        expected_output="""
        A database schema with efficient normalization and indexing, and a test
        report on its performance and integrity.

        Example:
        - Schema: Tables and relationships defined with creation scripts written.
        - Test Report: Performance and integrity tests passed.
        """,
    )

    setup_environments = task.Task(
        agent="",
        tools=[],
        goal="To prepare all necessary environments including CI/CD pipelines",
        expected_output="""
        Fully configured development, testing, and production environments

        Example:
        - Development environment setup at dev.example.com
        - Testing environment available at test.example.com
        - Production deployed to prod.example.com
        - CI/CD pipeline configured for automatic testing and deployment
        """,
    )

    pair_programming = task.Task(
        agent="",
        tools=[],
        goal="To implement and test a new feature",
        expected_output="""
        Feature implementation with passing tests, integrated into the codebase

        Example:
        - Feature: User login functionality
        - Tests: 5 tests, all passing
        - Codebase: Integrated into branch `feature/user-login`
        """,
    )

    code_review = task.Task(
        agent="",
        tools=[],
        goal="To review the code for quality and readiness",
        expected_output="""
        Approved code ready for integration into the main project branch

        Example:
        - Code Review Report: All standards met, ready for merge into `main`
        """,
    )

    documentation = task.Task(
        agent="",
        tools=[],
        goal="To create and update documentation",
        expected_output="""
        A comprehensive set of documents that describe the functionality, architecture, and usage of the software

        Example:
        - API Documentation: Available at /docs/api
        - User Manual: Included in /docs/user-manual.pdf
        - Code Comments: Throughout the codebase for key functions
        """,
    )

    crash_report_handling = task.Task(
        agent="",
        tools=[],
        input="Error logs and crash reports",
        goal="To analyze crash reports and prioritize them for fixing",
        expected_output="""
        A detailed crash analysis report, including steps for reproduction, affected components, and severity assessment

        Example:
        - Issue: Memory leak in the data processing module
        - Severity: High
        - Steps to Reproduce: Described in the report
        """,
    )

    post_mortem_report = task.Task(
        agent="",
        tools=[],
        goal="To conduct a thorough review of the incident",
        expected_output="""
        A post-mortem report outlining the cause of the incident, the response actions taken, lessons learned, and recommended changes to processes or systems

        Example:
        - Incident: Database outage on 2023-05-20
        - Cause: Failed database migration
        - Actions Taken: Rollback to previous version, data recovery procedures initiated
        - Lessons Learned: Need for better testing of migration scripts
        """,
    )

    feature_enhancement_proposal = task.Task(
        agent="",
        tools=[],
        goal="To evaluate and propose enhancements",
        expected_output="""
        A proposal document detailing the rationale, expected benefits, and implementation plan for the feature enhancement

        Example:
        - Proposal: Add voice command feature
        - Rationale: Increasing demand for hands-free operation
        - Benefits: Improved accessibility, user satisfaction
        - Implementation Plan: Detailed in the proposal document
        """,
    )

    security_audit = task.Task(
        agent="",
        tools=[],
        goal="To identify and assess security vulnerabilities",
        expected_output="""
        A security audit report highlighting vulnerabilities, risk levels, and recommendations for mitigation

        Example:
        - Vulnerabilities: Listed with descriptions
        - Risk Levels: High, Medium, Low
        - Recommendations: Specific actions for each identified vulnerability
        """,
    )

    performance_optimization = task.Task(
        agent="",
        tools=[],
        goal="To improve the performance of the software",
        expected_output="""
        A set of optimized code changes, configuration adjustments, and an updated performance benchmark report

        Example:
        - Performance Issue: Slow response time in the search functionality
        - Optimization: Indexing database tables, query optimization
        - Benchmark: Response time improved from 5s to 0.5s
        """,
    )

    update_dev_env = task.Task(
        agent="",
        tools=[],
        goal="To update the development environment with a new Dockerfile",
        expected_output="""
        A new Docker environment with the updated configuration and dependencies

        Example:
        - Dockerfile: Updated with new dependencies
        - Environment: Rebuilt and running with the latest changes
        """,
    )
