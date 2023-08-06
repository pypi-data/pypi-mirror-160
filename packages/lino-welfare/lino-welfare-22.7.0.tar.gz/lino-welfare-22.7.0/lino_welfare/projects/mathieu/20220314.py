from lino.api.shell import *
from rstgen.utils import i2d

qs = coachings.Coaching.objects.filter(end_date__isnull=True, user__user_type="110")
for obj in qs:
    print(obj.id, obj.client, obj.user.username, obj.start_date)

#print(qs)
#qs.update(end_date=i2d(20220313))
#print(qs)
