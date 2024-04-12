import psycopg2
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from config import load_config
from datetime import date
import os


def member_login():
    email = input("Please enter Email: ")
    password = input("Please enter Password: ")
    commands = (
        """
        select member_id from members where email = %s and password = %s;
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (email, password))
                member_id = cur.fetchone()
                if member_id:
                    print("logged in")
                    return member_id[0]
                else:
                    print("login failed")
                    return None
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def member_create_account():
    email = input("Please enter Email: ")
    password = input("Please enter Password: ")
    fname = input("Please enter first name: ")
    lname = input("Please enter last name: ")
    current_weight = input("Please enter your current weight: ")
    height = input("Please enter your height in cm: ")
    commands = (
        """
        insert into members(email, password, fname, lname, current_weight, height)
        values(%s,%s,%s,%s,%s,%s)
        returning member_id;
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (email, password, fname, lname,current_weight, height))
                member_id = cur.fetchone()[0]
        print("Account created")
        membership_fee(member_id)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def membership_fee(member_id):
    fee = 50
    billing_date = date.today().strftime('%Y-%m-%d')
    payment_type = "Membership"
    commands = """
        INSERT INTO billing (member_id, payment_amount, payment_date, payment_type)
        VALUES (%s, %s, %s, %s)
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id, fee, billing_date, payment_type))
        print("Membership fee of $50 has been charged")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def get_exercise_routine(member_id):
    # Connect to the database and retrieve exercise routine data for the member
    commands = """
    SELECT exercise_id, exercise_name, reps, sets FROM exercises WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id,))
                exercise_routine = cur.fetchall()
                return exercise_routine
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def get_health_stats(member_id):
    # Connect to the database and retrieve health data for the member
    commands = """
    SELECT height, current_weight FROM members WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id,))
                health_stats = cur.fetchone()
                return health_stats
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def get_fitness_achievements(member_id):
    commands = """
    SELECT achievement_id, achievement_name, achievement_desc, achievement_date FROM fitness_achievements WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id,))
                achievement = cur.fetchall()
                return achievement
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def get_fitness_goals(member_id):
    commands = """
    SELECT goal_id, goal_name, status from fitness_goals WHERE member_id = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands, (member_id,))
                goals = cur.fetchall()
                return goals
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def member_dashboard(member_id):
    console = Console()
    _width, _height = os.get_terminal_size()
    console.size = (_width-0, _height-17)
    layout = Layout()
    header_content = "Welcome to Your Dashboard"
    # Get exercise routine for the member

    goals = get_fitness_goals(member_id)
    if goals:
        goals_str = "\n".join([f" {goal_id}.{name}: {status}"for goal_id, name, status in goals])
    else:
        goals_str = "No goals found."


    exercise_routine = get_exercise_routine(member_id)
    if exercise_routine:
        # Format exercise routine data for display
        exercise_routine_str = "\n".join([f" {exercise_id}.{exercise_name}: {reps} reps x {sets} sets" for exercise_id, exercise_name, reps, sets in exercise_routine])
    else:
        exercise_routine_str = "No exercise routine found."
    # Get health stats for member
    health_stats = get_health_stats(member_id)
    if health_stats:
        height, current_weight = health_stats
        health_stats_str = f"Height: {height} cm\nCurrent Weight: {current_weight} lbs"
    else:
        health_stats_str = "No health statistics found."

    fitness_achievements = get_fitness_achievements(member_id)
    if fitness_achievements:
        fitness_achievement_str = "\n".join([f"{achievement_id}.{name} ({date}): {desc}" for achievement_id, name, desc, date in fitness_achievements])
    else:
        fitness_achievement_str = "No fitness achievements found."

    layout.split_column(
        Layout(name="Dashboard", size=4),
        Layout(name="middle", size=10),
        Layout(name="lower", size=10)
    )
    layout["middle"].split_row(
        Layout(name="Exercise Routines"),
        Layout(name="Fitness Goals"),
    )
    layout["lower"].split_row(
        Layout(name="Health Statistics"),
        Layout(name="Fitness Achievements"),
    )
    # Center the exercise routine text within a panel

    goals_text = Align.center(
        Text.from_markup(goals_str, justify="center"),
        vertical="middle",
        style="white",
    )
    goal_panel = Panel(goals_text, title="Goals", style="medium_purple2")

    achievements_stats_text = Align.center(
        Text.from_markup(fitness_achievement_str, justify="center"),
        vertical="middle",
        style="white",
    )
    fitness_achievements_panel = Panel(achievements_stats_text, title="Fitness Achievements", style="medium_purple2")

    health_stats_text = Align.center(
        Text.from_markup(health_stats_str, justify="center"),
        vertical="middle",
        style="white",
    )
    health_stats_panel = Panel(health_stats_text, title="Health Statistics", style="medium_purple2")

    exercise_text = Align.center(
        Text.from_markup(f"[blink]{exercise_routine_str}[/blink]\n", justify="center"),
        vertical="middle",
        style="white",
    )
    exercise_panel = Panel(exercise_text, title="Exercise Routine", style="medium_purple2")

    header_text = Align.center(
        Text.from_markup(header_content, justify="center"),
        vertical="middle",
        style="white",
    )
    header_panel = Panel(header_text, title="Dashboard", style="medium_purple2")

    layout["Health Statistics"].update(health_stats_panel)
    layout["Dashboard"].update(header_panel)
    layout["Exercise Routines"].update(exercise_panel)
    layout["Fitness Achievements"].update(fitness_achievements_panel)
    layout["Fitness Goals"].update(goal_panel)
    console.print(layout)
