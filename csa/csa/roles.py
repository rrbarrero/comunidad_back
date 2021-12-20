from rolepermissions.roles import AbstractUserRole

class Editor(AbstractUserRole):
    available_permissions = {
        'create_article': True,
        'create_comment': True,
        'create_post': True,
    }

class Moderator(AbstractUserRole):
    available_permissions = {
        'moderate_comment': True,
        'create_comment': True,
        'create_post': True,
    }

class Collaborator(AbstractUserRole):
    available_permissions = {
        'moderate_comment': True,
        'create_comment': True,
        'create_post': True,
    }

class CommunityUser(AbstractUserRole):
    available_permissions = {
        'create_comment': True,
        'create_post': True,
    }