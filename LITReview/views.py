from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import CreateAnUser, CreateATicket, CreateAReview, CreateAUserFollow, FollowAUser
from django.contrib.auth.models import User
from .models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("feed")
            else:
                return render(request, 'accounts/home.html', {"error": "connexion impossible"})
    else:
        return redirect("feed")
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == "POST":
        formcreateanuser = CreateAnUser(request.POST)
        if formcreateanuser.is_valid():
            username = formcreateanuser.cleaned_data['username']
            password = formcreateanuser.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect("login_page")
        else:
            pass
    else:
        formcreateanuser = CreateAnUser()
    return render(request, "accounts/register.html", {"form": formcreateanuser})


@login_required
def feed(request):
    users = UserFollows.objects.filter(user=request.user)
    reviewrecherche = [Review.objects.filter(user=user.followed_user) for user in users]
    ticketrecherche = [Ticket.objects.filter(user=user.followed_user) for user in users]
    reviewrecherche.append(Review.objects.filter(user=request.user))
    ticketrecherche.append(Ticket.objects.filter(user=request.user))
    newreview = []
    for ticketuser in Ticket.objects.filter(user=request.user):
        alreadydisplay = False
        for reviewquery in reviewrecherche:
            for review in reviewquery:
                if review.ticket == ticketuser:
                    alreadydisplay = True
        if not alreadydisplay:
            newreview = Review.objects.filter(ticket=ticketuser)
    reviewrecherche.append(newreview)
    aggregate = []
    ticket_used = []
    for review in reviewrecherche:
        if review:
            for r in review:
                ticket_used.append(r.ticket)
                aggregate.append({"type": "review",
                                  "obj": r})
    for ticket in ticketrecherche:
        if ticket:
            for t in ticket:
                if t in ticket_used:
                    used = True
                else:
                    used = False
                aggregate.append({"type": "ticket",
                                  "obj": t,
                                  "used": used})

    aggregate = sorted(aggregate, key=lambda item: item["obj"].time_created, reverse=True)
    return render(request, "accounts/feed.html", {"aggregate": aggregate})


@login_required
def makeaticket(request):
    if request.method == "POST":
        formticketmaking = CreateATicket(request.POST, request.FILES)
        if formticketmaking.is_valid():
            obj_ticket = formticketmaking.save(commit=False)
            obj_ticket.user = request.user
            obj_ticket.save()
            return redirect("feed")
        else:
            pass
    formticketmaking = CreateATicket()
    return render(request, "accounts/ticket.html", {"formticket": formticketmaking})


@login_required
def editaticket(request, pk_ticket):
    ticket = Ticket.objects.get(id=pk_ticket)
    formticketmaking = CreateATicket(initial={
        "title": ticket.title,
        "description": ticket.description,
        "image": ticket.image
    })
    if request.method == "POST":
        try:
            deleting = request.POST["image-clear"]
        except KeyError:
            deleting = False
        fomticket = CreateATicket(request.POST, request.FILES, instance=ticket)
        fomticket.save()
        return redirect("posts")
    return render(request, "accounts/ticket.html", {"formticket": formticketmaking,
                                                    "ticket": ticket})


@login_required
def makeareview(request):
    formticketmaking = CreateATicket()
    formreviewmaking = CreateAReview()
    if request.method == "POST":
        formticketmaking = CreateATicket(request.POST, request.FILES)
        formreviewmaking = CreateAReview(request.POST)
        if formticketmaking.is_valid():
            if formreviewmaking.is_valid():
                obj_ticket = formticketmaking.save(commit=False)
                obj_ticket.user = request.user
                obj_ticket.save()
                obj_review = formreviewmaking.save(commit=False)
                obj_review.user = request.user
                obj_review.ticket = obj_ticket
                obj_review.save()
                return redirect("feed")
            else:
                pass
        else:
            pass
    return render(request, "accounts/review.html", {"formticket": formticketmaking,
                                                    "formreview": formreviewmaking})


@login_required
def editareview(request, pk_review):
    review = Review.objects.get(id=pk_review)
    ticket = review.ticket
    formticketmaking = CreateATicket(instance=ticket)
    formreviewmaking = CreateAReview(instance=review)
    if request.method == "POST":
        formticket = CreateATicket(request.POST, request.FILES, instance=ticket)
        formticket.save()
        ticket.save()
        formreview = CreateAReview(request.POST, instance=review)
        formreview.save()
        return redirect("posts")
    return render(request, "accounts/review.html", {"formticket": formticketmaking,
                                                    "formreview": formreviewmaking,
                                                    "ticket": ticket})


@login_required
def posts(request):
    reviewrecheche = Review.objects.filter(user=request.user).order_by('-time_created')
    ticketrecherhe = Ticket.objects.filter(user=request.user).order_by('-time_created')
    aggregate = []

    for review in reviewrecheche:
        aggregate.append({"type": "review",
                          "obj": review})

    for ticket in ticketrecherhe:
        aggregate.append({"type": "ticket",
                          "obj": ticket})

    aggregate = sorted(aggregate, key=lambda item: item["obj"].time_created, reverse=True)
    return render(request, "accounts/post.html", {"aggregate": aggregate})


@login_required
def deletereview(request, pk_review):
    whichreviewt = Review.objects.get(id=pk_review)
    if request.user == whichreviewt.user:
        whichreviewt.delete()
    else:
        pass
    return redirect("posts", permanent=True)


@login_required
def deleteticket(request, pk_ticket):
    try:
        whichticket = Ticket.objects.get(id=pk_ticket)
        if request.user == whichticket.user:
            whichticket.delete()
        else:
            pass
    finally:
        pass
    return redirect("posts", permanent=True)


@login_required
def deconnection(request):
    logout(request)
    return redirect("login_page")


@login_required
def abonnements(request):
    if request.method == "POST":
        formabo = FollowAUser(request.POST)
        if formabo.is_valid():
            if not formabo.existing(userconnected=request.user):
                folling = User.objects.get(username=formabo.cleaned_data["following"])
                formfollow = CreateAUserFollow()
                obj = formfollow.save(commit=False)
                obj.user = request.user
                obj.followed_user = folling
                obj.save()
            else:
                pass
    else:
        formabo = FollowAUser()
    subs = [user_sub for user_sub in UserFollows.objects.filter(user=request.user)]
    followers = [follower for follower in UserFollows.objects.filter(followed_user=request.user)]
    return render(request, "accounts/following.html", {"subscriptions": subs,
                                                       "followers": followers,
                                                       "formulaire": formabo})


@login_required
def desabonnement(request, pk_user):
    whichuser = User.objects.get(id=pk_user)
    UserFollows.objects.get(user=request.user, followed_user=whichuser).delete()
    return redirect("following", permanent=True)


@login_required
def reviewed(request, pk_ticket):
    ticket = Ticket.objects.get(id=pk_ticket)
    formreviewmaking = CreateAReview()
    if request.method == "POST":
        formreviewmaking = CreateAReview(request.POST)
        if formreviewmaking.is_valid():
            obj_review = formreviewmaking.save(commit=False)
            obj_review.user = request.user
            obj_review.ticket = ticket
            obj_review.save()
            return redirect("feed")
        else:
            pass
    return render(request, "accounts/reviewed.html", {"ticket": ticket,
                                                      "formreview": formreviewmaking})


@login_required
def uniquereviewedit(request, pk_review):
    review = Review.objects.get(id=pk_review)
    ticket = review.ticket
    formreviewmaking = CreateAReview(initial={
        "headline": review.headline,
        "body": review.body,
        "rating": review.rating
    })
    if request.method == "POST":
        review.rating = request.POST["rating"]
        review.headline = request.POST["headline"]
        review.body = request.POST["body"]
        review.save()
        return redirect("posts")
    return render(request, "accounts/reviewed.html", {"ticket": ticket,
                                                      "formreview": formreviewmaking})
