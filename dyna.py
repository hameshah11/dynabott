import openai
import streamlit as st
import pandas as pd


# Initialize the OpenAI API key
openai.api_key = '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'

# Classes and Trainers Data as before
# Classes Data
classes_data = {
    "basics": {
        "description": "This class is designed for beginners. It focuses on building foundational strength and introducing core exercises.",
        "duration": "1 hour",
        "schedule": "Monday, Tuesday, Thursday, Friday"
    },
    "intermediate": {
        "description": "For those who've built some strength and are looking to take it to the next level. Includes compound exercises and cardio intervals.",
        "duration": "1.5 hours",
        "schedule": "Monday to Friday 6pm and 730pm"
    },
    "advanced": {
        "description": "For fitness enthusiasts looking to challenge themselves with high-intensity workouts and advanced techniques.",
        "duration": "2 hours",
        "schedule": "Monday to Friday 6pm and 730pm"
    }
}
new_classes = {
    "dynamik_kids": {
        "description": "For Ages 6-13 who wish to start their fitness journey early in life.",
        "duration": "1 hour",
        "schedule": "Wednesday and Saturday mornings"
    },
    "dynamik_seniors": {
        "description": "For Ages 50+ wishing to become healthier and increase lifespan.",
        "duration": "1 hour",
        "schedule": "Tuesday and Thursday mornings"
    },
    "dynamik_mornings": {
        "description": "For Ages 16+ at all levels of proficiency.",
        "duration": "1 hour",
        "schedule": "Monday to Friday mornings"
    }
}

# Add the new classes to the existing classes_data
classes_data.update(new_classes)

# Pricing Data
pricing_data = {
    "3_days_a_week": "15k per month",
    "4_days_a_week": "17k per month",
    "5_days_a_week": "18.5k per month",
    "registration_fee": "8k"
}

# Trainers Data
trainers_data = {
    "Ahmed": {
        "specialization": "Olympic Weightlifting, Crossfit, Gymnastics, Powerlifting",
        "experience": "5 years",
        "available": "Weekdays"
    },
    "Mohammad": {
        "specialization": "Cardio and HIIT",
        "experience": "3 years",
        "available": "Weekends"
    },
    "Sunny": {
        "specialization": "Flexibility and mobility",
        "experience": "4 years",
        "available": "Weekdays and Sundays"
    },
    "Mehmood": {
        "specialization": "Placeholder",
        "experience": "Placeholder",
        "available": "Placeholder"
    },
    "Nadia": {
        "specialization": "Placeholder",
        "experience": "Placeholder",
        "available": "Placeholder"
    },
    "Baqir": {
        "specialization": "Placeholder",
        "experience": "Placeholder",
        "available": "Placeholder"
    },
    "Danyal": {
        "specialization": "Placeholder",
        "experience": "Placeholder",
        "available": "Placeholder"
    },
    "Tahira": {
        "specialization": "Placeholder",
        "experience": "Placeholder",
        "available": "Placeholder"
    }
}

def display_pricing_table(pricing_data):
    # Remove registration fee from the pricing table data
    recurring_pricing_data = {k: v for k, v in pricing_data.items() if k != "registration_fee"}
    
    # Convert recurring pricing data to a DataFrame for display
    pricing_df = pd.DataFrame(list(recurring_pricing_data.items()), columns=['Plan', 'Price'])
    pricing_df['Plan'] = pricing_df['Plan'].str.replace('_', ' ').str.title()  # Clean up the plan names
    pricing_df.rename(columns={'Plan': 'Plan (per week)'}, inplace=True)  # Rename the column

    st.write("Our Recurring Plans (monthly):")
    st.table(pricing_df)

    # Display the registration fee separately
    st.write(f"One-time Registration Fee: {pricing_data['registration_fee']}")


@st.cache_data(show_spinner=False)
def cached_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=250,
        temperature=0.6)
    return response.choices[0].message['content']

def get_chatbot_response(user_input, conversation_history):
    # Check if user is asking about pricing
    if "price" in user_input.lower() or "cost" in user_input.lower():
        # Respond with a message about pricing plans
        return "Our pricing varies depending on the number of days you choose to train each week. " \
               "You can see the detailed plans above. There is also a one-time registration fee of 10k."

    # If not asking about pricing, continue with the usual process
    # Append user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Get response from OpenAI API using the cached function
    bot_response = cached_openai_response(conversation_history)

    # Post-process the response to ensure it doesn't cut off mid-sentence
    if bot_response.endswith(tuple('.!?')):
        final_response = bot_response
    else:
        final_response = bot_response.rsplit('.', 1)[0] + '.' if '.' in bot_response else bot_response

    # Add bot's response to the conversation history
    conversation_history.append({"role": "assistant", "content": final_response})

    return final_response

def display_classes_table(classes_data):
    # Create a DataFrame from the classes data
    classes_df = pd.DataFrame.from_dict(classes_data, orient='index')
    st.table(classes_df)

def display_trainers_table(trainers_data):
    # Create a DataFrame from the trainers data
    trainers_df = pd.DataFrame.from_dict(trainers_data, orient='index')
    st.table(trainers_df)

def main():
    st.title("DynaBot")

    # Initialize conversation history in session state if it doesn't exist
    if 'conversation_history' not in st.session_state:
        # Generate trainers information
        trainers_info = "\n".join([f"{trainer} specializes in {details['specialization']} and has {details['experience']} of experience. They are available on {details['available']}." for trainer, details in trainers_data.items()])
        
        # Set the initial conversation history
        st.session_state['conversation_history'] = [
            {"role": "system", "content": f"""
            You are DynaBot, a knowledgeable and friendly assistant for Dynamik Gym. Your role is to engage with potential clients, providing them with detailed and motivating information about our services, which include CrossFit-based Functional Training Programs, Aerial Yoga, Kickboxing, and Personal Training sessions. 
When discussing our programs, focus on the benefits of our training methods, such as improving Cardiovascular Endurance, building Strength & Power, enhancing Mobility and Flexibility, and boosting Speed & Agility. Your responses should inspire confidence and a sense of progress, embodying our motto: "No matter who you are today, you can become better tomorrow with Dynamik."
Be ready to answer questions about class schedules, pricing, trainer qualifications, and the unique advantages of joining the Dynamik community. If a user seems interested and no longer has questions, encourage them to follow our Instagram page @dynamik.duo for the latest updates or to message us on whatsapp at +923361118854 to get started on their fitness journey.
            """},
            {"role": "user", "content": f"""
            Dynamik Gym offers a variety of classes in the realm of crossfit, as well as personal training options. Here are the pricing details:
            - 3 days/week: {pricing_data['3_days_a_week']}
            - 4 days/week: {pricing_data['4_days_a_week']}
            - 5 days/week: {pricing_data['5_days_a_week']}
            Registration fee: {pricing_data['registration_fee']}
            """},
            {"role": "user", "content": f"""
            The gym offers three main classes: basics, intermediate, and advanced. 
            {classes_data['basics']['description']} It's scheduled on {classes_data['basics']['schedule']}.
            {classes_data['intermediate']['description']} It's scheduled on {classes_data['intermediate']['schedule']}.
            {classes_data['advanced']['description']} It's scheduled on {classes_data['advanced']['schedule']}.
            We also have personal trainers:
            {trainers_info}
            """}
        ]
    if 'show_pricing' not in st.session_state:
        st.session_state['show_pricing'] = False
    if 'show_classes' not in st.session_state:
        st.session_state['show_classes'] = False
    if 'show_trainers' not in st.session_state:
        st.session_state['show_trainers'] = False

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Pricing'):
            st.session_state['show_pricing'] = not st.session_state['show_pricing']
    with col2:
        if st.button('Crossfit Classes'):
            st.session_state['show_classes'] = not st.session_state['show_classes']
    with col3:
        if st.button('Coaches'):
            st.session_state['show_trainers'] = not st.session_state['show_trainers']


    # Greeting message for the user when they first visit the page
    if len(st.session_state['conversation_history']) == 3:  # Only the initial messages are there
        st.write("Welcome to Dynamik! I'm here to help you learn more about our gym and services. How can I assist you today?")

    # User input
    user_input = st.text_input("You:")

    # When the user provides input, process it and update the conversation history
    if user_input:
        response = get_chatbot_response(user_input, st.session_state['conversation_history'])
        st.session_state['conversation_history'].append({"role": "user", "content": user_input})
        st.session_state['conversation_history'].append({"role": "assistant", "content": response})
        st.write(f"Chatbot: {response}")
    st.markdown('### What would you like to know more about?')
 # Display the information based on the current state
    if st.session_state['show_pricing']:
        display_pricing_table(pricing_data)
    if st.session_state['show_classes']:
        with st.expander("Classes Information", expanded=True):
            display_classes_table(classes_data)

    if st.session_state['show_trainers']:
        with st.expander("Trainers Information", expanded=True):
            display_trainers_table(trainers_data)


if __name__ == "__main__":
    main()

