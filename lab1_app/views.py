from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

def user():
    try:
        user1 = AuthUser.objects.get(id=1)
    except:
        user1 = AuthUser(id=1, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1

class ComponentList(APIView):
    model_class = Component
    serializer_class = ComponentSerializer
    
    # GET список с фильтрацией. В списке услуг возвращается 
    # id заявки-черновика этого пользователя для страницы 
    # заявки и количество услуг в этой заявке
    
    def get(self, request, format=None):
        input_down = request.query_params.get('down', '')
        input_up = request.query_params.get('up', '')
        if input_down == '':
            input_down = '0'
        if input_up == '':
            input_up = '999999999999'
        resultComponents = Component.objects.filter(price__range=(int(input_down), int(input_up)))
        
        curUserObject = user()
        curAssemblyObject = Assembly.objects.filter(status='draft', creator=curUserObject).first()
        componentsInAssembly = MM.objects.filter(idAssembly=curAssemblyObject)
    
        if not curAssemblyObject:
            assemblyId = 0
        else:
            assemblyId = curAssemblyObject.pk

        if input_down == '0':
            input_down = ''
        if input_up == '999999999999':
            input_up = ''
        
        
        components = self.model_class.objects.all()
        serializer = self.serializer_class(components, many=True)
        return Response(serializer.data)
    # add filter

    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComponentDetail(APIView):
    model_class = Component
    serializer_class = ComponentSerializer

    
    def get(self, request, pk, format=None):
        component = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(component)
        return Response(serializer.data)

    
    def put(self, request, pk, format=None):
        component = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(component, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk, format=None):
        component = get_object_or_404(self.model_class, pk=pk)
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # add minio

# Обновляет информацию об акции (для пользователя)    
@api_view(['Put'])
def put(self, request, pk, format=None):
    component = get_object_or_404(self.model_class, pk=pk)
    serializer = self.serializer_class(component, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



curUser = 1

def GetMain(request):
    input_down = request.GET.get('down', '')
    input_up = request.GET.get('up', '')
    if input_down == '':
        input_down = '0'
    if input_up == '':
        input_up = '999999999999'
        
    resultComponents = Component.objects.filter(price__range=(int(input_down), int(input_up)))
    curUserObject = get_user_model().objects.get(pk=curUser)
    curAssemblyObject = Assembly.objects.filter(status='draft', creator=curUserObject).first()
    componentsInAssembly = MM.objects.filter(idAssembly=curAssemblyObject)
    
    if not curAssemblyObject:
        assemblyId = 0
    else:
        assemblyId = curAssemblyObject.pk

    if input_down == '0':
        input_down = ''
    if input_up == '999999999999':
        input_up = ''
        
    return render(request, 'main.html', {'data' : {
        'components': resultComponents,
        'price_down': input_down,
        'price_up': input_up,
        'cart_counter': len(componentsInAssembly),
        'assemblyId': assemblyId
    }})    
    
def GetComponent(request, id):
    this_component = Component.objects.get(pk=id)
    return render(request, 'component.html', {'data' : {
        'id': this_component.id,
        'title': this_component.title,
        'description': this_component.description,
        'price': this_component.price,
        'imgSrc': this_component.imgSrc
    }})
    
def GetAssembly(request, id):
    try:
        curAssemblyObject = Assembly.objects.get(pk=id)
        componentsInAssembly = MM.objects.filter(idAssembly=curAssemblyObject).select_related('idComp')
    except:
        componentsInAssembly = {}
        
    if curAssemblyObject.status == 'deleted':
        raise Http404("Сборка удалена!") 
        
    if curAssemblyObject.satelliteName == None:
        name = ''
    else:
        name = curAssemblyObject.satelliteName
        
    if curAssemblyObject.flyDate == None:
        date = ''
    else:
        date = curAssemblyObject.flyDate
    
    return render(request, 'assembly.html', {'data' : {
        'components': componentsInAssembly,
        'assemblyId': curAssemblyObject.id,
        'name': name,
        'date': date
    }})
    
def AddAssembly(request):
    compId = request.POST['componentId']
    curComponentObject = Component.objects.get(pk=compId)
    print(compId)
    
    curUserObject = get_user_model().objects.get(pk=curUser)
        
    try:
        curAssemblyObject = Assembly.objects.get(status='draft', creator=curUserObject)
    except:
        curAssemblyObject = Assembly(creator = curUserObject)
        curAssemblyObject.save()
    
    componentsInAssembly = MM.objects.filter(idAssembly=curAssemblyObject)
    
    try:
        curMMObject = MM.objects.get(idComp=curComponentObject, idAssembly=curAssemblyObject)
        if curMMObject in componentsInAssembly:
            curMMObject.count += 1
            curMMObject.save()
            print('if')
        print('try')
    except:
        addedComponent = MM(idComp=curComponentObject, idAssembly=curAssemblyObject, count=1)
        addedComponent.save()
        print('except')
        #componentsInAssembly = MM.objects.filter(idAssembly=curAssemblyObject)
    
    return redirect('main')

def DelAssembly(request):
    assemblyId = request.POST['assemblyId']
    c = connection.cursor()
    c.execute("update lab1_app_assembly set status = 'deleted' where id = %s", [assemblyId])
    transaction.commit()
    c.close()
    return redirect('main')
    