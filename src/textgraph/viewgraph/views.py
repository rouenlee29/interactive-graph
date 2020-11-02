from django.shortcuts import render
from django.http import HttpResponse
import json

all_movies_json_path = 'C:/Users/leero/Projects/text-graph/data-v0.1.json'

def index(request):
    context = {'name' : "Rowen"}
    return render(request, 'viewgraph/index.html', context)

def load_all_movies_in_str(all_movies_json_path):
    with open(all_movies_json_path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    data_json = json.dumps(data)
    
    return data_json

def landing_page(request):
    data_json = load_all_movies_in_str(all_movies_json_path)
    
    return render_graphs(request, data_json, True)

def render_graphs(request, data_json, landing_page_mode):

    return render(request,'viewgraph/graph.html', {'data' : data_json, 'landing_page_mode' : landing_page_mode})

def second_index(request):
    return HttpResponse("Hello, world. You're at the second index.")

def process_user_input(request):
    """
    return graphs containing only the requested movies 
    """
    # print("===================================================================")
    # print(dict(request.GET))
    # print("===================================================================")
    
    selection = dict(request.GET)
    user_choices = [int(selection[s][0]) for s in selection]
    
    if 9999 in user_choices:
        # load all movies 
        data_json = load_all_movies_in_str(all_movies_json_path)
    else:
        user_data = compile_json_object(user_choices)
        data_json = json.dumps(user_data)
    
    return render_graphs(request, data_json, False)

def compile_json_object(chosen_movie_idx):
    with open(all_movies_json_path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    
    chosen_links = []
    chosen_nodes = []
    nodes = data['nodes']
    links = data['links']
    graph_movie_idx = []

    for L in links:
        if (L['source_idx'] in chosen_movie_idx) or (L['target_idx'] in chosen_movie_idx):
            chosen_links.append(L)

            if L['source_idx'] not in graph_movie_idx:
                graph_movie_idx.append(L['source_idx'])

            if L['target_idx'] not in graph_movie_idx:
                graph_movie_idx.append(L['target_idx'])

    for n in nodes:
        if n['idx'] in graph_movie_idx:
            chosen_nodes.append(n)

    userJSON = {"nodes" : chosen_nodes, "links" : chosen_links}

    print('========================================')
    print(userJSON)
    print('=========================================')

    return userJSON


# data = {"nodes": [
#     {"idx" : 0, "id": "127 Hours", "genre": "biography, drama", "genre_value": 0.06640975177288055, "scaled_genre_value": 180}, 
#     {"idx" : 1, "id": "The A-Team", "genre": "action, adventure", "genre_value": 0.015871849842369556, "scaled_genre_value": 0},
#     {"idx" : 2, "id": "A Little Help", "genre": "comedy", "genre_value": 0.030338691547513008, "scaled_genre_value": 51}, 
#     {"idx" : 3, "id": "Adventures of Power", "genre": "comedy", "genre_value": 0.030338691547513008, "scaled_genre_value": 51}, 
#     {"idx" : 4, "id": "Alice in Wonderland", "genre": "family, fantasy", "genre_value": 0.04498301912099123, "scaled_genre_value": 103}
#     ], 
# "links": [
#     {"source_idx": 0, "target_idx": 2, "source": "127 Hours", "target": "A Little Help", "value": 0.41885014157709405}, 
#     {"source_idx": 0, "target_idx": 3, "source": "127 Hours", "target": "Adventures of Power", "value": 0.48244755233886155}, 
#     {"source_idx": 1, "target_idx": 2, "source": "The A-Team", "target": "A Little Help", "value": 0.44196822822778525}, 
#     {"source_idx": 1, "target_idx": 3, "source": "The A-Team", "target": "Adventures of Power", "value": 0.493246618477177}, 
#     {"source_idx": 1, "target_idx": 4, "source": "The A-Team", "target": "Alice in Wonderland", "value": 0.4401263842713225}, 
#     {"source_idx": 2, "target_idx": 3, "source": "A Little Help", "target": "Adventures of Power", "value": 0.5257436095080503}, 
#     {"source_idx": 2, "target_idx": 4, "source": "A Little Help", "target": "Alice in Wonderland", "value": 0.43601514521144}, 
#     {"source_idx": 3, "target_idx": 4, "source": "Adventures of Power", "target": "Alice in Wonderland", "value": 0.4389207520427561}
#     ]}
