
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 1000) AS sub_catalog_sales 
        NATURAL JOIN (SELECT * FROM date_dim LIMIT 1000) AS sub_date_dim 
        ORDER BY cs_wholesale_cost;
    