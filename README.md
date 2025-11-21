# 🏥 Community Health Worker (CHW) Assistant

AI-powered tool for **predicting patient risk** and supporting **community health workers** in rural and underserved areas.

---

## 🌍 **Problem Statement**

Community Health Workers (CHWs) play a critical role in delivering last-mile healthcare, yet they face several challenges:

* **Limited access to medical experts** in rural areas.
* **High patient loads**, making manual assessments slow or inaccurate.
* **Lack of real-time decision support tools** for risk triage.
* **Data not fully utilized** to inform early interventions.

This project introduces an **AI-based patient risk prediction system** to support CHWs with quick, accurate insights.

---

## 🎯 **Project Objectives**

* Predict whether a patient is at **high risk**, **medium risk**, or **low risk**.
* Provide CHWs with a **fast, easy-to-use** tool for decision support.
* Enable **offline-first community deployment** using Streamlit.
* Allow **real-world scalability** via API/Cloud deployment.

---

## 👥 **Target Market**

1. **Community Health Workers (Primary Users)**

   * Need simplified diagnostic support and early risk detection.
2. **County Governments & NGOs**

   * 63% are adopting digital health tools — making this a high-value solution.
3. **Small Clinics & Rural Health Facilities**

   * Limited experts → rely heavily on CHWs for primary care.
4. **Public Health Programs**

   * Require data-driven insights for planning interventions.

---

## 🧠 **Model Used**

### **XGBoost Classifier**

We selected **XGBoost** over logistic regression because:

* It handles **non-linear relationships** better.
* Performs superior **predictive accuracy**.
* Deals well with **imbalanced health datasets**.
* Robust to noise, missing values, and categorical variables.

The goal was *predictability*, and XGBoost achieved this best.

---

## 📁 **Project Structure**

```bash
CHW-Assistant/
│
├── data/                 # Dataset (.csv)
├── notebooks/            # Exploratory data analysis
├── models/               # Saved trained model (.pkl)
├── app.py                # Main Streamlit app
├── train.py              # Script for training the model
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## ⚙️ **How to Run the Project**

### **1. Clone the Repository**

```bash
git clone https://github.com/KIRUMAH-sam/CHW-Assistant.git
cd CHW-Assistant
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Train the Model (Optional)**

```bash
python models.py
```

This will generate a file like:

```
models/xgboost_chw_model.pkl
```

### **4. Run the Flask App**

```bash
Flask run - The app.py runs in the backend
```

This launches a web interface where CHWs can input patient features and get a prediction.

---


## 📊 **Key Features**

* Real-time risk prediction
* Simple UI for CHWs
* Deployed as a lightweight flask web tool
* Highly accurate XGBoost-based inference
* Easily extendable for more medical inputs

---

## 🧩 **Possible Future Extensions**

* Add mobile app version
* Add multilingual support (Swahili, Kikuyu, Somali)
* Enable voice-based data entry for CHWs
* Integrate with county health systems
* Use federated learning for privacy-preserving training

---


## 🏁 **Conclusion**

The CHW Assistant bridges the gap between **rural communities** and **quality healthcare** by giving CHWs predictive intelligence at their fingertips. The use of XGBoost ensures high performance, while Streamlit and flask allows rapid deployment anywhere.

---

