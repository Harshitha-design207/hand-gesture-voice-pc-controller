import customtkinter as ctk
import psutil
import random
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ---------------- SETTINGS ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ---------------- DASHBOARD ----------------

class AdminDashboard:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.geometry("1600x900")

        self.root.title("AI ADMIN DASHBOARD")

        self.command_count = 0

        self.create_ui()

        self.update_system()

        self.update_logs()

        self.update_graphs()

        self.root.mainloop()

    # ---------------- UI ----------------

    def create_ui(self):

        # HEADER
        header = ctk.CTkFrame(
            self.root,
            height=80,
            fg_color="#0f172a",
            corner_radius=20
        )

        header.pack(fill="x", padx=20, pady=20)

        title = ctk.CTkLabel(
            header,
            text="AI ADMIN MONITORING DASHBOARD",
            font=("Arial", 32, "bold"),
            text_color="cyan"
        )

        title.pack(side="left", padx=30, pady=20)

        # LIVE STATUS
        self.status_label = ctk.CTkLabel(
            header,
            text="● SYSTEM ONLINE",
            font=("Arial", 20, "bold"),
            text_color="lime"
        )

        self.status_label.pack(side="right", padx=30)

        # ANALYTICS FRAME
        analytics = ctk.CTkFrame(
            self.root,
            fg_color="#111827",
            corner_radius=20
        )

        analytics.pack(fill="x", padx=20, pady=10)

        # CARDS
        self.cpu_card = self.create_card(
            analytics,
            "CPU",
            "0%",
            "lime"
        )

        self.cpu_card.pack(side="left", padx=20, pady=20)

        self.ram_card = self.create_card(
            analytics,
            "RAM",
            "0%",
            "cyan"
        )

        self.ram_card.pack(side="left", padx=20, pady=20)

        self.command_card = self.create_card(
            analytics,
            "COMMANDS",
            "0",
            "orange"
        )

        self.command_card.pack(side="left", padx=20, pady=20)

        self.user_card = self.create_card(
            analytics,
            "ACTIVE USERS",
            "1",
            "yellow"
        )

        self.user_card.pack(side="left", padx=20, pady=20)

        # MAIN CONTENT
        content = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        content.pack(fill="both", expand=True, padx=20, pady=20)

        # LEFT SIDE
        left = ctk.CTkFrame(
            content,
            fg_color="#111827",
            corner_radius=20
        )

        left.pack(side="left", fill="both", expand=True, padx=10)

        # RIGHT SIDE
        right = ctk.CTkFrame(
            content,
            width=400,
            fg_color="#111827",
            corner_radius=20
        )

        right.pack(side="right", fill="y", padx=10)

        # ---------------- GRAPH ----------------

        graph_title = ctk.CTkLabel(
            left,
            text="REAL-TIME ANALYTICS",
            font=("Arial", 24, "bold"),
            text_color="cyan"
        )

        graph_title.pack(pady=20)

        self.figure = Figure(figsize=(8,4), dpi=100)

        self.ax = self.figure.add_subplot(111)

        self.chart = FigureCanvasTkAgg(self.figure, left)

        self.chart.get_tk_widget().pack(fill="both", expand=True)

        # ---------------- USER TABLE ----------------

        table_title = ctk.CTkLabel(
            left,
            text="USER ACTIVITY TABLE",
            font=("Arial", 24, "bold"),
            text_color="yellow"
        )

        table_title.pack(pady=20)

        self.table = ctk.CTkTextbox(
            left,
            height=200,
            font=("Consolas", 16)
        )

        self.table.pack(fill="x", padx=20, pady=20)

        # ---------------- LOGS ----------------

        logs_title = ctk.CTkLabel(
            right,
            text="LIVE LOGS",
            font=("Arial", 24, "bold"),
            text_color="lime"
        )

        logs_title.pack(pady=20)

        self.logs = ctk.CTkTextbox(
            right,
            width=350,
            height=300,
            font=("Consolas", 14)
        )

        self.logs.pack(padx=20, pady=20)

        # ---------------- SECURITY ----------------

        security_title = ctk.CTkLabel(
            right,
            text="SECURITY MONITOR",
            font=("Arial", 24, "bold"),
            text_color="red"
        )

        security_title.pack(pady=20)

        self.security = ctk.CTkTextbox(
            right,
            width=350,
            height=200,
            font=("Consolas", 14)
        )

        self.security.pack(padx=20, pady=20)

        self.security.insert(
            "end",
            "✔ System Secure\n✔ No threats detected\n"
        )

    # ---------------- CREATE CARD ----------------

    def create_card(self, parent, title, value, color):

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=140,
            corner_radius=25,
            fg_color="#1e293b",
            border_width=2,
            border_color=color
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 22, "bold"),
            text_color=color
        )

        title_label.pack(pady=10)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 32, "bold"),
            text_color="white"
        )

        value_label.pack()

        card.value_label = value_label

        return card

    # ---------------- UPDATE SYSTEM ----------------

    def update_system(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        self.command_count += random.randint(1, 5)

        self.cpu_card.value_label.configure(text=f"{cpu}%")

        self.ram_card.value_label.configure(text=f"{ram}%")

        self.command_card.value_label.configure(
            text=f"{self.command_count}"
        )

        self.root.after(1000, self.update_system)

    # ---------------- UPDATE LOGS ----------------

    def update_logs(self):

        actions = [
            "Opened Chrome",
            "Opened YouTube",
            "Played Song",
            "Voice Command",
            "Gesture Command",
            "Opened ChatGPT",
            "Opened Settings"
        ]

        action = random.choice(actions)

        current_time = time.strftime("%H:%M:%S")

        log = f"{current_time} - {action}\n"

        self.logs.insert("end", log)

        self.logs.see("end")

        # USER TABLE
        table_data = (
            f"USER: Harshitha | "
            f"ACTION: {action} | "
            f"TIME: {current_time}\n"
        )

        self.table.insert("end", table_data)

        self.table.see("end")

        self.root.after(3000, self.update_logs)

    # ---------------- UPDATE GRAPH ----------------

    def update_graphs(self):

        self.ax.clear()

        commands = [random.randint(10, 50) for _ in range(5)]

        gestures = [random.randint(5, 30) for _ in range(5)]

        voice = [random.randint(5, 40) for _ in range(5)]

        x = [1,2,3,4,5]

        self.ax.plot(x, commands, linewidth=3)

        self.ax.plot(x, gestures, linewidth=3)

        self.ax.plot(x, voice, linewidth=3)

        self.ax.set_title("AI Command Analytics")

        self.chart.draw()

        self.root.after(3000, self.update_graphs)

# ---------------- RUN ----------------

AdminDashboard()