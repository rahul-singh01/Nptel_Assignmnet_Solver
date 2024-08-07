import requests
from bs4 import BeautifulSoup



def get_data(filename):
    data = open(filename , 'r')
    content = data.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    images = soup.select('.yui-img')
    
    data = [ image.get("src")  for image in images ] 
   
    if(data):
        return data

    else:    
        # Select questions and options elements
        questions = soup.select('.qt-question')
        options = soup.select('.qt-choices')

        # Extract text from questions and options, handling potential empty lists
        question_texts = [question.get_text(strip=True) for question in questions]
        
        temp = []
        
        for option in options:
            choices = option.select('.gcb-mcq-choice')
            choiceData = [ i.get_text(strip=True)  for i in choices]
            temp.append(choiceData)
            
            
        qIndex = []
        
        for i in range(len(temp)):
            options = " \n ".join(temp[i])
            qIndex.append(f"{question_texts[i]} \n {options}")
            
        # Print the length of the data
        print(f"\nNumber of questions: {len(question_texts)}")
        print(f"Number of options: {len(temp)}")
        return qIndex
    
# print(get_data('output.html'))