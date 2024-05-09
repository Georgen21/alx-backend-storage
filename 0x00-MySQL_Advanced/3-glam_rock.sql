-- Script Lists all bands with Glam rock AS their main style 
-- list is ranked by their longevity

SELECT
    band_name,
    CASE
        WHEN formed = 0 OR split = 0 THEN 0
        ELSE 2022 - LEAST(formed, split)
    END AS lifespan
FROM
    metal_bands
WHERE
    style = 'Glam rock'
ORDER BY
    lifespan DESC;
