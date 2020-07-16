from django import template

register = template.Library()


@register.filter(name='is_follower')
def is_follower(user, user2):
    #check if user is a follower of user2
    followers = user2.profile.followers.all()
    if(user in followers):
        return True
    else:
        return False
