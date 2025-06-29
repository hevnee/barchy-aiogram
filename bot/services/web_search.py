from duckduckgo_search import DDGS

def search_web(request: str, max_results=3) -> str:
    """ Using the request is searched through DuckDuckGo.

        The answers may not be unambiguous. """

    with DDGS() as ddgs:
        results = ddgs.text(request)
        snippets = [r['body'] for r in results][:max_results]

    if not snippets:
        return "No results found."

    snippets = [f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results][:max_results]
    return "\n".join(snippets)