from typing import *
from .base_component import BaseComponent
from .exact_literal import ExactLiteral
import random


class OneOf(BaseComponent):
    def __init__(self, components: Sequence[BaseComponent|str], weights: Optional[Sequence[float]] = None) -> None:        
        self.components = self._parse_components(components)
        self.weights = weights

    def _parse_components(self, components: Sequence[BaseComponent|str]) -> Sequence[BaseComponent]:
        parsed_components = list()
        for component in components:
            if isinstance(component, str):
                parsed_components.append(ExactLiteral(component))
                continue
            if not isinstance(component, BaseComponent):
                raise TypeError(f"component has to be of type 'BaseComponent' or 'str', not '{component.__class__.__name__}'")
            parsed_components.append(component)
        return parsed_components

    def generate(self) -> str:
        return random.choices(self.components, weights=self.weights, k=1)[0].generate()

    def validate(self, sub_id: str) -> bool:
        return any(map(lambda component: component.validate(sub_id) , self.components))
    
    def reduce_all_matching(self, sub_id: str) -> Iterator[str]:
        for component in self.components:
            yield from component.reduce_all_matching(sub_id)
