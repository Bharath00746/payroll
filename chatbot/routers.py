class EmployeeRouter:
    """
    A router to control all database operations on models in the 'chatbot' app.
    """

    def db_for_read(self, model, **hints):
        """Point read operations for chatbot models to 'default' DB."""
        if model._meta.app_label == 'chatbot':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """Point write operations for chatbot models to 'default' DB."""
        if model._meta.app_label == 'chatbot':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if either model belongs to the chatbot app."""
        if obj1._meta.app_label == 'chatbot' or obj2._meta.app_label == 'chatbot':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure chatbot app only appears in the 'default' DB."""
        if app_label == 'chatbot':
            return db == 'default'
        return None
