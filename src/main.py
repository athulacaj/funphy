import flet as ft
import threading
import time


def main(page: ft.Page):
    # Set page background color
    page.bgcolor = "transparent"
    
    # Create background image from URL
    background_image = ft.Image(
        src="https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1600&auto=format&fit=crop",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER,
    )
    
    counter = ft.Text("0", size=50, data=0, color="white")

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()
    
    # Auto increment function with threading
    def auto_increment():
        while True:
            time.sleep(2)  # Wait for 2 seconds
            # Use page.update to make UI changes from another thread
            counter.data += 1
            counter.value = str(counter.data)
            page.update()  # Update the whole page to refresh the counter
    
    # Start auto increment in a separate thread
    threading.Thread(target=auto_increment, daemon=True).start()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )
    
    # Add a Stack control to layer the counter on top of the background image
    page.add(
        ft.Stack(
            [
                background_image,
                ft.SafeArea(
                    ft.Container(
                        counter,
                        alignment=ft.alignment.center,
                    ),
                    expand=True,
                )
            ],
            expand=True,
        )
    )


ft.app(main)
