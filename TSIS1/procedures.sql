-- Add phone to existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$ LANGUAGE plpgsql;


-- Move contact to group (create group if not exists)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- Get or create group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    -- Update contact
    UPDATE contacts SET group_id = v_group_id
    WHERE username = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Search contacts by name, email, or any phone number
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id       INT,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    phone    VARCHAR,
    type     VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.username,
        c.email,
        c.birthday,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.username ILIKE '%' || p_query || '%'
       OR c.email    ILIKE '%' || p_query || '%'
       OR p.phone    ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;


-- Paginated contacts
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(
    id       INT,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;