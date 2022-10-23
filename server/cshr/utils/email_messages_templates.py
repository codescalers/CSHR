from server.cshr.models.users import User


def get_vacation_request_email_template(user: User, data, url) -> str:
    msg = """Request information:
   Applying user: {user_fname} {user_lname}
   Reason: {reason}
   Start date : {start_date}
   End Date : {end_date}
   Status :{status}
   Request Url: {request_url}""".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        reason=data["reason"],
        start_date=data["from_date"],
        end_date=data["end_date"],
        status=data["status"],
        request_url=url,
    )
    return msg


def get_hr_letter_request_email_template(user: User, data, url) -> str:
    msg = """Request information:
    Applying user: {user_fname} {user_lname}
    Addresses : {addresses}
    Status :{status}
    Request Url: {request_url}""".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        addresses=data["addresses"],
        status=data["status"],
        request_url=url,
    )
    return msg

def get_official_document_request_email_template(user: User, data, url) -> str:
    msg = """Request information:
    Applying user: {user_fname} {user_lname}
    Addresses : {document}
    Status :{status}
    Request Url: {request_url}""".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        document=data["document"],
        status=data["status"],
        request_url=url,
    )
    return msg


def get_compensation_request_email_template(user: User, data, url) -> str:
    msg = """Request information:
    Applying user: {user_fname} {user_lname}
    Reason: {reason}
    Start date : {start_date}
    End Date : {end_date}
    Status :{status}
    Request Url: {request_url}""".format(
        user_fname=user.first_name,
        user_lname=user.last_name,
        reason=data["reason"],
        start_date=data["from_date"],
        end_date=data["end_date"],
        status=data["status"],
        request_url=url,
    )
    return msg


def get_vacation_reply_email_template(approving_user: User, data, url) -> str:
    msg = """Request information:
   Approving user: {user_fname} {user_lname}
   Reason: {reason}
   Start date : {start_date}
   End Date : {end_date}
   Status :{status}
   Request Url: {request_url}""".format(
        user_fname=approving_user.first_name,
        user_lname=approving_user.last_name,
        reason=data.reason,
        start_date=data.from_date,
        end_date=data.end_date,
        status=data.status,
        request_url=url,
    )
    return msg


def get_hr_letter_reply_email_template(approving_user: User, data, url) -> str:
    msg = """Reply information:
    Approving user: {user_fname} {user_lname}
    Addresses : {addresses}
    Status :{status}
    Request Url: {request_url}""".format(
        user_fname=approving_user.first_name,
        user_lname=approving_user.last_name,
        addresses=data.addresses,
        status=data.status,
        request_url=url,
    )
    return msg


def get_compensation_reply_email_template(approving_user: User, data, url) -> str:
    msg = """Reply information:
    Approving user: {user_fname} {user_lname}
    Reason: {reason}
    Start date : {start_date}
    End Date : {end_date}
    Status :{status}
    Request Url: {request_url}""".format(
        user_fname=approving_user.first_name,
        user_lname=approving_user.last_name,
        reason=data.reason,
        start_date=data.from_date,
        end_date=data.end_date,
        status=data.status,
        request_url=url,
    )
    return msg
