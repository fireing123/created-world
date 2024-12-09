from pygameHelper import Event, on_reset

on_broken = Event()

def on_reset_event():
    on_broken.clear()

on_reset.add_lisner(on_reset_event)