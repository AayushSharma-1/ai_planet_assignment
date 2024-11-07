from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv(r'reportagent\src\reportagent\.env')

import os, json, requests

class GithubSearchTool(BaseModel):
    """Input schema for GithubSearchTool."""
    argument: str = Field(..., description="It is the keyword for which you want to search the dataset or repository or any other releated thing on Github, make sure your keyword is general in nature should not specifically refer to a company / organization or a person. ")

class GithubSearch(BaseTool):
    name: str = "github_search_tool"
    description: str = (
        "This tool will search for datasets , repositorieson  Github for the given keyword."
    )
    args_schema: Type[BaseModel] = GithubSearchTool

    def _run(self, argument: str) -> str:
       # Perform the search on Github

        response = requests.get(
            "https://api.github.com/search/repositories",

            params={
                "q": argument,
                "sort": "stars",
                "order": "desc"
            },

            auth=(os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_AUTH_TOKEN")),

            headers={
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            }
        )


        if response.status_code != 200: 
            return f"Sorry, error occured {response.status_code}"
        
        data = response.json()

        if data['total_count'] == 0:
            return f"Sorry, I couldn't find any relevant repository on the internet for the keyword = {argument}."
        else:
            string = []

            for repo in data['items']:
                try:
                    string.append('\n'.join([
                        f"Name: {repo['name']}", 
                        f"Stars: {repo['stargazers_count']}", 
                        f"URL: {repo['html_url']}"
                    ]))
                except KeyError:
                    continue

                return '\n\n'.join(string)