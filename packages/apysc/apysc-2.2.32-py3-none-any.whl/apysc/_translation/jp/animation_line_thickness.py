"""This module is for the translation mapping data of the
following document:

Document file: animation_line_thickness.md
Language: jp
"""

from typing import Dict

MAPPING: Dict[str, str] = {

    '# animation_line_thickness interface':
    '# animation_line_thickness インターフェイス',

    'This page explains the `animation_line_thickness` method interface.':
    'このページでは`animation_line_thickness`メソッドのインターフェイスについて説明します。',

    '## What interface is this?':
    '## インターフェイス概要',

    'The `animation_line_thickness` method interface creates an `ap.AnimationLineThickness` instance. You can animate line thickness with it.':  # noqa
    '`animation_line_thickness`メソッドのインターフェイスは`ap.AnimationLineThickness`クラスのインスタンスを生成します。そのインスタンスを使用して線幅のアニメーションを設定することができます。',  # noqa

    'This interface exists on a `GraphicsBase` subclass, such as the `Rectangle` or `Circle` class.':  # noqa
    'このインターフェイスは`Rectangle`や`Circle`クラスなどの`GraphicsBase`のサブクラスで存在します。',

    '## Basic usage':
    '## 基本的な使い方',

    'The following example sets the line thickness animation (from 1 to 10) with the `animation_line_thickness` method:':  # noqa
    '以下のコード例では1～10の線幅のアニメーションを`animation_line_thickness`メソッドを使って設定しています。',

    '```py\n# runnable\nimport apysc as ap\n\nDURATION: int = 1000\n\n\ndef on_animation_complete_1(\n        e: ap.AnimationEvent[ap.Rectangle], options: dict) -> None:\n    """\n    The handler that the animation calls when its end.\n\n    Parameters\n    ----------\n    e : AnimationEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = e.this.target\n    rectangle.animation_line_thickness(\n        thickness=1, duration=DURATION,\n    ).animation_complete(on_animation_complete_2).start()\n\n\ndef on_animation_complete_2(\n        e: ap.AnimationEvent[ap.Rectangle], options: dict) -> None:\n    """\n    The handler that the animation calls when its end.\n\n    Parameters\n    ----------\n    e : AnimationEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = e.this.target\n    rectangle.animation_line_thickness(\n        thickness=10, duration=DURATION,\n    ).animation_complete(on_animation_complete_1).start()\n\n\nap.Stage(\n    stage_width=150, stage_height=150,\n    background_color=\'#333\', stage_elem_id=\'stage\')\nsprite: ap.Sprite = ap.Sprite()\nsprite.graphics.line_style(color=\'#eee\', thickness=1)\nrectangle: ap.Rectangle = sprite.graphics.draw_rect(\n    x=50, y=50, width=50, height=50)\nrectangle.animation_line_thickness(\n    thickness=10, duration=DURATION,\n).animation_complete(on_animation_complete_1).start()\n\nap.save_overall_html(\n    dest_dir_path=\'./animation_line_thickness_basic_usage/\')\n```':  # noqa
    '```py\n# runnable\nimport apysc as ap\n\nDURATION: int = 1000\n\n\ndef on_animation_complete_1(\n        e: ap.AnimationEvent[ap.Rectangle], options: dict) -> None:\n    """\n    The handler that the animation calls when its end.\n\n    Parameters\n    ----------\n    e : AnimationEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = e.this.target\n    rectangle.animation_line_thickness(\n        thickness=1, duration=DURATION,\n    ).animation_complete(on_animation_complete_2).start()\n\n\ndef on_animation_complete_2(\n        e: ap.AnimationEvent[ap.Rectangle], options: dict) -> None:\n    """\n    The handler that the animation calls when its end.\n\n    Parameters\n    ----------\n    e : AnimationEvent\n        Event instance.\n    options : dict\n        Optional arguments dictionary.\n    """\n    rectangle: ap.Rectangle = e.this.target\n    rectangle.animation_line_thickness(\n        thickness=10, duration=DURATION,\n    ).animation_complete(on_animation_complete_1).start()\n\n\nap.Stage(\n    stage_width=150, stage_height=150,\n    background_color=\'#333\', stage_elem_id=\'stage\')\nsprite: ap.Sprite = ap.Sprite()\nsprite.graphics.line_style(color=\'#eee\', thickness=1)\nrectangle: ap.Rectangle = sprite.graphics.draw_rect(\n    x=50, y=50, width=50, height=50)\nrectangle.animation_line_thickness(\n    thickness=10, duration=DURATION,\n).animation_complete(on_animation_complete_1).start()\n\nap.save_overall_html(\n    dest_dir_path=\'./animation_line_thickness_basic_usage/\')\n```',  # noqa

    '## animation_line_thickness API':
    '## animation_line_thickness API',

    '<span class="inconspicuous-txt">Note: the document build script generates and updates this API document section automatically. Maybe this section is duplicated compared with previous sections.</span>':  # noqa
    '<span class="inconspicuous-txt">特記事項: このAPIドキュメントはドキュメントビルド用のスクリプトによって自動で生成・同期されています。そのためもしかしたらこの節の内容は前節までの内容と重複している場合があります。</span>',  # noqa

    '**[Interface summary]** Set the line thickness animation setting.<hr>':
    '**[インターフェイス概要]** 線幅のアニメーションを設定します。<hr>',

    '**[Parameters]**':
    '**[引数]**',

    '- `thickness`: Int or int':
    '- `thickness`: Int or int',

    '  - The final line thickness of the animation.':
    '  - 線幅のアニメーションの最終値。',

    '- `duration`: Int or int, default 3000':
    '- `duration`: Int or int, default 3000',

    '  - Milliseconds before an animation ends.':
    '  - アニメーション完了までのミリ秒。',

    '- `delay`: Int or int, default 0':
    '- `delay`: Int or int, default 0',

    '  - Milliseconds before an animation starts.':
    '  - アニメーション開始までの遅延時間のミリ秒。',

    '- `easing`: Easing, default Easing.LINEAR':
    '- `easing`: Easing, default Easing.LINEAR',

    '  - Easing setting.':
    '  - イージング設定。',

    '<hr>':
    '<hr>',

    '**[Returns]**':
    '**[返却値]**',

    '- `animation_line_thickness`: AnimationLineThickness':
    '- `animation_line_thickness`: AnimationLineThickness',

    '  - Created animation setting instance.':
    '  - 生成されたアニメーションのインスタンス。',

    '<hr>':
    '<hr>',

    '**[Notes]**':
    '**[特記事項]**',

    'To start this animation, you need to call the `start` method of the returned instance.<hr>':  # noqa
    'アニメーションを開始するには返却されたインスタンスの`start`メソッドを呼び出す必要があります。<hr>',

    '**[Examples]**':
    '**[コードサンプル]**',

    '```py\n>>> import apysc as ap\n>>> stage: ap.Stage = ap.Stage()\n>>> sprite: ap.Sprite = ap.Sprite()\n>>> sprite.graphics.begin_fill(color=\'#0af\')\n>>> sprite.graphics.line_style(\n...     color=\'#fff\', thickness=1)\n>>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(\n...     x=50, y=50, width=50, height=50)\n>>> _ = rectangle.animation_line_thickness(\n...     thickness=6,\n...     duration=1500,\n...     easing=ap.Easing.EASE_OUT_QUINT,\n... ).start()\n```':  # noqa
    '```py\n>>> import apysc as ap\n>>> stage: ap.Stage = ap.Stage()\n>>> sprite: ap.Sprite = ap.Sprite()\n>>> sprite.graphics.begin_fill(color=\'#0af\')\n>>> sprite.graphics.line_style(\n...     color=\'#fff\', thickness=1)\n>>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(\n...     x=50, y=50, width=50, height=50)\n>>> _ = rectangle.animation_line_thickness(\n...     thickness=6,\n...     duration=1500,\n...     easing=ap.Easing.EASE_OUT_QUINT,\n... ).start()\n```',  # noqa

    '<hr>':
    '<hr>',

    '**[References]**':
    '**[関連資料]**',

    '- [Animation interfaces duration setting document](https://simon-ritchie.github.io/apysc/en/animation_duration.html)':  # noqa
    '- [各アニメーションインターフェイスの duration （アニメーション時間）設定](https://simon-ritchie.github.io/apysc/en/jp_animation_duration.html)',  # noqa

    '- [Animation interfaces delay setting document](https://simon-ritchie.github.io/apysc/en/animation_delay.html)':  # noqa
    '- [各アニメーションインターフェイスの delay （遅延時間）設定](https://simon-ritchie.github.io/apysc/en/jp_animation_delay.html)',  # noqa

    '- [Each animation interface return value document](https://simon-ritchie.github.io/apysc/en/animation_return_value.html)':  # noqa
    '- [各アニメーションインターフェイスの返却値](https://simon-ritchie.github.io/apysc/en/jp_animation_return_value.html)',  # noqa

    '- [Sequential animation setting document](https://simon-ritchie.github.io/apysc/en/sequential_animation.html)':  # noqa
    '- [連続したアニメーション設定](https://simon-ritchie.github.io/apysc/en/jp_sequential_animation.html)',  # noqa

    '- [animation_parallel interface document](https://simon-ritchie.github.io/apysc/en/animation_parallel.html)':  # noqa
    '- [animation_parallel （並列アニメーション設定）のインターフェイス](https://simon-ritchie.github.io/apysc/en/jp_animation_parallel.html)',  # noqa

    '- [Easing enum document](https://simon-ritchie.github.io/apysc/en/easing_enum.html)':  # noqa
    '- [イージングのenum](https://simon-ritchie.github.io/apysc/en/jp_easing_enum.html)',  # noqa

}
