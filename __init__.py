import bpy
from .ui import *

bl_info = {
    "name": "data_graph",
    "description": "Experimental viewer for ID data-blocks",
    "author": "Lateasusual",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D Viewport",
    "category": "Developer"
}

classes = [
    PT_DataGraphPanel,
    OT_DrawDataGraph
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()