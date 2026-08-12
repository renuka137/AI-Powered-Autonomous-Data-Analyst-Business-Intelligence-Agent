import os
import pandas as pd
import numpy as np


# ============================================================
# 1. PATHS
# ============================================================

raw_data_path = r"C:\Users\HP\Desktop\Project 1= ShopSphere\shopsphere_dataset\shopsphere_dataset\raw_data"

clean_data_path = r"C:\Users\HP\Desktop\Project 1= ShopSphere\shopsphere_dataset\shopsphere_dataset\clean_data"

# Create clean_data folder if it doesn't exist
os.makedirs(clean_data_path, exist_ok=True)


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

customers = pd.read_csv(
    os.path.join(raw_data_path, "customers.csv")
)

products = pd.read_csv(
    os.path.join(raw_data_path, "products.csv")
)

orders = pd.read_csv(
    os.path.join(raw_data_path, "orders.csv")
)

order_items = pd.read_csv(
    os.path.join(raw_data_path, "order_items.csv")
)

customer_interactions = pd.read_csv(
    os.path.join(raw_data_path, "customer_interactions.csv")
)

marketing_campaigns = pd.read_csv(
    os.path.join(raw_data_path, "marketing_campaigns.csv")
)

print("All raw datasets loaded successfully!")


# ============================================================
# 3. REMOVE EXACT DUPLICATES
# ============================================================

print("\n========== DUPLICATE RECORDS ==========")


# ---------- CUSTOMERS ----------

print(
    "Duplicate customers before:",
    customers.duplicated().sum()
)

customers = customers.drop_duplicates()

print(
    "Duplicate customers after:",
    customers.duplicated().sum()
)


# ---------- PRODUCTS ----------

print(
    "Duplicate products before:",
    products.duplicated().sum()
)

products = products.drop_duplicates()

print(
    "Duplicate products after:",
    products.duplicated().sum()
)


# ---------- ORDERS ----------

print(
    "Duplicate orders before:",
    orders.duplicated().sum()
)

orders = orders.drop_duplicates()

print(
    "Duplicate orders after:",
    orders.duplicated().sum()
)


# ---------- ORDER ITEMS ----------

print(
    "Duplicate order_items before:",
    order_items.duplicated().sum()
)

order_items = order_items.drop_duplicates()

print(
    "Duplicate order_items after:",
    order_items.duplicated().sum()
)


# ---------- CUSTOMER INTERACTIONS ----------

print(
    "Duplicate customer_interactions before:",
    customer_interactions.duplicated().sum()
)

customer_interactions = customer_interactions.drop_duplicates()

print(
    "Duplicate customer_interactions after:",
    customer_interactions.duplicated().sum()
)


# ---------- MARKETING CAMPAIGNS ----------

print(
    "Duplicate marketing_campaigns before:",
    marketing_campaigns.duplicated().sum()
)

marketing_campaigns = marketing_campaigns.drop_duplicates()

print(
    "Duplicate marketing_campaigns after:",
    marketing_campaigns.duplicated().sum()
)


# ============================================================
# 4. HANDLE MISSING VALUES
# ============================================================

print("\n========== MISSING VALUE TREATMENT ==========")


# ---------------- CUSTOMERS ----------------

# Missing city
customers["city"] = customers["city"].fillna("Unknown")


# Missing income
customers["income"] = customers["income"].fillna(
    customers["income"].median()
)


# Missing acquisition channel
customers["acquisition_channel"] = customers[
    "acquisition_channel"
].fillna("Unknown")


# date_of_birth:
# Keep missing values as NULL.
# We should NOT invent a customer's birth date.


# ---------------- PRODUCTS ----------------

# Missing category
products["category"] = products["category"].fillna(
    "Unknown"
)


# Missing brand
products["brand"] = products["brand"].fillna(
    "Unknown"
)


# ---------------- ORDERS ----------------

# Missing shipping city
orders["shipping_city"] = orders[
    "shipping_city"
].fillna("Unknown")


# ---------------- CUSTOMER INTERACTIONS ----------------

customer_interactions[
    "interaction_type"
] = customer_interactions[
    "interaction_type"
].fillna("Unknown")


# ---------------- MARKETING CAMPAIGNS ----------------

marketing_campaigns[
    "campaign_channel"
] = marketing_campaigns[
    "campaign_channel"
].fillna("Unknown")


# ============================================================
# 5. HANDLE INVALID DATE OF BIRTH
# ============================================================

print("\n========== DATE VALIDATION ==========")


# Convert DOB to datetime
customers["date_of_birth"] = pd.to_datetime(
    customers["date_of_birth"],
    errors="coerce"
)


# Dates before 1900 are considered invalid
customers.loc[
    customers["date_of_birth"] < "1900-01-01",
    "date_of_birth"
] = pd.NaT


print(
    "Remaining invalid DOB:",
    (
        customers["date_of_birth"] < "1900-01-01"
    ).sum()
)


# ============================================================
# 6. HANDLE INVALID PRODUCT PRICES
# ============================================================

print("\n========== PRODUCT PRICE CLEANING ==========")


# Negative cost prices are invalid
products.loc[
    products["cost_price"] < 0,
    "cost_price"
] = np.nan


# Zero or negative selling prices are invalid
products.loc[
    products["selling_price"] <= 0,
    "selling_price"
] = np.nan


# ============================================================
# 7. IMPUTE COST PRICE
#    Hierarchical approach
# ============================================================

print("\n========== COST PRICE IMPUTATION ==========")


# Level 1:
# Same subcategory + same brand
products["cost_price"] = products[
    "cost_price"
].fillna(
    products.groupby(
        ["subcategory", "brand"]
    )["cost_price"].transform("median")
)


# Level 2:
# Same subcategory
products["cost_price"] = products[
    "cost_price"
].fillna(
    products.groupby(
        "subcategory"
    )["cost_price"].transform("median")
)


# Level 3:
# Overall median
# Used only if no subcategory value is available
products["cost_price"] = products[
    "cost_price"
].fillna(
    products["cost_price"].median()
)


print(
    "Remaining missing cost_price:",
    products["cost_price"].isnull().sum()
)


# ============================================================
# 8. IMPUTE SELLING PRICE
#    Hierarchical approach
# ============================================================

print("\n========== SELLING PRICE IMPUTATION ==========")


# Level 1:
# Same subcategory + same brand
products["selling_price"] = products[
    "selling_price"
].fillna(
    products.groupby(
        ["subcategory", "brand"]
    )["selling_price"].transform("median")
)


# Level 2:
# Same subcategory
products["selling_price"] = products[
    "selling_price"
].fillna(
    products.groupby(
        "subcategory"
    )["selling_price"].transform("median")
)


# Level 3:
# Overall median
# Used only if no comparable product exists
products["selling_price"] = products[
    "selling_price"
].fillna(
    products["selling_price"].median()
)


print(
    "Remaining missing selling_price:",
    products["selling_price"].isnull().sum()
)


# ============================================================
# 9. HANDLE INVALID RELATIONSHIPS
# ============================================================

print("\n========== REFERENTIAL INTEGRITY ==========")


# ---------- ORDERS → CUSTOMERS ----------

invalid_customer_ids = ~orders[
    "customer_id"
].isin(
    customers["customer_id"]
)


print(
    "Orders removed due to invalid customer ID:",
    invalid_customer_ids.sum()
)


orders = orders[
    ~invalid_customer_ids
].copy()


# ---------- ORDER ITEMS → PRODUCTS ----------

invalid_product_ids = ~order_items[
    "product_id"
].isin(
    products["product_id"]
)


print(
    "Order items removed due to invalid product ID:",
    invalid_product_ids.sum()
)


order_items = order_items[
    ~invalid_product_ids
].copy()


# ---------- ORDER ITEMS → ORDERS ----------

invalid_order_ids = ~order_items[
    "order_id"
].isin(
    orders["order_id"]
)


print(
    "Order items removed due to invalid order ID:",
    invalid_order_ids.sum()
)


order_items = order_items[
    ~invalid_order_ids
].copy()


# ============================================================
# 10. HANDLE INVALID QUANTITY
# ============================================================

print("\n========== QUANTITY CLEANING ==========")


invalid_quantity = (
    order_items["quantity"] <= 0
)


print(
    "Invalid quantity records:",
    invalid_quantity.sum()
)


# Remove invalid order-item records
# because quantity is required to calculate revenue
order_items = order_items[
    ~invalid_quantity
].copy()


print(
    "Remaining invalid quantity:",
    (
        order_items["quantity"] <= 0
    ).sum()
)


# ============================================================
# 11. HANDLE INVALID UNIT PRICE
# ============================================================

print("\n========== UNIT PRICE CLEANING ==========")

# First merge product selling price
order_items = order_items.merge(
    products[
        [
            "product_id",
            "selling_price"
        ]
    ],
    on="product_id",
    how="left"
)

# Now identify invalid unit prices AFTER the merge
invalid_unit_price = (
    order_items["unit_price"] <= 0
)

print(
    "Invalid unit price records:",
    invalid_unit_price.sum()
)

# Replace invalid unit_price with product selling_price
order_items.loc[
    invalid_unit_price,
    "unit_price"
] = order_items.loc[
    invalid_unit_price,
    "selling_price"
]

# Remove temporary column
order_items.drop(
    columns=["selling_price"],
    inplace=True
)

# Final check
print(
    "Remaining invalid unit prices:",
    (
        order_items["unit_price"] <= 0
    ).sum()
)


# ============================================================
# 12. HANDLE ITEM REVENUE
# ============================================================

print("\n========== ITEM REVENUE ==========")


# Calculate revenue using cleaned quantity,
# unit price and discount
calculated_revenue = (
    order_items["quantity"]
    * order_items["unit_price"]
    * (
        1
        - order_items["discount_percent"] / 100
    )
)


# Fill missing item revenue
order_items["item_revenue"] = (
    order_items["item_revenue"]
    .fillna(calculated_revenue)
)


# Recalculate negative item revenue
# because negative revenue is invalid
invalid_revenue = (
    order_items["item_revenue"] < 0
)


print(
    "Negative item revenue before correction:",
    invalid_revenue.sum()
)


order_items.loc[
    invalid_revenue,
    "item_revenue"
] = calculated_revenue[
    invalid_revenue
]


print(
    "Remaining negative item_revenue:",
    (
        order_items["item_revenue"] < 0
    ).sum()
)


# ============================================================
# 13. RECALCULATE PROFIT
# ============================================================

print("\n========== PROFIT CALCULATION ==========")


# Profit = Revenue - Cost
order_items["profit"] = (
    order_items["item_revenue"]
    - order_items["item_cost"]
)


print(
    "Profit calculation completed."
)


# ============================================================
# 14. CALCULATE ORDER VALUE
# ============================================================

print("\n========== ORDER VALUE ==========")


# Sum item revenue for each order
order_totals = (
    order_items
    .groupby("order_id")["item_revenue"]
    .sum()
    .reset_index()
)


# Rename column
order_totals.rename(
    columns={
        "item_revenue":
        "calculated_order_value"
    },
    inplace=True
)


# Add shipping fee
order_totals = order_totals.merge(
    orders[
        [
            "order_id",
            "shipping_fee"
        ]
    ],
    on="order_id",
    how="left"
)


# Final calculated order value
order_totals["calculated_order_value"] = (
    order_totals["calculated_order_value"]
    + order_totals["shipping_fee"]
)


# Merge calculated order value with orders
orders = orders.merge(
    order_totals[
        [
            "order_id",
            "calculated_order_value"
        ]
    ],
    on="order_id",
    how="left"
)


# Check how many original order values
# are different from calculated values
order_value_difference = (
    orders["order_value"]
    - orders["calculated_order_value"]
)


mismatch_count = (
    order_value_difference.abs() > 0.01
).sum()


print(
    "Orders with order_value mismatch:",
    mismatch_count
)


print(
    "Total orders:",
    len(orders)
)


# Check missing calculated order values
print(
    "Missing calculated order_value:",
    orders[
        "calculated_order_value"
    ].isnull().sum()
)


# ============================================================
# 15. HANDLE INVALID ORDER VALUE
# ============================================================

print("\n========== ORDER VALUE VALIDATION ==========")


# Original negative order_value is invalid.
# We keep original order_value for traceability
# and use calculated_order_value for analysis.

print(
    "Negative original order_value:",
    (
        orders["order_value"] < 0
    ).sum()
)


print(
    "Negative calculated_order_value:",
    (
        orders["calculated_order_value"] < 0
    ).sum()
)


# ============================================================
# 16. SELLING PRICE BELOW COST FLAG
# ============================================================

print("\n========== PRODUCT BUSINESS FLAGS ==========")


products["selling_below_cost"] = (
    products["selling_price"]
    < products["cost_price"]
)


print(
    "Products selling below cost:",
    products["selling_below_cost"].sum()
)


# ============================================================
# 17. ORDER DATE
# ============================================================

print("\n========== ORDER DATE ==========")


orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)


# Create a data-quality flag
orders["order_date_missing"] = (
    orders["order_date"].isna()
)


print(
    "Orders with missing order_date:",
    orders["order_date_missing"].sum()
)


# We intentionally keep missing dates as NULL.
# We will exclude them from time-series analysis.


# ============================================================
# 18. FINAL DATASET SUMMARY
# ============================================================

print("\n========== FINAL DATASET SHAPES ==========")


print(
    "Customers:",
    customers.shape
)

print(
    "Products:",
    products.shape
)

print(
    "Orders:",
    orders.shape
)

print(
    "Order Items:",
    order_items.shape
)

print(
    "Customer Interactions:",
    customer_interactions.shape
)

print(
    "Marketing Campaigns:",
    marketing_campaigns.shape
)


# ============================================================
# 19. FINAL DATA QUALITY CHECK
# ============================================================

print("\n========== FINAL DATA QUALITY CHECK ==========")


print(
    "Missing selling_price:",
    products["selling_price"].isnull().sum()
)

print(
    "Invalid unit_price:",
    (
        order_items["unit_price"] <= 0
    ).sum()
)

print(
    "Negative item_revenue:",
    (
        order_items["item_revenue"] < 0
    ).sum()
)

print(
    "Invalid quantity:",
    (
        order_items["quantity"] <= 0
    ).sum()
)


# ============================================================
# 20. SAVE CLEAN DATA
# ============================================================

print("\n========== SAVING CLEAN DATA ==========")


customers.to_csv(
    os.path.join(
        clean_data_path,
        "customers_clean.csv"
    ),
    index=False
)


products.to_csv(
    os.path.join(
        clean_data_path,
        "products_clean.csv"
    ),
    index=False
)


orders.to_csv(
    os.path.join(
        clean_data_path,
        "orders_clean.csv"
    ),
    index=False
)


order_items.to_csv(
    os.path.join(
        clean_data_path,
        "order_items_clean.csv"
    ),
    index=False
)


customer_interactions.to_csv(
    os.path.join(
        clean_data_path,
        "customer_interactions_clean.csv"
    ),
    index=False
)


marketing_campaigns.to_csv(
    os.path.join(
        clean_data_path,
        "marketing_campaigns_clean.csv"
    ),
    index=False
)


print("\nAll cleaned datasets saved successfully!")


# ============================================================
# SAVE CLEAN DATA
# ============================================================

customers.to_csv(
    os.path.join(clean_data_path, "customers_clean.csv"),
    index=False
)

products.to_csv(
    os.path.join(clean_data_path, "products_clean.csv"),
    index=False
)

orders.to_csv(
    os.path.join(clean_data_path, "orders_clean.csv"),
    index=False
)

order_items.to_csv(
    os.path.join(clean_data_path, "order_items_clean.csv"),
    index=False
)

customer_interactions.to_csv(
    os.path.join(
        clean_data_path,
        "customer_interactions_clean.csv"
    ),
    index=False
)

marketing_campaigns.to_csv(
    os.path.join(
        clean_data_path,
        "marketing_campaigns_clean.csv"
    ),
    index=False
)

print("All cleaned datasets saved successfully!")

