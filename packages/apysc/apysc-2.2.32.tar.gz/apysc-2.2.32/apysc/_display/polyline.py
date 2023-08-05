"""Implementations of Polyline class.
"""


from typing import List
from typing import Optional as Op
from typing import Union

from apysc._display import graphics
from apysc._display.append_line_point_interface import AppendLinePointInterface
from apysc._display.child_interface import ChildInterface
from apysc._display.fill_alpha_interface import FillAlphaInterface
from apysc._display.fill_color_interface import FillColorInterface
from apysc._display.graphics_base import GraphicsBase
from apysc._display.line_caps import LineCaps
from apysc._display.line_dash_dot_setting import LineDashDotSetting
from apysc._display.line_dash_setting import LineDashSetting
from apysc._display.line_dot_setting import LineDotSetting
from apysc._display.line_joints import LineJoints
from apysc._display.line_round_dot_setting import LineRoundDotSetting
from apysc._display.set_x_and_y_with_minimum_point_interface_base import (
    SetXAndYWithMinimumPointInterfaceBase,
)
from apysc._display.x_interface import XInterface
from apysc._display.y_interface import YInterface
from apysc._geom.point2d import Point2D
from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.array import Array
from apysc._type.int import Int
from apysc._type.number import Number
from apysc._type.string import String
from apysc._type.variable_name_suffix_interface import VariableNameSuffixInterface
from apysc._validation import arg_validation_decos


class Polyline(
    XInterface,
    YInterface,
    GraphicsBase,
    AppendLinePointInterface,
    SetXAndYWithMinimumPointInterfaceBase,
    FillColorInterface,
    FillAlphaInterface,
    VariableNameSuffixInterface,
):
    """
    The polyline vector graphics class.

    References
    ----------
    - Polyline class document
        - https://simon-ritchie.github.io/apysc/en/polyline.html
    - Graphics move_to and line_to interfaces document
        - https://simon-ritchie.github.io/apysc/en/graphics_move_to_and_line_to.html  # noqa

    Examples
    --------
    >>> import apysc as ap
    >>> stage: ap.Stage = ap.Stage()
    >>> sprite: ap.Sprite = ap.Sprite()
    >>> sprite.graphics.line_style(color='#fff', thickness=5)
    >>> _ = sprite.graphics.move_to(x=50, y=50)
    >>> polyline: ap.Polyline = sprite.graphics.line_to(x=150, y=50)
    >>> polyline.line_color
    String('#ffffff')

    >>> polyline.line_thickness
    Int(5)
    """

    # self
    @arg_validation_decos.multiple_line_settings_are_not_set(arg_position_index=0)
    # points
    @arg_validation_decos.is_point_2ds(arg_position_index=1)
    # fill_color
    @arg_validation_decos.is_hex_color_code_format(arg_position_index=2)
    # fill_alpha
    @arg_validation_decos.num_is_0_to_1_range(arg_position_index=3)
    # line_color
    @arg_validation_decos.is_hex_color_code_format(arg_position_index=4)
    # line_alpha
    @arg_validation_decos.num_is_0_to_1_range(arg_position_index=5)
    # line_thickness
    @arg_validation_decos.is_integer(arg_position_index=6)
    @arg_validation_decos.num_is_gte_zero(arg_position_index=6)
    # line_cap
    @arg_validation_decos.is_line_cap(arg_position_index=7, optional=True)
    # line_joints
    @arg_validation_decos.is_line_joints(arg_position_index=8, optional=True)
    # line_dot_setting
    @arg_validation_decos.is_line_dot_setting(arg_position_index=9)
    # line_dash_setting
    @arg_validation_decos.is_line_dash_setting(arg_position_index=10)
    # line_round_dot_setting
    @arg_validation_decos.is_line_round_dot_setting(arg_position_index=11)
    # line_dash_dot_setting
    @arg_validation_decos.is_line_dash_dot_setting(arg_position_index=12)
    # parent
    @arg_validation_decos.is_display_object_container(
        arg_position_index=13, optional=True
    )
    # variable_name_suffix
    @arg_validation_decos.is_builtin_string(arg_position_index=14, optional=False)
    @add_debug_info_setting(module_name=__name__)
    def __init__(
        self,
        *,
        points: Union[Array[Point2D], List[Point2D]],
        fill_color: Union[str, String] = "",
        fill_alpha: Union[float, Number] = 1.0,
        line_color: Union[str, String] = "",
        line_alpha: Union[float, Number] = 1.0,
        line_thickness: Union[int, Int] = 1,
        line_cap: Op[Union[String, LineCaps]] = None,
        line_joints: Op[Union[String, LineJoints]] = None,
        line_dot_setting: Op[LineDotSetting] = None,
        line_dash_setting: Op[LineDashSetting] = None,
        line_round_dot_setting: Op[LineRoundDotSetting] = None,
        line_dash_dot_setting: Op[LineDashDotSetting] = None,
        parent: Op[ChildInterface] = None,
        variable_name_suffix: str = "",
    ) -> None:
        """
        Create a polyline vector graphic.

        Parameters
        ----------
        points : Array of Point2D or list of Point2D
            List of line points.
        fill_color : str or String, default ''
            A fill-color to set.
        fill_alpha : float or Number, default 1.0
            A fill-alpha to set.
        line_color : str or String, default ''
            A line-color to set.
        line_alpha : float or Number, default 1.0
            A line-alpha to set.
        line_thickness : int or Int, default 1
            A line-thickness (line-width) to set.
        line_cap : String or LineCaps or None, default None
            A line-cap setting to set.
        line_joints : String or LineJoints or None, default None
            A line-joints setting to set.
        line_dot_setting : LineDotSetting or None, default None
            A dot setting to set.
        line_dash_setting : LineDashSetting or None, default None
            A dash setting to set.
        line_round_dot_setting : LineRoundDotSetting or None, default None
            A round-dot setting to set.
        line_dash_dot_setting : LineDashDotSetting or None, default None
            A dash dot (1-dot chain) setting to set.
        parent : ChildInterface or None, default None
            A parent instance to add this instance.
            If a specified value is None, this interface uses
            a stage instance.
        variable_name_suffix : str, default ''
            A JavaScript variable name suffix string.
            This setting is sometimes useful for JavaScript's debugging.

        References
        ----------
        - Polyline class document
            - https://simon-ritchie.github.io/apysc/en/polyline.html

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> polyline: ap.Polyline = ap.Polyline(
        ...     points=[
        ...         ap.Point2D(x=50, y=50),
        ...         ap.Point2D(x=100, y=100),
        ...         ap.Point2D(x=150, y=50),
        ...     ],
        ...     line_color='#ffffff',
        ...     line_thickness=3)
        >>> polyline.line_color
        String('#ffffff')
        >>> polyline.line_thickness
        Int(3)
        """
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names

        self._variable_name_suffix = variable_name_suffix
        if isinstance(points, list):
            points = Array(points, variable_name_suffix=self._variable_name_suffix)
        variable_name: str = expression_variables_util.get_next_variable_name(
            type_name=var_names.POLYLINE
        )
        self.variable_name = variable_name
        self.points = points
        self._set_initial_basic_values(
            fill_color=fill_color,
            fill_alpha=fill_alpha,
            line_color=line_color,
            line_thickness=line_thickness,
            line_alpha=line_alpha,
            line_cap=line_cap,
            line_joints=line_joints,
        )
        self._append_constructor_expression()
        self._set_line_setting_if_not_none_value_exists(
            line_dot_setting=line_dot_setting,
            line_dash_setting=line_dash_setting,
            line_round_dot_setting=line_round_dot_setting,
            line_dash_dot_setting=line_dash_dot_setting,
        )
        self._set_x_and_y_with_minimum_point()
        super(Polyline, self).__init__(parent=parent, variable_name=variable_name)

    def _set_x_and_y_with_minimum_point(self) -> None:
        """
        Set an x and y properties coordinate with a minimum point.
        """
        min_x: int = min([point._x._value for point in self._points._value])
        min_y: int = min([point._y._value for point in self._points._value])

        suffix: str = self._get_attr_variable_name_suffix(attr_identifier="x")
        self._x = Int(min_x, variable_name_suffix=suffix)

        suffix = self._get_attr_variable_name_suffix(attr_identifier="y")
        self._y = Int(min_y, variable_name_suffix=suffix)

    @classmethod
    def _create_with_graphics(
        cls,
        *,
        graphics: "graphics.Graphics",
        points: Union[Array[Point2D], List[Point2D]],
        variable_name_suffix: str = "",
    ) -> "Polyline":
        """
        Create a polyline instance with the instance of
        specified graphics.

        Parameters
        ----------
        graphics : Graphics
            Graphics instance to link this instance.
        points : Array of Point2D or list of Point2D
            List of line points.
        variable_name_suffix : str, default ''
            A JavaScript variable name suffix string.
            This setting is sometimes useful for JavaScript's debugging.

        Returns
        -------
        polyline : Polyline
            A created polyline instance.
        """
        polyline: Polyline = Polyline(
            points=points,
            fill_color=graphics._fill_color,
            fill_alpha=graphics._fill_alpha,
            line_color=graphics._line_color,
            line_alpha=graphics._line_alpha,
            line_thickness=graphics._line_thickness,
            line_cap=graphics._line_cap,
            line_joints=graphics._line_joints,
            line_dot_setting=graphics._line_dot_setting,
            line_dash_setting=graphics._line_dash_setting,
            line_round_dot_setting=graphics._line_round_dot_setting,
            line_dash_dot_setting=graphics._line_dash_dot_setting,
            parent=graphics,
            variable_name_suffix=variable_name_suffix,
        )
        return polyline

    def __repr__(self) -> str:
        """
        Get a string representation of this instance (for the sake of
        debugging).

        Returns
        -------
        repr_str : str
            Type name and variable name will be set
            (e.g., `Polyline('<variable_name>')`).
        """
        repr_str: str = f"Polyline('{self.variable_name}')"
        return repr_str

    @add_debug_info_setting(module_name=__name__)
    def _append_constructor_expression(self) -> None:
        """
        Append constructor expression.
        """
        import apysc as ap

        stage: ap.Stage = ap.get_stage()
        points_var_name: str
        points_expression: str
        points_var_name, points_expression = self._make_2dim_points_expression()
        expression: str = (
            f"{points_expression}"
            f"\nvar {self.variable_name} = {stage.variable_name}"
            f"\n  .polyline({points_var_name})"
            "\n  .attr({"
        )
        expression = self._append_basic_vals_expression(
            expression=expression, indent_num=2
        )
        expression += "\n  });"
        ap.append_js_expression(expression=expression)
        self._points_var_name = points_var_name
