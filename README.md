# Hybrid-Block-Encryption-Algorithm-Machine
This project involves implementing a given encryption and decryption algorithm, ensuring secure message transmission between users. 
I have created an application that takes in a user's name, a chosen key, and a message, and displays the steps/processes of encryption, as well as the final encryption method.
<br/>
<br/>
<p align="center">
<img width="400" alt="Screenshot 2025-01-10 at 3 50 14 PM" src="https://github.com/user-attachments/assets/87cb0e63-ae5c-45a5-81f3-258800a357d9" />
</p>

# Launching Application
**To launch in terminal, copy the below commands line by line**:
<br/>
git clone https://github.com/jakelicata/Hybrid-Block-Encryption-Algorithm-Machine <br/>
cd Hybrid-Block-Encryption-Algorithm-Machine <br/>
python3 main_algorithm_and_GUI.py <br/>

**Troublshooting**: 
<br/>
Ensure you have Python installed, which should include Tkinter, if python is not installed, install it:
<br/>
python3 --version

If Python installed and application still not launching, ensure tinter installed (a small pop up should launch):
<br/>
python3 -m tkinter

If tkinter is not installed, you can install Tkinter:
<br/>
brew install python-tk





# Outline of Encryption Algorithm

<h3>Key Generation:</h3>
Each user will have their own, unique permutation table stored, allowing each user to generate unique keys based on their chosen input key (recommended to use their email).
<p align="center">
<br />
<img width="831" alt="Screenshot 2025-01-10 at 3 10 07 PM" src="https://github.com/user-attachments/assets/5e36f7f9-e838-45ba-95a5-833a34531e6f" />
</p>
<br />
<h3>Message Processing:</h3>
Messages are then encrypted to the block encryption scheme.

<p align="center">
<img width="801" alt="Screenshot 2025-01-10 at 3 10 19 PM" src="https://github.com/user-attachments/assets/2ebcc93d-a6e6-4015-a71d-11ecb44054a3" />
</p>


<h3>Encryption:</h3>
Then encryption occurs, involving the key and the message, resulting in a string of encrypted segments that are concatinated to create the final cipher text.
<br />
<p align="center">
<img width="662" alt="Screenshot 2025-01-10 at 3 10 28 PM" src="https://github.com/user-attachments/assets/95b070e5-8a81-4b11-94ad-5f74ad82e2f7" />
<br />
<img width="1298" alt="Screenshot 2025-01-10 at 3 52 30 PM" src="https://github.com/user-attachments/assets/ce08a77d-b457-40f7-af06-cfffa343dd49" />
</p>


# Decryption




