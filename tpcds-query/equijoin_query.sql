
        SELECT * 
        FROM (SELECT * FROM catalog_sales LIMIT 1000) AS sub_catalog_sales 
        JOIN (SELECT * FROM item LIMIT 1000) AS sub_item 
        ON sub_catalog_sales.cs_item_sk = sub_item.i_item_sk;
    