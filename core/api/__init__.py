from core.views_pkg.auth import (
    RegisterView, LoginView, LogoutView, ChangePasswordView,
    PasswordResetRequestView, PasswordResetConfirmView,
)
from core.views_pkg.profile import UserProfileView, UpdateProfileView, NilsenProfileView
from core.views_pkg.notifications import (
    NotificationView, NotificationTriggerView,
    mark_all_notifications_as_read, clear_all_notifications,
)
from core.views_pkg.projects import ProjetViewSet, ImageProjetViewSet
from core.views_pkg.competences import CompetenceViewSet
from core.views_pkg.education import EducationViewSet
from core.views_pkg.formation import FormationViewSet
from core.views_pkg.experience import ExperienceViewSet
from core.views_pkg.awards import AwardViewSet
from core.views_pkg.languages import LangueViewSet
from core.views_pkg.ratings import RatingView
from core.views_pkg.visits import RecordVisit, TotalVisits, MonthlyVisitStats
from core.views_pkg.emails import EmailViewSet, EmailResponseViewSet, SendEmailView, HistoricMailListView
from core.views_pkg.facebook import FacebookList
from core.views_pkg.mylogin import MyLoginViewSet
from core.views_pkg.system import KeepAliveView, get_all_users

__all__ = [
    'RegisterView','LoginView','LogoutView','ChangePasswordView',
    'PasswordResetRequestView','PasswordResetConfirmView',
    'UserProfileView','UpdateProfileView','NilsenProfileView',
    'NotificationView','NotificationTriggerView',
    'mark_all_notifications_as_read','clear_all_notifications',
    'ProjetViewSet','ImageProjetViewSet','CompetenceViewSet',
    'EducationViewSet','ExperienceViewSet','AwardViewSet','LangueViewSet',
    'RatingView','RecordVisit','TotalVisits','MonthlyVisitStats',
    'EmailViewSet','EmailResponseViewSet','SendEmailView','HistoricMailListView',
    'FacebookList','KeepAliveView','get_all_users','MyLoginViewSet'
]

