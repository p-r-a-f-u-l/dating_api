from users.models import ZodiocModel, zodio


def create_Zodioc():
    zodio = ZodiocModel.objects.all()
    if zodio.count() < zodio.__len__():
        ZodiocModel.objects.bulk_create([ZodiocModel(horo=n) for n in zodio])
