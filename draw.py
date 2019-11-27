import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader

draw_offset = [0, 0]

line_buffer = []


def draw_text(
        string,
        screen_pos,
        size=16,
        color=(1.0, 1.0, 1.0, 1.0),
        x_centred=True,
        use_offset=True):

    blf.size(0, size, 72)
    size = blf.dimensions(0, string)

    if x_centred:
        x = screen_pos[0] - size[0] / 2
    else:
        x = screen_pos[0]

    y = screen_pos[1] - size[1] / 2
    if use_offset:
        blf.position(0, x + draw_offset[0], y + draw_offset[1], 0)
    else:
        blf.position(0, x, y, 0)

    blf.color(0, *color)
    blf.draw(0, string)


def draw_line(point1, point2, color=(0.6, 0.6, 0.6, 1), use_offset=True):
    if use_offset:
        w = point2[0] + draw_offset[0]
        h = point2[1] + draw_offset[1]
        x = point1[0] + draw_offset[0]
        y = point1[1] + draw_offset[1]
    else:
        w = point2[0]
        h = point2[1]
        x = point1[0]
        y = point1[1]
    verts = (
        (x, y),
        (w, h)
    )
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": verts})
    shader.bind()
    shader.uniform_float("color", color)

    batch.draw(shader)


def buf_line_clear():
    line_buffer.clear()


def buf_line(p1, p2):
    line_buffer.append(p1)
    line_buffer.append(p2)


def buf_draw_line(color=(0.6, 0.6, 0.6, 1), use_offset=True):
    if use_offset:
        verts = [(point[0] + draw_offset[0], point[1] + draw_offset[1]) for point in line_buffer]
    else:
        verts = line_buffer
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": verts})
    shader.bind()
    shader.uniform_float("color", color)

    batch.draw(shader)


def draw_box(point1, point2, color=(0.4, 0.4, 0.4, 1), use_offset=True):
    if use_offset:
        w = point2[0] + draw_offset[0]
        h = point2[1] + draw_offset[1]
        x = point1[0] + draw_offset[0]
        y = point1[1] + draw_offset[1]
    else:
        w = point2[0]
        h = point2[1]
        x = point1[0]
        y = point1[1]

    verts = (
        (x, y),
        (x, h),
        (w, h),
        (w, y)
    )
    indices = ((0, 1, 2), (0, 2, 3))
    fill_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    background_batch = batch_for_shader(fill_shader, 'TRIS',
                                        {"pos": verts}, indices=indices)
    fill_shader.bind()
    fill_shader.uniform_float("color", color)

    background_batch.draw(fill_shader)


def fill_area(context, color=(0.1, 0.1, 0.1, 1)):
    a = context.area
    draw_box((0, 0), (a.width, a.height), color, use_offset=False)
