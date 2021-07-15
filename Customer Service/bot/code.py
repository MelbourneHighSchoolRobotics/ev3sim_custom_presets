# The users dictionary stores the user id, and the corresponding user information, such as plan / full name.
users = {}
# The plans dictionary stores the plan name, and the corresponding users on that plan.
plans = {}

def create_plan(plan_name):
    # Create the plan. Originally, it has no users.
    plans[plan_name] = []

def create_user(user_id, full_name, plan_name):
    # Create the user object.
    users[user_id] = {"full_name": full_name, "plan": full_name}
    # Add them to the plan list.
    plans[plan_name].append(user_id)

def get_user_plan(user_id):
    # Return the user's plan.
    return users[user_id]["plan"]

def set_user_plan(user_id, plan_name):
    # Remove the user from the old plan and update the user's plan
    old_plan = get_user_plan(user_id)
    plans[old_plan].remove(user_id)
    # Update the user's plan.
    users[user_id]["plan"] = plan_name

while True:
    msg = input()
    if msg == "That's all for today":
        # We are done for the day. End program.
        break
    elif "Can you create a new plan" in msg:
        # Can you create a new plan called <plan_name> please.
        plan_name = msg.split()[-2]
        create_plan(plan_name)
    elif "We have a new user" in msg:
        # 0  1    2 3   4    5      6      7      8    9       10    11   12   13 14   15
        # We have a new user called <full> <name> with user_id <id>. They want to join <plan>.
        full_name = msg.split()[6] + " " + msg.split()[7]
        # Avoid full stops.
        user_id = msg.split()[10][:-1]
        plan = msg.split()[15][:-1]
        create_user(user_id, full_name, plan)
    elif "wants to change their plan" in msg:
        # <user_id> wants to change their plan to <plan_name>.
        user_id = msg.split()[0]
        # Avoid full stop.
        new_plan = msg.split()[-1]
        set_user_plan(user_id, new_plan)
    elif "wants to know if they" in msg:
        # <user_id> wants to know if they are still on <plan_name>.
        user_id = msg.split()[0]
        # Avoid full stop.
        plan_name = msg.split()[-1][:-1]
        actual_plan = get_user_plan(user_id)
        if actual_plan == plan_name:
            print("Yes they are")
        else:
            print(f"No they aren't. They are on {actual_plan} now.")
    elif "How many" in msg:
        # How many people are currently on the <plan_name> plan?
        plan_name = msg.split()[-2]
        print(f"There are {len(plans[plan_name])} people on {plan_name}.")
