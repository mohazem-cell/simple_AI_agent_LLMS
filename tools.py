from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


def save_to_file(content: str, filename: str = "research_output.txt") -> str:
    """Saves content to a file with a timestamped filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fromated_txt = f"---Research Output - {timestamp}---\n\n{content}\n\n---End of Research Output---"
    # full_filename = f"{timestamp}_{filename}"
    with open(filename,"a",encoding="utf-8") as file:
        file.write(fromated_txt)
    return f"Content saved to {filename}"

save_tool = Tool(
    name="save_to_file",
    func=save_to_file,
    description="Saves the provided content to a text file and returns the filename."
)

search=DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="Search the web for information."
)

wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki)