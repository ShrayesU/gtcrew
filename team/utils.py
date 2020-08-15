# from django.utils.translation import ugettext_lazy as _

UNCLAIMED = 'unclaimed'
PENDING = 'pending'
APPROVED = 'approved'
PROFILE_STATUS_CHOICES = (
    (UNCLAIMED, 'Unclaimed'),
    (PENDING, 'Pending Approval'),
    (APPROVED, 'Approved')
)

STUDENT = 'student'
COACH = 'coach'
ALUMNI = 'alumni'
RACER = 'racer'
HELD_BY_CHOICES = (
    (STUDENT, 'Student'),
    (COACH, 'Coach'),
    (ALUMNI, 'Alumni'),
    (RACER, 'Racer'),
)

FALL = 'FALL'
SPRING = 'SPRING'
SEMESTER_CHOICES = (
    (FALL, 'Fall'),
    (SPRING, 'Spring'),
)

TEAM_FOUNDED = 1985

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)
