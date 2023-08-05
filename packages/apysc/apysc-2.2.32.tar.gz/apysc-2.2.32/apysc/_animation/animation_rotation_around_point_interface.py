"""Class implementation for the animation_rotation_around_point
interface.
"""

from typing import Union

from apysc._animation.animation_interface_base import AnimationInterfaceBase
from apysc._animation.animation_rotation_around_point import (
    AnimationRotationAroundPoint,
)
from apysc._animation.easing import Easing
from apysc._type.int import Int
from apysc._validation import arg_validation_decos


class AnimationRotationAroundPointInterface(AnimationInterfaceBase):
    @arg_validation_decos.is_integer(arg_position_index=1)
    @arg_validation_decos.is_integer(arg_position_index=2)
    @arg_validation_decos.is_integer(arg_position_index=3)
    @arg_validation_decos.is_integer(arg_position_index=4)
    @arg_validation_decos.num_is_gt_zero(arg_position_index=4)
    @arg_validation_decos.is_integer(arg_position_index=5)
    @arg_validation_decos.is_easing(arg_position_index=6)
    def animation_rotation_around_point(
        self,
        *,
        rotation_around_point: Union[int, Int],
        x: Union[int, Int],
        y: Union[int, Int],
        duration: Union[int, Int] = 3000,
        delay: Union[int, Int] = 0,
        easing: Easing = Easing.LINEAR
    ) -> AnimationRotationAroundPoint:
        """
        Set the rotation around the given point animation setting.

        Notes
        -----
        To start this animation, you need to call the `start` method of
        the returned instance.

        Parameters
        ----------
        rotation_around_point : Int or int
            The final rotation of the animation.
        x : Int or int
            X-coordinate.
        y : Int or int
            Y-coordinate.
        duration : Int or int, default 3000
            Milliseconds before an animation ends.
        delay : Int or int, default 0
            Milliseconds before an animation starts.
        easing : Easing, default Easing.LINEAR
            Easing setting.

        Returns
        -------
        animation_rotation_around_point : AnimationRotationAroundPoint
            Created animation setting instance.

        References
        ----------
        - animation_rotation_around_point interface document
            - https://simon-ritchie.github.io/apysc/en/animation_rotation_around_point.html  # noqa
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
        >>> _ = rectangle.animation_rotation_around_point(
        ...     rotation_around_point=90,
        ...     x=ap.Int(100),
        ...     y=ap.Int(100),
        ...     duration=1500,
        ...     easing=ap.Easing.EASE_OUT_QUINT,
        ... ).start()
        """
        animation_rotation_around_point: AnimationRotationAroundPoint = (
            AnimationRotationAroundPoint(
                target=self,
                rotation_around_point=rotation_around_point,
                x=x,
                y=y,
                duration=duration,
                delay=delay,
                easing=easing,
            )
        )
        return animation_rotation_around_point
