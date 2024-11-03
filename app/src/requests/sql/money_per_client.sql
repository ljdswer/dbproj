SELECT agreement_no, SUM(leftover) as sum, COUNT(account_id) as amount_of_accounts FROM account GROUP BY agreement_no 
