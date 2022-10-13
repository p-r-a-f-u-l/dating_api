from termcolor import colored
from django.contrib.auth import get_user_model

User = get_user_model()


class LoggerMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        print("\n")
        print(colored(" =" * 30, "white", attrs=["bold"]))
        print(colored(f"IP : {request.META.get('REMOTE_ADDR')}", "red", attrs=["bold"]))
        # print(colored(f"{request.user}", "green", attrs=["bold"]))

        ip_address = request.META.get("REMOTE_ADDR")
        userAgent = request.META.get("HTTP_USER_AGENT")

        print(colored(f"{ip_address}", "yellow", attrs=["bold"]))
        print(colored(" =" * 30, "white", attrs=["bold"]))

        # if request.path == "/rec/":
        #     user = UserConf.objects.filter(owner=request.user).first()
        #     relaodtime = user.reloadLimit - 1
        #     UserConf.objects.filter(owner=request.user).update(reloadLimit=abs(relaodtime))

        if ip_address:
            user = User.objects.filter(id=request.user.id)
            if user is not ip_address:
                User.objects.filter(id=request.user.id).update(last_ip=ip_address, ua=userAgent)

        # response["server"] = "Micro-Bot"

        return response
