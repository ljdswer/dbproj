SELECT count as 'Количество' FROM client_report cr WHERE MONTH(cr.client_report_date) = %s AND YEAR(cr.client_report_date) = %s;