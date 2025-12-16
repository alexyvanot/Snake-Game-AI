class BackToMenuException(Exception):
    pass


class GameEventHandler:
    
    @staticmethod
    def should_return_to_menu(event, back_button):
        import pygame
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button and back_button.is_clicked(event.pos):
                return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return False
