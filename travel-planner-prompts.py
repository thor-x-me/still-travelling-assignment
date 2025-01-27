import streamlit as st
import openai
from typing import Dict, List
import groq
import os

class TravelPlannerSystem:
    def __init__(self):
        # Initialize OpenAI client with API key from Streamlit secrets
        # self.client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # I am using Groq as I do not have openAI API key
        self.client = groq.Groq(api_key=st.secrets["GROQ_API_KAY"])
        self.system_prompt = """You are an expert travel planner with deep knowledge of destinations worldwide. 
        Your role is to create personalized travel itineraries that perfectly match each traveler's preferences, 
        budget, and interests. Always maintain a helpful, enthusiastic, and professional tone."""
    
    def get_completion(self, prompt: str, system_message: str = None, llm="openAI") -> str:
        if llm == "groq":
            messages = []
            if system_message:
                messages.append({"role": "user", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            try:
                response = self.client.chat.completions.create(model="llama3-70b-8192",
                                               messages=messages,
                                               max_tokens=4000,
                                               temperature=1.2)
                messages.append({
                 "role": "assistant",
                 "content": response.choices[0].message.content
                })
                return response.choices[0].message.content
            except Exception as e:
                st.error(f"Error calling GROQ API: {str(e)}")
                return None
        """     
        Get completion from OpenAI API
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error calling OpenAI API: {str(e)}")
            return None

    def initial_input_prompt(self) -> str:
        return """Please provide the following essential details for your trip:
        1. Destination
        2. Trip duration (in days)
        3. Budget range (low/moderate/high or specific amount)
        4. Primary purpose of travel (e.g., adventure, relaxation, culture, etc.)
        5. Any specific preferences or must-see attractions"""

    def refinement_prompt(self, initial_info: Dict) -> str:
        return f"""Based on your interest in visiting {initial_info['destination']} for {initial_info['duration']} days, 
        I'd like to understand more about your preferences:
        1. Do you have any dietary restrictions or preferences?
        2. What's your ideal pace of travel (relaxed/moderate/fast-paced)?
        3. Any mobility considerations I should know about?
        4. Preferred accommodation type (luxury/mid-range/budget) and location preferences?
        5. Are you interested in local cuisine experiences?
        6. Do you prefer guided tours or self-exploration?"""

    def generate_activities(self, user_info: Dict) -> List[str]:
        """
        Generate activity suggestions using OpenAI
        """
        prompt = f"""Given the following user preferences:
        - Destination: {user_info['destination']}
        - Duration: {user_info['duration']} days
        - Budget: {user_info['budget']}
        - Purpose: {user_info['purpose']}
        - Dietary needs: {user_info.get('dietary', 'None specified')}
        - Mobility: {user_info.get('mobility', 'No restrictions')}
        
        Please suggest 10-15 specific activities and attractions that:
        1. Match their budget and interests
        2. Can be reasonably completed within the time available
        3. Consider their dietary and mobility needs
        4. Include a mix of popular attractions and hidden gems
        5. Account for their preferred travel pace
        
        Format each activity as a bullet point with a brief description and estimated time needed."""
        
        response = self.get_completion(prompt, self.system_prompt, llm="groq")
        return response.split('\n') if response else []

    def generate_itinerary(self, user_info: Dict) -> str:
        """
        Generate final itinerary using OpenAI
        """
        prompt = f"""Create a detailed day-by-day itinerary for {user_info['duration']} days in {user_info['destination']}.
        
        User Preferences:
        - Budget: {user_info['budget']}
        - Purpose: {user_info['purpose']}
        - Pace: {user_info.get('pace', 'moderate')}
        - Dietary: {user_info.get('dietary', 'None specified')}
        - Accommodation: {user_info.get('accommodation', 'mid-range')}
        
        For each day, include:
        1. Morning, afternoon, and evening activities
        2. Estimated timing for each activity
        3. Recommended restaurants fitting their preferences and budget
        4. Transportation suggestions between locations
        5. Estimated costs for activities and meals
        
        Format the itinerary in a clear, easy-to-read structure with day headers.
        Consider local opening hours, travel time between locations, and logical grouping of nearby attractions."""
        
        return self.get_completion(prompt, self.system_prompt, llm='groq')

def main():
    st.title("AI Travel Planner")
    
    # Add API key setup through Streamlit secrets
    if 'OPENAI_API_KEY' not in st.secrets:
        st.error("Please set up your OpenAI API key in Streamlit secrets!")
        st.stop()
    
    planner = TravelPlannerSystem()
    
    # Create session state to store user inputs
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    # Step 1: Initial Input Collection
    if st.session_state.step == 1:
        st.header("Basic Trip Information")
        st.write(planner.initial_input_prompt())
        
        destination = st.text_input("Destination")
        duration = st.number_input("Duration (days)", min_value=1, max_value=30, value=7)
        budget = st.selectbox("Budget", ["Low", "Moderate", "High"])
        purpose = st.text_input("Primary Purpose of Travel")
        preferences = st.text_area("Specific Preferences or Must-see Attractions")
        
        if st.button("Next: Refine Preferences") and destination and purpose:
            st.session_state.initial_info = {
                "destination": destination,
                "duration": duration,
                "budget": budget,
                "purpose": purpose,
                "preferences": preferences
            }
            st.session_state.step = 2
            st.rerun()
    
    # Step 2: Refinement Input Collection
    elif st.session_state.step == 2:
        st.header("Detailed Preferences")
        st.write(planner.refinement_prompt(st.session_state.initial_info))
        
        dietary = st.text_input("Dietary Restrictions/Preferences")
        pace = st.selectbox("Travel Pace", ["Relaxed", "Moderate", "Fast-paced"])
        mobility = st.text_input("Mobility Considerations")
        accommodation = st.selectbox("Accommodation Type", ["Budget", "Mid-range", "Luxury"])
        
        if st.button("Generate Itinerary"):
            user_info = {
                **st.session_state.initial_info,
                "dietary": dietary,
                "pace": pace,
                "mobility": mobility,
                "accommodation": accommodation
            }
            
            with st.spinner("Generating your personalized itinerary..."):
                # Generate activities first
                activities = planner.generate_activities(user_info)
                
                # Generate final itinerary
                itinerary = planner.generate_itinerary(user_info)
                
                st.header("Your Personalized Itinerary")
                st.markdown(itinerary)
                
                # Add option to start over
                if st.button("Plan Another Trip"):
                    st.session_state.step = 1
                    st.rerun()

if __name__ == "__main__":
    main()
