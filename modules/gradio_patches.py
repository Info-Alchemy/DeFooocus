# IA-2024-07: Introduced Gradio Monkey Patching to add a logout route, and updated Tab to inherit from Changeable
import gradio as gr
from fastapi import status
from fastapi.responses import RedirectResponse
from gradio.blocks import BlockContext
from gradio.events import Changeable, Selectable
from gradio.routes import App
from gradio.layouts import Tab

original_create_app = App.create_app
original_init = Tab.__init__


def new_create_app(self, *args, **kwargs):
    app = original_create_app(self, *args, **kwargs)

    @app.get("/logout")
    def logout_route():
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key="access-token")
        response.delete_cookie(key="access-token-unsecure")
        print("Logout user!")
        return response
        # return self.logout()

    return app


def new_init(self, label: str, visible: bool = True, interactive: bool = True, *, id: int | str | None = None,
             elem_id: str | None = None, **kwargs):
    # Call BlockContext.__init__
    BlockContext.__init__(self, visible=visible, elem_id=elem_id, **kwargs)

    # Call Changeable.__init__
    Changeable.__init__(self)

    # Call Selectable.__init__
    Selectable.__init__(self)

    # Set attributes
    self.label = label
    self.id = id
    self.visible = visible
    self.interactive = interactive


App.create_app = new_create_app
Tab.__init__ = new_init

# Ensure Tab inherits from Changeable if it doesn't already
if Changeable not in Tab.__bases__:
    Tab.__bases__ = (*Tab.__bases__, Changeable)

# Update the __doc__ string to reflect the changes
Tab.__doc__ = Tab.__doc__.replace(
    "Parameters:",
    "Parameters:\n            visible: Whether the tab is visible. Defaults to True.\n            interactive: Whether the tab is interactive. Defaults to True."
)
# IA-2024-07: End of Gradio Monkey Patching to add a logout route, and updated Tab to inherit from Changeable
