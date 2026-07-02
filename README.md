# Phone Screen Wellbeing Analysis

## 📊 Project Overview

This project analyzes the relationship between smartphone usage patterns and mental health outcomes using the **StudentLife dataset** from Dartmouth College. The dataset contains passive sensing data from 48 students over a 10-week academic term, including GPS, accelerometer, WiFi, Bluetooth, conversation, and app usage data, along with mental health surveys and academic performance metrics.

## 🎯 Research Questions

- How do smartphone usage patterns correlate with stress levels?
- What behavioral indicators predict mental health outcomes?
- How does academic workload affect sleep, activity, and mood?
- Can we predict mental health status from passive sensor data?

## 📁 Project Structure

```
phone_screen_wellbeing/
├── data/
│   ├── raw/                    # Original StudentLife dataset files
│   ├── processed/              # Cleaned and aggregated data
│   └── external/               # Additional datasets (survey data)
├── notebooks/
│   ├── 01_EDA_StudentLife.ipynb  # Exploratory Data Analysis
│   ├── 02_Data_Cleaning.ipynb   # Data cleaning and preprocessing
│   ├── 03_Feature_Engineering.ipynb  # Feature extraction
│   └── 04_Modeling.ipynb        # Predictive modeling
├── scripts/
│   ├── data_loader.py          # Data loading utilities
│   ├── feature_extractor.py    # Feature extraction functions
│   └── visualization.py        # Visualization helpers
└── README.md                   # Project documentation
```

## 📥 Dataset Information

### StudentLife Dataset
- **Source**: Dartmouth College (2014)
- **Participants**: 48 undergraduate students
- **Duration**: 10-week academic term
- **Size**: ~3.04 GB (1983 files)
- **Kaggle**: https://www.kaggle.com/datasets/dartweichen/student-life

### Data Types

#### 1. **Passive Sensing Data** (Automatically collected)
- **GPS**: Location coordinates, timestamps
- **Accelerometer**: Physical activity (walking, running, stationary)
- **WiFi**: Indoor location, connection patterns
- **Bluetooth**: Social proximity, device interactions
- **Conversation**: Duration and frequency of conversations
- **App Usage**: Application usage patterns
- **Screen**: Screen on/off events

#### 2. **EMA Data** (Ecological Momentary Assessments)
- Self-reported stress levels
- Mood assessments
- Activity tracking
- Social interaction reports

#### 3. **Survey Data**
- **PHQ-9**: Depression scale
- **PSS**: Perceived Stress Scale
- **Flourishing Scale**: Mental well-being
- **SWLS**: Satisfaction with Life Scale
- **PANAS**: Positive and Negative Affect Schedule

#### 4. **Academic Data**
- Term GPA
- Cumulative GPA
- Class performance

## 🚀 Getting Started

### 1. Download the Dataset

```bash
# Download from Kaggle
# 1. Go to: https://www.kaggle.com/datasets/dartweichen/student-life
# 2. Click "Download" button
# 3. Extract the zip file
# 4. Place the 'dataset' folder contents in data/raw/
```

### 2. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
pip install geopandas plotly
```

### 3. Run Jupyter Notebook

```bash
jupyter notebook
```

Then open `notebooks/01_EDA_StudentLife.ipynb` to start exploring the data.

## 🔧 Data Processing Pipeline

### Step 1: Data Loading
- Load raw sensor files
- Parse timestamps and coordinate systems
- Handle missing data

### Step 2: Data Cleaning
- Remove corrupted files
- Filter invalid entries
- Standardize formats

### Step 3: Feature Engineering
- **Mobility Features**: Total distance, displacement, location entropy
- **Activity Features**: Steps, active minutes, sedentary time
- **Social Features**: Conversation frequency, duration, social clusters
- **Usage Features**: Screen time, app usage patterns
- **Temporal Features**: Daily/weekly aggregates, circadian rhythms

### Step 4: Data Integration
- Align sensor data with survey responses
- Create daily/weekly panels per student
- Merge behavioral features with mental health outcomes

### Step 5: Analysis & Modeling
- Correlation analysis
- Time series analysis
- Predictive modeling (stress, depression, GPA)
- Clustering analysis

## 📊 Key Files in StudentLife Dataset

The dataset contains approximately 1983 files organized by:

- **User ID**: Each student has a unique identifier (e.g., `u001`, `u002`)
- **Data Type**: Different sensor modalities
- **Date**: Daily or timestamped files

### Expected File Patterns:
- `gps/u{user_id}/gps_{date}.csv` - GPS location data
- `accel/u{user_id}/accel_{date}.csv` - Accelerometer data
- `wifi/u{user_id}/wifi_{date}.csv` - WiFi connection data
- `bluetooth/u{user_id}/bluetooth_{date}.csv` - Bluetooth scans
- `conversation/u{user_id}/conversation_{date}.csv` - Conversation logs
- `app/u{user_id}/app_{date}.csv` - App usage data
- `screen/u{user_id}/screen_{date}.csv` - Screen events
- `ema/u{user_id}/ema_{date}.csv` - Self-reported assessments
- `survey/u{user_id}/survey.csv` - Mental health surveys

## 🎓 Research Findings (from original study)

The StudentLife study found significant correlations between:
- **Stress levels** and sleep duration, physical activity
- **Academic performance** and regular sleep patterns, social interaction
- **Mental well-being** and mobility patterns, conversation frequency
- **Term progression**: Stress increases, sleep and activity decrease as term progresses

## 📝 Citation

If you use this dataset, please cite:

```
@inproceedings{wang2014studentlife,
  title={StudentLife: Assessing Mental Health, Academic Performance and Behavioral Trends of College Students using Smartphones},
  author={Wang, Rui and Chen, Fanglin and Chen, Zhenyu and Li, Tianxing and Harari, Gabriella and Tignor, Stefanie and Zhou, Xia and Ben-Zeev, Dror and Campbell, Andrew T},
  booktitle={Proceedings of the ACM Conference on Ubiquitous Computing},
  year={2014},
  organization={ACM}
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Maintainer**: Abubakirov (ahadjon10)

**Last Updated**: July 2026