SELECT user_id, user_role, agreement_no FROM auth_external WHERE user_name = %s AND user_pass_hash = SHA2(%s, 256)
