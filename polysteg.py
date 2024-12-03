import numpy as np
import random
import string
import matplotlib.pyplot as plt

def generate_polynomial():
    """
    Generates a random polynomial of degree 3-5 that maps x values 1-256 to y values 1-32
    Returns the coefficients of the polynomial
    
    Generally, this approach would benefit from more high-frequency functions
    """
    degree = random.randint(3, 5)
    coefficients = []
    
    # Generate random coefficients, but ensure they're small enough to keep values in range
    coefficients.append(random.uniform(-0.0125, 0.0125))  # x^n coefficient
    for _ in range(degree - 1):
        coefficients.append(random.uniform(-0.125, 0.125))
    
    # Add constant term to ensure values stay mostly within range
    coefficients.append(random.uniform(8, 24))
    
    return coefficients

def evaluate_polynomial(x, coefficients):
    """
    Evaluates the polynomial at point x
    Returns y value clamped between 1 and 32
    """
    y = 0
    for i, coef in enumerate(coefficients):
        y += coef * ((x-127) ** (len(coefficients) - 1 - i))
    
    # Clamp the result between 1 and 32
    return round(y) % 32 #max(0, min(31, round(y)))

def create_character_grid(message):
    """
    Creates a 256x32 grid of random characters with the message hidden along polynomial points
    Returns the grid and the polynomial coefficients used
    """
    if len(message) > 256:
        raise ValueError("Message must be 256 characters or less")
    
    # Pad message to full length with spaces
    # message = message.ljust(256)
    
    # Create grid filled with random characters
    grid = np.array([[random.choice(string.printable[:-5]) for _ in range(256)] for _ in range(32)])
    
    # Generate polynomial coefficients
    coefficients = generate_polynomial()
    
    # Place message characters along polynomial path
    for x in range(len(message)):
        y = evaluate_polynomial(x, coefficients)  # +1 to avoid x=0
        #print(y)
        grid[y][x] = message[x]  # -1 for 0-based indexing
    
    return grid, coefficients

def save_grid_to_file(grid, filename="encrypted_message.txt"):
    """
    Saves the passed in "grid" to specified or default "filename"
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write each row of the grid as a single line
            for row in grid:
                f.write(''.join(row) + '\n')
        print(f"Grid successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving grid to file: {e}")
        
def read_grid_from_file(filename="encrypted_message.txt"):
    """
    Reads from the passed in or default "filename" and puts it into
    a list variable
    """
    grid = None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Read each row of the file as a single line
            grid = f.readlines()
        print(f"Grid successfully read from {filename}")
        return grid
    except Exception as e:
        print(f"Error reading grid from file: {e}")
        
def decrypt(grid, coefficients):
    """
    Decrypts grid variable using coefficients as the key
    """
    # Decrypt
    indices = []
    
    # Check if grid is valid size
    try:
        for row in grid[:32]:
            # print(row)
            # print(len(row))
            if len(row) != 257:
                raise Exception("Grid is not valid size")
    except Exception as e:
        print(e)
        return
    
    for x in range(256):
        indices.append([x, evaluate_polynomial(x, coefficients)])
    
    decrypted = ''
    for x, y in indices:
        decrypted += grid[y][x]
    
    return decrypted

def plot_polynomial_with_grid(coefficients, grid, message):
    """
    Plots a polynomial based on given coefficients and overlays characters from a grid.
    """
    # Generate x values within the range 0 to 256
    x = np.array(range(256))
    # Compute the polynomial values for the x range
    y = np.array([evaluate_polynomial(x_val, coefficients) for x_val in x])

    # Clip y values to the range (0, 32)
    #y = np.clip(y, -32, 0)

    # Create the plot
    plt.figure(figsize=(14, 8))
    plt.plot(x, y, color='blue', label=f"Polynomial: {np.poly1d(coefficients)}", linewidth=1)
    plt.xlim(0, 256)
    plt.ylim(0, 32)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Polynomial Graph with Grid Overlay")
    plt.legend()
    plt.grid(False)

    # Overlay the grid characters
    message_index = 0
    ax = plt.gca()
    for i in range(256):  # Iterate over grid columns
        for j in range(32):  # Iterate over grid rows
            char = grid[j][i]
            text_color = 'black'
            if message_index < len(message) and char == message[message_index] and j == evaluate_polynomial(i, coefficients):
                text_color = 'red'
                rect = plt.Rectangle((i - 0.5, j - 0.5), 1, 1, linewidth=1, edgecolor='red', facecolor='none')
                ax.add_patch(rect)
                message_index += 1
            if char != '\n':  # Only draw non-whitespace characters
                plt.text(i, j, char, fontsize=8, ha='center', va='center', color=text_color)

    plt.show()

# Example usage
if __name__ == "__main__":
    # A settable seed for repeatable trials
    # random.seed(27)
    
    method = input("Encrypt or Decrypt message? (E for encrypt, D for decrypt): ").lower()
    
    if method == 'e':
        # Encrypt
        test_message = input("Enter the message to be encrypted (max size is 256 characters): ")
        opt_file = input("What file would you like to output to? (Leave empty for default): ")
        
        print("Original message:", test_message)
        grid, coefficients = create_character_grid(test_message)

        save_grid_to_file(grid, filename=opt_file if opt_file else "encrypted_message.txt")
        plot_polynomial_with_grid(coefficients, grid, test_message)
        
        key = ' '.join([str(c) for c in coefficients])
        print("\nPolynomial coefficients:", key)
    elif method == 'd':
        # Decrypt
        
        opt_file = input("What file would you like to decrypt? (Leave empty for default): ")
        coefficients = input("Enter key (coefficients from highest to lowest power like such: 5 4 3 2 1): ")
        
        decrypted = decrypt(grid = read_grid_from_file(filename=opt_file if opt_file else "encrypted_message.txt"), 
                            coefficients=[float(c) for c in coefficients.split(" ")])
        
        print("Decrypted Message:", decrypted)
    else:
        print("Please retry and enter either E or D")
           
    # assert test_message in decrypted, "Encryption/decryption failed!"
            
    

    