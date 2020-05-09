import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import DateField, SelectDateWidget
from django.shortcuts import render
from taskmanager.models import Project, Task, Journal, Status
from taskmanager.forms import NewTaskForm, NewJournalForm
from django.http import HttpResponse

from .resources import ProjectResource, StatusResource, TaskResource, JournalResource


def home(request):  # Page D'acceuille
    if request.user.is_authenticated:  # Si l'utilisateur est connectee on receuille ses donnees, qui passeront a la vue
        user = request.user
        projects = Project.objects.all()
    return render(request, 'home.html', locals())


def projectprogress(project):
    list_tasks = Task.objects.filter(project=project)
    i = 0
    progress = 0
    for task in list_tasks:
        i += 1
        progress += task.progress
    if i == 0:
        i = 1
    return (int(progress / i))


# View for the list of projects
@login_required
def projects(request):
    projects = Project.objects.all()
    user = request.user
    list_projects = []  # Each cell of list_projects will contains information about a project
    infos = []  # the info cell of a project
    count = 0
    for project in Project.objects.filter(members=user):
        infos.append(
            list(Project.objects.filter(members=user))[count])  # 1st cell of infos contains the members of the project
        infos.append(Task.objects.filter(project=project))  # 2nd cell of infos contains the tasks of the project
        infos.append(Task.objects.filter(project=project).order_by(
            "due_date"))  # 3rd cell of infos contains the tasks of the project ordered by due_date
        list_projects.append(infos)  # add the infos cells in the list of projects
        infos = []
        count += 1
    return render(request, 'list_projects.html', locals())


# View for the display of a project and its details
@login_required
def project(request, id_project):
    members = User.objects.all()
    projects = Project.objects.all()
    user = request.user
    project = Project.objects.get(id=id_project)
    list_tasks = Task.objects.filter(project=project)  # List of the tasks of this project
    progress = projectprogress(project)

    # # Now we apply more filters if the user requested some...
    # if (request.method == "GET") and ('member' in request.GET):
    #     query = request.GET.getlist("member")
    #     query_list = [User.objects.all().get(username=m) for m in query]
    #     list_tasks = list_tasks.filter(assignee__in=query_list)
    # list_tasks = ordering(request, list_tasks)
    list_tasks, status_q_list, query_list, date1, date2, date3, date4 = filters(request, list_tasks)

    # Needed for the template and form...
    Status_all = Status.objects.all()
    return render(request, 'project.html', locals())


# View for the display of a task and its details
@login_required
def task(request, id_task):
    projects = Project.objects.all()
    user = request.user
    task = Task.objects.get(id=id_task)
    project = Project.objects.get(id=task.project.id)
    list_journals = Journal.objects.filter(task=task)  # List of the Journal entries of this task
    return render(request, 'task.html', locals())


# View to fill a form to create a task and add it to the database
@login_required
def newtask(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            project = form['project'].value()
            return task(request, form.instance.id)  # if the form is valid, save it in database and display the new task
        else:  # if not, initialize the form and display the form
            form = NewTaskForm()
            list_projects = Project.objects.all()
            list_users = User.objects.all()
            list_status = Status.objects.all()
            return render(request, 'newtask.html', locals())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newtask.html', locals())


# View to update a task
@login_required
def updatetask(request, id_task):
    utask = Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST, instance=utask)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            # Get the data from the form
            utask.project = form.cleaned_data['project']
            utask.name = form.cleaned_data['name']
            utask.description = form.cleaned_data['description']
            utask.assignee = form.cleaned_data['assignee']
            utask.due_date = form.cleaned_data['due_date']
            utask.start_date = form.cleaned_data['start_date']
            utask.priority = form.cleaned_data['priority']
            utask.status = form.cleaned_data['status']
            utask.save()  # Update data in database

            project = form['project'].value()

            return task(request, utask.id)  # Display the updated task

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm(request.POST, instance=utask)
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'updatetask.html', locals())


# View to add a new journal entry
@login_required
def newjournal(request, id_task):
    jtask = Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewJournalForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # save
            # redirect to a new URL:
            form.save()
            return task(request, jtask.id)
        else:
            form = NewJournalForm()
            list_projects = Project.objects.all()
            list_users = User.objects.all()
            list_status = Status.objects.all()

        return render(request, 'newjournal.html', locals())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewJournalForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newjournal.html', locals())


@login_required
def mytasks(request):
    members = User.objects.all()
    projects = Project.objects.all()
    # First we check if a search was made, i.e if the Get request contains a "query" element
    if (request.method == "GET") and ("query" in request.GET):
        query = request.GET["query"]
        query_list = query.split()
        user = request.user
        list_tasks = Task.objects.filter(name__contains=query)
    # Else we just show the user all of HIS tasks
    else:
        user = request.user
        list_tasks = Task.objects.filter(assignee=user)
        list_projects = Project.objects.filter(members=user)
        chart_data = []
        for project in list_projects:
            chart_data.append(Task.objects.filter(assignee=user, project=project).count())
    return render(request, 'mytasks.html', locals())


@login_required
def donetasks(request):
    projects = Project.objects.all()
    user = request.user
    done_status = Status.objects.get(name="Terminée")
    list_tasks = Task.objects.filter(assignee=user, status=done_status)
    return (render(request, 'donetasks.html', locals()))


@login_required
def activity(request, id_project):
    user = request.user
    project = Project.objects.get(id=id_project)
    list_journals = Journal.objects.filter(task__project=project).order_by('-date')
    list_members = Project.objects.get(id=id_project).members.all()
    contributions = []
    for member in list_members:
        contributions.append(
            nb_contribution(User.objects.get(username=member.username), Project.objects.get(id=id_project)))

    return (render(request, 'activity.html', locals()))


@login_required
def gantt(request, id_project):
    list_members = Project.objects.get(id=id_project).members.all()
    contributions = []
    for member in list_members:
        contributions.append(
            nb_contribution(User.objects.get(username=member.username), Project.objects.get(id=id_project)))
    return (render(request, 'gantt.html', locals()))


def nb_contribution(user, project):
    n = Journal.objects.filter(task__project=project, author=user).count()
    return (n)


@login_required
def export(request):
    dataset_p = ProjectResource().export()
    dataset_s = StatusResource().export()
    dataset_t = TaskResource().export()
    dataset_j = JournalResource().export()
    response = HttpResponse({dataset_p.csv, dataset_s.csv, dataset_t, dataset_j}, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    return response


########Analog function for better readability, used for filtering queries #####------Ne fonctionne pas encore
def ordering(request, task_query_set):
    if (request.method == "GET") and ('sort' in request.GET):
        query = request.GET["sort"]
        q = query.split()
        if q[1] == "up":
            task_query_set.filter().order_by(q[0])
        else:
            task_query_set.order_by('-' + q[0])
    return task_query_set


def filters(request, list_tasks):
    # Initialisation des variables pour pouvoir return une liste vide si on a pas les methodes get necessaires..
    status_q_list = []
    query_list = []

    date1 = datetime.datetime.today().date()
    date2 = datetime.datetime.today().date()
    date3 = datetime.datetime.today().date()
    date4 = datetime.datetime.today().date()

    # cette partie sert simplement a convertir les placehholder dans le bon format pour django
    date1 = date1.isoformat()
    date2 = date2.isoformat()
    date3 = date3.isoformat()
    date4 = date4.isoformat()

    # On verifie si l'utilisateur a voulu filtrer selon le status ou pas
    if (request.method == "GET") and ('status' in request.GET):
        status_q = request.GET.getlist("status")
        status_q_list = [Status.objects.all().get(name=s) for s in status_q]
        list_tasks = list_tasks.filter(status__in=status_q_list)
    # On verifie si l'utilisateur a voulu filtrer selon les membres ou pas
    if (request.method == "GET") and ('member' in request.GET):
        query = request.GET.getlist("member")
        query_list = [User.objects.all().get(username=m) for m in query]
        list_tasks = list_tasks.filter(assignee__in=query_list)
    # On verifie si l'utilisateur a voulu filtrer selon les dates, je verifie donc si "date1" est incluse, et je receuille quand meme les autres, ou pas
    if (request.method=="GET" and ('date1' in request.GET)):
        date1 = request.GET["date1"]
        date2 = request.GET["date2"]
        date3 = request.GET["date3"]
        date4 = request.GET["date4"]
        #Rmq: comme la requete "date" est toujurs presente si on submit une recherche, je ne filtre que sur celles qui sont non nulles....
        if date1 != '':
            list_tasks = list_tasks.filter(start_date__gte=date1)
        if date2 != '':
            list_tasks = list_tasks.filter(start_date__lte=date2)
        if date3 != '':
            list_tasks = list_tasks.filter(due_date__gte=date3)
        if date4 != '':
            list_tasks = list_tasks.filter(due_date__lte=date4)
    # Enfin ces retours sont utilisés pour le template, pour une meilleure ergonomie je garde affichée les parametres de la recherche precendete.
    return (list_tasks, status_q_list, query_list, date1, date2, date3, date4)


