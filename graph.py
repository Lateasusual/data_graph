import bpy
import mathutils.noise
from .draw import *


class Node:
    name = ""
    type = ""
    weight = 0
    x = 0
    y = 0

    def __init__(self):
        self.users = list()


nodes = {}
excluded_types = {
    'Brush',
    'CacheFile',
    'FreestyleLineStyle',
    'PaintCurve',
    'Palette',
    'Screen',
    'WindowManager',
    'WorkSpace',
    'VectorFont',
    'World'
}


def id_type(ID):
    return ID.__class__.__name__


def update_graph():
    nodes.clear()

    data = bpy.data.user_map()
    for i, (ID, users) in enumerate(data.items()):
        if id_type(ID) not in excluded_types:
            n = Node()
            n.y = (mathutils.noise.random() - 0.5) * 1000
            n.x = (mathutils.noise.random() - 0.5) * 1000

            n.name = ID.name
            n.type = id_type(ID)

            if len(users) > 0:
                for other in users:
                    if id_type(other) not in excluded_types:
                        n.users.append(id_type(other) + other.name)
                n.weight = len(n.users)
                nodes[n.type + n.name] = n

    for key, n in nodes.items():
        for u in n.users:
            try:
                nodes[u].weight += 1
            except Exception:
                pass
        print(n.weight)


def draw_graph():
    buf_line_clear()
    for key, node in nodes.items():
        for user in node.users:
            try:
                buf_line((node.x, node.y), (nodes[user].x, nodes[user].y))
            except Exception:
                pass

    buf_draw_line(color=(0.8, 0.0, 0.0, 1))

    for key, node in nodes.items():
        draw_text(node.type, (node.x, node.y - 18), size=12, color=(0.4, 0.4, 0.4, 1))
        draw_text(node.name, (node.x, node.y), size=int(14 * (1 + (node.weight / 15))))
