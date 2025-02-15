import requests
from bs4 import BeautifulSoup


def question_answer_scrap():
    #File Handling
    # Read the file line by line
    urls=[]

    with open("urls/question_answer_urls.txt", "r") as file:
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

                #getting all the questions
                specific_section=soup.find_all('div',class_='sf-accordion__trigger-panel')
                question=[]
                if specific_section:
                    for que in specific_section:
                        question.append((que.get_text()).strip())
                    
                #getting all answers
                specific_section=soup.find_all('div',class_='sf-accordion__content')
                answer=[]
                if specific_section:
                    for ans in specific_section:
                        answer.append((ans.get_text()).strip())
                
                sz= min(len(question),len(answer))
                with open("info.txt", "a") as file:
                    for i in range(sz):     
                        file.write("Question "+(str(i+1))+": "+question[i]+" :This question has following answer: "+answer[i])   
                    file.write("\n")       
                file.close()
                    
                    

            

        except Exception as e:
            print(f"An error occurred: question_answer {e}")
    return 

if __name__ == "__main__":
    question_answer_scrap()
