from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
class ListUsers(ListView):
    model = Usuario
    template_name = 'users/index.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(ListUsers, self).dispatch(request, *args, **kwargs)
        return redirect('login')
        

class CreateUser(CreateView):
    model = Usuario
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        instance = form.instance
        instance.username = instance.email
        instance.set_password(instance.password)
        return super(CreateUser, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(CreateUser, self).dispatch(request, *args, **kwargs)
        return redirect('login')    

class EditUser(UpdateView):
    model = Usuario
    template_name = 'users/edit.html'
    form_class = UserForm
    success_url = reverse_lazy('users/index.html')

    def form_valid(self, form):
        instance = form.instance
        instance.username = instance.email
        return super(EditUser, self).form_valid(form)
        
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(EditUser, self).dispatch(request, *args, **kwargs)
        return redirect('login')    

def delete_user(request, id):
    user = Usuario.objects.get(id = id)
    user.delete()
    return redirect('users')

def upload_user(request):
    if request.method == 'POST':
        df = pd.read_excel(request.FILES['xlsUser'])
        data = pd.DataFrame(df, columns= ['RUT', 'Nombres', 'Dirección de correo electrónico', 
                                    'Primer apellido', 'Segundo apellido', 'Género'])

        estado = Estado.objects.get(idEstado = 1)
        rol = Rol.objects.filter(idRol = 1)
        for user in range(len(data)):
            rut = data.iloc[user, 0]
            nombres = data.iloc[user, 1]
            email = data.iloc[user, 2]
            apellido_p = data.iloc[user, 3]
            apellido_m = data.iloc[user, 4]
            sexo = data.iloc[user, 5]
            value = Usuario(
                is_superuser = 1,
                username = email,
                first_name = "",
                last_name = "",
                is_staff = 1,
                is_active = 1,
                date_joined = datetime.now(),
                rut = rut,
                nombres = nombres,
                apellido_paterno = apellido_p,
                apellido_materno = apellido_m,
                email = email,
                telefono = 0,
                sexo = sexo,
                fecha_nacimiento = '1950-01-01',
                created_at = datetime.now(),
                update_at = datetime.now(),
                estado = estado
            )
            value.set_password('test')
            value.save()
        return redirect('users')    