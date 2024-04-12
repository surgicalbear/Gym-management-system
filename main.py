from memberFunctions import (
    member_login,
    member_create_account,
    member_dashboard
)

from trainerFunctions import (
    trainer_login,
    display_trainer_data,
    delete_training_time,
    add_training_time,
    update_trainer_time,
    member_profile_viewing
)

from memberProfileManagement import (
    update_first_name,
    update_last_name,
    update_email,
    update_password,
    update_height,
    update_weight,
    add_fitness_achievement,
    delete_fitness_achievement,
    add_goal,
    update_goal,
    delete_goal,
    add_exercise,
    update_exercise,
    delete_exercise
)


from memberScheduleManagement import (
    schedule_personal_training_session,
    register_group_classes,
    register_training_session,
    display_user_registered_group_sessions,
    display_user_registered_sessions,
    cancel_personal_training_session,
    cancel_group_class,
    display_personal_training_sessions,
    display_group_classes
)


from adminFunctions import (
    admin_login,
    create_trainer_account,
    view_equipment,
    update_equipment_status,
    add_equipment,
    delete_equipment,
    get_group_classes,
    display_group_classes,
    add_new_group_class,
    delete_group_class,
    update_group_class_date,
    view_booked_rooms,
    add_room_booking,
    delete_booked_room,
    display_billing,
    waive_fee,
    charge_fee,
    edit_fee,
    display_trainer_times
)


def menu():
    while True:
        print_menu()
        choice = int(input("Enter your choice: "))
        if choice == 1:
            member_functions_menu()
        elif choice == 2:
            trainer_functions_menu()
        elif choice == 3:
            admin_functions_menu()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


def print_menu():
    print("Please select an option from below")
    print("1. Member functions")
    print("2. Trainer functions")
    print("3. Admin functions")
    print("4. Quit")


def member_functions_menu():
    while True:
        print("Member menu")
        print("1. Login")
        print("2. Create account")
        print("3. Back to main menu")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            member_id = member_login()
            if member_id:
                member_loggedin_options(member_id)
        elif choice == 2:
            member_create_account()
        elif choice == 3:
            break
        else:
            print("Invalid choice.")


def member_loggedin_options(member_id):
    while True:
        print("1. Display Dashboard")
        print("2. Profile Management")
        print("3. Schedule Management")
        print("4. Go back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            member_dashboard(member_id)
        elif choice == 2:
            member_profile_management(member_id)
        elif choice == 3:
            member_schedule_management(member_id)
        elif choice == 4:
            print("going back...")
            break
        else:
            print("Invalid choice.")

# notes for later, add fitness goals to the dashboard and DDL
def member_profile_management(member_id):
    while True:
        print("1. Update personal information")
        print("2. Update health metrics")
        print("3. Update fitness achievements")
        print("4. Update fitness goals")
        print("5. Update exercise routine")
        print("6. Go back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            while True:
                print("1. Update first name")
                print("2. Update last name")
                print("3. Update email")
                print("4. Update password")
                print("5. Go back")
                choice_personal = int(input("Enter your choice: "))
                if choice_personal == 1:
                    new_fname = input("Enter your new first name: ")
                    update_first_name(member_id, new_fname)
                elif choice_personal == 2:
                    new_lname = input("Enter your new last name: ")
                    update_last_name(member_id, new_lname)
                elif choice_personal == 3:
                    new_email = input("Enter your new email: ")
                    update_email(member_id, new_email)
                elif choice_personal == 4:
                    new_password = input("Enter your new password: ")
                    update_password(member_id, new_password)
                elif choice_personal == 5:
                    break
                else:
                    print("Invalid choice.")
        elif choice == 2:
            while True:
                print("1. Update current weight")
                print("2. Update current height")
                print("3. Go back")
                choice_health = int(input("Enter your choice: "))
                if choice_health == 1:
                    new_weight = int(input("Enter your new weight in lbs: "))
                    update_weight(member_id, new_weight)
                elif choice_health == 2:
                    new_height = int(input("Enter your new height in cm: "))
                    update_height(member_id, new_height)
                elif choice_health == 3:
                    break
                else:
                    print("Invalid choice")
        elif choice == 3:
            while True:
                print("1. Add new fitness achievement")
                print("2. Delete fitness achievement")
                print("3. Go back")
                choice_achievement = int(input("Enter your choice: "))
                if choice_achievement == 1:
                    name = input("Enter fitness achievement name: ")
                    description = input("Enter fitness achievement description: ")
                    date = input("Enter fitness achievement date (yyyy-mm-dd): ")
                    add_fitness_achievement(member_id, name, description, date)
                elif choice_achievement == 2:
                    achievement_id = int(input("Enter the ID of achievement: "))
                    delete_fitness_achievement(member_id, achievement_id)
                elif choice_achievement == 3:
                    break
                else:
                    print("Invalid choice")
        elif choice == 4:
            while True:
                print("1. Add new goal")
                print("2. Update progress of goal")
                print("3. Delete goal")
                print("4. Go back")
                choice_goal = int(input("Enter your choice: "))
                if choice_goal == 1:
                    goal_name = input("Enter the goal name: ")
                    goal_status = input("Enter the status of goal (Not Started, In Progress, Completed): ")
                    add_goal(member_id, goal_name, goal_status)
                elif choice_goal == 2:
                    goal_id = input("Enter the ID of the goal: ")
                    goal_progress = input("Enter the progress of the goal: ")
                    update_goal(member_id, goal_id, goal_progress)
                elif choice_goal == 3:
                    goal_id_del = int(input("Enter the ID of the goal: "))
                    delete_goal(member_id, goal_id_del)
                elif choice_goal == 4:
                    break
                else:
                    print("Invalid choice")
        elif choice == 5:
            while True:
                print("1. Add new exercise into routine")
                print("2. Update exercise in routine")
                print("3. Delete exercise in routine")
                print("4. Go back")
                choice_exercise = int(input("Enter your choice: "))
                if choice_exercise == 1:
                    exercise_name = input("Enter the name of exercise: ")
                    exercise_reps = int(input("Enter the amount of reps: "))
                    exercise_sets = int(input("Enter the amount of sets: "))
                    add_exercise(member_id, exercise_name, exercise_reps, exercise_sets)
                elif choice_exercise == 2:
                    exercise_id = input("Enter the ID of the exercise: ")
                    reps = int(input("Enter the amount of reps: "))
                    sets = int(input("Enter the amount on sets: "))
                    update_exercise(member_id, exercise_id, reps, sets)
                elif choice_exercise == 3:
                    exercise_del = int(input("Enter the ID of the exercise: "))
                    delete_exercise(member_id, exercise_del)
                elif choice_exercise == 4:
                    break
                else:
                    print("Invalid choice")
        elif choice == 6:
            print("going back...")
            break
        else:
            print("Invalid choice.")


def member_schedule_management(member_id):
    while True:
        print("1. Personal training session management")
        print("2. Group class session management")
        print("3. Go back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            while True:
                print("1. View personal training sessions")
                print("2. View registered training sessions")
                #print("3. Join existing personal training session")
                print("3. Schedule personal training session")
                print("4. Cancel personal training session")
                print("5. Go back")
                choice_personal = int(input("Enter your choice: "))
                if choice_personal == 1:
                    display_personal_training_sessions()
                elif choice_personal == 2:
                    display_user_registered_sessions(member_id)
                #elif choice_personal == 3:
                    #session_id = int(input("Enter the ID of the existing session you'd like to join: "))
                    #register_training_session(member_id, session_id)
                elif choice_personal == 3:
                    trainer_id = int(input("Enter the ID of the trainer you would like to schedule with: "))
                    date = input("Enter the date you would like to schedule on (yyyy-mm-dd): ")
                    start = input("Enter the time you'd like the session to start (00:00): ")
                    end = input("Enter the time you'd like the session to end (00:00): ")
                    schedule_personal_training_session(trainer_id, member_id, date, start, end)
                elif choice_personal == 4:
                    cancelled_id = input("Enter the ID of the session you'd like to cancel: ")
                    cancel_personal_training_session(member_id, cancelled_id)
                elif choice_personal == 5:
                    break
                else:
                    print("Invalid choice")
        elif choice == 2:
            while True:
                print("1. View group fitness classes")
                print("2. View registered group fitness classes")
                print("3. Join group training session")
                print("4. Cancel group fitness training session")
                print("5. Go back")
                choice_group = int(input("Enter your choice: "))
                if choice_group == 1:
                    display_group_classes()
                elif choice_group == 2:
                    display_user_registered_group_sessions(member_id)
                elif choice_group == 3:
                    group_id = int(input("Enter the ID of the group training session you'd like to join: "))
                    register_group_classes(member_id, group_id)
                elif choice_group == 4:
                    group_id_cancel = int(input("Enter the ID of the group training session you'd like to cancel: "))
                    cancel_group_class(member_id, group_id_cancel)
                elif choice_group == 5:
                    break
                else:
                    print("Invalid choice")
        elif choice == 3:
            break
        else:
            print("Invalid choice")


def trainer_functions_menu():
    while True:
        print("1. Login")
        print("2. Back to main menu")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            trainer_id = trainer_login()
            if trainer_id:
                trainer_loggedin_options(trainer_id)
        elif choice == 2:
            break
        else:
            print("Invalid choice.")


def trainer_loggedin_options(trainer_id):
    while True:
        print("1. Schedule Management")
        print("2. Member Profile Viewing")
        print("3. Go back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            while True:
                print("1. View my availability")
                print("2. Update availability")
                print("3. Remove availability")
                print("4. Add availability")
                print("5. Go back")
                choice_tr = int(input("Enter your choice: "))
                if choice_tr == 1:
                    display_trainer_data(trainer_id)
                elif choice_tr == 2:
                    time_id = int(input("Enter the ID of the time slot you'd like to update: "))
                    date = input("Enter the new date you'd like to schedule for (yyyy-mm-dd): ")
                    start = input("Enter the new start time you'd like to schedule for (00:00): ")
                    end = input("Enter the new end time you'd like to schedule for (00:00): ")
                    update_trainer_time(time_id, date, start, end)
                elif choice_tr == 3:
                    time_id_del = input("Enter the ID of the time slot you'd like to delete: ")
                    delete_training_time(time_id_del)
                elif choice_tr == 4:
                    t_date = input("Enter the date you'd like to schedule for (yyyy-mm-dd): ")
                    t_start = input("Enter the start time you'd like to schedule for (00:00): ")
                    t_end = input("Enter the end time you'd like to schedule for (00:00): ")
                    add_training_time(trainer_id, t_date, t_start, t_end)
                elif choice_tr == 5:
                    break
                else:
                    ("Invalid choice")
        elif choice == 2:
            member_fname = input("Enter the first name of the member you'd like to search for: ")
            member_lname = input("Enter the last name of the member you'd like to search for: ")
            member_profile_viewing(member_fname, member_lname)

        elif choice == 3:
            break
        else:
            print("Invalid choice")


def admin_functions_menu():
    while True:
        print("1. Login")
        print("2. Back to main menu")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            admin_id = admin_login()
            if admin_id:
                admin_loggedin_options(admin_id)
        elif choice == 2:
            break
        else:
            print("Invalid choice.")


def admin_loggedin_options(admin_id):
    while True:
        print("1. Room booking management")
        print("2. Equipment maintenance monitoring")
        print("3. Class schedule updating")
        print("4. Billing")
        print("5. Register new trainer")
        print("6. Go back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            while True:
                print("1. View rooms")
                print("2. View trainer times")
                print("3. Add new booking")
                print("4. Remove booking")
                print("5. Go back")
                choice_room = int(input("Enter your choice: "))
                if choice_room == 1:
                    view_booked_rooms()
                elif choice_room == 2:
                    display_trainer_times()
                elif choice_room == 3:
                    trainer_id = int(input("Enter the ID of the trainer you'd like to book the room for: "))
                    room_number = int(input("Enter the room number of the room you'd like to book for: "))
                    booking_date = input("Enter the date you'd like to book for (yyyy-mm-dd): ")
                    booking_start_time = input("Enter the start time (00:00): ")
                    booking_end_time = input("Enter the end time (00:00): ")
                    add_room_booking(trainer_id, room_number, booking_date, booking_start_time, booking_end_time)
                elif choice_room == 4:
                    room_id = int(input("Enter the room number you'd like to remove the booking for: "))
                    delete_booked_room(room_id)
                elif choice_room == 5:
                    break
                else:
                    print("Invalid choice")
        elif choice == 2:
            while True:
                print("1. View equipment reports")
                print("2. Update report status")
                print("3. Add new equipment report")
                print("4. Delete equipment report")
                print("5. Go back")
                choice_equip = int(input("Enter your choice: "))
                if choice_equip == 1:
                    view_equipment()
                elif choice_equip == 2:
                    equipment_id = int(input("Enter the ID of the equipment you'd like to update: "))
                    equipment_status = input("Enter the updated status (Not fixed, In Progress, Fixed): ")
                    update_equipment_status(equipment_status, equipment_id)
                elif choice_equip == 3:
                    equipment_name = input("Enter the piece of equipments name: ")
                    equipment_cost = int(input("Enter the cost: "))
                    equipment_type = input("Enter the maintenance type: ")
                    equipment_statuss = input("Enter the status (Not fixed, In Progress, Fixed): ")
                    add_equipment(equipment_name, equipment_cost, equipment_type, equipment_statuss)
                elif choice_equip == 4:
                    id_equip = int(input('Enter the ID of the equipment report youd like to delete: '))
                    delete_equipment(id_equip)
                elif choice_equip == 5:
                    break
                else:
                    print("Invalid choice")
        elif choice == 3:
            while True:
                print("1. View group classes")
                print("2. View room schedule")
                print("3. View trainer schedule")
                print("4. Add new group class")
                print("5. Update group class")
                print("6. Delete group class")
                print("7. Go back")
                choice_group = int(input("Enter your choice: "))
                if choice_group == 1:
                    display_group_classes()
                elif choice_group == 2:
                    view_booked_rooms()
                elif choice_group == 3:
                    display_trainer_times()
                elif choice_group == 4:
                    group_name = input("Enter the name of the group class: ")
                    group_trainer = int(input("Enter the ID of the trainer you'd like to lead the class: "))
                    group_room = int(input("Enter the room you'd like to hold the class in: "))
                    group_date = input("Enter the date you'd like to hold the class on (yyyy-mm-dd): ")
                    group_start = input("Enter the time you'd like the class to start (00:00): ")
                    group_end = input("Enter the time you'd like the class to end (00:00): ")
                    add_new_group_class(group_name, group_trainer, group_room, group_date, group_start, group_end)
                elif choice_group == 5:
                    group_class_id = int(input("Enter the ID of the class you'd like to update: "))
                    group_trainer_id = int(input("Enter the ID of the trainer you'd like to schedule: "))
                    group_class_date = input("Enter the new date to schedule the class for (yyyy-mm-dd): ")
                    group_class_start = input("Enter the new start time you'd like to schedule the class for (00:00): ")
                    group_class_end = input("Enter the new end time you'd like to schedule the class for (00:00): ")
                    update_group_class_date(group_class_id, group_class_date, group_class_start, group_class_end, group_trainer_id)
                elif choice_group == 6:
                    id_cancelled = int(input("Enter the ID of the class you'd like to cancel: "))
                    delete_group_class(id_cancelled)
                elif choice_group == 7:
                    break
                else:
                    print("Invalid choice")

        elif choice == 4:
            while True:
                print("1. View all bills")
                print("2. Waive fee")
                print("3. Charge fee")
                print("4. Edit fee")
                print("5. Go back")
                choice_bill = int(input("Enter your choice: "))
                if choice_bill == 1:
                    display_billing()
                elif choice_bill == 2:
                    id_bill = int(input("Enter the ID of the bill you'd like to waive: "))
                    waive_fee(id_bill)
                elif choice_bill == 3:
                    id_member = int(input("Enter the ID of the member you'd like to charge: "))
                    fee_amount = int(input("Enter the amount you'd like to charge: "))
                    fee_type = input("Enter the reason for the fee: ")
                    charge_fee(id_member, fee_amount, fee_type)
                elif choice_bill == 4:
                    id_billing = int(input("Enter the ID of the bill you'd like to update: "))
                    id_members = int(input("Enter the ID of the member: "))
                    id_fee = int(input("Enter the amount you'd like to charge: "))
                    id_type = input("Enter the reason for the fee: ")
                    edit_fee(id_billing, id_members, id_fee, id_type)
                elif choice_bill == 5:
                    break
                else:
                    print("Invalid choice")
        elif choice == 5:
            create_trainer_account()
        elif choice == 6:
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()
