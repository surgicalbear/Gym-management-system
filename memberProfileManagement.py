import psycopg2
from config import load_config


def update_first_name(member_id, new_fname):
    commands = """
    UPDATE members SET fname = %s WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (new_fname, member_id,))
                conn.commit()
        print("First name has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_last_name(member_id, new_lname):
    commands = """
    UPDATE members SET lname = %s WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (new_lname, member_id,))
                conn.commit()
        print("Last name has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_email(member_id, new_email):
    commands = """
    UPDATE members SET email = %s WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (new_email, member_id,))
                conn.commit()
        print("Email has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_password(member_id, new_password):
    commands = """
    UPDATE members SET password = %s WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (new_password, member_id,))
                conn.commit()
        print("Password has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_weight(member_id, new_weight):
    commands = """
    UPDATE members SET current_weight = %s WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (new_weight, member_id,))
                conn.commit()
        print("Weight has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_height(member_id, new_height):
    commands = """
    UPDATE members SET height = %s WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (new_height, member_id,))
                conn.commit()
        print("Height has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def add_fitness_achievement(member_id, name, description, date):
    commands = """
    INSERT INTO fitness_achievements (member_id, achievement_name, achievement_desc, achievement_date)
    VALUES (%s, %s, %s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, name, description, date,))
                conn.commit()
        print("Achievement has been added successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_fitness_achievement(member_id, achievement_id):
    commands = """
    DELETE FROM fitness_achievements WHERE achievement_id = %s and member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (achievement_id, member_id))
                conn.commit()
        print("Achievement has been succesfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def add_goal(member_id, goal_name, goal_status):
    commands = """
    INSERT INTO fitness_goals (member_id, goal_name, status)
    VALUES (%s, %s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, goal_name, goal_status,))
                conn.commit()
        print("Goal has been added successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_goal(member_id, goal_id, goal_progress):
    commands = """
    UPDATE fitness_goals SET status = %s WHERE goal_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (goal_progress, goal_id,))
                conn.commit()
        print("Goal has been succesfully updated")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_goal(member_id, goal_id):
    commands = """
    DELETE FROM fitness_goals WHERE goal_id = %s AND member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (goal_id, member_id,))
                conn.commit()
        print("Goal has been succesfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def add_exercise(member_id, name, reps, sets):
    commands = """
    INSERT INTO exercises (member_id, exercise_name, reps, sets)
    VALUES (%s, %s, %s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, name, reps, sets,))
                conn.commit()
        print("Exercise has been added successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_exercise(member_id, exercise_id, reps, sets):
    commands = """
    UPDATE exercises SET reps = %s, sets = %s WHERE exercise_id = %s AND member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (reps, sets, exercise_id, member_id))
                conn.commit()
        print("Exercise has been succesfully updated")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_exercise(member_id, exercise_id):
    commands = """
    DELETE FROM exercises WHERE member_id = %s AND exercise_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, exercise_id,))
                conn.commit()
        print("Exercise has been succesfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
