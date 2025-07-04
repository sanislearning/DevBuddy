import os
import json
import asyncio
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import BrowserConfig, CacheMode
from typing import Dict, List, Union
from crawl4ai.content_filter_strategy import LLMContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from dotenv import load_dotenv
from textwrap import dedent

load_dotenv()

class InfoConsume(BaseModel):
    Name: str = Field(..., description="Name of the concept")
    commands: str = Field(..., description="Different pieces of code associated with the concept")
    structure: str = Field(
        ..., description="Information on how it is to be used and any conflicts that might occur"
    )

async def extract_structured_data_using_llm(
    provider: str, api_token: str = None, llm_api_headers: Dict[str, str] = None
):
    """
    Crawls a React documentation URL, extracts educational content, and then
    further extracts structured programming concepts using an LLM.

    Args:
        provider (str): The LLM provider string (e.g., "gemini/gemini-2.0-flash").
        api_token (str, optional): The API token for the LLM. Defaults to None.
        llm_api_headers (Dict[str, str], optional): Extra headers for LLM API calls. Defaults to None.
    """
    filter = LLMContentFilter(
        llm_config=LLMConfig(provider=provider, api_token=api_token),
        instruction=dedent("""
            Focus on extracting the core educational content.
            Include:
            - Key concepts and explanations
            - Important code examples
            - Essential technical details
            Exclude:
            - Navigation elements
            - Sidebars
            - Footer content
            - Advertisements or promotional material
            - Irrelevant external links
            Format the output as clean markdown with proper code blocks and headers.
        """),
        chunk_token_threshold=1024,
        verbose=True
    )
    print(f"\n--- Extracting Structured Data with {provider} ---")

    markdown_generator = DefaultMarkdownGenerator(
        content_filter=filter,
        options={"ignore_links": False}
    )

    # BrowserConfig for the web crawler (e.g., for headless Browse)
    browser_config = BrowserConfig(headless=False)

    # Extra arguments for the LLM calls within LLMExtractionStrategy
    llm_extra_args = {"temperature": 0, "top_p": 0.9,}
    if llm_api_headers:
        llm_extra_args["extra_headers"] = llm_api_headers

    crawler_config = CrawlerRunConfig(
        markdown_generator=markdown_generator,
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=50000,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=1,
            max_pages=1, # Only one page for initial testing
            include_external=False
        ),
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider=provider, api_token=api_token), # Use passed api_token
            schema=InfoConsume,
            extraction_type='schema',
            instruction=dedent("""
                From the crawled content, extract all programming concepts discussed, including:
                1. The name of the concept.
                2. Related commands or code snippets.
                3. Its structure and usage notes, including any conflicts or caveats.

                Return everything in structured format based on the provided schema. Do not skip any relevant concepts.
                Ensure all fields in the schema are populated with relevant information from the text.
            """),
            extra_args=llm_extra_args # Pass LLM specific extra args here
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler: # Pass browser_config to the crawler
        results = await crawler.arun_many(
            urls=["https://react.dev/learn"],
            config=crawler_config
        )

    print(f"Total pages crawled: {len(results)}\n")
    markdown_output = "# Extracted Concepts from React Docs \n\n"

    for i, res in enumerate(results):
        if res.success and res.extracted_content:
            # Ensure extracted_content is a list of InfoConsume models or dictionaries
            concepts: Union[List[InfoConsume], Dict] = res.extracted_content

            if isinstance(concepts, dict): # LLM might return a single dict instead of a list
                concepts = [concepts]
            
            # Type hinting for clarity and robustness, assuming pydantic models are returned
            # Or if dictionaries are returned, ensure they match the schema's keys
            for concept_data in concepts:
                # If LLMExtractionStrategy returns Pydantic models directly, use .dict()
                if isinstance(concept_data, BaseModel):
                    concept_dict = concept_data.dict()
                else: # Assume it's already a dictionary
                    concept_dict = concept_data

                markdown_output += f"## Concept: {concept_dict.get('Name', 'Unnamed Concept')}\n\n"
                markdown_output += f"### Commands\n"
                markdown_output += f"```javascript\n{concept_dict.get('commands', '').strip()}\n```\n\n" # Added 'javascript' for syntax highlighting
                markdown_output += f"### Structure\n{concept_dict.get('structure', '').strip()}\n\n"
        else:
            print(f"Failed to process {res.url}: {res.error_message}")
            if not res.success:
                print(f"Crawler failed on {res.url} with error: {res.error_message}")
            elif not res.extracted_content:
                print(f"No content extracted by LLM for {res.url}")

    with open("extracted_concepts.md", "w", encoding='utf-8') as f:
        f.write(markdown_output)
    print("✅ Markdown written to extracted_concepts.md")

if __name__ == "__main__":
    try:
        asyncio.run(
            extract_structured_data_using_llm(
                provider="gemini/gemini-2.0-flash", api_token=os.getenv("GEMINI_API_KEY")
            )
        )
    except Exception as e:
        print(f"An error occurred during execution: {e}")