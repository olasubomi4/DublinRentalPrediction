from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, MinMaxScaler

app = Flask(__name__)

# Load models
models = {
    'randomForest': joblib.load("RandomForest.pkl"),
    'linearRegression': joblib.load("LinearRegression.pkl"),
    'elasticNet': joblib.load("ElasticNet.pkl"),
    'gradientBoosting': joblib.load("GradientBoosting.pkl"),

}

scaler = StandardScaler()

# Create an instance of OneHotEncoder
encoder = OneHotEncoder(handle_unknown='ignore')

# Define expected columns (including one-hot encoded columns)
expected_columns = ['TV', 'First aid kit', 'Washer', 'Kitchen', 'Dishwasher', 'Heating',
       'Microwave', 'Iron', 'accommodates', 'minimum_nights', 'bathrooms',
       'bedrooms', 'beds', 'room_type', 'county_Dublin 1', 'county_Dublin 10',
       'county_Dublin 11', 'county_Dublin 12', 'county_Dublin 13',
       'county_Dublin 14', 'county_Dublin 15', 'county_Dublin 16',
       'county_Dublin 17', 'county_Dublin 18', 'county_Dublin 2',
       'county_Dublin 20', 'county_Dublin 22', 'county_Dublin 24',
       'county_Dublin 3', 'county_Dublin 4', 'county_Dublin 5',
       'county_Dublin 6', 'county_Dublin 6W', 'county_Dublin 7',
       'county_Dublin 8', 'county_Dublin 9', 'property_type_Entire condo',
       'property_type_Entire guest suite', 'property_type_Entire home',
       'property_type_Entire rental unit',
       'property_type_Entire serviced apartment',
       'property_type_Entire townhouse', 'property_type_Private room in condo',
       'property_type_Private room in home',
       'property_type_Private room in rental unit',
       'property_type_Private room in townhouse',
       'property_type_Shared room in hostel']


def set_one_hot_feature(df, feature_name, feature_value):
    """Set a one-hot encoded feature in the DataFrame."""
    encoded_feature = f'{feature_name}_{feature_value}'
    if encoded_feature in expected_columns:
        df[encoded_feature] = 1
    else:
        df[encoded_feature] = 0  # Default value if feature is not in expected columns

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        input_df = pd.DataFrame([input_data])  # Check if the selected model is valid
        selected_model = input_data.get('model', 'linearRegression')
        model = models.get(selected_model, models['linearRegression'])

        # Extract values from input data
        county = input_data.get('county')
        property_type = input_data.get('property_type')

        # Map the county and property type to their respective one-hot encoded columns
        set_one_hot_feature(input_df, 'county', county)
        set_one_hot_feature(input_df, 'property_type', property_type)

        for feature in expected_columns:
            if feature not in input_df.columns:
                input_df[feature] = 0  # Set default val

            # Ensure the DataFrame has the correct columns in the expected order
        input_df = input_df[expected_columns]

        # Make a prediction
        predictions = model.predict(input_df)

        # Return the prediction as a JSON response
        return jsonify({'predictions': predictions[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
