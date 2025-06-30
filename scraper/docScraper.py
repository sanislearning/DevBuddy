import requests
from bs4 import BeautifulSoup
import html2text

def html_to_markdown_single(html):
    soup = BeautifulSoup(html, "html.parser")
    h2_sections = soup.find_all("h2")

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.bypass_tables = False
    h.ignore_emphasis = False

    output_md = []

    for h2 in h2_sections:
        section_title = h2.get_text(strip=True)
        section_content = ""
        
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break
            section_content += str(sibling)

        md_section = h.handle(f"<h2>{section_title}</h2>\n{section_content}")
        output_md.append(md_section)

    return "\n".join(output_md)

# --- Example usage ---
if __name__ == "__main__":
    url = "https://react.dev/learn"  # You can change this to any other doc page
    print(f"📥 Downloading from: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"❌ Error downloading page: {e}")
        exit(1)

    print("✅ HTML downloaded. Converting to Markdown...")
    full_markdown = html_to_markdown_single(html)

    with open("react_docs.md", "w", encoding="utf-8") as f:
        f.write(full_markdown)

    print("✅ Markdown saved to react_docs.md")
