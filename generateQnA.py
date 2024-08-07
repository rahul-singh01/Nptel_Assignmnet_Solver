import asyncio
import concurrent.futures
from contentScraper import get_data
from geminiAI import init_gemini
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from PDFBeautify import create_pdf_beautify

# Define a synchronous function to process each piece of data
def process_data(data):
    return init_gemini(data)

# Define an asynchronous function to manage the overall process
async def search_and_process_results_async(filename):
    # Load data using get_data
    data = get_data(filename=filename)
    
    if not data:
        print("No data found.")
        return
    
    # Collect results concurrently using ThreadPoolExecutor
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run process_data in a thread pool
        tasks = [loop.run_in_executor(executor, process_data, d) for d in data]
        results_list = await asyncio.gather(*tasks)
    
    # Store the collected results into a PDF
    create_pdf_beautify(results_list, "output.pdf")

# Define a synchronous function to manage the overall process
def search_and_process_results_sync(filename):
    # Load data using get_data
    data = get_data(filename=filename)
    
    if not data:
        print("No data found.")
        return
    
    # Collect results synchronously
    results_list = [process_data(d) for d in data]
    
    # Store the collected results into a PDF
    create_pdf_beautify(results_list, "output.pdf")

def init(filename, async_mode=True):
    if async_mode:
        asyncio.run(search_and_process_results_async(filename))
    else:
        search_and_process_results_sync(filename)

# Example usage
# init('your_data_file_name_here', async_mode=True)  # For async processing
# init('your_data_file_name_here', async_mode=False) # For sync processing
