"""Module for creation and manipulation of GDSII and OASIS files."""
from collections import Sequence
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, TypedDict, Union, overload

import numpy
from typing_extensions import Self

__version__ = "0.8.3"

Point = complex | tuple[float, float] | Sequence[float]
EndTypes = (
    Literal["flush", "extended", "round", "smooth"] | tuple[float, float] | Callable
)
JoinTypes = Literal["natural", "miter", "bevel", "round", "smooth"] | Callable
AnchorType = Literal["n", "s", "e", "w", "o", "ne", "nw", "se", "sw"]
PropertyValueType = str | bytes | int
PropertiesType = list[list[PropertyValueType]]
PolygonType = Union["Polygon", "FlexPath", "RobustPath", "Reference"]

class Cell:
    """
    Cell(name)

    Cell structure.

    A cell is a fundamental structure in the layout. It stores the
    geometry, labels and references that make up the final layout. A single
    library can contain any number of independent cells, which can,
    themselves, contain references to other cells in the form of
    :class:`gdstk.Reference`.

    Args:
        name (str): Cell name. It must be ASCII encoded and unique within a
          library.
    """

    @property
    def labels(self) -> list[Label]:
        """List of cell labels.

        Notes:
            This attribute is read-only."""
    name: str
    """Cell name."""

    @property
    def paths(self) -> list[FlexPath | RobustPath]:
        """List of cell paths.

        Notes:
            This attribute is read-only."""
    @property
    def polygons(self) -> list[Polygon]:
        """List of cell polygons.

        Notes:
            This attribute is read-only."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""

    @property
    def references(self) -> list[Reference]:
        """List of cell references.

        Notes:
            This attribute is read-only."""
    def __init__(self, name: str) -> None: ...
    def add(
        self, *elements: Polygon | FlexPath | RobustPath | Label | Reference
    ) -> Self:
        """
        add(*elements) -> self

        Add polygons, paths, labels and references to this cell.
        """
    def area(self, by_spec: bool = False) -> float | dict[tuple[int, int], float]:
        """
        area(by_spec=False) -> float or dictionary

        Calulate the area of this cell.

        Args:
            by_spec: If ``True``, return a dictionary with keys
              ``(layer, datatype)``.

        Returns:
            Area of the geometry in this cell, optionally indexed by layer and
            data type.

        Notes:
            This operation can be slow because all paths and references are
            included in the computation.
        """
    def bounding_box(self) -> tuple[tuple[float, float], tuple[float, float]] | None:
        """
        bounding_box() -> tuple or None

        Calculate the cell bounding box.

        Returns:
            The lower-left and upper-right corners of the bounding box of the
            cell: ``((min_x, min_y), (max_x, max_y))``.

        Examples:
            >>> polygons = gdstk.text("F", 10, (0, 0))
            >>> f_cell = gdstk.Cell("F_CELL")
            >>> f_cell.add(*polygons)
            >>> ang = numpy.pi / 4
            >>> array_ref = gdstk.Reference(f_cell, rotation=ang)
            >>> array_ref.repetition = gdstk.Repetition(columns=3, rows=2,
            ...     v1=8 * numpy.exp(1j * ang), v2=10j * numpy.exp(1j * ang))
            >>> path = gdstk.FlexPath([(-5, 0), (0, -5), (5, 0)], 1,
            ...                       simple_path=True)
            >>> main_cell = gdstk.Cell("MAIN")
            >>> main_cell.add(array_ref, path)
            >>> bbox = main_cell.bounding_box()
            >>> print(bbox)
            ((-12.816310409006173, -5.707106781186548),
             (11.313708498984761, 27.66555281392367))
            >>> polygon_bb = gdstk.rectangle(*bbox, datatype=1)

            .. image:: ../cell/bounding_box.*
               :align: center

        Notes:
            This operation can be slow because all paths and references are
            included in the computation.
        """
    def convex_hull(self) -> numpy.ndarray:
        """
        convex_hull() -> numpy.ndarray

        Calculate the convex hull of the cell.

        The convex hull is the smallest convex polygon that contains all
        elements of the cell.

        Returns:
            Vertices of the convex hull.

        Examples:
            >>> polygons = gdstk.text("F", 10, (0, 0))
            >>> f_cell = gdstk.Cell("F_CELL")
            >>> f_cell.add(*polygons)
            >>> ang = numpy.pi / 4
            >>> array_ref = gdstk.Reference(f_cell, rotation=ang)
            >>> array_ref.repetition = gdstk.Repetition(columns=3, rows=2,
            ...     v1=8 * numpy.exp(1j * ang), v2=10j * numpy.exp(1j * ang))
            >>> path = gdstk.FlexPath([(-5, 0), (0, -5), (5, 0)], 1,
            ...                       simple_path=True)
            >>> main_cell = gdstk.Cell("MAIN")
            >>> main_cell.add(array_ref, path)
            >>> hull = main_cell.convex_hull()
            >>> polygon_hull = gdstk.Polygon(hull, datatype=1)

            .. image:: ../cell/convex_hull.*
               :align: center

        Notes:
            This operation can be slow because all paths and references are
            included in the computation.
        """
    def copy(
        self,
        name,
        translation=...,
        rotation=...,
        magnification=...,
        x_reflection=...,
        deep_copy=...,
    ) -> Cell:
        """
        copy(name, translation=(0, 0), rotation=0, magnification=1, x_reflection=False, deep_copy=True) -> gdstk.Cell

        Create a copy of this cell.

        A transformation can be applied to the contents of the new cell. They
        follow the same order as reference transformations.

        Args:
            name (str): Name of the new cell.
            translation (coordinate pair or complex): Amount to translate the
              cell contents.
            rotation: Rotation angle (in radians).
            magnification: Scaling factor.
            x_reflection: If ``True``, the geometry is reflected across the
              horizontal axis before rotation.
            deep_copy: If ``True``, new elements (polygons, paths, references,
              and labels) are also created for the copied cell. If any
              transformation is applied, this value is always ``True``.

        Returns:
            Copy of this cell.
        """
    def delete_property(self, name) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def dependencies(self, recursive: bool) -> list[Cell | RawCell]:
        """
        dependencies(recursive) -> list

        List of cells and raw cells that are referenced by this cell.

        Args:
            recursive: If ``True``, includes all dependencies recursively.
        """
    def filter(
        self,
        layers: Sequence[int],
        types: Sequence[int],
        operation: Literal["and", "or", "xor", "nand", "nor", "nxor"],
        polygons: bool = True,
        paths: bool = True,
        labels: bool = True,
    ) -> Self:
        """
        filter(layers, types, operation, polygons=True, paths=True, labels=True) -> self

        Remove elements from this cell based on their layer and data/text type.

        An element will be removed if the following check returns True:
        ``(element.layer in layers) op (element.datatype in types)``

        Args:
            layers: Sequence of layers.
            types: Sequence of data/text types.
            operation (str): Logical operation to be used in the filter check.
              One of "and", "or", "xor", "nand", "nor", "nxor".
            polygons: Whether to filter the cell's polygons.
            paths: Whether to filter the cell's paths.
            labels: Whether to filter the cell's labels.

        Examples:
            >>> # Remove all elements in layer 3 and with type 10:
            >>> cell.filter([3], [10], "and")
            >>> # Remove all elements except for those on layer 5:
            >>> cell.filter([5], [], "nor")
        """
    def flatten(self, apply_repetitions: bool = True) -> Self:
        """
        flatten(apply_repetitions=True) -> self

        Transform all references into polygons, paths and labels.

        Args:
            apply_repetitions: Define whether repetitions should be flattened
              for polygons, paths and labels (reference repetitions are always
              applied).

        Examples:
            >>> poly1 = gdstk.Polygon([(0, 0), (1, 0), (0.5, 1)])
            >>> cell1 = gdstk.Cell('CELL_1')
            >>> cell1.add(poly1)
            >>> poly2 = gdstk.Polygon([(1, 0), (1.5, 1), (0.5, 1)], layer=1)
            >>> ref = gdstk.Reference(cell1)
            >>> ref.repetition = gdstk.Repetition(columns=2, rows=2,
            ...                                   spacing=(1, 1))
            >>> cell2 = gdstk.Cell('CELL_2')
            >>> cell2.add(poly2, ref)
            >>> print(len(cell2.polygons), len(cell2.references),
            ...       len(cell2.dependencies(True)))
            1 1 1
            >>> cell2.flatten()
            >>> print(len(cell2.polygons), len(cell2.references),
            ...       len(cell2.dependencies(True)))
            5 0 0

            .. image:: ../cell/flatten.*
               :align: center
        """
    def get_labels(
        self, apply_repetitions=..., depth=..., layer=..., texttype=...
    ) -> list:
        """
        get_labels(apply_repetitions=True, depth=None, layer=None, texttype=None) -> list

        Return a copy of all labels in the cell.

        Args:
            apply_repetitions: Define whether repetitions should be applied in
              the created labels.
            depth: If non negative, indicates the number of reference levels
              processed recursively.  A value of 0 will result in no references
              being visited.  A value of ``None`` (the default) or a negative int
              will include all reference levels below the cell.
            layer: If set, only labels in the defined layer and text type are
              returned.
            texttype: If set, only labels in the defined layer and text type
              are returned.

        Notes:
            Arguments ``layer`` and ``texttype`` must both be set to integers
            for the filtering to be executed.  If either one is ``None`` they
            are both ignored.
        """
    def get_paths(
        self, apply_repetitions=..., depth=..., layer=..., datatype=...
    ) -> list:
        """
        get_paths(apply_repetitions=True, depth=None, layer=None, datatype=None) -> list

        Return a copy of all paths in the cell.

        Args:
            apply_repetitions: Define whether repetitions should be applied in
              the created paths.
            depth: If non negative, indicates the number of reference levels
              processed recursively.  A value of 0 will result in no references
              being visited.  A value of ``None`` (the default) or a negative int
              will include all reference levels below the cell.
            layer: If set, only paths in the defined layer and data type are
              returned.
            datatype: If set, only paths in the defined layer and data type are
              returned.

        Notes:
            Arguments ``layer`` and ``datatype`` must both be set to integers
            for the filtering to be executed.  If either one is ``None`` they
            are both ignored.
        """
    def get_polygons(
        self,
        apply_repetitions: bool = True,
        include_paths: bool = True,
        depth: int | None = None,
        layer: int | None = None,
        datatype: int | None = None,
    ) -> list[Polygon]:
        """
        get_polygons(apply_repetitions=True, include_paths=True, depth=None, layer=None, datatype=None) -> list

        Return a copy of all polygons in the cell.

        Args:
            apply_repetitions: Define whether repetitions should be applied in
              the created polygons.
            include_paths: If ``True``, polygonal representation of paths are
              also included in the result.
            depth: If non negative, indicates the number of reference levels
              processed recursively.  A value of 0 will result in no references
              being visited.  A value of ``None`` (the default) or a negative int
              will include all reference levels below the cell.
            layer: If set, only polygons in the defined layer and data type are
              returned.
            datatype: If set, only polygons in the defined layer and data type
              are returned.

        Notes:
            Arguments ``layer`` and ``datatype`` must both be set to integers
            for the filtering to be executed.  If either one is ``None`` they
            are both ignored.
        """
    def get_property(self, name) -> list:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def remove(self, *elements) -> Self:
        """
        remove(*elements) -> self

        Remove polygons, paths, labels and references from this cell.

        Examples:
            >>> polygons = gdstk.text("Filter dots\nin i and j!", 8, (0, 0))
            >>> cell = gdstk.Cell("FILTERED")
            >>> cell.add(*polygons)
            >>> dots = [poly for poly in cell.polygons if poly.area() < 2]
            >>> cell.remove(*dots)

            .. image:: ../cell/remove.*
               :align: center
        """
    def set_property(self, name, value) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """
    def write_svg(
        self,
        outfile,
        scaling=...,
        precision=...,
        shape_style=...,
        label_style=...,
        background=...,
        pad=...,
        sort_function=...,
    ) -> Self:
        """
        write_svg(outfile, scaling=10, precision=6, shape_style=None, label_style=None, background="#222222", pad="5%", sort_function=None) -> self

        Export this cell to an SVG image file. Colors and attributes must follow
        SVG specification.

        Args:
            outfile (str or pathlib.Path): Name of the output file.
            scaling: Scaling factor for the whole geometry.
            precision (positive integer): Maximum number of digits for
              coordinates after scaling.
            shape_style (dict): SVG attributes for each layer and data type.
            label_style (dict): SVG attributes for each layer and text type.
            background (str): Image background color.
            pad (number, str): Viewport margin around the image content. It can
              be specified as an absolute dimension or a percentage of the
              largest image dimension.
            sort_function (callable): If set, the polygons on each cell will be
              sorted according to this fuction.  It must accept 2 polygons and
              return ``True`` if the first one is below the second.

        Notes:
            Labels in referenced cells will be affected by the the reference
            transformation, including magnification.

        Examples:
            >>> # (layer, datatype) = (0, 1)
            >>> poly1 = gdstk.ellipse((0, 0), (13, 10), datatype=1)
            >>> # (layer, datatype) = (1, 0)
            >>> poly2 = gdstk.ellipse((0, 0), (10, 7), layer=1)
            >>> (layer, texttype) = (3, 2)
            >>> label = gdstk.Label("Example", (0, 0), layer=3, texttype=2)
            >>> cell = gdstk.Cell("SVG")
            >>> cell.add(poly1, poly2, label)
            >>> cell.write_svg(
            ...     "example.svg",
            ...     background="none",
            ...     shape_style={(0, 1): {"fill": "none",
            ...                           "stroke": "black",
            ...                           "stroke-dasharray": "8,8"}},
            ...     label_style={(3, 2): {"fill": "none",
            ...                           "stroke": "red",
            ...                           "font-size": "32px"}},
            ...     pad="5%",
            ...     sort_function=lambda p1, p2: p1.layer < p2.layer,
            ... )

            .. image:: ../cell/write_svg.*
               :align: center
        """

class Curve:
    """
    Curve(xy, tolerance=0.01)

    Curve object for construction of complex polygons.

    The methods are loosely based on the definition of SVG paths.

    Args:
        xy: Curve starting point. It can be a sequence of 2 numbers or a
          single complex value.
        tolerance: Tolerance used for calculating the polygonal
          approximation of the curve.

    Examples:
        >>> curve = gdstk.Curve((3, 4), tolerance=1e-3)
        >>> curve.segment((1, 1), True)
        >>> curve.turn(1, -numpy.pi / 2)
        >>> curve.segment((1, -1), True)
        >>> polygon = gdstk.Polygon(curve.points())

        .. image:: ../curve/init.*
           :align: center
    """

    tolerance: float
    """Tolerance used for calculating the polygonal approximation of the curve.

    Examples:
        >>> curve = gdstk.Curve((-2.5, 0), tolerance=1e-1)
        >>> curve.arc((2, 3), 0, numpy.pi)
        >>> polygon_1 = gdstk.Polygon(curve.points())
        >>> print(polygon_1.size)
        7
        >>> curve = gdstk.Curve((2.5, 0), tolerance=1e-3)
        >>> curve.arc((2, 3), 0, numpy.pi)
        >>> polygon_2 = gdstk.Polygon(curve.points())
        >>> print(polygon_2.size)
        62

        .. image:: ../curve/tolerance.*
        :align: center"""

    def __init__(self, xy: Point, tolerance: float = 0.01) -> None: ...
    def arc(self, radius, initial_angle, final_angle, rotation=...) -> Self:
        """
        arc(radius, initial_angle, final_angle, rotation=0) -> self

        Append an elliptical arc to this curve.

        Args:
            radius (number or sequence[2]): Circular arc radius or elliptical
              arc radii.
            initial_angle: Starting angle (in radians).
            final_angle: Ending angle (in radians).
            rotation: Arc rotation.

        Examples:
            >>> curve = gdstk.Curve((-0.6, 0), tolerance=1e-3)
            >>> curve.segment((1, 0), True)
            >>> curve.arc(1, 0, numpy.pi / 2)
            >>> polygon_1 = gdstk.Polygon(curve.points())

            >>> curve = gdstk.Curve((0.6, 0), tolerance=1e-3)
            >>> curve.segment((1, 0), True)
            >>> curve.arc((2 ** -0.5, 0.4), -numpy.pi / 4, 3 * numpy.pi / 4,
            ...           -numpy.pi / 4)
            >>> polygon_2 = gdstk.Polygon(curve.points())

            .. image:: ../curve/arc.*
               :align: center
        """
    def bezier(self, xy, relative=...) -> Self:
        """
        bezier(xy, relative=False) -> self

        Append a Bézier curve to this curve.

        Args:
            xy (sequence of points): Curve control points.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> points = [(4, 1), (4, 3), (0, 5), (-4, 3), (-4, -2), (0, -4),
            ...           (0, 0)]
            >>> curve = gdstk.Curve((0, 0))
            >>> curve.segment(points)
            >>> control_poly = gdstk.Polygon(curve.points(), datatype=1)
            >>> curve = gdstk.Curve((0, 0), tolerance=1e-3)
            >>> curve.bezier(points)
            >>> polygon = gdstk.Polygon(curve.points())

            .. image:: ../curve/bezier.*
               :align: center
        """
    def commands(self, *args) -> Self:
        """
        commands(*args) -> self

        Parse commands to append sections to this curve.

        Commands are single characters followed by a pre-defined number of
        numerical arguments, according to the table below:

        ======= ======================= ===========================
        Command Primitive               Arguments
        ======= ======================= ===========================
        L/l     Line segment            x, y
        H/h     Horizontal segment      x
        V/v     Vertical segment        y
        C/c     Cubic Bézier            x0, y0, x1, y1, x2, y2
        S/s     Smooth cubic Bézier     x0, y0, x1, y1
        Q/q     Quadratic Bézier        x0, y0, x1, y1
        T/t     Smooth quadratic Bézier x, y
        a       Circular turn           rad, ang
        A       Circular arc            rad, ang0, ang1
        E       Elliptical arc          rad0, rad1, ang0, ang1, rot
        ======= ======================= ===========================

        Uppercase commands assume that coordinates are absolute, whereas the
        lowercase versions assume they are relative to the previous endpoint.

        Notes:
            The meaning and order of the arguments of all commands are identical
            to the corresponding method.

        Examples:
            >>> curve = gdstk.Curve((0, 0), tolerance=1e-3)
            >>> curve.commands("l", 1, 1, "a", 1, -numpy.pi / 2, "l", 1, -1,
            ...                "S", 1, -2, 0, -2)
            >>> polygon = gdstk.Polygon(curve.points())

            .. image:: ../curve/commands.*
               :align: center
        """
    def cubic(self, xy, relative=...) -> Self:
        """
        cubic(xy, relative=False) -> self

        Append cubic Bézier curves to this curve.

        Args:
            xy (sequence of points): Each set of 3 consecutive points is
              interpreted as 2 control points and an end point.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> curve = gdstk.Curve((0, 0), tolerance=1e-3)
            >>> curve.cubic([(1, -2), (2, -2), (3, 0)])
            >>> curve.cubic([(2.7, 1), (1.8, 1), (1.5, 0),
            ...              (1.3, -0.2), (0.3, -0.2), (0, 0)])
            >>> polygon = gdstk.Polygon(curve.points())

            .. image:: ../curve/cubic.*
               :align: center
        """
    def cubic_smooth(self, xy, relative=...) -> Self:
        """
        cubic_smooth(xy, relative=False) -> self

        Append smooth cubic Bézier curves to this curve.

        The first control point is assumed to be the reflection of the last
        control point of this curve with respect to its end point.

        Args:
            xy (sequence of points): Each set of 2 consecutive points is
              interpreted as the second control point and an end point.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> curve = gdstk.Curve((0, 0), tolerance=1e-3)
            >>> curve.cubic([1 + 0j, 2.5 + 1.5j, 2 + 2j])
            >>> curve.cubic_smooth([1j, 0j])
            >>> polygon = gdstk.Polygon(curve.points())
            >>> polygon = gdstk.Polygon(curve.points())

            .. image:: ../curve/cubic_smooth.*
               :align: center
        """
    def horizontal(self, x, relative=...) -> Self:
        """
        horizontal(x, relative=False) -> self

        Append horizontal segments to this curve.

        Args:
            x (number or sequence): End point x coordinates.
            relative: If ``True``, coordinates are relative to the last point.
        """
    def interpolation(
        self,
        points,
        angles=...,
        tension_in=...,
        tension_out=...,
        initial_curl=...,
        final_curl=...,
        cycle=...,
        relative=...,
    ) -> Self:
        """
        interpolation(points, angles=None, tension_in=1, tension_out=1, initial_curl=1, final_curl=1, cycle=False, relative=False) -> self

        Append a smooth interpolating curve through the given points.

        Use the Hobby algorithm [#]_ to calculate a smooth interpolating
        curve made of cubic Bezier segments between each pair of points.  Angle
        and tension parameters can be specified at each point, and the curve can
        be open or closed.

        Args:
            points (sequence[N] of points): Vertices in the interpolating curve.
            angles (``None`` or sequence[N + 1]): Tangent angles at each point
              (in radians). Angles defined as ``None`` are automatically
              calculated.
            tension_in (number or sequence[N + 1]): Tension parameter when
              arriving at each point. One value per point or a single value used
              for all points.
            tension_out (number or sequence[N + 1]): Tension parameter when
              leaving each point. One value per point or a single value used for
              all points.
            initial_curl: Ratio between the mock curvatures at the first point
              and at its neighbor. A value of 1 renders the first segment a good
              approximation for a circular arc. A value of 0 will better
              approximate a straight segment. It has no effect for closed curves
              or when an angle is defined for the first point.
            final_curl: Ratio between the mock curvatures at the last point and
              at its neighbor. It has no effect for closed curves or when an
              angle is defined for the first point.
            cycle: If ``True``, calculates control points for a closed curve,
              with an additional segment connecting the first and last points.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> points = [(4, 1), (4, 3), (0, 5), (-4, 3), (-4, -2), (0, -4)]
            >>> curve = gdstk.Curve((0, 0))
            >>> curve.segment(points)
            >>> control_poly_1 = gdstk.Polygon(curve.points(), datatype=1)
            >>> curve = gdstk.Curve((0, 0), tolerance=1e-3)
            >>> curve.interpolation(points, cycle=True)
            >>> polygon_1 = gdstk.Polygon(curve.points())

            >>> half_pi = numpy.pi / 2
            >>> angles = [half_pi, None, None, None, -half_pi, -half_pi, None]
            >>> curve = gdstk.Curve((4, -9))
            >>> curve.segment(points, relative=True)
            >>> control_poly_2 = gdstk.Polygon(curve.points(), datatype=1)
            >>> curve = gdstk.Curve((4, -9), tolerance=1e-3)
            >>> curve.interpolation(points, angles, cycle=True, relative=True)
            >>> polygon_2 = gdstk.Polygon(curve.points())

            .. image:: ../curve/interpolation.*
               :align: center

        .. [#] Hobby, J.D. "Smooth, easy to compute interpolating splines."
           *Discrete Comput Geom* 1, 123–140 (1986). `DOI: 10.1007/BF02187690
           <https://doi.org/10.1007/BF02187690>`_.
        """
    def parametric(self, curve_function, relative=...) -> Self:
        """
        parametric(curve_function, relative=True) -> self

        Append a parametric curve to this curve.

        Args:
            curve_function (callable): Function that defines the curve. Must be
              a function of one argument (that varies from 0 to 1) that returns
              a 2-element sequence or complex with the coordinates of the curve.
            relative: If ``True``, the return values of ``curve_function`` are
              used as offsets from the current path position, i.e., to ensure a
              continuous path, ``curve_function(0)`` must be (0, 0). Otherwise,
              they are used as absolute coordinates.

        Examples:
            >>> pi = numpy.pi
            >>> def top(u):
            ...     x = 4 * u
            ...     y = 1 - numpy.cos(4 * pi * u)
            ...     return (x, y)
            ...
            >>> curve = gdstk.Curve((-2, 0), tolerance=1e-3)
            >>> curve.parametric(top)
            >>> curve.parametric(
            ...     lambda u: (4 - 2 * u ** 0.5) * numpy.exp(-1.5j * pi * u) - 4
            ... )
            >>> polygon = gdstk.Polygon(curve.points())

            .. image:: ../curve/parametric.*
               :align: center
        """
    def points(self) -> numpy.ndarray:
        """
        points() -> numpy.ndarray

        Return the polygonal approximation of this curve.

        Examples:
            >>> curve = gdstk.Curve((0, 0))
            >>> curve.segment([(1, 0), (0, 1)])
            >>> curve.points()
            array([[0., 0.],
                   [1., 0.],
                   [0., 1.]])
        """
    def quadratic(self, xy, relative=...) -> Self:
        """
        quadratic(xy, relative=False) -> self

        Append quadratic Bézier curves to this curve.

        Args:
            xy (sequence of points): Each set of 2 consecutive points is
              interpreted as control point and an end point.
            relative: If ``True``, coordinates are relative to the last point.

        See also:
            :meth:`gdstk.Curve.cubic`
        """
    def quadratic_smooth(self, xy, relative=...) -> Self:
        """
        quadratic_smooth(xy, relative=False) -> self

        Append smooth quadratic Bézier curves to this curve.

        The control point is assumed to be the reflection of the last control
        point of this curve with respect to its end point.

        Args:
            xy (sequence of points): Curve end points.
            relative: If ``True``, coordinates are relative to the last point.

        See also:
            :meth:`gdstk.Curve.cubic_smooth`
        """
    def segment(self, xy, relative=...) -> Self:
        """
        segment(xy, relative=False) -> self

        Append straight segments to this curve.

        Args:
            xy: Segment end point. It can be a sequence of 2 numbers or a single
              complex. Multiple segments can be constructed by using a sequence
              of points.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> curve = gdstk.Curve((1, 0))
            >>> curve.segment((0, 1))
            >>> curve.segment([0j, -1+0j])
            >>> curve.segment([(0, -1), (2, -1)], True)
            >>> polygon = gdstk.Polygon(curve.points())

            .. image:: ../curve/segment.*
               :align: center
        """
    def turn(self, radius, angle) -> Self:
        """
        turn(radius, angle) -> self

        Append a circular turn to this curve.

        Args:
            radius: Circular arc radius.
            angle: Turning angle. Positive values turn counter clockwise and
              negative values, clockwise.
        """
    def vertical(self, y, relative=...) -> Self:
        """
        vertical(y, relative=False) -> self

        Append vertical segments to this curve.

        Args:
            y (number or sequence): End point y coordinates.
            relative: If ``True``, coordinates are relative to the last point.
        """

class FlexPath:
    """
    FlexPath(points, width, offset=0, joins="natural", ends="flush", bend_radius=0, bend_function=None, tolerance=1e-2, simple_path=False, scale_width=True, layer=0, datatype=0)

    Flexible path creation.

    FlexPath can be used to create single and multiple parallel paths with
    controlled widths and offsets. Joins and end caps can be customized
    freely and, if desired, bends can be automatically created to join path
    segments continuously.

    Adjacent sections are expected to be joined smoothly when at least one
    of them is curved.  If that condition cannot be met,
    :class:`gdstk.RobustPath` should be used instead.

    Args:
        points: Single point or sequence of points that make up the path.
          Each point can be a pair of coordinates or a complex value.
        width (number or sequence): Width of the paths. If this is a
          sequence, its length defines the number of paths created.
        offset (number or sequence): If this is a number, it is treated as
          the distance between centers of adjacent paths. If it is a
          sequence, each number represents the absolute offset from the
          center of the path.
        joins: Definition for the joins. One of "natural", "miter", "bevel",
          "round", "smooth", or a callable. A callable must accept 6
          arguments (end point and direction vector for each edge adjacent
          to the join, the center of the join, and the path width) and
          return a sequence of points that define the join shape.
        ends: Definition for the end caps. One of "flush", "extended",
          "round", "smooth", a 2-tuple, or a callable. A 2-tuple defines the
          extension length on both ends of the path. A callable must accept
          4 arguments (cap end point and direction for both path sides) and
          return a sequence of points that define the cap shape.
        bend_radius (number or sequence): If a positive number, path
          segments are joined by a bend shape (defaults to a circular arc)
          when possible.
        bend_function (callable): A callable that takes 4 arguments (radius,
          initial and final angles, and the bend center) and returns a
          sequence of points defining the bend shape.
        tolerance: Tolerance used for calculating the polygonal
          approximation of the paths.
        simple_path: If ``True``, the paths will be stored as GDSII path
          elements. They require less memory, but do not support "smooth" or
          callable joins and end caps, or width changes along the path.
        scale_width: If ``False``, the path widths are not scaled when
          transforming this path.
        layer: layer number assigned to this path.
        datatype: data type number assigned to this path.

    Notes:
        If ``width`` is a number and ``offset`` a sequence, the number of
        parallel paths is defined by the latter.

        Arguments ``joins``, ``ends``, ``bend_radius``, ``bend_function``,
        ``layer``, and ``datatype`` can also be lists with one definition
        for each path created.

    Examples:
        >>> path = gdstk.FlexPath(
        ...     [(0, 5), (0, 0), (5, 0), (15, 10), (15, -5)],
        ...     [0.8, 0.8, 0.8, 0.8],
        ...     1.0,
        ...     joins=["natural", "bevel", "miter", "round"],
        ...     ends=["flush", "extended", (0.4, 0.8), "round"],
        ...     layer=[0, 1, 2, 3],
        ... )

        .. image:: ../flexpath/init.*
           :align: center

        >>> points = [(0, 8), (0, 0), (8, 0), (18, 13), (18, -8)]
        >>> path_1 = gdstk.FlexPath(points , 1, datatype=1)
        >>> path_2 = gdstk.FlexPath(points , 1, bend_radius=3)

        .. image:: ../flexpath/init0.*
           :align: center

        >>> def custom_broken_join(p0, v0, p1, v1, center, width):
        ...     p0 = numpy.array(p0)
        ...     v0 = numpy.array(v0)
        ...     p1 = numpy.array(p1)
        ...     v1 = numpy.array(v1)
        ...     center = numpy.array(center)
        ...     # Calculate intersection point p between lines defined by
        ...     # p0 + u0 * v0 (for all u0) and p1 + u1 * v1 (for all u1)
        ...     den = v1[1] * v0[0] - v1[0] * v0[1]
        ...     lim = 1e-12 * ((v0[0] ** 2 + v0[1] ** 2) *
        ...                    (v1[0] ** 2 + v1[1] ** 2))
        ...     if den ** 2 < lim:
        ...         # Lines are parallel: use mid-point
        ...         u0 = u1 = 0
        ...         p = 0.5 * (p0 + p1)
        ...     else:
        ...         dx = p1[0] - p0[0]
        ...         dy = p1[1] - p0[1]
        ...         u0 = (v1[1] * dx - v1[0] * dy) / den
        ...         u1 = (v0[1] * dx - v0[0] * dy) / den
        ...         p = 0.5 * (p0 + v0 * u0 + p1 + v1 * u1)
        ...     if u0 <= 0 and u1 >= 0:
        ...         # Inner corner
        ...         return [p]
        ...     # Outer corner
        ...     return [p0, center, p1]
        >>> def custom_pointy_end(p0, v0, p1, v1):
        ...     p0 = numpy.array(p0)
        ...     v0 = numpy.array(v0)
        ...     p1 = numpy.array(p1)
        ...     v1 = numpy.array(v1)
        ...     r = 0.5 * numpy.sqrt(numpy.sum((p0 - p1) ** 2))
        ...     v0 /= numpy.sqrt(numpy.sum(v0 ** 2))
        ...     v1 /= numpy.sqrt(numpy.sum(v1 ** 2))
        ...     return [p0, 0.5 * (p0 + p1) + 0.5 * (v0 - v1) * r, p1]
        >>> path = gdstk.FlexPath(
        ...     [(0, 5), (0, 0), (5, 0), (15, 10), (15, -5)],
        ...     3,
        ...     joins=custom_broken_join,
        ...     ends=custom_pointy_end,
        ... )

        .. image:: ../flexpath/init1.*
           :align: center
    """

    @property
    def bend_function(self) -> list[Callable | None]:
        """Bend function for each path.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.FlexPath.set_bend_function`"""
    @property
    def bend_radius(self) -> list[float]:
        """Bend radius for each path.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.FlexPath.set_bend_radius`"""
    @property
    def datatypes(self) -> list[int]:
        """FlexPath data type.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.FlexPath.set_datatypes`"""
    @property
    def ends(self) -> list[EndTypes]:
        """End types for each path.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.FlexPath.set_ends`"""
    @property
    def joins(self) -> list[JoinTypes]:
        """Join types for each path.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.FlexPath.set_joins`"""
    @property
    def layers(self) -> list[int]:
        """FlexPath layer.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.FlexPath.set_layers`"""
    @property
    def num_paths(self) -> int:
        """Number of paths.

        Notes:
            This attribute is read-only."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""
    repetition: Repetition
    """Repetition associated with this element."""
    scale_width: bool
    """Scale width flag."""
    simple_path: bool
    """Simple path flag."""

    @property
    def size(self) -> int:
        """Number of points in the path spine.

        Notes:
            This attribute is read-only."""
    tolerance: float
    """Path tolerance."""

    def __init__(
        self,
        points: Point | Sequence[Point],
        width: float | Sequence[float],
        offset: float | Sequence[float] = 0,
        joins: Literal["natural", "miter", "bevel", "round", "smooth"]
        | Callable = "natural",
        ends: Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable = "flush",
        bend_radius: float | Sequence[float] = 0,
        bend_function: Callable | None = None,
        tolerance: float = 1e-2,
        simple_path: bool = False,
        scale_width: bool = True,
        layer: int = 0,
        datatype: int = 0,
    ) -> None: ...
    def apply_repetition(self) -> list:
        """
        apply_repetition() -> list

        Create new flexpaths based on this object's ``repetition`` attribute.

        After the repetition is applyed, the original attribute is set to
        ``None``.

        Returns:
            Newly created objects.
        """
    def arc(
        self, radius, initial_angle, final_angle, rotation=..., width=..., offset=...
    ) -> Self:
        """
        arc(radius, initial_angle, final_angle, rotation=0, width=None, offset=None) -> self

        Append an elliptical arc to this path.

        Args:
            radius (number or sequence[2]): Circular arc radius or elliptical
              arc radii.
            initial_angle: Starting angle (in radians).
            final_angle: Ending angle (in radians).
            rotation: Arc rotation.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.

        Examples:
            >>> path = gdstk.FlexPath((0, 0), [0.2, 0.3], 0.4, tolerance=1e-3)
            >>> path.vertical(5)
            >>> path.arc(2.5, numpy.pi, 0)
            >>> path.arc(5, -numpy.pi, -numpy.pi / 2)

            .. image:: ../flexpath/arc.*
               :align: center
        """
    def bezier(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        bezier(xy, width=None, offset=None, relative=False) -> self

        Append a Bézier curve to this path.

        Args:
            xy (sequence of points): Curve control points.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> path = gdstk.FlexPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.bezier([(4, 1), (4, 3), (0, 5),
            ...              (-4, 3), (-4, -2), (0, -4)])

            .. image:: ../flexpath/bezier.*
               :align: center
        """
    def commands(self, *args, **kwargs) -> Self:
        """
        commands(path_commands...) -> self

        Append sections to this path according to commands.

        Commands are single characters followed by a pre-defined number of
        numerical arguments, according to the table below:

        ======= ======================= ===========================
        Command Primitive               Arguments
        ======= ======================= ===========================
        L/l     Line segment            x, y
        H/h     Horizontal segment      x
        V/v     Vertical segment        y
        C/c     Cubic Bézier            x0, y0, x1, y1, x2, y2
        S/s     Smooth cubic Bézier     x0, y0, x1, y1
        Q/q     Quadratic Bézier        x0, y0, x1, y1
        T/t     Smooth quadratic Bézier x, y
        a       Circular turn           rad, ang
        A       Circular arc            rad, ang0, ang1
        E       Elliptical arc          rad0, rad1, ang0, ang1, rot
        ======= ======================= ===========================

        Uppercase commands assume that coordinates are absolute, whereas the
        lowercase versions assume they are relative to the previous endpoint.

        Notes:
            The meaning and order of the arguments of all commands are identical
            to the corresponding method.

        Examples:
            >>> path = gdstk.FlexPath((0, 0), [0.2, 0.4, 0.2], 0.5,
            ...                       tolerance=1e-3)
            >>> path.commands("l", 3, 4,
            ...               "A", 2, numpy.arctan2(3, -4), numpy.pi / 2,
            ...               "h", 0.5,
            ...               "a", 3, -numpy.pi)

            .. image:: ../flexpath/commands.*
               :align: center
        """
    def copy(self) -> FlexPath:
        """
        copy() -> gdstk.FlexPath

        Create a copy this flexpath.

        Returns:
            Copy of this flexpath.
        """
    def cubic(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        cubic(xy, width=None, offset=None, relative=False) -> self

        Append cubic Bézier curves to this path.

        Args:
            xy (sequence of points): Each set of 3 consecutive points is
              interpreted as 2 control points and an end point.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Changes in width and offset are split equally among curve parts
            defined by ``xy``.

        Examples:
            >>> path = gdstk.FlexPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.cubic([(0, 1), (1, 1), (1, 0)])
            >>> path.cubic([(1, -1), (2, -1), (2.5, -0.5),
            ...             (3, 0), (3, 1), (2, 1)], width=0.5)

            .. image:: ../flexpath/cubic.*
               :align: center
        """
    def cubic_smooth(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        cubic_smooth(xy, width=None, offset=None, relative=False) -> self

        Append smooth cubic Bézier curves to this path.

        The first control point is assumed to be the reflection of the last
        control point of this path with respect to its end point.

        Args:
            xy (sequence of points): Each set of 2 consecutive points is
              interpreted as the second control points and an end point.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Changes in width and offset are split equally among curve parts
            defined by ``xy``.

        Examples:
            >>> path = gdstk.FlexPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.cubic([(0, 1), (1, 1), (1, 0)])
            >>> path.cubic_smooth([(2, -1), (2.5, -0.5), (3, 1), (2, 1)],
            ...                   width=0.5)

            .. image:: ../flexpath/cubic_smooth.*
               :align: center
        """
    def delete_gds_property(self, attr) -> Self:
        """
        delete_gds_property(attr) -> self

        Delete a GDSII property of this element.

        Args:
            attr (number): Property number.
        """
    def delete_property(self, name) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def get_gds_property(self, attr) -> str:
        """
        get_gds_property(attr) -> str

        Return a GDSII property of this element.

        Args:
            attr (number): Property number.

        Returns:
            str or None: Property value. If the property number does not exist,
            ``None`` is returned.
        """
    def get_property(self, name) -> list:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def horizontal(
        self,
        x: float | Sequence[float],
        width: float | Sequence[float] | None = None,
        offset: float | Sequence[float] | None = None,
        relative: bool = False,
    ) -> Self:
        """
        horizontal(x, width=None, offset=None, relative=False) -> self

        Append horizontal segments to this path.

        Args:
            x (number or sequence): End point x coordinates.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            If ``x`` is a sequence, changes in width and offset are split
            equally among segments.

        Examples:
            >>> path = gdstk.FlexPath([(0, 0)], 0.2)
            >>> path.horizontal(2, width=0.4, relative=True)
            >>> path.horizontal(2, offset=[0.4], relative=True)
            >>> path.horizontal(2, relative=True)
            >>> print(path.spine())
            ... [[0. 0.]
            ...  [2. 0.]
            ...  [4. 0.]
            ...  [6. 0.]]

            .. image:: ../flexpath/horizontal.*
               :align: center

        See also:
            :meth:`gdstk.FlexPath.segment`
        """
    def interpolation(
        self,
        points,
        angles=...,
        tension_in=...,
        tension_out=...,
        initial_curl=...,
        final_curl=...,
        cycle=...,
        width=...,
        offset=...,
        relative=...,
    ) -> Self:
        """
        interpolation(points, angles=None, tension_in=1, tension_out=1, initial_curl=1, final_curl=1, cycle=False, width=None, offset=None, relative=True) -> self

        Append a smooth interpolating curve through the given points.

        Use the Hobby algorithm [#]_ to calculate a smooth interpolating
        path made of cubic Bezier segments between each pair of points.  Angle
        and tension parameters can be specified at each point, and the path can
        be open or closed.

        Args:
            points (sequence[N] of points): Vertices in the interpolating path.
            angles (``None`` or sequence[N + 1]): Tangent angles at each point
              (in radians). Angles defined as ``None`` are automatically
              calculated.
            tension_in (number or sequence[N + 1]): Tension parameter when
              arriving at each point. One value per point or a single value used
              for all points.
            tension_out (number or sequence[N + 1]): Tension parameter when
              leaving each point. One value per point or a single value used for
              all points.
            initial_curl: Ratio between the mock curvatures at the first point
              and at its neighbor. A value of 1 renders the first segment a good
              approximation for a circular arc. A value of 0 will better
              approximate a straight segment. It has no effect for closed paths
              or when an angle is defined for the first point.
            final_curl: Ratio between the mock curvatures at the last point and
              at its neighbor. It has no effect for closed paths or when an
              angle is defined for the first point.
            cycle: If ``True``, calculates control points for a closed path,
              with an additional segment connecting the first and last points.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> half_pi = numpy.pi / 2
            >>> points = [(4, 1), (4, 3), (0, 5), (-4, 3), (-4, -2), (0, -4)]
            >>> angles = [half_pi, None, None, None, -half_pi, -half_pi, None]
            >>> path_1 = gdstk.FlexPath((0, 0), 0.2, tolerance=1e-3)
            >>> path_1.interpolation(points, cycle=True)
            >>> path_2 = gdstk.FlexPath((6, -8), 0.2, tolerance=1e-3)
            >>> path_2.interpolation(points, angles, cycle=True, relative=True)

            .. image:: ../flexpath/interpolation.*
               :align: center

        .. [#] Hobby, J.D. "Smooth, easy to compute interpolating splines."
           *Discrete Comput Geom* 1, 123–140 (1986). `DOI: 10.1007/BF02187690
           <https://doi.org/10.1007/BF02187690>`_.
        """
    def mirror(self, p1, p2=...) -> Self:
        """
        mirror(p1, p2=(0, 0)) -> self

        Mirror this path across the line through `p1` and `p2`.

        Args:
            p1 (coordinate pair or complex): First point in the mirror line.
            p2 (coordinate pair or complex): Second point in the mirror line.
        """
    def offsets(self) -> numpy.ndarray:
        """
        offsets() -> numpy.ndarray

        Offsets of all paths at every point.

        Returns:
            The offsets of each path at each point.
        """
    def parametric(self, path_function, width=..., offset=..., relative=...) -> Self:
        """
        parametric(path_function, width=None, offset=None, relative=True) -> self

        Append a parametric curve to this path.

        Args:
            path_function (callable): Function that defines the path. Must be a
              function of one argument (that varies from 0 to 1) that returns a
              2-element sequence or complex with the coordinates of the path.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, the return values of ``path_function`` are
              used as offsets from the current path position, i.e., to ensure a
              continuous path, ``path_function(0)`` must be (0, 0). Otherwise,
              they are used as absolute coordinates.

        Examples:

            >>> def spiral(u):
            ...     rad = 2 * u ** 0.5
            ...     ang = 3 * numpy.pi * u
            ...     return (rad * numpy.cos(ang), rad * numpy.sin(ang))
            >>> path = gdstk.FlexPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.parametric(spiral)

            .. image:: ../flexpath/parametric.*
               :align: center
        """
    def path_spines(self) -> list:
        """
        path_spines() -> list

        Central spines of each parallel path.

        Returns:
            Copy of the points that make up each parallel path.
        """
    def quadratic(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        quadratic(xy, width=None, offset=None, relative=False) -> self

        Append quadratic Bézier curves to this path.

        Args:
            xy (sequence of points): Each set of 2 consecutive points is
              interpreted as control point and an end point.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Changes in width and offset are split equally among curve parts
            defined by ``xy``.

        See also:
            :meth:`gdstk.FlexPath.cubic`
        """
    def quadratic_smooth(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        quadratic_smooth(xy, width=None, offset=None, relative=False) -> self

        Append smooth quadratic Bézier curves to this path.

        The control point is assumed to be the reflection of the last control
        point of this curve with respect to its end point.

        Args:
            xy (sequence of points): Curve end points.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Changes in width and offset are split equally among curve parts
            defined by ``xy``.

        See also:
            :meth:`gdstk.FlexPath.cubic_smooth`
        """
    def rotate(self, angle, center=...) -> Self:
        """
        rotate(angle, center=(0, 0)) -> self

        Rotate this path.

        Args:
            angle: Rotation angle (in radians).
            center (coordinate pair or complex): Center of the transformation.
        """
    def scale(self, s, center=...) -> Self:
        """
        scale(s, center=(0, 0)) -> self

        Scale this path.

        Args:
            s: Scaling factor.
            center (coordinate pair or complex): Center of the transformation.
        """
    def segment(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        segment(xy, width=None, offset=None, relative=False) -> self

        Append straight segments to this path.

        Args:
            xy: Segment end point or sequence of end points. Each point can be a
              pair of coordinates or a complex value.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            If ``xy`` is a sequence, changes in width and offset are split
            equally among segments.

        Examples:
            >>> points = [(1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
            >>> path_1 = gdstk.FlexPath((0, 0), 0.2)
            >>> path_1.segment(points, 0.6)
            >>> path_2 = gdstk.FlexPath((3, 0), [0.1, 0.1], 0.2)
            >>> path_2.segment(points, offset=0.6, relative=True)

            .. image:: ../flexpath/segment.*
               :align: center
        """
    def set_bend_function(self, *functions) -> Self:
        """
        set_bend_function(*functions) -> self

        Set the bend function for all paths.

        Args:
            functions: Sequence of callable or ``None``.

        See also:
            :class:`gdstk.FlexPath`
        """
    def set_bend_radius(self, *radii) -> Self:
        """
        set_bend_radius(*radii) -> self

        Set the bend radius for all paths.

        Args:
            radii: Sequence of floats.

        See also:
            :class:`gdstk.FlexPath`
        """
    def set_datatypes(self, *datatypes) -> Self:
        """
        set_datatypes(*datatypes) -> self

        Set the datatypes for all paths.

        Args:
            datatypes: data type numbers for all paths.
        """
    def set_ends(self, *ends) -> Self:
        """
        set_ends(*ends) -> self

        Set the end types for all paths.

        Args:
            ends: Sequence of "flush", "extended", "round", "smooth", a 2-tuple,
              or a callable.

        See also:
            :class:`gdstk.FlexPath`
        """
    def set_gds_property(self, attr, value) -> Self:
        """
        set_gds_property(attr, value) -> self

        Set a GDSII property for this element.

        GDSII properties are stored under the special name "S_GDS_PROPERTY", as
        defined by the OASIS specification.

        Args:
            attr (number): Property number.
            value (str): Property value.
        """
    def set_joins(self, *joins) -> Self:
        """
        set_joins(*joins) -> self

        Set the end types for all paths.

        Args:
            joins: Sequence of "natural", "miter", "bevel", "round", "smooth",
              or a callable.

        See also:
            :class:`gdstk.FlexPath`
        """
    def set_layers(self, *layers) -> Self:
        """
        set_layers(*layers) -> self

        Set the layers for all paths.

        Args:
            layers: layer numbers for all paths.
        """
    def set_property(self, name, value) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """
    def spine(self) -> numpy.ndarray:
        """
        spine() -> numpy.ndarray

        Central path spine.

        Returns:
            Copy of the points that make up the path at zero offset.
        """
    def to_polygons(self) -> list[Polygon]:
        """
        to_polygons() -> list

        Calculate the polygonal representations of this path.

        Returns:
            The polygonal contours defined by this path.
        """
    def translate(self, dx: Point, dy: float | None = None) -> Self:
        """
        translate(dx, dy=None) -> self

        Translate this path.

        Args:
            dx: Translation in the x coordinate or translation vector.
            dy: Translation in the y coordinate.
        """
    def turn(self, radius, angle, width=..., offset=...) -> Self:
        """
        turn(radius, angle, width=None, offset=None) -> self

        Append a circular turn to this path.

        Args:
            radius: Circular arc radius.
            angle: Turning angle. Positive values turn counter clockwise and
              negative values, clockwise.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
        """
    def vertical(self, y, width=..., offset=..., relative=...) -> Self:
        """
        vertical(y, width=None, offset=None, relative=False) -> self

        Append vertical segments to this path.

        Args:
            y (number or sequence): End point y coordinates.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            If ``y`` is a sequence, changes in width and offset are split
            equally among segments.

        See also:
            :meth:`gdstk.FlexPath.segment`, :meth:`gdstk.FlexPath.horizontal`
        """
    def widths(self) -> numpy.ndarray:
        """
        widths() -> numpy.ndarray

        Widths of all paths at every point.

        Returns:
            The widths of each path at each point.
        """

class GdsWriter:
    """
    GdsWriter(outfile, name="library", unit=1e-6, precision=1e-9, max_points=199, timestamp=None)

    Multi-step GDSII stream file writer.

    When a design is too large to be completely created in memory, it is not
    possible to create a :class:`gdstk.Library` to save it as a GDSII file.
    In such cases, it might be possible to still create the desired design
    creating, saving and deleting one cell at a time. Saving one cell at a
    time can be done thru this class.

    Args:
        outfile (str or pathlib.Path): Name of the output file.
        unit: User units in meters.
        precision: Desired precision to store the units once written to a
          GDSII file.
        max_points: Maximal number of vertices per polygon. Polygons with
          more vertices that this are automatically fractured.
        timestamp (datetime object): Timestamp to be stored in the GDSII
          file. If ``None``, the current time is used.

    Eaxmples:
        >>> writer = gdstk.GdsWriter()
        >>> cell1 = some_function_that_creates_a_huge_cell()
        >>> writer.write(cell1)
        >>> del cell1
        >>> cell2 = some_function_that_creates_a_huge_cell()
        >>> writer.write(cell2)
        >>> del cell2
        >>> writer.close()

    See also:
        :ref:`about-units`, :meth:`gdstk.Library.write_gds`
    """

    def __init__(
        self,
        outfile: str | Path,
        name: str = "library",
        unit: float = 1e-6,
        precision: float = 1e-9,
        max_points: int = 199,
        timestamp: datetime | None = None,
    ) -> None: ...
    def close(self) -> None:
        """
        close() -> None

        Finish writing the output file and close it.
        """
    def write(self, *cells: Cell) -> Self:
        """
        write(*cells) -> self

        Write cells to the output file.
        """

class Label:
    """
    Label(text, origin, anchor="o", rotation=0, magnification=1, x_reflection=False, layer=0, texttype=0)

    Text objects with out geometrical information.

    Labels do not create any new geometry in the layout. They can be used to
    add descriptions, flags, or comments to the design. For polygonal text,
    :func:`gdstk.text` should be used instead.

    Args:
        text (str): Text string.
        origin (coordinate pair or complex): Label position.
        anchor (str): Origin position with respect to the label text. One of
          "n", "s", "e", "w", "o", "ne", "nw", "se", or "sw".
        rotation: Rotation angle (in radians).
        magnification: Scaling factor.
        x_reflection: If ``True``, the label is reflected across the
          horizontal axis before rotation.
        layer: layer number assigned to this label.
        texttype: text type number assigned to this label.

    Examples:
        >>> frame = gdstk.rectangle((-2, -1), (2, 1), datatype=1)
        >>> label_o = gdstk.Label("Center", (0, 0), rotation=numpy.pi / 6)
        >>> label_n = gdstk.Label("North", (0, 1), "n")
        >>> label_s = gdstk.Label("South", (0, -1), "s")
        >>> label_e = gdstk.Label("East", (2, 0), "e")
        >>> label_w = gdstk.Label("West", (-2, 0), "w")
        >>> label_ne = gdstk.Label("Northeast", (2, 1), "ne")
        >>> label_se = gdstk.Label("Southeast", (2, -1), "se")
        >>> label_nw = gdstk.Label("Northwest", (-2, 1), "nw")
        >>> label_sw = gdstk.Label("Southwest", (-2, -1), "sw")

        .. image:: ../label/init.*
           :align: center

        Note that this example can only be correctly displayed in browsers
        with good support for text alignment in SVG images.

    Notes:
        Label anchor and transformations (rotation, magnification and
        reflection) are not supported by the OASIS format.
    """

    anchor: AnchorType
    """Label anchor."""
    layer: int
    """Label layer."""
    magnification: float
    """Label scaling factor."""

    @property
    def origin(self) -> tuple[float, float]:
        """Label origin."""
    @origin.setter
    def origin(self, value: Point) -> None:
        """Label origin."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""
    repetition: Repetition
    """Repetition associated with this element."""
    rotation: float
    """Label rotation angle."""
    text: str
    """Label text."""
    texttype: int
    """Label text type."""
    x_reflection: bool
    """Label reflection across the x axis."""

    def __init__(
        self,
        text: str,
        origin: Point,
        anchor: AnchorType = "o",
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        layer: int = 0,
        texttype: int = 0,
    ) -> None: ...
    def apply_repetition(self) -> list[Label]:
        """
        apply_repetition() -> list

        Create new labels based on this object's ``repetition`` attribute.

        After the repetition is applyed, the original attribute is set to
        ``None``.

        Returns:
            Newly created objects.
        """
    def copy(self) -> Label:
        """
        copy() -> gdstk.Label

        Create a copy this label.

        Returns:
            Copy of this label.
        """
    def delete_gds_property(self, attr: int) -> Self:
        """
        delete_gds_property(attr) -> self

        Delete a GDSII property of this element.

        Args:
            attr (number): Property number.
        """
    def delete_property(self, name: str) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def get_gds_property(self, attr: int) -> str:
        """
        get_gds_property(attr) -> str

        Return a GDSII property of this element.

        Args:
            attr (number): Property number.

        Returns:
            str or None: Property value. If the property number does not exist,
            ``None`` is returned.
        """
    def get_property(self, name: str) -> list:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def set_gds_property(self, attr: int, value: str) -> Self:
        """
        set_gds_property(attr, value) -> self

        Set a GDSII property for this element.

        GDSII properties are stored under the special name "S_GDS_PROPERTY", as
        defined by the OASIS specification.

        Args:
            attr (number): Property number.
            value (str): Property value.
        """
    def set_property(
        self, name: str, value: PropertyValueType | list[PropertyValueType]
    ) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """

class Library:
    """
    Library(name="library", unit=1e-6, precision=1e-9)

    GDSII/OASIS library.

    The library is a container for multiple cells which keeps track of the
    units used to generate the design.

    Args:
        name: Library name.
        unit: User units in meters.
        precision: Desired precision to store the units once written to a
          GDSII/OASIS file.

    See also:
        :ref:`about-units`
    """

    @property
    def cells(self) -> list[Cell | RawCell]:
        """List of library cells.

        Notes:
            This attribute is read-only."""
    name: str
    """Library name."""
    precision: float
    """Library precision."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""
    unit: float
    """Library unit."""

    def __init__(
        self, name: str = "library", unit: float = 1e-6, precision: float = 1e-9
    ) -> None: ...
    def add(self, *cells: Cell | RawCell) -> Self:
        """
        add(*cells) -> self

        Add cells to this library.

        Examples:
            >>> polygon = gdstk.rectangle((0, 0), (1, 1))
            >>> cell = gdstk.Cell("MAIN")
            >>> cell.add(polygon)
            >>> lib = gdstk.Library()
            >>> lib.add(cell)

        Notes:
            This method does not check whether cell names are duplicated in the
            library.  If duplicates are found in the library, the resulting file
            will be invalid.

        See also:
            :meth:`gdstk.Library.replace`
        """
    def delete_property(self, name: str) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def get_property(self, name: str) -> list[PropertyValueType] | None:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def layers_and_datatypes(self) -> set[tuple[int, int]]:
        """
        layers_and_datatypes() -> set

        Return a set of tuples with the layer and data types in the library.
        """
    def layers_and_texttypes(self) -> set[tuple[int, int]]:
        """
        layers_and_texttypes() -> set

        Return a set of tuples with the layer and text types in the library.
        """
    def new_cell(self, name: str) -> Cell:
        """
        new_cell(name) -> gdstk.Cell

        Create a new cell and add it to this library.

        Args:
            name (str): Name of the new cell.

        Examples:
            >>> lib = gdstk.Library()
            >>> cell = lib.new_cell("MAIN")
            >>> polygon = gdstk.rectangle((0, 0), (1, 1))
            >>> cell.add(polygon)
        """
    def remove(self, *cells: Cell | RawCell) -> Self:
        """
        remove(*cells) -> self

        Remove cells from this library.
        """
    def replace(self, *cells: Cell | RawCell) -> Self:
        """
        replace(*cells) -> self

        Add cells to this library, replacing any cells with the same name.

        References to any removed cells are also replaced with the new cell.

        Examples:
            >>> polygon = gdstk.rectangle((-10, -10), (10, 10))
            >>> cell = gdstk.Cell("Alignment Mark")
            >>> cell.add(polygon)
            >>> lib = gdstk.read_gds("layout.gds")
            >>> lib.replace(cell)
        """
    def set_property(
        self, name: str, value: PropertyValueType | list[PropertyValueType]
    ) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """
    def top_level(self) -> list[Cell]:
        """
        top_level() -> list

        Return the top-level cells in the library.

        Top-level cells are cells that do not appear as dependency of any other
        cells in the library.
        """
    def write_gds(
        self,
        outfile: str | Path,
        max_points: int = 199,
        timestamp: datetime | None = None,
    ) -> None:
        """
        write_gds(outfile, max_points=199, timestamp=None) -> None

        Save this library to a GDSII file.

        Args:
            outfile (str or pathlib.Path): Name of the output file.
            max_points: Maximal number of vertices per polygon. Polygons with
              more vertices that this are automatically fractured.
            timestamp (datetime object): Timestamp to be stored in the GDSII
              file. If ``None``, the current time is used.

        See also:
            :ref:`getting-started`
        """
    def write_oas(
        self,
        outfile,
        compression_level=...,
        detect_rectangles=...,
        detect_trapezoids=...,
        circletolerance=...,
        standard_properties=...,
        validation=...,
    ) -> None:
        """
        write_oas(outfile, compression_level=6, detect_rectangles=True, detect_trapezoids=True, circletolerance=0, standard_properties=False, validation=None) -> None

        Save this library to an OASIS file.

        Args:
            outfile (str or pathlib.Path): Name of the output file.
            compression_level: Level of compression for cells (between 0 and 9).
              Setting to 0 will disable cell compression, 1 gives the best speed
              and 9, the best compression.
            detect_rectangles: Store rectangles in compressed format.
            detect_trapezoids: Store trapezoids in compressed format.
            circle_tolerance: Tolerance for detecting circles. If less or equal
              to 0, no detection is performed. Circles are stored in compressed
              format.
            validation ("crc32", "checksum32", None): type of validation to
              include in the saved file.
            standard_properties: Staore standard OASIS properties in the file.

        Notes:
            The standard OASIS options include the maximal string length and
            integer size used in the file, maximal numbers of polygon and path
            vertices, cell bounding boxes and cell offsets inside the file.
            Some of these properties are computationally expensive to calculate.
            Use only when required.

        See also:
            :ref:`getting-started`
        """

class Polygon:
    """
    Polygon(points, layer=0, datatype=0)

    Polygonal geometric object.

    Args:
        points (sequence): Vertices of the polygon. Each element can be a
          pair of coordinates or a complex value.
        layer: layer number assigned to this polygon.
        datatype: data type number assigned to this polygon.

    Examples:
        >>> polygon_1 = gdstk.Polygon([(0, 0), (1, 0), 1 + 1.5j, 1j])
        >>> polygon_2 = gsdkt.Polygon([0j, (-1, 1), (-1, 0)], 2, 3)

        .. image:: ../polygon/init.*
           :align: center
    """

    datatype: int
    """Polygon data type."""
    layer: int
    """Polygon layer."""

    @property
    def points(self) -> list[tuple[float, float]]:
        """Vertiecs of the polygon.

        Notes:
            This attribute is read-only."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""
    repetition: Repetition
    """Repetition associated with this element."""

    @property
    def size(self) -> int:
        """Number of vertices in this polygon.

        Notes:
            This attribute is read-only."""
    def __init__(
        self, points: Sequence[Point], layer: int = 0, datatype: int = 0
    ) -> None: ...
    def apply_repetition(self) -> list[Polygon]:
        """
        apply_repetition() -> list

        Create new polygons based on this object's ``repetition`` attribute.

        After the repetition is applyed, the original attribute is set to
        ``None``.

        Returns:
            Newly created objects.
        """
    def area(self) -> float:
        """
        area() -> float

        Polygon area.

        Returns:
            Area of the polygon.
        """
    def bounding_box(self) -> tuple:
        """
        bounding_box() -> tuple

        Calculate the polygon bounding box.

        Returns:
            The lower-left and upper-right corners of the bounding box of the
            polygon: ``((min_x, min_y), (max_x, max_y))``.

        Examples:
            >>> polygon = gdstk.Polygon([(0, 1), (1, 2), (3, -1)])
            >>> bbox = polygon.bounding_box()
            >>> print(bbox)
            ((0.0, -1.0), (3.0, 2.0))
            >>> polygon_bb = gdstk.rectangle(*bbox, datatype=1)

            .. image:: ../polygon/bounding_box.*
               :align: center
        """
    def contain(self, *args, **kwargs) -> Any:
        """
        contain(*points) -> bool, tuple

        Check whether points are inside this polygon.

        Points on the polygon edges or coinciding with any of its vertices are
        considered inside.

        Args:
            points (point or sequence of points): Points to check. Arguments
              can be a pair of coordinates, a complex number, or a sequence of
              those.

        Returns:
            If the argument is a single point, returns a boolean. In the case of
            a sequence, a tuple of booleans (one for each point) is returned.
        """
    def contain_all(self, *points) -> bool:
        """
        contain_all(*points) -> bool

        Check whether all points are inside this polygon.

        Points on the polygon edges or coinciding with any of its vertices are
        considered inside.

        Args:
            points: Points to check. Each point can be a pair of coordinates or
              a complex number.

        Returns:
            `True` if all points are inside the polygon, `False` otherwise.
        """
    def contain_any(self, *points) -> bool:
        """
        contain_any(*points) -> bool

        Check whether any of the points are inside this polygon.

        Points on the polygon edges or coinciding with any of its vertices are
        considered inside.

        Args:
            points: Points to check. Each point can be a pair of coordinates or
              a complex number.

        Returns:
            `True` if any of the points are inside the polygon, `False`
            otherwise.
        """
    def copy(self) -> Polygon:
        """
        copy() -> gdstk.Polygon

        Create a copy this polygon.

        Returns:
            Copy of this polygon.
        """
    def delete_gds_property(self, attr) -> Self:
        """
        delete_gds_property(attr) -> self

        Delete a GDSII property of this element.

        Args:
            attr (number): Property number.
        """
    def delete_property(self, name) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def fillet(self, radius, tolerance=...) -> Self:
        """
        fillet(radius, tolerance=0.01) -> self

        Fillet the corners of this polygon.

        Args:
            radius (number or sequence): Fillet radius. A sequence of values can
              be used to define the fillet radius for each vertex.
            tolerance: Tolerance used for calculating the polygonal
              approximation of the filleted corners.

        Notes:
            The actual fillet radius for a given corner is the specified value
            or half the lenght of the shortest segment adjacent to that corner,
            whichever is smaller.

        Examples:
            >>> points = [(0, 0), (1.2, 0), (1.2, 0.3), (1, 0.3), (1.5, 1),
            ...           (0, 1.5)]
            >>> polygon_1 = gdstk.Polygon(points, datatype=1)
            >>> polygon_2 = gdstk.Polygon(points).fillet(0.3, tolerance=1e-3)

            .. image:: ../polygon/fillet.*
               :align: center
        """
    def fracture(self, max_points=..., precision=...) -> list:
        """
        fracture(max_points=199, precision=1e-3) -> list

        Fracture this polygon into a list of polygons.

        Args:
            max_points: Maximal number of vertices for each resulting polygon.
              Official GDSII documentation requires that all polygons have at
              most 199 vertices, but 8190 is usually supported by most software.
            precision: Desired vertex precision for fracturing.

        Returns:
            List of fractured polygons.

        Notes:
            If ``max_points < 5`` the return value is an empty list.

        Examples:
            >>> polygon = gdstk.racetrack((0, 0), 30, 60, 40, tolerance=1e-3)
            >>> poly_list = polygon.fracture()
            >>> print(len(poly_list))
            10
            >>> print([p.size for p in poly_list])
            [102, 103, 103, 101, 101, 102, 102, 103, 103, 102]

            .. image:: ../polygon/fracture.*
               :align: center
        """
    def get_gds_property(self, attr) -> str:
        """
        get_gds_property(attr) -> str

        Return a GDSII property of this element.

        Args:
            attr (number): Property number.

        Returns:
            str or None: Property value. If the property number does not exist,
            ``None`` is returned.
        """
    def get_property(self, name) -> list:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def mirror(self, p1, p2=...) -> Self:
        """
        mirror(p1, p2=(0, 0)) -> self

        Mirror this polygon across the line through ``p1`` and ``p2``.

        Args:
            p1 (coordinate pair or complex): First point in the mirror line.
            p2 (coordinate pair or complex): Second point in the mirror line.
        """
    def rotate(self, angle, center=...) -> Self:
        """
        rotate(angle, center=(0, 0)) -> self

        Rotate this polygon.

        Args:
            angle: Rotation angle (in radians).
            center (coordinate pair or complex): Center of the transformation.
        """
    def scale(self, sx, sy=..., center=...) -> Self:
        """
        scale(sx, sy=0, center=(0, 0)) -> self

        Scale this polygon.

        Args:
            sx: Scaling in the x direction.
            sy: Scaling in the y direction. If set to 0, ``sx`` is used instead.
            center (coordinate pair or complex): Center of the transformation.
        """
    def set_gds_property(self, attr, value) -> Self:
        """
        set_gds_property(attr, value) -> self

        Set a GDSII property for this element.

        GDSII properties are stored under the special name "S_GDS_PROPERTY", as
        defined by the OASIS specification.

        Args:
            attr (number): Property number.
            value (str): Property value.
        """
    def set_property(self, name, value) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """
    def transform(
        self,
        magnification=...,
        x_reflection=...,
        rotation=...,
        translation=...,
        matrix=...,
    ) -> Self:
        """
        transform(magnification=1, x_reflection=False, rotation=0, translation=None, matrix=None) -> self

        Transform the vertices of this polygon.

        The transformation if applied in the order of the arguments in the
        method signature, starting with a magnification.  If a transformation
        matrix is given, it is applied after the other transforms.

        Args:
            magnification (number): Magnification factor.
            x_reflection (bool): If `True`, the vertices are reflected across
              the x axis.
            rotation (number): Rotation angle (in radians).
            translation (coordinate pair or complex): Translation vector.
            matrix (matrix-like): Transformation matrix with 2 or 3 rows and 2
              or 3 columns.

        Notes:
            If the number of rows or columns of the transformation matrix is 3,
            homogeneous coordinates are used.
        """
    def translate(self, dx: float | Point, dy: float | None = None) -> Self:
        """
        translate(dx, dy=None) -> self

        Translate this polygon.

        Args:
            dx: Translation in the x coordinate or translation vector.
            dy: Translation in the y coordinate.
        """

class RawCell:
    """
    RawCell(name)

    A Cell structure that is stored in binary GDSII format.

    Raw cells are not meant to be created in the same way cells are. They
    come from :func:`gdstk.read_rawcells` and are used when the imported
    elements will not be modified in any way. They are smaller in memory and
    require almost no processing to be used, making them a preferred option
    when using an external GDSII file as a parts library (such as in PDKs).

    Notes:
        The units of the imported ``RawCell`` are not checked against the
        current user units. It is up to the user to ensure they are equal.

    See also:
        :func:`gdstk.read_rawcells`, :func:`gdstk.gds_units`
    """

    @property
    def name(self) -> str:
        """Raw cell name.

        Notes:
            This attribute is read-only."""
    @property
    def size(self) -> int:
        """Raw cell size (in bytes).

        Notes:
            This attribute is read-only."""
    def __init__(self, name: str) -> None: ...
    def dependencies(self, recursive: bool) -> list[RawCell]:
        """
        dependencies(recursive) -> list

        List of raw cells that are referenced by this raw cell.

        Args:
            recursive: If ``True``, includes all dependencies recursively.
        """

class Reference:
    """
    Reference(cell, origin=(0, 0), rotation=0, magnification=1, x_reflection=False, columns=1, rows=1, spacing=None)

    Reference to another cell.

    References are used to instance repetitive geometries across different
    cells, optionally applying a transformation.

    Args:
        cell (gdstk.Cell, gdstk.RawCell, str): referenced cell.
        origin: Insertion position of the referenced cell.
        rotation: Cell rotation angle (in radians).
        magnification: Geometry scaling for this reference.
        x_reflection: If ``True``, the geometry is reflected across the
          horizontal axis before rotation.
        columns: Number of repetitions along the first direction.
        rows: Number of repetitions along the second direction.
        spacing: Spacing between insertions points of repetitions.

    Examples:
        >>> polygons = gdstk.text("F", 10, (0, 0))
        >>> f_cell = gdstk.Cell("F_CELL")
        >>> f_cell.add(*polygons)
        >>> ref = gdstk.Reference(f_cell, rotation=numpy.pi / 2)
        >>> array_ref = gdstk.Reference(f_cell, columns=3, rows=2,
        ...                             spacing=(8, 10))

        .. image:: ../reference/init.*
           :align: center

    Notes:
        If ``cell`` is a str (cell name), operations on the referenced cell
        are not performed, such as computing the bounding box.

        When ``spacing`` is set, a repetition is defined according to the
        ``rotation`` and ``x_reflection`` arguments.
    """

    cell: Cell | RawCell | str
    """Cell referenced by this object."""
    magnification: float
    """Reference magnification."""

    @property
    def origin(self) -> tuple[float, float]:
        """Reference origin."""
    @origin.setter
    def origin(self, value: Point) -> None:
        """Reference origin."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""

    repetition: Repetition
    """Repetition associated with this element."""
    rotation: float
    """Reference rotation angle (in radians)."""
    x_reflection: bool
    """Reference reflection across the x axis."""

    def __init__(
        self,
        cell: Cell | RawCell | str,
        origin: Point = (0, 0),
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        columns: int = 1,
        rows: int = 1,
        spacing: Point | None = None,
    ) -> None: ...
    def apply_repetition(self) -> list:
        """
        apply_repetition() -> list

        Create new references based on this object's ``repetition`` attribute.

        After the repetition is applyed, the original attribute is set to
        ``None``.

        Returns:
            Newly created objects.
        """
    def bounding_box(self) -> tuple:
        """
        bounding_box() -> tuple

        Calculate the bounding box of this reference.

        Returns:
            The lower-left and upper-right corners of the bounding box of the
            polygon: ``((min_x, min_y), (max_x, max_y))``.

        Notes:
            This operation can be slow because the precise bounding box
            calculation requires recursively querying the polygonal
            representations of all shapes created by this reference.

        Examples:
            >>> polygons = gdstk.text("F", 10, (0, 0))
            >>> f_cell = gdstk.Cell("F_CELL")
            >>> f_cell.add(*polygons)
            >>> ang = numpy.pi / 4
            >>> array_ref = gdstk.Reference(f_cell, rotation=ang)
            >>> array_ref.repetition = gdstk.Repetition(columns=3, rows=2,
            ...     v1=8 * numpy.exp(1j * ang), v2=10j * numpy.exp(1j * ang))
            >>> array_ref = gdstk.Reference(f_cell, rotation=numpy.pi / 4)
            >>> array_ref.repetition = gdstk.Repetition(columns=3, rows=2,
            ...                                         spacing=(8, 10))
            >>> bbox = array_ref.bounding_box()
            >>> print(bbox)
            ((-12.816310409006173, 1.7677669529663689),
             (11.313708498984761, 27.66555281392367))
            >>> polygon_bb = gdstk.rectangle(*bbox, datatype=1)

            .. image:: ../reference/bounding_box.*
               :align: center
        """
    def convex_hull(self) -> numpy.ndarray:
        """
        convex_hull() -> ndarray

        Calculate the convex hull of this reference.

        The convex hull is the smallest convex polygon that contains all
        elements of this reference.

        Returns:
            Vertices of the convex hull.

        Examples:
            >>> polygons = gdstk.text("F", 10, (0, 0))
            >>> f_cell = gdstk.Cell("F_CELL")
            >>> f_cell.add(*polygons)
            >>> ang = numpy.pi / 4
            >>> array_ref = gdstk.Reference(f_cell, rotation=ang)
            >>> array_ref.repetition = gdstk.Repetition(columns=3, rows=2,
            ...     v1=8 * numpy.exp(1j * ang), v2=10j * numpy.exp(1j * ang))
            >>> path = gdstk.FlexPath([(-5, 0), (0, -5), (5, 0)], 1,
            ...                       simple_path=True)
            >>> main_cell = gdstk.Cell("MAIN")
            >>> main_cell.add(array_ref, path)
            >>> hull = main_cell.convex_hull()
            >>> polygon_hull = gdstk.Polygon(hull, datatype=1)

            .. image:: ../reference/convex_hull.*
               :align: center

        Notes:
            This operation can be slow because all paths and references are
            included in the computation.
        """
    def copy(self) -> Reference:
        """
        copy() -> gdstk.Reference

        Create a copy this reference.

        Returns:
            Copy of this reference.
        """
    def delete_gds_property(self, attr) -> Self:
        """
        delete_gds_property(attr) -> self

        Delete a GDSII property of this element.

        Args:
            attr (number): Property number.
        """
    def delete_property(self, name) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def get_gds_property(self, attr) -> str:
        """
        get_gds_property(attr) -> str

        Return a GDSII property of this element.

        Args:
            attr (number): Property number.

        Returns:
            str or None: Property value. If the property number does not exist,
            ``None`` is returned.
        """
    def get_property(self, name) -> list:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def set_gds_property(self, attr, value) -> Self:
        """
        set_gds_property(attr, value) -> self

        Set a GDSII property for this element.

        GDSII properties are stored under the special name "S_GDS_PROPERTY", as
        defined by the OASIS specification.

        Args:
            attr (number): Property number.
            value (str): Property value.
        """
    def set_property(self, name, value) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """

class Repetition:
    """
    Repetition(columns=None, rows=None, spacing=None, v1=None, v2=None, offsets=None, x_offsets=None, y_offsets=None)

    Repetition object that creates multiple identical elements.

    A repetition can be set in any polygon, path, label or reference to
    indicate that the element should be copied to multiple positions.
    Repetitions can be of 5 different types, depending on which arguments
    are set:

    - Rectangular: requires `columns`, `rows` and `spacing`. Creates a
      rectangular array of copies.
    - Regular: requires `columns`, `rows`, `v1` and `v2`. Creates an array
      of copies along the specified direction vectors.
    - Explicit: requires `offsets`. Creates copies at the specified position
      offsets. The original element at offset (0, 0) is always present, so
      it should not be specified in the `offsets` array.
    - X-explicit: requires `x-offsets`. Creates a linear array of copies
      at the given x coordinates. Coordinate 0 is always included, so it
      should not be specified.
    - Y-explicit: requires `y-offsets`. Creates a linear array of copies
      at the given y coordinates.  Coordinate 0 is always included, so it
      should not be specified.

    Args:
        columns (int): Number of copies in the x direction (rectangular) or
          along `v1` (regular).
        rows (int): Number of copies in the y direction (rectangular) or
          along `v2` (regular).
        spacing (coordinate pair or complex): Step sizes in x and y
          directions for rectangular array.
        v1 (coordinate pair or complex): First vector defining the shape of
          a regular array.
        v2 (coordinate pair or complex): Second vector defining the shape of
          a regular array.
        offsets (sequence of points): Explicit offsets for copies.
        x_offsets (sequence of numbers): Explicit x coordinates for copies.
        y_offsets (sequence of numbers): Explicit y coordinates for copies.

    Examples:
        >>> ref_array = gdstk.Reference("Some Cell")
        >>> # Create an array of 3 by 2 references:
        >>> ref_array.repetition = gdstk.Repetition(
        ...     offsets=[(10, 10), (20, 0), (10, -10)]
        ... )

    Notes:
        All attributes of Repetition objects are read-only.
    """

    @property
    def columns(self) -> int | None:
        """Number of columns in a rectangular or regular array."""
    @property
    def offsets(self) -> numpy.ndarray | None:
        """Offsets for an explicit array."""
    @property
    def rows(self) -> int | None:
        """Number of rows in a rectangular or regular array."""
    @property
    def size(self) -> int:
        """Number of offsets generated by this repetition."""
    @property
    def spacing(self) -> tuple[float, float] | None:
        """Spacing in a rectangular array."""
    @property
    def v1(self) -> tuple[float, float] | None:
        """First vector defining a regular array."""
    @property
    def v2(self) -> tuple[float, float] | None:
        """Second vector defining a regular array."""
    @property
    def x_offsets(self) -> numpy.ndarray | None:
        """X coordinates for an x-explicit array."""
    @property
    def y_offsets(self) -> numpy.ndarray | None:
        """Y coordinates for a y-explicit array."""
    @overload
    def __init__(self, columns: int, rows: int, spacing: Point) -> None: ...
    @overload
    def __init__(self, columns: int, rows: int, v1: Point, v2: Point) -> None: ...
    @overload
    def __init__(self, offsets: Sequence[Point]) -> None: ...
    @overload
    def __init__(self, x_offsets: Sequence[float]) -> None: ...
    @overload
    def __init__(self, y_offsets: Sequence[float]) -> None: ...
    def get_offsets(self) -> numpy.ndarray:
        """
        get_offsets() -> numpy.ndarray

        Calculate all offsets generated by this repetition.

        Returns:
            Offsets generated by this repetition.
        """

class RobustPath:
    """
    RobustPath(initial_point, width, offset=0, ends="flush",tolerance=1e-2, max_evals=1000, simple_path=False, scale_width=True, layer=0, datatype=0)

    Robust path creation.

    RobusPath can be used to create single and multiple parallel paths with
    parametrized widths and offsets. End caps can be customized freely.
    Intersections between adjacent sections are numerically determined so
    that curved sections do not need to be joined smoothly.

    Args:
        initial_point (coordinate pair or complex): Starting point of the
          path.
        width (number or sequence): Width of the paths. If this is a
          sequence, its length defines the number of paths created.
        offset (number or sequence): If this is a number, it is treated as
          the distance between centers of adjacent paths. If it is a
          sequence, each number represents the absolute offset from the
          center of the path.
        ends: Definition for the end caps. One of "flush", "extended",
          "round", "smooth", a 2-tuple, or a callable. A 2-tuple defines the
          extension length on both ends of the path. A callable must accept
          4 arguments (cap end point and direction for both path sides) and
          return a sequence of points that define the cap shape.
        tolerance: Tolerance used for calculating the polygonal
          approximation of the paths.
        max_evals: Maximal number of path evaluations per section.  Used for
          intersection finding at joins and to create the polygonal
          approximation for each section.
        simple_path: If ``True``, the paths will be stored as GDSII path
          elements. They require less memory, but do not support "smooth" or
          callable joins and end caps, or width changes along the path.
        scale_width: If ``False``, the path widths are not scaled when
          transforming this path.
        layer: layer number assigned to this path.
        datatype: data type number assigned to this path.

    Notes:
        If ``width`` is a number and ``offset`` a sequence, the number of
        parallel paths is defined by the latter.

        Arguments ``ends``, ``layer``, and ``datatype`` can also be lists
        with one definition for each path created.

    Examples:
        >>> fpath = gdstk.FlexPath((0, 0), 0.5, tolerance=1e-3)
        >>> fpath.arc(1, 0, numpy.pi/2)
        >>> fpath.arc(1, 0, -numpy.pi/2)
        >>> rpath = gdstk.RobustPath((3, 0), 0.5, tolerance=1e-3)
        >>> rpath.arc(1, 0, numpy.pi/2)
        >>> rpath.arc(1, 0, -numpy.pi/2)

        .. image:: ../robustpath/init.*
           :align: center

        >>> path = gdstk.RobustPath((0, 0),
        ...     [0.8, 0.8, 0.8, 0.8],
        ...     1.0,
        ...     ends=["flush", "extended", (0.4, 0.8), "round"],
        ...     tolerance=1e-3,
        ...     layer=[0, 1, 2, 3],
        ... )
        >>> path.horizontal(5)

        .. image:: ../robustpath/init1.*
           :align: center
    """

    @property
    def datatypes(self) -> list[int]:
        """RobustPath data type.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.RobustPath.set_datatypes`"""
    @property
    def ends(self) -> list[EndTypes]:
        """End types for each path.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.RobustPath.set_ends`"""
    @property
    def layers(self) -> list[int]:
        """RobustPath layer.

        Notes:
            This attribute is read-only.

        See also:
            :meth:`gdstk.RobustPath.set_layers`"""
    @property
    def num_paths(self) -> int:
        """Number of paths.

        Notes:
            This attribute is read-only."""
    properties: PropertiesType
    """Properties of this element.

    Properties are represented as a list of lists, each containing the
    property name followed by its values."""

    repetition: Repetition
    """Repetition associated with this element."""
    scale_width: bool
    """Scale width flag."""
    simple_path: bool
    """Simple path flag."""

    @property
    def size(self) -> int:
        """Number of sections in this path.

        Notes:
            This attribute is read-only."""
    tolerance: float
    """Path tolerance."""
    max_evals: int
    """Maximal number of path evaluations per section."""

    def __init__(
        self,
        initial_point: Point,
        width: float | Sequence[float],
        offset: float | Sequence[float] = 0,
        ends: EndTypes = "flush",
        tolerance: float = 1e-2,
        max_evals: int = 1000,
        simple_path: bool = False,
        scale_width: bool = True,
        layer: int | Sequence[int] = 0,
        datatype: int | Sequence[int] = 0,
    ) -> None: ...
    def apply_repetition(self) -> list:
        """
        apply_repetition() -> list

        Create new robustpaths based on this object's ``repetition`` attribute.

        After the repetition is applyed, the original attribute is set to
        ``None``.

        Returns:
            Newly created objects.
        """
    def arc(
        self,
        radius: float | Sequence[float],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
        width=...,
        offset=...,
    ) -> Self:
        """
        arc(radius, initial_angle, final_angle, rotation=0, width=None, offset=None) -> self

        Append an elliptical arc to this path.

        Args:
            radius (number or sequence[2]): Circular arc radius or elliptical
              arc radii.
            initial_angle: Starting angle (in radians).
            final_angle: Ending angle (in radians).
            rotation: Arc rotation.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.

        Examples:
            >>> path = gdstk.FlexPath((0, 0), [0.2, 0.3], 0.4, tolerance=1e-3)
            >>> path.vertical(5)
            >>> path.arc(2.5, numpy.pi, 0)
            >>> path.arc((3, 5), -numpy.pi, -numpy.pi / 2)

            .. image:: ../robustpath/arc.*
               :align: center
        """
    def bezier(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        bezier(xy, width=None, offset=None, relative=False) -> self

        Append a Bézier curve to this path.

        Args:
            xy (sequence of points): Control points for the Bézier. Each point
              can be a coordinate pair or a complex.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        Examples:
            >>> path = gdstk.RobustPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.bezier(
            ...     [(4, 1), (4, 3), (0, 5), (-4, 3), (-4, -2), (0, -4)],
            ...     width=lambda u: 0.2 + 0.8 * u ** 2,
            ... )

            .. image:: ../robustpath/bezier.*
               :align: center

        See also:
            :meth:`gdstk.RobustPath.segment`
        """
    def commands(self, *args, **kwargs) -> Self:
        """
        commands(path_commands...) -> self

        Append sections to this path according to commands.

        Commands are single characters followed by a pre-defined number of
        numerical arguments, according to the table below:

        ======= ======================= ===========================
        Command Primitive               Arguments
        ======= ======================= ===========================
        L/l     Line segment            x, y
        H/h     Horizontal segment      x
        V/v     Vertical segment        y
        C/c     Cubic Bézier            x0, y0, x1, y1, x2, y2
        S/s     Smooth cubic Bézier     x0, y0, x1, y1
        Q/q     Quadratic Bézier        x0, y0, x1, y1
        T/t     Smooth quadratic Bézier x, y
        a       Circular turn           rad, ang
        A       Circular arc            rad, ang0, ang1
        E       Elliptical arc          rad0, rad1, ang0, ang1, rot
        ======= ======================= ===========================

        Uppercase commands assume that coordinates are absolute, whereas the
        lowercase versions assume they are relative to the previous endpoint.

        Notes:
            The meaning and order of the arguments of all commands are identical
            to the corresponding method.

        Examples:
            >>> path = gdstk.RobustPath((0, 0), [0.2, 0.4, 0.2], 0.5,
            ...                         tolerance=1e-3)
            >>> path.commands("l", 3, 4,
            ...               "A", 2, numpy.arctan2(3, -4), numpy.pi / 2,
            ...               "h", 0.5,
            ...               "a", 3, -numpy.pi)

            .. image:: ../robustpath/commands.*
               :align: center
        """
    def copy(self) -> RobustPath:
        """
        copy() -> gdstk.RobustPath

        Create a copy this robustpath.

        Returns:
            Copy of this robustpath.
        """
    def cubic(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        cubic(xy, width=None, offset=None, relative=False) -> self

        Append a cubic Bézier curve to this path.

        Args:
            xy (sequence of 3 points): Control points and end point for the
              Bézier. Each point can be a coordinate pair or a complex.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        Examples:
            >>> path = gdstk.RobustPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.cubic([(0.5, 0.8), (0.5, 2.2), (0, 3)])
            >>> path.cubic([(0.8, -0.5), (2.2, -0.5), (3, 0)], relative=True)
            >>> path.cubic([(-0.5, -0.8), (-0.5, -2.2), (0, -3)], relative=True)

            .. image:: ../robustpath/cubic.*
               :align: center

        See also:
            :meth:`gdstk.RobustPath.segment`
        """
    def cubic_smooth(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        cubic_smooth(xy, width=None, offset=None, relative=False) -> self

        Append a smooth cubic Bézier curve to this path.

        The first control point of the Bézier is such that the gradient of the
        path is continuous.

        Args:
            xy (sequence of 2 points): Second control point and end point for
              the Bézier. Each can be a coordinate pair or a complex.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        Examples:
            >>> path = gdstk.RobustPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.cubic([(0.5, 0.8), (0.5, 2.2), (0, 3)])
            >>> path.cubic_smooth([(3.5, 0.8), (3, 0)], relative=True)
            >>> path.cubic_smooth([(-0.5, -2.2), (0, -3)], relative=True)

            .. image:: ../robustpath/cubic_smooth.*
               :align: center

        See also:
            :meth:`gdstk.RobustPath.segment`, :meth:`gdstk.RobustPath.cubic`
        """
    def delete_gds_property(self, attr) -> Self:
        """
        delete_gds_property(attr) -> self

        Delete a GDSII property of this element.

        Args:
            attr (number): Property number.
        """
    def delete_property(self, name) -> Self:
        """
        delete_property(name) -> self

        Delete the first property of this element matching a name.

        Args:
            name (str): Property name.
        """
    def get_gds_property(self, attr) -> str:
        """
        get_gds_property(attr) -> str

        Return a GDSII property of this element.

        Args:
            attr (number): Property number.

        Returns:
            str or None: Property value. If the property number does not exist,
            ``None`` is returned.
        """
    def get_property(self, name) -> list:
        """
        get_property(name) -> list

        Return the values of the first property of this element matching a name.

        Args:
            name (str): Property name.

        Returns:
            list or None: List of property values. If no property is found,
            ``None`` is returned.
        """
    def gradient(self, u, from_below=...) -> numpy.ndarray:
        """
        gradient(u, from_below=True) -> numpy.ndarray

        Calculate the gradient of this path.

        Args:
            u (number): Where in the path to calculate the position. The value
              must be in the range 0 thru :attr:`gdstk.RobustPath.size`,
              inclusive.
            from_below: If there is a discontinuity at ``u``, use the value
              approaching from below.

        Returns:
            The spine gradient of the path at ``u``.
        """
    def horizontal(self, x, width=..., offset=..., relative=...) -> Self:
        """
        horizontal(x, width=None, offset=None, relative=False) -> self

        Append a horizontal segment to this path.

        Args:
            x (number): End point x coordinate.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        See also:
            :meth:`gdstk.RobustPath.segment`
        """
    def interpolation(
        self,
        points,
        angles=...,
        tension_in=...,
        tension_out=...,
        initial_curl=...,
        final_curl=...,
        cycle=...,
        width=...,
        offset=...,
        relative=...,
    ) -> Self:
        """
        interpolation(points, angles=None, tension_in=1, tension_out=1, initial_curl=1, final_curl=1, cycle=False, width=None, offset=None, relative=True) -> self

        Append a smooth interpolating curve through the given points.

        Use the Hobby algorithm [#]_ to calculate a smooth interpolating
        path made of cubic Bezier segments between each pair of points.  Angle
        and tension parameters can be specified at each point, and the path can
        be open or closed.

        Args:
            points (sequence[N] of points): Vertices in the interpolating path.
            angles (``None`` or sequence[N + 1]): Tangent angles at each point
              (in radians). Angles defined as ``None`` are automatically
              calculated.
            tension_in (number or sequence[N + 1]): Tension parameter when
              arriving at each point. One value per point or a single value used
              for all points.
            tension_out (number or sequence[N + 1]): Tension parameter when
              leaving each point. One value per point or a single value used for
              all points.
            initial_curl: Ratio between the mock curvatures at the first point
              and at its neighbor. A value of 1 renders the first segment a good
              approximation for a circular arc. A value of 0 will better
              approximate a straight segment. It has no effect for closed paths
              or when an angle is defined for the first point.
            final_curl: Ratio between the mock curvatures at the last point and
              at its neighbor. It has no effect for closed paths or when an
              angle is defined for the first point.
            cycle: If ``True``, calculates control points for a closed path,
              with an additional segment connecting the first and last points.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Examples:
            >>> half_pi = numpy.pi / 2
            >>> points = [(4, 1), (4, 3), (0, 5), (-4, 3), (-4, -2), (0, -4)]
            >>> angles = [half_pi, None, None, None, -half_pi, -half_pi, None]
            >>> path_1 = gdstk.RobustPath((0, 0), 0.2, tolerance=1e-3)
            >>> path_1.interpolation(points, cycle=True)
            >>> path_2 = gdstk.RobustPath((6, -8), 0.2, tolerance=1e-3)
            >>> path_2.interpolation(points, angles, cycle=True, relative=True)

            .. image:: ../robustpath/interpolation.*
               :align: center

        See also:
            :meth:`gdstk.RobustPath.segment`

        .. [#] Hobby, J.D. "Smooth, easy to compute interpolating splines."
           *Discrete Comput Geom* 1, 123–140 (1986). `DOI: 10.1007/BF02187690
           <https://doi.org/10.1007/BF02187690>`_.
        """
    def mirror(self, p1, p2=...) -> Self:
        """
        mirror(p1, p2=(0, 0)) -> self

        Mirror this path across the line through `p1` and `p2`.

        Args:
            p1 (coordinate pair or complex): First point in the mirror line.
            p2 (coordinate pair or complex): Second point in the mirror line.
        """
    def offsets(self, u, from_below=...) -> numpy.ndarray:
        """
        offsets(u, from_below=True) -> numpy.ndarray

        Calculate the offset of this path.

        Args:
            u (number): Where in the path to calculate the width. The value must
              be in the range 0 thru :attr:`gdstk.RobustPath.size`, inclusive.
            from_below: If there is a discontinuity at ``u``, use the value
              approaching from below.

        Returns:
            The offsets of each path at ``u``.
        """
    def parametric(
        self, path_function, path_gradient=..., width=..., offset=..., relative=...
    ) -> Self:
        """
        parametric(path_function, path_gradient=None, width=None, offset=None, relative=True) -> self

        Append a parametric curve to this path.

        Args:
            path_function (callable): Function that defines the path. Must be a
              function of one argument (that varies from 0 to 1) that returns a
              2-element sequence or complex with the coordinates of the path.
            path_gradient (callable): Function that returns the path gradient.
              Must be a function of one argument (that varies from 0 to 1) that
              returns a 2-element sequence or complex with the gradient.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, the return values of ``path_function`` are
              used as offsets from the current path position, i.e., to ensure a
              continuous path, ``path_function(0)`` must be (0, 0). Otherwise,
              they are used as absolute coordinates.

        Examples:

            >>> def spiral(u):
            ...    rad = 2 * u ** 0.5
            ...    ang = 3 * numpy.pi * u
            ...    return (rad * numpy.cos(ang), rad * numpy.sin(ang))
            >>> path = gdstk.RobustPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.parametric(spiral, width=lambda u: 0.2 + 0.6 * u ** 2)

            .. image:: ../robustpath/parametric.*
               :align: center
        """
    def path_spines(self) -> list:
        """
        path_spines() -> list

        Central spines of each parallel path.

        Returns:
            Copy of the points that make up each parallel path.
        """
    def position(self, u, from_below=...) -> numpy.ndarray:
        """
        position(u, from_below=True) -> numpy.ndarray

        Calculate the position of this path.

        Args:
            u (number): Where in the path to calculate the position. The value
              must be in the range 0 thru :attr:`gdstk.RobustPath.size`,
              inclusive.
            from_below: If there is a discontinuity at ``u``, use the value
              approaching from below.

        Returns:
            The spine position of the path at ``u``.
        """
    def quadratic(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        quadratic(xy, width=None, offset=None, relative=False) -> self

        Append a quadratic Bézier curve to this path.

        Args:
            xy (sequence of 2 points): Control point and end point for the
              Bézier. Each point can be a coordinate pair or a complex.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        See also:
            :meth:`gdstk.RobustPath.segment`, :meth:`gdstk.RobustPath.cubic`
        """
    def quadratic_smooth(self, xy, width=..., offset=..., relative=...) -> Self:
        """
        quadratic_smooth(xy, width=None, offset=None, relative=False) -> self

        Append a smooth quadratic Bézier curve to this path.

        The control point of the Bézier is such that the gradient of the path is
        continuous.

        Args:
            xy (coordinate pair or complex): End point for the Bézier.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        See also:
            :meth:`gdstk.RobustPath.segment`,
            :meth:`gdstk.RobustPath.cubic_smooth`
        """
    def rotate(self, angle, center=...) -> Self:
        """
        rotate(angle, center=(0, 0)) -> self

        Rotate this path.

        Args:
            angle: Rotation angle (in radians).
            center (coordinate pair or complex): Center of the transformation.
        """
    def scale(self, s, center=...) -> Self:
        """
        scale(s, center=(0, 0)) -> self

        Scale this path.

        Args:
            s: Scaling factor.
            center (coordinate pair or complex): Center of the transformation.
        """
    def segment(self, xy: Point, width=..., offset=..., relative: bool = ...) -> Self:
        """
        segment(xy, width=None, offset=None, relative=False) -> self

        Append a straight segment to this path.

        Args:
            xy (coordinate pair or complex): Segment end point.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        Examples:
            >>> path = gdstk.RobustPath((0, 0), 0.2, tolerance=1e-3)
            >>> path.segment((5, 0), 1.0)
            >>> path.segment((5, 3), (0.2, "constant"))
            >>> path.segment((0, 3), (1.2, "smooth"))
            >>> path.segment(
            ...     (0, 7),
            ...     lambda u: 0.2 + 0.8 * numpy.cos(2 * numpy.pi * u) ** 2
            ... )

            .. image:: ../robustpath/segment.*
               :align: center

            >>> path = gdstk.RobustPath((0, 0), [0.2, 0.2], 0.3, tolerance=1e-3)
            >>> path.segment((5, 0), offset=0.8)
            >>> path.segment((5, 3), offset=(0.3, "constant"))
            >>> path.segment((0, 3), offset=(1.0, "smooth"))
            >>> path.segment((0, 7), offset=[
            ...     lambda u: -0.2 - 0.8 * numpy.cos(2 * numpy.pi * u) ** 2,
            ...     lambda u: 0.2 + 0.8 * numpy.cos(2 * numpy.pi * u) ** 2
            ... ])

            .. image:: ../robustpath/segment1.*
               :align: center
        """
    def set_datatypes(self, *datatypes) -> Self:
        """
        set_datatypes(*datatypes) -> self

        Set the datatypes for all paths.

        Args:
            datatypes: data type numbers for all paths.
        """
    def set_ends(self, *ends) -> Self:
        """
        set_ends(*ends) -> self

        Set the end types for all paths.

        Args:
            ends: Sequence of "flush", "extended", "round", "smooth", a 2-tuple,
              or a callable.

        See also:
            :class:`gdstk.RobustPath`
        """
    def set_gds_property(self, attr, value) -> Self:
        """
        set_gds_property(attr, value) -> self

        Set a GDSII property for this element.

        GDSII properties are stored under the special name "S_GDS_PROPERTY", as
        defined by the OASIS specification.

        Args:
            attr (number): Property number.
            value (str): Property value.
        """
    def set_layers(self, *layers) -> Self:
        """
        set_layers(*layers) -> self

        Set the layers for all paths.

        Args:
            layers: layer numbers for all paths.
        """
    def set_property(self, name, value) -> Self:
        """
        set_property(name, value) -> self

        Set a property for this element.

        The property name does not have to be unique. Multiple properties can
        have the same name.

        Args:
            name (str): Property name.
            value (str, bytes, number, or sequence of those): Values associated with
              the property.

        Notes:
            General properties are not supported by GDSII files. Use the
            specific methods to access GDSII properties.
        """
    def spine(self) -> numpy.ndarray:
        """
        spine() -> numpy.ndarray

        Central path spine.

        Returns:
            Copy of the points that make up the path at zero offset.
        """
    def to_polygons(self) -> list:
        """
        to_polygons() -> list

        Calculate the polygonal representations of this path.

        Returns:
            The polygonal contours defined by this path.
        """
    def translate(self, dx, dy=...) -> Self:
        """
        translate(dx, dy=None) -> self

        Translate this path.

        Args:
            dx: Translation in the x coordinate or translation vector.
            dy: Translation in the y coordinate.
        """
    def turn(
        self,
        radius: float,
        angle: float,
        width: float | Sequence[float] = ...,
        offset: float | Sequence[float] = ...,
    ) -> Self:
        """
        turn(radius, angle, width=None, offset=None) -> self

        Append a circular turn to this path.

        Args:
            radius: Circular arc radius.
            angle: Turning angle. Positive values turn counter clockwise and
              negative values, clockwise.
            width (number or sequence): Width at the end point(s). If this is a
              sequence, it must define the width for each path. The width is
              linearly tapered from its previous value.
            offset (number or sequence): If this is a number, it is treated as
              the distance between centers of adjacent paths. If it is a
              sequence, each number represents the absolute offset from the
              center of the path. The offsets are linearly tapered from their
              previous values.
        """
    def vertical(self, y, width=..., offset=..., relative=...) -> Self:
        """
        vertical(y, width=None, offset=None, relative=False) -> self

        Append a vertical segment to this path.

        Args:
            y (number): End point x coordinate.
            width (number, tuple, or callable): Width of this section. A tuple
              of 2 elements (number, str) can be used to define the width value
              and the interpolation type from the previous section to the end
              point ("constant", "linear", or "smooth"). If only a number is
              used, the interpolation defaults to "linear". A callable must
              accept a single number from 0 to 1 and return the desired width at
              the corresponding position along the section.
            offset (number, tuple, or callable): Offset from the central path
              position. A tuple or callable can be used as in ``width``.
            relative: If ``True``, coordinates are relative to the last point.

        Notes:
            Arguments ``width`` and ``offset`` can also be lists with one
            definition for each path.

            If ``offset`` is a single number or tuple, it is treated as the
            distance between adjacent paths.

        See also:
            :meth:`gdstk.RobustPath.segment`
        """
    def widths(self, u, from_below=...) -> numpy.ndarray:
        """
        widths(u, from_below=True) -> numpy.ndarray

        Calculate the width of this path.

        Args:
            u (number): Where in the path to calculate the width. The value must
              be in the range 0 thru :attr:`gdstk.RobustPath.size`, inclusive.
            from_below: If there is a discontinuity at ``u``, use the value
              approaching from below.

        Returns:
            The widths of each path at ``u``.
        """

def all_inside(
    points: Sequence[Point], polygons: PolygonType | Sequence[PolygonType]
) -> bool:
    """
    all_inside(points, polygons) -> bool

    Check whether all points are inside the set of polygons.

    Points on polygon edges or coinciding with any of their vertices are
    considered inside.

    Args:
        points: Points to check. Each point can be a pair of coordinates or
          a complex number.
        polygons (Polygon, FlexPath, RobustPath, Reference, sequence):
          Polygons to test against. If this is a sequence, each element can
          be any of the polygonal types or a sequence of points (coordinate
          pairs or complex).

    Returns:
        `True` if all points are inside the polygon set, `False` otherwise.
    """

def any_inside(
    points: Sequence[Point], polygons: PolygonType | Sequence[PolygonType]
) -> bool:
    """
    any_inside(points, polygons) -> bool

    Check whether any of the points are inside the set of polygons.

    Points on polygon edges or coinciding with any of their vertices are
    considered inside.

    Args:
        points: Points to check. Each point can be a pair of coordinates or
          a complex number.
        polygons (Polygon, FlexPath, RobustPath, Reference, sequence):
          Polygons to test against. If this is a sequence, each element can
          be any of the polygonal types or a sequence of points (coordinate
          pairs or complex).

    Returns:
        `True` if any point is inside the polygon set, `False` otherwise.
    """

def boolean(
    operand1: PolygonType | Sequence[PolygonType],
    operand2: PolygonType | Sequence[PolygonType],
    operation: Literal["or", "and", "xor", "not"],
    precision: float = 1e-3,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]:
    """
    boolean(operand1, operand2, operation, precision=1e-3, layer=0, datatype=0) -> list

    Execute boolean (clipping) operations between polygons.

    Args:
        operand1 (Polygon, FlexPath, RobustPath, Reference, sequence): First
          operand. If this is a sequence, each element can be any of the
          polygonal types or a sequence of points (coordinate pairs or
          complex).
        operand2 (Polygon, FlexPath, RobustPath, Reference, sequence):
          Second operand.
        operation (str): Boolean operation to be executed. One of "or",
          "and", "xor", or "not". The "not" operation performs the set
          difference ``operand1 - operand2``.
        precision: Desired precision for rounding vertex coordinates.
        layer: layer number assigned to the resulting polygons.
        datatype: data type number assigned to the resulting polygons.

    Returns:
        List of :class:`gdstk.Polygon`.

    Examples:
        >>> circle = gdstk.ellipse((0, 0), 50)
        >>> path = gdstk.FlexPath((-50, 30), [5, 5], 10)
        >>> path.interpolation([(20, 15), (0, 0), (-20, -15), (50, -30)],
        ...                    angles=[0.3, None, None, None, 0.3])
        >>> text = gdstk.text("GDSTK", 40, (-2.5 * 40 * 9 / 16, -40 / 2))
        >>> result = gdstk.boolean(circle, text + [path], "not")

        .. image:: ../function/boolean.*
           :align: center

    Notes:
        Repetitions are not applied to any elements, except references and
        their contents.
    """

def contour(
    data: numpy.ndarray,
    level: float = 0,
    length_scale: float = 1,
    precision: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]:
    """
    contour(data, level=0, length_scale=1, precision=0.01, layer=0, datatype=0) -> list

    Extract polygonal contours from 2-d array data at given level.

    Args:
        data (array-like[M][N]): 2-dimensional array with shape `(M, N)`.
        level: Polygons are created representing the regions where `data` is
          at least `level`.
        length_scale: Distance between neighboring elements in `data`.
        precision: Desired precision for rounding vertex coordinates.
        layer: layer number assigned to the resulting polygons.
        datatype: data type number assigned to the resulting polygons.

    Returns:
        List of :class:`gdstk.Polygon`.

    Examples:
        >>> y, x = numpy.mgrid[0.5:1.5:128j, -1:1:255j]
        >>> data = (numpy.sin(4 * numpy.pi * x * y)
        ...         - 0.8 * numpy.sin(2 * numpy.pi * y))
        >>> contours = gdstk.contour(data, 0, 1 / 127, 0.01 / 127)
        >>> rect = gdstk.rectangle((0, 0), (2, 1), datatype=1)

        .. image:: ../function/contour.*
           :align: center

    Notes:
        The length scale for the polygons is one element of `data`, i.e.,
        the full region represented by `data` represents a rectangular area
        of `lenght_scale * (N - 1)` × `length_scale * (M - 1)`.  Argument
        `precision` is understood in this length scale.
    """

def cross(
    center: Point, full_size: float, arm_width: float, layer: int = 0, datatype: int = 0
) -> Polygon:
    """
    cross(center, full_size, arm_width, layer=0, datatype=0) -> gdstk.Polygon

    Create a cross shape.

    Args:
        center (coordinate pair or complex): Center of the cross.
        full_size (number): Total length of the cross.
        arm_width (number): Width of the arms.
        layer: layer number assigned to this polygon.
        datatype: data type number assigned to this polygon.

    Examples:
        >>> cross1 = gdstk.cross((0, 0), 10, 1)
        >>> cross2 = gdstk.cross((0.5, 0.5), 5, 0.75, layer=1)

        .. image:: ../function/cross.*
           :align: center
    """

def ellipse(
    center: Point,
    radius: float | Sequence[float],
    inner_radius: float | Sequence[float] | None = None,
    initial_angle: float = 0,
    final_angle: float = 0,
    tolerance: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon:
    """
    ellipse(center, radius, inner_radius=None, initial_angle=0, final_angle=0, tolerance=0.01, layer=0, datatype=0) -> gdstk.Polygon

    Create an ellipse, circle, slice or ring.

    Args:
        center (coordinate pair or complex): Circle/ellipse center.
        radius (number or sequence): Circle radius of the circle. A pair of
          numbers can be used to define an ellipse.
        inner_radius (number or sequence): If set, creates a ring.
        initial_angle: Initial angle to define a slice.
        final_angle: Final slice angle.
        tolerance: Tolerance used for calculating the polygonal
          approximation of this shape.
        layer: layer number assigned to this polygon.
        datatype: data type number assigned to this polygon.

    Examples:
        >>> circle = gdstk.ellipse((0, 0), 40)
        >>> ellipse = gdstk.ellipse((100, 0), (40, 30), layer=1)
        >>> ring = gdstk.ellipse((0, 100), 40, inner_radius=(30, 20),
                                 layer=2)
        >>> c_slice = gdstk.ellipse((100, 100), 40,
        ...                         initial_angle=-numpy.pi / 4,
        ...                         final_angle=5 * numpy.pi / 4,
        ...                         layer=3)
        >>> r_slice = gdstk.ellipse((50, 200), (70, 30), (60, 20),
        ...                         -3 * numpy.pi / 4, numpy.pi / 2,
        ...                         layer=4)

        .. image:: ../function/ellipse.*
           :align: center
    """

class GdsInfoDict(TypedDict):
    cell_names: list[str]
    layers_and_datatypes: set[tuple[int, int]]
    layers_and_texttypes: set[tuple[int, int]]
    num_polygons: int
    num_paths: int
    num_references: int
    num_labels: int
    unit: float
    precision: float

def gds_info(infile: str | Path) -> GdsInfoDict:
    """
    gds_info(infile) -> dict

    Gather information from a GDSII file without loading the geometry.

    Args:
        infile (str or pathlib.Path): Name of the input file.

    Returns:
        Dictionary with library info.

        The following keys are available in the return dictionary:

        ``cell_names``: list with all cell names

        ``layers_and_datatypes``: set of 2-tuples with layers and data
        types

        ``layers_and_texttypes``: set of 2-tuples with layers and text
        types

        ``num_polygons``: number of polygons in the library

        ``num_paths``: number of paths in the library

        ``num_references``: number of references in the library

        ``num_labels``: number of labels in the library

        ``unit``: library unit

        ``precision`` library precision
    """

def gds_timestamp(filename: str | Path, timestamp: datetime | None = None) -> datetime:
    """
    gds_timestamp(filename, timestamp=None) -> datetime

    Get and set the timestamp of a GDSII file.

    Args:
        filename (str or pathlib.Path): Name of the GDSII file.
        timestamp (datetime object): If not ``None``, the timestamp of the
          file is set to this value.

    Returns:
        Timestamp of the file before modification (if any).

    Notes:
        This function modifies the contents of the file. The creation,
        modification and access timestamps of the file itself are modified
        according to the file system rules in place for reading and
        writing.
    """

def gds_units(infile: str | Path) -> tuple[float, float]:
    """
    gds_units(infile) -> tuple

    Read the unit and precision of a GDSII file.

    Args:
        infile (str or pathlib.Path): Name of the input file.

    Returns:
        Tuple with the unit and precision of the library in the file.
    """

def inside(
    points: Sequence[Point], polygons: PolygonType | Sequence[PolygonType]
) -> tuple[bool, ...]:
    """
    inside(points, polygons) -> tuple

    Check whether each point is inside the set of polygons.

    Points on polygon edges or coinciding with any of their vertices are
    considered inside.

    Args:
        points: Points to check. Each point can be a pair of coordinates or
          a complex number.
        polygons (Polygon, FlexPath, RobustPath, Reference, sequence):
          Polygons to test against. If this is a sequence, each element can
          be any of the polygonal types or a sequence of points (coordinate
          pairs or complex).

    Returns:
        Tuple of booleans (one for each point).
    """

def oas_precision(infile: str | Path) -> float:
    """
    oas_precision(infile) -> float

    Read the precision of an OASIS file.

    Args:
        infile (str or pathlib.Path): Name of the input file.

    Returns:
        Precision of the library in the file.
    """

def oas_validate(infile: str | Path) -> tuple[bool, int]:
    """
    oas_validate(infile) -> tuple

    Check the validation signature of an OASIS file, if any.

    Args:
        infile (str or pathlib.Path): Name of the input file.

    Returns:
        Validation result (True/False) and the calculated signature. If the
        file does not have a signature, returns (None, 0)
    """

def offset(
    polygons: PolygonType | Sequence[PolygonType],
    distance: float,
    join: Literal["miter", "bevel", "round"] = "miter",
    tolerance: float = 2,
    precision: float = 1e-3,
    use_union: bool = False,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]:
    """
    offset(polygons, distance, join="miter", tolerance=2, precision=1e-3, use_union=False, layer=0, datatype=0) -> list

    Dilate or erode polygons.

    Args:
        polygons (Polygon, FlexPath, RobustPath, Reference, sequence):
          Polygons to offset. If this is a sequence, each element can be any
          of the polygonal types or a sequence of points (coordinate pairs
          or complex).
        distance (number): Offset distance. Positive values dilate the
          geometry, whereas negative values erode it.
        join: Type of joins for the offset polygon. One of "miter", "bevel",
          or "round".
        tolerance: For miter joints, this number must be at least 2 and it
          represents the maximal distance in multiples of offset between new
          vertices and their original position before beveling to avoid
          spikes at acute joints. For round joints, it indicates the
          curvature resolution in number of points per full circle.
        precision: Desired precision for rounding vertex coordinates.
        use_union: Apply a union operation before the offset to merge
          adjacent polygons.
        layer: layer number assigned to the resulting polygons.
        datatype: data type number assigned to the resulting polygons.

    Returns:
        List of :class:`gdstk.Polygon`.

    Examples:
        >>> text = gdstk.text("#A", 10, (0, 0), datatype=1)
        >>> circle = gdstk.ellipse((5, 11), 5, initial_angle=0,
        ...                        final_angle=numpy.pi, datatype=1)
        >>> path = gdstk.FlexPath([(0, -1), (5, -10), (10, -1)], 1, datatype=1)
        >>> dilated = gdstk.offset(text + [circle, path], 0.4)
        >>> eroded = gdstk.offset(text + [circle, path], -0.4,
        ...                       use_union=True, layer=1)

        .. image:: ../function/offset.*
           :align: center

    Notes:
        Repetitions are not applied to any elements, except references and
        their contents.
    """

def racetrack(
    center: Point,
    straight_length: float,
    radius: float,
    inner_radius: float = 0,
    vertical: bool = False,
    tolerance: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon:
    """
    racetrack(center, straight_length, radius, inner_radius=0, vertical=False, tolerance=0.01, layer=0, datatype=0) -> gdstk.Polygon

    Create a racetrack shape.

    Args:
        center (coordinate pair or complex): Polygon center.
        straight_length (number): Length of the straight segment.
        radius (number): Radius of the circular arc.
        inner_radius (number): If greater than 0, create a racetrack ring.
        vertical: If ``True``, the racetrack is created vertically.
        tolerance: Tolerance used for calculating the polygonal
          approximation for the circular arcs.
        layer: layer number assigned to this polygon.
        datatype: data type number assigned to this polygon.

    Examples:
        >>> racetrack1 = gdstk.racetrack((0, 0), 8, 5)
        >>> racetrack2 = gdstk.racetrack((18, 0), 8, 5, 3, True)

        .. image:: ../function/racetrack.*
           :align: center
    """

def read_gds(infile: str | Path, unit: float = 0, tolerance: float = 1e-2) -> Library:
    """
    read_gds(infile, unit=0, tolerance=1e-2, filter=None) -> gdstk.Library

    Import a library from a GDSII stream file.

    Args:
        infile (str or pathlib.Path): Name of the input file.
        unit (number): If greater than zero, convert the imported geometry
          to the this unit.
        tolerance (number): Default tolerance for loaded paths.
        filter (iterable of tuples): If not ``None``, only shapes with
          layer and data type in the iterable are read.

    Returns:
        The imported library.

    Examples:
        >>> library = gdstk.read_gds("layout.gds")
        >>> top_cells = library.top_level()
        >>> filtered_lib = gdstk.read_gds("layout.gds", filter={(0, 1)})
    """

def read_oas(infile: str | Path, unit: float = 0, tolerance: float = 1e-2) -> Library:
    """
    read_oas(infile, unit=0, tolerance=1e-2) -> gdstk.Library

    Import a library from an OASIS stream file.

    Args:
        infile (str or pathlib.Path): Name of the input file.
        unit (number): If greater than zero, convert the imported geometry
          to the this unit.
        tolerance (number): Default tolerance for loaded paths.

    Returns:
        The imported library.

    Examples:
        >>> library = gdstk.read_gds("layout.oas")
        >>> top_cells = library.top_level()
    """

def read_rawcells(infile: str | Path) -> dict[str, RawCell]:
    """
    read_rawcells(infile) -> dict

    Load cells form a GDSII file without decoding them.

    Args:
        infile (str or pathlib.Path): Name of the input file.

    Returns:
        Dictionary of :class:`gdstk.RawCell` indexed by name.

    Examples:
        >>> cell1 = gdstk.Cell("CELL_1")
        >>> cell1.add(gdstk.rectangle((0, 0), (2, 1)))
        >>> cell2 = gdstk.Cell("CELL_2")
        >>> cell2.add(gdstk.Reference(cell1, (-1, 0)))
        >>> library = gdstk.Library()
        >>> library.add(cell1, cell2)
        >>> library.write_gds("test.gds")
        >>> raw_cells = gdstk.read_rawcells("test.gds")
        >>> print(raw_cells.keys())
        dict_keys(['CELL_2', 'CELL_1'])
        >>> print(len(raw_cells["CELL_1"].dependencies(True)))
        0
        >>> print(len(raw_cells["CELL_2"].dependencies(True)))
        1
        >>> deps = raw_cells["CELL_2"].dependencies(True)
        >>> print(deps[0] is raw_cells["CELL_1"])
        True
    """

def rectangle(
    corner1: Point, corner2: Point, layer: int = ..., datatype: int = ...
) -> Polygon:
    """
    rectangle(corner1, corner2, layer=0, datatype=0) -> gdstk.Polygon

    Create a rectangle.

    Args:
        corner1 (coordinate pair or complex): First rectangle corner.
        corner2 (coordinate pair or complex): Opposing corner.
        layer: layer number assigned to this polygon.
        datatype: data type number assigned to this polygon.
    """

def regular_polygon(
    center: Point,
    side_length: float,
    sides: int,
    rotation: float = 0,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon:
    """
    regular_polygon(center, side_length, sides, rotation=0, layer=0, datatype=0) -> gdstk.Polygon

    Create a regular polygon.

    Args:
        center (coordinate pair or complex): Polygon center.
        side_length (number): Length of the sides of the polygon.
        sides (integer): Number of polygon sides.
        rotation: Rotation angle (in radians).
        layer: layer number assigned to this polygon.
        datatype: data type number assigned to this polygon.

    Examples:
        >>> poly3 = gdstk.regular_polygon((0, 0), 9, 3)
        >>> poly4 = gdstk.regular_polygon((10, 0), 7, 4, layer=1)
        >>> poly5 = gdstk.regular_polygon((0, 10), 5, 5, layer=2)
        >>> poly6 = gdstk.regular_polygon((10, 10), 4, 6, layer=3)

        .. image:: ../function/regular_polygon.*
           :align: center
    """

def slice(
    polygons: PolygonType | Sequence[PolygonType],
    position: float | Sequence[float],
    axis: Literal["x", "y"],
    precision: float = 1e-3,
) -> list[list[Polygon]]:
    """
    slice(polygons, position, axis, precision=1e-3) -> list

    Slice polygons along x and y axes.

    Args:
        polygons (Polygon, FlexPath, RobustPath, Reference, sequence):
          Polygons to offset. If this is a sequence, each element can be any
          of the polygonal types or a sequence of points (coordinate pairs
          or complex).
        position (number or sequence): Cut positions.
        axis (str): One of "x" or "y". Indicated the axis where positions
          are specified. The cut direction is orthogonal to this axis.
        precision: Desired precision for rounding vertex coordinates.

    Returns:
        List with N + 1 elements, where N is the number of cut positions.
        Each element is a list of polygons obtained between cuts.

    Examples:
        >>> triangle = gdstk.regular_polygon((-10, 0), 8, 3)
        >>> ring = gdstk.ellipse((10, 0), 8, 5, layer=1)
        >>> result = gdstk.slice([triangle, ring], (-10, -5, 0, 6, 14), "x")
        >>> print(len(result))
        6
        >>> print([len(polys) for polys in result])
        [1, 1, 0, 1, 2, 1]

        .. image:: ../function/slice.*
           :align: center

    Notes:
        Repetitions are not applied to any elements, except references and
        their contents.
    """

def text(
    text: str,
    size: float,
    position: Point,
    vertical: bool = False,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]:
    """
    text(text, size, position, vertical=False, layer=0, datatype=0) -> list

    Create polygonal text.

    Args:
        text (str): Text string.
        size (number): Full height of the font.
        position (coordinate pair or complex): Text starting position.
        vertical: Writing direction.
        layer: layer number assigned to the polygons.
        datatype: data type number assigned to the polygons.

    Returns:
        List of :class:`gdstk.Polygon`.

    Examples:
        >>> text = gdstk.text(f"Created with\nGDSTK {gdstk.__version__}", 1,
        ...                   (0, 0))
        >>> rect = gdstk.rectangle((0, -5 / 4), (12 * 9 / 16, 1),
        ...                        datatype=1)

        .. image:: ../function/text.*
           :align: center

    Notes:
        The character aspect ratio is 1:2. For horizontal text, spacings
        between characters and between lines are 9 / 16 and 5 / 4 times the
        full height ``size``, respectively. For vertical text, characters
        and columns are respectively spaced by 9 / 8 and 1 times ``size``.
    """
