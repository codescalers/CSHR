

def run():
    from server.cshr.models.users import User
    from server.cshr.models.vacation_balance import VacationBalance
    from server.cshr.utils.vacation_balance_helper import VacationBalanceHelper
    v = VacationBalanceHelper()
    u = User.objects.get(pk=13)
    v.update('annual_leaves', u.vacationbalance, 2)

run()