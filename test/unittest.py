import unittest
import pandas as pd
import mysql.connector
from main import SalesReportGenerator


class TestSalesReportGenerator(unittest.TestCase):
    def setUp(self):
        self.config = {
            "host": "localhost",
            "user": "test_user",
            "password": "test_password",
            "database": "test_db",
        }
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        self.create_test_database()

    def tearDown(self):
        self.cursor.execute("DROP TABLE IF EXISTS transactions")
        self.cursor.execute("DROP TABLE IF EXISTS products")
        self.connection.close()

    def create_test_database(self):
        self.cursor.execute("CREATE TABLE products (product_code INT PRIMARY KEY)")
        self.cursor.execute(
            "CREATE TABLE transactions (product_code INT, order_date DATE, sales_qty INT, sales_amount FLOAT)"
        )

        self.cursor.execute("INSERT INTO products (product_code) VALUES (1)")
        self.cursor.execute(
            "INSERT INTO transactions (product_code, order_date, sales_qty, sales_amount) VALUES (1, '2020-01-01', 10, 100)"
        )
        self.connection.commit()

    def test_generate_sales_report(self):
        report_generator = SalesReportGenerator(self.config)
        sales_data = report_generator.generate_sales_report()

        expected_data = pd.DataFrame({"product_code": [1], "month": [1], "total_sales": [1000]})
        pd.testing.assert_frame_equal(sales_data, expected_data)

    def test_plot_sales_trend(self):
        report_generator = SalesReportGenerator(self.config)
        sales_data = pd.DataFrame({"product_code": [1], "month": [1], "total_sales": [1000]})

        try:
            report_generator.plot_sales_trend(sales_data)
        except Exception as e:
            self.fail(f"plot_sales_trend() raised an unexpected exception: {e}")


if __name__ == "__main__":
    unittest.main()
