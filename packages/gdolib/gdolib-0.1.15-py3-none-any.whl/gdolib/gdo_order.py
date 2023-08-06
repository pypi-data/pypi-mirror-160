class gdo_order:

    def headers_ssl(api: str) -> str:
        try:
            api = str(api)
            a1 = api.split(': ')[0]
            a2 = api.split(': ')[1]
            k = ("headers[" + "'" + a1 + "'" + "]=" + "'" + a2 + "'")
            m = (k.replace(" ", ""))
            return m
        except IndexError:
            return False

    def headers(api: str) -> str:
        try:
            api = str(api)
            a1 = api.split(': ')[0]
            a2 = api.split(': ')[1]
            ka = "'" + a1 + "':'" + a2 + "',"
            return ka
        except IndexError:
            return False

    def headers_config(api: str) -> str:
        try:
            asp = "  HEADER " + '"' + api + '"'
            return asp
        except IndexError:
            return False

    def edit_domin_email(email: str, domin: str) -> str:
        try:
            email = str(email)
            email = str(email.split("@")[0]) + str(domin)
            return email
        except IndexError:
            return False

    def add_domin_user(user: str, domin: str) -> str:
        user = str(user)
        if "@" in user:
            user = user.split('@')[0]
            email = user + domin
            return email
        else:
            email = user + domin
            return email

    def del_domin_email(email: str) -> str:
        email = str(email)
        if "@" in email:
            azoz = email.split("@")[0]
            return azoz
        else:
            azoz = email
            return azoz

# -------------------------[CoDe BY GDØ]------------------------
# -------------------------[CoDe BY GDØ]------------------------
# -------------------------[CoDe BY GDØ]------------------------
