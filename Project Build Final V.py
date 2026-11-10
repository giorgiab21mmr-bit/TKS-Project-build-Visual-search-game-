
import tkinter as tk
import random
import time

# VISUAL SEARCH GAME - 10 LEVELS

TOTAL_LEVELS = 10
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

LEVEL_SETTINGS = {
    1: (40, 8),
    2: (40, 8),
    3: (40, 8),
    4: (40, 8),
    5: (80, 10),
    6: (80, 10),
    7: (120, 12),
    8: (120, 12),
    9: (160, 16),
    10: (160, 16)
}


class VisualSearchGame:

    def __init__(self, root):

        self.root = root
        self.root.title("Visual Search Game")
        self.root.geometry("950x850")
        self.root.configure(bg="#f2f5f8")

        self.level = 0
        self.total_errors = 0
        self.level_times = []
        self.target_position = None
        self.start_time = None
        self.game_start_time = None
        self.buttons = []

        self.title_label = tk.Label(
            root,
            text="VISUAL SEARCH GAME",
            font=("Arial", 20, "bold"),
            bg="#f2f5f8"
        )
        self.title_label.pack(pady=10)

        self.target_label = tk.Label(
            root,
            text="TARGET: ?",
            font=("Arial", 24, "bold"),
            fg="#1769aa",
            bg="white",
            padx=20,
            pady=10
        )
        self.target_label.pack(pady=8)

        self.info_label = tk.Label(
            root,
            text="Level 0/10 | Errors: 0",
            font=("Arial", 12),
            bg="#f2f5f8"
        )
        self.info_label.pack(pady=5)

        self.grid_frame = tk.Frame(
            root,
            bg="#f2f5f8"
        )
        self.grid_frame.pack(pady=10)

        self.message_label = tk.Label(
            root,
            text="Press START to begin.",
            font=("Arial", 12),
            bg="#f2f5f8"
        )
        self.message_label.pack(pady=8)

        self.results_frame = tk.Frame(
            root,
            bg="#f2f5f8"
        )

        self.start_button = tk.Button(
            root,
            text="START",
            font=("Arial", 14, "bold"),
            bg="#1769aa",
            fg="white",
            padx=25,
            pady=8,
            command=self.start_game
        )
        self.start_button.pack(pady=8)

    def start_game(self):

        self.level = 0
        self.total_errors = 0
        self.level_times = []

        self.game_start_time = time.perf_counter()

        self.start_button.pack_forget()
        self.results_frame.pack_forget()

        self.next_level()

    def next_level(self):

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []

        if self.level >= TOTAL_LEVELS:
            self.show_results()
            return

        self.level += 1

        number_of_letters, columns = LEVEL_SETTINGS[self.level]

        # Choose one target letter
        target = random.choice(LETTERS)

        # Exclude target from distractors
        other_letters = LETTERS.replace(target, "")

        # Generate repeated distractor letters
        letters = [
            random.choice(other_letters)
            for _ in range(number_of_letters)
        ]

        # Insert target exactly once
        self.target_position = random.randrange(
            number_of_letters
        )

        letters[self.target_position] = target

        self.target_label.config(
            text="TARGET: " + target
        )

        self.info_label.config(
            text=f"Level {self.level}/{TOTAL_LEVELS} | Errors: {self.total_errors}"
        )

        self.message_label.config(
            text=f"Find the target! Grid: {number_of_letters} letters"
        )

        # Create the grid
        for position, letter in enumerate(letters):

            button = tk.Button(
                self.grid_frame,
                text=letter,
                font=("Arial", 12, "bold"),
                width=3,
                height=1,
                command=lambda p=position: self.check_answer(p)
            )

            button.grid(
                row=position // columns,
                column=position % columns,
                padx=2,
                pady=2
            )

            self.buttons.append(button)

        self.start_time = time.perf_counter()

    def check_answer(self, clicked_position):

        if clicked_position == self.target_position:

            elapsed = time.perf_counter() - self.start_time
            self.level_times.append(elapsed)

            self.message_label.config(
                text=f"Correct! Time: {elapsed:.2f} seconds"
            )

            for button in self.buttons:
                button.config(state="disabled")

            self.root.after(700, self.next_level)

        else:

            self.total_errors += 1

            self.info_label.config(
                text=f"Level {self.level}/{TOTAL_LEVELS} | Errors: {self.total_errors}"
            )

            self.message_label.config(
                text="Wrong letter! Try again."
            )

    def show_results(self):

        # Remove the game grid
        self.grid_frame.pack_forget()

        total_time = (
            time.perf_counter() - self.game_start_time
        )

        average_time = (
            sum(self.level_times) / len(self.level_times)
        )

        self.target_label.config(
            text="GAME COMPLETE!"
        )

        self.info_label.config(
            text=f"Total errors: {self.total_errors}"
        )

        self.message_label.config(
            text="Congratulations! You completed all 10 levels.",
            font=("Arial", 12, "bold")
        )

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Results heading
        heading = tk.Label(
            self.results_frame,
            text="YOUR RESULTS",
            font=("Arial", 18, "bold"),
            fg="#1769aa",
            bg="#f2f5f8"
        )
        heading.pack(pady=8)

        # Individual level times
        for i, seconds in enumerate(self.level_times):

            result_label = tk.Label(
                self.results_frame,
                text=f"LEVEL {i + 1}:  {seconds:.2f} seconds",
                font=("Arial", 11, "bold"),
                fg="#222222",
                bg="#f2f5f8",
                width=35,
                anchor="center"
            )
            result_label.pack(pady=2)

        # Separator
        separator = tk.Label(
            self.results_frame,
            text="-------------------------------",
            font=("Arial", 12),
            bg="#f2f5f8"
        )
        separator.pack(pady=5)

        # Average time
        average_label = tk.Label(
            self.results_frame,
            text=f"AVERAGE TIME: {average_time:.2f} seconds",
            font=("Arial", 14, "bold"),
            fg="#1769aa",
            bg="#f2f5f8"
        )
        average_label.pack(pady=5)

        # Total time
        total_label = tk.Label(
            self.results_frame,
            text=f"TOTAL TIME: {total_time:.2f} seconds",
            font=("Arial", 14, "bold"),
            fg="#1769aa",
            bg="#f2f5f8"
        )
        total_label.pack(pady=5)

        # Completed levels
        completed_label = tk.Label(
            self.results_frame,
            text="LEVELS COMPLETED: 10/10",
            font=("Arial", 13, "bold"),
            bg="#f2f5f8"
        )
        completed_label.pack(pady=5)

        self.results_frame.pack(pady=5)

        # Show replay button
        self.start_button.config(
            text="PLAY AGAIN",
            state="normal"
        )
        self.start_button.pack(pady=10)


if __name__ == "__main__":

    window = tk.Tk()

    game = VisualSearchGame(window)

    window.mainloop()
