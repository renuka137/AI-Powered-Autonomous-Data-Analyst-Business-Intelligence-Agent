import os
import pandas as pd

data_path = r"C:\Users\HP\Desktop\Project 1= ShopSphere\shopsphere_dataset\shopsphere_dataset\raw_data"

customers = pd.read_csv(os.path.join(data_path, "customers.csv"))
products = pd.read_csv(os.path.join(data_path, "products.csv"))
orders = pd.read_csv(os.path.join(data_path, "orders.csv"))
order_items = pd.read_csv(os.path.join(data_path, "order_items.csv"))
customer_interactions = pd.read_csv(os.path.join(
    data_path, "customer_interactions.csv"
))
marketing_campaigns = pd.read_csv(os.path.join(
    data_path, "marketing_campaigns.csv"
))

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Customer Interactions:", customer_interactions.shape)
print("Marketing Campaigns:", marketing_campaigns.shape)

print("Customers_info:")
customers.info()

print("Products_info:")
products.info()

print("Orders_info:")
orders.info()

print("Order Items_info:")
order_items.info()

print("Customer Interactions_info:")
customer_interactions.info()

print("Marketing Campaigns_info:")
marketing_campaigns.info()

print("Customers_describe:")
print(customers.describe(include='all'))

print("Products_describe:")
print(products.describe(include='all'))

print("Orders_describe:")
print(orders.describe(include='all'))

print("Order Items_describe:")
print(order_items.describe(include='all'))

print("Customer Interactions_describe:")
print(customer_interactions.describe(include='all'))

print("Marketing Campaigns_describe:")
print(marketing_campaigns.describe(include='all'))

print("Customers_missing_values:")
print(customers.isnull().sum())
print("Products_missing_values:")
print(products.isnull().sum())
print("Orders_missing_values:")
print(orders.isnull().sum())
print("Order Items_missing_values:")
print(order_items.isnull().sum())
print("Customer Interactions_missing_values:")
print(customer_interactions.isnull().sum())
print("Marketing Campaigns_missing_values:")
print(marketing_campaigns.isnull().sum())

print("Customers_duplicate:")
print(customers.duplicated().sum())
print("Products_duplicate:")
print(products.duplicated().sum())
print("Orders_duplicate:")
print(orders.duplicated().sum())
print("Order Items_duplicate:")
print(order_items.duplicated().sum())
print("Customer Interactions_duplicate:")
print(customer_interactions.duplicated().sum())
print("Marketing Campaigns_duplicate:")
print(marketing_campaigns.duplicated().sum())

#check Invalid values

print("Invalid customer income:")
print(customers[customers["income"] <= 0].shape[0])

print("Invalid date of birth:")
print(customers[customers["date_of_birth"] < "1900-01-01"].shape[0])

print("Invalid cost price:")
print(products[products["cost_price"] < 0].shape[0])

print("Invalid selling price:")
print(products[products["selling_price"] <= 0].shape[0])

print("Selling price less than cost price:")
print(
    products[
        products["selling_price"] < products["cost_price"]
    ].shape[0]
)

print("Invalid order value:")
print(orders[orders["order_value"] < 0].shape[0])

print("Orders with missing order date:")
print(orders[orders["order_date"].isna()].shape[0])

print("Invalid quantity:")
print(order_items[order_items["quantity"] <= 0].shape[0])

#Check Outliers

def check_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    print(f"\nColumn: {column}")
    print(f"Lower Bound: {lower_bound}")
    print(f"Upper Bound: {upper_bound}")
    print(f"Number of Outliers: {len(outliers)}")

    return outliers

check_outliers(customers, "income")

check_outliers(products, "cost_price")

check_outliers(products, "selling_price")

check_outliers(orders, "order_value")

check_outliers(order_items, "item_revenue")

check_outliers(order_items, "profit")

#Check relationships between tables?

#Check orders.customer_id
print("Check orders.customer_id")
invalid_customer_ids = orders[
    ~orders["customer_id"].isin(customers["customer_id"])
]

print("Invalid customer IDs:", len(invalid_customer_ids))

#Check order_items.order_id
print("Check order_items.order_id")
invalid_order_ids = order_items[
    ~order_items["order_id"].isin(orders["order_id"])
]

print("Invalid order IDs:", len(invalid_order_ids))

#Check order_items.product_id
print("Check order_items.product_id")
invalid_product_ids = order_items[
    ~order_items["product_id"].isin(products["product_id"])
]

print("Invalid product IDs:", len(invalid_product_ids))
