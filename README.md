
````markdown
# 📊 Retail Intelligence System

A simple AI-powered dashboard to analyze retail sales data, visualize trends, and provide business insights.

---

## 🚀 Features

- Dashboard showing revenue, orders, and sales
- Charts (Bar, Pie, Line) for data visualization
- ML insights (top and low performing products)
- AI chatbot for business suggestions
- CSV file upload for analysis

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn

---

## ⚙️ Setup

### 1. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API key

Create a `.env` file and add:

```bash
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

---

## 📊 Input Format

```bash
Product, Quantity, Price, Date
```

---

## 💡 Output

* Revenue analysis
* Top-selling product
* Low-performing product
* Sales trends
* AI-based suggestions

---

## 👨‍💻 Author

Ruha Eilaf
