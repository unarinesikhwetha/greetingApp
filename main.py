import flet as ft


def main(page: ft.Page):
  page.title = "Two-View Greeting App"
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

  # Requirement 1: Keep the entered name in a variable inside main so both views can use it.
  user_name = ft.TextField(
      label="Enter your name",
      width=300,
      autofocus=True,
  )

  # Greeting text control for the second view
  greeting_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)

  # Route change handler to manage views
  def route_change(route):
    page.views.clear()

    # Home view (/)
    page.views.append(
        ft.View(
            "/",
            [
                ft.AppBar(
                    title=ft.Text("Home View"), background_color=ft.colors.BLUE
                ),
                ft.Column(
                    [
                        ft.Text(
                            "Welcome!",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        user_name,
                        ft.ElevatedButton(
                            text="Continue",
                            # Async click handler for navigation
                            on_click=on_continue_click,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Greeting view (/greeting)
    if page.route == "/greeting":
      greeting_text.value = f"Hello, {user_name.value}!"
      page.views.append(
          ft.View(
              "/greeting",
              [
                  ft.AppBar(
                      title=ft.Text("Greeting View"),
                      background_color=ft.colors.GREEN,
                  ),
                  ft.Column(
                      [
                          greeting_text,
                          ft.ElevatedButton(
                              text="Back",
                              on_click=lambda _: page.maybe_pop(),
                          ),
                      ],
                      alignment=ft.MainAxisAlignment.CENTER,
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                      spacing=20,
                  ),
              ],
              vertical_alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          )
      )

    page.update()

  def view_pop(view):
    page.views.pop()
    top_view = page.views[-1]
    page.route = top_view.route
    page.update()

  page.on_route_change = route_change
  page.on_view_pop = view_pop

  # Async click handler for the Continue button
  async def on_continue_click(e):
    # Requirement 2: If the name field is empty, show an AlertDialog instead of navigating.
    if not user_name.value.strip():
      dlg = ft.AlertDialog(
          title=ft.Text("Validation Error"),
          content=ft.Text("Please enter your name before continuing."),
          actions=[ft.TextButton("OK", on_click=lambda _: close_dlg(dlg))],
      )
      page.dialog = dlg
      dlg.open = True
      page.update()
    else:
      # Navigate to greeting view using page.route
      page.route = "/greeting"
      page.update()

  def close_dlg(dlg):
    dlg.open = False
    page.update()

  # Start at root view using page.route
  page.route = "/"
  page.update()


# Requirement 3: Start the app with ft.run
if __name__ == "__main__":
  ft.run(main)