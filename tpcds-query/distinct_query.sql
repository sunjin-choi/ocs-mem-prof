SELECT DISTINCT cs_item_sk FROM (SELECT * FROM catalog_sales LIMIT 100) AS sub_catalog_sales;