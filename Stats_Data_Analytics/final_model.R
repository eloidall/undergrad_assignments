# MGSC401 - Final Project
# Author: Eloi Dallaire

## Imports

install.packages('corrplot')
library(corrplot)
install.packages("plotly")
install.packages("reshape2")
library(reshape2)
install.packages("patchwork")
install.packages("gbm")
library(gbm)
install.packages("caret")
library(caret)
install.packages("xgboost")
library(xgboost)
library(dplyr)
library(ggplot2)
library(plotly)
install.packages("RColorBrewer")
library(RColorBrewer)

automobile <- read.csv("C:\\Users\\eloid\\Documents\\School\\Classes\\Stats. Founds. DA\\Final Project\\Automobile data.csv")


###############################################################################
# 1: Data Pre-processing
###############################################################################
# Check for duplicates
duplicates <- automobile[duplicated(automobile), ]

# Verify data types and Missing values
summary(automobile)
colSums(is.na(automobile))
## NOTES: Missing values '?' don't show

# Understand data a bit more
uniq <- function(df) {
  data.frame(
    feature = names(df),
    val = sapply(df, function(x) toString(unique(x))),
    types = sapply(df, class),
    len = sapply(df, function(x) length(unique(x)))
  )
}
unique_df <- uniq(automobile)

# Drop 'engine.location': almost unary (99%)
automobile <- automobile[, -c(9)]

# Split Numerical and Categorical
numerical_val <- c('normalized.losses','wheel.base','length','width','height',
             'curb.weight', 'engine.size','bore','stroke','compression.ratio',
             'horsepower','peak.rpm', 'city.mpg','highway.mpg','price')
categorical_val <- setdiff(names(automobile), numerical_val)

# Convert selected columns to numeric
automobile[numerical_val] <- lapply(automobile[numerical_val], as.numeric)
colSums(is.na(automobile))
## NOTES: Now missing values are showing as NA

# Handle Missing Values
## Numerical features: replace with mean
columns_to_fill <- c('normalized.losses', 'bore', 'horsepower', 'stroke', 'peak.rpm', 'city.mpg', 'price')
for (f in columns_to_fill) {
  mean_val <- mean(automobile[[f]], na.rm = TRUE)
  automobile[[f]][is.na(automobile[[f]])] <- mean_val
  cat(paste("Mean for", f, ":", mean_val, "\n"))
}
## NOTES: most distribution of variables are symmetric so the use of mean is appropriate
## Categorical: 'num.of.doors: replace with appropriate value ('four')
automobile $ num.of.doors <- gsub("\\?", "four", automobile $ num.of.doors)
# Verify
unique_df <- uniq(automobile)


char_columns <- sapply(automobile, is.character)
automobile[char_columns] <- lapply(automobile[char_columns], as.factor)
automobile$symboling <- as.factor(automobile$symboling)




###############################################################################
# 2: Exploratory Data Analysis (EDA)
###############################################################################
## Numerical features correlation
numeric_columns <- sapply(automobile, is.numeric)
cor_matrix <- cor(automobile[, numeric_columns])
# Plot
ggplot(data = melt(cor_matrix), aes(x = Var1, y = Var2, fill = value, label = round(value, 2))) +
  geom_tile(color = "white") +
  scale_fill_gradientn(colors = c("#C5E8B7", '#ABE098', "#83D475", '#66CDAA', "#20B2AA", '#01796F', '#004953'), values = scales::rescale(c(-1, 0, 1))) +
  theme_minimal() +
  labs(title = "Correlation Heatmap", x = "Variables", y = "Variables") +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1),
    panel.grid = element_blank()
  ) +
  geom_text(aes(color = abs(value) > 0.8), size = 3, vjust = 1, show.legend = FALSE)


## Numerical features distribution: Histogram + boxplot
plot_hist_box <- function(df, variable) {
  # Calculate the bin width
  bin_width <- diff(quantile(df[[variable]], c(0.25, 0.75))) / (2 * IQR(df[[variable]])^0.3333)
  # Plot histogram with trend line
  hist_plot <- ggplot(df, aes(x = !!sym(variable))) +
    geom_histogram(binwidth = bin_width, fill = "darkgreen", color = "lightgreen", alpha = 0.7) +
    labs(title = paste("Histogram of", variable)) +
    theme(plot.title = element_text(hjust = 0.5))  # Center the title
  # Plot boxplot
  box_plot <- ggplot(df, aes(x = 1, y = !!sym(variable))) +
    geom_boxplot(fill = "purple", color = "black", alpha = 0.7) +
    labs(title = paste("Boxplot of", variable)) +
    theme(axis.text.x = element_blank(), axis.ticks.x = element_blank(), plot.title = element_text(hjust = 0.5)) + 
    labs(y = NULL, x = NULL)  # Hide x-axis label
  # Combine
  combined_plot <- patchwork::wrap_plots(hist_plot, box_plot, ncol = 2)
  print(combined_plot)
}
# Plot all numerical features
plot_hist_box(automobile, "horsepower")
plot_hist_box(automobile, "normalized.losses")
plot_hist_box(automobile, "wheel.base")
plot_hist_box(automobile, "length")
plot_hist_box(automobile, "width")
plot_hist_box(automobile, "height")
plot_hist_box(automobile, "curb.weight")
plot_hist_box(automobile, "engine.size")
plot_hist_box(automobile, "bore")
plot_hist_box(automobile, "stroke")
plot_hist_box(automobile, "compression.ratio")
plot_hist_box(automobile, "horsepower")
plot_hist_box(automobile, "peak.rpm")
plot_hist_box(automobile, "city.mpg")
plot_hist_box(automobile, "highway.mpg")
plot_hist_box(automobile, "price")



## Categorical features (10)
# categorical_vars <- c('symboling', 'make','fuel.type','aspiration','num.of.doors','body.style',
#                   'drive.wheels', 'engine.type','num.of.cylinders','fuel.system')

# Barplot (horizontal): make, Hue: symboling
ggplot(ordered_make, aes(y = make, fill = symboling)) +
  geom_bar() +
  scale_fill_viridis_d(option = "C", end = 0.9) +  
  theme_minimal(base_size = 14) +
  labs(title = "Count of Cars by Make and Symboling") +
  theme(legend.position = "right",  # Adjust legend position as needed
        plot.title = element_text(hjust = 0.5)) +
  guides(fill = guide_legend(title = "Symboling"))  # Customize the legend title


# Pie chart
## engine.type
temp_1 <- as.data.frame(table(automobile$engine.type))
colnames(temp_1) <- c("engine.type", "count")
temp_1$fraction <- temp_1$count / sum(temp_1$count)
temp_1$ymax <- cumsum(temp_1$fraction)
temp_1$ymin <- c(0, head(temp_1$ymax, n = -1))
# Plotting the pie chart
ggplot(temp_1, aes(ymax = ymax, ymin = ymin, xmax = 4, xmin = 3, fill = engine.type)) +
  geom_rect() +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  coord_polar(theta = "y") +
  xlim(c(2, 4)) +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, size = 16), legend.title = element_blank()) +
  guides(fill = guide_legend(override.aes = list(shape = NA))) +
  ggtitle("Distribution of Engine Types")

## fuel.system
temp_ <- as.data.frame(table(automobile$fuel.system))
colnames(temp_) <- c("fuel.system", "count")
temp_$fraction <- temp_$count / sum(temp_$count)
temp_$ymax <- cumsum(temp_$fraction)
temp_$ymin <- c(0, head(temp_$ymax, n = -1))
# Plotting the pie chart
ggplot(temp_, aes(ymax = ymax, ymin = ymin, xmax = 4, xmin = 3, fill = fuel.system)) +
  geom_rect() +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  coord_polar(theta = "y") +
  xlim(c(2, 4)) +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, size = 16), legend.title = element_blank()) +
  guides(fill = guide_legend(override.aes = list(shape = NA))) +
  ggtitle("Distribution of Fuel System Types")

## num.of.cylinders
temp_df <- as.data.frame(table(automobile$num.of.cylinders))
colnames(temp_df) <- c("num.of.cylinders", "count")
temp_df$fraction <- temp_df$count / sum(temp_df$count)
temp_df$ymax <- cumsum(temp_df$fraction)
temp_df$ymin <- c(0, head(temp_df$ymax, n = -1))
# Plotting the pie chart
ggplot(temp_df, aes(ymax = ymax, ymin = ymin, xmax = 4, xmin = 3, fill = num.of.cylinders)) +
  geom_rect() +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  coord_polar(theta = "y") +
  xlim(c(2, 4)) +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, size = 16), legend.title = element_blank()) +
  guides(fill = guide_legend(override.aes = list(shape = NA))) +
  ggtitle("Distribution of Cylinder Counts")


# Countplot (vertical): symboling with hue
## Hue: fuel.type
ggplot(automobile, aes(x = symboling, fill = fuel.type)) +
  geom_bar(position = "fill") +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  theme_minimal(base_size = 14) +
  labs(title = "Count of Cars by Symboling and Fuel Type") +
  theme(plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  xlab("Symboling") +
  ylab("Count")
## Hue: aspiration
ggplot(automobile, aes(x = symboling, fill = aspiration)) +
  geom_bar(position = "fill") +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  theme_minimal(base_size = 14) +
  labs(title = "Count of Cars by Symboling and Aspiration") +
  theme(plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  xlab("Symboling") +
  ylab("Count")
## Hue: num.of.doors
ggplot(automobile, aes(x = symboling, fill = num.of.doors)) +
  geom_bar(position = "fill") +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  theme_minimal(base_size = 14) +
  labs(title = "Count of Cars by Symboling and Number of Doors") +
  theme(plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  xlab("Symboling") +
  ylab("Count")
## Hue: drive.wheels
ggplot(automobile, aes(x = symboling, fill = drive.wheels)) +
  geom_bar(position = "fill") +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  theme_minimal(base_size = 14) +
  labs(title = "Count of Cars by Symboling and Drive Wheels") +
  theme(plot.title = element_text(hjust = 0.5), legend.title = element_blank()) +
  xlab("Symboling") +
  ylab("Count")


# Barplot of the mean price over symboling
ggplot(automobile, aes(x = as.factor(symboling), y = price, fill = as.factor(symboling))) +
  stat_summary(fun = "mean", geom = "bar", position = "dodge") +
  scale_fill_viridis_d(option = "C", end = 0.9) +
  theme_minimal(base_size = 14) +
  labs(title = "Mean Price Over Symboling", x = "Symboling", y = "Mean Price") +
  theme(plot.title = element_text(hjust = 0.5), legend.title = element_blank())





###############################################################################
# 3: Classification model
###############################################################################
# 1. Split the data
set.seed(123)  # Set seed for reproducibility
train_indices <- createDataPartition(automobile$symboling, p = 0.67, list = FALSE)
train_data <- automobile[train_indices, ]
test_data <- automobile[-train_indices, ]

X_train <- subset(train_data, select = -symboling)
y_train <- train_data$symboling

X_test <- subset(test_data, select = -symboling)
y_test <- test_data$symboling



#######################
# 3.1: Boosted Forest
#######################
# Base model & Hyperparameters tuning
gbm1 <- gbm(
  symboling ~ ., 
  data = train_data, 
  distribution = "multinomial", 
  n.trees = 500, 
  interaction.depth = 1, # Smaller: less complexity
  n.minobsinnode = 20,  # Greater: less complexity
  shrinkage = 0.005,  # Smaller: more robust
  bag.fraction = 0.5, 
  train.fraction = 0.67, # Bigger: better generalization
  verbose = TRUE
  )
print(gbm1)
## NOTES:
## n.minobsinnode: could not go greater than 20 (sample size too small)
## train.fraction: follows same as initial split
## Look for best balance between lowest TrainDeviance VS ValidDeviance

# Predict and Evaluate model
predict_evaluate <- function(model, test_df, ntrees) {
  
  predictions <- predict(model, newdata = test_df, n.trees = ntrees, type = 'response')
  predicted_df <- as.data.frame(predictions)
  colnames(predicted_df) <- levels(test_df$symboling)
  predicted_df$index <- rownames(test_df)
  rownames(predicted_df) <- NULL
  rownames(predicted_df) <- predicted_df$index
  predicted_df$index <- NULL
  predicted_df$predicted <- colnames(predicted_df)[apply(predicted_df, 1, which.max)]
  predicted_df$actual = test_df$symboling
  predicted_df <- predicted_df[, c(7,8)]
  predicted_df$correct <- predicted_df$predicted == predicted_df$actual
  accuracy <- sum(predicted_df$correct) / length(predicted_df)
  print(accuracy)
}

# Check performance using the out-of-bag (OOB) error
# NOTES: the OOB error typically underestimates the optimal number of iterations
best.iter <- gbm.perf(gbm1, method = "OOB")
print(best.iter)
## NOTES: optimal n.trees = 232

# Print 1st and last tree for curiosity
print(pretty.gbm.tree(gbm1, i.tree = 1))
print(pretty.gbm.tree(gbm1, i.tree = gbm1$n.trees))

# Plot feature importance in ascending order
feature_importance_gbm <- summary(gbm1)
feature_importance_gbm <- feature_importance_gbm %>% arrange(rel.inf)
feature_importance_gbm$var <- factor(feature_importance_gbm$var, levels = feature_importance_gbm$var)

ggplot(feature_importance_gbm, aes(x = rel.inf, y = var, fill = rel.inf)) +
  geom_bar(stat = "identity") +
  scale_fill_viridis_c(option = "C", end = 0.9) +  
  theme_minimal(base_size = 14) +  
  labs(title = "GBM Model - Feature Importance", x = 'Relative Importance', y = 'Features') +
  theme(legend.position = "none", plot.title = element_text(hjust = 0.5)) +
  geom_text(
    aes(label = sprintf("%.3f", rel.inf)),
    position = position_dodge(width = 0.8),  # Adjust the width as needed
    vjust = 0.5, hjust = -0.2, size = 3)


# Re-train new model with optimal n.trees
gbm2 <- gbm(
  symboling ~ ., 
  data = train_data, 
  distribution = "multinomial", 
  n.trees = 3000, 
  interaction.depth = 1, # Smaller: less complexity
  n.minobsinnode = 20,  # Greater: less complexity
  shrinkage = 0.001,  # Smaller: more robust
  bag.fraction = 0.5, 
  train.fraction = 0.67, # Bigger: better generalization
  verbose = TRUE
)
print(gbm2)


# Evaluate model
predict_evaluate(gbm2, test_data, 232)

best.iter <- gbm.perf(gbm2, method = "OOB")
print(best.iter)



