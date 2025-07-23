async def get_user_or_create(conn, nome, matricula):
    user = await conn.fetchrow("SELECT * FROM users WHERE matricula=$1", matricula)
    if user:
        print(user)
        return user
    else:
        return await conn.fetchrow(
            "INSERT INTO users (nome, matricula) VALUES ($1, $2) RETURNING *",
            nome, matricula
        )