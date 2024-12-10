class POI:
    _name: str
    _address: str
    _description: str
    _coordinates: list
    _duration: str  # Duration as a string like "2h 30m"
    _keywords: list[str]

    def __init__(self, name: str, address: str, description: str, duration: str):
        self._name = name
        self._address = address
        self._description = description
        self._coordinates = []
        self._duration = duration

    def update_coordinates(self, coords: list):
        self._coordinates = coords

    def update_keywords(self, keywords: list[str]):
        self._keywords = keywords

    def get_poi(self, include_fields=None, exclude_fields=None):
        """
        Retrieve a dictionary representation of the POI object.

        Args:
        - include_fields (list, optional): Specific fields to include. If None, all fields are included.
        - exclude_fields (list, optional): Fields to exclude from the result. Ignored if include_fields is provided.

        Returns:
        - dict: The POI as a dictionary.
        """
        # Collect all instance variables as a dictionary
        poi_dict = {
            "name": self._name,
            "address": self._address,
            "description": self._description,
            "coordinates": self._coordinates if self._coordinates else None,
            "duration": self._duration if self._duration else None,
            "keywords": self._keywords if self._keywords else None
        }

        if include_fields:
            return {key: poi_dict[key] for key in include_fields if key in poi_dict}

        if exclude_fields:
            return {key: value for key, value in poi_dict.items() if key not in exclude_fields}

        return poi_dict