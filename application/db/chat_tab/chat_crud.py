async def create_chat_tab(conn, user_id, title):
    return await conn.fetchrow("""
        INSERT INTO chat_tabs (user_id, title)
        VALUES ($1, $2)
        RETURNING id, title, created_at
    """, user_id, title)

async def delete_chat_tab(conn, chat_tab_id):
    await conn.execute("DELETE FROM chat_messages WHERE chat_tab_id=$1", chat_tab_id)
    await conn.execute("DELETE FROM chat_tabs WHERE id=$1", chat_tab_id)

async def update_at_by_chat_tab_id(conn, chat_tab_id):
    await conn.execute("UPDATE chat_tabs SET updated_at = NOW() WHERE id=$1", chat_tab_id)

async def update_chat_tab_context(conn, chat_tab_id, context):
    await conn.execute("UPDATE chat_tabs SET context=$1 WHERE id=$2", context, chat_tab_id)

async def get_chat_tab_context(conn, chat_tab_id):
    row = await conn.fetchrow("SELECT context FROM chat_tabs WHERE id = $1", chat_tab_id)
    return row["context"] if row and "context" in row else None

async def get_chat_tabs_by_matricula(conn, matricula):
    return await conn.fetch("""
        SELECT ct.id, ct.title, ct.updated_at
        FROM chat_tabs ct
        JOIN users u ON ct.user_id = u.id
        WHERE u.matricula = $1
        ORDER BY ct.created_at
    """, matricula)

async def get_chat_messages_by_chat_id(conn, chat_id):
    return await conn.fetch("""
        SELECT role, content, filename, created_at
        FROM chat_messages
        WHERE chat_tab_id = $1
        ORDER BY created_at
    """, chat_id)

async def add_chat_message(conn, chat_tab_id, role, content, filename):
    await conn.execute("""
        INSERT INTO chat_messages (chat_tab_id, role, content, filename)
        VALUES ($1, $2, $3, $4)
    """, chat_tab_id, role, content, filename)