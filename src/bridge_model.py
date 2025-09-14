import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class BridgeComponent:
    """
    Represents a single structural component in the digital twin model.
    """
    component_id: str
    component_type: str  # e.g., 'Tower', 'DeckSegment', 'MainCable', 'SuspenderCable'
    geometry: Dict[str, Any]  # e.g., {'position': [x, y, z], 'dimensions': [l, w, h]}
    material: str

# A simplified data model of a suspension bridge.
# This serves as the 'BIM' data for the digital twin.
BRIDGE_MODEL: List[BridgeComponent] = [
    # Main Towers
    BridgeComponent(
        component_id='TWR-N',
        component_type='Tower',
        geometry={'position_base': [50, 0, 0], 'dimensions': [10, 15, 80]},
        material='Concrete'
    ),
    BridgeComponent(
        component_id='TWR-S',
        component_type='Tower',
        geometry={'position_base': [450, 0, 0], 'dimensions': [10, 15, 80]},
        material='Concrete'
    ),
    # Deck Segments (modeling as one continuous segment for simplicity)
    BridgeComponent(
        component_id='DECK-MAIN',
        component_type='DeckSegment',
        geometry={'start_point': [0, 0, 20], 'dimensions': [500, 20, 2]},
        material='Steel'
    ),
    # Main Suspension Cables
    BridgeComponent(
        component_id='CBL-M-E',
        component_type='MainCable',
        geometry={'start_anchor': [0, 5, 22], 'end_anchor': [500, 5, 22], 'tower_saddles': [[50, 5, 80], [450, 5, 80]], 'sag_midpoint': 40},
        material='Steel'
    ),
    BridgeComponent(
        component_id='CBL-M-W',
        component_type='MainCable',
        geometry={'start_anchor': [0, -5, 22], 'end_anchor': [500, -5, 22], 'tower_saddles': [[50, -5, 80], [450, -5, 80]], 'sag_midpoint': 40},
        material='Steel'
    ),
    # A few representative vertical suspender cables
    BridgeComponent(
        component_id='CBL-V-N1',
        component_type='SuspenderCable',
        geometry={'main_cable_connection': [150, 5, 55], 'deck_connection': [150, 5, 21]},
        material='Steel'
    ),
    BridgeComponent(
        component_id='CBL-V-S1',
        component_type='SuspenderCable',
        geometry={'main_cable_connection': [350, 5, 55], 'deck_connection': [350, 5, 21]},
        material='Steel'
    ),
]

def get_component_by_id(component_id: str) -> BridgeComponent | None:
    """Finds a bridge component by its unique ID."""
    for component in BRIDGE_MODEL:
        if component.component_id == component_id:
            return component
    return None
