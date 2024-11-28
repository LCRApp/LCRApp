import openai
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# Remplacez 'votre_clé_api_openai' par votre clé API OpenAI
openai.api_key = 'vsk-proj-paq6wkN3zSFuxVi0nucmK4FKtuwrpA417DRWXdGa6o_HTVShimKEmVgAmt773KR1JUZgqlpH73T3BlbkFJzM6JWTtaXh-oOtKv3xC1X7-Xkn-_S0o8cDFcZvOIu9in5MaHRhcqA_LwouJkoCiJ008o9exgoA'  # Clé API OpenAI

class HomeScreen(Screen):
    def on_button_click(self, screen_name):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screen_name

class RecognitionScreen(Screen):
    def on_button_click(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'

    def on_prevention_button_click(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'prevention'

class PreventionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text="Entrez le nom du ravageur pour les mesures de prévention", font_size=20)
        self.pest_name_input = TextInput(hint_text="Nom du ravageur", size_hint_y=None, height=30)
        self.get_prevention_button = Button(text="Obtenir les mesures de prévention", size_hint_y=None, height=40)
        self.result_label = Label(text="", font_size=16, size_hint_y=None, height=300)

        # Définir les actions des boutons
        self.get_prevention_button.bind(on_press=self.fetch_prevention_measures)

        # Organiser les widgets
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        layout.add_widget(self.label)
        layout.add_widget(self.pest_name_input)
        layout.add_widget(self.get_prevention_button)
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def fetch_prevention_measures(self, instance):
        pest_name = self.pest_name_input.text.strip()
        
        if pest_name:
            try:
                # Requête à l'API OpenAI avec la syntaxe correcte
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Choisir le modèle GPT-3.5 ou GPT-4
                    messages=[
                        {"role": "system", "content": "Tu es un assistant qui fournit des informations sur les ravageurs."},
                        {"role": "user", "content": f"Quelles sont les mesures de prévention pour {pest_name} ?"}
                    ]
                )

                # Extraire la réponse
                prevention_message = response['choices'][0]['message']['content'].strip()
                self.result_label.text = f"Mesures de prévention:\n\n{prevention_message}"

            except Exception as e:  # Utiliser une exception générique
                self.result_label.text = f"Erreur lors de la récupération des données: {str(e)}"
        else:
            self.result_label.text = "Veuillez entrer un nom de ravageur."

class SolutionsScreen(Screen):
    def on_button_click(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'

class FormationsScreen(Screen):
    def on_button_click(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'

class LCRApp(App):
    def build(self):
        Builder.load_file('style.kv')  # Charger le fichier .kv
        sm = ScreenManager()  # Créer le gestionnaire d'écrans
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RecognitionScreen(name='recognition'))
        sm.add_widget(PreventionScreen(name='prevention'))
        sm.add_widget(SolutionsScreen(name='solutions'))
        sm.add_widget(FormationsScreen(name='formations'))
        return sm

if __name__ == '__main__':
    LCRApp().run()
