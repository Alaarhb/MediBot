import requests

def get_drug_info(drug_name):
    """
    Fetches drug information from OpenFDA API.
    """
    base_url = "https://api.fda.gov/drug/label.json"
    query = f'search=openfda.brand_name:"{drug_name}"&limit=1'
    
    try:
        response = requests.get(f"{base_url}?{query}")
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            
            # Extract relevant info
            purpose = result.get('purpose', ['Information not available'])[0]
            warnings = result.get('warnings', ['No specific warnings found'])[0]
            
            # Truncate if too long (simple approach)
            if len(warnings) > 300:
                warnings = warnings[:300] + "..."
                
            return {
                "found": True,
                "name": drug_name,
                "purpose": purpose,
                "warnings": warnings
            }
        else:
            return {"found": False}
    except Exception as e:
        print(f"Error fetching drug info: {e}")
        return {"found": False, "error": str(e)}

def get_hospitals(city):
    """
    Fetches hospital information for a given city using OpenStreetMap (Nominatim).
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"hospitals in {city}",
        "format": "json",
        "limit": 3,
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "MediBot/1.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if not data:
            return {"found": False}

        hospitals = []
        for place in data:
            name = place.get('display_name', 'Unknown Hospital').split(',')[0]
            lat = place.get('lat')
            lon = place.get('lon')
            hospitals.append({"name": name, "lat": lat, "lon": lon})
            
        return {"found": True, "hospitals": hospitals}
        
    except Exception as e:
        print(f"Error fetching hospital info: {e}")
        return {"found": False, "error": str(e)}

if __name__ == "__main__":
    # Simple test
    print(get_drug_info("Advil"))
    print(get_hospitals("San Francisco"))
