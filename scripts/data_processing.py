import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from utils import setup_logger
from pathlib import Path

# Initialize logger
logger = setup_logger("processing", Path("logs/processing.log"))


def run_data_processing():
    logger.info(" Starting Data Processing & Validation...")

    # -----------------------------
    # 1. Load Data
    # -----------------------------
    csv_path = "data/raw/sample_data.csv"
    api_path = "data/raw/api_products.csv"

    df = pd.read_csv(csv_path)
    api_df = pd.read_csv(api_path)

    logger.info(f"CSV Loaded: {df.shape}")
    logger.info(f"API Loaded: {api_df.shape}")

    # -----------------------------
    # 2. Data Validation
    # -----------------------------
    logger.info("🔍 Performing Data Validation")

    logger.info(f"Missing Values:\n{df.isnull().sum()}")
    logger.info(f"Duplicate Rows: {df.duplicated().sum()}")

    # -----------------------------
    # 3. Data Cleaning
    # -----------------------------
    logger.info(" Cleaning Data")

    df = df[['user_id', 'product_id', 'event_time', 'event_type']]
    df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')

    df = df.dropna()
    df = df.drop_duplicates()

    logger.info(f"After cleaning: {df.shape}")

    # -----------------------------
    # 4. Fix product_id
    # -----------------------------
    df['product_id'] = df['product_id'] % 20 + 1

    # -----------------------------
    # 5. Merge
    # -----------------------------
    df = df.merge(api_df, on='product_id', how='left')
    logger.info(f"After merge: {df.shape}")

    # -----------------------------
    # 6. EDA
    # -----------------------------
    logger.info("Generating EDA plots")

    os.makedirs("reports/eda_plots", exist_ok=True)

    # Product popularity
    product_counts = df['product_id'].value_counts().head(10)

    plt.figure()
    product_counts.plot(kind='bar')
    plt.title("Top 10 Most Popular Products")
    plt.tight_layout()
    plt.savefig("reports/eda_plots/product_popularity.png")
    plt.close()

    # User activity
    user_counts = df['user_id'].value_counts().head(10)

    plt.figure()
    user_counts.plot(kind='bar')
    plt.title("Top 10 Most Active Users")
    plt.tight_layout()
    plt.savefig("reports/eda_plots/user_activity.png")
    plt.close()

    logger.info("EDA plots saved successfully")

    # -----------------------------
    # 7. Save processed data
    # -----------------------------
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/cleaned_data.csv"

    df.to_csv(output_path, index=False)

    logger.info(f"Processed data saved to {output_path}")

    # -----------------------------
    # 8. Data Quality Report + Images
    # -----------------------------
    logger.info(" Generating Data Quality Report")

    os.makedirs("reports", exist_ok=True)

    doc = SimpleDocTemplate("reports/data_quality_report.pdf")
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Data Quality Report", styles['Title']))
    content.append(Spacer(1, 12))

    # Overview
    content.append(Paragraph(f"Dataset Shape: {df.shape}", styles['Heading2']))
    content.append(Spacer(1, 12))

    # Columns
    columns = ", ".join(df.columns)
    content.append(Paragraph("Columns:", styles['Heading2']))
    content.append(Paragraph(columns, styles['Normal']))
    content.append(Spacer(1, 12))

    # Data types
    dtypes = df.dtypes.to_string()
    content.append(Paragraph("Data Types:", styles['Heading2']))
    content.append(Paragraph(dtypes, styles['Normal']))
    content.append(Spacer(1, 12))

    # Missing values
    missing = df.isnull().sum().to_string()
    content.append(Paragraph("Missing Values:", styles['Heading2']))
    content.append(Paragraph(missing, styles['Normal']))
    content.append(Spacer(1, 12))

    # Duplicates
    duplicates = df.duplicated().sum()
    content.append(Paragraph(f"Duplicate Rows: {duplicates}", styles['Heading2']))
    content.append(Spacer(1, 12))

    # Stats
    content.append(Paragraph("Price Statistics:", styles['Heading2']))
    content.append(Paragraph(f"Mean Price: {df['price'].mean():.2f}", styles['Normal']))
    content.append(Paragraph(f"Min Price: {df['price'].min():.2f}", styles['Normal']))
    content.append(Paragraph(f"Max Price: {df['price'].max():.2f}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Unique counts
    content.append(Paragraph("Unique Counts:", styles['Heading2']))
    content.append(Paragraph(f"Unique Users: {df['user_id'].nunique()}", styles['Normal']))
    content.append(Paragraph(f"Unique Products: {df['product_id'].nunique()}", styles['Normal']))
    content.append(Spacer(1, 20))

    # EDA images
    content.append(Paragraph("EDA Visualizations:", styles['Heading2']))
    content.append(Spacer(1, 12))

    try:
        img1 = Image("reports/eda_plots/product_popularity.png", width=400, height=200)
        content.append(img1)
    except:
        logger.warning("Product popularity image not found")

    try:
        img2 = Image("reports/eda_plots/user_activity.png", width=400, height=200)
        content.append(img2)
    except:
        logger.warning("User activity image not found")

    doc.build(content)

    logger.info(" Data quality report generated successfully")
    logger.info(" Data Processing Completed Successfully")


if __name__ == "__main__":
    run_data_processing()