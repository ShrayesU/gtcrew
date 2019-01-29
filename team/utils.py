STUDENT = 'student'
COACH = 'coach'
ALUMNI = 'alumni'
HELD_BY_CHOICES = (
    (STUDENT, 'Student'),
    (COACH, 'Coach'),
    (ALUMNI, 'Alumni'),
)

FALL = 'FALL'
SPRING = 'SPRING'
SEMESTER_CHOICES = (
    (FALL, 'Fall'),
    (SPRING, 'Spring'),
)

DEFAULT = 'BASE'
HOME = 'HOME'
ABOUT = 'ABOUT'
TEAM = 'TEAM'
TEMPLATE_CHOICES = (
    (DEFAULT, 'Regular'),
    (HOME, 'Home'),
    (ABOUT, 'About'),
    (TEAM, 'Team'),
)

TEAM_FOUNDED = 1985
