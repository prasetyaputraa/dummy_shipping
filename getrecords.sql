SELECT * FROM lpd_dummy_shipping.records_receiptinstance as t1
	JOIN
    (SELECT no, weight, count, sender, addr_ship_from, addr_ship_to, status, MAX(datetime) as datetime
		FROM lpd_dummy_shipping.records_receiptwrite
		GROUP BY no 
	) as t2
		ON t1.no = REPLACE(t2.no, "-", "");