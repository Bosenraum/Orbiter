import copy
import json

import easygui
import pygame
import sys
import random

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2

from data.team_names import generate_team_names
from data.player_names import generate_player_names


from league import *


class LeagueEngine(Engine):
    APP_NAME = "The League"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", True)

        # Create the league
        self.league = League("Major League League", 0, 30, 10, 10)
        self.league.create_teams(generate_team_names(self.league.num_teams))
        self.league.create_players(generate_player_names(self.league.num_players))
        self.league.draft()

        self.pause = True
        self.mouse_pos = (0, 0)

        pf = 1
        super().__init__(width, height, pf)

    def process_key_inputs(self, ev: pygame.event.Event):
        if ev.key == pygame.K_SPACE:
            print(f"Pressed space.")

        if ev.key == pygame.K_l:
            # Load
            loadfile = easygui.fileopenbox("Load", "Load a League", filetypes=[".json"])
            load_data = {}
            with open(loadfile, "r") as lf:
                load_data = json.load(lf)

            league = create_league()
            league.deserialize(load_data)
            self.league = league

            if self.debug:
                print(self.league)
                print(f"League loaded.")

        if ev.key == pygame.K_s:
            # Save
            save_data = self.league.serialize()
            savefile = easygui.filesavebox("Save", "Save your League", filetypes=[".json"])
            with open(savefile, "w") as sf:
                json.dump(save_data, sf)

            if self.debug:
                print(self.league)
                print(f"League saved.")

        if ev.key == pygame.K_g:
            self.league.play_round()

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

        if ev.key == pygame.K_ESCAPE:
            self.pause = not self.pause

    def process_mouse_inputs(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Mouse down events
            pass

        if ev.type == pygame.MOUSEBUTTONUP:
            # Mouse up events
            pass

        if ev.type == pygame.MOUSEWHEEL:
            # Mousewheel events
            pass

        if ev.type == pygame.MOUSEMOTION:
            # Mouse motion events
            pass

    def on_start(self):

        if self.debug:
            for team in self.league.teams:
                print(team)
                for member in team.get_roster():
                    print(f"\t- {member}")

            print(f"Undrafted players")
            for player in self.league.available_players:
                print(f"\t- {player}")

        self.debug_font.size = 20

    def on_update(self, et):
        self.clock.tick(24)

        self.mouse_pos = pygame.mouse.get_pos()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_key_inputs(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

            if event.type == pygame.JOYBUTTONDOWN:
                pass

            if event.type == pygame.JOYHATMOTION:
                pass

        self.screen.fill(colors.BLACK)

        # Create a rectangular area for each team

        

        num_cols = 1
        teams_per_col = int(self.league.num_teams / num_cols)
        x_offset, y_offset = 20, 100
        col_width = (self.width - 2 * x_offset) / num_cols

        self.debug_font.render_to(self.screen,
                                  (x_offset, x_offset),
                                  f"{self.league.name} Season {self.league.season} : Round {self.league.round}",
                                  colors.WHITE)

        for i, team in enumerate(self.league.teams):
            col = i // teams_per_col
            color = colors.GREEN if i < self.league.num_playoff_teams else colors.WHITE
            self.debug_font.render_to(self.screen, (x_offset + col_width * col, y_offset + (i % teams_per_col) * self.debug_font.size), str(team), color)

        pygame.draw.circle(self.screen, colors.GREEN, self.mouse_pos, 5, width=1)

        pygame.display.update()


if __name__ == "__main__":
    LeagueEngine(800, 800)
