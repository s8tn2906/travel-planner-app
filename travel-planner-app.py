import streamlit as st
import random
from datetime import datetime, timedelta

def generate_detailed_itinerary(inputs):
    # Activity templates based on trip purpose
    activity_templates = {
        'leisure': [
            {'name': 'City Sightseeing', 'time': '09:00-12:00', 'type': 'Cultural'},
            {'name': 'Local Market Exploration', 'time': '14:00-16:00', 'type': 'Cultural'},
            {'name': 'Relaxation Time', 'time': '16:30-18:00', 'type': 'Rest'}
        ],
        'business': [
            {'name': 'Conference/Meetings', 'time': '09:00-12:00', 'type': 'Professional'},
            {'name': 'Networking Lunch', 'time': '12:30-14:00', 'type': 'Networking'},
            {'name': 'Work Session', 'time': '15:00-17:00', 'type': 'Professional'}
        ],
        'adventure': [
            {'name': 'Outdoor Expedition', 'time': '07:00-12:00', 'type': 'Active'},
            {'name': 'Local Terrain Exploration', 'time': '14:00-16:30', 'type': 'Active'},
            {'name': 'Adventure Sports', 'time': '17:00-19:00', 'type': 'Extreme'}
        ],
        'relaxation': [
            {'name': 'Spa Treatment', 'time': '10:00-12:00', 'type': 'Wellness'},
            {'name': 'Beach/Park Relaxation', 'time': '14:00-16:30', 'type': 'Rest'},
            {'name': 'Meditation Session', 'time': '17:00-18:30', 'type': 'Wellness'}
        ],
        'cultural': [
            {'name': 'Museum Tour', 'time': '09:00-11:30', 'type': 'Cultural'},
            {'name': 'Historical Site Visit', 'time': '13:00-15:30', 'type': 'Educational'},
            {'name': 'Local Performance/Workshop', 'time': '18:00-20:00', 'type': 'Cultural'}
        ]
    }

    transportation_options = ['Public Transit', 'Walking', 'Taxi/Rideshare', 'Rental Bike']
    
    dining_options = {
        'vegetarian': ['Vegetarian Café', 'Plant-Based Restaurant'],
        'vegan': ['Vegan Bistro', 'Organic Eatery'],
        'halal': ['Halal Restaurant', 'Middle Eastern Cuisine'],
        'local': ['Traditional Local Restaurant', 'Street Food Experience']
    }

    duration = int(inputs['duration'])
    budget = float(inputs['budget'])
    daily_budget = budget / duration

    days = {}
    start_date = datetime.now()

    for day in range(1, duration + 1):
        current_date = start_date + timedelta(days=day-1)
        purpose_activities = activity_templates.get(inputs['purpose'], activity_templates['leisure'])
        
        days[day] = {
            'date': current_date.strftime('%Y-%m-%d'),
            'activities': purpose_activities,
            'transportation': {
                'primary': random.choice(transportation_options),
                'estimated_cost': round(daily_budget * 0.1, 2)
            },
            'dining': {
                'breakfast': dining_options.get(inputs.get('dietary'), ['Local Breakfast'])[0],
                'lunch': inputs.get('dining', 'Local Restaurant'),
                'dinner': dining_options.get(inputs.get('dietary'), ['Dinner Experience'])[-1]
            },
            'accommodation': {
                'type': inputs.get('accommodation', 'Standard Hotel'),
                'estimated_cost': round(daily_budget * 0.4, 2)
            },
            'daily_budget': round(daily_budget, 2),
            'notes': inputs.get('mobility', 'No specific mobility notes')
        }

    return {
        'destination': inputs['destination'],
        'days': days
    }

def main():
    st.title('🌍 AI Travel Planner')

    # Input form
    with st.form(key='travel_planner_form'):
        col1, col2 = st.columns(2)
        with col1:
            destination = st.text_input('Destination', placeholder='City, country, or region')
            budget = st.number_input('Total Budget ($)', min_value=0, step=100)
        
        with col2:
            duration = st.number_input('Trip Duration (Days)', min_value=1, max_value=30, step=1)
            purpose = st.selectbox('Trip Purpose', 
                ['Leisure', 'Business', 'Adventure', 'Relaxation', 'Cultural Exploration'])

        accommodation = st.text_input('Accommodation Preferences', 
            placeholder='Hotel type, location preference')
        
        col3, col4 = st.columns(2)
        with col3:
            dietary = st.text_input('Dietary Preferences', 
                placeholder='Vegetarian, vegan, halal')
        with col4:
            dining = st.text_input('Dining Preferences', 
                placeholder='Local cuisine, restaurant type')

        interests = st.text_area('Specific Interests/Activities', 
            placeholder='Photography, wildlife, history, etc.')
        
        mobility = st.text_input('Mobility Considerations', 
            placeholder='Walking limitations, accessibility needs')

        submit_button = st.form_submit_button(label='Generate Itinerary')

    # Itinerary Generation
    if submit_button:
        if not all([destination, budget, duration]):
            st.error('Please fill in destination, budget, and duration')
        else:
            inputs = {
                'destination': destination,
                'budget': budget,
                'duration': duration,
                'purpose': purpose.lower(),
                'accommodation': accommodation,
                'dietary': dietary,
                'dining': dining,
                'interests': interests,
                'mobility': mobility
            }

            with st.spinner('Generating your personalized travel plan...'):
                itinerary = generate_detailed_itinerary(inputs)

            # Display Itinerary
            st.header(f'🗺️ {itinerary["destination"]} Travel Itinerary')

            for day, details in itinerary['days'].items():
                with st.expander(f'Day {day} - {details["date"]}'):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader('Activities')
                        for activity in details['activities']:
                            st.write(f"{activity['time']}: {activity['name']} ({activity['type']})")
                    
                    with col2:
                        st.subheader('Logistics')
                        st.write(f"**Transportation:** {details['transportation']['primary']} "
                                 f"(Est. Cost: ${details['transportation']['estimated_cost']})")
                        st.write(f"**Dining:**\n"
                                 f"- Breakfast: {details['dining']['breakfast']}\n"
                                 f"- Lunch: {details['dining']['lunch']}\n"
                                 f"- Dinner: {details['dining']['dinner']}")
                        st.write(f"**Accommodation:** {details['accommodation']['type']} "
                                 f"(Est. Cost: ${details['accommodation']['estimated_cost']})")
                    
                    if details['notes'] != 'No specific mobility notes':
                        st.info(f"**Notes:** {details['notes']}")

            # Trip Summary
            st.sidebar.header('Trip Summary')
            st.sidebar.metric('Total Budget', f'${budget}')
            st.sidebar.metric('Average Daily Expenditure', 
                              f'${round(budget/duration, 2)}')

if __name__ == '__main__':
    main()
