def debug():
    from django.contrib.auth.models import User
    user = User.objects.filter(groups__name='Manager')

    for manager in user:
        # print(dir(manager))
        print(manager.first_name + ' - ' + manager.last_name)
    