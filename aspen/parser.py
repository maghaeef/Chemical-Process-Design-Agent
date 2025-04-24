from typing import Dict, Any, List, Optional
from ..models.specifications import ProductSpecification, ProductSpecificationsList

class SimulationResultParser:
    """Parser for analyzing simulation results."""
    
    @staticmethod
    def extract_product_properties(results: Dict[str, Any], product_streams: List[str]) -> Dict[str, Dict[str, Any]]:
        """Extract product properties from simulation results.
        
        Args:
            results: The simulation results dictionary
            product_streams: List of stream IDs that are considered products
            
        Returns:
            Dictionary mapping product stream IDs to their properties
        """
        product_properties = {}
        
        for stream_id in product_streams:
            if stream_id in results:
                stream_data = results[stream_id]
                
                # Extract the basic properties
                properties = {
                    "temperature": stream_data.get("temperature"),
                    "pressure": stream_data.get("pressure"),
                    "state": "vapor" if stream_data.get("vapor_fraction", 0) > 0.99 else 
                             "liquid" if stream_data.get("vapor_fraction", 0) < 0.01 else
                             "mixed",
                }
                
                # Extract composition and calculate purity
                composition = stream_data.get("composition", {})
                if composition:
                    total_flow = sum(composition.values())
                    mass_fractions = {comp: flow/total_flow for comp, flow in composition.items() if total_flow > 0}
                    
                    # Find the main component (highest mass fraction)
                    main_component = max(mass_fractions.items(), key=lambda x: x[1]) if mass_fractions else (None, 0)
                    
                    properties["composition"] = mass_fractions
                    properties["main_component"] = main_component[0]
                    properties["purity"] = main_component[1]
                
                product_properties[stream_id] = properties
        
        return product_properties
    
    @staticmethod
    def check_specifications(
        product_properties: Dict[str, Dict[str, Any]], 
        specifications: ProductSpecificationsList
    ) -> Dict[str, Dict[str, bool]]:
        """Check if products meet specifications.
        
        Args:
            product_properties: Dictionary of product properties
            specifications: Product specifications
            
        Returns:
            Dictionary mapping product names to dictionaries of specification results
        """
        specification_results = {}
        
        # Create a lookup dictionary for specifications by name
        spec_dict = {spec.name: spec for spec in specifications.specifications}
        
        for stream_id, properties in product_properties.items():
            # Extract the main component name
            product_name = properties.get("main_component")
            
            if product_name and product_name in spec_dict:
                # Check if the product meets its specifications
                spec = spec_dict[product_name]
                results = spec.is_satisfied_by(properties)
                specification_results[product_name] = results
        
        return specification_results
    
    @staticmethod
    def check_mass_balance(results: Dict[str, Any]) -> Dict[str, float]:
        """Check mass balance across the simulation.
        
        Args:
            results: Simulation results
            
        Returns:
            Dictionary with mass balance errors for components
        """
        # Find all streams
        streams = [stream_id for stream_id in results if isinstance(results[stream_id], dict) and "composition" in results[stream_id]]
        
        # Categorize streams as inputs or outputs based on naming convention
        # This is a simplified approach and might need to be adjusted
        input_streams = [s for s in streams if s.startswith("FEED")]
        output_streams = [s for s in streams if s.startswith("PRODUCT") or s not in input_streams]
        
        # Calculate total input and output for each component
        component_balance = {}
        
        # Sum inputs
        for stream_id in input_streams:
            composition = results[stream_id].get("composition", {})
            for comp, flow in composition.items():
                if comp not in component_balance:
                    component_balance[comp] = {"input": 0, "output": 0}
                component_balance[comp]["input"] += flow
        
        # Sum outputs
        for stream_id in output_streams:
            composition = results[stream_id].get("composition", {})
            for comp, flow in composition.items():
                if comp not in component_balance:
                    component_balance[comp] = {"input": 0, "output": 0}
                component_balance[comp]["output"] += flow
        
        # Calculate mass balance error
        mass_balance_errors = {}
        for comp, flows in component_balance.items():
            if flows["input"] > 0:
                # Calculate relative error
                error = (flows["output"] - flows["input"]) / flows["input"]
                mass_balance_errors[comp] = error
        
        return mass_balance_errors
    
    @staticmethod
    def check_energy_balance(results: Dict[str, Any]) -> float:
        """Check energy balance across the simulation.
        
        Args:
            results: Simulation results
            
        Returns:
            Overall energy balance error
        """
        # This is a simplified implementation
        # A real implementation would need to extract energy flows from all streams and utilities
        
        # For now, we'll just return a placeholder value
        # In a real implementation, you would:
        # 1. Sum all energy inputs (feed enthalpies, heat added)
        # 2. Sum all energy outputs (product enthalpies, heat removed)
        # 3. Calculate the difference
        
        return 0.0
    
    @staticmethod
    def analyze_simulation_errors(results: Dict[str, Any]) -> List[str]:
        """Analyze any simulation errors or warnings.
        
        Args:
            results: Simulation results
            
        Returns:
            List of error messages
        """
        errors = []
        
        # Check for unit operation errors
        for block_id, block_data in results.items():
            if isinstance(block_data, dict) and "type" in block_data:
                status = block_data.get("status")
                if status and status.lower() != "ok":
                    errors.append(f"Block {block_id} has status: {status}")
        
        return errors