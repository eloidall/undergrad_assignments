# Kickstarter Campaign Success Prediction

## Project Overview

This project aims to predict the success or failure of Kickstarter campaigns using classification and clustering techniques. The analysis uses a dataset scraped from Kickstarter, containing 45 variables related to each project. The main objective is to develop a **classification model** that predicts whether a project will be successful at the time of its launch and to apply **clustering** techniques to group projects based on shared characteristics.

## Project Files

- **`final_model.py`**: Jupyter Notebook with all data exploration, preprocessing, model development, and evaluation steps.
- **`Kickstarter.xlsx`**: Dataset containing Kickstarter project information used in the analysis.
- **`Project_guidelines.pdf`**: This file contains an overview of the project, file structure, and requirements for building models.

## Steps in the Analysis

1. **Data Cleaning & Preprocessing**:
   - Removed canceled/suspended projects and handled missing values.
   - Dropped irrelevant features and features realized after project launch.
   - One-hot encoded categorical variables and applied stratified data splitting.

2. **Exploratory Data Analysis (EDA)**:
   - Analyzed distributions and correlations between variables.
   - Observed relationships, e.g., projects with the `staff_pick` flag showed a higher success rate.

3. **Classification Model**:
   - **Base Model**: Logistic Regression was used as the baseline.
   - **Model Selection**: Random Forest and Gradient Boosting models were built, tuned, and evaluated using cross-validation.
   - **Final Model**: Gradient Boosting, with hyperparameter tuning, achieved the highest accuracy of 75%.
   - Feature selection reduced complexity while maintaining accuracy.

4. **Clustering Model**:
   - PCA was used to reduce dimensions, followed by clustering algorithms (K-Means, K-Prototypes, DBSCAN).
   - **Final Model**: K-Means with 4 clusters was selected based on Silhouette scores and provided insights into project characteristics.

5. **Model Evaluation**:
   - Evaluation metrics included **Accuracy**, **Precision**, **Recall**, and **F1 Score**.
   - Outlier removal and feature selection helped improve model robustness.

## Key Insights

- Projects flagged as `staff_pick` and projects in categories like `Web` and `Software` have higher success rates.
- Clusters revealed insights about launch times and project characteristics, with some clusters showing better success rates during specific times or regions.

## Results

- **Final Classification Accuracy**: 75% on the test data using Gradient Boosting.
- **Clustering Insights**: Identified distinct project groupings based on launch times, categories, and region.

## Future Improvements

- Further refinement of clustering techniques to improve cohesion and separation.
- Implementation of real-time monitoring for live Kickstarter campaigns.
