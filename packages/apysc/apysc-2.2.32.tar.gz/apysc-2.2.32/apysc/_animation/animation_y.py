"""Class implementation for the y animation value.
"""

from typing import Generic
from typing import TypeVar
from typing import Union

from apysc._animation.animation_base import AnimationBase
from apysc._animation.easing import Easing
from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.int import Int
from apysc._type.variable_name_interface import VariableNameInterface

_T = TypeVar("_T", bound=VariableNameInterface)


class AnimationY(AnimationBase[_T], Generic[_T]):
    """
    The animation class for a y-coordinate.

    References
    ----------
    - animation_y interface document
        - https://simon-ritchie.github.io/apysc/en/animation_y.html
    - Animation interfaces duration setting document
        - https://simon-ritchie.github.io/apysc/en/animation_duration.html
    - Animation interfaces delay setting document
        - https://simon-ritchie.github.io/apysc/en/animation_delay.html
    - Each animation interface return value document
        - https://simon-ritchie.github.io/apysc/en/animation_return_value.html  # noqa
    - Sequential animation setting document
        - https://simon-ritchie.github.io/apysc/en/sequential_animation.html
    - animation_parallel interface document
        - https://simon-ritchie.github.io/apysc/en/animation_parallel.html
    - Easing enum document
        - https://simon-ritchie.github.io/apysc/en/easing_enum.html

    Examples
    --------
    >>> import apysc as ap
    >>> stage: ap.Stage = ap.Stage()
    >>> sprite: ap.Sprite = ap.Sprite()
    >>> sprite.graphics.begin_fill(color='#0af')
    >>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(
    ...     x=50, y=50, width=50, height=50)
    >>> animation: ap.AnimationY = rectangle.animation_y(
    ...     y=100,
    ...     duration=1500,
    ...     easing=ap.Easing.EASE_OUT_QUINT,
    ... )
    >>> _ = animation.start()
    """

    _y: Int

    @add_debug_info_setting(module_name=__name__)
    def __init__(
        self,
        *,
        target: _T,
        y: Union[int, Int],
        duration: Union[int, Int] = 3000,
        delay: Union[int, Int] = 0,
        easing: Easing = Easing.LINEAR,
    ) -> None:
        """
        The animation class for a y-coordinate.

        Parameters
        ----------
        target : VariableNameInterface
            A target instance of the animation target
            (e.g., `DisplayObject` instance).
        y : int or Int
            Destination of the y-coordinate.
        duration : int or Int, default 3000
            Milliseconds before an animation ends.
        delay : int or Int, default 0
            Milliseconds before an animation starts.
        easing : Easing, default Easing.LINEAR
            Easing setting.
        """
        from apysc._converter import to_apysc_val_from_builtin
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names

        variable_name: str = expression_variables_util.get_next_variable_name(
            type_name=var_names.ANIMATION_Y
        )
        self._y = to_apysc_val_from_builtin.get_copied_int_from_builtin_val(integer=y)
        self._set_basic_animation_settings(
            target=target, duration=duration, delay=delay, easing=easing
        )
        super(AnimationY, self).__init__(variable_name=variable_name)

    def _get_animation_func_expression(self) -> str:
        """
        Get a animation function expression.

        Returns
        -------
        expression : str
            Animation function expression.
        """
        from apysc._type import value_util

        y_str: str = value_util.get_value_str_for_expression(value=self._y)
        return f"\n  .y({y_str});"

    def _get_complete_event_in_handler_head_expression(self) -> str:
        """
        Get an expression to insert into the complete event
        handler's head.

        Returns
        -------
        expression : str
            An expression to insert into the complete event
            handler's head.
        """
        from apysc._display.y_interface import YInterface

        expression: str = ""
        if isinstance(self._target, YInterface):
            self._target._initialize_y_if_not_initialized()
            expression = (
                f"{self._target._y.variable_name} = " f"{self._y.variable_name};"
            )
        return expression
