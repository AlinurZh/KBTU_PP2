CREATE OR REPLACE PROCEDURE upsert_user(
    p_username VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook WHERE username = p_username
    ) THEN 
        UPDATE phonebook
        SET phone = p_phone
        WHERE p_username = username;
    ELSE
        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE insert_many_users(
    p_usernames TEXT[],
    p_phones TEXT[]
)
AS $$
DECLARE
    i INT;
    invalid_data TEXT := '';
BEGIN
    IF array_length(p_usernames, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN 
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i in 1..array_length(p_usernames, 1) LOOP
        IF p_phones[i] ~ '^(\+7|8)[0-9]{10}$' THEN 
            CALL upsert_user(p_usernames[i], p_phones[i]);
        ELSE 
            invalid_data := invalid_data || '(' || p_usernames[i] || ', ' || p_phones[i] || ') ';
        END IF;
    END LOOP;

    IF invalid_data <> '' THEN 
        RAISE NOTICE 'Incorrect data: %', invalid_data;
    END IF; 
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_user(
    p_username VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
) 
AS $$
BEGIN 
    IF p_username IS NOT NULL THEN
        DELETE FROM phonebook
        WHERE username = p_username;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook
        WHERE phone = p_phone;
    ELSE
        RAISE EXCEPTION 'Provide username or phone';
    END IF;
END;
$$ LANGUAGE plpgsql;