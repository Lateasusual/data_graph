import bpy
from .draw import *
from .graph import *


class PT_DataGraphPanel(bpy.types.Panel):
    """ Test """
    bl_label = "DataGraph"
    bl_idname = "PT_DataGraphPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Misc"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.draw_data_graph")


class OT_DrawDataGraph(bpy.types.Operator):
    """ Test """
    bl_idname = "wm.draw_data_graph"
    bl_label = "Draw Data Graph"

    def __init__(self):
        self.draw_handle = None
        self.is_moving = False
        self.move_start = [0, 0]
        self.view_transform = [0, 0]
        self.middle_mouse = False

    def invoke(self, context, event):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (self, context), 'WINDOW',
                                                                  'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        update_graph()
        self.view_transform[0] = context.area.width / 2
        self.view_transform[1] = context.area.height / 2
        context.area.tag_redraw()
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "MIDDLEMOUSE":
            if event.value == 'PRESS':
                self.middle_mouse = True
            if event.value == 'RELEASE':
                self.middle_mouse = False

        if event.type == "MOUSEMOVE" and self.middle_mouse:
            x = context.area.width - event.mouse_region_x
            y = context.area.height - event.mouse_region_y
            if not self.is_moving:
                self.is_moving = True
                self.move_start = [x + self.view_transform[0], y + self.view_transform[1]]
            else:
                self.view_transform = [self.move_start[0] - x, self.move_start[1] - y]
            context.area.tag_redraw()
        else:
            self.is_moving = False

        if event.type in {'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
            context.area.tag_redraw()
            return {'FINISHED'}

        return {'INTERFACE'}

    def draw_callback(self, op, context):
        fill_area(context)
        draw_offset[0] = self.view_transform[0]
        draw_offset[1] = self.view_transform[1]
        draw_text("Press ESC to exit", (20, 20), x_centred=False, use_offset=False)
        draw_graph()
