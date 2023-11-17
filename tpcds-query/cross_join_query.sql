
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 100) AS sub_catalog_sales 
        CROSS JOIN (SELECT * FROM item LIMIT 100) AS sub_item;
    