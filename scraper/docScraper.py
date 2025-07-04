import os
import json
import asyncio
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import BrowserConfig,CacheMode
from typing import Dict
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
    provider: str, api_token: str = None, extra_headers: Dict[str, str] = None #the equal tos set the default value
):
    filter=LLMContentFilter(
        llm_config=LLMConfig(provider=provider,api_token=api_token),
        instruction="""
        Focus on extracting the core educational content.
        Include:
        - Key concepts and explanations
        - Important code examples
        - Essential technical details
        Exclude:
        - Navigation elements
        - Sidebars
        - Footer content
        Format the output as clean markdown with proper code blocks and headers.
        """,
        chunk_token_threshold=1024,
        verbose=True
    )
    print(f"\n--- Extracting Structured Data with {provider} ---")

    markdown_generator=DefaultMarkdownGenerator(
        content_filter=filter,
        options={"ignore_links":False}
    )
    browser_config = BrowserConfig(headless=False)

    extra_args = {"temperature": 0, "top_p": 0.9, "max_tokens": 2000}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    crawler_config = CrawlerRunConfig(
        markdown_generator=markdown_generator,
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1, #Tells the crawler to ignore very short blocks lower than the number given
        page_timeout=50000,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=1,
            max_pages=1,
            include_external=False
        ),
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider=provider,api_token=api_token),
            schema=InfoConsume,
            extraction_type='schema',
            instruction=dedent("""
                From the crawled content, extract all programming concepts discussed, including:
                1. The name of the concept.
                2. Related commands or code snippets.
                3. Its structure and usage notes, including any conflicts or caveats.

                Return everything in structured format based on the provided schema. Do not skip any relevant concepts.
            """),
            extra_args=extra_args
        ),
        )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(
            urls=["https://react.dev/learn"],
            config=crawler_config
        )
    print(f"Total pages crawled: {len(results)}\n")
    markdown_output="# Extracted Concepts from React Docs \n\n"
    for i,res in enumerate(results):
        if res.success and res.extracted_content:
            concepts=res.extracted_content

            if isinstance(concepts,dict):
                concepts=[concepts]
            for concept in concepts:
                markdown_output+=f"## Concept: {concept.get('Name','Unnamed')}\n\n"
                markdown_output += f"### Commands\n"
                markdown_output += f"```js\n{concept.get('commands', '').strip()}\n```\n\n"
                markdown_output += f"### Structure\n{concept.get('structure', '').strip()}\n\n"

        else:
            print(f"Failed on {res.url}:{res.error_message}")

    with open("extracted_concepts.md","w",encoding='utf-8') as f:
        f.write(markdown_output)
    print("✅ Markdown written to extracted_concepts.md")
    



if __name__ == "__main__":

    asyncio.run(
        extract_structured_data_using_llm(
            provider="gemini/gemini-2.0-flash", api_token=os.getenv("GEMINI_API_KEY")
        )
    )
