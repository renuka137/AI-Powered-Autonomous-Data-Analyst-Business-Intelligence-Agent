# ============================================================
# SHOPSPHERE - POWER BI DATA PREPARATION
# ============================================================
# Purpose:
# Prepare cleaned ShopSphere datasets for Power BI.
#
# Input:
#   customers_clean.csv
#   products_clean.csv
#   orders_clean.csv
#   order_items_clean.csv
#   customer_interactions_clean.csv
#   marketing_campaigns_clean.csv
#
# Output:
#   Power BI-ready CSV files inside:
#   power_bi_data/
#
# IMPORTANT:
# calculated_order_value is used as the primary revenue field.
# Original order_value is retained only for comparison/reference.
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:,.2f}".format)


print("=" * 70)
print("SHOPSPHERE POWER BI DATA PREPARATION")
print("=" * 70)


# ============================================================
# 2. PATHS
# ============================================================

clean_data_path = (
    r"C:\Users\HP\Desktop\Project 1= ShopSphere"
    r"\shopsphere_dataset\shopsphere_dataset\clean_data"
)


power_bi_path = (
    r"C:\Users\HP\Desktop\Project 1= ShopSphere"
    r"\shopsphere_dataset\shopsphere_dataset\power_bi_data"
)


# Create Power BI output folder if it does not exist

os.makedirs(power_bi_path, exist_ok=True)


print("\nInput path:")
print(clean_data_path)

print("\nPower BI output path:")
print(power_bi_path)


# ============================================================
# 3. LOAD CLEANED DATA
# ============================================================

print("\n========== LOADING DATA ==========")


customers = pd.read_csv(
    os.path.join(
        clean_data_path,
        "customers_clean.csv"
    )
)


products = pd.read_csv(
    os.path.join(
        clean_data_path,
        "products_clean.csv"
    )
)


orders = pd.read_csv(
    os.path.join(
        clean_data_path,
        "orders_clean.csv"
    )
)


order_items = pd.read_csv(
    os.path.join(
        clean_data_path,
        "order_items_clean.csv"
    )
)


customer_interactions = pd.read_csv(
    os.path.join(
        clean_data_path,
        "customer_interactions_clean.csv"
    )
)


marketing_campaigns = pd.read_csv(
    os.path.join(
        clean_data_path,
        "marketing_campaigns_clean.csv"
    )
)


print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print(
    "Customer Interactions:",
    customer_interactions.shape
)
print(
    "Marketing Campaigns:",
    marketing_campaigns.shape
)


# ============================================================
# 4. DATE CONVERSION
# ============================================================

print("\n========== DATE CONVERSION ==========")


date_columns = {
    "customers": ["date_of_birth", "signup_date"],
    "products": ["launch_date"],
    "orders": ["order_date"],
    "customer_interactions": ["interaction_datetime"],
    "marketing_campaigns": ["campaign_date"]
}


for column in date_columns["customers"]:

    if column in customers.columns:

        customers[column] = pd.to_datetime(
            customers[column],
            errors="coerce"
        )


for column in date_columns["products"]:

    if column in products.columns:

        products[column] = pd.to_datetime(
            products[column],
            errors="coerce"
        )


for column in date_columns["orders"]:

    if column in orders.columns:

        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )


for column in date_columns["customer_interactions"]:

    if column in customer_interactions.columns:

        customer_interactions[column] = pd.to_datetime(
            customer_interactions[column],
            errors="coerce"
        )


for column in date_columns["marketing_campaigns"]:

    if column in marketing_campaigns.columns:

        marketing_campaigns[column] = pd.to_datetime(
            marketing_campaigns[column],
            errors="coerce"
        )


print("Date conversion completed.")


# ============================================================
# 5. CHECK REQUIRED COLUMNS
# ============================================================

print("\n========== COLUMN VALIDATION ==========")


required_columns = {

    "customers": [
        "customer_id"
    ],

    "products": [
        "product_id"
    ],

    "orders": [
        "order_id",
        "customer_id",
        "order_date",
        "order_status",
        "shipping_fee",
        "discount_amount",
        "calculated_order_value"
    ],

    "order_items": [
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_percent",
        "item_revenue",
        "item_cost",
        "profit"
    ],

    "customer_interactions": [
        "interaction_id",
        "customer_id",
        "interaction_type",
        "device_type",
        "converted",
        "session_duration_min"
    ],

    "marketing_campaigns": [
        "campaign_id",
        "campaign_name",
        "campaign_channel",
        "impression",
        "clicked",
        "converted",
        "campaign_cost",
        "attributed_revenue"
    ]
}


dataset_objects = {
    "customers": customers,
    "products": products,
    "orders": orders,
    "order_items": order_items,
    "customer_interactions": customer_interactions,
    "marketing_campaigns": marketing_campaigns
}


for dataset_name, columns in required_columns.items():

    df = dataset_objects[dataset_name]

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"{dataset_name} is missing columns: "
            f"{missing_columns}"
        )


print("All required columns are available.")


# ============================================================
# 6. CREATE VALID REVENUE ORDERS
# ============================================================

print("\n========== REVENUE DATA PREPARATION ==========")


# Do not change original orders dataframe.

valid_revenue_orders = orders[
    orders["calculated_order_value"].notna()
].copy()


print(
    "Total source orders:",
    len(orders)
)


print(
    "Orders with valid calculated revenue:",
    len(valid_revenue_orders)
)


print(
    "Orders excluded from revenue calculations:",
    orders["calculated_order_value"].isna().sum()
)


# ============================================================
# 7. ORDER TIME FEATURES
# ============================================================

print("\n========== TIME FEATURES ==========")


valid_revenue_orders["year"] = (
    valid_revenue_orders["order_date"].dt.year
)


valid_revenue_orders["month_number"] = (
    valid_revenue_orders["order_date"].dt.month
)


valid_revenue_orders["month_name"] = (
    valid_revenue_orders["order_date"].dt.month_name()
)


valid_revenue_orders["quarter_number"] = (
    valid_revenue_orders["order_date"].dt.quarter
)


valid_revenue_orders["quarter"] = (
    "Q"
    + valid_revenue_orders["quarter_number"]
    .fillna(0)
    .astype(int)
    .astype(str)
)


valid_revenue_orders["year_month"] = (
    valid_revenue_orders["order_date"]
    .dt.to_period("M")
    .astype(str)
)


valid_revenue_orders["year_quarter"] = (
    valid_revenue_orders["year"].astype("Int64")
    .astype(str)
    + "-"
    + valid_revenue_orders["quarter"]
)


print("Time features created.")


# ============================================================
# 8. FACT ORDERS TABLE
# ============================================================

print("\n========== FACT ORDERS ==========")


fact_orders_columns = [
    "order_id",
    "customer_id",
    "order_date",
    "order_status",
    "payment_method",
    "shipping_region",
    "shipping_fee",
    "discount_amount",
    "order_value",
    "calculated_order_value",
    "year",
    "month_number",
    "month_name",
    "quarter_number",
    "quarter",
    "year_month",
    "year_quarter"
]


fact_orders_columns = [
    column
    for column in fact_orders_columns
    if column in valid_revenue_orders.columns
]


fact_orders = valid_revenue_orders[
    fact_orders_columns
].copy()


print(
    "Fact Orders rows:",
    len(fact_orders)
)


# ============================================================
# 9. FACT ORDER ITEMS TABLE
# ============================================================

print("\n========== FACT ORDER ITEMS ==========")


fact_order_items = order_items.copy()


print(
    "Fact Order Items rows:",
    len(fact_order_items)
)


# ============================================================
# 10. FACT SALES TABLE
# ============================================================
# Combines order item information with product information
# and order date information.
# ============================================================

print("\n========== FACT SALES ==========")


fact_sales = (
    order_items
    .merge(
        products,
        on="product_id",
        how="left",
        suffixes=("", "_product")
    )
    .merge(
        valid_revenue_orders[
            [
                "order_id",
                "customer_id",
                "order_date",
                "order_status",
                "shipping_region",
                "year",
                "month_number",
                "month_name",
                "quarter_number",
                "quarter",
                "year_month",
                "year_quarter"
            ]
        ],
        on="order_id",
        how="inner"
    )
)


print(
    "Fact Sales rows:",
    len(fact_sales)
)


# ============================================================
# 11. DIM CUSTOMER
# ============================================================

print("\n========== DIM CUSTOMER ==========")


dim_customer = customers.copy()


print(
    "Dim Customer rows:",
    len(dim_customer)
)


# ============================================================
# 12. DIM PRODUCT
# ============================================================

print("\n========== DIM PRODUCT ==========")


dim_product = products.copy()


print(
    "Dim Product rows:",
    len(dim_product)
)


# ============================================================
# 13. DIM DATE
# ============================================================

print("\n========== DIM DATE ==========")


valid_dates = valid_revenue_orders[
    "order_date"
].dropna()


if len(valid_dates) > 0:

    min_date = valid_dates.min().normalize()
    max_date = valid_dates.max().normalize()

    date_range = pd.date_range(
        start=min_date,
        end=max_date,
        freq="D"
    )

    dim_date = pd.DataFrame({
        "date": date_range
    })

    dim_date["year"] = (
        dim_date["date"].dt.year
    )

    dim_date["month_number"] = (
        dim_date["date"].dt.month
    )

    dim_date["month_name"] = (
        dim_date["date"].dt.month_name()
    )

    dim_date["month_short"] = (
        dim_date["date"].dt.strftime("%b")
    )

    dim_date["quarter_number"] = (
        dim_date["date"].dt.quarter
    )

    dim_date["quarter"] = (
        "Q"
        + dim_date["quarter_number"].astype(str)
    )

    dim_date["year_month"] = (
        dim_date["date"]
        .dt.to_period("M")
        .astype(str)
    )

    dim_date["year_quarter"] = (
        dim_date["year"].astype(str)
        + "-"
        + dim_date["quarter"]
    )

    dim_date["day"] = (
        dim_date["date"].dt.day
    )

    dim_date["day_name"] = (
        dim_date["date"].dt.day_name()
    )

    dim_date["day_of_week"] = (
        dim_date["date"].dt.dayofweek + 1
    )

else:

    dim_date = pd.DataFrame()


print(
    "Dim Date rows:",
    len(dim_date)
)


# ============================================================
# 14. KPI SUMMARY
# ============================================================

print("\n========== KPI SUMMARY ==========")


total_revenue = (
    valid_revenue_orders[
        "calculated_order_value"
    ].sum()
)


total_orders = (
    orders["order_id"].nunique()
)


valid_orders_count = (
    valid_revenue_orders["order_id"].nunique()
)


total_customers = (
    customers["customer_id"].nunique()
)


average_order_value = (
    valid_revenue_orders[
        "calculated_order_value"
    ].mean()
)


total_product_revenue = (
    order_items["item_revenue"].sum()
)


total_profit = (
    order_items["profit"].sum()
)


profit_margin = (
    total_profit / total_product_revenue * 100
    if total_product_revenue != 0
    else 0
)


cancelled_orders = orders[
    orders["order_status"]
    .astype(str)
    .str.lower()
    .eq("cancelled")
]["order_id"].nunique()


cancellation_rate = (
    cancelled_orders / total_orders * 100
    if total_orders != 0
    else 0
)


kpi_summary = pd.DataFrame({

    "metric": [
        "Total Revenue",
        "Total Source Orders",
        "Valid Revenue Orders",
        "Total Customers",
        "Average Order Value",
        "Total Product Revenue",
        "Total Profit",
        "Profit Margin %",
        "Cancelled Orders",
        "Cancellation Rate %"
    ],

    "value": [
        total_revenue,
        total_orders,
        valid_orders_count,
        total_customers,
        average_order_value,
        total_product_revenue,
        total_profit,
        profit_margin,
        cancelled_orders,
        cancellation_rate
    ]

})


print(kpi_summary.to_string(index=False))


# ============================================================
# 15. MONTHLY SALES
# ============================================================

print("\n========== MONTHLY SALES ==========")


monthly_sales = (
    valid_revenue_orders
    .dropna(subset=["order_date"])
    .groupby(
        [
            "year",
            "month_number",
            "month_name",
            "year_month"
        ],
        as_index=False
    )
    .agg(
        revenue=(
            "calculated_order_value",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        ),

        average_order_value=(
            "calculated_order_value",
            "mean"
        )
    )
)


monthly_sales = monthly_sales.sort_values(
    [
        "year",
        "month_number"
    ]
)


print(
    "Monthly sales rows:",
    len(monthly_sales)
)


# ============================================================
# 16. QUARTERLY SALES
# ============================================================

print("\n========== QUARTERLY SALES ==========")


quarterly_sales = (
    valid_revenue_orders
    .dropna(subset=["order_date"])
    .groupby(
        [
            "year",
            "quarter_number",
            "quarter",
            "year_quarter"
        ],
        as_index=False
    )
    .agg(
        revenue=(
            "calculated_order_value",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        ),

        average_order_value=(
            "calculated_order_value",
            "mean"
        )
    )
)


quarterly_sales = quarterly_sales.sort_values(
    [
        "year",
        "quarter_number"
    ]
)


quarterly_sales["revenue_growth_pct"] = (
    quarterly_sales["revenue"]
    .pct_change()
    * 100
)


# ============================================================
# 17. CATEGORY PERFORMANCE
# ============================================================

print("\n========== CATEGORY PERFORMANCE ==========")


category_performance = (
    order_items
    .merge(
        products[
            [
                "product_id",
                "category",
                "subcategory",
                "brand"
            ]
        ],
        on="product_id",
        how="left"
    )
    .groupby(
        "category",
        as_index=False
    )
    .agg(
        revenue=(
            "item_revenue",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        ),

        units_sold=(
            "quantity",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        )
    )
)


category_performance["profit_margin_pct"] = np.where(
    category_performance["revenue"] != 0,
    (
        category_performance["profit"]
        /
        category_performance["revenue"]
        * 100
    ),
    0
)


category_performance = category_performance.sort_values(
    "revenue",
    ascending=False
)


# ============================================================
# 18. SUBCATEGORY PERFORMANCE
# ============================================================

print("\n========== SUBCATEGORY PERFORMANCE ==========")


subcategory_performance = (
    order_items
    .merge(
        products[
            [
                "product_id",
                "category",
                "subcategory"
            ]
        ],
        on="product_id",
        how="left"
    )
    .groupby(
        [
            "category",
            "subcategory"
        ],
        as_index=False
    )
    .agg(
        revenue=(
            "item_revenue",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        ),

        units_sold=(
            "quantity",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        )
    )
)


subcategory_performance["profit_margin_pct"] = np.where(
    subcategory_performance["revenue"] != 0,
    (
        subcategory_performance["profit"]
        /
        subcategory_performance["revenue"]
        * 100
    ),
    0
)


subcategory_performance = (
    subcategory_performance
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ============================================================
# 19. PRODUCT PERFORMANCE
# ============================================================

print("\n========== PRODUCT PERFORMANCE ==========")


product_performance = (
    order_items
    .merge(
        products[
            [
                "product_id",
                "product_name",
                "category",
                "subcategory",
                "brand"
            ]
        ],
        on="product_id",
        how="left"
    )
    .groupby(
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "brand"
        ],
        as_index=False
    )
    .agg(
        revenue=(
            "item_revenue",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        ),

        units_sold=(
            "quantity",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        )
    )
)


product_performance["profit_margin_pct"] = np.where(
    product_performance["revenue"] != 0,
    (
        product_performance["profit"]
        /
        product_performance["revenue"]
        * 100
    ),
    0
)


product_performance = (
    product_performance
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ============================================================
# 20. CUSTOMER PERFORMANCE
# ============================================================

print("\n========== CUSTOMER PERFORMANCE ==========")


customer_performance = (
    valid_revenue_orders
    .groupby(
        "customer_id",
        as_index=False
    )
    .agg(
        total_revenue=(
            "calculated_order_value",
            "sum"
        ),

        total_orders=(
            "order_id",
            "nunique"
        ),

        average_order_value=(
            "calculated_order_value",
            "mean"
        )
    )
)


customer_performance = customer_performance.merge(
    customers[
        [
            "customer_id",
            "customer_segment",
            "customer_status",
            "acquisition_channel",
            "region"
        ]
    ],
    on="customer_id",
    how="left"
)


customer_performance["customer_type"] = np.where(
    customer_performance["total_orders"] > 1,
    "Repeat Customer",
    "One-Time Customer"
)


customer_performance = (
    customer_performance
    .sort_values(
        "total_revenue",
        ascending=False
    )
)


# ============================================================
# 21. CUSTOMER SEGMENT PERFORMANCE
# ============================================================

print("\n========== CUSTOMER SEGMENT PERFORMANCE ==========")


segment_performance = (
    customer_performance
    .groupby(
        "customer_segment",
        as_index=False
    )
    .agg(
        revenue=(
            "total_revenue",
            "sum"
        ),

        customers=(
            "customer_id",
            "nunique"
        ),

        orders=(
            "total_orders",
            "sum"
        )
    )
)


segment_performance["revenue_per_customer"] = np.where(
    segment_performance["customers"] != 0,
    (
        segment_performance["revenue"]
        /
        segment_performance["customers"]
    ),
    0
)


segment_performance = (
    segment_performance
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ============================================================
# 22. REGION PERFORMANCE
# ============================================================

print("\n========== REGION PERFORMANCE ==========")


region_performance = (
    valid_revenue_orders
    .groupby(
        "shipping_region",
        as_index=False
    )
    .agg(
        revenue=(
            "calculated_order_value",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        ),

        average_order_value=(
            "calculated_order_value",
            "mean"
        )
    )
)


region_performance = (
    region_performance
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ============================================================
# 23. PAYMENT METHOD PERFORMANCE
# ============================================================

print("\n========== PAYMENT METHOD PERFORMANCE ==========")


payment_performance = (
    valid_revenue_orders
    .groupby(
        "payment_method",
        as_index=False
    )
    .agg(
        revenue=(
            "calculated_order_value",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        ),

        average_order_value=(
            "calculated_order_value",
            "mean"
        )
    )
)


payment_performance = (
    payment_performance
    .sort_values(
        "revenue",
        ascending=False
    )
)


# ============================================================
# 24. ORDER STATUS PERFORMANCE
# ============================================================

print("\n========== ORDER STATUS PERFORMANCE ==========")


order_status_performance = (
    orders
    .groupby(
        "order_status",
        as_index=False
    )
    .agg(
        orders=(
            "order_id",
            "nunique"
        ),

        revenue=(
            "calculated_order_value",
            "sum"
        )
    )
)


# ============================================================
# 25. DISCOUNT PERFORMANCE
# ============================================================

print("\n========== DISCOUNT PERFORMANCE ==========")


discount_performance = valid_revenue_orders[
    [
        "order_id",
        "calculated_order_value",
        "discount_amount",
        "shipping_fee"
    ]
].copy()


discount_performance["discount_rate_pct"] = np.where(
    (
        discount_performance["calculated_order_value"]
        +
        discount_performance["discount_amount"]
    ) != 0,

    discount_performance["discount_amount"]
    /
    (
        discount_performance["calculated_order_value"]
        +
        discount_performance["discount_amount"]
    )
    * 100,

    0
)


# ============================================================
# 26. MARKETING CAMPAIGN PERFORMANCE
# ============================================================

print("\n========== MARKETING CAMPAIGN PERFORMANCE ==========")


campaign_performance = (
    marketing_campaigns
    .groupby(
        [
            "campaign_id",
            "campaign_name",
            "campaign_channel"
        ],
        as_index=False
    )
    .agg(
        impressions=(
            "impression",
            "sum"
        ),

        clicks=(
            "clicked",
            "sum"
        ),

        conversions=(
            "converted",
            "sum"
        ),

        campaign_cost=(
            "campaign_cost",
            "sum"
        ),

        attributed_revenue=(
            "attributed_revenue",
            "sum"
        )
    )
)


campaign_performance["CTR_pct"] = np.where(
    campaign_performance["impressions"] != 0,

    campaign_performance["clicks"]
    /
    campaign_performance["impressions"]
    * 100,

    0
)


campaign_performance["conversion_rate_pct"] = np.where(
    campaign_performance["clicks"] != 0,

    campaign_performance["conversions"]
    /
    campaign_performance["clicks"]
    * 100,

    0
)


campaign_performance["ROAS"] = np.where(
    campaign_performance["campaign_cost"] != 0,

    campaign_performance["attributed_revenue"]
    /
    campaign_performance["campaign_cost"],

    0
)


# ============================================================
# 27. MARKETING CHANNEL PERFORMANCE
# ============================================================

print("\n========== MARKETING CHANNEL PERFORMANCE ==========")


channel_performance = (
    marketing_campaigns
    .groupby(
        "campaign_channel",
        as_index=False
    )
    .agg(
        impressions=(
            "impression",
            "sum"
        ),

        clicks=(
            "clicked",
            "sum"
        ),

        conversions=(
            "converted",
            "sum"
        ),

        cost=(
            "campaign_cost",
            "sum"
        ),

        revenue=(
            "attributed_revenue",
            "sum"
        )
    )
)


channel_performance["CTR_pct"] = np.where(
    channel_performance["impressions"] != 0,

    channel_performance["clicks"]
    /
    channel_performance["impressions"]
    * 100,

    0
)


channel_performance["conversion_rate_pct"] = np.where(
    channel_performance["clicks"] != 0,

    channel_performance["conversions"]
    /
    channel_performance["clicks"]
    * 100,

    0
)


channel_performance["ROAS"] = np.where(
    channel_performance["cost"] != 0,

    channel_performance["revenue"]
    /
    channel_performance["cost"],

    0
)


channel_performance = (
    channel_performance
    .sort_values(
        "ROAS",
        ascending=False
    )
)


# ============================================================
# 28. CUSTOMER INTERACTION PERFORMANCE
# ============================================================

print("\n========== CUSTOMER INTERACTION PERFORMANCE ==========")


interaction_performance = (
    customer_interactions
    .groupby(
        "interaction_type",
        as_index=False
    )
    .agg(
        interactions=(
            "interaction_id",
            "count"
        ),

        conversions=(
            "converted",
            "sum"
        ),

        avg_session_duration=(
            "session_duration_min",
            "mean"
        )
    )
)


interaction_performance["conversion_rate_pct"] = np.where(
    interaction_performance["interactions"] != 0,

    interaction_performance["conversions"]
    /
    interaction_performance["interactions"]
    * 100,

    0
)


# ============================================================
# 29. DEVICE PERFORMANCE
# ============================================================

print("\n========== DEVICE PERFORMANCE ==========")


device_performance = (
    customer_interactions
    .groupby(
        "device_type",
        as_index=False
    )
    .agg(
        interactions=(
            "interaction_id",
            "count"
        ),

        conversions=(
            "converted",
            "sum"
        ),

        avg_session_duration=(
            "session_duration_min",
            "mean"
        )
    )
)


device_performance["conversion_rate_pct"] = np.where(
    device_performance["interactions"] != 0,

    device_performance["conversions"]
    /
    device_performance["interactions"]
    * 100,

    0
)


# ============================================================
# 30. CUSTOMER RETENTION
# ============================================================

print("\n========== CUSTOMER RETENTION ==========")


retention_summary = (
    customer_performance
    .groupby(
        "customer_type",
        as_index=False
    )
    .agg(
        customers=(
            "customer_id",
            "nunique"
        ),

        revenue=(
            "total_revenue",
            "sum"
        )
    )
)


total_customer_count = (
    retention_summary["customers"].sum()
)


retention_summary["percentage"] = np.where(
    total_customer_count != 0,

    retention_summary["customers"]
    /
    total_customer_count
    * 100,

    0
)


# ============================================================
# 31. YEARLY PERFORMANCE
# ============================================================

print("\n========== YEARLY PERFORMANCE ==========")


yearly_performance = (
    valid_revenue_orders
    .dropna(subset=["order_date"])
    .groupby(
        "year",
        as_index=False
    )
    .agg(
        revenue=(
            "calculated_order_value",
            "sum"
        ),

        orders=(
            "order_id",
            "nunique"
        ),

        average_order_value=(
            "calculated_order_value",
            "mean"
        )
    )
)


yearly_performance["revenue_growth_pct"] = (
    yearly_performance["revenue"]
    .pct_change()
    * 100
)


# ============================================================
# 32. CATEGORY QUARTERLY PERFORMANCE
# ============================================================

print("\n========== CATEGORY QUARTERLY PERFORMANCE ==========")


category_quarterly = (
    order_items
    .merge(
        valid_revenue_orders[
            [
                "order_id",
                "year",
                "quarter",
                "quarter_number"
            ]
        ],
        on="order_id",
        how="inner"
    )
    .merge(
        products[
            [
                "product_id",
                "category"
            ]
        ],
        on="product_id",
        how="left"
    )
    .groupby(
        [
            "year",
            "quarter_number",
            "quarter",
            "category"
        ],
        as_index=False
    )
    .agg(
        revenue=(
            "item_revenue",
            "sum"
        ),

        profit=(
            "profit",
            "sum"
        ),

        units_sold=(
            "quantity",
            "sum"
        )
    )
)


category_quarterly["profit_margin_pct"] = np.where(
    category_quarterly["revenue"] != 0,

    category_quarterly["profit"]
    /
    category_quarterly["revenue"]
    * 100,

    0
)


# ============================================================
# 33. CUSTOMER ACQUISITION PERFORMANCE
# ============================================================

print("\n========== CUSTOMER ACQUISITION PERFORMANCE ==========")


acquisition_performance = (
    customer_performance
    .groupby(
        "acquisition_channel",
        as_index=False
    )
    .agg(
        customers=(
            "customer_id",
            "nunique"
        ),

        revenue=(
            "total_revenue",
            "sum"
        ),

        orders=(
            "total_orders",
            "sum"
        )
    )
)


acquisition_performance["revenue_per_customer"] = np.where(
    acquisition_performance["customers"] != 0,

    acquisition_performance["revenue"]
    /
    acquisition_performance["customers"],

    0
)


# ============================================================
# 34. SAVE FUNCTION
# ============================================================

def save_csv(df, filename):

    output_file = os.path.join(
        power_bi_path,
        filename
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Saved: {filename:<45} "
        f"Rows: {len(df):,}"
    )


# ============================================================
# 35. SAVE POWER BI TABLES
# ============================================================

print("\n========== SAVING POWER BI TABLES ==========")


save_csv(
    fact_orders,
    "fact_orders.csv"
)


save_csv(
    fact_order_items,
    "fact_order_items.csv"
)


save_csv(
    fact_sales,
    "fact_sales.csv"
)


save_csv(
    dim_customer,
    "dim_customer.csv"
)


save_csv(
    dim_product,
    "dim_product.csv"
)


save_csv(
    dim_date,
    "dim_date.csv"
)


save_csv(
    kpi_summary,
    "kpi_summary.csv"
)


save_csv(
    monthly_sales,
    "monthly_sales.csv"
)


save_csv(
    quarterly_sales,
    "quarterly_sales.csv"
)


save_csv(
    yearly_performance,
    "yearly_performance.csv"
)


save_csv(
    category_performance,
    "category_performance.csv"
)


save_csv(
    subcategory_performance,
    "subcategory_performance.csv"
)


save_csv(
    product_performance,
    "product_performance.csv"
)


save_csv(
    customer_performance,
    "customer_performance.csv"
)


save_csv(
    segment_performance,
    "segment_performance.csv"
)


save_csv(
    region_performance,
    "region_performance.csv"
)


save_csv(
    payment_performance,
    "payment_performance.csv"
)


save_csv(
    order_status_performance,
    "order_status_performance.csv"
)


save_csv(
    discount_performance,
    "discount_performance.csv"
)


save_csv(
    campaign_performance,
    "campaign_performance.csv"
)


save_csv(
    channel_performance,
    "channel_performance.csv"
)


save_csv(
    interaction_performance,
    "interaction_performance.csv"
)


save_csv(
    device_performance,
    "device_performance.csv"
)


save_csv(
    retention_summary,
    "retention_summary.csv"
)


save_csv(
    category_quarterly,
    "category_quarterly.csv"
)


save_csv(
    acquisition_performance,
    "acquisition_performance.csv"
)


# ============================================================
# 36. FINAL VALIDATION
# ============================================================

print("\n========== POWER BI DATA VALIDATION ==========")


print(
    "Total Revenue: ₹"
    f"{total_revenue:,.2f}"
)


print(
    "Total Source Orders:",
    total_orders
)


print(
    "Valid Revenue Orders:",
    valid_orders_count
)


print(
    "Orders excluded from revenue calculations:",
    total_orders - valid_orders_count
)


print(
    "Total Customers:",
    total_customers
)


print(
    "Total Product Revenue: ₹"
    f"{total_product_revenue:,.2f}"
)


print(
    "Total Profit: ₹"
    f"{total_profit:,.2f}"
)


print(
    "Profit Margin:",
    f"{profit_margin:.2f}%"
)


print(
    "Cancellation Rate:",
    f"{cancellation_rate:.2f}%"
)


# ============================================================
# 37. BEST PERFORMERS
# ============================================================

print("\n========== TOP BUSINESS PERFORMERS ==========")


if not category_performance.empty:

    best_category = (
        category_performance
        .sort_values(
            "revenue",
            ascending=False
        )
        .iloc[0]
    )

    print(
        "Highest Revenue Category:",
        best_category["category"]
    )

    print(
        "Category Revenue: ₹"
        f"{best_category['revenue']:,.2f}"
    )


if not segment_performance.empty:

    best_segment = (
        segment_performance
        .sort_values(
            "revenue",
            ascending=False
        )
        .iloc[0]
    )

    print(
        "\nHighest Revenue Customer Segment:",
        best_segment["customer_segment"]
    )

    print(
        "Segment Revenue: ₹"
        f"{best_segment['revenue']:,.2f}"
    )


if not channel_performance.empty:

    best_channel = (
        channel_performance
        .sort_values(
            "ROAS",
            ascending=False
        )
        .iloc[0]
    )

    print(
        "\nHighest ROAS Marketing Channel:",
        best_channel["campaign_channel"]
    )

    print(
        "ROAS:",
        f"{best_channel['ROAS']:.2f}"
    )


if not product_performance.empty:

    best_product = (
        product_performance
        .sort_values(
            "revenue",
            ascending=False
        )
        .iloc[0]
    )

    print(
        "\nHighest Revenue Product:",
        best_product["product_name"]
    )

    print(
        "Product Revenue: ₹"
        f"{best_product['revenue']:,.2f}"
    )


# ============================================================
# 38. OUTPUT FILE COUNT
# ============================================================

output_files = [
    file
    for file in os.listdir(power_bi_path)
    if file.lower().endswith(".csv")
]


print("\n========== OUTPUT SUMMARY ==========")


print(
    "Power BI CSV files created:",
    len(output_files)
)


for file in sorted(output_files):

    print(
        " -",
        file
    )


# ============================================================
# 39. COMPLETED
# ============================================================

print("\n" + "=" * 70)

print(
    "POWER BI DATA PREPARATION COMPLETED SUCCESSFULLY!"
)

print(
    "Output folder:"
)

print(
    power_bi_path
)

print("=" * 70)