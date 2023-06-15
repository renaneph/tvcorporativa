from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VisualContent, Campaign, ContentCampaign
from django.contrib import messages
from user.models import UserProfile
from datetime import date, datetime
from django.http import JsonResponse
from json import dumps
from django.core.exceptions import PermissionDenied

# Create your views here.

LIST_EXTENSION_IMAGES = [
    'image/jpeg',
    'image/png'
]


LIST_EXTENSION_VIDEO = [
    'video/mp4'
]


@login_required(login_url='/login')
def table_contents(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    contents = VisualContent.objects.all()
    return render(request, 'visual_contents.html', {'contents': contents, 'type_user': user.type_user})


@login_required(login_url='/login')
def register_content(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    context = {'type_user': user.type_user, 'form': request.POST}

    if request.method == "GET":
        return render(request, 'register_contents.html', context)

    name = request.POST.get('name')
    type_content = request.POST.get('type-content')
    content = request.FILES.get('content')
    status = request.POST.get('customRadio')

    if content.content_type not in LIST_EXTENSION_IMAGES and content.content_type not in LIST_EXTENSION_VIDEO:
        messages.warning(request, 'Erro: O tipo de arquivo não é permitido!')
    elif type_content == 'IE' and content.content_type in LIST_EXTENSION_VIDEO or type_content == 'ID' and content.content_type in LIST_EXTENSION_IMAGES:
        messages.warning(request, 'Erro: O tipo de arquivo para o conteúdo visual selecionado não é válido!')
    else:
        VisualContent.objects.create(name=name, type_content=type_content, content=content, status=status)
        return redirect('/campaign/visual-content/list-contents/')

    return render(request, 'register_contents.html', context)


@login_required(login_url='/login')
def deletecontent(request, id):

    if request.method == "POST":
        VisualContent.objects.filter(id=id).delete()
        messages.success(request, 'O conteúdo visual foi deletado com sucesso!')
        return redirect('/campaign/visual-content/list-contents/')


@login_required(login_url='/login')
def editcontent(request, id):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    visual_content = VisualContent.objects.get(id=id)

    if request.method == "GET":
        return render(request, 'edit_contents.html', {'visual_content': visual_content, 'type_user': user.type_user})

    name = request.POST.get('name')
    type_content = request.POST.get('type-content')
    content = request.FILES.get('content')
    status = request.POST.get('customRadio')

    if content:
        if content.content_type not in LIST_EXTENSION_IMAGES and content.content_type not in LIST_EXTENSION_VIDEO:
            messages.warning(request, 'Erro: O tipo de arquivo não é permitido!')
            return render(request, 'edit_contents.html', {'visual_content': visual_content, 'type_user': user.type_user})

        elif type_content == 'IE' and content.content_type in LIST_EXTENSION_VIDEO or type_content == 'ID' and content.content_type in LIST_EXTENSION_IMAGES:
            messages.warning(request, 'Erro: O tipo de arquivo para o conteúdo visual selecionado não é válido!')
            return render(request, 'edit_contents.html', {'visual_content': visual_content, 'type_user': user.type_user})
        else:
            visual_content.content = content

    visual_content.name = name
    visual_content.type_content = type_content
    visual_content.status = status
    visual_content.save()
    messages.success(request, 'Conteudo Visual editado com sucesso!')
    return redirect('/campaign/visual-content/list-contents/')


@login_required(login_url='/login')
def table_campaigns(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)

    if request.method == "GET":
        campaigns = Campaign.objects.all()
        return render(request, 'campaigns.html', {'campaigns': campaigns, 'type_user': user.type_user})


@login_required(login_url='/login')
def register_campaign(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    contents = VisualContent.objects.all()
    context = {'contents': contents, 'type_user': user.type_user, 'form': request.POST}

    if request.method == "GET":
        return render(request, 'register_campaigns.html', context)

    name = request.POST.get('name')
    type_regularity = request.POST.get('type_regularity')
    priority = request.POST.get('priority')
    initial_datetime = request.POST.get('initial_datetime')
    final_datetime = request.POST.get('final_datetime')
    visual_content = request.POST.getlist('visual_content')
    duration = request.POST.getlist('duration-visualcontent')
    status = request.POST.get('customRadio')
    current_date = str(date.today())
    current_time = datetime.now().strftime("%H:%M")
    initial_date = initial_datetime[0:10]
    initial_time = initial_datetime[11:]
    final_date = final_datetime[0:10]
    final_time = final_datetime[11:]

    if initial_date < current_date or final_date < current_date:
        messages.warning(request, 'Erro: A data Inicial e Final não pode ser menor que a data atual!')

    elif initial_date > final_date:
        messages.warning(request, 'Erro: A data Inicial não pode ser maior que a data final da campanha!')

    elif initial_date == final_date and initial_time > final_time:
        messages.warning(request, 'Erro: A Hora Final não pode ser menor do que a hora inicial da campanha!')

    elif initial_time < current_time:
        messages.warning(request, 'Erro: A Hora Inicial não pode ser menor do que a hora atual do sistema!')

    elif len(visual_content) == 0 or len(duration) == 0:
        messages.warning(request, 'Por favor, preencha com o conteúdo visual e a duração!')

    else:

        campaign = Campaign.objects.create(name=name, regularity=type_regularity, priority=priority, initial_datetime=initial_datetime, final_datetime=final_datetime, status=status)

        list_contents = []
        for content, duration in zip(visual_content, duration):
            list_contents.append(ContentCampaign(campaign_id=campaign.id, content_id=int(content), duration_visibility=duration))

        ContentCampaign.objects.bulk_create(list_contents)

        messages.success(request, 'A campanha foi enviada para aprovação!')
        return redirect('/campaign/list-campaigns/')

    return render(request, 'register_campaigns.html', context)


@login_required(login_url='/login')
def deletecampaign(request, id):

    if request.method == "POST":
        Campaign.objects.filter(id=id).delete()
        messages.success(request, 'A campanha foi deletada com sucesso!')
        return redirect('/campaign/list-campaigns/')


@login_required(login_url='/login')
def contentcampaign(request, id):

    dataJSON = {}

    if request.method == "GET":
        content_campaign = ContentCampaign.objects.filter(campaign_id=id)
        dict_contents = []
        for content_campaigns in content_campaign:
            visual_content = VisualContent.objects.get(
                id=content_campaigns.content_id
            )
            dataDictionary = {
                'id': visual_content.id,
                'name': visual_content.name,
                'type_content': visual_content.type_content,
                'content': visual_content.content.name,
            }
            dict_contents.append(dataDictionary)

        dataJSON = dumps(dict_contents)

    return JsonResponse({'data': dataJSON})


@login_required(login_url='/login')
def editcampaign(request, id):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    campaign = Campaign.objects.get(id=id)
    contents = VisualContent.objects.all()
    context = {'contents': contents, 'type_user': user.type_user}

    if request.method == "GET":
        content_campaign = ContentCampaign.objects.filter(
            campaign=campaign.id
        ).values('content')
        list_ids_visualcontent = []
        for content in content_campaign:
            list_ids_visualcontent.append(content['content'])

        campaign_contents = ContentCampaign.objects.filter(campaign=campaign.id)

        data = {
            'campaign': campaign,
            'type_user': user.type_user,
            'list_ids_visualcontent': list_ids_visualcontent,
            'visual_content': contents,
            'campaign_contents': campaign_contents,
        }

        return render(request, 'edit_campaign.html', data)

    name = request.POST.get('name')
    type_regularity = request.POST.get('type_regularity')
    priority = request.POST.get('priority')
    initial_datetime = request.POST.get('initial_datetime')
    final_datetime = request.POST.get('final_datetime')
    visual_content = request.POST.getlist('visual_content')
    duration = request.POST.getlist('duration-visualcontent')
    status = request.POST.get('customRadio')
    current_date = str(date.today())
    current_time = datetime.now().strftime("%H:%M")
    initial_date = initial_datetime[0:10]
    initial_time = initial_datetime[11:]
    final_date = final_datetime[0:10]
    final_time = final_datetime[11:]

    if initial_date < current_date or final_date < current_date:
        messages.warning(request, 'Erro: A data Inicial e Final não pode ser menor que a data atual!')

    elif initial_date > final_date:
        messages.warning(request, 'Erro: A data Inicial não pode ser maior que a data final da campanha!')

    elif initial_date == final_date and initial_time > final_time:
        messages.warning(request, 'Erro: A Hora Final não pode ser menor do que a hora inicial da campanha!')

    elif initial_time < current_time:
        messages.warning(request, 'Erro: A Hora Inicial não pode ser menor do que a hora atual do sistema!')

    else:

        ContentCampaign.objects.filter(campaign=campaign.id).delete()
        campaign.name = name
        campaign.regularity = type_regularity
        campaign.priority = priority
        campaign.initial_datetime = initial_datetime
        campaign.final_datetime = final_datetime

        list_contents = []
        for content, duration in zip(visual_content, duration):
            list_contents.append(
                ContentCampaign(campaign_id=campaign.id, content_id=int(content), duration_visibility=duration)
            )

        ContentCampaign.objects.bulk_create(list_contents)

        campaign.status = status
        campaign.approval = 1
        campaign.justify = ''
        campaign.save()
        messages.success(request, 'Campanha atualizada e enviada para aprovação!')
        return redirect('/campaign/list-campaigns/')

    return render(request, 'register_campaigns.html', context)


@login_required(login_url='/login')
def table_approval_campaigns(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    if user.type_user == 'O':
        raise PermissionDenied

    if request.method == "GET":
        campaigns = Campaign.objects.all()
        return render(request, 'approval_campaigns.html', {'campaigns': campaigns, 'type_user': user.type_user})


@login_required(login_url='/login')
def approved_campaign(request, id):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    if user.type_user == 'O':
        raise PermissionDenied

    if request.method == "POST":
        campaign = Campaign.objects.filter(id=id).first()
        campaign.approval = 2
        campaign.save()
        messages.success(request, 'A campanha foi aprovada com sucesso!')
        return redirect('/campaign/approval-campaigns/')


@login_required(login_url='/login')
def disapproved_campaign(request, id):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    if user.type_user == 'O':
        raise PermissionDenied

    if request.method == "POST":
        justify = request.POST.get('justify')
        campaign = Campaign.objects.filter(id=id).first()
        campaign.approval = 0
        campaign.justify = justify
        campaign.save()
        messages.success(request, 'A campanha foi reprovada com sucesso!')
        return redirect('/campaign/approval-campaigns/')
