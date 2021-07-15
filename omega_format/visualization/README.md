# Visualizer

What is being rendered is handled by visualization modules (located in `./modules`). The `Visualizer` has an attribute `visualizers`, which is a list of the active visualization modules. You can change that list on initialization or by directly changing the attribute.

To create your own visualization modules you have to subclass `modules.base.VisualizationModule`. Depending on whether you want render something static or something dynamic you have to overload `visualize_static` or `visualize_dymanics`. As a return value a `list` of `PyQt.QtWidgets.QGraphicsItem` is expected.


 