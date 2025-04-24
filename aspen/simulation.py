import os
import logging
import json
from typing import Dict, Any, List, Tuple, Optional
from .interface import AspenPlusInterface
from ..models.materials import RawMaterial, RawMaterialsList
from ..models.specifications import ProductSpecification, ProductSpecificationsList

logger = logging.getLogger(__name__)

class ProcessSimulation:
    """Class responsible for building and running chemical process simulations."""
    
    def __init__(self, aspen_path: str, template_path: Optional[str] = None):
        """Initialize the process simulation.
        
        Args:
            aspen_path: Path to Aspen Plus executable
            template_path: Optional path to a template simulation file
        """
        self.aspen = AspenPlusInterface(aspen_path)
        self.template_path = template_path
        self.simulation_path = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize the simulation environment."""
        if self.aspen.initialize():
            if self.aspen.load_simulation(self.template_path):
                self.initialized = True
                return True
        return False
    
    def setup_materials(self, materials: RawMaterialsList) -> bool:
        """Set up the raw materials in the simulation."""
        if not self.initialized:
            logger.error("Simulation not initialized")
            return False
            
        try:
            # Add components to simulation
            for material in materials.materials:
                self.aspen.add_component(material.name, material.chemical_formula)
                
            # Set property method - using a default here
            self.aspen.set_property_method("NRTL")
            
            # Create feed streams
            for i, material in enumerate(materials.materials):
                stream_id = f"FEED_{i+1}"
                
                # Prepare stream data
                stream_data = {
                    "temperature": material.temperature or 298.15,  # Default to 25°C
                    "pressure": material.pressure or 101325,  # Default to 1 atm
                    "composition": {material.name: material.amount or 100}  # Default amount
                }
                
                # Add the stream
                self.aspen.add_stream(stream_id, stream_data)
                
            return True
        except Exception as e:
            logger.error(f"Error setting up materials: {str(e)}")
            return False
    
    def build_process(self, process_design: Dict[str, Any]) -> bool:
        """Build a process based on the provided design."""
        if not self.initialized:
            logger.error("Simulation not initialized")
            return False
            
        try:
            # Add unit operations
            for unit_id, unit_data in process_design.get("units", {}).items():
                unit_type = unit_data.get("type")
                params = unit_data.get("parameters", {})
                self.aspen.add_unit_operation(unit_type, unit_id, params)
            
            # Connect blocks with streams
            for connection in process_design.get("connections", []):
                source = connection.get("source")
                destination = connection.get("destination")
                stream_id = connection.get("stream")
                self.aspen.connect_blocks(source, destination, stream_id)
            
            return True
        except Exception as e:
            logger.error(f"Error building process: {str(e)}")
            return False
    
    def run(self) -> Tuple[bool, Dict[str, Any]]:
        """Run the simulation and get results."""
        if not self.initialized:
            logger.error("Simulation not initialized")
            return False, {}
            
        try:
            # Run the simulation
            if self.aspen.run_simulation():
                # Get results
                results = self.aspen.get_simulation_results()
                return True, results
            else:
                return False, {}
        except Exception as e:
            logger.error(f"Error running simulation: {str(e)}")
            return False, {}
    
    def save(self, file_path: str) -> bool:
        """Save the current simulation."""
        if not self.initialized:
            logger.error("Simulation not initialized")
            return False
            
        try:
            return self.aspen.save_simulation(file_path)
        except Exception as e:
            logger.error(f"Error saving simulation: {str(e)}")
            return False
    
    def close(self):
        """Close the simulation."""
        if self.initialized:
            self.aspen.close()
            self.initialized = False