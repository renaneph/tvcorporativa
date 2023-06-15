from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from user.models import UserProfile
from campaign.models import VisualContent, Campaign
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='/login')
def equipment(request):
    user = UserProfile.objects.get(djuser_id=request.user.id)
    count_campaigns = Campaign.objects.all().count()
    count_campaigns_approved = Campaign.objects.filter(approval=2).count()
    count_campaigns_disapproved = Campaign.objects.filter(approval=0).count()
    count_campaigns_approval = Campaign.objects.filter(approval=1).count()
    count_visualcontents = VisualContent.objects.all().count()
    count_users = User.objects.all().count()
    if request.method == "GET":
        context = {
            'type_user': user.type_user,
            'campaign': count_campaigns,
            'campaign_approved': count_campaigns_approved,
            'campaign_disapproved': count_campaigns_disapproved,
            'campaign_approval': count_campaigns_approval,
            'visualcontents': count_visualcontents,
            'users': count_users
        }
        return render(request, 'dashboard_home.html', context)
    else:
        return HttpResponse('método POST')
