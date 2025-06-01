from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial

import database

Builder.load_file("kivy_files/main_scr.kv")

class Main_Scr(Screen):
    def on_pre_enter(self):
        self.products = database.get_all_products()
        self.items = database.get_all_items()

        self.filter_products("")
        self.filter_items("")

        user_role = App.get_running_app().user_role
        self.ids.manage_users_btn.opacity = 1 if user_role == "owner" else 0
        self.ids.manage_users_btn.disabled = user_role != "owner"

    def filter_products(self, query):
        query = query.lower()
        self.ids.products_box.clear_widgets()

        grouped = {}
        for prod in self.products:
            key = (prod[1].lower(), prod[2], prod[4])  # name, category, price
            if query in prod[1].lower():
                grouped.setdefault(key, []).append(prod)

        for (name, category, price), prods in grouped.items():
            total_qty = sum(p[3] for p in prods)
            any_prod = prods[0]

            item = BoxLayout(size_hint_y=None, height=40, spacing=10)
            item.add_widget(Label(text=name, font_size=16))
            item.add_widget(Label(text=category, font_size=16))
            item.add_widget(Label(text=str(total_qty), font_size=16))
            item.add_widget(Label(text=str(price), font_size=16))

            edit_btn = Button(text="Изменить", size_hint_x=None, width=180, font_size=16)
            edit_btn.bind(on_release=self.make_edit_handler(any_prod))
            item.add_widget(edit_btn)

            self.ids.products_box.add_widget(item)

    def make_edit_handler(self, product):
        return lambda *args: self.edit_product(product)

    def filter_items(self, query):
        query = query.lower()
        self.ids.items_box.clear_widgets()

        items = database.get_all_items_full()  # список кортежей (name, quantity, price)

        for name, qty, price in items:
            if query in name.lower():
                row = BoxLayout(size_hint_y=None, height=30, spacing=10)

                row.add_widget(Label(text=name))
                minus_btn = Button(text="-", size_hint_x=None, width=40)
                minus_btn.bind(on_release=partial(self.change_item_qty, name, -1))
                row.add_widget(minus_btn)

                row.add_widget(Label(text=str(qty)))
                plus_btn = Button(text="+", size_hint_x=None, width=40)
                plus_btn.bind(on_release=partial(self.change_item_qty, name, 1))
                row.add_widget(plus_btn)

                row.add_widget(Label(text=str(price)))

                self.ids.items_box.add_widget(row)

    def change_item_qty(self, item_name, delta, *args):
        if delta > 0:
            success = database.increase_item_quantity(item_name)
        else:
            success = database.decrease_item_quantity(item_name)

        if success:
            self.items = database.get_all_items()
            self.products = database.get_all_products()
            self.filter_products(self.ids.product_search.text)
            self.filter_items(self.ids.item_search.text)

    def edit_product(self, product):
        self.manager.current_product = product
        self.manager.current = "edit_product"


