
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 100) AS sub_catalog_sales 
        WHERE cs_item_sk IS NOT NULL;
    