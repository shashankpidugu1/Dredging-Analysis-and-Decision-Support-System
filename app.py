import streamlit as st
import pandas as pd
import joblib

# Load your models and the LabelEncoder
clf = joblib.load('dredging_classifier.pkl')  # RandomForestClassifier model
reg = joblib.load('dredging_regressor.pkl')   # RandomForestRegressor model

# Dredging Frequency Guidelines
frequency_guidelines = {
    'River': {
        'Sand': (2, 5),
        'Clay': (5, 10),
        'Silt': (3, 7)
    },
    'Lake': {
        'Sand': (5, 10),
        'Clay': (10, 20),
        'Silt': (7, 15)
    },
    'Ocean': {
        'Sand': (10, 20),
        'Clay': (20, 30),
        'Silt': (15, 25)
    }
}

# Manual mappings for Sediment Type and Type of Water Body
sediment_mapping = {'Sand': 0, 'Silt': 1, 'Clay': 2}
water_body_mapping = {'River': 0, 'Lake': 1, 'Ocean': 2}

# Streamlit interface
st.title("Dredging Decision and Cost Estimation")

# Option menu for multipage navigation
page = st.sidebar.selectbox("Select Page", ["Home", "Prediction", "About"])

if page == "Home":
    st.write("Welcome to the Dredging Decision and Cost Estimation Tool. Use the Prediction page to input data and get estimates.")

elif page == "Prediction":
    # Input fields for prediction
    sedimentation_depth = st.number_input("Sedimentation Depth (m):", min_value=0.0, step=0.1)
    sediment_type = st.selectbox("Sediment Type:", options=['Sand', 'Silt', 'Clay'])
    water_flow_rate = st.number_input("Water Flow Rate (m³/s):", min_value=0.0, step=0.1)
    precipitation_levels = st.number_input("Precipitation Levels (mm):", min_value=0.0, step=0.1)
    previous_dredging_date = st.number_input("Previous Dredging Date:", min_value=2000, max_value=2025, step=1)
    type_of_water_body = st.selectbox("Type of Water Body:", options=['River', 'Lake', 'Ocean'])
    water_body_depth = st.number_input("Water Body Depth (m):", min_value=0.0, step=0.1)

    # Button to trigger prediction
    if st.button("Predict"):
        # Manually encode sediment type and type of water body
        sediment_type_encoded = sediment_mapping[sediment_type]
        type_of_water_body_encoded = water_body_mapping[type_of_water_body]

        # Convert input data to a list for model prediction
        features = [
            sedimentation_depth,
            sediment_type_encoded,
            water_flow_rate,
            precipitation_levels,
            previous_dredging_date,
            type_of_water_body_encoded,
            water_body_depth
        ]

        # Create DataFrame for model input
        feature_names = [
            'Sedimentation Depth (m)',
            'Sediment Type',
            'Water Flow Rate (m³/s)',
            'Precipitation Levels (mm)',
            'Previous Dredging Dates',
            'Type of Water Body',
            'Water Body Depth (m)'
        ]
        
        input_df = pd.DataFrame([features], columns=feature_names)

        # Predict dredging decision
        dredging_decision = clf.predict(input_df)[0]
        dredging_decision_label = 'Yes' if dredging_decision == 1 else 'No'

        # Predict dredging cost
        estimated_cost = reg.predict(input_df)[0]

        # Get the original sediment type and water body type
        sediment_type_original = sediment_type
        type_of_water_body_original = type_of_water_body
        
        # Dredging frequency guidelines based on sediment type and water body type
        dredging_range = frequency_guidelines.get(type_of_water_body_original, {}).get(sediment_type_original, (0, 0))
        min_years, _ = dredging_range

        # Calculate future dredging year
        future_dredging_year = previous_dredging_date + min_years if dredging_range != (0, 0) else previous_dredging_date + 5

        # Display results
        st.write(f"Dredging Decision: **{dredging_decision_label}**")
        if dredging_decision_label == 'Yes':
            st.write(f"Estimated Dredging Cost: **₹{estimated_cost:.2f}**")
        else:
            st.write(f"Future Dredging Year: **{future_dredging_year}**")

elif page == "About":
    st.write("This tool provides estimates for dredging decisions based on various input parameters. It utilizes machine learning models trained on historical data to predict costs and future dredging requirements.")
