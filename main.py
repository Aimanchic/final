from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.log import Log_Scr
from screens.main_scr import Main_Scr
from screens.new_prod import New_Prod_Scr
from screens.reg import RegScr
from screens.manager import Manager_Scr
from screens.new_item import New_It_Scr
from screens.edit_prod import Edit_Prod_Scr

import database


class BakeryApp(App):
    def build(self):
        Window.size = (1000, 600)
        database.create_tables()
        database.create_extended_tables()

        sm = ScreenManager()
        sm.app = self
        self.sm = sm
        self.user_role = None

        sm.add_widget(Log_Scr(name="login"))
        sm.add_widget(Main_Scr(name="products"))
        sm.add_widget(New_Prod_Scr(name="add_product"))
        sm.add_widget(RegScr(name="register"))
        sm.add_widget(Manager_Scr(name="manage_users"))
        sm.add_widget(New_It_Scr(name="add_item"))
        sm.add_widget(Edit_Prod_Scr(name="edit_product"))

        sm.current = "login"

#        database.debug_show_users()

        return sm


if __name__ == "__main__":
    BakeryApp().run()




