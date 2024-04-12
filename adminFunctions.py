from config import load_config
from rich.table import Table
from rich.console import Console
import psycopg2
from datetime import date


def admin_login():
    email = input("Please enter Email: ")
    password = input("Please enter Password: ")
    commands = (
        """
        select admin_id from admins where email = %s and password = %s;
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (email, password))
                admin_id = cur.fetchone()
                if admin_id:
                    print("logged in")
                    return admin_id[0]
                else:
                    print("login failed")
                    return None
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None

def create_trainer_account():
    email = input("Please enter Email: ")
    password = input("Please enter Password: ")
    fname = input("Please enter first name: ")
    lname = input("Please enter last name: ")
    commands = (
        """
        insert into trainers(email, password, fname, lname)
        values(%s,%s,%s,%s)
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (email, password, fname, lname,))
        print("Account created")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def view_equipment():
    commands = """
    SELECT maintenance_id, equipment_name, maintenance_cost, maintenance_type, status FROM equipment_maintenance;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                data = cur.fetchall()
                if data:
                    table = Table(title="Maintenance monitoring")
                    table.add_column("Maintenance ID", style="cyan")
                    table.add_column("Equipment Name", style="green")
                    table.add_column("Cost", style="magenta")
                    table.add_column("Type", style="yellow")
                    table.add_column("Status", style="yellow")
                    for row in data:
                        table.add_row(
                            str(row[0]),
                            str(row[1]),
                            str(row[2]),
                            str(row[3]),
                            str(row[4])
                        )
                    console = Console()
                    console.print(table)
                else:
                    print("No equipment found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_equipment_status(status, maintenance_id):
    commands = """
    UPDATE equipment_maintenance SET status = %s where maintenance_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (status, maintenance_id,))
                conn.commit()
        print("Status has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def add_equipment(name, cost, m_type, status):
    commands = """
    INSERT into equipment_maintenance(equipment_name, maintenance_cost, maintenance_type, status)
    values(%s, %s, %s, %s)
    ;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (name, cost, m_type, status,))
                conn.commit()
        print("maintenance report has been succesfully added")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_equipment(id):
    commands = """
    DELETE FROM equipment_maintenance WHERE maintenance_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (id,))
                conn.commit()
        print("maintenance report has been succesfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def get_group_classes():
    commands = """
    SELECT group_classes_id, trainer_id, class_name, room_number, class_date, class_start_time, class_end_time from group_classes;
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


def display_group_classes():
    group_classes = get_group_classes()
    if not group_classes:
        print("No group classes found.")
        return
    table = Table(title="Group Classes")
    table.add_column("Class ID", style="cyan")
    table.add_column("Trainer ID", style="green")
    table.add_column("Class Name", style="magenta")
    table.add_column("Room Number", style="magenta")
    table.add_column("Class Date", style="blue")
    table.add_column("Start Time", style="yellow")
    table.add_column("End Time", style="yellow")
    for class_data in group_classes:
        table.add_row(
            str(class_data[0]),  # Class ID
            str(class_data[1]),       # Class Name
            str(class_data[2]),  # Room Number
            str(class_data[3]),  # Class Date
            str(class_data[4]),  # Start Time
            str(class_data[5]),   # End Time
            str(class_data[6])
        )
    console = Console()
    console.print(table)

def add_new_group_class(name, id, room, date, start, end):
    if not is_trainer_available(id, date, start, end):
        print("Trainer not available")
        return
    if is_room_available(room, date, start, end):
        print("Room is not available at the specified time.")
        return
    commands = """
    INSERT INTO group_classes (class_name, trainer_id, room_number, class_date, class_start_time, class_end_time)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (name, id, room, date, start, end,))
                conn.commit()
        print("New group class added succesfully")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_group_class(id):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM group_class_registrations WHERE group_class_id = %s;", (id,))
                cur.execute("DELETE FROM group_classes WHERE group_classes_id = %s;", (id,))
                conn.commit()
        print("Group class has been successfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_group_class_date(class_id, date, new_start_time, new_end_time, trainer_id):
    if not is_trainer_available(trainer_id, date, new_start_time, new_end_time):
        print("Trainer not available")
        return
    if is_room_available_date(date, new_start_time, new_end_time):
        print("Room is not available at the specified time.")
        return
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE group_classes SET class_date = %s, class_start_time = %s, class_end_time = %s WHERE group_classes_id = %s;", (date, new_start_time, new_end_time, class_id,))
                conn.commit()
        print("Group class time updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def view_booked_rooms():
    commands = """
    SELECT booking_id, trainer_id, room_number, booking_date, booking_start_time, booking_end_time FROM room_booking;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                data = cur.fetchall()
                if data:
                    table = Table(title="Room Bookings")
                    table.add_column("Booking ID", style="cyan")
                    table.add_column("Trainer ID", style="blue")
                    table.add_column("Room Numbner", style="green")
                    table.add_column("Date", style="magenta")
                    table.add_column("Start Time", style="yellow")
                    table.add_column("End Time", style="yellow")
                    for row in data:
                        table.add_row(
                            str(row[0]),
                            str(row[1]),
                            str(row[2]),
                            str(row[3]),
                            str(row[4]),
                            str(row[5])
                        )
                    console = Console()
                    console.print(table)
                else:
                    print("No equipment found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def is_room_available(room, session_date, start_time, end_time):
    commands = """
    SELECT COUNT(*) FROM room_booking
    WHERE room_number = %s
    AND booking_date = %s
    AND (booking_start_time <= %s AND booking_end_time >= %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (room, session_date, start_time, end_time))
                count = cur.fetchone()[0]
                return count == 0
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


def is_room_available_date(session_date, start_time, end_time):
    commands = """
    SELECT COUNT(*) FROM room_booking
    WHERE booking_date = %s
    AND (booking_start_time <= %s AND booking_end_time >= %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (session_date, start_time, end_time))
                count = cur.fetchone()[0]
                return count == 0
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False


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

def add_room_booking(trainer_id, room_number, booking_date, booking_start_time, booking_end_time):
    if not is_trainer_available(trainer_id, booking_date, booking_start_time, booking_end_time):
        print("Trainer not available at the time")
        return
    commands = """
        INSERT INTO room_booking (trainer_id, room_number, booking_date, booking_start_time, booking_end_time)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING booking_id;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (trainer_id, room_number, booking_date, booking_start_time, booking_end_time))
                conn.commit()
        print("Room booking added successfull")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_booked_room(room_id):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM group_class_registrations WHERE group_class_id IN (SELECT group_classes_id FROM group_classes WHERE room_number = %s);", (room_id,))
                cur.execute("DELETE FROM group_classes where room_number=%s;", (room_id,))
                cur.execute("DELETE FROM room_booking WHERE room_number = %s;", (room_id,))
                conn.commit()
        print("Booked room has been successfully deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def display_billing():
    commands = """
    SELECT billing_id, member_id, payment_amount, payment_date, payment_type FROM billing;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                data = cur.fetchall()
                if data:
                    table = Table(title="Billing")
                    table.add_column("Billing ID", style="cyan")
                    table.add_column("Member ID", style="blue")
                    table.add_column("Amount", style="green")
                    table.add_column("Date Billed", style="magenta")
                    table.add_column("Fee Type", style="yellow")
                    for row in data:
                        table.add_row(
                            str(row[0]),
                            str(row[1]),
                            str(row[2]),
                            str(row[3]),
                            str(row[4])
                        )
                    console = Console()
                    console.print(table)
                else:
                    print("No billing info found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def display_trainer_times():
    commands = """
    SELECT trainer_id, availability_date, start_time, end_time FROM trainer_times;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                data = cur.fetchall()
                if data:
                    table = Table(title="Trainer times")
                    table.add_column("Trainer ID", style="cyan")
                    table.add_column("Date", style="blue")
                    table.add_column("Start time", style="yellow")
                    table.add_column("End time", style="yellow")
                    for row in data:
                        table.add_row(
                            str(row[0]),
                            str(row[1]),
                            str(row[2]),
                            str(row[3]),
                        )
                    console = Console()
                    console.print(table)
                else:
                    print("No trainer info found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def waive_fee(billing_id):
    commands = """
    DELETE FROM billing WHERE billing_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (billing_id,))
                conn.commit()
        print("Fee has been succesfully waived")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def charge_fee(member_id, fee, payment_type):
    billing_date = date.today().strftime('%Y-%m-%d')
    commands = """
        INSERT INTO billing (member_id, payment_amount, payment_date, payment_type)
        VALUES (%s, %s, %s, %s)
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, fee, billing_date, payment_type))
        print("Fee has been charged")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def edit_fee(billing_id, member_id, fee, payment_type):
    billing_date = date.today().strftime('%Y-%m-%d')
    commands = """
    UPDATE billing SET member_id = %s, payment_amount = %s, payment_date= %s, payment_type =%s where billing_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, fee, billing_date, payment_type, billing_id,))
                conn.commit()
        print("Billing has been updated successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
