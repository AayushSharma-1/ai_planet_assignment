from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import os, json, requests
from dotenv import load_dotenv
load_dotenv(r'reportagent\src\reportagent\.env')

class HuggingFaceSearchTool(BaseModel):
    """Input schema for HuggingFaceSearchTool."""
    argument: str = Field(..., description="It is the keyword for which you want to search dataset on HuggingFace, make sure your keyword is general in nature should not specifically refer to a company / organization or a person.")    

class HuggingFaceSearch(BaseTool):
    name: str = "huggingface_search_tool"
    description: str = (
        "This tool will search for datasets on HuggingFace for the given keyword."
    )
    args_schema: Type[BaseModel] = HuggingFaceSearchTool

    def _run(self, argument: str) -> str:
       # Perform the search on HuggingFace

        response = requests.get(
            "https://huggingface.co/api/datasets",

            params={"search":argument,"limit":5,"full":"False"},

            headers={"Authorization": os.getenv("HUGGING_FACE_AUTH_TOKEN")}
        )


        if  response.text == '[]':    
            return f"Sorry, I couldn't find any relevant information on huggingFace for the given {argument}."
        
        data = response.json()

        string = []

        for dataset in data:
            try:
                string.append('\n'.join([
                    f"ID: {dataset['id']}",
                    f"Author: {dataset['author']}",
                    f"Downloads: {dataset['downloads']}",
                    f"Likes: {dataset['likes']}",
                    f"Last Modified: {dataset['lastModified']}",
                    f"Tags: {', '.join(dataset['tags'])}",
                    f"Private: {'Yes' if dataset['private'] else 'No'}",
                    f"Gated: {'Yes' if dataset['gated'] else 'No'}"
                ]))
            except KeyError:
                continue

            return '\n\n'.join(string)