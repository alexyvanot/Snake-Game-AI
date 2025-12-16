import time


class TimeEstimator:
    """Estimateur de temps restant pour les taches longues"""

    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = None
        self.step_times = []  # Historique des temps par étape
        self.max_history = 10  # Moyenne mobile sur les X dernières étapes

    def start(self):
        """Démarre le chrono"""
        self.start_time = time.time()
        self.last_step_time = self.start_time

    def step(self, step_number=None):
        """Update l'estimateur après une étape"""
        now = time.time()

        if step_number is not None:
            self.current_step = step_number
        else:
            self.current_step += 1

        # calcul du temps de cette etape
        step_duration = now - self.last_step_time
        self.step_times.append(step_duration)

        # on garder seulement les X dernières étapes pour la moyenne mobile
        if len(self.step_times) > self.max_history:
            self.step_times.pop(0)

        self.last_step_time = now

    def get_elapsed(self):
        """Return le temps écoulé en secondes"""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def get_avg_step_time(self):
        """Return le temps moyen par étape"""
        if not self.step_times:
            return 0
        return sum(self.step_times) / len(self.step_times)

    def get_remaining_time(self):
        """Return le temps restant estimé en secondes"""
        if self.current_step == 0:
            return None

        remaining_steps = self.total_steps - self.current_step
        avg_time = self.get_avg_step_time()

        return remaining_steps * avg_time

    def get_progress_percent(self):
        """Return le pourcentage de progression"""
        if self.total_steps == 0:
            return 100
        return (self.current_step / self.total_steps) * 100

    def get_eta(self):
        """Return l'heure estimée de fin"""
        remaining = self.get_remaining_time()
        if remaining is None:
            return None
        return time.time() + remaining

    @staticmethod
    def format_duration(seconds):
        """Format une durée en string lisible"""
        if seconds is None:
            return "..."

        seconds = int(seconds)

        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}m {secs}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"

    def get_status_string(self):
        """Return un string résumant le status actuel"""
        elapsed = self.format_duration(self.get_elapsed())
        remaining = self.format_duration(self.get_remaining_time())
        percent = self.get_progress_percent()

        return f"{percent:.0f}% - Ecoulé: {elapsed} - Restant: {remaining}"
