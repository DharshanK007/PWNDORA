import os
import sys
from faker import Faker
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

fake = Faker()

def get_random_enum_value(enum_class):
    return random.choice(list(enum_class))
