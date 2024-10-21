import random
import tkinter as tk
from tkinter import messagebox, font, RIDGE

class ExtendedMarkovChain:
    def __init__(self, corpus):
        self.model = {}
        self.build_model(corpus)

    def build_model(self, corpus):
        words = corpus.lower().split()
        for i in range(len(words) - 1):
            bigram = (words[i], words[i + 1])
            if bigram not in self.model:
                self.model[bigram] = []
            if i + 2 < len(words):
                self.model[bigram].append(words[i + 2])

    def predict(self, word1, word2, num_predictions=5):
        bigram = (word1.lower(), word2.lower())
        if bigram in self.model:
            return random.sample(self.model[bigram], k=min(num_predictions, len(self.model[bigram])))
        else:
            # Fallback prediction mechanism
            return self.fallback_predict([word1, word2], num_predictions)

    def fallback_predict(self, last_words, num_predictions):
        possible_predictions = []
        
        # Generate predictions based on previous words
        for ngram in self.model.keys():
            if ngram[:-1] == tuple(last_words[-1:]):
                possible_predictions.extend(self.model[ngram])

        # If no direct match found, suggest common words from the model
        if not possible_predictions:
            possible_predictions = [word for ngram in self.model.keys() for word in self.model[ngram]]

        return random.sample(possible_predictions, k=min(num_predictions, len(possible_predictions))) if possible_predictions else []

# Enhanced corpus with diverse content
enhanced_corpus = (
    "Hello, how are you? Hope you are doing well. "
    "Greetings! How can I assist you today? "
    "You are doing great; how about you? "
    "How are you today? It's wonderful to see you. "
    "In this rapidly changing world, communication is key. "
    "You can explore countless opportunities in the digital landscape. "
    "Have you considered learning a new skill? "
    "Technology is evolving every day; staying updated is essential. "
    "With determination and persistence, you can achieve your goals. "
    "What are your thoughts on the recent developments in AI? "
    "Understanding diverse perspectives is vital for growth. "
    "Let's embark on a journey of discovery together."
)

markov_chain = ExtendedMarkovChain(enhanced_corpus)

# GUI Code
class PredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1550x800+0+0")  # Window size
        self.root.config(bg="white")

        # Set a custom font
        self.custom_font = font.Font(family="Arial", size=12)

        # Title Header with customized style
        self.title_label = tk.Label(self.root, text="Word Prediction Application",
                                     font=("times new roman", 35, "bold"),
                                     bg="light gray", fg="#010c48",
                                     anchor="center", padx=20)
        self.title_label.place(x=0, y=0, relwidth=1, height=70)  # Positioned title to center with full width

        # Data Frame for Inputs with border and relief
        self.data_frame = tk.Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.data_frame.place(x=450, y=80, width=530, height=200)  # Positioned frame

        self.label1 = tk.Label(self.data_frame, text="Enter first word:", bg="white", font=self.custom_font)
        self.label1.place(x=30, y=20)

        self.word1_entry = tk.Entry(self.data_frame, font=self.custom_font, width=20, bd=2, relief="groove")
        self.word1_entry.place(x=180, y=20)

        self.label2 = tk.Label(self.data_frame, text="Enter second word:", bg="white", font=self.custom_font)
        self.label2.place(x=30, y=60)

        self.word2_entry = tk.Entry(self.data_frame, font=self.custom_font, width=20, bd=2, relief="groove")
        self.word2_entry.place(x=180, y=60)

        # Button
        self.predict_button = tk.Button(self.data_frame, text="Predict", command=self.predict_words,
                                         bg="#FF5722", fg="white", font=self.custom_font, bd=2, relief="raised")
        self.predict_button.place(x=200, y=120)

        # Output Frame
        self.output_frame = tk.Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.output_frame.place(x=1010, y=80, width=350, height=200)  # Positioned output frame

        self.result_label = tk.Label(self.output_frame, text="", bg="white", font=self.custom_font)
        self.result_label.place(x=20, y=20)

    def predict_words(self):
        word1 = self.word1_entry.get()
        word2 = self.word2_entry.get()
        
        if not word1 or not word2:
            messagebox.showwarning("Input Error", "Please enter both words.")
            return

        predictions = markov_chain.predict(word1, word2)
        if predictions:
            self.result_label.config(text="Predictions: " + ', '.join(predictions))
        else:
            self.result_label.config(text="No predictions found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictionApp(root)
    root.mainloop()
