from core.views_pkg.auth import (
    ChangePasswordView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
)
from core.views_pkg.awards import AwardViewSet
from core.views_pkg.competences import CompetenceViewSet
from core.views_pkg.cv import CVListView, CVView
from core.views_pkg.education import EducationViewSet
from core.views_pkg.emails import (
    EmailResponseViewSet,
    EmailViewSet,
    HistoricMailListView,
    SendEmailView,
)
from core.views_pkg.experience import ExperienceViewSet
from core.views_pkg.facebook import FacebookList
from core.views_pkg.formation import FormationViewSet
from core.views_pkg.languages import LangueViewSet
from core.views_pkg.mylogin import MyLoginViewSet
from core.views_pkg.notifications import (
    NotificationTriggerView,
    NotificationView,
    clear_all_notifications,
    mark_all_notifications_as_read,
)
from core.views_pkg.profile import NilsenProfileView, UpdateProfileView, UserProfileView
from core.views_pkg.projects import ImageProjetViewSet, ProjetViewSet
from core.views_pkg.prospecting import (
    MessageTemplateViewSet,
    ProspectAttachmentUploadView,
    ProspectAttachmentViewSet,
    ProspectMessagePreviewView,
    ProspectMessageSendView,
    ProspectMessageView,
    ProspectNoteViewSet,
    ProspectRatingView,
    ProspectStatsView,
    ProspectStatusView,
    ProspectViewSet,
)
from core.views_pkg.ratings import RatingView
from core.views_pkg.system import KeepAliveView, get_all_users
from core.views_pkg.visits import MonthlyVisitStats, RecordVisit, TotalVisits
from core.views_pkg.webauthn_auth import (
    WebAuthnCredentialListView,
    WebAuthnLoginBeginView,
    WebAuthnLoginCompleteView,
    WebAuthnRegisterBeginView,
    WebAuthnRegisterCompleteView,
)

__all__ = [
    "RegisterView",
    "LoginView",
    "LogoutView",
    "ChangePasswordView",
    "PasswordResetRequestView",
    "PasswordResetConfirmView",
    "UserProfileView",
    "UpdateProfileView",
    "NilsenProfileView",
    "NotificationView",
    "NotificationTriggerView",
    "mark_all_notifications_as_read",
    "clear_all_notifications",
    "ProjetViewSet",
    "ImageProjetViewSet",
    "CompetenceViewSet",
    "EducationViewSet",
    "ExperienceViewSet",
    "AwardViewSet",
    "LangueViewSet",
    "RatingView",
    "RecordVisit",
    "TotalVisits",
    "MonthlyVisitStats",
    "EmailViewSet",
    "EmailResponseViewSet",
    "SendEmailView",
    "HistoricMailListView",
    "FacebookList",
    "KeepAliveView",
    "get_all_users",
    "MyLoginViewSet",
    "CVView",
    "CVListView",
    "ProspectViewSet",
    "ProspectStatusView",
    "ProspectStatsView",
    "ProspectNoteViewSet",
    "ProspectMessageView",
    "ProspectMessageSendView",
    "ProspectMessagePreviewView",
    "MessageTemplateViewSet",
    "ProspectRatingView",
    "ProspectAttachmentUploadView",
    "ProspectAttachmentViewSet",
    # WebAuthn / Face ID
    "WebAuthnRegisterBeginView",
    "WebAuthnRegisterCompleteView",
    "WebAuthnLoginBeginView",
    "WebAuthnLoginCompleteView",
    "WebAuthnCredentialListView",
]
