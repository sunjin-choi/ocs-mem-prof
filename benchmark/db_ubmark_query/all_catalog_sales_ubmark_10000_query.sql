SELECT * FROM catalog_sales_ubmark_10000 WHERE cs_item_sk IS NOT NULL;

SELECT * FROM catalog_sales_ubmark_10000 A CROSS JOIN item B;

SELECT * FROM catalog_sales_ubmark_10000 JOIN item ON catalog_sales_ubmark_10000.cs_item_sk = item.i_item_sk;

SELECT * FROM catalog_sales_ubmark_10000 WHERE d_year BETWEEN 5 AND 15;

SELECT DISTINCT cs_item_sk FROM catalog_sales_ubmark_10000;

SELECT cs_bill_customer_sk, COUNT(*) FROM catalog_sales_ubmark_10000 GROUP BY cs_bill_customer_sk;

SELECT * FROM catalog_sales_ubmark_10000 ORDER BY cs_wholesale_cost;

