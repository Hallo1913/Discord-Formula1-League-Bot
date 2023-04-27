# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import numpy as np
import pandas as pd
import os
import discord as dc
from discord.ext import commands

# Global vars

TOKEN = os.getenv('DISCORD_TOKEN')

points_race = {'1': 25, '2': 21, '3': 18, '4': 15, '5': 12, '6': 10, '7': 8, '8': 6, '9': 4, '10': 3, '11': 2, '12': 1}
points_sprint = {'1': 10, '2': 9, '3': 8, '4': 7, '5': 6, '6': 5, '7': 4, '8': 3, '9': 2, '10': 1}
Teams = {1: 'Mercedes', 2: 'Red Bull', 3: 'Ferrari', 4: 'Alpine', 5: 'McLaren',
         6: 'Aston Martin', 7: 'Alfa Romeo', 8: 'Alpha Tauri', 9: 'Williams', 10: 'Haas'}

path = f'{os.getcwd()}\SKL_League\SKL_LeagueStandings.csv'
# Bot settings

bot = commands.Bot(command_prefix='!')


# Util Functions
# TODO Discord Integration    ?! half Done
# TODO use Table2ascii module for Print


def __get_driver_index(Standings: pd.DataFrame, changed_driver):
    index = Standings.index[Standings['Driver Name'] == changed_driver].values[0]
    return index


def __remove_unnamed(__standings: pd.DataFrame):
    if 'Unnamed: 0' in __standings:
        __standings.drop('Unnamed: 0', axis=1, inplace=True)
    else:
        pass
    return __standings


def __get_player_sum(Standings):
    total_points = []
    for i in range(20):
        total_points.append(Standings.loc[i][3:].sum())
    Standings['Total'] = total_points
    return __remove_unnamed(Standings)


def __change_driver_results(Standings: pd.DataFrame, corr_Track: str, changed_driver: str, new_result, points: dict):
    wanted_driver = __get_driver_index(Standings, changed_driver)
    Standings.loc[int(wanted_driver), corr_Track] = points[
        new_result]  # expects Full list of Race-result
    Standings = __remove_unnamed(Standings)
    return Standings


@bot.command(name='Load_Standings', help='')
async def Load_Standings(ctx, path: str):
    try:
        old_Standings = pd.read_csv(path)  # load saved league standings csv
    except:
        __data = {'Driver Name': [], 'Team': []}
        old_Standings = pd.DataFrame(data=__data)
    await ctx.send('Loading Complete')
    return old_Standings


@bot.command(name='add_driver', help='')
async def add_driver(ctx, Drivers: pd.DataFrame, new_Driver: list, team_key: list):
    Driver_Lineup = Drivers
    for i in range(len(new_Driver)):
        new_Entry = {'Driver Name': [new_Driver[i]], 'Team': Teams[team_key[i]]}
        df2 = pd.DataFrame(data=new_Entry)
        Driver_Lineup = Driver_Lineup.append(df2, ignore_index=True)
    await ctx.send(f'added Driver/s to ther respective Team/s\n{Driver_Lineup}')
    return Driver_Lineup


@bot.command(name='add_race', help='')
async def add_race(ctx, Standings, points_table: dict, Race: str, participants: list, result: list):
    Standings = __remove_unnamed(Standings)
    Standings[Race] = 0
    for i in range(len(participants)):
        __change_driver_results(Standings, Race, participants[i], result[i], points_table)
    Standings.fillna(0, inplace=True)  # will add 0 to drivers that will join after a certain Race
    Standings = __get_player_sum(Standings)
    await ctx.send(f'added Race_Result to Standings\n{Standings}')
    return Standings


@bot.command(name='change_result', help='')
async def change_result(ctx, Standings: pd.DataFrame, corr_Track: str, changed_driver: str, new_result, points: dict):
    Standings = __change_driver_results(Standings, corr_Track, changed_driver, new_result, points)
    await ctx.send('changes results to given Parameters')
    return Standings


@bot.command(name='display_team_standings', help='')
async def display_team_standings(ctx, Standings: pd.DataFrame):
    team_points = Standings[['Team', 'Total']].groupby('Team').sum()
    await ctx.send({team_points})
    return team_points


@bot.command(name='save_standings_to_csv', help='')
async def save_standings_to_csv(ctx, Standings: pd.DataFrame, league_name: str, mkdir: bool):
    current_dir = os.getcwd()
    path = os.path.join(current_dir, league_name)
    if not mkdir:  # will create a folder named after the league
        pass
    else:
        os.mkdir(path)
    Standings.to_csv(f'{path}\{league_name}Standings.csv')
    await ctx.send(f'Saving Complete, lookup{league_name}Standings.csv')


'''
@bot.command(name='add_race', help='')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
'''


def Connect_MSG():
    client = dc.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    client.run(TOKEN)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Main Call
if __name__ == '__main__':
    Driver_Lineup = Load_Standings(path)  # -> load of local copy
    Standings = Driver_Lineup
    # Driver_Lineup = add_driver(Driver_Lineup, ['Hallo', 'Zimmi', 'EDK', 'Malte', 'Robin', 'Schmiddi', 'Timo', 'Tino',
    #                                           'Mullenbesen', 'Advatange', 'Navaz', 'Ayfl', 'Sash', 'Anubis', 'Henry',
    #                                          'Leon', 'Knoot', 'Boski', 'KMAG', 'Pander'],
    #                                          [7, 8, 6, 2, 8, 7, 5, 1, 1, 9, 4, 3, 9, 10, 2, 8, 5, 4, 3, 6])  # -> init of Driver Field
    # Standings = add_race(Standings=Driver_Lineup, points_table=points_race, Race='Monza',
    #                     participants=['Zimmi', 'Sash', 'Malte', 'Ayfl', 'Henry'],
    #                     result=['1', '5', '8', '3', '2'])  # ->  Add Race-result (only 1-12 required) other will get 0 pts. auto.
    # Standings = __change_driver_results(Driver_Lineup, 'Portimao', 'Malte', '5')
    Standings = __get_player_sum(Standings)
    team_standings = display_team_standings(Standings)
    print(Standings)  # Debugging print in Console
    print(team_standings)
    save_standings_to_csv(Standings, league_name='SKL_League', mkdir=False)  # -> local copy of Champ.Standings
