import psycopg2
from config import load_config
from rich.table import Table
from rich.console import Console
from datetime import date


def get_personal_training_sessions():
    commands = """
    SELECT session_id, trainer_id, sessions, sessions_start_time, sessions_end_time from training_sessions;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                data = cur.fetchall()
                return data
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def get_group_classes():
    commands = """
    SELECT group_classes_id, class_name, room_number, class_date, class_start_time, class_end_time from group_classes;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                class_group = cur.fetchall()
                return class_group
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def get_user_registered_sessions(member_id):
    commands = """
    SELECT ts.session_id, ts.trainer_id, ts.sessions, ts.sessions_start_time, ts.sessions_end_time 
    FROM training_sessions ts
    INNER JOIN personal_training_registrations ptr ON ts.session_id = ptr.session_id
    WHERE ptr.member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id,))
                data = cur.fetchall()
                return data
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def get_user_registered_group_sessions(member_id):
    commands = """
    SELECT gc.group_classes_id, gc.class_name, gc.room_number, gc.class_date, gc.class_start_time, gc.class_end_time
    FROM group_classes gc
    INNER JOIN group_class_registrations gcr ON gc.group_classes_id = gcr.group_class_id
    WHERE gcr.member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id,))
                data = cur.fetchall()
                return data
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def is_registered_personal(member_id, session_id):
    commands = """
    SELECT EXISTS (
        SELECT 1 FROM personal_training_registrations
        WHERE member_id = %s AND session_id = %s
    );
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, session_id))
                return cur.fetchone()[0]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


def is_registered_group(member_id, session_id):
    commands = """
    SELECT EXISTS (
        SELECT 1  FROM group_class_registrations
        WHERE member_id = %s AND group_class_id = %s
    );
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, session_id))
                return cur.fetchone()[0]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


def personal_training_fee(member_id):
    fee = 40
    billing_date = date.today().strftime('%Y-%m-%d')
    payment_type = "Personal Training"
    commands = """
        INSERT INTO billing (member_id, payment_amount, payment_date, payment_type)
        VALUES (%s, %s, %s, %s)
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, fee, billing_date, payment_type))
        print("Personal training fee of $40 has been charged")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def group_class_fee(member_id):
    fee = 20
    billing_date = date.today().strftime('%Y-%m-%d')
    payment_type = "Group Class"
    commands = """
        INSERT INTO billing (member_id, payment_amount, payment_date, payment_type)
        VALUES (%s, %s, %s, %s)
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, fee, billing_date, payment_type))
        print("Group Class fee of $20 has been charged")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def register_training_session(member_id, session_id):
    if is_registered_personal(member_id, session_id):
        print("You are already registered for this session.")
        return
    commands = """
    INSERT INTO personal_training_registrations (member_id, session_id)
    VALUES (%s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, session_id,))
                conn.commit()
        print("You have been registered succesfully.")
        personal_training_fee(member_id)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def register_group_classes(member_id, session_id):
    if is_registered_group(member_id, session_id):
        print("You are already registered for this group session")
        return
    commands = """
    INSERT INTO group_class_registrations (member_id, group_class_id)
    VALUES (%s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, session_id,))
                conn.commit()
        print("You have been registered succesfully.")
        group_class_fee(member_id)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def is_trainer_available(trainer_id, session_date, start_time, end_time):
    commands = """
    SELECT COUNT(*) FROM trainer_times
    WHERE trainer_id = %s
    AND availability_date = %s
    AND (start_time::TIME <= %s::TIME AND end_time::TIME >= %s::TIME);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id, session_date, start_time, end_time))
                count = cur.fetchone()[0]
                return count > 0
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


def does_training_session_exist_date(trainer_id, session_date, start_time, end_time):
    commands = """
    SELECT EXISTS (
        SELECT 1 FROM training_sessions
        WHERE trainer_id = %s
        AND sessions = %s
        AND sessions_start_time = %s
        AND sessions_end_time = %s
    );
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id, session_date, start_time, end_time))
                return cur.fetchone()[0]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


def schedule_personal_training_session(trainer_id, member_id, session_date, start_time, end_time):
    if not is_trainer_available(trainer_id, session_date, start_time, end_time):
        print("Trainer is not available at the specified time.")
        return

    if does_training_session_exist_date(trainer_id, session_date, start_time, end_time):
        print("Training session already exists at the specified time.")
        return
    commands = """
    INSERT INTO training_sessions (trainer_id, sessions, sessions_start_time, sessions_end_time)
    VALUES (%s, %s, %s, %s)
    RETURNING session_id;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id, session_date, start_time, end_time))
                session_id = cur.fetchone()[0]
                conn.commit()
        commands = """
        INSERT INTO personal_training_registrations (session_id, member_id)
        VALUES (%s, %s);
        """
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (session_id, member_id))
                conn.commit()

        print("Personal training session scheduled successfully.")
        personal_training_fee(member_id)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def cancel_personal_training_session(member_id, session_id):
    commands = """
    DELETE FROM personal_training_registrations WHERE session_id = %s and member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (session_id, member_id))
                conn.commit()
        print("Personal training session has been deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def cancel_group_class(member_id, session_id):
    commands = """
    DELETE FROM group_class_registrations WHERE group_class_id = %s and member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (session_id, member_id))
                conn.commit()
        print("Group class session has been deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def display_group_classes():
    group_classes = get_group_classes()
    if not group_classes:
        print("No group classes found.")
        return
    table = Table(title="Group Classes")
    table.add_column("Class ID", style="cyan")
    table.add_column("Class Name", style="green")
    table.add_column("Room Number", style="magenta")
    table.add_column("Class Date", style="blue")
    table.add_column("Start Time", style="yellow")
    table.add_column("End Time", style="yellow")
    for class_data in group_classes:
        table.add_row(
            str(class_data[0]),  # Class ID
            class_data[1],       # Class Name
            str(class_data[2]),  # Room Number
            str(class_data[3]),  # Class Date
            str(class_data[4]),  # Start Time
            str(class_data[5])   # End Time
        )
    console = Console()
    console.print(table)


def display_personal_training_sessions():
    session = get_personal_training_sessions()
    if not session:
        print("No personal training sessions found.")
        return
    table = Table(title="Personal training sessions")
    table.add_column("Session ID", style="cyan")
    table.add_column("Trainer ID", style="green")
    table.add_column("Session Date", style="blue")
    table.add_column("Start Time", style="yellow")
    table.add_column("End Time", style="yellow")
    for data in session:
        table.add_row(
            str(data[0]),  # Class ID
            str(data[1]),  # Class Date
            str(data[2]),  # Class Start time
            str(data[3]),  # end time
            str(data[4])
        )
    console = Console()
    console.print(table)


def display_user_registered_sessions(member_id):
    registered_sessions = get_user_registered_sessions(member_id)
    if not registered_sessions:
        print("No registered personal training sessions found for this user.")
        return

    table = Table(title="Registered Personal Training Sessions")
    table.add_column("Session ID", style="cyan")
    table.add_column("Trainer ID", style="green")
    table.add_column("Session Date", style="blue")
    table.add_column("Start Time", style="yellow")
    table.add_column("End Time", style="yellow")

    for session_data in registered_sessions:
        table.add_row(
            str(session_data[0]),  # Session ID
            str(session_data[1]),  # Session Date
            str(session_data[2]),  # Start Time
            str(session_data[3]),   # End Time
            str(session_data[4])
        )

    console = Console()
    console.print(table)


def display_user_registered_group_sessions(member_id):
    registered_sessions = get_user_registered_group_sessions(member_id)
    if not registered_sessions:
        print("No registered group sessions found for this user.")
        return

    table = Table(title="Registered Group Classes")
    table.add_column("Class ID", style="cyan")
    table.add_column("Class Name", style="green")
    table.add_column("Room Number", style="magenta")
    table.add_column("Class Date", style="blue")
    table.add_column("Start Time", style="yellow")
    table.add_column("End Time", style="yellow")

    for session_data in registered_sessions:
        table.add_row(
            str(session_data[0]),  # Class ID
            session_data[1],       # Class Name
            str(session_data[2]),  # Room Number
            str(session_data[3]),  # Class Date
            str(session_data[4]),  # Start Time
            str(session_data[5])   # End Time
        )

    console = Console()
    console.print(table)
