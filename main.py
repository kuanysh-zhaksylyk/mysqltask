from typing import Dict, List
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import logging
import os
import io


class SalesReportGenerator:
    """
    Generates sales report for products in 2020 and plots the monthly sales trend for each product.
    """

    def __init__(self, config: Dict[str, str]):
        self.config = config

    def _connect_to_database(self) -> mysql.connector.connection.MySQLConnection:
        """Establishes a connection to the MySQL database."""
        return mysql.connector.connect(**self.config)

    def _fetch_data_from_database(
        self, connection: mysql.connector.connection.MySQLConnection
    ) -> pd.DataFrame:
        """Fetches data for 2020 from the MySQL database."""
        query = """
        SELECT products.product_code, MONTH(order_date) AS month,
              SUM(sales_qty * sales_amount) AS total_sales
        FROM transactions
        JOIN products ON transactions.product_code = products.product_code
        WHERE YEAR(order_date) = 2020
        GROUP BY products.product_code, MONTH(order_date)
        ORDER BY products.product_code ASC, MONTH(order_date) ASC
        """
        return pd.read_sql_query(query, connection)

    def generate_sales_report(self) -> pd.DataFrame:
        """
        Generates the sales report for products in 2020.

        Returns:
            pd.DataFrame: DataFrame containing sales data for products in 2020.
        """
        connection = self._connect_to_database()
        df = self._fetch_data_from_database(connection)
        connection.close()
        return df

    def plot_sales_trend(self, df: pd.DataFrame):
        """
        Plots the monthly sales trend for each product in 2020.

        Args:
            df (pd.DataFrame): DataFrame containing sales data for products in 2020.
        """
        plt.figure(figsize=(12, 6))
        for product, data in df.groupby("product_code"):
            plt.plot(data["month"], data["total_sales"], label=f"Product {product}")

        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.title("Monthly Sales Trend for Each Product in 2020")
        plt.legend()
        plt.grid(True)
        plt.xticks(
            range(1, 13),
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        )
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    dotenv_path = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    """
    import credentials from .env
    """
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        raise Exception("Doesn't load credentials from .env")

    # Создание конфигурационного словаря
    config = {"host": DB_HOST, "user": DB_USER, "password": DB_PASSWORD, "database": DB_NAME}

    report_generator = SalesReportGenerator(config)

    logging.info("Starting data loading process")
    try:
        sales_data = report_generator.generate_sales_report()
        print(sales_data)
        report_generator.plot_sales_trend(sales_data)
        logging.info("Data loading process completed successfully")
        print("Successful")
    except Exception as e:
        print("Error with database work", e)
