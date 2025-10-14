import dearpygui.dearpygui as dpg
import random, time, threading

# Create the main context
dpg.create_context()

# Global variable for the note label
note_label = None

# List of possible notes (placeholder for real detection)
NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

# Function to simulate live note changes
def update_note():
    while dpg.is_dearpygui_running():
        note = random.choice(NOTES)
        dpg.set_value("note_text", f"🎵 Detected Note: {note}")
        time.sleep(0.5)  # Update every half second

# Main window
with dpg.window(label="MUGUI - Music Note Detector", width=400, height=200):
    note_label = dpg.add_text("🎶 Waiting for input...", tag="note_text")
    dpg.add_separator()
    dpg.add_text("This is a live note display prototype.")

# Setup and show viewport
dpg.create_viewport(title='MUGUI', width=400, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()

# Run update function in the background
threading.Thread(target=update_note, daemon=True).start()

# Start the GUI loop
dpg.start_dearpygui()
dpg.destroy_context()
