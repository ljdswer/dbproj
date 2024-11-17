UPDATE client
SET last_name = %s,
    date_of_birth = %s,
    address = %s,
    phone_no = %s
WHERE agreement_no = %s;