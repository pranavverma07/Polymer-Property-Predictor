from flask import Flask, request, Response, jsonify
import pandas as pd
import numpy as np
import time
from rdkit import Chem
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Chem import Descriptors
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from lightgbm import LGBMRegressor
from sklearn.multioutput import MultiOutputRegressor
import joblib
import os
from ollama import chat
from flask_cors import CORS
from pymongo import MongoClient
import json

# from shs import calculate_steric_hindrance_score

# Flask app
app = Flask(__name__)
CORS(app)

# MongoDB Setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["polymer_database"]
collection = db["polymer_descriptions"]

# Load trained model and scalers (Ensure these are saved during training)
# Define the directory where the files are stored
model_dir = os.path.join(os.path.dirname(__file__), "models")

# Load the saved files
model = joblib.load(os.path.join(model_dir, "model.pkl"))
feature_scaler = joblib.load(os.path.join(model_dir, "feature_scaler.pkl"))
target_scaler = joblib.load(os.path.join(model_dir, "target_scaler.pkl"))
descriptor_columns = joblib.load(os.path.join(model_dir, "descriptor_columns.pkl"))

# Load dataset for sampling
dataset_path = "dataset.csv"
dataset = pd.read_csv(dataset_path)

# Define molecular descriptor calculator
descriptor_names = [desc[0] for desc in Descriptors.descList]
calculator = MoleculeDescriptors.MolecularDescriptorCalculator(descriptor_names)


def calculate_descriptors(smile):
    """Calculate molecular descriptors for a given SMILES string."""
    try:
        mol = Chem.MolFromSmiles(smile)
        if mol is None:
            raise ValueError("Invalid SMILES string.")
        return list(calculator.CalcDescriptors(mol))
    except Exception as e:
        raise ValueError(f"Error processing SMILES string: {str(e)}")


@app.route('/predict', methods=['POST'])
def predict_properties():
    """
    API endpoint to predict properties for a given SMILES string.
    Input: JSON {"smiles": "SMILES_STRING"}
    Output: JSON with predicted properties
    """
    data = request.get_json()
    if "smiles" not in data:
        return jsonify({"error": "Missing 'smiles' key in request body"}), 400

    smiles_input = data["smiles"]

    # Validate SMILES
    try:
        mol = Chem.MolFromSmiles(smiles_input)
        if mol is None:
            return jsonify({"error": f"Invalid SMILES string: {smiles_input}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error validating SMILES string: {str(e)}"}), 400

    # Calculate descriptors
    try:
        input_descriptors = pd.DataFrame([calculate_descriptors(smiles_input)], columns=descriptor_names)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Ensure descriptor consistency with the training set
    input_descriptors = input_descriptors[descriptor_columns]

    # Replace missing values with 0
    input_descriptors = input_descriptors.fillna(0)

    # Scale descriptors
    input_features = feature_scaler.transform(input_descriptors)

    # Predict properties
    predictions = model.predict(input_features)
    predictions_original = target_scaler.inverse_transform(predictions)

    # Prepare results
    result = {
        "density": predictions_original[0][0],
        "refractive_index": predictions_original[0][1],
        "dielectric_const_dc": predictions_original[0][2],
        "thermal_conductivity": predictions_original[0][3],
    }

    return jsonify(result)


@app.route('/describe', methods=['POST'])
def describe_polymer():
    """
    API endpoint to describe a polymer based on its properties.
    Input: JSON {"smiles": "SMILES_STRING", "properties": {"density": float, "refractive_index": float, ...}}
    Output: Streamed description in chunks.
    """
    data = request.get_json()
    if "properties" not in data or "smiles" not in data:
        return jsonify({"error": "Missing 'smiles' or 'properties' key in request body"}), 400

    smiles = data["smiles"]
    properties = data["properties"]

    # Check if description exists in MongoDB
    existing_entry = collection.find_one({"smiles": smiles})
    if existing_entry:
        # Stream the stored description
        def stream_stored_description():
            description = existing_entry["description"]
            for chunk in description.split(". "):  # Split into chunks
                yield chunk + ". "  # Mimic streaming by sending chunked sentences
                time.sleep(0.1)  # Optional: Add a slight delay to mimic live streaming

        return Response(stream_stored_description(), content_type='text/plain; charset=utf-8')

    # Generate description using LLM if not found
    prompt = f"""
    Based on the following properties:
    - **Density**: {properties['density']:.4f} g/cm³
    - **Refractive Index**: {properties['refractive_index']:.4f}
    - **Dielectric Constant (DC)**: {properties['dielectric_const_dc']:.4f}
    - **Thermal Conductivity**: {properties['thermal_conductivity']:.4f} W/mK

    
    Provide a detailed description of the polymer in only 4-5 lines that includes:
    1. **Description**: Key characteristics and features
    2. **Applications**: Potential use cases
    """

    def generate_stream():
        stream = chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': prompt}], stream=True)
        description = ""
        for chunk in stream:
            content = chunk['message']['content']
            description += content
            yield content  # Stream to the frontend

        # Save the generated description to MongoDB
        collection.insert_one({
            "smiles": smiles,
            "description": description.strip(),
            "properties": properties,
        })

    return Response(generate_stream(), content_type='text/plain; charset=utf-8')


@app.route('/random-sample', methods=['GET'])
def get_random_sample():
    """
    API endpoint to return a random sample from the dataset.
    Returns random rows from the dataset.
    """
    try:
        # Randomly sample 10 rows from the dataset
        sampled_data = dataset.sample(n=10, random_state=np.random.randint(1, 1000))
        # Convert to a dictionary for JSON response
        sample_values = sampled_data.to_dict(orient="list")
        return jsonify(sample_values)
    except Exception as e:
        return jsonify({"error": f"Error fetching random sample: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
