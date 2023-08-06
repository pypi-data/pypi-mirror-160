# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_gearbox', 'manim_gearbox.gear_mobject']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.13.1', 'scipy']

entry_points = \
{'manim.plugins': ['manim_gearbox = manim_gearbox']}

setup_kwargs = {
    'name': 'manim-gearbox',
    'version': '0.2.4',
    'description': 'This is an extension of Manim that helps drawing nice looking gears.',
    'long_description': "# manim-Gearbox\nThis is a plugin for Manim that enables you to draw realistic looking gears and mechanisms.\nMostly based on these tec-science pages:\n[https://www.tec-science.com/mechanical-power-transmission/involute-gear/geometry-of-involute-gears/](https://www.tec-science.com/mechanical-power-transmission/involute-gear/geometry-of-involute-gears/)\n\nCurrently supported Involute gear features:\n- Basic spur gears\n- Inside ring-gears\n- Basic rack\n- Undercutting (gears with fewer than 17 teeth)\n- Profile shifted gears\n- Meshing calculation with distance variation\n\nPlanned further development:\n- Cycloid gears, cycloid rack\n\n\n## Installation\n`manim-gearbox` is a package on pypi, and can be directly installed using pip:\n```\npip install manim-gearbox\n```\nNote: `manim-gearbox` uses, and depends on SciPy and Manim.\n\n## Usage\nMake sure include these two imports at the top of the .py file\n```py\nfrom manim import *\nfrom manim_gearbox import *\n```\nAdd Gear objects, use mesh_to() method to position 2 gears into meshing.\nI tend to use 'fill_opacity=1' and 'stroke_opacity=0' options because the stroke increases the gear size by a couple pixels, and gives the feeling of interference.\n\n# Examples\n\n## 2 basic gears\n\n```py\nclass gear_example(Scene):\n\tdef construct(self):\n\t\t# small gear\n\t\tgear1=Gear(15, stroke_opacity=0, fill_color=WHITE,fill_opacity=1)\n\t\t# larger gear\n\t\tgear2=Gear(25,  stroke_opacity=0, fill_color=RED, fill_opacity=1)\n\t\t# shifting gear1 away from center\n\t\tgear1.shift(-gear1.rp * 1.5 * RIGHT)\n\t\t# position gear2 next to gear1 so that they mesh together\n\t\tgear2.mesh_to(gear1)\n\n\t\tself.add(gear1, gear2)\n\t\tself.play(Rotate(gear1, gear1.pitch_angle, rate_func=linear),\n\t\t\t\t  Rotate(gear2, - gear2.pitch_angle, rate_func=linear),\n\t\t\t\t  run_time=4)\n\t\t\n```\n![involute_gear_example](/media/involute_gear_example.gif)\n\n## inner gear\n\n```py\nclass gear_example_inner(Scene):\n    def construct(self):\n        # smaller gear\n        gear1 = Gear(12, module=1, profile_shift=0.3, stroke_opacity=0, fill_color=WHITE,fill_opacity=1)\n        # larger gear with inner teeth\n        gear2 = Gear(36, module=1, inner_teeth=True, profile_shift=0.1, stroke_opacity=0, fill_color=RED, fill_opacity=1)\n        gear1.shift(gear1.rp * UP)\n        gear2.shift(gear2.rp * UP)\n        # mesh with 0.15*module larger distance than default\n        # bias param is used to define left or right tooth flank shall engage if there is offset and play\n        gear2.mesh_to(gear1,offset=0.15,bias=False)\n\n        self.add(gear1)\n        self.add(gear2)\n        self.play(Rotate(gear1, gear1.pitch_angle, rate_func=linear),\n                  Rotate(gear2, gear2.pitch_angle, rate_func=linear),\n                  run_time=10)\n\n```\n![inner_gear_example](/media/inner_gear_example.gif)\n",
    'author': 'GarryBGoode',
    'author_email': 'bgeri91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GarryBGoode/manim-GearBox',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
