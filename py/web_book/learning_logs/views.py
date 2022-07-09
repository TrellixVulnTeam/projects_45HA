from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm

# Create your views here

def index(request):
    # Pagina inicial de Leaning Log
    return render(request, 'learning_logs/index.html')

# A função exige um parâmetro: o objeto request recebido do servidor
def topics(request): # Mostra todos os assuntos
    
    # Então consultamos o banco de dados solicitando objetos topic com 
        # atributo date_added
        # armazenamos o queryset resultante em topics
    topics = Topic.objects.order_by('date_added')

    # Definimos o contexto enviado ao template
    # Contexto é um dicionário em que:

        # chaves = nomes que usaremos no template para acessar dados;
        # valores = dados que devemos enviar ao template.
        # neste caso há apenas um par chave e valor, que são os assuntos
    context = {'topics': topics}

    # Ao construir um página que use dados, passamos context ao Render, além do objeto
    # request e path do template
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id): # Mostra um assunto e todas as suas entradas

    topic = Topic.objects.get(id=topic_id)

    #-date_added exibe a data da Mais Recente para a Menos Recente
    entries = topic.entry_set.order_by("-date_added")
    context = {'topic' : topic, 'entries' : entries}
    
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):

    if request != 'POST': 
        # Nenhum dado submetido. Cria um formulário em branco
        form = TopicForm()
    else:
        # Dados submetidos, processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}

    return render(request, 'learning_logs/new_topic.html', context)