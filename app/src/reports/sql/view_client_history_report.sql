SELECT c.agreement_no AS Договор, c.last_name AS Фамилия, ard.amount AS "Сумма переводов"
FROM acc_report ar
LEFT JOIN acc_report_data ard ON ar.acc_report_id = ard.acc_report_id
JOIN client c ON c.agreement_no = ard.agreement_no 
WHERE MONTH(ar.acc_report_date) = %s
  AND YEAR(ar.acc_report_date) = %s;