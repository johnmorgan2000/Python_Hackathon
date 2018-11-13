from pybcca.tui_helper import run
from core import *
import os


def check_space_action(state, direction):
    if state.player_check_space(direction) == 'enemy':
        state.state = "battle"
        return state


def on_enemy_space_action(state):
    enemies = state.player.room.enemies
    enemy = state.player_check_for_enemy(enemies)
    if enemy is not None:
        state.state = 'battle'
        state.enemy = enemy
    return state


def explore_update(key, state: Game) -> Game:
    if key == "KEY_UP":
        state.clear_player_spot()
        # check_space_action(state, 'north')
        state.move_player_north()
        state.player_new_spot()
        on_enemy_space_action(state)

        return state
    elif key == "KEY_DOWN":
        state.clear_player_spot()
        # check_space_action(state, 'south')
        state.move_player_south()
        state.player_new_spot()
        on_enemy_space_action(state)
        return state
    elif key == "KEY_LEFT":
        state.clear_player_spot()
        # check_space_action(state, 'west')
        state.move_player_west()
        state.player_new_spot()
        on_enemy_space_action(state)
        return state
    elif key == "KEY_RIGHT":
        state.clear_player_spot()
        # check_space_action(state, 'east')
        state.move_player_east()
        on_enemy_space_action(state)
        state.player_new_spot()

        return state
    else:
        return state
    return state


def battle_update(key, state: Game) -> Game:
    if key == "1":
        attack(state.player, state.enemy)

    elif key == "2":
        cast_spell(state.player, state.enemy)

    if state.enemy.is_dead():
        state.state = 'explore'
    return state


def update(key, state: Game) -> Game:
    if state.state == "explore":
        state = explore_update(key, state)
    elif state.state == "battle":
        state = battle_update(key, state)

    return state


def explore_view(state, x, y):
    string = f'Use the Arrow keys to move\nPlayer: {state.player.name}\n\n\t'
    for row in state.player.room.build:
        for cell in row:
            if cell == 0:
                string += "   "
            elif cell == 1:
                string += " P "
            elif cell == 2:
                string += "|W|"
            elif cell == 3:
                string += " E "
            elif cell == 4:
                string += " X "
        string += "\n\t"
    return string


def battle_view(state, x, y):
    player = state.player
    enemy = state.enemy
    space = ""

    string = ''

    str_names = '\t|| {:6} || {:<10} || {} ||'.format(player.name, space,
                                                      enemy.name)
    str_health = '\n\tHealth: {:<3}{:<13}Health: {:<3}'.format(
        player.health, space, enemy.health)
    str_magic = '\n\tMagic Core: {:<3}{:<9}Magic Core: {:<3}'.format(
        player.magic, space, enemy.magic)
    str_weapons = '\n\tWeapon: {:<13}{:<3}Weapon: {:<13}'.format(
        player.weapon['name'], space, enemy.weapon['name'])
    str_spell = '\n\tSpell: {:<13}{:<4}Spell: {:<13}'.format(
        player.spell, space, enemy.spell)
    str_armor = '\n\tArmor: {:<13}{:<4}Armor: {:<13}'.format(
        player.armor['name'], space, enemy.armor['name'])

    return string + str_names + str_health + str_magic + str_weapons + str_spell + str_armor


def view(state, x, y):
    if state.state == "explore":
        string = explore_view(state, x, y)
    elif state.state == "battle":
        string = battle_view(state, x, y)
    return string


def player_name():

    name = input("What is your name: ")
    if len(name) == 0:
        player_name()

    else:
        return name


def main():
    os.system('clear')
    _map = load_map()
    name = player_name()
    player = Player(100, name, 100, {'x': 2, 'y': 1}, _map[0])
    player.weapon = get_weapon('none')
    player.armor = get_armor('none')

    run(Game(player, _map, "explore"), update, view)


if __name__ == "__main__":
    main()
