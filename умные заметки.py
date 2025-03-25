import tkinter as tk
from tkinter import messagebox
import json

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Умная заметка")
        self.users = self.load_users()
        
        # Регистрация администратора
        if not self.users:
            self.admin_username = "admin"
            admin_password = "password123"
            self.users[self.admin_username] = {
                "password": admin_password, 
                "notes": {}, 
                "is_admin": True
            }
            self.save_users()
        
        self.current_user = None
        self.note_title = None
        self.note_text = None
        
        self.login_page()
    
    def login_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Вход в систему", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Имя пользователя:").pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()
        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack()
        
        tk.Button(self.root, text="Войти", command=self.login, width=10).pack(pady=10)
        tk.Button(self.root, text="Регистрация", command=self.register_page, width=10).pack()
    
    def register_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Регистрация", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Имя пользователя:").pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()
        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack()
        tk.Label(self.root, text="Подтвердите пароль:").pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*", width=30)
        self.confirm_password_entry.pack()
        
        tk.Button(self.root, text="Зарегистрироваться", command=self.register, width=10).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.login_page, width=10).pack()
    
    def main_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Главная страница", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Создать заметку", command=self.create_note_page, width=15).pack(pady=10)
        tk.Button(self.root, text="Просмотреть заметки", command=self.view_notes_page, width=15).pack()
        tk.Button(self.root, text="Редактировать заметку", command=self.edit_note_page, width=15).pack()
        tk.Button(self.root, text="Изменить данные", command=self.change_data_page, width=15).pack()
        
        if self.is_admin():
            tk.Button(self.root, text="Управление пользователями", command=self.manage_users_page, width=20).pack(pady=10)
            tk.Button(self.root, text="Все заметки", command=self.view_all_notes_page, width=20).pack()
        
        tk.Button(self.root, text="Выйти", command=self.login_page, width=10).pack()

    def create_note_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Создать заметку", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Название заметки:").pack()
        self.note_title_entry = tk.Entry(self.root, width=30)
        self.note_title_entry.pack()
        tk.Label(self.root, text="Текст заметки:").pack()
        self.note_text_entry = tk.Text(self.root, height=10, width=40)
        self.note_text_entry.pack()
        
        tk.Button(self.root, text="Создать", command=self.create_note, width=10).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.main_page, width=10).pack()
    
    def view_notes_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Заметки", font=("Arial", 16)).pack(pady=20)
        
        if not self.users[self.current_user]["notes"]:
            tk.Label(self.root, text="Заметок нет.").pack()
        else:
            for title in self.users[self.current_user]["notes"]:
                tk.Button(self.root, text=title, command=lambda title=title: self.show_note(title), width=20).pack(pady=5)
        
        tk.Button(self.root, text="Назад", command=self.main_page, width=10).pack()
    
    def show_note(self, title):
        self.clear_page()
        
        tk.Label(self.root, text=f"Название: {title}", font=("Arial", 14)).pack(pady=10)
        note_text = tk.Text(self.root, height=15, width=50)
        note_text.pack()
        note_text.insert(tk.END, self.users[self.current_user]["notes"][title])
        note_text.config(state="disabled")
        
        tk.Button(self.root, text="Назад", command=self.view_notes_page, width=10).pack()
    
    def edit_note_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Редактировать заметку", font=("Arial", 16)).pack(pady=20)
        
        if not self.users[self.current_user]["notes"]:
            tk.Label(self.root, text="Заметок нет.").pack()
        else:
            for title in self.users[self.current_user]["notes"]:
                tk.Button(self.root, text=title, command=lambda title=title: self.edit_note(title), width=20).pack(pady=5)
        
        tk.Button(self.root, text="Назад", command=self.main_page, width=10).pack()
    
    def edit_note(self, title):
        self.clear_page()
        
        tk.Label(self.root, text=f"Редактировать заметку: {title}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Новый текст заметки:").pack()
        self.note_text_entry = tk.Text(self.root, height=10, width=40)
        self.note_text_entry.insert(tk.END, self.users[self.current_user]["notes"][title])
        self.note_text_entry.pack()
        
        tk.Button(self.root, text="Сохранить изменения", command=lambda title=title: self.save_edit_note(title), width=15).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.edit_note_page, width=10).pack()
    
    def save_edit_note(self, title):
        new_text = self.note_text_entry.get("1.0", tk.END)
        self.users[self.current_user]["notes"][title] = new_text
        self.save_users()
        messagebox.showinfo("Успех", "Заметка отредактирована!")
        self.edit_note_page()
    
    def change_data_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Изменить данные", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Новый логин:").pack()
        self.new_username_entry = tk.Entry(self.root, width=30)
        self.new_username_entry.pack()
        tk.Label(self.root, text="Новый пароль:").pack()
        self.new_password_entry = tk.Entry(self.root, show="*", width=30)
        self.new_password_entry.pack()
        tk.Label(self.root, text="Подтвердите пароль:").pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*", width=30)
        self.confirm_password_entry.pack()
        
        tk.Button(self.root, text="Сохранить изменения", command=self.save_changes, width=15).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.main_page, width=10).pack()

    def save_changes(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if new_password == confirm_password:
            if new_username != self.current_user and new_username in self.users:
                messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
                return
            
            if new_username != self.current_user:
                # Перенос заметок на новый логин
                self.users[new_username] = self.users.pop(self.current_user)
                self.current_user = new_username
            
            self.users[self.current_user]["password"] = new_password
            self.save_users()
            messagebox.showinfo("Успех", "Данные успешно изменены!")
            self.main_page()
        else:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")

    def manage_users_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Управление пользователями", font=("Arial", 16)).pack(pady=20)
        
        for username in self.users:
            if username != self.current_user and not self.users[username].get("is_admin", False):
                frame = tk.Frame(self.root)
                frame.pack(pady=5)
                tk.Label(frame, text=username, width=15).pack(side=tk.LEFT)
                tk.Button(frame, text="Удалить", 
                         command=lambda u=username: self.delete_user(u)).pack(side=tk.LEFT)
        
        tk.Button(self.root, text="Назад", command=self.main_page, width=10).pack()

    def delete_user(self, username):
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            del self.users[username]
            self.save_users()
            self.manage_users_page()

    def view_all_notes_page(self):
        self.clear_page()
        
        tk.Label(self.root, text="Все заметки пользователей", font=("Arial", 16)).pack(pady=20)
        
        for username in self.users:
            if username != self.current_user:
                user_notes = self.users[username]["notes"]
                if user_notes:
                    tk.Label(self.root, text=f"Пользователь: {username}", font=("Arial", 12)).pack()
                    for title in user_notes:
                        frame = tk.Frame(self.root)
                        frame.pack(pady=2)
                        tk.Button(frame, text=title, width=20,
                                 command=lambda u=username, t=title: self.admin_note_actions(u, t)).pack(side=tk.LEFT)
        
        tk.Button(self.root, text="Назад", command=self.main_page, width=10).pack()

    def admin_note_actions(self, username, title):
        self.clear_page()
        
        tk.Label(self.root, text=f"Заметка: {title}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Пользователь: {username}").pack()
        
        # Просмотр содержимого заметки
        note_text = tk.Text(self.root, height=10, width=50)
        note_text.insert(tk.END, self.users[username]["notes"][title])
        note_text.pack(pady=10)
        
        # Кнопки управления
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        tk.Button(frame, text="Редактировать", 
                 command=lambda: self.edit_note_admin(username, title)).pack(side=tk.LEFT)
        tk.Button(frame, text="Удалить", 
                 command=lambda: self.delete_note_admin(username, title)).pack(side=tk.LEFT)
        tk.Button(self.root, text="Назад", command=self.view_all_notes_page, width=10).pack()

    def edit_note_admin(self, username, title):
        self.clear_page()
        
        tk.Label(self.root, text=f"Редактирование заметки {title}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Пользователь: {username}").pack()
        
        self.note_text_entry = tk.Text(self.root, height=10, width=50)
        self.note_text_entry.insert(tk.END, self.users[username]["notes"][title])
        self.note_text_entry.pack(pady=10)
        
        tk.Button(self.root, text="Сохранить", 
                 command=lambda: self.save_admin_edit(username, title), width=10).pack()
        tk.Button(self.root, text="Назад", 
                 command=lambda: self.admin_note_actions(username, title), width=10).pack()

    def save_admin_edit(self, username, title):
        new_text = self.note_text_entry.get("1.0", tk.END)
        self.users[username]["notes"][title] = new_text
        self.save_users()
        messagebox.showinfo("Успех", "Заметка успешно изменена!")
        self.admin_note_actions(username, title)

    def delete_note_admin(self, username, title):
        if messagebox.askyesno("Подтверждение", f"Удалить заметку {title}?"):
            del self.users[username]["notes"][title]
            self.save_users()
            self.view_all_notes_page()

    def is_admin(self):
        return self.users[self.current_user].get("is_admin", False)

    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.main_page()
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль.")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if password == confirm_password:
            if username not in self.users:
                self.users[username] = {"password": password, "notes": {}}
                self.save_users()
                messagebox.showinfo("Успех", "Регистрация успешна!")
                self.login_page()
            else:
                messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
        else:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
    
    def create_note(self):
        title = self.note_title_entry.get()
        text = self.note_text_entry.get("1.0", tk.END)
        
        self.users[self.current_user]["notes"][title] = text
        self.save_users()
        messagebox.showinfo("Успех", "Заметка создана!")
        self.main_page()
    
    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def save_users(self):
        with open('users.json', 'w') as file:
            json.dump(self.users, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = NoteApp(root)
    root.mainloop()
