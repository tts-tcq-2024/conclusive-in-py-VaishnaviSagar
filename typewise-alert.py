def infer_breach(value, lower_limit, upper_limit):
    return 'TOO_LOW' if value < lower_limit else 'TOO_HIGH' if value > upper_limit else 'NORMAL'


def classify_temperature_breach(cooling_type, temperature_in_c):
    limits = {
        'PASSIVE_COOLING': (0, 35),
        'HI_ACTIVE_COOLING': (0, 45),
        'MED_ACTIVE_COOLING': (0, 40)
    }
    
    lower_limit, upper_limit = limits.get(cooling_type, (0, 0))
    return infer_breach(temperature_in_c, lower_limit, upper_limit)


def check_and_alert(alert_target, battery_char, temperature_in_c):
    breach_type = classify_temperature_breach(battery_char['coolingType'], temperature_in_c)
    alert_methods = {
        'TO_CONTROLLER': send_to_controller,
        'TO_EMAIL': send_to_email
    }
    
    alert_method = alert_methods.get(alert_target)
    if alert_method:
        alert_method(breach_type)


def send_to_controller(breach_type):
    header = 0xfeed
    print(f'{header}, {breach_type}')


def send_to_email(breach_type):
    recipient = "a.b@c.com"
    messages = {
        'TOO_LOW': 'Hi, the temperature is too low',
        'TOO_HIGH': 'Hi, the temperature is too high'
    }
    
    message = messages.get(breach_type, 'Temperature is normal')
    print(f'To: {recipient}')
    print(message)
