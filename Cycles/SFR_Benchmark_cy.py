import bpy

from ..Utils.SFR_TestRender import TestRender

from bpy.types import Context, Operator
from .. import SFR_Settings
from ..install_deps import dependencies


class SFR_Benchmark_cy(Operator):
    bl_idname = "render.superfastrender_benchmark"
    bl_label = "Frame Benchmark"
    bl_description = "Tests your scene to detect the best optimization settings."

    @classmethod
    def poll(cls, context):
        if not dependencies.checked or dependencies.needs_install:
            dependencies.check_dependencies()

        return not dependencies.needs_install

    def execute(self, context: Context):

        #####################
        ### SET LOW VALUE ###
        #####################

        scene = context.scene
        cycles = scene.cycles
        settings: SFR_Settings = scene.sfr_settings

        # return {'FINISHED'}
        prefs = context.preferences.addons['cycles'].preferences

        for device_type in prefs.get_device_types(context):
            prefs.get_devices_for_type(device_type[0])

        if prefs.get_devices_for_type == 'OPTIX':
            scene.render.tile_x = 512
            scene.render.tile_y = 512
        elif prefs.get_devices_for_type == 'CUDA':
            scene.render.tile_x = 256
            scene.render.tile_y = 256
        elif prefs.get_devices_for_type == 'OPENCL':
            scene.render.tile_x = 256
            scene.render.tile_y = 256
        elif prefs.get_devices_for_type == 'CPU':
            scene.render.tile_x = 32
            scene.render.tile_y = 32

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        scene.render.use_persistent_data = True
        scene.render.use_save_buffers = True

        # set adaptive samples
        cycles.use_adaptive_sampling = True
        cycles.samples = 50000
        cycles.adaptive_threshold = 0.01
        cycles.adaptive_min_samples = 64

        # set max bounces
        cycles.max_bounces = 512
        cycles.diffuse_bounces = 0
        cycles.glossy_bounces = 0
        cycles.transparent_max_bounces = 0
        cycles.transmission_bounces = 0
        cycles.volume_bounces = 0
        cycles.light_sampling_threshold = 0.01
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 10
        cycles.caustics_reflective = False
        cycles.caustics_refractive = False
        cycles.blur_glossy = 10
        cycles.volume_step_rate = 5
        cycles.volume_preview_step_rate = 5
        cycles.volume_max_steps = 256

        # simplfy the scene
        scene.render.use_simplify = True
        # viewport
        scene.render.simplify_subdivision = 2
        scene.render.simplify_child_particles = 0.2
        cycles.texture_limit = '2048'
        cycles.ao_bounces = 2
        # render
        scene.render.simplify_subdivision_render = 4
        scene.render.simplify_child_particles_render = 1
        cycles.texture_limit_render = '4096'
        cycles.ao_bounces_render = 4
        # culling
        cycles.use_camera_cull = True
        cycles.use_distance_cull = True
        cycles.camera_cull_margin = 0.1
        cycles.distance_cull_margin = 50

        ##################
        ### INITIALIZE ###
        ##################

        ### old settings ###
        oldCompositing = scene.render.use_compositing
        oldSequencer = scene.render.use_sequencer
        oldResX = scene.render.resolution_x
        oldResY = scene.render.resolution_y
        oldPercent = scene.render.resolution_percentage

        scene.render.use_compositing = False
        scene.render.use_sequencer = False

        ### set settings ###
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'

        path = settings.inputdir

        iteration = 0
        repeat = True

        ### DIFFUSE ###
        while repeat and settings.use_diffuse:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            print("Diffuse Bounces Pre: ", cycles.diffuse_bounces)
            cycles.diffuse_bounces += 1
            # set next
            iteration += 1
            print("Diffuse Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
            print("Diffuse Bounces Post: ", cycles.diffuse_bounces)
        cycles.diffuse_bounces -= 1
        print("Diffuse Bounces Final: ", cycles.diffuse_bounces)

        iteration = 0
        repeat = True

        ### GLOSS1 ###
        while repeat and settings.use_glossy:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.glossy_bounces += 1
            # set next
            iteration += 1
            print("Glossy Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.glossy_bounces -= 1

        iteration = 0
        repeat = True

        ### TRANSMISSION1 ###
        while repeat and settings.use_transmission:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.transmission_bounces += 1
            # set next
            iteration += 1
            print("Transmission Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.transmission_bounces -= 1

        iteration = 0
        repeat = True

        ### GLOSS2 ###
        while repeat and settings.use_glossy:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.glossy_bounces += 1
            # set next
            iteration += 1
            print("Glossy2 Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.glossy_bounces -= 1

        iteration = 0
        repeat = True

        ### TRANSMISSION2 ###
        while repeat and settings.use_transmission:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.transmission_bounces += 1
            # set next
            iteration += 1
            print("Transmission2 Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.transmission_bounces -= 1

        iteration = 0
        repeat = True

        ### TRANSPARENT ###
        while repeat and settings.use_transparent:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.transparent_max_bounces += 1
            # set next
            iteration += 1
            print("Transparent Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.transparent_max_bounces -= 1

        iteration = 0
        repeat = True

        ### VOLUME ###
        while repeat and settings.use_volume:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.volume_bounces += 1
            # set next
            iteration += 1
            print("Volume Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.volume_bounces -= 1

        iteration = 0
        repeat = True

        ### INDIRECT ###
        while repeat and settings.use_indirect:
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.sample_clamp_indirect += 1
            # set next
            iteration += 1
            print("Indirect Clamp Iteration: ", iteration)
            # start second render
            repeat = TestRender(path, iteration, settings)
        cycles.sample_clamp_indirect -= 1

        iteration = 0
        repeat = True

        ### CAUSTIC BLUR ###
        if settings.use_caustics:
            while repeat:
                # start first render
                TestRender(path, iteration, settings)
                # set settings
                cycles.blur_glossy += 1
                # set next
                iteration += 1
                print("Caustic Blur Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.blur_glossy -= 1

            iteration = 0
            repeat = True

            ### CAUSTIC REFL ###
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.caustics_reflective = True
            # start second render
            cycles.caustics_reflective = TestRender(path, iteration, settings)

            iteration = 0
            repeat = True

            ### CAUSTIC REFR ###
            # start first render
            TestRender(path, iteration, settings)
            # set settings
            cycles.caustics_refractive = True
            # start second render
            cycles.caustics_refractive = TestRender(path, iteration, settings)

            iteration = 0
            repeat = True

        ### get old settings ###
        scene.render.use_compositing = oldCompositing
        scene.render.use_sequencer = oldSequencer
        scene.render.resolution_x = oldResX
        scene.render.resolution_y = oldResY
        scene.render.resolution_percentage = oldPercent

        ### TOTAL ###
        cycles.max_bounces = cycles.diffuse_bounces + cycles.glossy_bounces + cycles.transmission_bounces + cycles.volume_bounces

        self.report({'INFO'}, "Benchmark complete")

        return {'FINISHED'}
