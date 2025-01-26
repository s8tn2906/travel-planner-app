import streamlit as st
import random

# Mock data for destinations and activities
DESTINATIONS = [
    {"name": "Bali, Indonesia", "type": "Beach", "avgCost": 1200},
    {"name": "Tokyo, Japan", "type": "City", "avgCost": 2000},
    {"name": "Swiss Alps", "type": "Mountains", "avgCost": 2500}
]

ACTIVITIES = {
    "Beach": [
        "Beach Relaxation", 
        "Snorkeling", 
        "Island Hopping", 
        "Local Market Visit", 
        "Sunset Cruise", 
        "Water Sports", 
        "Cultural Performance"
    ],
    "City": [
        "City Tour", 
        "Museum Visit", 
        "Local Cuisine Experience", 
        "Shopping", 
        "Historical Site Tour", 
        "Park Exploration", 
        "Night Market"
    ],
    "Mountains": [
        "Hiking", 
        "Mountain Biking", 
        "Scenic Viewpoint Visit", 
        "Local Village Tour", 
        "Skiing/Snowboarding", 
        "Nature Photography", 
        "Hot Springs"
    ]
}

INTERESTS = [
    'Adventure', 'Relaxation', 'Culture', 'History', 'Cuisine'
]

FOOD_PREFERENCES = [
    'Vegetarian', 'Vegan', 'Gluten-Free', 'No Restrictions'
]

def generate_destination_suggestions(budget, interests):
    """Filter destinations based on budget and interests."""
    return [
        dest for dest in DESTINATIONS 
        if int(budget) >= dest['avgCost'] and len(interests) > 0
    ]

def generate_itinerary(destination, duration, budget):
    """Generate a travel itinerary based on destination and duration."""
    # Find the destination type
    dest_type = next(dest['type'] for dest in DESTINATIONS if dest['name'] == destination)
    
    # Generate activities for each day
    activities = []
    available_activities = ACTIVITIES[dest_type].copy()
    
    for day in range(1, int(duration) + 1):
        # Randomly select an activity, remove to avoid repetition
        if available_activities:
            activity = random.choice(available_activities)
            available_activities.remove(activity)
        else:
            # Refill activities if depleted
            available_activities = ACTIVITIES[dest_type].copy()
            activity = random.choice(available_activities)
        
        # Simple cost calculation
        cost = random.randint(50, 200)
        
        activities.append({
            'day': day, 
            'activity': activity, 
            'cost': cost
        })
    
    # Calculate total estimated cost
    total_estimated_cost = sum(activity['cost'] for activity in activities)
    
    return {
        'destination': destination,
        'days': int(duration),
        'budget': int(budget),
        'activities': activities,
        'totalEstimatedCost': total_estimated_cost
    }
    
def main():
    st.title('✈️ Dream Travel Planner')
    
    # Sidebar for inputs
    st.sidebar.header('Trip Details')
    budget = st.sidebar.number_input('Total Budget ($)', min_value=500, max_value=10000, value=2000)
    duration = st.sidebar.number_input('Trip Duration (Days)', min_value=1, max_value=30, value=1)
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
