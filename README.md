# Hybrid-Block-Encryption-Algorithm-Machine
This project involves implementing a given encryption and decryption algorithm, ensuring secure message transmission between users. 
I have created an application that takes in a user's name, a chosen key, and a message, and displays the steps/processes of encryption, as well as the final encryption method.
<br/>
<br/>
<p align="center">
<img width="450" alt="Screenshot 2025-01-10 at 4 43 42 PM" src="https://github.com/user-attachments/assets/f6c56920-7310-43e2-bb43-0f43aebbc064" />
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
The encryption algorithm being used can be roughly broken up into 3 main steps: Key Generation, Message Processing, and Encryption. They are outlined below.
<br/>
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
Lastly, for the structure of the encryption algorithm that this project was based on, decryption is not possible. This has to do with the the sbox step on encryption, and essentially because of the randomness of how it is implemented, to "unscramble" this section it would require an expensive brute force algorithm that ultimately would not be possible to implement. I have attached a text file of what a decription algorithm typically would look like, however, the chances of this accurately decrypting is very, very, very, very, very, very low, hence why this machine only includes encryption. If created with a different encryption algorithm, a **similar** decryption algorithm could be used. 



