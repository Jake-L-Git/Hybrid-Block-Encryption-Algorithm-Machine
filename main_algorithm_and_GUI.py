import hashlib
import random
import tkinter as tk
from tkinter import scrolledtext
from encryption import *
from helper_functions import *

class encryption_gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Machine")
        self.root.geometry("800x675")
        self.root.minsize(800, 675)
        self.root.configure(bg="#5c5c5c")


        # User input fields
        tk.Label(root, text="User:", bg="#5c5c5c", fg="white", font=("Helvetica", 16)).pack()
        self.user_entry = tk.Entry(root, highlightbackground="#5c5c5c")
        self.user_entry.pack()


        tk.Label(root, text="Key (use your email):", bg="#5c5c5c", fg="white", font=("Helvetica", 16)).pack()
        self.key_entry = tk.Entry(root, highlightbackground="#5c5c5c")
        self.key_entry.pack()

        tk.Label(root, text="Text to encrypt:", bg="#5c5c5c", fg="white", font=("Helvetica", 16)).pack()
        self.text_entry = tk.Entry(root, width=80, highlightbackground="#5c5c5c")
        self.text_entry.pack()

        # Output display area
        self.output_frame = tk.Frame(root, height=20, bg="#5c5c5c")  # adding margin
        self.output_frame.pack(pady=10)  # adding margin
        self.output_text = scrolledtext.ScrolledText(
            root, width=80, height=20, bg="#d9fffe", font=("Courier", 12)
        )
        self.output_text.pack()
        
        self.output_text.tag_configure("odd", foreground="green", font=("Courier", 12))
        self.output_text.tag_configure("odd_title", foreground="green", font=("Courier", 12, "bold"))
        self.output_text.tag_configure("even", foreground="blue", font=("Courier", 12))
        self.output_text.tag_configure("even_title", foreground="blue", font=("Courier", 12, "bold"))
        self.output_text.tag_configure("answer", foreground="red", font=("Courier", 12))
        self.output_text.tag_configure("answer_title", foreground="red", font=("Courier", 12, "bold"))



        # Buttons
        self.encrypt_button = tk.Button(root, text="Encrypt", highlightbackground="#5c5c5c", font=("Helvetica", 16), command=self.run_encryption, activeforeground="green")
        self.encrypt_button.pack(pady=7)

        self.clear_button = tk.Button(root, text="Clear", highlightbackground="#5c5c5c", font=("Helvetica", 16), command=self.clear_fields, activeforeground="blue")
        self.clear_button.pack(pady=7)

        self.users_button = tk.Button(root, text="Show Users", highlightbackground="#5c5c5c", font=("Helvetica", 16), command=self.show_users, activeforeground="yellow")
        self.users_button.pack(pady=7)

        self.quit_button = tk.Button(root, text="Quit", highlightbackground="#5c5c5c", font=("Helvetica", 16), command=root.quit, activeforeground="red")
        self.quit_button.pack(pady=7)

    def clear_fields(self):
        # Clear all fields
        self.user_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.text_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
    
    def show_users(self):
        # Clear all fields
        self.user_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.text_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        for key in users_list:
            self.output_text.insert(tk.END, f'{key}\n')



    def run_encryption(self):
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        # Get user inputs
        user = self.user_entry.get()
        key = self.key_entry.get()
        text_input = self.text_entry.get()

        # key generation
        hash_gen = hash_generation(key)
        self.output_text.insert(tk.END, f'Hashed Key: ', "odd_title")
        self.output_text.insert(tk.END, f'{hash_gen}\n', "odd")
        hash_seg = hash_segmentation(hash_gen)
        self.output_text.insert(tk.END, f'Segmented Hash Key: ', "even_title")
        self.output_text.insert(tk.END, f'{hash_seg}\n', "even")
        perm = permutations(hash_seg, user)
        self.output_text.insert(tk.END, f'Permutated Hash Key: ', "odd_title")
        self.output_text.insert(tk.END, f'{perm}\n', "odd")


        # message processing
        split_256 = split_input_text_into_256_bit_blocks(text_input)
        self.output_text.insert(tk.END, f'Input Text 256 bit blocks: ', "even_title")
        self.output_text.insert(tk.END, f'{split_256}\n', "even")
        hash_seg_inp = hash_segmentation_input(split_256)
        perm_inp = permutation_input(hash_seg_inp, user)

        # xoring and segmenting
        key_exp = key_expansion(perm)
        expan = expansion(perm_inp)
        xor_segs = xor_segments(key_exp, expan)
        forty_eight_to_six = fortyeight_to_six_segs(xor_segs)

        # running through s-boxes
        s_box_complete = s_box_func(forty_eight_to_six)
        final_encryption = encrypted_message(s_box_complete)
        cipher_text = bin_to_text(final_encryption)
        self.output_text.insert(tk.END, f'Encrypted text:\n', "answer_title")
        self.output_text.insert(tk.END, cipher_text, "answer")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = encryption_gui(root)
    root.mainloop()