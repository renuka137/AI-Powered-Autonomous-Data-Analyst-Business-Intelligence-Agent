import os
import pandas as pd
import numpy as np


# ============================================================
# 1. PATH
# ============================================================

clean_data_path = r"C:\Users\HP\Desktop\Project 1= ShopSphere\shopsphere_dataset\shopsphere_dataset\clean_data"


# ============================================================
# 2. LOAD CLEANED DATA
# ============================================================

customers = pd.read_csv(
    os.path.join(clean_data_path, "customers_clean.csv")
)

products = pd.read_csv(
    os.path.join(clean_data_path, "products_clean.csv")
)

orders = pd.read_csv(
    os.path.join(clean_data_path, "orders_clean.csv")
)

order_items = pd.read_csv(
    os.path.join(clean_data_path, "order_items_clean.csv")
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

print("All cleaned datasets loaded successfully!")


# ============================================================
# 3. DATASET SHAPES
# ============================================================

print("\n========== DATASET SHAPES ==========")

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
# 4. MISSING VALUE CHECK
# ============================================================

print("\n========== MISSING VALUES ==========")

datasets = {
    "Customers": customers,
    "Products": products,
    "Orders": orders,
    "Order Items": order_items,
    "Customer Interactions": customer_interactions,
    "Marketing Campaigns": marketing_campaigns
}

for name, df in datasets.items():

    print(f"\n{name}")

    missing = df.isnull().sum()

    print(
        missing[missing > 0]
    )


# ============================================================
# 5. DUPLICATE CHECK
# ============================================================

print("\n========== DUPLICATE CHECK ==========")

for name, df in datasets.items():

    duplicate_count = df.duplicated().sum()

    print(
        f"{name} duplicates:",
        duplicate_count
    )


# ============================================================
# 6. INVALID VALUE CHECK
# ============================================================

print("\n========== INVALID VALUE CHECK ==========")


# ---------- CUSTOMERS ----------

print(
    "Invalid customer income:",
    (
        customers["income"] <= 0
    ).sum()
)


print(
    "Invalid date_of_birth:",
    (
        pd.to_datetime(
            customers["date_of_birth"],
            errors="coerce"
        ) < "1900-01-01"
    ).sum()
)


# ---------- PRODUCTS ----------

print(
    "Invalid cost_price:",
    (
        products["cost_price"] < 0
    ).sum()
)


print(
    "Invalid selling_price:",
    (
        products["selling_price"] <= 0
    ).sum()
)


print(
    "Selling price below cost:",
    (
        products["selling_price"]
        < products["cost_price"]
    ).sum()
)


# ---------- ORDERS ----------

print(
    "Invalid order_value:",
    (
        orders["order_value"] < 0
    ).sum()
)

print(
    "Invalid calculated_order_value:",
    (
        orders["calculated_order_value"] < 0
    ).sum()
)

print(
    "Invalid quantity:",
    (
        order_items["quantity"] <= 0
    ).sum()
)


# ============================================================
# 7. REFERENTIAL INTEGRITY
# ============================================================

print("\n========== REFERENTIAL INTEGRITY ==========")


# Orders → Customers

invalid_customer_ids = orders[
    ~orders["customer_id"].isin(
        customers["customer_id"]
    )
]

print(
    "Invalid customer IDs:",
    len(invalid_customer_ids)
)


# Order Items → Orders

invalid_order_ids = order_items[
    ~order_items["order_id"].isin(
        orders["order_id"]
    )
]

print(
    "Invalid order IDs:",
    len(invalid_order_ids)
)


# Order Items → Products

invalid_product_ids = order_items[
    ~order_items["product_id"].isin(
        products["product_id"]
    )
]

print(
    "Invalid product IDs:",
    len(invalid_product_ids)
)


# ============================================================
# 8. BUSINESS RULE VALIDATION
# ============================================================

print("\n========== BUSINESS RULE VALIDATION ==========")


# Quantity must be positive

print(
    "Quantity <= 0:",
    (
        order_items["quantity"] <= 0
    ).sum()
)


# Discount must be between 0 and 100

print(
    "Invalid discount percentage:",
    (
        (order_items["discount_percent"] < 0)
        |
        (order_items["discount_percent"] > 100)
    ).sum()
)


# Revenue should not be negative

print(
    "Negative item revenue:",
    (
        order_items["item_revenue"] < 0
    ).sum()
)


# Profit can legitimately be negative,
# so we DO NOT treat negative profit as invalid.


# Shipping fee should not be negative

print(
    "Negative shipping fee:",
    (
        orders["shipping_fee"] < 0
    ).sum()
)


# Discount amount should not be negative

print(
    "Negative discount amount:",
    (
        orders["discount_amount"] < 0
    ).sum()
)


# ============================================================
# 9. ORDER VALUE CONSISTENCY
# ============================================================

print("\n========== ORDER VALUE CONSISTENCY ==========")

order_totals = (
    order_items
    .groupby("order_id")["item_revenue"]
    .sum()
    .reset_index()
)

order_totals.rename(
    columns={
        "item_revenue":
        "calculated_item_revenue"
    },
    inplace=True
)

order_totals = order_totals.merge(
    orders[
        [
            "order_id",
            "shipping_fee",
            "order_value"
        ]
    ],
    on="order_id",
    how="left"
)

order_totals["calculated_order_value"] = (
    order_totals["calculated_item_revenue"]
    + order_totals["shipping_fee"]
)


# Calculate difference

order_totals["difference"] = (
    order_totals["order_value"]
    - order_totals["calculated_order_value"]
)


# Allow tiny floating-point difference

inconsistent_orders = order_totals[
    order_totals["difference"].abs() > 0.01
]

print(
    "Original source order_value mismatches:",
    len(inconsistent_orders)
)


# ============================================================
# 10. OUTLIER REPORT
# ============================================================

print("\n========== OUTLIER CHECK ==========")


def count_outliers(df, column):

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR

    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound)
        |
        (df[column] > upper_bound)
    ]

    return len(outliers)


print(
    "Income outliers:",
    count_outliers(
        customers,
        "income"
    )
)

print(
    "Cost price outliers:",
    count_outliers(
        products,
        "cost_price"
    )
)

print(
    "Selling price outliers:",
    count_outliers(
        products,
        "selling_price"
    )
)

print(
    "Calculated order value outliers:",
    count_outliers(
        orders,
        "calculated_order_value"
    )
)

print(
    "Item revenue outliers:",
    count_outliers(
        order_items,
        "item_revenue"
    )
)

print(
    "Profit outliers:",
    count_outliers(
        order_items,
        "profit"
    )
)


# ============================================================
# 11. FINAL DATA QUALITY SUMMARY
# ============================================================

print("\n========== FINAL DATA QUALITY SUMMARY ==========")

print(
    "Customers:",
    len(customers)
)

print(
    "Products:",
    len(products)
)

print(
    "Orders:",
    len(orders)
)

print(
    "Order Items:",
    len(order_items)
)

print(
    "Customer Interactions:",
    len(customer_interactions)
)

print(
    "Marketing Campaigns:",
    len(marketing_campaigns)
)

print("\nPost-cleaning validation completed successfully!")

print("\n========== NEGATIVE ITEM REVENUE ==========")

negative_revenue = order_items[
    order_items["item_revenue"] < 0
]

print(
    negative_revenue[
        [
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount_percent",
            "item_revenue",
            "item_cost",
            "profit"
        ]
    ].head(20)
)