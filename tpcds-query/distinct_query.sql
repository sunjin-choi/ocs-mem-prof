
        SELECT DISTINCT cs_item_sk 
        FROM (SELECT * FROM catalog_sales LIMIT 1000) AS sub_catalog_sales;
    