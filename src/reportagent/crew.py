import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.serper_search_tool import MySerperTool
from tools.hugging_face_search_tool import HuggingFaceSearch
from tools.github_search_tool import GithubSearch
from dotenv import load_dotenv
load_dotenv()



search_tool = MySerperTool()
hugging_face_search_tool = HuggingFaceSearch()
github_search_tool = GithubSearch()

@CrewBase
class ReportagentCrew():
	"""Reportagent crew"""

	llm = LLM(
    model="gemini/gemini-1.5-flash-8b",
    api_key=os.getenv("GEMINI_API_KEY"),
)

	@agent
	def expert_ai_ml_engineer(self) -> Agent:
		return Agent(
			config=self.agents_config['expert_ai_ml_engineer'],
			tools=[search_tool, hugging_face_search_tool, github_search_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			allow_delegation = True, 
			llm=self.llm
		)

	@agent
	def market_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['market_researcher'],
			tools=[search_tool, hugging_face_search_tool, github_search_tool],
			verbose=True,
			allow_delegation = True,
			llm=self.llm
		) 

	@agent
	def product_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['product_researcher'],
			tools=[search_tool, hugging_face_search_tool, github_search_tool],
			verbose=True,
			allow_delegation = True,
			llm=self.llm
		)
	
	@agent
	def resource_manager_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['resource_manager_agent'],
			tools=[search_tool, hugging_face_search_tool, github_search_tool],
			verbose=True,
			allow_delegation = True,
			llm=self.llm
		)
	
	

	@task
	def market_research(self) -> Task:
		return Task(
			config=self.tasks_config['market_research'],
			output_file='market_research.md'
		)
	@task
	def product_research(self) -> Task:
		return Task(
			config=self.tasks_config['product_research'],
			context=[self.market_research()],
			output_file='product.md'
		)
	@task
	def resource_manager(self) -> Task:
		return Task(
			config=self.tasks_config['resource_manager'],
			context=[self.product_research()],
			output_file='resources.md'
		)
	
	@task
	def develop_report(self) -> Task:
		return Task(
			config=self.tasks_config['develop_report'],
			context=[self.market_research(), 
					self.product_research(), 
					self.resource_manager()],

			output_file='report.md'
		)
	

	@crew
	def crew(self) -> Crew:
		"""Creates the Reportagent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)