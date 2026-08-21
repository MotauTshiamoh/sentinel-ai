# sentinel-ai

# Enterprise AI Security Intelligence Platform


Sentinel AI is an end-to-end cybersecurity machine learning project designed to detect malicious network activity and identify anomalous network behaviour.

The project combines network-flow data analysis, supervised machine learning, unsupervised anomaly detection, distribution-shift analysis, threshold tuning, automated testing, and a FastAPI backend.

The goal is not simply to achieve high model accuracy, but to investigate whether a model can **generalise to network traffic it has not seen before**.



# Why Sentinel AI?

Traditional intrusion detection systems often rely on known attack signatures or models trained on historical data.

However, real-world network environments change.

Traffic patterns can differ between:

- different days
- different environments
- different applications
- different attack types
- different network conditions

A model that performs extremely well on a random train/test split may therefore fail when exposed to genuinely unseen traffic.

Sentinel AI explores this problem by evaluating both **standard machine learning performance** and **generalisation to unseen network traffic**.


# Project Objectives

Sentinel AI was built to:

1. Analyse network-flow traffic.
2. Prepare and clean large-scale cybersecurity datasets.
3. Detect malicious network activity using supervised machine learning.
4. Detect previously unseen anomalies using unsupervised learning.
5. Investigate data leakage and duplicate observations.
6. Evaluate models against an unseen day of network traffic.
7. Analyse distribution shift between different traffic environments.
8. Tune anomaly detection thresholds.
9. Expose detection functionality through a FastAPI backend.
10. Provide a foundation for an intelligent cybersecurity monitoring system.



#  Machine Learning Pipeline

The Sentinel AI ML pipeline consists of several stages.

```text
Raw Network Traffic
        │
        ▼
Dataset Inspection
        │
        ▼
Data Cleaning & Preprocessing
        │
        ▼
Duplicate / Leakage Analysis
        │
        ▼
Train / Test Split
        │
        ├───────────────|
        ▼               ▼
Random Forest     Isolation Forest
        │               │
        ▼               ▼
Baseline          Anomaly Detection
Evaluation              │
        │               │
        └───────┬───────┘
                ▼
       Unseen-Day Evaluation
                │
                ▼
       Distribution-Shift Analysis
                │
                ▼
         Threshold Tuning
text '''


Dataset

Sentinel AI uses network-flow data containing 78 numerical traffic features and a target label.

The datasets used during development include:

Tuesday Working Hours

445,909 rows

Attack classes:

Label	Count	Percentage
BENIGN	432,074	96.90%
FTP-Patator	7,938	1.78%
SSH-Patator	5,897	1.32%
Wednesday Working Hours

692,703 rows

Attack classes:

Label	Count	Percentage
BENIGN	440,031	63.52%
DoS Hulk	231,073	33.36%
DoS GoldenEye	10,293	1.49%
DoS slowloris	5,796	0.84%
DoS Slowhttptest	5,499	0.79%
Heartbleed	11	~0.00%

The datasets contain network-flow features such as:

Flow duration
Forward and backward packet counts
Packet lengths
Packet timing
TCP flags
Flow bytes/second
Flow packets/second
Inter-arrival times
Header lengths
Initial TCP window sizes
Active/idle statistics

Data Preparation:

The raw datasets were inspected before model training.

The combined dataset contained:

1,138,612 rows

After removing duplicate observations:

1,024,591 rows

The dataset contains a binary target:

0 = BENIGN
1 = ATTACK

The final binary distribution was:

BENIGN: 821,680
ATTACK: 202,911

The preprocessing pipeline also handles missing values and normalises feature names so that the same features can be consistently passed through the machine learning pipeline.

Data Leakage & Duplicate Analysis:

Before training the models, Sentinel AI checks for duplicate observations and potential leakage between training and testing datasets.

An initial train/test split revealed duplicate feature rows appearing on both sides of the split.

Further investigation identified 22 overlapping feature rows.

These observations were removed before final model evaluation.

The final dataset split contained:

Training rows: 819,556
Testing rows:  204,889

Automated tests were also created to ensure that duplicate feature rows do not appear across the training and testing datasets.

Supervised Learning: Random Forest:

A Random Forest classifier was initially trained as the supervised baseline.

The first evaluation used a random train/test split.

Results
Metric	Result
Accuracy	99.96%
ROC-AUC	1.0000
BENIGN F1	0.9998
ATTACK F1	0.9991

Confusion matrix:

                Predicted
              BENIGN  ATTACK


Actual BENIGN 164271     50
       ATTACK     23  40545

At first glance, this appears to be an excellent model.

However, this result raised an important question:

Does the model actually generalise to traffic from a different environment?

Unseen-Day Evaluation:

To test generalisation more realistically, Sentinel AI was evaluated using:

Training → Tuesday traffic
Testing  → Wednesday traffic

This prevents the model from seeing Wednesday traffic during training.

The result was dramatically different.

Random Forest on Unseen Wednesday Traffic
Metric	Result
Accuracy	63.52%
ROC-AUC	0.4791
Attack Recall	0.00%

The model predicted every Wednesday observation as benign.

                Predicted
              BENIGN  ATTACK


Actual BENIGN 440031      0
       ATTACK 252672      0

This demonstrated that the extremely high random-split performance did not translate into generalisation to the unseen traffic environment.

This became one of the key findings of the project.

Distribution Shift Analysis:

To understand why the model failed on the unseen day, Sentinel AI performs feature-level distribution-shift analysis.

The analysis identified significant differences between Tuesday and Wednesday traffic.

Some of the features with the largest observed distribution shifts included:

Feature	Effect Size
Fwd IAT Std	0.686
Packet Length Std	0.666
Idle Max	0.666
Bwd Packet Length Std	0.663
Idle Mean	0.663
Flow IAT Max	0.657
Fwd IAT Max	0.657
Idle Min	0.656
Packet Length Variance	0.644
Max Packet Length	0.637

This analysis provided evidence that the two traffic environments had substantially different feature distributions.

The project therefore treats distribution shift as an important cybersecurity ML problem, rather than assuming that a high validation score guarantees reliable deployment performance.

Unsupervised Anomaly Detection:

Because supervised models can struggle with previously unseen traffic, Sentinel AI also implements an Isolation Forest anomaly detector.

The Isolation Forest is trained using benign network traffic and attempts to identify observations that differ significantly from normal behaviour.

Benign Network Traffic
          │
   Isolation Forest
          │
Anomaly Score
          │
 Normal / Anomalous

Unseen Wednesday Results
Metric	Result
Accuracy	81.52%
ROC-AUC	0.8294
Attack Precision	86.80%
Attack Recall	58.19%
Attack F1	69.67%

Confusion matrix:

                Predicted
              BENIGN  ANOMALY


Actual BENIGN 417681   22350
       ATTACK 105644  147028

Unlike the Random Forest, the anomaly detector was able to identify a substantial portion of the attack traffic from the unseen day.

Anomaly Threshold Tuning:

The Isolation Forest produces anomaly scores which can be converted into attack predictions using a configurable threshold.

Several thresholds were evaluated.

Threshold	Precision	Recall	F1	False Positive Rate
-0.150	0.6160	0.6907	0.6512	24.73%
-0.100	0.7522	0.6861	0.7176	12.98%
-0.050	0.8261	0.6729	0.7416	8.14%
0.000	0.8680	0.5819	0.6967	5.08%
0.040	0.9205	0.5741	0.7072	2.85%
0.080	0.9371	0.4176	0.5777	1.61%
0.100	0.8768	0.1539	0.2618	1.24%

The best F1 score was obtained at:

Threshold: -0.050
Precision: 82.61%
Recall:    67.29%
F1:        74.16%

This demonstrates the trade-off between detecting more attacks and reducing false positives.

The threshold is configurable rather than hard-coded into the model.

Backend Architecture:

Sentinel AI includes a FastAPI backend designed to provide a foundation for integrating the machine learning models into an application.

The backend contains:

API routes
Risk evaluation logic
Machine learning configuration
Data processing modules
Model training modules
Model evaluation modules

The ML components are organised separately from the API layer to maintain a modular architecture.

Testing:

Automated tests are implemented using pytest.

The project currently tests areas including:

Dataset splitting
Duplicate prevention
Column-name preprocessing
Risk-engine behaviour
Normal HTTPS traffic
High-risk RDP traffic

The final test suite currently passes:

4 passed

Technology Stack:
Programming
Python
Machine Learning
scikit-learn
Random Forest
Isolation Forest
pandas
NumPy
Backend
FastAPI
Uvicorn
Pydantic
Testing
pytest
Development
Git
GitHub
VS Code
Cybersecurity / Data
Network-flow analysis
Intrusion detection
Anomaly detection
Distribution-shift analysis
Network traffic classification

Project Structure
sentinel-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │
│   │   └── ml/
│   │       ├── data/
│   │       │   ├── data_loader.py
│   │       │   ├── inspect_dataset.py
│   │       │   ├── prepare_dataset.py
│   │       │   ├── preprocessor.py
│   │       │   ├── check_leakage.py
│   │       │   ├── analyze_attack_distribution.py
│   │       │   └── analyze_distribution_shift.py
│   │       │
│   │       └── training/
│   │           ├── train_baseline.py
│   │           ├── evaluate_unseen_day.py
│   │           ├── train_anomaly_detector.py
│   │           ├── evaluate_anomaly_detector.py
│   │           ├── analyze_anomaly_scores.py
│   │           ├── tune_anomaly_threshold.py
│   │           └── split_dataset.py
│   │
│   └── requirements.txt
│
├── data/
│   └── README.md
│
├── docs/
│   └── architecture.md
│
├── models/
│   └── intrusion_detection/
│       ├── random_forest_baseline.joblib
│       └── isolation_forest.joblib
│
├── tests/
│   ├── test_dataset_split.py
│   └── test_preprocessor.py
│
├── frontend/
│
├── scripts/
│
└── README.md

 Running the Project:

Clone the repository:

git clone https://github.com/MotauTshiamoh/sentinel-ai.git
cd sentinel-ai

Create and activate the Python virtual environment:

Windows PowerShell
python -m venv backend/venv
.\backend\venv\Scripts\Activate.ps1

Install dependencies:

cd backend
pip install -r requirements.txt

Run the tests:
python -m pytest ..\tests -v

Current Status:
Completed
 Project structure
 FastAPI backend foundation
 Dataset inspection
 Data preprocessing
 Duplicate detection
 Leakage analysis
 Dataset splitting
 Random Forest baseline
 Unseen-day evaluation
 Distribution-shift analysis
 Isolation Forest anomaly detection
 Anomaly score analysis
 Threshold tuning
 Automated testing
 Model persistence
 Architecture documentation

In Progres:s
 Integrating ML predictions into the application
 Expanding the risk-scoring engine
 Building the frontend monitoring interface
 Adding richer security-event visualisation

Future Improvements:

Future versions of Sentinel AI may include:

Real-time network-flow ingestion
Live anomaly monitoring
Security event dashboards
Explainable ML predictions
Attack-type classification
Model monitoring
Drift detection in production
Alert prioritisation
Historical event analysis
Containerised deployment
Cloud deployment

Key Learning:

One of the most important findings from Sentinel AI was that high model performance does not necessarily mean good real-world generalisation.

A random train/test split produced almost perfect results, but evaluation on a genuinely unseen traffic day exposed significant model failure.

This led to the investigation of:

data leakage
duplicate observations
class imbalance
distribution shift
anomaly detection
threshold selection

The project therefore focuses not only on building a machine learning model, but on understanding how reliable that model is when the data changes.

Author

Tshiamo Motau

Computer Science & Business Computing

Interested in:

Artificial Intelligence
Machine Learning
Cybersecurity
Data Science
Software Engineering
Sentinel AI

Detect • Investigate • Predict



