from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.tasks import cache_a_staff_group_perms


class Command(BaseCommand):
    help = "Caching each users aggregate groups permissions"

    def handle(self, *args, **options):
        try:
            Staff = get_user_model()
            staffs = Staff.objects.all()
            for staff in staffs:
                cache_a_staff_group_perms.delay(staff.id)

            self.stdout.write(self.style.SUCCESS("User permissions are being cached"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(e))

