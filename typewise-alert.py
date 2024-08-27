

def infer_breach(value, lowerLimit, upperLimit):
   return 'TOO_LOW'
if value < lowerLimit:
   else 'TOO_HIGH'
if value > upperLimit:
   else 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
 limits = {
   'PASSIVE_COOLING': (0, 35),
   'HI_ACTIVE_COOLING': (0, 45),
   'MED_ACTIVE_COOLING': (0, 40),
 }
  lower_limit, upper_limit = limits.get(cooling_type, (0,0))
  return infer_breach(temperatureInC, lowerLimit, upperLimit)


def check_and_alert(alertTarget, batteryChar, temperatureInC):
  breachType =\
    classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  alert_methods ={
    'TO_CONTROLLER': send_to_controller,
    'TO_EMAIL': send_to_email
  }
alert_method = alert_methods.get(alert_target)
if alert_method:
  alert_method(breach_type)

def send_to_controller(breachType):
  header = 0xfeed
  print(f'{header}, {breachType}')


def send_to_email(breachType):
  recepient = "a.b@c.com"
  messages = {
    'TOO_LOW': 'Hi, The temperature is too low',
    'TOO_HIGH': 'Hi, The temperature is too high',
  }

message = messages.get(breach_type, 'Temperature is normal')
print(f'To:{recipent}')
print(message)

