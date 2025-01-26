from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    EducationViewSet, 
    UserProfileView, 
    ExperienceViewSet, 
    ProjetViewSet, 
    EmailViewSet,
    SendEmailView,
    HistoricMailListView,
    EmailResponseViewSet, 
    LangueViewSet,
    get_all_users,
    UpdateProfileView,
    PasswordResetRequestView, 
    PasswordResetConfirmView,
    ProjetViewSet, ImageProjetViewSet,
    CompetenceViewSet,
    FormationViewSet,
   
    AwardViewSet,
    RatingView,
    ChangePasswordView,
    NotificationView,
    # ChatbotView,
    RecordVisit,
    TotalVisits,
    MonthlyVisitStats,
    NotificationTriggerView,
    mark_all_notifications_as_read,
    clear_all_notifications

    )

from django.conf import settings
from django.conf.urls.static import static
from .views import NilsenProfileView


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('education/', EducationViewSet.as_view({'get': 'list', 'post': 'create'}), name='education-list-create'),
    path('education/<int:pk>/', EducationViewSet.as_view({'get': 'list','put': 'update', 'post': 'create'}), name='education-detail-update-delete'),
    path('experience/', ExperienceViewSet.as_view({'get': 'list', 'post': 'create'}), name='experience-list-create'),
    path('experience/<int:pk>/', ExperienceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='experience-detail-update-delete'),
    path('NilsenProfile/', NilsenProfileView.as_view(), name='user-profile'),
    path('competences/', CompetenceViewSet.as_view({'get': 'list', 'post': 'create'}), name='competence-list-create'),
    path('competences/<int:pk>/', CompetenceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='competence-detail-update-delete'),
    path('projets/', ProjetViewSet.as_view({'get': 'list', 'post': 'create'}), name='projet-list-create'),
    path('projets/<int:pk>/', ProjetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='projet-detail-update-delete'),

    path('formations/', FormationViewSet.as_view({'get': 'list', 'post': 'create'}), name='formation-list-create'),
    path('formations/<int:pk>/', FormationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='formation-detail-update-delete'),

    path('awards/', AwardViewSet.as_view({'get': 'list', 'post': 'create'}), name='award-list-create'),
    path('awards/<int:pk>/', AwardViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='award-detail-update-delete'),
    path('rating/', RatingView.as_view(), name='rating-create'),
    path('rating/<int:project_id>/', RatingView.as_view(), name='rating-detail'),

    path('notifications/', NotificationView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/mark-as-read/', NotificationView.as_view(), name='notification-mark-as-read'),
    path('notifications/trigger/', NotificationTriggerView.as_view(), name='notification-trigger'),
    path("notifications/mark-all-read/", mark_all_notifications_as_read, name="mark-all-read"),
    path("notifications/clear-all/", clear_all_notifications, name="clear-all-notifications"),

    path('images/', ImageProjetViewSet.as_view({'get': 'list', 'post': 'create'}), name='image-list-create'),
    path('images/<int:pk>/', ImageProjetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='image-detail-update-delete'),

    path('users/', get_all_users, name='get-all-users'),
   
    path('emails/', EmailViewSet.as_view({'get': 'list', 'post': 'create'}), name='email-list-create'),
    path('emails/<int:pk>/', EmailViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='email-detail-update-delete'),
    
    path('emails/<int:email_id>/responses/', EmailResponseViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('email-responses/<int:pk>/', EmailResponseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='emailresponse-detail-update-delete'),
    path('emails/<int:email_id>/responses/', EmailResponseViewSet.as_view({'get': 'list'}), name='email-responses-list'),
    path('mail_entreprise/', SendEmailView.as_view(), name='send-email'),
    path('historic-mails/', HistoricMailListView.as_view(), name='historic_mails'),
    path('langues/', LangueViewSet.as_view({'get': 'list', 'post': 'create'}), name='langue-list-create'),
    path('langues/<int:pk>/', LangueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='langue-detail-update-delete'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('record-visit/', RecordVisit.as_view(), name='record-visit'),
    path('total-visits/', TotalVisits.as_view(), name='total-visits'),
    path('monthly-visit-stats/', MonthlyVisitStats.as_view(), name='monthly-visit-stats'),
    ]
