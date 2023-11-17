
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 1000) AS sub_catalog_sales 
        CROSS JOIN (SELECT * FROM item LIMIT 1000) AS sub_item;
    