
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 100) AS sub_catalog_sales 
        JOIN (SELECT * FROM item LIMIT 100) AS sub_item 
        ON sub_catalog_sales.cs_item_sk = sub_item.i_item_sk;
    