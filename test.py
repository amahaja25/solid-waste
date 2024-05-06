from playwright.sync_api import sync_playwright
import os
import csv
import shutil

def main():
    url = "https://opendata.maryland.gov/stories/s/LMA-Solid-Waste-Program-Violation/rqzj-6qrm/"
    pdf_folder = "pdfs"
    csv_filename = "pdf_links.csv"
    os.makedirs(pdf_folder, exist_ok=True)
    

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")

        relevant_links = page.locator("a[href*='https://mdedataviewer.mde.state.md.us/OpenDataDocuments']")
        link_handles = relevant_links.element_handles()

        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['pdf_id', 'page_url'])

            for link in link_handles:
                with context.expect_page() as new_page_info:
                    link.click()
                new_page = new_page_info.value
                new_page.wait_for_load_state("networkidle")
                page_url = new_page.url
                pdf_id = page_url.split('=')[-1]
                href = link.get_attribute('href')

                pdf_input = new_page.query_selector("input[type='image'][class='fdoc-pdf']")
                if pdf_input:
                    file_id = pdf_input.get_attribute("title")
                    pdf_id = file_id.split("_")[0]

                    with new_page.expect_download() as download_info:
                        pdf_input.click()

                    download = download_info.value

                    downloaded_file_path = download.path()

                    pdf_filename = f"{pdf_folder}/{pdf_id}.pdf" 

                    shutil.move(downloaded_file_path, pdf_filename)

                    print(f"PDF downloaded: {pdf_filename}")
                else:
                    print("PDF link not found on the page.")

                writer.writerow([pdf_id, href])

                new_page.close()
        
        context.close()
        browser.close()

if __name__ == "__main__":
    main()