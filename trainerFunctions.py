import psycopg2
from config import load_config
from rich.table import Table
from rich.console import Console


def trainer_login():
    email = input("Please enter Email: ")
    password = input("Please enter Password: ")
    commands = (
        """
        select trainer_id from trainers where email = %s and password = %s;
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (email, password))
                trainer_id = cur.fetchone()
                if trainer_id:
                    print("logged in")
                    return trainer_id[0]
                else:
                    print("login failed")
                    return None
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def update_trainer_time(time_id, date, start, end):
    commands = """
    UPDATE trainer_times SET availability_date = %s, start_time = %s, end_time = %s WHERE time_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (date, start, end, time_id))
                conn.commit()
        print("Availability has been succesfully updated")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def add_training_time(trainer_id, date, start, end):
    if does_training_session_exist_date(trainer_id, date, start, end):
        print("You are already available for this date")
        return
    commands = """
    INSERT into trainer_times(trainer_id, availability_date, start_time, end_time)
    values(%s, %s, %s, %s)
    ;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id,date, start, end,))
                conn.commit()
        print("training time has been succesfully added")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_training_time(time_id):
    commands = """
    DELETE FROM trainer_times WHERE time_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (time_id,))
                conn.commit()
        print("training availability has been succesfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def does_training_session_exist_date(trainer_id, date, start_time, end_time):
    commands = """
    SELECT EXISTS (
        SELECT 1 FROM trainer_times
        WHERE trainer_id = %s
        AND availability_date = %s
        AND start_time = %s
        AND end_time = %s
    );
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id, date, start_time, end_time))
                return cur.fetchone()[0]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


def get_personal_training_sessions(trainer_id):
    commands = """
    SELECT time_id, trainer_id, availability_date, start_time, end_time from trainer_times where trainer_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id,))
                data = cur.fetchall()
                return data
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def display_trainer_data(trainer_id):
    schedule = get_personal_training_sessions(trainer_id)
    if not schedule:
        print("No schedule found.")
        return
    table = Table(title="Trainer Schedule")
    table.add_column("Availability ID", style="blue")
    table.add_column("Trainer ID", style="cyan")
    table.add_column("Date", style="green")
    table.add_column("Start Time", style="yellow")
    table.add_column("End Time", style="yellow")
    for class_data in schedule:
        table.add_row(
            str(class_data[0]),  # Class ID
            str(class_data[1]),       # Class Name
            str(class_data[2]),  # Room Number
            str(class_data[3]),  # Class Date
            str(class_data[4])
        )
    console = Console()
    console.print(table)


def member_profile_viewing(fname, lname):
    commands = """
    SELECT fname, lname, email, current_weight, height FROM members WHERE fname = %s AND lname = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (fname, lname))
                data = cur.fetchone()
                if data:
                    table = Table()
                    title = f"Member Profile: {data[0]} {data[1]}"
                    table.title = title
                    table.add_column("First Name", style="cyan")
                    table.add_column("Last Name", style="green")
                    table.add_column("Email", style="magenta")
                    table.add_column("Current Weight", style="yellow")
                    table.add_column("Height", style="yellow")
                    table.add_row(
                        str(data[0]),
                        str(data[1]),
                        str(data[2]),
                        str(data[3]),
                        str(data[4])
                    )
                    console = Console()
                    console.print(table)
                else:
                    print("No data found for the given member.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
