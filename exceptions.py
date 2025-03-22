class Impossible(Exception):

    pass

class QuitWithoutSaving(SystemExit):
    """Can be raised to exit the game without automatically saving."""

    pass