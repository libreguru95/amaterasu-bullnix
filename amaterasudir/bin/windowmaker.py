import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import subprocess
import os
import threading
from datetime import datetime

class CustomDesktop:
    def __init__(self, master):
        self.master = master
        self.master.title("Window Maker 2000")
        self.master.configure(bg="#008080")
        self.master.geometry("800x600")

        # Меню
        menu_bar = Menu(master)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Terminal", command=self.open_new_window)
        file_menu.add_command(label="Open Text Editor", command=self.open_text_editor)
        file_menu.add_command(label="Open File Explorer", command=self.open_file_explorer)  # Новый пункт меню
        file_menu.add_command(label="Exit", command=master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        master.config(menu=menu_bar)

        # Панель инструментов
        self.toolbar = ttk.Frame(master, relief=tk.RAISED, borderwidth=2)
        self.open_terminal_button = ttk.Button(self.toolbar, text="Open Terminal", command=self.open_new_window)
        self.open_terminal_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.open_editor_button = ttk.Button(self.toolbar, text="Open Text Editor", command=self.open_text_editor)
        self.open_editor_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Статусная строка
        self.status = tk.StringVar()
        self.status.set("Ready")
        self.status_bar = tk.Label(master, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Запуск обновления времени
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status.set(f"Ready | Time: {current_time}")
        self.master.after(1000, self.update_time)

    def open_new_window(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("TermX")
        new_window.geometry("400x300")

        self.text_area = tk.Text(new_window, bg="black", fg="white", font=("Courier", 10))
        self.text_area.pack(expand=True, fill='both')

        self.text_area.bind("<Return>", self.send_command)
        self.text_area.bind("<Key>", self.on_key_press)

        self.process = subprocess.Popen(
            ["python", os.path.join(os.path.dirname(os.path.abspath(__file__)), "keitou.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, universal_newlines=True
        )

        threading.Thread(target=self.read_output, daemon=True).start()

    def send_command(self, event):
        command = self.text_area.get("end-2c linestart", "end-1c")
        self.text_area.insert(tk.END, "\n")

        if command.strip() == "clear":
            self.text_area.delete(1.0, tk.END)
        else:
            if self.process:
                self.process.stdin.write(command + "\n")
                self.process.stdin.flush()

        return "break"

    def read_output(self):
        for line in self.process.stdout:
            self.update_text_area(line)

    def update_text_area(self, output):
        self.text_area.insert(tk.END, output)
        self.text_area.see(tk.END)

    def on_key_press(self, event):
        if event.keysym == "Return":
            return "break"

    def open_text_editor(self):
        editor_window = tk.Toplevel(self.master)
        editor_window.title("Imacs+")
        editor_window.geometry("600x400")

        self.editor_text_area = tk.Text(editor_window, wrap='word')
        self.editor_text_area.pack(expand=True, fill='both')

        editor_menu = Menu(editor_window)
        file_menu = Menu(editor_menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        editor_menu.add_cascade(label="File", menu=file_menu)
        editor_window.config(menu=editor_menu)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.editor_text_area.delete(1.0, tk.END)
                    self.editor_text_area.insert(tk.END, content)
                    self.status.set(f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    content = self.editor_text_area.get(1.0, tk.END)
                    file.write(content)
                    self.status.set(f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    content = self.editor_text_area.get(1.0, tk.END)
                    file.write(content)
                    self.status.set(f"Saved as: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def open_file_explorer(self):
        explorer_window = tk.Toplevel(self.master)
        explorer_window.title("File Explorer")
        explorer_window.geometry("600x400")

        # Создаем виджет Treeview для отображения файлов и папок
        self.tree = ttk.Treeview(explorer_window)
        self.tree.pack(expand=True, fill='both')

        # Добавляем вертикальный скроллбар
        scrollbar = ttk.Scrollbar(explorer_window, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Заполняем дерево файлами и папками
        self.populate_tree()

        # Двойной клик для открытия папки или файла
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def populate_tree(self, path=""):
        # Очищаем текущее содержимое
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Получаем список файлов и папок
        if path == "":
            path = os.path.expanduser("~")  # Начинаем с домашней директории

        self.tree.insert("", "end", path, text=os.path.basename(path), open=True)

        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                is_dir = os.path.isdir(full_path)
                self.tree.insert(path, "end", full_path, text=entry, open=False)
        except Exception as e:
            messagebox.showerror("Error", f"Could not list directory: {e}")

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()[0]
        if os.path.isdir(selected_item):
            self.populate_tree(selected_item)  # Заполняем дерево содержимым выбранной папки
        else:
            os.startfile(selected_item)  # Открываем файл

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomDesktop(root)
    root.mainloop()
