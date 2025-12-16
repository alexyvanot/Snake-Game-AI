class BackToMenuException(Exception):
    pass


class GameEventHandler:
    def __init__(self, vue):
        self.vue = vue
    
    def handle(self, event):
        if self.vue.back_button.is_clicked(event):
            raise BackToMenuException()
        if self.vue.stats_button.is_clicked(event):
            self.vue.stats_panel.toggle()
