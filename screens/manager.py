from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import database
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

Builder.load_file("kivy_files/manager.kv")

class Manager_Scr(Screen):
    def on_pre_enter(self):
        role = App.get_running_app().user_role
        if role != "owner":
            self.manager.current = "products"
            return

        self.ids.username_input.text = ""
        self.ids.password_input.text = ""
        self.ids.message.text = ""

        self.ids.user_list.clear_widgets()
        users = database.get_all_users()
        for username, role in users:
            if username == "admin":
                continue
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(Label(text=username))
            row.add_widget(Label(text=role))
            delete_btn = Button(text="Удалить", size_hint_x=0.3)
            delete_btn.bind(on_press=lambda instance, u=username: self.delete_user(u))
            row.add_widget(delete_btn)
            self.ids.user_list.add_widget(row)

    def delete_user(self, username):
        database.delete_user(username)
        self.on_pre_enter()

    def add_user(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        if not username or not password:
            self.ids.message.text = "Заполните все поля"
            return
        success = database.register_user(username, password, "employee")
        if success:
            self.ids.message.text = "Сотрудник добавлен"
            self.on_pre_enter()
        else:
            self.ids.message.text = "Пользователь уже существует"
