import tkinter as tk
from tkinter import messagebox
import math
import random

class TicTacToeElite:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: Elite Edition")
        self.root.geometry("450x750")
        self.root.configure(bg="#050a18")
        self.root.resizable(False, False)

        # Global State
        self.user_name = "shree"
        self.user_avatar = "👤"
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.board = [" " for _ in range(9)]
        self.game_mode = "AI"
        self.difficulty = "3"
        self.current_turn = "X"
        self.game_active = True

        self.setup_profile_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- ANIMATION HELPER ---
    def type_text(self, label, text, index=0):
        """Creates a typewriter effect for labels."""
        if index <= len(text):
            label.config(text=text[:index])
            self.root.after(60, self.type_text, label, text, index + 1)

    # --- 1. PROFILE SCREEN ---
    def setup_profile_screen(self):
        self.clear_screen()
        
        container = tk.Frame(self.root, bg="#050a18", pady=50)
        container.pack(expand=True)

        self.title_label = tk.Label(container, text="", font=("Impact", 32), bg="#050a18", fg="#00d4ff")
        self.title_label.pack(pady=20)
        self.type_text(self.title_label, "WELCOME PLAYER")

        tk.Label(container, text="IDENTIFY YOURSELF:", font=("Verdana", 9, "bold"), bg="#050a18", fg="#5f7adb").pack()
        self.name_entry = tk.Entry(container, font=("Verdana", 14), bg="#10182d", fg="white", 
                                   insertbackground="#00d4ff", relief="flat", justify="center", borderwidth=15)
        self.name_entry.insert(0, self.user_name)
        self.name_entry.pack(pady=15)

        self.avatar_var = tk.StringVar(value="👤")
        avatar_frame = tk.Frame(container, bg="#050a18")
        avatar_frame.pack(pady=20)

        avatars = ["👤", "🥷", "🤖", "🚀", "👑"]
        for av in avatars:
            tk.Radiobutton(avatar_frame, text=av, variable=self.avatar_var, value=av, font=("Arial", 22), 
                           bg="#050a18", fg="white", selectcolor="#1a263f", indicatoron=0, 
                           borderwidth=0, padx=10, cursor="hand2").pack(side=tk.LEFT)

        start_btn = tk.Button(container, text="START MISSION", font=("Verdana", 12, "bold"), bg="#00d4ff", fg="#050a18",
                                   activebackground="#00a3c4", padx=40, pady=15, relief="flat", cursor="hand2", 
                                   command=self.save_profile)
        start_btn.pack(pady=30)

    def save_profile(self):
        name = self.name_entry.get().strip()
        if name: self.user_name = name
        self.user_avatar = self.avatar_var.get()
        self.main_menu()

    # --- 2. MAIN MENU (STYLIZED) ---
    def main_menu(self):
        self.clear_screen()
        
        header = tk.Frame(self.root, bg="#10182d", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"{self.user_avatar} AGENT: {self.user_name.upper()}", font=("Verdana", 9, "bold"), 
                 bg="#10182d", fg="#00d4ff").pack()

        # Typewriter Title for Main Menu
        menu_title = tk.Label(self.root, text="", font=("Impact", 50), bg="#050a18", fg="white", pady=50)
        menu_title.pack()
        self.type_text(menu_title, "TIC-TAC-TOE")

        def on_enter(e, color): e.widget['background'] = color
        def on_leave(e, color): e.widget['background'] = color

        battle_btn = tk.Button(self.root, text="DUAL BATTLE", bg="#1a263f", fg="white", 
                               font=("Verdana", 12, "bold"), width=22, pady=15, relief="flat", 
                               cursor="hand2", command=lambda: self.start_game("PVP"))
        battle_btn.pack(pady=15)
        battle_btn.bind("<Enter>", lambda e: on_enter(e, "#253556"))
        battle_btn.bind("<Leave>", lambda e: on_leave(e, "#1a263f"))

        # --- AI TEXT LABEL ABOVE MODES ---
        tk.Label(self.root, text="PLAY WITH COMPUTER", font=("Verdana", 9, "bold"), bg="#050a18", fg="#4a5d8a").pack(pady=10)
        
        modes = [("EASY MODE", "#00ff88", "1"), ("TACTICAL", "#ffcc00", "2"), ("IMPOSSIBLE", "#ff4b2b", "3")]
        for text, color, diff in modes:
            btn = tk.Button(self.root, text=text, bg=color, fg="#050a18", font=("Verdana", 11, "bold"), 
                            width=22, pady=12, relief="flat", cursor="hand2", command=lambda d=diff: self.start_game("AI", d))
            btn.pack(pady=6)

        exit_btn = tk.Button(self.root, text="TERMINATE PROGRAM", font=("Verdana", 8, "bold"), bg="#050a18", fg="#ff4b2b", 
                            relief="flat", cursor="hand2", command=self.root.quit)
        exit_btn.pack(side=tk.BOTTOM, pady=30)

    # --- 3. GAME INTERFACE (Logic remains unchanged) ---
    def start_game(self, mode, diff="3"):
        self.game_mode = mode
        self.difficulty = diff
        self.board = [" " for _ in range(9)]
        self.current_turn = "X"
        self.game_active = True
        self.setup_game_ui()

    def setup_game_ui(self):
        self.clear_screen()
        score_box = tk.Frame(self.root, bg="#10182d", pady=20)
        score_box.pack(fill=tk.X)
        self.score_label = tk.Label(score_box, text="", font=("Verdana", 11, "bold"), bg="#10182d", fg="white")
        self.score_label.pack()
        self.update_score_label()

        self.grid_container = tk.Frame(self.root, bg="#10182d", padx=3, pady=3)
        self.grid_container.pack(pady=40)
        self.grid_frame = tk.Frame(self.grid_container, bg="#050a18")
        self.grid_frame.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.grid_frame, text="", font=("Impact", 36), width=4, height=1,
                            bg="#0f172a", fg="white", relief="flat", activebackground="#1e293b",
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            self.buttons.append(btn)

        self.status_label = tk.Label(self.root, text=f"{self.user_name.upper()}'S TURN (X)", 
                                     font=("Verdana", 12, "bold"), bg="#050a18", fg="#00d4ff")
        self.status_label.pack(pady=10)

        self.ctrl_frame = tk.Frame(self.root, bg="#050a18")
        self.ctrl_frame.pack(pady=20)

    def on_click(self, i):
        if self.board[i] == " " and self.game_active:
            self.make_move(i, self.current_turn)
            if not self.check_end():
                if self.game_mode == "AI":
                    self.game_active = False
                    self.status_label.config(text="SYSTEM ANALYZING...", fg="#5f7adb")
                    self.root.after(600, self.ai_play)
                else:
                    self.current_turn = "O" if self.current_turn == "X" else "X"
                    self.status_label.config(text=f"TURN: {self.current_turn}", 
                                             fg="#00d4ff" if self.current_turn == "X" else "#00ff88")

    def make_move(self, i, char):
        self.board[i] = char
        color = "#00d4ff" if char == "X" else "#00ff88"
        self.buttons[i].config(text=char, state="disabled", disabledforeground=color)

    def ai_play(self):
        move = self.get_ai_move()
        self.game_active = True
        self.make_move(move, "O")
        if not self.check_end():
            self.status_label.config(text=f"{self.user_name.upper()}'S TURN (X)", fg="#00d4ff")

    def get_ai_move(self):
        empty = [i for i, x in enumerate(self.board) if x == " "]
        if self.difficulty == "1": return random.choice(empty)
        if self.difficulty == "2" and random.random() > 0.5: return random.choice(empty)
        best_score, move = -float('inf'), empty[0]
        for i in empty:
            self.board[i] = "O"; score = self.minimax(self.board, False); self.board[i] = " "
            if score > best_score: best_score, move = score, i
        return move

    def minimax(self, board, is_max):
        win = self.check_win_logic(board)
        if win == "O": return 1
        if win == "X": return -1
        if " " not in board: return 0
        scores = []
        for i in range(9):
            if board[i] == " ":
                board[i] = "O" if is_max else "X"; scores.append(self.minimax(board, not is_max)); board[i] = " "
        return max(scores) if is_max else min(scores)

    def check_win_logic(self, b):
        ways = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for w in ways:
            if b[w[0]] == b[w[1]] == b[w[2]] != " ": return b[w[0]]
        return None

    def check_end(self):
        winner = self.check_win_logic(self.board)
        if winner or " " not in self.board:
            self.game_active = False
            if winner: 
                self.scores[winner] += 1
                result_text = "MISSION ACCOMPLISHED!" if winner == "X" else "SYSTEM BREACHED!"
                self.status_label.config(text=result_text, fg="#ffcc00")
            else: 
                self.scores["Draws"] += 1
                self.status_label.config(text="DATA STALEMATE", fg="#5f7adb")
            
            self.update_score_label()
            
            tk.Button(self.ctrl_frame, text="RESTART", font=("Verdana", 10, "bold"), bg="#00ff88", fg="#050a18",
                      width=12, pady=10, relief="flat", cursor="hand2", command=self.setup_game_ui).grid(row=0, column=0, padx=10)
            tk.Button(self.ctrl_frame, text="EXIT", font=("Verdana", 10, "bold"), bg="#1a263f", fg="white",
                      width=12, pady=10, relief="flat", cursor="hand2", command=self.main_menu).grid(row=0, column=1, padx=10)
            return True
        return False

    def update_score_label(self):
        self.score_label.config(text=f"AGENT: {self.scores['X']}   |   CORE: {self.scores['O']}   |   DRAW: {self.scores['Draws']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeElite(root)
    root.mainloop()