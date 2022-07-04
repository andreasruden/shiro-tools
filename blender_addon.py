bl_info = {
    'name': 'Shiro Tools',
    'author': 'Shiro',
    'blender': (2, 80, 0)
}

import bpy

class ToggleWeightPaintingAndPosing(bpy.types.Operator):
    bl_idname = 'shiro_tools.toggle_weight_painting_and_posing'
    bl_label = 'Switch between Weight Painting and Pose Mode'
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        if bpy.context.mode == 'PAINT_WEIGHT':
            # Switch to Pose mode for armature
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='POSE')
                    break
            # Update shown layers
            layer_list = [False] * 32
            layer_list[1] = True
            bpy.ops.armature.armature_layers(layers=layer_list)
        elif bpy.context.mode == 'POSE':
            # Switch to Weight Paint mode
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    print('selected armature!')
                    mesh_obj = recursive_object_search(
                        lambda o: obj in [m.object for m in o.modifiers if m.type == 'ARMATURE'])
                    obj.select_set(True)
                    mesh_obj.select_set(True)
                    bpy.context.view_layer.objects.active = mesh_obj
                    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
                    break
            # Update shown layers
            layer_list = [False] * 32
            layer_list[0] = True
            bpy.ops.armature.armature_layers(layers=layer_list)
        return {'FINISHED'}

def recursive_object_search(condition, container=None):
    if container == None:
        container = bpy.context.view_layer.objects # Cannot appear in the declaration becasue blender will restrict it
    for obj in container:
        if condition(obj):
            return obj
        in_children = recursive_object_search(condition, obj.children)
        if in_children != None:
            return in_children
    return None

# Registration

addon_keymaps = []

def register():
    bpy.utils.register_class(ToggleWeightPaintingAndPosing)
    # Keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY', region_type='WINDOW')
    kmi = km.keymap_items.new(ToggleWeightPaintingAndPosing.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(ToggleWeightPaintingAndPosing)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == '__main__':
    register()
