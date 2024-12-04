# Information
Welcome to our Polynomial-based Steganography project!

Our group is comprised of Logan McDonald, Taylor Carlson, Garret Snitchler, and Thadd Post

Logan and Thadd worked on the code side of the project, creating a python script that allows a user to encrypt and 
decrypt messages. The encryption algorithm encrypts a message, saves it to a file of the user's choice, and then 
outputs the polynomial key. The decryption algorithm has a user choose a file to decrypt, and then input the key.

Taylor and Garret worked on the report. They outlined the problem we wanted to address, motivation, and objectives 
of our project while also doing research to highlight the background and integrity of the idea we are pursuing.

## Included files
- README.md
- polysteg.py
- test_polysteg.py
- requirements.txt
- Screenshots of all relevant artifacts


## Execution
To excute this python code, you first need to have Python 3 or greater installed. You also need to be using python
3.10.8 as the interpreter version. (It may work with other versions of python, but this is the recommended version.)

### Procedure
1. Open a terminal in the same directory as `polysteg.py`
2. Install any requirements using the command `pip install -r requirements.txt` or `pip3 install requirements.txt`
3. Once requirements are installed, run the command `python polysteg.py` or `python3 polysteg.py`
4. From there, you will be prompted to either encrypt text or decrypt a file.

### Operation
Once you have reached a stage where you can run the file and choose to encrypt or decrypt a file, here is a general walkthrough of how inputs and outputs from the program work.
#### Encryption
1. When prompted to either encrypt or decrypt a file, you may enter the letter `e` to begin encrypting a file.
2. The next action would be to enter a message to be encrypted. This should be less than or equal to 256 characters in length. You do not need to include any quotation marks surrounding this text.
3. You will be prompted to enter a path to the output file where the ciphertext will be stored. Leaving this blank will save the ciphertext in some `encrypted_message.txt` file in the running directory.
4. After entering the previous information, a grid will be created, a mathplotlib plot will show up displaying the encrypted text and its polynomial graph (this may take a while to load), and the polynomial coefficients will be printed in the terminal. These numbers are your key for decryption, so be sure to put them somewhere secure.

#### Decryption
1. When prompted to either encrypt or decrypt a file, you may enter the letter `d` to begin decrypting a file.
2. When prompted for the file you want to decrypt, enter the filepath for the file which you are looking to decrypt. This defaults to `encrypted_message.txt` when left blank.
3. When prompted to enter the key, enter the polynomial coefficients in the order that they were given from the encryption process (that is, coefficient to the highest order factor first, then the next highest, etc...). These terms should be separated only by a single space.
4. The output will be a string in the console containing the encrypted message.

### Testing
To run the tests for this code, you can run the following command:<br>
`python test_polysteg.py` or `python3 test_polysteg.py`

Results of getting code coverage using the `pytest-cov` library can be seen below:![alt text](artifacts/coverage.png)

The apparent low coverage of `polysteg.py` is due to not testing the user inputs, not testing the exception catch branches, and not testing the `plot_polynomial_with_grid(...)` method.