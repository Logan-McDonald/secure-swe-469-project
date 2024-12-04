import unittest
import os
import random
import numpy as np
from polysteg import (
    generate_polynomial,
    evaluate_polynomial,
    create_character_grid,
    save_grid_to_file,
    read_grid_from_file,
    decrypt
)

class TestPolynomialEncryption(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment by fixing the random seed and defining a test message.
        """
        random.seed(42)
        self.test_message = "This is a test message for encryption and decryption."
        self.test_filename = "test_encrypted_message.txt"

    def test_generate_polynomial(self):
        """
        Test polynomial generation to ensure it adheres to constraints and is reproducible with a fixed seed.
        """
        random.seed(42)
        coefficients = generate_polynomial()
        
        self.assertGreaterEqual(len(coefficients), 4)
        self.assertLessEqual(len(coefficients), 6)
        
        self.assertTrue(-0.0125 <= coefficients[0] <= 0.0125, "First coefficient out of bounds")
        for coef in coefficients[1:-1]:
            self.assertTrue(-0.125 <= coef <= 0.125, "Intermediate coefficient out of bounds")
        self.assertTrue(8 <= coefficients[-1] <= 24, "Constant term out of bounds")


    def test_evaluate_polynomial(self):
        """
        Test polynomial evaluation to ensure correct y values are computed.
        """
        coefficients = [-0.003905, 0.104075, 17.036691]
        y_value = evaluate_polynomial(128, coefficients)
        self.assertEqual(y_value, 17)

    def test_create_character_grid(self):
        """
        Test grid creation and ensure the message is correctly placed along the polynomial path.
        """
        grid, coefficients = create_character_grid(self.test_message)
        for x in range(len(self.test_message)):
            y = evaluate_polynomial(x, coefficients)
            self.assertEqual(grid[y][x], self.test_message[x])

    def test_save_and_read_grid(self):
        """
        Test saving the grid to a file and reading it back.
        """
        grid, _ = create_character_grid(self.test_message)
        save_grid_to_file(grid, self.test_filename)
        
        self.assertTrue(os.path.exists(self.test_filename))
        
        read_grid = read_grid_from_file(self.test_filename)
        for row_saved, row_read in zip(grid, read_grid):
            self.assertEqual(''.join(row_saved), row_read.strip())

    def test_encrypt_and_decrypt(self):
        """
        Test full encryption and decryption process.
        """
        grid, coefficients = create_character_grid(self.test_message)
        save_grid_to_file(grid, self.test_filename)
        
        read_grid = read_grid_from_file(self.test_filename)
        decrypted_message = decrypt(read_grid, coefficients)
        
        self.assertTrue(self.test_message in decrypted_message, "Decrypted message does not contain the original message")


    def tearDown(self):
        """
        Clean up by removing any generated test files.
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

if __name__ == "__main__":
    unittest.main()
