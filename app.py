from flask import Flask, request, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
from flask_cors import CORS
app = Flask(__name__)
CORS(app,origins=["http://localhost:3000/"])

# Load data and models
df = pd.read_excel('events.xlsx')
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Precompute embeddings
event_descriptions = df['Description'].fillna('').tolist()
event_embeddings = model.encode(event_descriptions, show_progress_bar=True)

MONTHS = [month.lower() for month in [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
]]

def detect_month(user_input):
    for month in MONTHS:
        if month in user_input.lower():
            return month.capitalize()
    return None

def analyze_input_context(user_input):
    sentiment_result = sentiment_pipeline(user_input)
    label = sentiment_result[0]['label']
    score = sentiment_result[0]['score']
    return "negative" if label == 'NEGATIVE' and score > 0.7 else \
           "positive" if label == 'POSITIVE' and score > 0.7 else "neutral"

def get_sbert_embeddings(text):
    return model.encode(text)

@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.json.get("user_input", "")
    if not user_input:
        return jsonify({"error": "Please provide a valid user input."}), 400

    selected_month = detect_month(user_input)
    filtered_df = df

    if selected_month:
        filtered_df = df[df['Month'].str.contains(selected_month, na=False, case=False)]
        if filtered_df.empty:
            return jsonify({"message": f"No events found for {selected_month}."})

    context = analyze_input_context(user_input)
    user_input_embedding = get_sbert_embeddings(user_input)
    filtered_descriptions = filtered_df['Description'].fillna('').tolist()
    filtered_embeddings = model.encode(filtered_descriptions, show_progress_bar=False)
    similarities = cosine_similarity([user_input_embedding], filtered_embeddings)[0]

    relevant_events = []
    threshold = 0.4 if context == "positive" else 0.3 if context == "neutral" else 0.5

    for idx, similarity in enumerate(similarities):
        if similarity > threshold:
            relevant_events.append((idx, similarity))

    if relevant_events:
        relevant_events = sorted(relevant_events, key=lambda x: x[1], reverse=True)[:3]
        result = filtered_df.iloc[[idx for idx, _ in relevant_events]].to_dict(orient="records")
        return jsonify({"events": result})
    else:
        return jsonify({"message": "No relevant events found."})

if __name__ == '__main__':
    app.run(debug=True)
