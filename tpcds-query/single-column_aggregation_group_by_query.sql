
        SELECT cs_bill_customer_sk, COUNT(*) 
        FROM (SELECT * FROM catalog_sales LIMIT 100) AS sub_catalog_sales 
        GROUP BY cs_bill_customer_sk;
    