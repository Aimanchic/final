from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import database
from kivy.app import App

Builder.load_file("kivy_files/reg.kv")

class RegScr(Screen):

    def on_pre_enter(self):
        role = App.get_running_app().user_role
        if role != "owner":
            self.manager.current = "products"

    def register(self):
        role = App.get_running_app().user_role
        if role != "owner":
            self.ids.message.text = "Доступ только для владельца"
            return

        username = self.ids.username_input.text
        password = self.ids.password_input.text

        success = database.register_user(username, password, "employee")
        if success:
            self.ids.message.text = "Сотрудник добавлен"
        else:
            self.ids.message.text = "Такой пользователь уже существует"
