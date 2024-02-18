"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx
import json
import time


class State(rx.State):
    """The app state."""

class searchbarState(rx.State):
    """The state of the homepage searchbar"""
    oscillating: bool = True
    text: str = "Chest pain"
    word_list: list = json.load(open("assets/samples.json"))["terms"]
    word_index: int = 0
    def reset_states(self):
        self.oscillating = True
        self.text = "Chest pain"
        self.word_index = 0

    #functions to enable word oscillations
    def pause_oscillation(self, text):
        self.oscillating = False
    def resume_oscillation(self, text):
        self.oscillating = True
    @rx.background
    async def iterate_word(self):
        while True:
            async with self:
                if self.oscillating:
                    self.text = self.word_list[self.word_index]
                    self.word_index = (self.word_index + 1) % len(self.word_list)
                    time.sleep(0.1)



class QueryState(rx.State):
    query: str = ""


@rx.page(on_load=searchbarState.reset_states)
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Welcome to Rondo!", size="9"),
            rx.hstack(
                rx.input(size="4",
                         value = searchbarState.text,
                         on_focus=searchbarState.pause_oscillation,
                         on_mount=searchbarState.iterate_word,
                         on_change=searchbarState.set_text,),
                rx.button(
                    "Go",
                    size="4",
            )),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )

# def search() -> rx.Component:
#     return rx.center(
#         rx.vstack(
#             rx.heading("Search Results:", size="9"),
#             rx.box(
#                 rx.hstack(
#                     rx.text("Query: ",size = "4", weight = "bold"),
#                     rx.text("Chest Pain",size = "4", weight = "regular")
#                 )
#             )
#         )
#     )


app = rx.App()
app.add_page(index)
