import vtkmodules.all as vtk


class VtkVisualizeBase:
    def __init__(self):
        self._file_reader = None
        self._geom_actor_prop = vtk.vtkProperty()
        self._geom_actor_prop.SetColor((0.91, 0.87, 0.67))
        self._geom_actor_prop.SetOpacity(0.3)
        self._geom_actor_prop.SetDiffuse(0)
        self._geom_actor_prop.SetAmbient(1)
        self._geom_actor_prop.SetLineWidth(1)
        self._mesh_actor_prop = vtk.vtkProperty()
        self._mesh_actor_prop.SetColor((0, 0, 0))
        self._mesh_actor_prop.SetOpacity(1)
        self._mesh_actor_prop.SetDiffuse(0)
        self._mesh_actor_prop.SetAmbient(1)
        self._mesh_actor_prop.SetLineWidth(1)


class VtkVisualize(VtkVisualizeBase):
    def __init__(self):
        VtkVisualizeBase.__init__(self)

    def read_file(self, filename):
        self._file_reader = vtk.vtkUnstructuredGridReader()
        self._file_reader.SetFileName(filename)
        # For contour use.
        self._file_reader.Update()

    def set_geometry_actor_property(self, color, opacity=1, diffuse=0, ambient=1, line_width=1):
        """
        Change geometry actor porperty.
        :param color: Tuple | (R, G, B).
        :param opacity: Float | [0, 1] | 0 is transparent and 1 is solid.
        :param diffuse: Float | [0, 1]
        :param ambient: Float | [0, 1]
        :param line_width: Float
        :return:
        """
        self._geom_actor_prop.SetColor(color)
        self._geom_actor_prop.SetOpacity(opacity)
        self._geom_actor_prop.SetDiffuse(diffuse)
        self._geom_actor_prop.SetAmbient(ambient)
        self._geom_actor_prop.SetLineWidth(line_width)

    def set_mesh_actor_property(self, color, opacity=1, diffuse=0, ambient=1, line_width=1):
        """
        Change mesh actor porperty.
        :param color: Tuple | (R, G, B) | (0, 0, 0) is black and (1, 1, 1) is white.
        :param opacity: Float | [0, 1] | 0 is transparent and 1 is solid.
        :param diffuse: Float | [0, 1]
        :param ambient: Float | [0, 1]
        :param line_width: Float
        :return:
        """
        self._mesh_actor_prop.SetColor(color)
        self._mesh_actor_prop.SetOpacity(opacity)
        self._mesh_actor_prop.SetDiffuse(diffuse)
        self._mesh_actor_prop.SetAmbient(ambient)
        self._mesh_actor_prop.SetLineWidth(line_width)

    def show_mesh(self):
        # Make geometry filter.
        geometryFileter = vtk.vtkGeometryFilter()
        geometryFileter.SetInputConnection(self._file_reader.GetOutputPort())
        # Make polydata mapper.
        geometryMapper = vtk.vtkPolyDataMapper()
        geometryMapper.SetInputConnection(geometryFileter.GetOutputPort())
        # Extract edge.
        edges = vtk.vtkExtractEdges()
        edges.SetInputConnection(geometryFileter.GetOutputPort())
        # Edge mapper.
        edgeMapper = vtk.vtkPolyDataMapper()
        edgeMapper.SetInputConnection(edges.GetOutputPort())
        # Make geometry actor.
        geometry_actor = vtk.vtkActor()
        geometry_actor.SetMapper(geometryMapper)
        geometry_actor.SetProperty(self._geom_actor_prop)
        # Make edges actor.
        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edgeMapper)
        edge_actor.SetProperty(self._mesh_actor_prop)
        # Make renderer.
        renderer = vtk.vtkRenderer()
        renderer.SetBackground((1, 1, 1))
        renderer.AddActor(edge_actor)
        renderer.AddActor(geometry_actor)
        # Make render window.
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.SetSize(800, 800)
        # Render window interactor.
        interactor = vtk.vtkRenderWindowInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        interactor.SetInteractorStyle(style)
        interactor.SetRenderWindow(render_window)
        interactor.Initialize()
        interactor.Start()
