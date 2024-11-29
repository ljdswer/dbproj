INSERT INTO acc_history
			(agreement_no, account_id_src, account_id_dest, amount, leftover_assign_date)
			VALUES(%s, %s, %s, %s, NOW());