import google.generativeai as genai
import os
from termcolor import colored
import json

# Initialize Gemini API
API_KEY = "AIzaSyBWjOOLgLfF1IE1YR_0-G8meAUdZE8ZCco"

class UserInfo:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.gender = ""
        self.country = ""
        self.state = ""
        self.symptoms = []

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def get_user_info():
    user = UserInfo()
    print(colored("\nPlease provide your information:", "cyan"))
    
    user.name = input(colored("Name: ", "yellow")).strip()
    while True:
        try:
            user.age = int(input(colored("Age: ", "yellow")))
            if 0 < user.age < 150:
                break
            print("Please enter a valid age between 1 and 150")
        except ValueError:
            print("Please enter a valid number for age")
    
    while True:
        user.gender = input(colored("Gender (M/F/Other): ", "yellow")).strip().upper()
        if user.gender in ['M', 'F', 'OTHER']:
            break
        print("Please enter M, F, or Other")
    
    user.country = input(colored("Country: ", "yellow")).strip()
    user.state = input(colored("State/Province: ", "yellow")).strip()
    return user

def get_symptom_prediction(model, user_info, symptoms):
    context = f"""
    Patient Information:
    - Age: {user_info.age}
    - Gender: {user_info.gender}
    - Location: {user_info.state}, {user_info.country}
    
    Reported Symptoms:
    {', '.join(symptoms)}
    
    Based on these symptoms, what are the possible conditions? Also suggest if any other relevant symptoms should be checked. 
    Format the response as follows:
    1. Possible Conditions (list top 3 most likely conditions)
    2. Additional Symptoms to Check (list 2-3 most relevant symptoms to ask about)
    3. Recommendation (include a medical disclaimer)
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Error generating prediction: {str(e)}"

def main():
    print(colored("Welcome to the Disease Prediction Bot!", "blue", attrs=["bold"]))
    print(colored("This bot will help predict possible conditions based on your symptoms.", "blue"))
    print(colored("Note: This is for informational purposes only and not a substitute for professional medical advice.", "red"))
    
    try:
        model = initialize_gemini(API_KEY)
        user_info = get_user_info()
        
        print(colored("\nLet's discuss your symptoms.", "green"))
        symptoms = []
        
        while True:
            symptom = input(colored("\nPlease describe a symptom you are experiencing (or type 'done' if finished): ", "yellow")).strip()
            
            if symptom.lower() == 'done':
                if not symptoms:
                    print(colored("Please enter at least one symptom.", "red"))
                    continue
                break
                
            symptoms.append(symptom)
            
            # Get prediction and follow-up questions after each symptom
            if symptoms:
                print(colored("\nAnalyzing your symptoms...", "cyan"))
                prediction = get_symptom_prediction(model, user_info, symptoms)
                print(colored("\nAnalysis Result:", "green"))
                print(prediction)
                
                continue_check = input(colored("\nWould you like to add more symptoms? (yes/no): ", "yellow")).strip().lower()
                if continue_check != 'yes':
                    break
        
        # Final prediction and disclaimer
        print(colored("\nFinal Analysis:", "blue", attrs=["bold"]))
        final_prediction = get_symptom_prediction(model, user_info, symptoms)
        print(final_prediction)
        
        print(colored("\nIMPORTANT DISCLAIMER:", "red", attrs=["bold"]))
        print(colored("This prediction is based on AI analysis and should not be considered as a medical diagnosis. "
                     "Please consult with a qualified healthcare professional for proper diagnosis and treatment. "
                     "If you are experiencing severe symptoms, seek immediate medical attention.", "red"))
        
    except Exception as e:
        print(colored(f"\nAn error occurred: {str(e)}", "red"))

if __name__ == "__main__":
    main()
