# Analyzing Car Risk: Predictive Modeling and Insights in the Automotive Domain

## Project Overview

This project explores car risk prediction using a **Gradient Boosting Machine (GBM) classification model**. The dataset consists of automobile features such as engine type, horsepower, price, and more, which are used to predict the `symboling` risk category assigned to cars. In addition to classification, **clustering techniques** such as K-Means and PCA were employed to uncover underlying patterns within the data. The analysis highlights the limitations of small datasets and emphasizes potential strategies for improvement.

## Project Files

- **`final_model.R`**: R file containing the full workflow, including data preprocessing, exploratory data analysis, model building, and evaluation.
- **`Automobile data.csv`**: The dataset used for the project, featuring car specifications and risk levels.
- **`Written_report.pdf`**: The final written report detailing the analysis, results, and recommendations for future improvements.
-  **`Final Project Fall 2023.pdf`**: Guidelines and requirements regarding how to build the model.

## Steps in the Analysis

1. **Data Cleaning & Preprocessing**:
   - Duplicates and missing values were handled by imputation (mean imputation for numerical values).
   - Missing entries encoded as "?" were recoded properly, and features such as `engine location` were removed due to lack of predictive value.
   - Target variable `symboling` was converted into a categorical factor for classification.

2. **Exploratory Data Analysis (EDA)**:
   - Generated a **correlation heatmap** to identify collinear variables and visualized distributions of features.
   - Histograms and box plots were used to detect outliers in key variables like `price`, `compression-ratio`, and `engine size`.
   - Pie charts and bar plots illustrated the breakdown of categorical variables and their relationship with car risk (e.g., Volvo and Subaru cars tended to have lower risk levels, while sports car brands like Porsche showed higher risks).

3. **Classification Model**:
   - The **Gradient Boosting Machine (GBM)** was chosen for its ability to handle complex relationships.
   - **Hyperparameter tuning** focused on shrinkage rates and the number of trees. A final model with 232 trees and a shrinkage rate of 0.001 was selected based on cross-validation performance.
   - Feature selection was based on the importance scores provided by the GBM model.

4. **Clustering Model**:
   - **Principal Component Analysis (PCA)** was used for dimensionality reduction.
   - Applied **K-Means clustering** to group cars based on risk-related attributes, with the **Elbow and Silhouette methods** guiding the selection of the optimal number of clusters.
   - Additional clustering methods such as **K-Prototypes** and **DBSCAN** were explored.

5. **Model Evaluation**:
   - The final classification model achieved an accuracy of 29%, highlighting challenges related to the small dataset and imbalanced classes.
   - Clustering provided valuable insights into car risk profiles, though it did not directly contribute to classification accuracy.

## Key Insights

- The `make` variable (car brand) played a significant role in determining car risk, with luxury and sports car brands showing higher risk levels.
- Price was also a critical factor, with both high-end and budget cars being either very risky or safe compared to their price.
- Clustering revealed latent patterns in the data, grouping cars with similar risk characteristics, though the small dataset limited the robustness of these clusters.

## Results

- **Final Classification Accuracy**: 29% on the test data using Gradient Boosting.
- **Clustering Insights**: K-Means revealed distinct groupings of cars based on risk factors, but more data is required for conclusive insights.

## Future Improvements

- Expanding the dataset and addressing class imbalances will enhance model performance and generalization.
- A comparative analysis of alternative classification models, such as Random Forest and Logistic Regression, could provide more stable predictions.
- Further refinement of clustering models with additional features and improved dimensionality reduction techniques is needed for more accurate insights.
