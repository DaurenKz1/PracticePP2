-- 1. Add phone
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid
    FROM contacts
    WHERE first_name = p_contact_name
    LIMIT 1;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;


-- 2. Move to group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE gid INT;
DECLARE cid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES(p_group_name)
        RETURNING id INTO gid;
    END IF;

    SELECT id INTO cid FROM contacts
    WHERE first_name = p_contact_name;

    UPDATE contacts
    SET group_id = gid
    WHERE id = cid;
END;
$$;


-- 3. Extended search
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, c.last_name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.first_name ILIKE '%' || p_query || '%'
        OR c.last_name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;