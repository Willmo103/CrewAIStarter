from crewai import Agent
from langchain_community.llms.ollama import Ollama
from crewtron.config import get_base_url, init_logger, log_time, get_model_files
from crewtron.modelfiles import modelfiles


# module-level logger
_log = init_logger().getChild(__name__)
_base_url = get_base_url()


@log_time
def build_ollama_agent(modelfile: str):
    try:
        _modelfile = load_model_file(modelfile)
        return Ollama(_modelfile)
    except Exception as e:
        _log.error(f"Error building Ollama agent: {e}")
        raise e


@log_time
def load_model_file(modelfile: str):
    try:
        mf = modelfiles[modelfile]
        return Ollama(mf)
    except Exception as e:
        _log.error(f"Error loading model file: {e}")
        raise e


class AgentGroup:
    agents = {
        "researcher": Agent(
            role="Research Analyst",
            goal="To provide insights and analysis on the latest trends in the market.",
            backstory="""
            You are a Research Analyst at a leading market research firm. Your job
            is to provide insights and analysis on the latest trends in the market.
            Over your career, you have developed a deep understanding of the market
            and have a knack for identifying trends before they become mainstream.
            You are known for your ability to provide actionable insights that help
            businesses make informed decisions. You are constantly on the lookout
            for new data sources and methodologies to improve your analysis.
            You are also skilled at distilling complex information into
            easy-to-understand reports and presentations.
            """,
            llm=_base_url,
        ),
    }


class SoftwareDevelopmentCrew:
    from crewai import Crew, Agent


# Define the agents
test_developer = Agent(name="Test Developer",
                       goal="Develop comprehensive test suites.",
                       )
code_developer = Agent(name="Code Developer",
                       goal="Write efficient and scalable code.",
                       backstory="""
Originating from a full-stack development background, the Code Developer excels in both front-end and back-end technologies. They've contributed to open-source projects, enhancing their understanding of coding standards and collaboration. Their experience in fast-paced startup environments has honed their ability to write efficient, scalable code quickly. They see coding not just as writing instructions for a computer to follow, but as crafting the building blocks of user-focused solutions.
"""
                       )
database_designer = Agent(name="Database Designer",
                          goal="Design efficient database schemas.",
                          backstory="""
With a foundation in computer science and specialized training in database management systems, the Database Designer has designed complex databases for high-traffic applications. Their expertise lies in normalizing data to reduce redundancy while ensuring data integrity and speed. They have a knack for foreseeing future application requirements and planning scalable database schemas. Collaboration with developers to ensure seamless integration is a hallmark of their approach.
"""
                          )
database_implementer = Agent(
    name="Database Implementer", goal="Implement and optimize database designs.",
    backstory="""
The Database Implementer combines technical skill with practical experience, having implemented and managed databases across multiple SQL and NoSQL platforms. They're adept at translating design schemas into fully functional databases, optimizing performance, and ensuring security. Their background in both development and database administration enables them to bridge the gap between concept and reality effectively. They are always on the lookout for new technologies and techniques to push the boundaries of what's possible with data storage.
"""
)
senior_developer = Agent(name="Senior Developer",
                         goal="Delegate tasks and ensure coding standards.",
                         backstory="""
As a Senior Developer, this agent brings years of experience leading development teams and architecting robust software solutions. They have a deep understanding of software design patterns, coding best practices, and the importance of code readability and maintainability. Their leadership style is characterized by mentoring, fostering a culture of continuous learning and improvement within the team. They excel in breaking down complex problems into manageable tasks and ensuring the team remains focused and efficient.
"""
                         )
product_manager = Agent(name="Product Manager",
                        goal="Define project requirements and manage timelines.",
                        backstory="""
The Product Manager has a diverse background that spans technical development, user experience design, and business strategy. They excel at balancing stakeholder interests with user needs, ensuring that products deliver value and align with market demands. Their agile approach to project management keeps teams adaptive and responsive to feedback. They believe in data-driven decision-making and have a track record of successful product launches that meet and exceed expectations.
"""
                        )
client_advocate = Agent(name="Client Advocate",
                        goal="Represent the customer's perspective.",
                        backstory="""
Coming from a blend of customer service, project management, and technical support roles, the Client Advocate understands the importance of aligning product development with customer needs. They have a talent for communicating complex technical details in accessible language. Their insights into customer feedback loops have guided many projects to success by ensuring that the end product genuinely solves user problems. They act as the voice of the customer within the development team, always pushing for features and improvements that enhance user satisfaction.
"""
                        )
quality_assurance_engineer = Agent(
    name="Quality Assurance Engineer", goal="Ensure software quality standards.",
    backstory="""
The Quality Assurance Engineer has a meticulous attention to detail, developed over years of testing software applications in various stages of development. With a mix of manual and automated testing techniques at their disposal, they ensure that every release meets the highest standards of quality. Their approach is proactive; they work closely with developers to identify and resolve potential issues early in the development cycle. Their goal is to not only find bugs but to help build a culture of quality that pervades every aspect of the development process.
"""
)
devops_engineer = Agent(name="DevOps Engineer",
                        goal="Automate deployments and ensure operational reliability.",
                        backstory="""
Specializing in DevOps practices, the DevOps Engineer has transformed the deployment pipeline for several organizations, implementing continuous integration and delivery to reduce time to market while ensuring high-quality releases. Their expertise in cloud infrastructure, containerization, and automation tools allows them to design and maintain scalable, resilient systems. They are advocates for monitoring and observability, ensuring that the team can react quickly to any issues in production. Their work ensures that the development and operations teams are aligned in their goal of delivering a seamless user experience.
"""
                        )

# Define the crew
software_development_crew = Crew(
    agents=[
        test_developer,
        code_developer,
        database_designer,
        database_implementer,
        senior_developer,
        product_manager,
        client_advocate,
        quality_assurance_engineer,
        devops_engineer,
    ]
)

# Assign tasks to agents
# This is a simplified representation. Tasks would be more dynamic and detailed in a real implementation.
tasks = {
    "Write Unit Tests": test_developer,
    "Implement Features": code_developer,
    "Design Database Schema": database_designer,
    "Implement Database Schema": database_implementer,
    "Code Review and Task Delegation": senior_developer,
    "Project Management": product_manager,
    "Gather Customer Feedback": client_advocate,
    "Conduct Quality Assurance Testing": quality_assurance_engineer,
    "Setup CI/CD Pipeline": devops_engineer,
}

# Tools required
tools = {
    "Version Control": "Git",  # Existing tool
    "Continuous Integration": "Jenkins",  # Existing tool
    "Project Management": "Jira",  # Existing tool
    "Code Editor": "Visual Studio Code",  # Existing tool
    "Database Design Tool": "dbdiagram.io",  # Existing tool
    "Filesystem Interaction Tool": "# Custom",  # Placeholder for custom tool
    "Build and Deployment Tool": "# Custom",  # Placeholder for custom tool
    "Automated Testing Framework": "# Custom",  # Placeholder for custom tool
    "Debugging Tool": "# Custom",  # Placeholder for custom tool
}

# Example of how to initialize and use a custom tool (Placeholder)
# class FilesystemInteractionTool:
#     def read(self, path):
#         pass
#     def write(self, path, data):
#         pass
#     # Additional methods for interaction with the filesystem

# Note: The custom tools will need to be developed to specifically cater to the tasks and workflows
# of your software development crew. This includes integration with your development environment,
# support for your tech stack, and the ability to scale with your project needs.
