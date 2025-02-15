import requests
from bs4 import BeautifulSoup

def fact_sheet_scrap():
    #File Handling
    # Read the file line by line
    urls=[]

    with open("urls/fact_sheet_urls.txt", "r") as file: #ENTER the file name
        for line in file:
            urls.append(line.strip())

    # Close the file
    file.close()





    #WEB Scrapping

    for url in urls:
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                #getting all the sections 
                specific_section=soup.find_all('article',class_='sf-detail-body-wrapper')
                if specific_section:

                    with open("info.txt", "a") as file:

                        for article in specific_section: 
                            file.write(article.get_text())
                        file.write("\n")
                    file.close()
                    

            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: fact_sheet {e}")
    return 

if __name__ == "__main__":
    fact_sheet_scrap()