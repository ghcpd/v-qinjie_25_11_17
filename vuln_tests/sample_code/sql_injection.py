def get_user(conn, username):
    # Vulnerable: building SQL via string concatenation
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    conn.execute(query)
