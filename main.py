from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from sqlite3 import connect
from kivymd.app import MDApp


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = connect('database.sqlite3')
        self.cursor = self.database.cursor()
        self.create_table()  # Chama o método para criar a tabela
        self.input_text = TextInput()
        self.list_view = MDList()

    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS names (name TEXT);"
        self.cursor.execute(query)
        self.database.commit()

    def build(self):
        root = BoxLayout(orientation='vertical')
        button_save = Button(text="Salvar")
        button_list = Button(text="Listar")
        button_save.bind(on_press=self.save_name)
        button_list.bind(on_press=self.list_names)

        root.add_widget(self.input_text)
        root.add_widget(button_save)
        root.add_widget(button_list)

        scroll_view = MDScrollView()
        scroll_view.add_widget(self.list_view)
        root.add_widget(scroll_view)

        return root

    def save_name(self, instance):
        name = self.input_text.text
        self.cursor.execute("INSERT INTO names (name) VALUES (?);", (name,))
        self.database.commit()
        self.input_text.text = ""  # Limpa o TextInput após salvar

    def list_names(self, instance):
        self.cursor.execute("SELECT name FROM names;")
        names = self.cursor.fetchall()
        self.list_view.clear_widgets()
        for name in names:
            item = OneLineListItem(text=name[0])
            self.list_view.add_widget(item)


if __name__ == "__main__":
    MainApp().run()
