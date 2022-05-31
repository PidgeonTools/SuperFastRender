import bpy
import itertools as it

from bpy.types import Context, Operator

from .. import SFR_Settings
from ..Utils.SFR_TestRender import TestRender
from ..install_deps import dependencies
from ..Utils.fib import fib


class SFR_Benchmark_cy(Operator):
    bl_idname = "render.superfastrender_benchmark"
    bl_label = "Frame Benchmark"
    bl_description = "Tests your scene to detect the best optimization settings."

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        layout = self.layout
        layout.label(text = "Benchmarking your scene can take a while.")
        layout.label(text = "We recommend you open the System Console, if you are on Windows.")
        layout.label(text = 'To do so, go to your top bar "Window" -> "Toggle System Console"')
        layout.label(text = "There you will be able to see the progress.")
        layout.separator()
        layout.label(text = "Blender will appear to freeze, please be patient.")
        layout.separator()
        layout.label(text = "To proceed with the benchmark, press [OK]")

    insert_keyframes: bpy.props.BoolProperty(
        name="Insert keyframes",
        description="Inserts keyframes for each property to the current frame (used for benchmarking animations)",
        default=False,
        options=set(),  # Not animatable!
    )

    @classmethod
    def poll(cls, context: Context):
        if not dependencies.checked or dependencies.needs_install:
            dependencies.check_dependencies()

        return context.scene.render.engine == 'CYCLES' and not dependencies.needs_install

    def execute(self, context: Context):

        #####################
        ### SET LOW VALUE ###
        #####################

        scene = context.scene
        cycles = scene.cycles
        settings: SFR_Settings = scene.sfr_settings
        keyframe_insert = scene.keyframe_insert

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        scene.render.use_persistent_data = True

        # set adaptive samples
        cycles.use_adaptive_sampling = True
        cycles.samples = 50000
        if bpy.app.version < (3, 0, 0):
            cycles.adaptive_threshold = 0.01
        else:
            # Adaptive sampling has been tweaked in 3.0
            cycles.adaptive_threshold = 0.04
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

        if self.insert_keyframes:
            keyframe_insert('cycles.max_bounces')
            if settings.use_diffuse:
                keyframe_insert('cycles.diffuse_bounces')
            if settings.use_glossy:
                keyframe_insert('cycles.glossy_bounces')
            if settings.use_transmission:
                keyframe_insert('cycles.transmission_bounces')
            if settings.use_transparent:
                keyframe_insert('cycles.transparent_max_bounces')
            if settings.use_volume:
                keyframe_insert('cycles.volume_bounces')
            if settings.use_indirect:
                keyframe_insert('cycles.sample_clamp_indirect')
            if settings.use_caustics:
                keyframe_insert('cycles.blur_glossy')
                keyframe_insert('cycles.caustics_reflective')
                keyframe_insert('cycles.caustics_refractive')

        # simplify the scene
        old_use_simplify = scene.render.use_simplify
        scene.render.use_simplify = True
        # viewport
        old_simplify_subdivision = scene.render.simplify_subdivision
        old_simplify_child_particles = scene.render.simplify_child_particles
        old_texture_limit = cycles.texture_limit
        old_ao_bounces = cycles.ao_bounces
        scene.render.simplify_subdivision = 2
        scene.render.simplify_child_particles = 0.2
        cycles.texture_limit = '256'
        cycles.ao_bounces = 2
        # render
        old_simplify_subdivision_render = scene.render.simplify_subdivision_render
        old_simplify_child_particles_render = scene.render.simplify_child_particles_render
        old_texture_limit_render = cycles.texture_limit_render
        old_ao_bounces_render = cycles.ao_bounces_render
        scene.render.simplify_subdivision_render = 4
        scene.render.simplify_child_particles_render = 1
        cycles.texture_limit_render = '128'
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

        ### TRANSPARENT ###
        if settings.use_transparent:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.transparent_max_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.transparent_max_bounces')
                # set next
                iteration += 1
                print("Transparent Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.transparent_max_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.transparent_max_bounces')

        ### DIFFUSE ###
        if settings.use_diffuse:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                print("Diffuse Bounces Pre: ", cycles.diffuse_bounces)
                cycles.diffuse_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.diffuse_bounces')
                # set next
                iteration += 1
                print("Diffuse Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
                print("Diffuse Bounces Post: ", cycles.diffuse_bounces)
            cycles.diffuse_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.diffuse_bounces')
            print("Diffuse Bounces Final: ", cycles.diffuse_bounces)

        ### GLOSS1 ###
        if settings.use_glossy:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.glossy_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.glossy_bounces')
                # set next
                iteration += 1
                print("Glossy Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.glossy_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.glossy_bounces')

        ### TRANSMISSION1 ###
        if settings.use_transmission:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.transmission_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.transmission_bounces')
                # set next
                iteration += 1
                print("Transmission Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.transmission_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.transmission_bounces')

        ### GLOSS2 ###
        if settings.use_transmission and settings.use_glossy:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.glossy_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.glossy_bounces')
                # set next
                iteration += 1
                print("Glossy2 Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.glossy_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.glossy_bounces')

        ### TRANSMISSION2 ###
        if settings.use_transmission and settings.use_glossy:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.transmission_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.transmission_bounces')
                # set next
                iteration += 1
                print("Transmission2 Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.transmission_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.transmission_bounces')

        ### VOLUME ###
        if settings.use_volume:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.volume_bounces += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.volume_bounces')
                # set next
                iteration += 1
                print("Volume Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.volume_bounces -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.volume_bounces')

        ### INDIRECT ###
        if settings.use_indirect:
            # start first render
            iteration = 0
            repeat = True
            TestRender(path, iteration, settings)
            for x in it.takewhile(lambda _: repeat, fib()):
                # save best value found so far before rendering next iteration
                best_val_found = cycles.sample_clamp_indirect
                # set settings
                cycles.sample_clamp_indirect += x
                print(f"Indirect Clamp increment {x} to {cycles.sample_clamp_indirect}")
                if self.insert_keyframes:
                    keyframe_insert('cycles.sample_clamp_indirect')
                # set next
                iteration += 1
                print("Indirect Clamp Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            print(f"Best value found: {best_val_found}")
            cycles.sample_clamp_indirect = best_val_found
            if self.insert_keyframes:
                keyframe_insert('cycles.sample_clamp_indirect')

        ### CAUSTIC BLUR ###
        if settings.use_caustics:
            # start first render
            iteration = 0
            repeat = TestRender(path, iteration, settings)
            while repeat:
                # set settings
                cycles.blur_glossy += 1
                if self.insert_keyframes:
                    keyframe_insert('cycles.blur_glossy')
                # set next
                iteration += 1
                print("Caustic Blur Iteration: ", iteration)
                # start second render
                repeat = TestRender(path, iteration, settings)
            cycles.blur_glossy -= 1
            if self.insert_keyframes:
                keyframe_insert('cycles.blur_glossy')

            ### CAUSTIC REFL ###
            # start first render
            iteration = 0
            TestRender(path, iteration, settings)
            # set settings
            cycles.caustics_reflective = True
            if self.insert_keyframes:
                keyframe_insert('cycles.caustics_reflective')
            # set next
            iteration += 1
            print("Caustics Reflective Iteration: ", iteration)
            # start second render
            cycles.caustics_reflective = TestRender(path, iteration, settings)
            if self.insert_keyframes:
                keyframe_insert('cycles.caustics_reflective')

            ### CAUSTIC REFR ###
            # start first render
            iteration = 0
            TestRender(path, iteration, settings)
            # set settings
            cycles.caustics_refractive = True
            if self.insert_keyframes:
                keyframe_insert('cycles.caustics_refractive')
            # set next
            iteration += 1
            print("Caustics Refractive Iteration: ", iteration)
            # start second render
            cycles.caustics_refractive = TestRender(path, iteration, settings)
            if self.insert_keyframes:
                keyframe_insert('cycles.caustics_refractive')

        ### get old settings ###
        scene.render.use_simplify = old_use_simplify
        scene.render.simplify_subdivision = old_simplify_subdivision
        scene.render.simplify_subdivision_render = old_simplify_subdivision_render
        scene.render.simplify_child_particles = old_simplify_child_particles
        scene.render.simplify_child_particles_render = old_simplify_child_particles_render
        cycles.texture_limit = old_texture_limit
        cycles.texture_limit_render = old_texture_limit_render
        cycles.ao_bounces = old_ao_bounces
        cycles.ao_bounces_render = old_ao_bounces_render
        scene.render.use_compositing = oldCompositing
        scene.render.use_sequencer = oldSequencer
        scene.render.resolution_x = oldResX
        scene.render.resolution_y = oldResY
        scene.render.resolution_percentage = oldPercent

        ### TOTAL ###
        cycles.max_bounces = cycles.diffuse_bounces + cycles.glossy_bounces + cycles.transmission_bounces + cycles.volume_bounces
        if self.insert_keyframes:
            keyframe_insert('cycles.max_bounces')

        self.report({'INFO'}, "Benchmark complete")

        return {'FINISHED'}
