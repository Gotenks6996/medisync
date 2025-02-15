import requests
from bs4 import BeautifulSoup


def disease_outbreak_scrap():
    #File Handling
    # Read the file line by line
    urls=[]

    with open("urls/disease_outbreak_urls.txt", "r") as file:
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
                specific_section=soup.find_all('h3',class_='don-section')
                if specific_section:
                    section = []
                    a=0
                    # putting all sections in an array
                    for div in specific_section:
                            if div.get_text()=="Epidemiology":
                                a=1
                            section.append(div.get_text())



                    specific_content = soup.find_all('div', class_='don-content')
                    # getting only particular sections
                    if specific_content:
                        i=0
                        #file handling to append in the info file
                        with open("info.txt", "a") as file:

                            for div in specific_content: 
                                # condition to get only particular section
                                if section[i]=="Description of the situation" and a==0:
                                    file.write(div.get_text())
                                if section[i]=="Epidemiology":
                                    file.write(div.get_text())
                                if section[i]=="WHO advice":
                                    file.write(div.get_text())
                                i+=1
                            file.write("\n")
                        file.close()
                    

            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: disease_outbreak {e}")
    return 

if __name__ == "__main__":
    disease_outbreak_scrap()
