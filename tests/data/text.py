"""
Тексты для тестов.
"""


dirty = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit.§Officia, animi culpa saepe dolorum quis assumenda neque laborum numquam illo 
officiis dignissimos eos asperiores maxime harum et. Voluptatum eligendi, non incidunt.
∙Lorem ipsum dolor sit amet, consectetur adipisicing elit.
‣Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
⁃Lorem ipsum dolor sit amet, consectetur adipisicing elit.
⁌Lorem ipsum dolor sit amet, consectetur adipisicing elit.
⁍Lorem ipsum dolor sit amet, consectetur adipisicing elit.
◦Lorem ipsum dolor sit amet, consectetur adipisicing elit.
¶Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
Odit amet deserunt consequatur dicta, impedit nobis optio enim praesentium minima cupiditate 
dolores officiis atque officia dolor, non molestias repellat, omnis accusamus?
"""


cleaned = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit.
Officia, animi culpa saepe dolorum quis assumenda neque laborum numquam illo 
officiis dignissimos eos asperiores maxime harum et. Voluptatum eligendi, non incidunt.

Lorem ipsum dolor sit amet, consectetur adipisicing elit.

Lorem ipsum dolor sit amet, consectetur adipisicing elit. 

Lorem ipsum dolor sit amet, consectetur adipisicing elit.

Lorem ipsum dolor sit amet, consectetur adipisicing elit.

Lorem ipsum dolor sit amet, consectetur adipisicing elit.

Lorem ipsum dolor sit amet, consectetur adipisicing elit.

Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
Odit amet deserunt consequatur dicta, impedit nobis optio enim praesentium minima cupiditate 
dolores officiis atque officia dolor, non molestias repellat, omnis accusamus?
"""
