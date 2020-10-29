from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
    
    context = {'name' : "Rowen"}
    return render(request, 'viewgraph/index.html', context)

def landing_page(request):
    with open('C:/Users/leero/Projects/text-graph/data.json', encoding='utf-8') as data_file:
     
        data = json.loads(data_file.read())
    #print(dataJSON)
    dataJSON = json.dumps(data)
    return render(request,'viewgraph/graph.html', {'data': dataJSON,  'foo' : "hello"})


def second_index(request):
    return HttpResponse("Hello, world. You're at the second index.")

def process_user_input(request):
    user_choices = []
    for i in range(4):
        query = request.GET.get(f'movie{str(i)}')
        if query is not None:
            user_choices.append(int(query))
    
    user_data = compile_json_object(user_choices)
    

    dataJSON = json.dumps(user_data)
    
    return render(request,'viewgraph/graph.html', {'data': dataJSON})
    # return graphs containing only the requested movies 


def compile_json_object(chosen_movie_idx):
    
    movie_idx = []
    chosen_links = []
    chosen_nodes = []
    nodes = data['nodes']
    links = data['links']
        
    for L in links:
        if (L['source_idx'] in chosen_movie_idx) or (L['target_idx'] in chosen_movie_idx):
            chosen_links.append(L)

            if L['source_idx'] not in movie_idx:
                movie_idx.append(L['source_idx'])

            if L['target_idx'] not in movie_idx:
                movie_idx.append(L['target_idx'])

    
    for i in movie_idx:
        chosen_nodes.append(nodes[i])


    userJSON = {"nodes" : chosen_nodes, "links" : chosen_links}

    # print('========================================')
    # print(userJSON)
    # print('=========================================')

    return userJSON


data = {"nodes": [
    {"idx" : 0, "id": "127 Hours", "genre": "biography, drama", "genre_value": 0.06640975177288055, "scaled_genre_value": 180}, 
    {"idx" : 1, "id": "The A-Team", "genre": "action, adventure", "genre_value": 0.015871849842369556, "scaled_genre_value": 0},
    {"idx" : 2, "id": "A Little Help", "genre": "comedy", "genre_value": 0.030338691547513008, "scaled_genre_value": 51}, 
    {"idx" : 3, "id": "Adventures of Power", "genre": "comedy", "genre_value": 0.030338691547513008, "scaled_genre_value": 51}, 
    {"idx" : 4, "id": "Alice in Wonderland", "genre": "family, fantasy", "genre_value": 0.04498301912099123, "scaled_genre_value": 103}
    ], 
"links": [
    {"source_idx": 0, "target_idx": 2, "source": "127 Hours", "target": "A Little Help", "value": 0.41885014157709405}, 
    {"source_idx": 0, "target_idx": 3, "source": "127 Hours", "target": "Adventures of Power", "value": 0.48244755233886155}, 
    {"source_idx": 1, "target_idx": 2, "source": "The A-Team", "target": "A Little Help", "value": 0.44196822822778525}, 
    {"source_idx": 1, "target_idx": 3, "source": "The A-Team", "target": "Adventures of Power", "value": 0.493246618477177}, 
    {"source_idx": 1, "target_idx": 4, "source": "The A-Team", "target": "Alice in Wonderland", "value": 0.4401263842713225}, 
    {"source_idx": 2, "target_idx": 3, "source": "A Little Help", "target": "Adventures of Power", "value": 0.5257436095080503}, 
    {"source_idx": 2, "target_idx": 4, "source": "A Little Help", "target": "Alice in Wonderland", "value": 0.43601514521144}, 
    {"source_idx": 3, "target_idx": 4, "source": "Adventures of Power", "target": "Alice in Wonderland", "value": 0.4389207520427561}
    ]}
