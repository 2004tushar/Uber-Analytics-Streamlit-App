# 🚖 Uber Analytics Streamlit App

An interactive, multi-page data analytics dashboard built with **Python** and **Streamlit** to explore, filter, and visualize Uber ride booking data — no coding required.

---

## 📸 Features at a Glance

| Module | What It Does |
|---|---|
| 📋 Dataset Explorer | Browse, search, filter & download raw data |
| 📊 Business Overview | KPIs, revenue breakdowns & cancellation audit |
| 🚀 Ride Analytics | Advanced charts — sunburst, treemap, Sankey, heatmap |
| 🤖 Data Assistant | Ask questions in plain English, get instant charts |

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** — web app framework
- **Pandas** — data manipulation
- **Plotly Express & Graph Objects** — interactive visualizations
- **streamlit-option-menu** — sidebar navigation

---

## 📁 Project Structure

```
Uber-Analytics-Streamlit-App/
│
├── UberDashboard.py       # Main application file (508 lines)
├── uber.csv               # Uber ride dataset
├── requirements           # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/2004tushar/Uber-Analytics-Streamlit-App.git
cd Uber-Analytics-Streamlit-App
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pandas plotly streamlit-option-menu
```

### 3. Run the App

```bash
streamlit run UberDashboard.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📊 Module Details

### 📋 1. Dataset Explorer

- **Column Selector** — Show/hide specific columns
- **Full-Text Search** — Search any value across all columns
- **Column Filter** — Filter rows by column value with Apply/Reset support (session-state persistent)
- **Row Slider** — Control how many rows to display
- **Statistics** — `describe()` output for all columns + deep dive for numeric columns
- **Distribution Charts** — Auto-generated histograms for selected numeric columns
- **CSV Download** — Download the filtered dataset with one click

---

### 📊 2. Business Overview

**KPI Cards:**
- 💰 Gross Revenue
- ✅ Fulfilment Rate
- 📍 Average Trip Distance
- ⭐ Average Customer Rating
- 🚖 Total Bookings

**Charts & Tables:**
- Vehicle Performance Matrix (revenue, bookings, distance, rating, share %)
- Revenue & Rating bar charts by Vehicle Type
- Operational Efficiency table (Avg VTAT & CTAT by Vehicle Type)
- Booking Status pie chart
- Payment Method breakdown
- Top Cancellation Reasons (Customer + Driver)

---

### 🚀 3. Ride Analytics

Advanced visualizations with sidebar vehicle-type filters:

| Chart | Insight |
|---|---|
| 🌞 Sunburst | Revenue hierarchy by Vehicle → Payment Method |
| 🗺️ Treemap | Revenue distribution across segments |
| 📦 Box Plot | Customer rating spread by vehicle type |
| 📍 Scatter + OLS | Ride distance vs. booking value with trendline |
| 🔀 Sankey Diagram | Ride flow from Vehicle Type → Booking Status |
| 🔥 Heatmap | Avg rating across Vehicle Type × Payment Method |

---

### 🤖 4. Data Assistant

A simple keyword-based query interface. Type a question and get an instant chart:

| Query Keyword | Response |
|---|---|
| `total rides` | Bar chart of rides by booking status |
| `revenue` | Bar chart of revenue by vehicle type |
| `distance` | Scatter plot of distance vs. booking value |

---

## 🎨 UI & Design

- **Dark theme** with custom CSS styling
- **Sidebar navigation** using `streamlit-option-menu`
- **Metric cards** with custom background (`#1a1a2e`) and border styling
- **Green accent** (`#1DB954`) throughout for consistency
- **Session-state filters** that persist across page interactions
- **`@st.cache_data`** for fast, cached data loading

---

## 📦 Dataset — `uber.csv`

The app reads from `uber.csv` which is expected to contain the following columns:

| Column | Description |
|---|---|
| `Booking ID` | Unique ride identifier |
| `Booking Status` | Completed / Cancelled / etc. |
| `Vehicle Type` | Type of Uber vehicle |
| `Ride Distance` | Distance of the trip (km) |
| `Booking Value` | Fare charged |
| `Payment Method` | Cash / Card / UPI / etc. |
| `Customer Rating` | Rating given by customer (out of 5) |
| `Avg VTAT` | Average Vehicle Turnaround Time |
| `Avg CTAT` | Average Customer Turnaround Time |
| `Reason for cancelling by Customer` | Cancellation reason |
| `Driver Cancellation Reason` | Driver-side cancellation reason |

---

## 🚀 Deployment

You can deploy this app for free on **Streamlit Community Cloud**:

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file as `UberDashboard.py`
5. Click **Deploy**

---

## 🙌 Author

**Tushar** — [@2004tushar](https://github.com/2004tushar)

---

## 📄 License

This project is open source and available for educational and portfolio use.
