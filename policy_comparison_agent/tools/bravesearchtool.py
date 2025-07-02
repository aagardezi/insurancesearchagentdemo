from brave import Brave
from . import helpercode

PROJECT_ID = helpercode.get_project_id()
SEARCH_API_KEY=helpercode.access_secret_version(PROJECT_ID, "bravesearchkey")

def brave_search_tool(query: str) -> dict:
    """Does a general web search using the brave search enging in order to provide responses
    to help fulfill the query. The search string should be detailed
    ensure you are searching for PDFs

    Args:
        query (str): The search query to perform.

    Returns:
        dict: status and result or error msg.
    """
    brave = Brave(SEARCH_API_KEY)

    num_results = 10

    search_results = brave.search(q=query, count=num_results)
    print(search_results.web_results)
    # pdfresults = search_results.download_all_pdfs()
    # for pdf in pdfresults:
    #     print(pdf)
    results =[]
    for result in search_results.web_results:
        if 'content_type' in result:
            if result['content_type'] =='pdf':
                results.append({'Dscription': result['description'], 'Content': helpercode.get_text_from_pdf_url2(result['url'])})


    return {
        "status": "success",
        "report": (
            results
        ),
    }