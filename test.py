from playwright.sync_api import sync_playwright
import os
import shutil

def main():
    url = "https://opendata.maryland.gov/stories/s/LMA-Solid-Waste-Program-Violation/rqzj-6qrm/"
    pdf_folder = "pdfs"
    os.makedirs(pdf_folder, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        # Wait for the page to load
        page.wait_for_load_state("networkidle")

        # Extract relevant links from the iframe
        relevant_links = page.locator("a[href*='https://mdedataviewer.mde.state.md.us/OpenDataDocuments']")
        link_handles = relevant_links.element_handles()

        for link in link_handles:
            with context.expect_page() as new_page_info:
                link.click()
            new_page = new_page_info.value
            new_page.wait_for_load_state("networkidle")
            page_url = new_page.url
            pdf_id = page_url.split('=')[-1]

            pdf_input = new_page.query_selector("input[type='image'][class='fdoc-pdf']")
            if pdf_input:
                # Get the file ID from the 'title' attribute of the PDF input element
                file_id = pdf_input.get_attribute("title")
                # Extract the PDF ID from the file ID
                pdf_id = file_id.split("_")[0]

                # Click on the PDF input element to initiate the download
                with new_page.expect_download() as download_info:
                    pdf_input.click()

                # Get the downloaded file
                download = download_info.value

                # Get the path of the downloaded file
                downloaded_file_path = download.path()

                # Generate the desired filename for the PDF
                pdf_filename = f"{pdf_folder}/{pdf_id}.pdf" 

                # Move the downloaded file to the desired location with the new filename
                shutil.move(downloaded_file_path, pdf_filename)

                print(f"PDF downloaded: {pdf_filename}")
            else:
                print("PDF link not found on the page.")

            new_page.close()

        context.close()
        browser.close()

if __name__ == "__main__":
    main()