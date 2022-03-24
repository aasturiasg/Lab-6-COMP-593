""" 
COMP 593 - Lab 6

Description: 
  Receives the name or number of a pokemon to look up information about it,
  then posts its abilities to PasteBin specifying a title for the paste.

Usage:
  python PokemonPasteBin.py pokemon_name

Parameters:
  pokemon_name = Name or number of the pokemon to be searched on the PokeAPI.

History:
  Date        Author      Description
  2022-03-24  A.Asturias  Initial creation
"""

from sys import argv, exit
import requests

def main():

    print("Welcome to the best PokeScript!")

    #get the command line paramater for the name of the pokemon
    pokemon_name = get_pokemon_name()
    if not pokemon_name:
        exit("Script stopping...")

    #get pokemon information
    pokemon_data = retrieve_pokemon_data(pokemon_name)
    if not pokemon_data:
        exit("Script stopping...")

    #build the strings for the paste to PasteBin
    strings_for_paste = string_builder(pokemon_data)

    #make the paste to PasteBin
    pastebin_link = pastebin_paste(strings_for_paste[0], strings_for_paste[1])

    print(pastebin_link)
    print("Thanks for using the best PokeScript!")

def get_pokemon_name():

    #make sure the user inputed a command line parameter
    if len(argv) < 2:
        print("Command line parameter required, please input at least one pokemon name or number!")
        return None
    else:#obtain and return the parameter
        return argv[1].lower()

def retrieve_pokemon_data(pokemon_name):

    #establish a connection and get all the iformation from a pokemon
    print("Getting Pokemon data from PokeAPI...")
    request_response = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(pokemon_name))

    #verify the request was successful
    if request_response.status_code == 200:
        print("Request successful, data for " + pokemon_name + " gathered.")
        return request_response.json()
    elif request_response.status_code == 404:
        print("Unable to establish connection: " + str(request_response.status_code) + "\nMake sure to input a valid name/number")
        return None
    else:
        print("Unable to establish connection: " + str(request_response.status_code))
        return None

def string_builder(pokemon_data):

    print("Building title and body for paste...")
    #concatenate strings to build the title
    title_for_paste = str(pokemon_data['name']).capitalize() + "'s Abilities"

    #concatenate strings to build the body
    body_for_paste = ""
    #loop through all the abilities of the pokemon
    abilities_count = len(pokemon_data['abilities'])
    for i in range(abilities_count):
        if abilities_count == i + 1:
            body_for_paste += "- " + pokemon_data['abilities'][i]['ability']['name']
        else:
            body_for_paste += "- " + pokemon_data['abilities'][i]['ability']['name'] + "\n"

    return (title_for_paste, body_for_paste)

def pastebin_paste(title_for_paste, body_for_paste):

    #establish a connection and post to PasteBin
    print("Posting to PasteBin...")
    #parameters for the post
    request_parameters = {
    'api_dev_key': "f4R0OTFza_qTQ1NZJYLjoCeLqoHQux4X",
    'api_option': "paste",
    'api_paste_code': body_for_paste,
    'api_paste_name': title_for_paste,
    'api_paste_private': 0
    }
    #make the post request
    request_response = requests.post('https://pastebin.com/api/api_post.php', data=request_parameters)

    #verify the request was successful
    if request_response.status_code == 200:
        print("Paste successful!")
        return "Link to PasteBin paste: " + str(request_response.text)
    else:
        return "Unable to post to PasteBin: " + str(request_response.status_code)

main()