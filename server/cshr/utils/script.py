

def run():
    from server.cshr.models.users import User
    from server.cshr.models.vacation_balance import VacationBalance
    from server.cshr.utils.vacation_balance_helper import VacationBalanceHelper
    v = VacationBalanceHelper()
    u = User.objects.get(pk=1)
    v.old_balance_format(u)
    # print(v.read().get('annual_leaves'))
    # v.write(
    #     {
    #         'annual_leaves': 15,
    #         'sick_leaves': 100,
    #         'compensation': 0,
    #         'unpaid': 0,
    #         'emergencies': 6,
    #         'leave_execuses': 3,
    #         'public_holidays': 0,
    #         "year": 2022
    #     }
    # )
    # u = User.objects.get(pk=1)
    # v.check(u)
    # v.update('annual_leaves', u.vacationbalance, 16)

run()