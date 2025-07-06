import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os
import pickle

# ----- Game Data -----
emoji_song_data = [
    {"emojis": "👫💞🔗🎶", "answer": "Belong Together", "file": "Belong_Together.mp3"},
    {"emojis": "✍️⭐💫🚀", "answer": "Rewrite the stars", "file": "Rewrite_the_stars.mp3"},
    {"emojis": "1💓 - Hindi", "answer": "Phela Pyar", "file": "Phela_Pyar.mp3"},
    {"emojis": "🍬❤️", "answer": "Sweetheart", "file": "Sweetheart.mp3"},
    {"emojis": "🕵️💰My👧", "answer": "Steal my girl", "file": "steal_my_girl.mp3"},
    {"emojis": "🌃🕰️🔁", "answer": "night changes", "file": "night_changes.mp3"},
    {"emojis": "🛣️🎒🚞🎶", "answer": "journey song", "file": "journey_song.mp3"},
    {"emojis": "💃🔥❤️🎤", "answer": "Senorita", "file": "Senorita.mp3"},
    {"emojis": "Ajeeb⭕💭❓", "answer": "ajeeb o gareeb", "file": "ajeeb_o_gareeb.mp3"},
    {"emojis": "👧💃de -Hindi", "answer": "kudi nu nachne de", "file": "Kudi Nu Nachne de.mp3"}
]

# ----- Score Data -----
score_file = "high_score.pkl"
if os.path.exists(score_file):
    with open(score_file, "rb") as f:
        high_score = pickle.load(f)
else:
    high_score = 0

# ----- Audio Setup -----
pygame.init()
pygame.mixer.init()

# ----- GUI Setup -----
class GuessTheSongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎶 Guess the Song by Emoji 🎶")
        self.root.geometry("550x450")
        self.root.configure(bg="#ffe6f0")
        self.score = 0
        self.round = 0
        self.used_indexes = []

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_window()
        tk.Label(self.root, text="🎉 Welcome to Emoji Song Guess 🎉", font=("Comic Sans MS", 22, "bold"), fg="#ff3399", bg="#ffe6f0").pack(pady=25)
        tk.Label(self.root, text=f"🏆 High Score: {high_score} points", font=("Arial", 14), bg="#ffe6f0").pack()

        tk.Button(self.root, text="🎮 Start Game", command=self.start_game, font=("Arial", 16, "bold"), bg="#ffccff", fg="#4d004d", width=15).pack(pady=15)
        tk.Button(self.root, text="❌ Exit", command=self.root.quit, font=("Arial", 14), bg="#ff9999", fg="#660000", width=10).pack(pady=5)

    def start_game(self):
        self.score = 0
        self.round = 0
        self.used_indexes = []
        self.next_question()

    def next_question(self):
        if self.round == 10:
            self.end_game()
            return

        self.clear_window()
        self.root.configure(bg="#e6f2ff")
        self.index = random.choice([i for i in range(10) if i not in self.used_indexes])
        self.used_indexes.append(self.index)
        data = emoji_song_data[self.index]
        self.correct_answer = data["answer"].lower()
        self.song_file = data["file"]

        tk.Label(self.root, text=f"🎵 Round {self.round+1}/10 🎵", font=("Helvetica", 16, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=15)
        self.emoji_label = tk.Label(self.root, text=data["emojis"], font=("Arial", 42), bg="#e6f2ff")
        self.emoji_label.pack(pady=20)

        self.entry = tk.Entry(self.root, font=("Arial", 16), justify='center')
        self.entry.pack(pady=10)
        self.entry.focus()

        tk.Button(self.root, text="Submit Guess ✅", command=self.check_answer, font=("Arial", 14), bg="#cce5ff", fg="#000080").pack(pady=10)

    def check_answer(self):
        user_input = self.entry.get().strip().lower()
        if user_input == self.correct_answer:
            self.score += 10
            messagebox.showinfo("Correct! 🎉", "That's right! Let's play the song 🎶")
            try:
                pygame.mixer.music.load(self.song_file)
                pygame.mixer.music.play()
            except:
                messagebox.showwarning("Audio Error", f"Couldn't play {self.song_file}. Check the file.")
        else:
            messagebox.showerror("Oops! 😬", f"Wrong answer! The correct answer was: {self.correct_answer}")
        self.round += 1
        self.root.after(1500, self.next_question)

    def end_game(self):
        global high_score
        if self.score > high_score:
            high_score = self.score
            with open(score_file, "wb") as f:
                pickle.dump(high_score, f)

        self.clear_window()
        self.root.configure(bg="#fff2e6")
        tk.Label(self.root, text="🏁 Game Over 🏁", font=("Arial", 24, "bold"), bg="#fff2e6", fg="#cc6600").pack(pady=20)
        tk.Label(self.root, text=f"🎯 Your Score: {self.score}", font=("Arial", 18), bg="#fff2e6").pack(pady=10)
        tk.Label(self.root, text=f"🥇 High Score: {high_score}", font=("Arial", 18), bg="#fff2e6").pack(pady=10)
        tk.Button(self.root, text="Play Again 🔁", command=self.start_game, font=("Arial", 14), bg="#ffd699", width=15).pack(pady=10)
        tk.Button(self.root, text="Exit 🚪", command=self.root.quit, font=("Arial", 14), bg="#ffcccc", width=10).pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ----- Run Game -----
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessTheSongGame(root)
    root.mainloop()
