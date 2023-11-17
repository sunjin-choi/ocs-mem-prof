
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 1000) AS sub_catalog_sales 
        WHERE cs_item_sk IS NOT NULL;
    