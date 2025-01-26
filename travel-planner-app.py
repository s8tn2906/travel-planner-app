import streamlit as st
import random

# Mock data for destinations
DESTINATIONS = [
    {
        'name': 'Bali, Indonesia',
        'type': 'Beach',
        'avgCost': 1200,
        'highlights': ['Beaches', 'Temples', 'Surfing'],
        'activities': ['Beach Yoga', 'Temple Tour', 'Snorkeling']
    },
    {
        'name': 'Tokyo, Japan',
        'type': 'City',
        'avgCost': 2000,
        'highlights': ['Technology', 'Culture', 'Food'],
        'activities': ['City Tour', 'Sushi Experience', 'Tech Museum']
    },
    {
        'name': 'Swiss Alps',
        'type': 'Mountains',
        'avgCost': 2500,
        'highlights': ['Hiking', 'Scenery', 'Alpine Villages'],
        'activities': ['Mountain Hiking', 'Scenic Train Ride', 'Village Tour']
    }
]

INTERESTS = ['Adventure', 'Relaxation', 'Culture', 'History', 'Cuisine']
FOOD_PREFERENCES = ['Vegetarian', 'Vegan', 'Gluten-Free', 'No Restrictions']

def generate_itinerary(destination, duration, budget):
    # Generate random activities based on trip duration
    activities = random.sample(destination['activities'], min(len(destination['activities']), duration))
    
    # Calculate costs
    daily_budget = budget / duration
    activities_with_cost = [
        {
            'day': i+1, 
            'activity': activity, 
            'cost': round(random.uniform(50, daily_budget/2), 2)
        } 
        for i, activity in enumerate(activities)
    ]
    
    total_cost = sum(activity['cost'] for activity in activities_with_cost)
    
    return {
        'destination': destination['name'],
        'activities': activities_with_cost,
        'total_cost': round(total_cost, 2),
        'budget_status': 'Within Budget' if total_cost <= budget else 'Exceeds Budget'
    }

def main():
    st.title('✈️ Dream Travel Planner')
    
    # Sidebar for inputs
    st.sidebar.header('Trip Details')
    budget = st.sidebar.number_input('Total Budget ($)', min_value=500, max_value=10000, value=2000)
    duration = st.sidebar.number_input('Trip Duration (Days)', min_value=1, max_value=30, value=2)
    interests = st.sidebar.multiselect('Select Interests', INTERESTS)
    food_preference = st.sidebar.selectbox('Food Preference', FOOD_PREFERENCES)
    
    # Filter destinations
    eligible_destinations = [
        dest for dest in DESTINATIONS 
        if dest['avgCost'] <= budget and len(interests) > 0
    ]
    
    # Main content area
    if eligible_destinations:
        st.header('Suggested Destinations')
        
        for destination in eligible_destinations:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(destination['name'])
                st.write(f"Type: {destination['type']}")
                st.write(f"Estimated Cost: ${destination['avgCost']}")
                st.write(f"Highlights: {', '.join(destination['highlights'])}")
            
            with col2:
                if st.button(f'Plan Trip to {destination["name"]}'):
                    itinerary = generate_itinerary(destination, duration, budget)
                    
                    st.header(f"Itinerary for {destination['name']}")
                    st.write(f"**Total Trip Cost:** ${itinerary['total_cost']}")
                    st.write(f"**Budget Status:** {itinerary['budget_status']}")
                    
                    st.subheader('Daily Activities:')
                    for activity in itinerary['activities']:
                        st.write(f"**Day {activity['day']}:** {activity['activity']} (${activity['cost']:.2f})")
    else:
        st.warning('No destinations match your budget. Try increasing your budget.')

if __name__ == '__main__':
    main()
