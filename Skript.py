import bpy
import math


def create_rack():
    # -------------------------------------------------
    # Clear existing mesh objects
    # -------------------------------------------------
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # -------------------------------------------------
    # Dimensions
    # -------------------------------------------------
    RACK_WIDTH = 3.0
    RACK_DEPTH = 2.0
    RACK_HEIGHT = 2.5

    POST_SIZE = 0.1
    BEAM_THICKNESS = 0.08

    SHELF_LEVELS = [0.2, 1.2, 2.2]

    # -------------------------------------------------
    # 1. CREATE UPRIGHT POSTS
    # -------------------------------------------------
    corners = [
        (-RACK_WIDTH/2, -RACK_DEPTH/2),
        (-RACK_WIDTH/2,  RACK_DEPTH/2),
        ( RACK_WIDTH/2, -RACK_DEPTH/2),
        ( RACK_WIDTH/2,  RACK_DEPTH/2)
    ]

    for i, (x, y) in enumerate(corners):
        bpy.ops.mesh.primitive_cube_add(size=1)
        post = bpy.context.active_object
        post.name = f"Upright_Post_{i+1}"

        post.scale = (POST_SIZE, POST_SIZE, RACK_HEIGHT)
        post.location = (x, y, RACK_HEIGHT / 2)

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # -------------------------------------------------
    # 2. CREATE BEAMS & FIRST SHELF ONLY
    # -------------------------------------------------
    for level_idx, z_height in enumerate(SHELF_LEVELS):

        # FRONT BEAM (ONLY LEVEL 1)
        if level_idx == 0:
            bpy.ops.mesh.primitive_cube_add(size=1)
            f_beam = bpy.context.active_object
            f_beam.name = "Front_Beam_Level_1"
            f_beam.scale = (
                RACK_WIDTH - POST_SIZE,
                POST_SIZE * 0.6,
                BEAM_THICKNESS
            )
            f_beam.location = (0, -RACK_DEPTH/2, z_height)

            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # BACK BEAM (ALL LEVELS)
        bpy.ops.mesh.primitive_cube_add(size=1)
        b_beam = bpy.context.active_object
        b_beam.name = f"Back_Beam_Level_{level_idx+1}"
        b_beam.scale = (
            RACK_WIDTH - POST_SIZE,
            POST_SIZE * 0.6,
            BEAM_THICKNESS
        )
        b_beam.location = (0, RACK_DEPTH/2, z_height)

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # WIRE DECKING (ONLY LEVEL 1)
        if level_idx == 0:

            bpy.ops.mesh.primitive_plane_add(size=1)
            deck = bpy.context.active_object
            deck.name = "Wire_Decking_1"

            deck.location = (0, 0, z_height + BEAM_THICKNESS / 2)
            deck.scale = (
                RACK_WIDTH - POST_SIZE,
                RACK_DEPTH - POST_SIZE,
                1
            )

            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=12)
            bpy.ops.object.mode_set(mode='OBJECT')

            mod = deck.modifiers.new(
                name="Wireframe",
                type='WIREFRAME'
            )
            mod.thickness = 0.015
            mod.use_replace = True

    # -------------------------------------------------
    # 3. SIDE BRACING
    # -------------------------------------------------
    for x_pos in [-RACK_WIDTH/2, RACK_WIDTH/2]:
        for z_height in [0.5, 1.5, 2.0]:

            bpy.ops.mesh.primitive_cube_add(size=1)
            brace = bpy.context.active_object
            brace.name = f"Side_Brace_{x_pos}_{z_height}"

            brace.scale = (
                POST_SIZE * 0.4,
                RACK_DEPTH - POST_SIZE,
                POST_SIZE * 0.4
            )

            brace.location = (x_pos, 0, z_height)

            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # -------------------------------------------------
    # 4. THREE SIDE WIRE MESH PANELS
    # -------------------------------------------------

    def create_wire_panel(name, location, rotation, scale):

        bpy.ops.mesh.primitive_plane_add(size=1)
        panel = bpy.context.active_object
        panel.name = name

        panel.location = location
        panel.rotation_euler = rotation
        panel.scale = scale

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=20)
        bpy.ops.object.mode_set(mode='OBJECT')

        wire = panel.modifiers.new(
            name="Wireframe",
            type='WIREFRAME'
        )
        wire.thickness = 0.01
        wire.use_replace = True

    # BACK PANEL
    create_wire_panel(
        "Back_Wire_Mesh",
        (0, RACK_DEPTH/2, RACK_HEIGHT/2),
        (math.radians(90), 0, 0),
        (RACK_WIDTH - POST_SIZE, RACK_HEIGHT, 1)
    )

    # LEFT PANEL
    create_wire_panel(
        "Left_Wire_Mesh",
        (-RACK_WIDTH/2, 0, RACK_HEIGHT/2),
        (math.radians(90), 0, math.radians(90)),
        (RACK_DEPTH - POST_SIZE, RACK_HEIGHT, 1)
    )

    # RIGHT PANEL
    create_wire_panel(
        "Right_Wire_Mesh",
        (RACK_WIDTH/2, 0, RACK_HEIGHT/2),
        (math.radians(90), 0, math.radians(90)),
        (RACK_DEPTH - POST_SIZE, RACK_HEIGHT, 1)
    )

    print("Industrial rack generated successfully!")


create_rack()
