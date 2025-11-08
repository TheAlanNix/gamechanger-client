# -*- coding: utf-8 -*-
"""GameChanger 'Search' API wrapper."""

from typing import Any, Dict, List, Optional

from gamechanger_client.endpoints.rest_endpoint import RestEndpoint

class SearchEndpoint(RestEndpoint):

    def __init__(self, session):
        super().__init__(session, 'search')
    
    @staticmethod
    def create_season(name: str, year: int) -> Dict[str, Any]:
        """
        Helper method to create a properly formatted season object.
        
        Args:
            name: Season name. Must be one of: "fall", "winter", "spring", "summer"
            year: Season year as a number
            
        Returns:
            Dict with properly formatted season object
            
        Raises:
            ValueError: If season name is not valid
        """
        valid_seasons = ["fall", "winter", "spring", "summer"]
        if name not in valid_seasons:
            raise ValueError(f"Season name must be one of: {valid_seasons}")
        
        return {"name": name, "year": year}
    
    @staticmethod  
    def create_coordinates(lat: float, long: float) -> Dict[str, float]:
        """
        Helper method to create a properly formatted coordinates object.
        
        Args:
            lat: Latitude as a number
            long: Longitude as a number
            
        Returns:
            Dict with properly formatted coordinates object
        """
        return {"lat": lat, "long": long}

    def search(self, 
               name: str,
               *,  # Force keyword-only arguments after this
               types: List[str] = None,
               seasons: List[Dict[str, Any]] = None,
               sport: Optional[str] = None,
               city: Optional[str] = None,
               states: List[str] = None,
               include_older_seasons: Optional[bool] = None,
               coordinates: Optional[Dict[str, float]] = None,
               features: Optional[Dict[str, Any]] = None,
               additional_fields: Dict[str, Any] = None,
               **kwargs) -> dict:
        """
        Perform a search across GameChanger data.
        
        Args:
            name: Search query name/term
            types: List of types to search for. Valid values: ["team", "org_league", "org_tournament", "org_travel"]
            seasons: List of season objects with 'name' and 'year'. Season names: ["fall", "winter", "spring", "summer"]
            sport: Specific sport to filter by (optional)
            city: City to filter by (optional)
            states: List of states to filter by (default: [])
            include_older_seasons: Whether to include older seasons (optional)
            coordinates: Dict with 'lat' and 'long' keys for location-based search (optional)
            features: Dict with feature flags like 'search_by_coach' (optional)
            additional_fields: Dict of additional search parameters
            **kwargs: Additional search parameters passed as keyword arguments
            
        Returns:
            dict: API response with search results
            
        Raises:
            SchemaValidationError: If the request parameters don't match the API schema
        """
        search_params = {
            'name': name,
        }
        
        # Only include non-None optional parameters
        if types is not None:
            search_params['types'] = types
        if seasons is not None:
            search_params['seasons'] = seasons
        if sport is not None:
            search_params['sport'] = sport
        if city is not None:
            search_params['city'] = city
        if states is not None:
            search_params['states'] = states
        if include_older_seasons is not None:
            search_params['include_older_seasons'] = include_older_seasons
        if coordinates is not None:
            search_params['coordinates'] = coordinates
        if features is not None:
            search_params['features'] = features
        
        # Merge additional fields
        if additional_fields:
            search_params.update(additional_fields)
            
        # Merge kwargs
        search_params.update(kwargs)
        
        return super().post(**search_params)
