CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id
    FROM phonebook
    WHERE username ILIKE p_contact_name
    LIMIT 1;

    IF v_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type: %. Use home, work, or mobile.', p_type;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);

    RAISE NOTICE 'Phone % (%) added to contact "%".', p_phone, p_type, p_contact_name;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM phonebook
    WHERE username ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name ILIKE p_group_name
    LIMIT 1;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name)
        VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'Group "%" created.', p_group_name;
    END IF;

    -- Update contact
    UPDATE phonebook
    SET group_id = v_group_id
    WHERE id = v_contact_id;

    RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id       INTEGER,
    username VARCHAR,
    phone    VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        pb.id,
        pb.username,
        pb.phone,
        pb.email,
        pb.birthday,
        g.name AS grp
    FROM phonebook pb
    LEFT JOIN groups g  ON g.id  = pb.group_id
    LEFT JOIN phones ph ON ph.contact_id = pb.id
    WHERE
        pb.username ILIKE '%' || p_query || '%'
        OR pb.phone  ILIKE '%' || p_query || '%'
        OR pb.email  ILIKE '%' || p_query || '%'
        OR ph.phone  ILIKE '%' || p_query || '%'
    ORDER BY pb.username;
END;
$$;