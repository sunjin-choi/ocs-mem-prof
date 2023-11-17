
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 100) AS sub_catalog_sales 
        NATURAL JOIN (SELECT * FROM date_dim LIMIT 100) AS sub_date_dim 
        ORDER BY cs_wholesale_cost;
    