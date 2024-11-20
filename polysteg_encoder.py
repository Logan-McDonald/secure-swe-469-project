import numpy as np
import random
import string

def generate_polynomial():
    """
    Generates a random polynomial of degree 3-5 that maps x values 1-256 to y values 1-32
    Returns the coefficients of the polynomial
    """
    degree = random.randint(3, 5)
    coefficients = []
    
    # Generate random coefficients, but ensure they're small enough to keep values in range
    coefficients.append(random.uniform(-0.0001, 0.0001))  # x^n coefficient
    for _ in range(degree - 1):
        coefficients.append(random.uniform(-0.01, 0.01))
    
    # Add constant term to ensure values stay mostly within range
    coefficients.append(random.uniform(10, 20))
    
    return coefficients

def evaluate_polynomial(x, coefficients):
    """
    Evaluates the polynomial at point x
    Returns y value clamped between 1 and 32
    """
    y = 0
    for i, coef in enumerate(coefficients):
        y += coef * (x ** (len(coefficients) - 1 - i))
    
    # Clamp the result between 1 and 32
    return max(1, min(32, round(y)))

def create_character_grid(message):
    """
    Creates a 256x32 grid of random characters with the message hidden along polynomial points
    Returns the grid and the polynomial coefficients used
    """
    if len(message) > 256:
        raise ValueError("Message must be 256 characters or less")
    
    # Pad message to full length with spaces
    message = message.ljust(256)
    
    # Create grid filled with random characters
    grid = np.array([[random.choice(string.printable[:-5]) for _ in range(256)] for _ in range(32)])
    
    # Generate polynomial coefficients
    coefficients = generate_polynomial()
    
    # Place message characters along polynomial path
    # TODO I am being stupid why can't I figure this out
    for x in range(256):
        y = evaluate_polynomial(x + 1, coefficients)  # +1 to avoid x=0
        print(y)
        grid[y][x-1] = message[x]  # -1 for 0-based indexing
    
    return grid, coefficients

def save_grid_to_file(grid, filename="encrypted_message.txt"):
    """
    Takes a grid from create_character_grid and saves it to a text file
    
    Parameters:
        grid (numpy.ndarray): The 256x32 character grid
        filename (str): The name of the output file (default: encrypted_message.txt)
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write each row of the grid as a single line
            for row in grid:
                f.write(''.join(row) + '\n')
        print(f"Grid successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving grid to file: {e}")

# Example usage
if __name__ == "__main__":
    # Test message
    test_message = "Hello, this is a secret message!"
    
    # Encrypt
    print("Original message:", test_message)
    grid, coefficients = create_character_grid(test_message)
            
    save_grid_to_file(grid)
    print("\nPolynomial coefficients:", coefficients)
    
    # Verify
    # assert test_message == decrypted, "Encryption/decryption failed!"