import bpy
import bmesh

import numpy as np 
import os

from eden_perlin import PerlinCircle
from sca_brancher import SCACircleBrancher


# get scene
scene = bpy.context.scene

# configure camera position and orientation
bpy.data.objects["Camera"].location = (0, 0, 50)
bpy.data.objects["Camera"].rotation_euler = (0,0,0)

center = np.array([0,0,0])

# eden layer
eden = PerlinCircle(center=center,
                    radius_range=np.array([1,20,2]),
                    shape=np.array([1,1]))

eden_layers = eden.grow()

# sca layers
sca_layers = {}

# sca circle layer 1
scaCL1_radius = 3
scaCL1 = SCACircleBrancher(center=[0,0,0.3],
                          n_sca_trees=10,
                          root_circle_radius=scaCL1_radius,
                          leaves_spread=np.array([3,3,1]),
                          n_leaves=15,
                          branch_thickness_max=0.1,
                          name='scaCL')

scaCL1.initialize_sca_forest(scene)
sca_layers[scaCL1_radius] = scaCL1

# sca circle layer 2
scaCL2_radius = 10
scaCL2 = SCACircleBrancher(center=[0,0,0.3],
                          n_sca_trees=15,
                          root_circle_radius=scaCL2_radius,
                          leaves_spread=np.array([8,8,1]),
                          n_leaves=20,
                          branch_thickness_max=0.2,
                          name='scaCLA')

scaCL2.initialize_sca_forest(scene)
sca_layers[scaCL2_radius] = scaCL2

# sca circle layer 2
scaCL3_radius = 15
scaCL3 = SCACircleBrancher(center=[0,0,0.2],
                          n_sca_trees=25,
                          root_circle_radius=scaCL3_radius,
                          leaves_spread=np.array([15,15,1]),
                          n_leaves=20,
                          branch_thickness_max=0.25,
                          name='scaCLA')

scaCL3.initialize_sca_forest(scene)
sca_layers[scaCL3_radius] = scaCL3

# render
render_out = '/home/lovro/Documents/FER/diplomski/growth_models_results/blender_impl/eden_sca_bmesh/tmp/'
render_iter = 0

eden_layer_idx = 0
eden_render_done = False

sca_layers_done = False

while True:

        render_iter += 1
        
        # add eden layer
        if not eden_render_done:
            eden_layer = eden_layers[eden_layer_idx]
            scene.objects.link(eden_layer[1])  # add mesh

        # add sca layer
        sca_layers_rendered = 0
        for radius, layer in sca_layers.items():
            if radius <= eden_layer[0]: # compare with eden layer radius
                if layer.emerge_sca_volume():
                    sca_layers_rendered += 1

        # render
        bpy.context.scene.render.filepath = os.path.join(render_out, str(render_iter))
        bpy.ops.render.render(write_still=True)

        # check eden 
        eden_layer_idx += 1
        if eden_layer_idx >= len(eden_layers):
            eden_render_done = True

        # check sca
        print(sca_layers_rendered, len(sca_layers))
        if sca_layers_rendered == len(sca_layers):
            
            sca_layers_done = True

        # final check
        if eden_render_done and sca_layers_done:
            break


