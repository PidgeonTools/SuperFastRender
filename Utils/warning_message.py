def draw_warning(self, context):
    layout = self.layout
    layout.label(text = "This action can take a while.")
    layout.label(text = "We recommend you open the System Console, if you are on Windows.")
    layout.label(text = 'To do so, go to your top bar "Window" -> "Toggle System Console"')
    layout.label(text = "There you will be able to see the progress.")
    layout.separator()
    layout.label(text = "Blender will appear to freeze, please be patient.")
    layout.separator()
    layout.label(text = "To proceed, press [OK]")
