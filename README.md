# 🤖 Robot Radar - AI Content Detector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

**Robot Radar** is a Streamlit-based AI content detector that analyzes text burstiness and complexity. It provides instant probability scores, visual gauges, and detailed readability metrics to distinguish between human writing and AI-generated text.

## 🚀 Features

* **Advanced Pattern Analysis:** Measures sentence variance ("burstiness") and word complexity to detect robotic phrasing.
* **Visual Scoring:** Real-time gauge chart indicating AI probability.
* **Deep Metrics:** Breakdowns of Flesch-Kincaid Grade Level, complex word ratios, and sentence counts.
* **Comparison Mode:** Built-in sample texts to demonstrate the difference between AI and Human writing styles.

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/robot-radar.git](https://github.com/your-username/robot-radar.git)
    cd robot-radar
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

* `app.py`: The main application logic and UI.
* `requirements.txt`: List of Python dependencies.
* `README.md`: Project documentation.

## ☁️ Deployment

This app is ready to be deployed on **Streamlit Community Cloud**:

1.  Push this code to a GitHub repository.
2.  Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3.  Click **New app**, select your repository, and click **Deploy**.

## ⚠️ Disclaimer

This tool uses heuristic algorithms to estimate the likelihood of text being AI-generated based on statistical patterns (sentence length variance, complex word ratios). It is a probabilistic tool and should be used for guidance rather than as absolute proof.
