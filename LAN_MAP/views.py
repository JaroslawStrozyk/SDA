from django.shortcuts import render, redirect
from .models import Lan
from django.conf import settings

#
# https://tutorial101.blogspot.com/2022/05/python-django-mysql-crud-create-read.html
#


def LanView(request):
    name_log = request.user.first_name + " " + request.user.last_name
    about = settings.INFO_PROGRAM
    return render(request, 'LAN_MAP/lan_main.html', {
        'name_log': name_log,
        'about': about,
    })


def LanAdd(request):
    member = Lan(ip=request.POST['ip'],
                 nazwa=request.POST['nazwa'],
                 typ=request.POST['typ'],
                 opis=request.POST['opis'],
                 uwagi=request.POST['uwagi'])
    member.save()
    return redirect('lan_start')


def LanRead(request):
    members = Lan.objects.all().order_by('-ip')
    context = {'members': members}
    return render(request, 'LAN_MAP/result.html', context)


def LanEdit(request, id):
    members = Lan.objects.get(id=id)
    context = {'member': members}
    return render(request, 'LAN_MAP/edit.html', context)


def LanUpdate(request, id):
    member = Lan.objects.get(id=id)
    member.ip = request.POST['ip']
    member.nazwa = request.POST['nazwa']
    member.typ = request.POST['typ']
    member.opis = request.POST['opis']
    member.uwagi = request.POST['uwagi']
    member.save()
    return redirect('lan_start')


def LanDelete(request, id):
    member = Lan.objects.get(id=id)
    member.delete()
    return redirect('lan_start')



















# class LanView(ListView):
#     model = Lan
#     template_name = 'LAN_MAP/lan_main.html'
#     context_object_name = 'lany'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tytul_tabeli'] = "Lista adresów IP z sieci LAN"
#         context['about'] = settings.INFO_PROGRAM
#         context['name_log'] = self.request.user.first_name + " " + self.request.user.last_name
#         return context
#
#
# class CreateLan(View):
#     def  get(self, request):
#         ip1 = request.GET.get('ip', None)
#         nazwa1 = request.GET.get('nazwa', None)
#         typ1 = request.GET.get('typ', None)
#         opis1 = request.GET.get('opis', None)
#         uwagi1 = request.GET.get('uwagi', None)
#
#         obj = Lan.objects.create(
#             ip = ip1,
#             nazwa = nazwa1,
#             typ = typ1,
#             opis = opis1,
#             uwagi = uwagi1
#         )
#
#         lan = {'id':obj.id, 'ip':obj.ip, 'nazwa':obj.nazwa, 'typ':obj.typ, 'opis':obj.opis, 'uwagi':obj.uwagi}
#         data = {
#             'lan': lan
#         }
#         return JsonResponse(data)
#
#
# class UpdateLan(View):
#     def  get(self, request):
#         id1 = request.GET.get('id', None)
#         ip1 = request.GET.get('ip', None)
#         nazwa1 = request.GET.get('nazwa', None)
#         typ1 = request.GET.get('typ', None)
#         opis1 = request.GET.get('opis', None)
#         uwagi1 = request.GET.get('uwagi', None)
#
#         print("DANE WEJ: " + id1 + ", " + ip1 + ", " + nazwa1 + ", " + typ1 + ", " + opis1 + ", " + uwagi1);
#
#         obj = Lan.objects.get(id=id1)
#         obj.ip = ip1,
#         obj.nazwa = nazwa1,
#         obj.typ = typ1,
#         obj.opis = opis1,
#         obj.uwagi = uwagi1
#         obj.save()
#
#         lan = {'id':obj.id, 'ip':obj.ip, 'nazwa':obj.nazwa, 'typ':obj.typ, 'opis':obj.opis, 'uwagi':obj.uwagi}
#         data = {
#             'lan': lan
#         }
#         return JsonResponse(data)
#
#
# class DeleteLan(View):
#     def  get(self, request):
#         id1 = request.GET.get('id', None)
#         Lan.objects.get(id=id1).delete()
#         data = {
#             'deleted': True
#         }
#         return JsonResponse(data)
