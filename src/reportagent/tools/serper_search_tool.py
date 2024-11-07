from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import os, json, requests
from bs4 import BeautifulSoup

class MySerperSearchTool(BaseModel):
    """Input schema for MySerperTool."""
    argument: str = Field(..., description="It is the keyword for which you want to search on Google.")

class MySerperTool(BaseTool):
    name: str = "search_tool"
    description: str = (
        "This Tool will do Google search for You and scrape content from the links provided."
    )
    args_schema: Type[BaseModel] = MySerperSearchTool

    def _run(self, argument: str) -> str:
        # Perform a Google search via Serper API
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": argument})
        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if 'organic' not in response.json():      
            return "Sorry, I couldn't find any relevant information on the internet for the given query."
        
        results = response.json()['organic']
        output = []

        for result in results[:4]:
            try:
                title = result['title']
                link = result['link']
                snippet = result['snippet']
                
                # Scrape content directly within _run function
                scraped_content = self.scrape_link_content(link)

                # Append result with title, link, snippet, and scraped content
                output.append(
                    f"Title: {title}\nLink: {link}\nSnippet: {snippet}\nContent:\n{scraped_content}"
                )
            except KeyError:
                continue

        return '\n\n'.join(output)

    def scrape_link_content(self, url: str) -> str:
        """Fetches and scrapes the main content of a webpage from a URL."""
        try:
            page = requests.get(url, timeout=5)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Extract main text content (e.g., paragraphs within main article sections)
            content = []
            for paragraph in soup.find_all('p')[:3]:
                content.append(paragraph.get_text())

            return '\n'.join(content)  # Return first 10 paragraphs for brevity
        except requests.RequestException:
            return "Content could not be fetched."
