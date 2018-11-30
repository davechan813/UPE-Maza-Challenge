from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import requests
import queue

url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com'
UID  = '804783490'

def go(token, dire):
    request = Request(url + '/game?token=' + token, urlencode({"action": dire}).encode())
    data = json.load(urlopen(request))
    # print(data)
    return data["result"]

def dfs(token, m, n, i, j, dire, visited):
    # print("try to go:", dire, "to", i, j)
    if i < 0 or i >= m or j < 0 or j >= n or visited[i][j]:
        return False
    
    result = go(token, dire)
    if result == "END":
        print("END")
        return True
    if result == "WALL" or result == "OUT_OF_BOUNDS":
        return False

    # print("\nvisited", i, j)
    visited[i][j] = True
    if dfs(token, m, n, i+1, j, "DOWN", visited):
        return True
    if dfs(token, m, n, i, j+1, "RIGHT", visited):
        return True
    if dfs(token, m, n, i-1, j, "UP", visited):
        return True
    if dfs(token, m, n, i, j-1, "LEFT", visited):
        return True

    visited[i][j] = False
    if dire == 'DOWN':
        go(token, 'UP')
    if dire == 'UP':
        go(token, 'DOWN')
    if dire == 'LEFT':
        go(token, 'RIGHT')
    if dire == 'RIGHT':
        go(token, 'LEFT')

    return False

def dfs_wrap(token, m, n, i, j, visited):
    if dfs(token, m, n, i+1, j, "DOWN", visited): return
    if dfs(token, m, n, i, j+1, "RIGHT", visited): return
    if dfs(token, m, n, i-1, j, "UP", visited): return
    if dfs(token, m, n, i, j-1, "LEFT", visited): return

def play():
    while True:
        fields = {'uid': UID}
        request = Request(url + '/session', urlencode(fields).encode())
        data = json.load(urlopen(request))
        token = data['token']
        
        contents = json.load(urlopen(url + '/game?token=' + token))

        m, n = contents["maze_size"][::-1]
        i, j = contents["current_location"][::-1]
        status = contents["status"]
        levels_completed = contents["levels_completed"]
        total_levels = contents["total_levels"]
        print(contents)

        visited = [[False for a in range(n)] for b in range(m)]
        # print("\nvisited", i, j)
        visited[i][j] = True
        dfs_wrap(token, m, n, i, j, visited)
        if levels_completed == total_levels-1:
            break


if __name__== "__main__":
  play()
