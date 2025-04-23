from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any

class RawMaterial(BaseModel):
    """Model representing a raw material input."""
    name: str
    chemical_formula: Optional[str] = None
    cas_number: Optional[str] = None
    amount: Optional[float] = None
    units: Optional[str] = None
    state: Optional[str] = None  # gas, liquid, solid
    temperature: Optional[float] = None  # Kelvin
    pressure: Optional[float] = None  # Pascal
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    def to_aspen_format(self) -> Dict[str, Any]:
        """Convert to format suitable for Aspen Plus."""
        # Implementation depends on Aspen Plus API requirements
        return {
            "ID": self.name,
            "Formula": self.chemical_formula,
            "CAS": self.cas_number,
            "State": self.state,
            "Amount": self.amount,
            "Units": self.units,
            "T": self.temperature,
            "P": self.pressure,
            # Additional properties as needed
        }

class RawMaterialsList(BaseModel):
    """Collection of raw materials."""
    materials: List[RawMaterial]