# 📅 Event Recommendation API (Flask + SBERT + Sentiment)

A lightweight Flask API that recommends events based on user input using semantic similarity (SBERT) and sentiment analysis.

---

## 🚀 Features

- Recommends relevant events based on natural language input
- Uses SBERT (`paraphrase-MiniLM-L6-v2`) for semantic similarity
- Uses sentiment analysis to adjust result relevance
- Filters events by month if mentioned in the input
- Loads events from a local `events.xlsx` file
- Supports CORS for frontend access

---

## 🧰 Tech Stack

- Flask
- SentenceTransformers
- Hugging Face Transformers
- Pandas
- scikit-learn
- Flask-CORS

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
flask
flask-cors
pandas
scikit-learn
sentence-transformers
transformers
```

3. **Add your events file**

Make sure there is an `events.xlsx` file in the project root with the following structure:

| Description                    | Month    |
|--------------------------------|----------|
| Jazz Festival in Central Park | June     |
| Winter Art Show               | December |
| ...                           | ...      |

---

## ▶️ Running the API

Start the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

---

## 📡 API Endpoint

### `POST /recommend`

Returns the top 3 most relevant events based on the user's input.

#### Request Body

```json
{
  "user_input": "I'm looking for fun events in June with music"
}
```

#### Possible Responses

**Relevant events found:**

```json
{
  "events": [
    {
      "Description": "Jazz Festival in Central Park",
      "Month": "June"
    },
    {
      "Description": "Summer Music Fest",
      "Month": "June"
    }
  ]
}
```

**No events for the specified month:**

```json
{
  "message": "No events found for June."
}
```

**No relevant events found:**

```json
{
  "message": "No relevant events found."
}
```

**Invalid input:**

```json
{
  "error": "Please provide a valid user input."
}
```

---

## 🧠 How It Works

1. User sends a text input (e.g., "fun events in June").
2. The API detects a month keyword, if present (e.g., "June").
3. Filters the dataset by that month if available.
4. Analyzes sentiment (positive, neutral, negative).
5. Encodes the input and event descriptions using SBERT.
6. Computes cosine similarity and returns the most relevant events (up to 3), based on sentiment-adjusted thresholds.

---

## 🌐 CORS Support

The server includes [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) to support frontend integration (React, Vue, etc.).

---

## 📌 Notes

- Semantic search is powered by `paraphrase-MiniLM-L6-v2`.
- Sentiment analysis uses `distilbert-base-uncased`.
- Similarity thresholds are tuned based on sentiment polarity:
  - Positive: 0.4
  - Neutral: 0.3
  - Negative: 0.5
- Ensure your `events.xlsx` file has enough descriptive and clean data for meaningful results.
