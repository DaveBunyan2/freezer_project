import unittest
from unittest.mock import patch, MagicMock, create_autospec
from src.insert_data import insert_data
import mysql.connector


class TestInsertDataFunction(unittest.TestCase):
    @patch('src.insert_data.mysql.connector.pooling.MySQLConnectionPool')
    def test_successful_insertion(self, mock_connection_pool):
        # Set up the mock connection pool and cursor for a successful insertion
        mock_cursor = MagicMock()
        mock_connection_pool.return_value.get_connection.return_value.cursor.return_value = mock_cursor

        # Call the function with the mocked connection and data
        data = [('2023-01-01', 1, 42.0), ('2023-01-01', 2, 37.5)]
        result = insert_data(data, mock_connection_pool, table_name='temperature_sensor_data')

        # Add assertions for the expected behavior of insert_data
        mock_cursor.executemany.assert_called_once()
        mock_connection_pool.return_value.get_connection.assert_called_once()
        mock_connection_pool.return_value.release_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with("INSERT INTO sensor_data (timestamp, sensor_id, value) VALUES (%s, %s, %s)", ('2023-01-01', 1, 42.0))
        mock_connection_pool.return_value.commit.assert_called_once()
        self.assertIsNone(result)

    @patch('src.insert_data.mysql.connector.pooling.MySQLConnectionPool')
    def test_unsuccessful_insertion(self, mock_connection_pool):
        # Set up the mock connection pool and cursor for an unsuccessful insertion
        mock_cursor = create_autospec(mysql.connector.connection.MySQLConnection().cursor)
        mock_cursor.executemany.side_effect = Exception("Mocked database error")
        mock_connection_pool.return_value.get_connection.return_value.cursor.return_value = mock_cursor

        # Call the function with the mocked connection and data
        data = [('2023-01-01', 1, 42.0), ('2023-01-01', 2, 37.5)]
        result = insert_data(data, mock_connection_pool, table_name='temperature_sensor_data')

        # Add assertions for the expected behavior of insert_data
        mock_cursor.executemany.assert_called_once()
        mock_connection_pool.return_value.get_connection.assert_called_once()
        mock_connection_pool.return_value.rollback.assert_called_once()
        self.assertIsNotNone(result)  

if __name__ == '__main__':
    unittest.main()
