-- List amenities linked to places via the association table
SELECT amenities.name AS name,
       places.name AS name
FROM amenities
JOIN place_amenity ON amenities.id = place_amenity.amenity_id
JOIN places ON places.id = place_amenity.place_id
ORDER BY amenities.name ASC, places.name DESC;
