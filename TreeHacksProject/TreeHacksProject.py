"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx
import json
import time

import TreeHacksProject.searcher.search_results as search_results
import TreeHacksProject.searcher.searcher as searcher

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
    @rx.var
    def get_text(self) -> str:
        return self.text
    
    """The states of the search page"""
    _results: search_results.SearchResults = None
    result_link1: str = ""
    result_title1: str = ""
    result_link2: str = ""
    result_title2: str = ""
    result_link3: str = ""
    result_title3: str = ""
    

    #functions to enable word oscillations
    def pause_oscillation(self, text):
        self.oscillating = False
    def pause_oscillation_(self):
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
    
    #functions to run a search
    def get_results(self):
        self._results = searcher.search(self.text)
        self.result_title1 = self._results.results[0][0]
        self.result_link1 = self._results.results[0][1]
        self.result_title2 = self._results.results[1][0]
        self.result_link2 = self._results.results[1][1]
        self.result_title3 = self._results.results[2][0]
        self.result_link3 = self._results.results[2][1]
    
    # def update_result_fields(self, index: int):
    #     self.result_title = self._results.results[0][0]
    #     self.result_link = self._results.results[0][1]


    



# class QueryState(rx.State):
#     text: str = "pig"
#     def init_query(self):
#         self.text = searchbarState.text
#         print(self.text)



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
                rx.link(
                    rx.button(
                    "Go",
                    size="4",
                    on_click=searchbarState.pause_oscillation_),
                    href="/search"
                )
            ),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )

@rx.page(on_load=searchbarState.get_results)
def search() -> rx.Component:
    return rx.box( 
        rx.center(
            rx.vstack(
                rx.heading("Search Results:", size="7"),
                padding="10px"
            )
        ),
        rx.box(
            rx.hstack(
                rx.text("Query: ",size = "8", weight = "bold"),
                rx.text(searchbarState.text, size="8", weight="medium"),
            ),
            width="100%",
            background_color="var(--accent-2)",
            border_radius="15px",
            align = "start",
            padding = "5px"
        ),
        rx.grid(
            rx.card("hi"),
            rx.card(
                rx.heading("Results", size="7"),
                rx.box(
                    rx.flex(
                        rx.link(
                            rx.card(
                                rx.heading(searchbarState.result_title1),
                                _hover={
                                    "color": "white",
                                    "background_color": "navy"}
                            ),
                            href=searchbarState.result_link1
                        ),
                        rx.divider(),
                        rx.link(
                            rx.card(
                                rx.heading(searchbarState.result_title2),
                                _hover={
                                    "color": "white",
                                    "background_color": "navy"}
                            ),
                            href=searchbarState.result_link2
                        ),
                        rx.divider(),
                        rx.link(
                            rx.card(
                                rx.heading(searchbarState.result_title3),
                                _hover={
                                    "color": "white",
                                    "background_color": "navy"}
                            ),
                            href=searchbarState.result_link3
                        ),
                        spacing = "4",
                        direction="column",
                    ),
                    width="100%",
                    background_color="var(--plum-2)",
                    border_radius="15px",
                    padding = "5px",
                )
            ),
            columns = "2"
        )
    )


app = rx.App()
app.add_page(index)
app.add_page(search)
