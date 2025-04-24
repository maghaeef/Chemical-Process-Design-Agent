from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any, Literal

class ProductSpecification(BaseModel):
    """Model representing specifications for a desired product."""
    name: str
    chemical_formula: Optional[str] = None
    cas_number: Optional[str] = None
    purity: Optional[float] = None  # Decimal between 0 and 1
    yield_requirement: Optional[float] = None  # Decimal between 0 and 1
    state: Optional[Literal["gas", "liquid", "solid"]] = None
    temperature_range: Optional[Dict[str, float]] = None  # {"min": value, "max": value} in Kelvin
    pressure_range: Optional[Dict[str, float]] = None  # {"min": value, "max": value} in Pascal
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    def is_satisfied_by(self, product_data: Dict[str, Any]) -> Dict[str, bool]:
        """Check if a produced product meets the specifications."""
        results = {}
        
        # Check purity
        if self.purity is not None and "purity" in product_data:
            results["purity"] = product_data["purity"] >= self.purity
            
        # Check yield
        if self.yield_requirement is not None and "yield" in product_data:
            results["yield"] = product_data["yield"] >= self.yield_requirement
            
        # Check state
        if self.state is not None and "state" in product_data:
            results["state"] = product_data["state"] == self.state
            
        # Check temperature
        if self.temperature_range is not None and "temperature" in product_data:
            temp = product_data["temperature"]
            min_temp = self.temperature_range.get("min")
            max_temp = self.temperature_range.get("max")
            
            if min_temp is not None and max_temp is not None:
                results["temperature"] = min_temp <= temp <= max_temp
            elif min_temp is not None:
                results["temperature"] = temp >= min_temp
            elif max_temp is not None:
                results["temperature"] = temp <= max_temp
        
        # Check pressure
        if self.pressure_range is not None and "pressure" in product_data:
            pressure = product_data["pressure"]
            min_pressure = self.pressure_range.get("min")
            max_pressure = self.pressure_range.get("max")
            
            if min_pressure is not None and max_pressure is not None:
                results["pressure"] = min_pressure <= pressure <= max_pressure
            elif min_pressure is not None:
                results["pressure"] = pressure >= min_pressure
            elif max_pressure is not None:
                results["pressure"] = pressure <= max_pressure
                
        # Check custom properties
        for prop_name, prop_value in self.properties.items():
            if isinstance(prop_value, dict) and "min" in prop_value and "max" in prop_value:
                if prop_name in product_data:
                    results[prop_name] = prop_value["min"] <= product_data[prop_name] <= prop_value["max"]
            elif prop_name in product_data:
                results[prop_name] = product_data[prop_name] == prop_value
                
        return results
        
    def all_specifications_met(self, product_data: Dict[str, Any]) -> bool:
        """Check if all specifications are met."""
        results = self.is_satisfied_by(product_data)
        return all(results.values())

class ProductSpecificationsList(BaseModel):
    """Collection of product specifications."""
    specifications: List[ProductSpecification]