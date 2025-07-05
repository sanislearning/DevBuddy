import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import LLMContentFilter
from crawl4ai import LLMConfig
import os
from dotenv import load_dotenv

load_dotenv()
async def main():
        # Configure a 2-level deep crawl
    markdown_generator = DefaultMarkdownGenerator(
        content_filter=LLMContentFilter(
            llm_config=LLMConfig(provider="gemini/gemini-2.0-flash", api_token=os.getenv("GEMINI_API_KEY")),
            instruction="Extract all relevant content and format it as clean markdown.", # Modified instruction
            verbose=True
        )
    )

    config = CrawlerRunConfig(
        markdown_generator=markdown_generator,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_pages=10,
            max_depth=2,
            include_external=False
        ),
        cache_mode="bypass"
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun("https://python.langchain.com/docs/tutorials/agents/?utm_source=chatgpt.com", config=config)

        print(f"Crawled {len(results)} pages in total")

        # Access individual results
        for result in results:
            print(f"URL: {result.url} | Depth: {result.metadata.get('depth', 0)}")
            if not result.markdown.fit_markdown.strip():
                print("⚠️ No content found.")
            else:
                print(result.markdown.fit_markdown[:500])  # Limit for readability


if __name__ == "__main__":
    asyncio.run(main())
